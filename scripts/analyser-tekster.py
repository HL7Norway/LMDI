import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import requests

class FHIRProfileAnalyzer:
    def __init__(self):
        self.properties = ['short', 'definition', 'comment']
        self.profile_properties = ['description', 'purpose']
        self.base_resources_cache = {}

    def load_json_file(self, file_path: str) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Feil ved lesing av fil {file_path}: {str(e)}")
            return None

    def get_base_resource(self, base_url: str) -> dict:
        if base_url in self.base_resources_cache:
            return self.base_resources_cache[base_url]

        resource_type = base_url.split('/')[-1]
        
        local_path = f"base_resources/{resource_type}.json"
        if os.path.exists(local_path):
            base = self.load_json_file(local_path)
        else:
            try:
                api_url = f"http://hl7.org/fhir/R4/StructureDefinition-{resource_type}.json"
                response = requests.get(api_url)
                if response.status_code == 404:
                    api_url = f"http://hl7.org/fhir/R4/{resource_type}.profile.json"
                    response = requests.get(api_url)
                
                if response.status_code != 200:
                    print(f"Kunne ikke laste baseressurs: {resource_type} (HTTP {response.status_code})")
                    return None
                    
                base = response.json()
                
                with open(local_path, 'w', encoding='utf-8') as f:
                    json.dump(base, f, ensure_ascii=False, indent=2)
                    
            except Exception as e:
                print(f"Feil ved lasting av baseressurs {resource_type}: {str(e)}")
                return None

        self.base_resources_cache[base_url] = base
        return base

    def find_path_elements(self, profile: dict, path: str) -> List[dict]:
        """Finn alle elementer som matcher en gitt sti i profilen"""
        elements = []
        # Sjekk differential først
        if 'differential' in profile:
            for elem in profile['differential'].get('element', []):
                if elem.get('path', '') == path:
                    elements.append(elem)
        
        # Sjekk snapshot hvis ingen funnet i differential
        if not elements and 'snapshot' in profile:
            for elem in profile['snapshot'].get('element', []):
                if elem.get('path', '') == path:
                    elements.append(elem)
        
        return elements

    def find_slices(self, profile: dict, path: str) -> List[Tuple[str, dict]]:
        slices = []
        processed_paths = set()

        # Sjekk først i differential
        differential_elements = profile.get('differential', {}).get('element', [])
        for element in differential_elements:
            element_path = element.get('path', '')
            
            if not element_path.startswith(path):
                continue
                
            # Sjekk for direkte slice-definisjon (med kolon)
            if ':' in element_path and element_path not in processed_paths:
                slice_name = element_path.split(':')[-1]
                slices.append((element_path, element))
                processed_paths.add(element_path)
                continue
                
            # Sjekk for sliceName attributt
            slice_name = element.get('sliceName')
            if slice_name and element_path == path:
                slice_path = f"{path}:{slice_name}"
                if slice_path not in processed_paths:
                    slices.append((slice_path, element))
                    processed_paths.add(slice_path)
                continue
                
            # Sjekk for pattern
            if element_path == path:
                pattern_system = element.get('patternUri')
                if pattern_system:
                    # For identifier med pattern, bruk system-mønsteret for å finne slice-navnet
                    if '2.16.578.1.12.4.1.4.101' in pattern_system:
                        slice_path = f"{path}:ENH"
                    elif '2.16.578.1.12.4.1.4.102' in pattern_system:
                        slice_path = f"{path}:RESH"
                    else:
                        continue
                        
                    if slice_path not in processed_paths:
                        slices.append((slice_path, element))
                        processed_paths.add(slice_path)

        # Hvis ingen slices funnet i differential, sjekk snapshot
        if not slices and 'snapshot' in profile:
            snapshot_elements = profile.get('snapshot', {}).get('element', [])
            for element in snapshot_elements:
                element_path = element.get('path', '')
                if element_path.startswith(path + ':') and element_path not in processed_paths:
                    slices.append((element_path, element))
                    processed_paths.add(element_path)

        return sorted(slices, key=lambda x: x[0])

    def should_show_element(self, path: str, element_type: str, resource_type: str, element: dict) -> bool:
        if self.is_root_element(path, resource_type):
            return False
            
        parts = path.split('.')
        
        # Tillat elementer med slice-markør
        if len(parts) > 2 and not ':' in path:
            return False
            
        # Sjekk kardinalitet
        max_value = element.get('max', '')
        if max_value == '0':
            return False
        elif max_value.isdigit():
            if int(max_value) <= 0:
                return False
                
        return True

    def is_root_element(self, path: str, resource_type: str) -> bool:
        return path == resource_type

    def escape_markdown(self, text: str) -> str:
        if not text:
            return ''
            
        escaped = text
        escaped = escaped.replace('\\', '\\\\')
        escaped = escaped.replace('|', '\\|')
        special_chars = ['*', '_', '`', '[', ']', '(', ')', '#', '+', '-', '.', '!']
        for char in special_chars:
            escaped = escaped.replace(char, '\\' + char)
        escaped = escaped.replace('\n', '<br>')
        escaped = escaped.replace('\r', '')
        
        return escaped

    def format_value(self, value: str, base_value: str, is_slice: bool = False) -> str:
        if not value:
            return ''
            
        escaped_value = self.escape_markdown(value)
        
        # For slices eller når verdien er forskjellig fra base
        if is_slice or value != base_value:
            return f"**{escaped_value}**"
            
        return escaped_value

    def clean_element_name(self, element_name: str, resource_type: str) -> str:
        if element_name.startswith(f"{resource_type}."):
            return element_name[len(resource_type)+1:]
        return element_name

    def get_element_type(self, element: dict) -> str:
        if 'type' in element:
            if isinstance(element['type'], list):
                return element['type'][0].get('code', '')
            return element['type'].get('code', '')
        return ''

    def analyze_profile(self, file_path: str):
        profile = self.load_json_file(file_path)
        if not profile:
            return

        profile_name = self.escape_markdown(profile.get('name', ''))
        base_url = profile.get('baseDefinition', '')
        
        if not base_url:
            print(f"Ingen baseDefinition funnet i profilen: {file_path}")
            return
            
        base_type = base_url.split('/')[-1]

        base_resource = self.get_base_resource(base_url)
        if not base_resource:
            return

        print(f"# {profile_name} : {base_type}\n")

        print("## Profilinformasjon\n")
        print("| Egenskap | Verdi |")
        print("|-----------|-------|")
        for prop in self.profile_properties:
            value = profile.get(prop, '')
            formatted_value = self.escape_markdown(value)
            print(f"| {prop.capitalize()} | {formatted_value} |")
        print("\n## Elementinformasjon\n")

        base_elements = {elem.get('path', ''): elem 
                        for elem in base_resource.get('snapshot', {}).get('element', [])}
        
        # Kombiner snapshot og differential
        profile_elements = {}
        if 'snapshot' in profile:
            profile_elements.update({elem.get('path', ''): elem 
                                  for elem in profile.get('snapshot', {}).get('element', [])})
        if 'differential' in profile:
            profile_elements.update({elem.get('path', ''): elem 
                                  for elem in profile.get('differential', {}).get('element', [])})

        print("| Elementnavn | Type | Tekst |")
        print("|------------------|-----------|-----------------------------------------------|")

        processed_paths = set()

        for path in sorted(set(base_elements.keys()) | set(profile_elements.keys())):
            if path in processed_paths:
                continue

            base_elem = base_elements.get(path, {})
            profile_elem = profile_elements.get(path, {})
            
            element_type = self.get_element_type(profile_elem) or self.get_element_type(base_elem)
            current_elem = profile_elem if profile_elem else base_elem

            if not self.should_show_element(path, element_type, base_type, current_elem):
                continue

            # Vis hovedelement
            element_name = self.clean_element_name(path, base_type)
            
            # Vis hovedinformasjon
            first_row = True
            for prop in self.properties:
                base_value = base_elem.get(prop, '')
                profile_value = profile_elem.get(prop, '')
                
                value = profile_value if profile_value else base_value
                formatted_value = self.format_value(value, base_value)
                
                if first_row:
                    print(f"| {element_name} | {prop.capitalize()} | {formatted_value} |")
                    first_row = False
                else:
                    print(f"| | {prop.capitalize()} | {formatted_value} |")

            # Finn og vis slices
            slices = self.find_slices(profile, path)
            for slice_path, slice_elem in slices:
                slice_name = slice_path.split(':')[-1] if ':' in slice_path else ''
                full_slice_name = f"{element_name}:{slice_name}"
                
                first_row = True
                for prop in self.properties:
                    value = slice_elem.get(prop, '')
                    formatted_value = self.format_value(value, '', is_slice=True)
                    
                    if first_row:
                        print(f"| {full_slice_name} | {prop.capitalize()} | {formatted_value} |")
                        first_row = False
                    else:
                        print(f"| | {prop.capitalize()} | {formatted_value} |")
                
                processed_paths.add(slice_path)

            processed_paths.add(path)

def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Angi sti til profil eller katalog (standard: 'profiles'): ").strip() or "profiles"

    os.makedirs("base_resources", exist_ok=True)

    analyzer = FHIRProfileAnalyzer()
    
    if os.path.isfile(path):
        analyzer.analyze_profile(path)
    elif os.path.isdir(path):
        for file_path in Path(path).glob('*.json'):
            print(f"\nAnalyserer {file_path}:\n")
            analyzer.analyze_profile(str(file_path))
    else:
        print(f"Feil: Kunne ikke finne fil eller katalog: {path}")

if __name__ == "__main__":
    main()