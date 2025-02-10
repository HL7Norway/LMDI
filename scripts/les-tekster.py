import os
import sys
import re
import json
from pathlib import Path
import requests

class FSHProfileAnalyzer:
    def __init__(self):
        # Disse tre egenskapene er de vi ønsker å hente ut fra FSH
        self.properties = ['short', 'definition', 'comment']
        self.base_resources_cache = {}

    def load_fsh_file(self, file_path: str) -> dict:
        """
        Leser en FSH-fil linje for linje og ekstraherer:
        - Profilnavn (Profile:)
        - BaseDefinition (Parent:) -> baseDefinition-URL
        - Elementer med cardinalities som ikke er 0..0
        - short/definition/comment hvis tilgjengelig (linjer med ^short, ^definition, ^comment)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Hvis filen kun beskriver Instanser (Instance:), hoppe over
        if content.strip().startswith('Instance:'):
            return {}

        lines = content.split('\n')
        profile_data = {
            'name': '',
            'baseDefinition': '',
            'elements': {}
        }

        # Finn profilnavn (Profile: XXXX)
        profile_match = re.search(r'^Profile:\s*([^\r\n]+)', content, re.MULTILINE)
        if profile_match:
            profile_data['name'] = profile_match.group(1).strip()
        else:
            # Ikke en profil, retur tom
            return {}

        # Finn parent (Parent: XXXX)
        parent_match = re.search(r'^Parent:\s*([^\r\n]+)', content, re.MULTILINE)
        if parent_match:
            parent_name = parent_match.group(1).strip()
            base_url = f"http://hl7.org/fhir/StructureDefinition/{parent_name}"
            profile_data['baseDefinition'] = base_url
        else:
            # Ingen parent, returer tom
            return {}

        # Først må vi finne alle elementer med 0..0 for å ekskludere dem
        zero_zero_elements = set()
        for line in lines:
            zero_match = re.match(r'^\*\s+(\S+)\s+(0\..0)', line.strip())
            if zero_match:
                zero_zero_elements.add(zero_match.group(1))

        # Hjelpestruktur for å lagre midlertidig cardinality per element
        # format: elements[elementName] = {
        #    'card': '1..1',
        #    'short': '',
        #    'definition': '',
        #    'comment': '',
        #    'type': ''
        # }
        elements = {}

        # Regex for cardinality-linjer (eksempel: "* subject 1..1")
        card_pattern = re.compile(r'^\*\s+(\S+)\s+(\d+\..(\d+|\*))')

        # Regex for only-linjer (eksempel: "* subject only Reference(Patient)")
        only_pattern = re.compile(r'^\*\s+(\S+)\s+only\s+(.+)')

        # Regex for short/definition/comment-linjer (eksempel: "* subject ^short = \"Tekst\"")
        prop_pattern = re.compile(r'^\*\s+(\S+)\s+\^(short|definition|comment)\s*=\s*\"(.*)\"')

        for line in lines:
            line_stripped = line.strip()

            if not line_stripped.startswith('*'):
                continue

            # Hopp over 0..0-elementer
            skip_elem = None
            for zero_elem in zero_zero_elements:
                if zero_elem in line_stripped:
                    skip_elem = zero_elem
                    break
            if skip_elem:
                continue

            # Sjekk cardinality
            cm = card_pattern.match(line_stripped)
            if cm:
                elem_name = cm.group(1)
                card = cm.group(2)
                if elem_name not in elements:
                    elements[elem_name] = {'card': card, 'short': '', 'definition': '', 'comment': '', 'type': ''}
                else:
                    elements[elem_name]['card'] = card

            # Sjekk only-linje (eksempel: "* subject only Reference(Patient)")
            om = only_pattern.match(line_stripped)
            if om:
                elem_name = om.group(1)
                type_str = om.group(2).strip()
                if elem_name not in elements:
                    elements[elem_name] = {'card': '', 'short': '', 'definition': '', 'comment': '', 'type': type_str}
                else:
                    elements[elem_name]['type'] = type_str

            # Sjekk short/definition/comment-linje
            pm = prop_pattern.match(line_stripped)
            if pm:
                elem_name = pm.group(1)
                prop_name = pm.group(2)
                prop_value = pm.group(3)
                if elem_name not in elements:
                    elements[elem_name] = {'card': '', 'short': '', 'definition': '', 'comment': '', 'type': ''}
                elements[elem_name][prop_name] = prop_value

        # Filtrer ut 0..0 og manglende cardinality
        filtered_elements = {}
        for ename, edata in elements.items():
            if ename in zero_zero_elements:
                continue
            if not edata['card']:
                edata['card'] = '0..1'
            if edata['card'] == '0..0':
                continue
            filtered_elements[ename] = edata

        profile_data['elements'] = filtered_elements
        return profile_data

    def get_base_resource(self, base_url: str) -> dict:
        """Henter base-definisjonen fra HL7 FHIR eller lokal cache."""
        if not base_url:
            return {}
        if base_url in self.base_resources_cache:
            return self.base_resources_cache[base_url]

        resource_type = base_url.split('/')[-1]
        local_path = f"base_resources/{resource_type}.json"

        if os.path.exists(local_path):
            with open(local_path, 'r', encoding='utf-8') as f:
                base = json.load(f)
        else:
            try:
                api_url = f"http://hl7.org/fhir/R4/StructureDefinition-{resource_type}.json"
                response = requests.get(api_url)
                if response.status_code == 404:
                    api_url = f"http://hl7.org/fhir/R4/{resource_type}.profile.json"
                    response = requests.get(api_url)

                if response.status_code != 200:
                    print(f"Kunne ikke laste baseressurs: {resource_type} (HTTP {response.status_code})")
                    return {}

                base = response.json()
                os.makedirs("base_resources", exist_ok=True)
                with open(local_path, 'w', encoding='utf-8') as f:
                    json.dump(base, f, ensure_ascii=False, indent=2)

            except Exception as e:
                print(f"Feil ved lasting av baseressurs {resource_type}: {str(e)}")
                return {}

        self.base_resources_cache[base_url] = base
        return base

    def escape_markdown(self, text: str) -> str:
        if not text:
            return ''
        return (text.replace('|', '\|')
                    .replace('*', '\*')
                    .replace('_', '\_')
                    .replace('\n', '<br>'))

    def analyze_profile(self, file_path: str):
        profile = self.load_fsh_file(file_path)
        if not profile:
            return

        profile_name = self.escape_markdown(profile.get('name', ''))
        base_url = profile.get('baseDefinition', '')
        base_type = base_url.split('/')[-1] if base_url else ''

        base_resource = self.get_base_resource(base_url)
        base_elements = {}
        if base_resource:
            snapshot = base_resource.get('snapshot', {})
            base_elems = snapshot.get('element', [])
            base_elements = {
                elem.get('path', '').split('.')[-1]: elem
                for elem in base_elems
            }

        # Start med en HTML-header
        print(f"<html>")
        print(f"<h2>{profile_name} : {base_type}</h2>")
        print("<table border='1' style='border-collapse: collapse;'>")
        print("  <thead>")
        print("    <tr><th>Elementnavn</th><th>Type</th><th>Tekst</th></tr>")
        print("  </thead>")
        print("  <tbody>")

        for element_name, profile_elem in profile.get('elements', {}).items():
            base_elem = base_elements.get(element_name, {})

            # Hvis vi ikke har type, sjekk base-elementets type
            element_type = profile_elem['type']
            if not element_type and base_elem.get('type'):
                if isinstance(base_elem['type'], list) and len(base_elem['type']) > 0:
                    element_type = base_elem['type'][0].get('code', '')
                elif isinstance(base_elem['type'], dict):
                    element_type = base_elem['type'].get('code', '')
                else:
                    element_type = ''

            first_row = True
            for prop in self.properties:
                profile_value = profile_elem.get(prop, '')
                base_value = base_elem.get(prop, '')
                value = profile_value if profile_value else base_value

                if profile_value and profile_value != base_value:
                    # Uthev i fet skrift
                    formatted_value = f"<strong>{self.escape_markdown(value)}</strong>"
                else:
                    formatted_value = self.escape_markdown(value)

                if first_row:
                    print(f"    <tr><td rowspan=\"3\">{element_name}<br>{element_type}</td><td>{prop.capitalize()}</td><td>{formatted_value}</td></tr>")
                    first_row = False
                else:
                    # Vis property i en ny rad
                    print(f"    <tr><td>{prop.capitalize()}</td><td>{formatted_value}</td></tr>")

        print("  </tbody>")
        print("</table>")
        print(f"</html>")


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Angi sti til FSH-profil eller katalog (standard: 'profiles'): ").strip() or "profiles"

    analyzer = FSHProfileAnalyzer()

    if os.path.isfile(path):
        analyzer.analyze_profile(path)
    elif os.path.isdir(path):
        for file_path in Path(path).glob('*.fsh'):
            print(f"\nAnalyserer {file_path}:\n")
            analyzer.analyze_profile(str(file_path))
    else:
        print(f"Feil: Kunne ikke finne fil eller katalog: {path}")

if __name__ == "__main__":
    main()
