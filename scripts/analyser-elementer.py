#!/usr/bin/env python3
import json
import os
import sys
from typing import Dict, List, Optional, Set, Tuple
from pathlib import Path
import requests
from dataclasses import dataclass
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ElementInfo:
    path: str
    type: str
    cardinalityProfile: str
    cardinalityBase: str
    slicing: str
    valueSetBinding: str
    attributes: str

class FHIRProfileAnalyzer:
    def __init__(self):
        self.cache = {}
        self.max_retries = 3
        self.timeout = 30

    def load_resource(self, path: str) -> dict:
        """Load a FHIR StructureDefinition from file or URL."""
        try:
            if urlparse(path).scheme in ('http', 'https'):
                for attempt in range(self.max_retries):
                    try:
                        response = requests.get(path, timeout=self.timeout)
                        response.raise_for_status()
                        return response.json()
                    except requests.RequestException as e:
                        if attempt == self.max_retries - 1:
                            raise
                        logger.warning(f"Attempt {attempt + 1} failed: {e}")
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading resource from {path}: {e}")
            raise

    def get_element_type(self, element: dict) -> str:
        """Extract and format element type information."""
        try:
            if not element or 'type' not in element:
                return ""

            types = []
            element_types = element['type']
            
            # Handle case where type might be a string instead of list
            if isinstance(element_types, str):
                element_types = [{'code': element_types}]
            elif isinstance(element_types, dict):
                element_types = [element_types]
                
            for t in element_types:
                if not isinstance(t, dict):
                    logger.warning(f"Unexpected type format: {t}")
                    continue
                    
                code = t.get('code', '')
                if not code:
                    continue

                if code == 'Reference':
                    target_profiles = t.get('targetProfile', [])
                    if isinstance(target_profiles, str):
                        target_profiles = [target_profiles]
                    if target_profiles:
                        types.append(f"Reference({' | '.join(self._get_profile_names(target_profiles))})")
                    else:
                        types.append("Reference")
                elif code == 'Extension':
                    url = ''
                    if isinstance(element.get('definition'), dict):
                        url = element['definition'].get('url', '')
                    elif isinstance(element.get('url'), str):
                        url = element['url']
                    types.append(f"Extension ({url}{'*' if self._is_custom_extension(url) else ''})")
                else:
                    types.append(code.replace('http://hl7.org/fhirpath/System.', ''))

            return ' | '.join(types)
            
        except Exception as e:
            logger.error(f"Error processing element type: {e}")
            logger.error(f"Element: {json.dumps(element, indent=2)}")
            return "Error processing type"

    def _is_custom_extension(self, url: str) -> bool:
        """Check if an extension is custom (non-HL7)."""
        return not url.startswith('http://hl7.org/')

    def _get_profile_names(self, urls: List[str]) -> List[str]:
        """Extract profile names from URLs."""
        return [url.split('/')[-1] for url in urls]

    def get_valueset_binding(self, element: dict) -> str:
        """Format ValueSet binding information."""
        binding = element.get('binding', {})
        if not binding:
            return ""

        # Handle both string valueSet and object valueSet formats
        valueset = binding.get('valueSet', {})
        if isinstance(valueset, str):
            url = valueset
            display = ''
            version = ''
        else:
            url = valueset.get('url', '')
            display = valueset.get('display', '')
            version = valueset.get('version', '')

        strength = binding.get('strength', '')

        if not any([display, url, strength]):
            return ""

        binding_str = []
        if display:
            binding_str.append(display)
        if url:
            url_str = f"({url}"
            if version:
                url_str += f", {version}"
            url_str += ")"
            binding_str.append(url_str)
        if strength:
            binding_str.append(f"[{strength}]")

        return " ".join(binding_str)

    def get_attributes(self, element: dict) -> str:
        """Collect and format element attributes."""
        attrs = []
        if element.get('mustSupport'):
            attrs.append('MS')
        if element.get('isModifier'):
            attrs.append('?!')
        if element.get('isSummary'):
            attrs.append('SU')
        if 'fixed' in element:
            attrs.append('F')
        if element.get('extension'):
            attrs.append('E')
        return ' '.join(attrs)

    def format_slicing(self, element: dict) -> str:
        """Format slicing information."""
        slicing = element.get('slicing', {})
        if not slicing:
            return ""

        discriminator = ', '.join(f"{d['type']} on {d['path']}" 
                                for d in slicing.get('discriminator', []))
        name = slicing.get('name', '')
        rules = slicing.get('rules', '')
        ordered = 'ordered' if slicing.get('ordered') else 'unordered'

        return f"{name} ({discriminator}, {rules}, {ordered})"

    def analyze_profile(self, profile_path: str) -> str:
        """Analyze a FHIR StructureDefinition and generate Markdown output."""
        try:
            profile = self.load_resource(profile_path)
            logger.debug(f"Loaded profile: {json.dumps(profile, indent=2)}")

            base_url = profile.get('baseDefinition', '')
            logger.debug(f"Base URL: {base_url}")

            base_resource = None
            if base_url:
                try:
                    base_resource = self.load_resource(base_url)
                    logger.debug(f"Loaded base resource: {json.dumps(base_resource, indent=2)}")
                except Exception as e:
                    logger.warning(f"Could not load base resource {base_url}: {e}")

            # Generate markdown
            md = []
            
            # Extract name safely
            profile_name = profile.get('name', 'Unknown Profile')
            base_name = base_url.split('/')[-1] if base_url else 'Unknown Base'
            
            md.append(f"# {profile_name} : {base_name}\n")
            
            # Process elements
            elements = self._process_elements(profile, base_resource)
            
            # Generate tables
            md.extend(self._generate_tables(elements))
            
            # Add attribute codes description
            md.extend(self._generate_attribute_codes())
            
            return '\n'.join(md)

        except Exception as e:
            logger.error(f"Error analyzing profile {profile_path}: {e}")
            logger.error("Exception details:", exc_info=True)
            raise

    def _process_elements(self, profile: dict, base_resource: Optional[dict]) -> List[ElementInfo]:
        """Process all elements in the profile."""
        elements = []
        snapshot = profile.get('snapshot', {}).get('element', [])
        
        if not snapshot and base_resource:
            # Generate snapshot from differential
            differential = profile.get('differential', {}).get('element', [])
            snapshot = self._generate_snapshot(differential, base_resource)

        for element in snapshot:
            if element['path'] == profile['type']:  # Skip resource element itself
                continue

            if element.get('max') == '0':  # Skip removed elements
                continue

            # Create ElementInfo object
            element_info = ElementInfo(
                path=self._format_path(element['path'], profile['type']),
                type=self.get_element_type(element),
                cardinalityProfile=f"{element.get('min', '0')}..{element.get('max', '*')}",
                cardinalityBase=self._get_base_cardinality(element, base_resource),
                slicing=self.format_slicing(element),
                valueSetBinding=self.get_valueset_binding(element),
                attributes=self.get_attributes(element)
            )
            elements.append(element_info)

        return self._sort_elements(elements)

    # alfabetisk innenfor hver gruppe
    # def _sort_elements(self, elements: List[ElementInfo]) -> List[ElementInfo]:
    #     """Sort elements according to specified grouping rules."""
    #     def get_group(element: ElementInfo) -> int:
    #         path = element.path
    #         if any(core in path for core in ['id', 'meta']):
    #             return 1
    #         if 'extension' in path:
    #             return 3
    #         return 2

    #     return sorted(elements, key=lambda e: (get_group(e), e.path))

    def _sort_elements(self, elements: List[ElementInfo]) -> List[ElementInfo]:
        """Sorter elementene alfabetisk etter path."""
        return sorted(elements, key=lambda e: e.path)

    def _generate_tables(self, elements: List[ElementInfo]) -> List[str]:
        """Generate all required Markdown tables."""
        tables = []
        
        # Complex types table
        tables.append("## Elementer")
        tables.extend(self._generate_element_table(
            [e for e in elements if '.' not in e.path]))
        
        # All elements table
        tables.append("\n## All Elements\n")
        tables.extend(self._generate_element_table(elements))
        
        # Removed elements table
        tables.append("\n## Removed Elements\n")
        tables.extend(self._generate_removed_elements_table(
            [e for e in elements if e.cardinalityProfile == '0..0']))
        
        return tables

    def _generate_element_table(self, elements: List[ElementInfo]) -> List[str]:
        """Generate a Markdown table for elements."""
        table = [
            "| Element | Type | Profile | Base |",
            "|---------|------|---------|------|"
        ]
        
        for element in elements:
            table.append(
                f"| {element.path} | {element.type} | {element.cardinalityProfile} | "
                f"{element.cardinalityBase} | "
            )
        
        return table

    def _generate_removed_elements_table(self, elements: List[ElementInfo]) -> List[str]:
        """Generate a Markdown table for removed elements."""
        if not elements:
            return ["No removed elements."]
            
        table = [
            "| Element | Description |",
            "|---------|-------------|"
        ]
        
        for element in elements:
            table.append(f"| {element.path} | {element.type} |")
            
        return table

    def _generate_attribute_codes(self) -> List[str]:
        """Generate attribute codes description table."""
        return [
            "\n## Attribute Codes\n",
            "| Code | Description |",
            "|------|-------------|",
            "| MS | Must Support |",
            "| ?! | Is Modifier |",
            "| SU | Is Summary |",
            "| F | Fixed Value |",
            "| E | Has Extensions |"
        ]

    def _format_path(self, path: str, resource_type: str) -> str:
        """Format element path according to specifications."""
        # Remove resource name prefix
        if path.startswith(f"{resource_type}."):
            path = path[len(resource_type) + 1:]

        # Truncate if necessary
        if len(path) > 100:
            return "..." + path[-40:]

        return path

    def _get_base_cardinality(self, element: dict, base_resource: Optional[dict]) -> str:
        """Get cardinality from base resource."""
        if not base_resource:
            return ""

        base_elements = base_resource.get('snapshot', {}).get('element', [])
        for base_element in base_elements:
            if base_element['path'] == element['path']:
                return f"{base_element.get('min', '0')}..{base_element.get('max', '*')}"

        return ""

    def _generate_snapshot(self, differential: List[dict], base: dict) -> List[dict]:
        """Generate snapshot from differential and base resource."""
        # This is a simplified version - in practice, you'd need more complex
        # snapshot generation logic
        base_elements = {e['path']: e for e in base.get('snapshot', {}).get('element', [])}
        result = []

        for element in differential:
            path = element['path']
            if path in base_elements:
                # Merge base and differential
                merged = {**base_elements[path], **element}
                result.append(merged)
            else:
                # New element
                result.append(element)

        return result

def main():
    """Main function to handle command line operation."""
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Enter path to FHIR StructureDefinition or directory: ").strip()

    if not path:
        path = "profiles"

    analyzer = FHIRProfileAnalyzer()

    try:
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith('.json'):
                    file_path = os.path.join(path, filename)
                    print(f"\nAnalyzing {filename}...")
                    print(analyzer.analyze_profile(file_path))
        else:
            print(analyzer.analyze_profile(path))

    except FileNotFoundError:
        print(f"Error: Path '{path}' not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()