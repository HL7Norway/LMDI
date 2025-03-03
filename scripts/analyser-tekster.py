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

    def get_base_elements(self, base_resource: dict) -> dict:
        """
        Bygger en dictionary med nøkkel = path og verdi = liste over alle base-elementene
        for den pathen.
        """
        elements = {}
        for elem in base_resource.get('snapshot', {}).get('element', []):
            path = elem.get('path', '')
            if not path:
                continue
            if path not in elements:
                elements[path] = []
            elements[path].append(elem)
        return elements

    def get_base_text(self, base_elements: dict, path: str, prop: str) -> str:
        """
        Returnerer verdien for en gitt egenskap (prop) fra det første base-elementet
        for en gitt path som har en definert verdi.
        """
        elems = base_elements.get(path, [])
        for elem in elems:
            val = elem.get(prop, '')
            if val:
                return val
        return ''



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
    
    def find_path_elements(self, profile: dict, path: str, include_slices: bool = True) -> List[dict]:
        """Find all elements that match a given path in the profile"""
        elements = []
        
        # Check differential first
        if 'differential' in profile:
            for elem in profile['differential'].get('element', []):
                elem_path = elem.get('path', '')
                # If we don't want slices, skip elements with slice names
                if not include_slices and ':' in elem_path:
                    continue
                if elem_path == path:
                    elements.append(elem)
        
        # Check snapshot if none found in differential
        if not elements and 'snapshot' in profile:
            for elem in profile['snapshot'].get('element', []):
                elem_path = elem.get('path', '')
                # If we don't want slices, skip elements with slice names
                if not include_slices and ':' in elem_path:
                    continue
                if elem_path == path:
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

    def is_in_differential(self, path: str, profile: dict) -> bool:
        """Sjekker om et element er oppført i differential i profilen."""
        differential_elements = profile.get('differential', {}).get('element', [])
        for elem in differential_elements:
            if elem.get('path') == path:
                return True
        return False

    def has_modified_sub_element(self, path: str, profile: dict) -> bool:
        """Sjekker om noen under-elementer av path er oppført i differential."""
        differential_elements = profile.get('differential', {}).get('element', [])
        
        # Sjekk om noen elementer starter med 'path.' (under-elementer)
        for elem in differential_elements:
            elem_path = elem.get('path', '')
            if elem_path.startswith(path + '.'):
                return True
        return False



    def should_show_element(self, path: str, element_type: str, resource_type: str, 
                            profile_elements: dict, base_elements: dict) -> bool:
        """
        Bestemmer om et element (gitt full path, f.eks. "Medication.code.coding")
        skal vises i tabellen.
        
        - Toppelementer (Resource.<element>) vises alltid.
        - For andre elementer:
          * Dersom differential har en oppføring for full path med overstyrt tekst (non‑tom short, definition eller comment), vis den.
          * Dersom differential kun er til stede for slicing (ingen overstyrte tekster),
            skal den generelle raden skjules – UNLESS base‑teksten (fra baseressursen) faktisk er definert.
          * Dersom ingen direkte endringer er gjort, men noen under‑elementer (med path som starter med "path.") er modifisert, vis forelderen.
        """
        profile = profile_elements.get('profile', {})

        # 1. Toppelementer: resourceType + ett punkt vises alltid.
        if path.startswith(resource_type + ".") and path.count('.') == 1:
            return True

        # 2. Se etter differentialoppføringer (uten slices)
        profile_elems = self.find_path_elements(profile, path, include_slices=False)
        if profile_elems:
            # Hvis en av oppføringene har en overstyrt tekst, vis elementet.
            for elem in profile_elems:
                for prop in self.properties:
                    if elem.get(prop, '').strip():
                        return True
            # Hvis det finnes differentialoppføringer uten overstyrt tekst,
            # sjekk om basen faktisk har definert tekst for noen egenskaper.
            for prop in self.properties:
                if self.get_base_text(base_elements, path, prop).strip():
                    return True
            # Dersom differentialoppføringer finnes og det også finnes slices,
            # undertrykk den generelle raden.
            if self.find_slices(profile, path):
                return False

        # 3. Dersom ingen direkte differentialoppføringer finnes, men noen under-elementer er modifisert, vis forelderen.
        if self.has_modified_sub_element(path, profile):
            return True

        return False



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
                type_code = element['type'][0].get('code', '')
            else:
                type_code = element['type'].get('code', '')
                
            # Fjern "http://hl7.org/fhirpath/System." prefikset hvis det eksisterer
            if type_code.startswith('http://hl7.org/fhirpath/System.'):
                return type_code.replace('http://hl7.org/fhirpath/System.', '')
                
            return type_code
        return ''

    def format_binding(self, binding: dict) -> str:
        if not binding:
            return ''
            
        # Hent binding name fra extension
        binding_name = ''
        if 'extension' in binding:
            for ext in binding['extension']:
                if ext.get('url') == 'http://hl7.org/fhir/StructureDefinition/elementdefinition-bindingName':
                    binding_name = ext.get('valueString', '')
                    break
        
        # Capitalize strength
        strength = binding.get('strength', '')
        if strength:
            strength = strength[0].upper() + strength[1:]
        
        # Escape alle verdier individuelt før de kombineres
        strength = self.escape_markdown(strength)
        binding_name = self.escape_markdown(binding_name)
        value_set = self.escape_markdown(binding.get('valueSet', ''))
        description = self.escape_markdown(binding.get('description', ''))
        
        # Konstruer binding tekst
        binding_text = f"{strength} binding: "
        
        # Legg til binding name og valueSet
        if binding_name and value_set:
            binding_text += f"[{binding_name}]({value_set})"
        elif value_set:
            binding_text += f"[{value_set}]({value_set})"
            
        # Legg til description
        if description:
            binding_text += f": <br> {description}"

        return binding_text


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

        # Bygg en dictionary over base-elementer med path som nøkkel
        base_elements = self.get_base_elements(base_resource)
        print("| Elementnavn | Egenskap | Tekst |")
        print("|------------------|-----------|-----------------------------------------------|")

        processed_paths = set()
        # Samle alle paths fra både basen og profilen
        all_paths = sorted(
            set(base_elements.keys()) |
            {elem.get('path', '') for elem in profile.get('snapshot', {}).get('element', [])} |
            {elem.get('path', '') for elem in profile.get('differential', {}).get('element', [])}
        )

        for path in all_paths:
            if path in processed_paths or not path:
                continue

            # Hent base-elementer (bruker den første for visning)
            base_elem_list = base_elements.get(path, [])
            base_elem = base_elem_list[0] if base_elem_list else {}

            # Hent et tilsvarende profile-element (uten slice-navn)
            profile_elem_base = None
            if 'differential' in profile:
                profile_elem_base = next(
                    (elem for elem in profile['differential'].get('element', [])
                    if elem.get('path') == path and ':' not in elem.get('path', '')),
                    None
                )
            if not profile_elem_base and 'snapshot' in profile:
                profile_elem_base = next(
                    (elem for elem in profile['snapshot'].get('element', [])
                    if elem.get('path') == path and ':' not in elem.get('path', '')),
                    None
                )

            # Hvis profilen definerer slicing for dette elementet,
            # sjekk om noen av overstyringsegenskapene er satt.
            # Hvis ikke, bruk baseteksten (dvs. ignorer profile-oppføringen).
            if profile_elem_base and 'slicing' in profile_elem_base:
                if not any(profile_elem_base.get(prop, '').strip() for prop in self.properties):
                    profile_elem_base = None

            # Bestem om elementet skal vises
            element_type = self.get_element_type(profile_elem_base if profile_elem_base else base_elem)
            if not self.should_show_element(path, element_type, base_type, {'profile': profile}, base_elements):
                continue

            element_name = self.clean_element_name(path, base_type)
            # Vis hovedinformasjon: for hver egenskap, bruk profilen dersom definert, ellers basetekst
            first_row = True
            for prop in self.properties:
                base_value = self.get_base_text(base_elements, path, prop)
                profile_value = profile_elem_base.get(prop, '') if profile_elem_base else ''
                # Bruk overstyrt tekst fra profilen dersom den finnes, ellers basetekst
                value = profile_value if profile_value.strip() else base_value
                formatted_value = self.format_value(value, base_value)
                if first_row:
                    print(f"| {element_name} | Short | {formatted_value} |")
                    first_row = False
                else:
                    print(f"| | {prop.capitalize()} | {formatted_value} |")

            # Vis binding dersom den finnes
            base_binding = base_elem.get('binding', {})
            profile_binding = profile_elem_base.get('binding', {}) if profile_elem_base else {}
            binding = profile_binding if profile_binding else base_binding
            if binding:
                formatted_binding = self.format_binding(binding)
                if formatted_binding:
                    print(f"| | Binding | {formatted_binding} |")

            # Finn og vis slices
            slices = self.find_slices(profile, path)
            for slice_path, slice_elem in slices:
                slice_name = slice_path.split(':')[-1] if ':' in slice_path else ''
                full_slice_name = f"{element_name}:{slice_name}"
                first_row = True
                for prop in self.properties:
                    # For slices bruker vi teksten fra slice-elementet direkte
                    value = slice_elem.get(prop, '')
                    formatted_value = self.format_value(value, '', is_slice=True)
                    if first_row:
                        print(f"| {full_slice_name} | {prop.capitalize()} | {formatted_value} |")
                        first_row = False
                    else:
                        print(f"| | {prop.capitalize()} | {formatted_value} |")
                slice_binding = slice_elem.get('binding')
                if slice_binding:
                    formatted_binding = self.format_binding(slice_binding)
                    if formatted_binding:
                        print(f"| | Binding | {formatted_binding} |")
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