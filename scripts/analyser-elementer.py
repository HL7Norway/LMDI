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

RESOURCE_NAME_MAPPING = {
    'lmdi-bundle': 'LegemiddelregisterBundle',
    'lmdi-condition': 'Diagnose',
    'lmdi-encounter': 'Episode',
    'lmdi-episodeofcare': 'Institusjonsopphold',
    'lmdi-medication': 'Legemiddel',
    'lmdi-medicationadministration': 'Legemiddeladministrering',
    'lmdi-medicationrequest': 'Legemiddelrekvirering',
    'lmdi-organization': 'Organisasjon',
    'lmdi-patient': 'Pasient',
    'lmdi-practitioner': 'Helsepersonell',
    'lmdi-practitionerrole': 'Helsepersonellrolle'
}


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ElementInfo:
    path: str
    type: str
    binding_name: str
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
        self.base_resources_cache = {}

    def _get_resource_name(self, resource_id: str) -> str:
        """Oversetter resource ID til navn hvis det finnes i mappingen."""
        return RESOURCE_NAME_MAPPING.get(resource_id, resource_id)

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

    def get_base_resource(self, base_url: str) -> Optional[dict]:
        """
        Last ned (eller hent fra cache) en baseressurs for et gitt base_url.
        Søker først lokalt i base_resources/<resource_type>.json, deretter
        i http://hl7.org/fhir/R4/StructureDefinition-<resource_type>.json osv.
        """
        if not base_url:
            return None

        if base_url in self.base_resources_cache:
            return self.base_resources_cache[base_url]

        resource_type = base_url.split('/')[-1]  # f.eks "Organization"

        local_path = f"base_resources/{resource_type}.json"
        if os.path.exists(local_path):
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    base = json.load(f)
                self.base_resources_cache[base_url] = base
                return base
            except Exception as e:
                logger.warning(f"Feil ved lasting av baseressurs lokalt for {resource_type}: {e}")

        try:
            api_url = f"http://hl7.org/fhir/R4/StructureDefinition-{resource_type}.json"
            response = requests.get(api_url)
            if response.status_code == 404:
                api_url = f"http://hl7.org/fhir/R4/{resource_type}.profile.json"
                response = requests.get(api_url)

            if response.status_code != 200:
                logger.warning(f"Kunne ikke laste baseressurs: {resource_type} (HTTP {response.status_code})")
                return None

            base = response.json()

            os.makedirs("base_resources", exist_ok=True)
            with open(local_path, 'w', encoding='utf-8') as f:
                json.dump(base, f, ensure_ascii=False, indent=2)

            self.base_resources_cache[base_url] = base
            return base

        except Exception as e:
            logger.warning(f"Feil ved lasting av baseressurs {resource_type}: {e}")
            return None

    def get_element_type(self, element: dict) -> str:
        """Extract and format element type information."""
        try:
            if not element or 'type' not in element:
                return ""

            types = []
            element_types = element['type']

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
        """Extract profile names from URLs and translate to readable names."""
        profile_ids = [url.split('/')[-1] for url in urls]
        return [self._get_resource_name(profile_id) for profile_id in profile_ids]

    def get_valueset_binding(self, element: dict) -> str:
        """Format ValueSet binding information."""
        binding = element.get('binding', {})
        if not binding:
            return ""

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

            base_resource = self.get_base_resource(base_url)

            md = []

            profile_name = self._get_resource_name(profile.get('name', 'Unknown Profile'))
            base_name = self._get_resource_name(base_url.split('/')[-1] if base_url else 'Unknown Base')

            md.append(f"# {profile_name} : {base_name}\n")

            elements = self._process_elements(profile, base_resource)

            md.extend(self._generate_tables(elements))

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
            differential = profile.get('differential', {}).get('element', [])
            snapshot = self._generate_snapshot(differential, base_resource)

        for element in snapshot:
            if element['path'] == profile['type']:  # skip resource element itself
                continue

            element_id = element.get('id', '')
            path = element['path']

            if ':' in element_id:
                base_path, slice_name = element_id.rsplit(':', 1)
                formatted_path = f"{self._format_path(path, profile['type'])}:{slice_name}"
            else:
                formatted_path = self._format_path(path, profile['type'])

            binding_name = ""
            if 'binding' in element:
                for ext in element['binding'].get('extension', []):
                    if ext.get('url') == 'http://hl7.org/fhir/StructureDefinition/elementdefinition-bindingName':
                        binding_name = ext.get('valueString', '')
                        break

            element_info = ElementInfo(
                path=formatted_path,
                type=self.get_element_type(element),
                binding_name=binding_name,
                cardinalityProfile=f"{element.get('min', '0')}..{element.get('max', '*')}",
                cardinalityBase=self._get_base_cardinality(element, base_resource),
                slicing=self.format_slicing(element),
                valueSetBinding=self.get_valueset_binding(element),
                attributes=self.get_attributes(element)
            )
            elements.append(element_info)

        return self._sort_elements(elements)

    def _sort_elements(self, elements: List[ElementInfo]) -> List[ElementInfo]:
        """Sorter elementene alfabetisk etter path."""
        return sorted(elements, key=lambda e: e.path)

    def _generate_tables(self, elements: List[ElementInfo]) -> List[str]:
        """Generate all required Markdown tables."""
        kept, removed = self._split_removed_elements(elements)

        tables = []

        top_level_kept = [e for e in kept if '.' not in e.path]
        tables.append("## Elementer")
        tables.extend(self._generate_element_table(top_level_kept))

        tables.append("\n## All Elements\n")
        tables.extend(self._generate_element_table(kept))

        tables.append("\n## Removed Elements\n")
        tables.extend(self._generate_removed_elements_table(removed))

        return tables

    def _generate_element_table(self, elements: List[ElementInfo]) -> List[str]:
        """Generate a Markdown table for elements."""
        table = [
            "| Element | Type | Profile | Base |",
            "|---------|------|---------|------|"
        ]

        for element in elements:
            if element.cardinalityProfile == '0..0':
                continue

            if element.cardinalityProfile != element.cardinalityBase:
                cardinalityProfile = f"**{element.cardinalityProfile}**"
            else:
                cardinalityProfile = element.cardinalityProfile

            # Escaper '|' tegnet i type-kolonnen ved å erstatte det med '\|'
            type_column = element.type.replace('|', '\\|')
            if element.binding_name:
                type_column = f"{type_column}<br/> Binding: {element.binding_name}"

            table.append(
                f"| {element.path} | {type_column} | {cardinalityProfile} | "
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

    def _format_path(self, path: str, resource_type: str) -> str:
        """Format element path according to specifications."""
        if path.startswith(f"{resource_type}."):
            path = path[len(resource_type) + 1:]
        if len(path) > 100:
            return "..." + path[-40:]
        return path

    def _get_base_cardinality(self, element: dict, base_resource: Optional[dict]) -> str:
        """Get cardinality from base resource."""
        if not base_resource:
            return ""

        base_elements = base_resource.get('snapshot', {}).get('element', [])
        element_path = element['path']

        # Prøv eksakt match:
        for base_element in base_elements:
            if base_element['path'] == element_path:
                return f"{base_element.get('min', '0')}..{base_element.get('max', '*')}"

        # Hvis nested element, sjekk delvis match som en fallback:
        if '.' in element_path:
            base_path_parts = element_path.split('.')
            for base_element in base_elements:
                base_element_path = base_element['path'].split('.')
                if all(part in base_element_path for part in base_path_parts):
                    return f"{base_element.get('min', '0')}..{base_element.get('max', '*')}"

        return "0..1"  # fallback

    def _generate_snapshot(self, differential: List[dict], base: dict) -> List[dict]:
        """Generate snapshot from differential and base resource (for simplicity)."""
        base_elements = {e['path']: e for e in base.get('snapshot', {}).get('element', [])}
        result = []

        for element in differential:
            path = element['path']
            if path in base_elements:
                # Merge base og differential
                merged = {**base_elements[path], **element}
                result.append(merged)
            else:
                # Nytt element
                result.append(element)

        return result

    def _split_removed_elements(self, elements: List[ElementInfo]) -> (List[ElementInfo], List[ElementInfo]):
        """
        Returnerer to lister: (kept, removed).
        - removed inneholder kun de elementene som har cardinalityProfile == '0..0' (altså "fjernede rot-elementer").
        - barne-elementer (path som starter med "<forelder>." eller "<forelder>:") blir helt skjult (er verken i kept eller removed).
        """

        # 1) Finn alle "rot-elementer" som eksplisitt har 0..0
        removed_explicit = [e for e in elements if e.cardinalityProfile == '0..0']

        # 2) Finn alle under-elementer/slices av disse fjernede elementene
        #    Disse vil vi utelukke fra "kept" og "removed" (helt skjult).
        hidden_paths = set()
        for elem in removed_explicit:
            # Legg til selve element.path i removed-settet:
            hidden_paths.add(elem.path)

            # Søk etter barne-elementer med path som starter på "<elem.path>." eller "<elem.path>:"
            prefix_dot = elem.path + '.'
            prefix_slice = elem.path + ':'
            for other in elements:
                if other.path.startswith(prefix_dot) or other.path.startswith(prefix_slice):
                    hidden_paths.add(other.path)

        # 3) Del i "fjernet" (bare de eksplisitte 0..0-elementene), mens barne-elementer ikke listes
        removed = [e for e in removed_explicit]

        # 4) kept er alle elementer som ikke ligger i hidden_paths
        kept = [e for e in elements if e.path not in hidden_paths]

        return (kept, removed)

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