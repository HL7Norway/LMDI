import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import requests
import argparse
import os

DEFAULT_PATH = r"c:\dev\lmdi\lmdi\fsh-generated\resources"

@dataclass
class FHIRElementInfo:
    path: str
    type_code: str
    cardinality: str
    changes: str

def generate_example(resource_type: str, elements: List[FHIRElementInfo]) -> dict:
    """Generate example data based on resource type and elements."""
    example = {
        "resourceType": resource_type,
        "id": "example-1",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2024-02-05T13:28:17+01:00"
        }
    }
    
    # Hent alle elementer som skal inkluderes (cardinality ikke 0..0)
    required_elements = [elem for elem in elements if not (elem.cardinality == '0..0')]
    
    for element in required_elements:
        if '.' not in element.path:
            continue
            
        path_parts = f"{resource_type}.{element.path}".split('.')
        current = example
        
        for i, part in enumerate(path_parts[1:]):
            if i == len(path_parts[1:]) - 1:
                if element.type_code == "string":
                    current[part] = f"Eksempel {part}"
                elif element.type_code == "code":
                    current[part] = "active"
                elif element.type_code == "uri":
                    current[part] = "urn:oid:2.16.578.1.12.4.1.4.1"
                elif element.type_code == "boolean":
                    current[part] = True
                elif element.type_code == "integer":
                    current[part] = 42
                elif element.type_code == "decimal":
                    current[part] = 37.5
                elif element.type_code == "positiveInt":
                    current[part] = 42
                elif element.type_code == "unsignedInt":
                    current[part] = 42
                elif element.type_code == "base64Binary":
                    current[part] = "SGVsbG8="
                elif element.type_code == "instant":
                    current[part] = "2024-02-05T13:28:17+01:00"
                elif element.type_code == "date":
                    current[part] = "2024-02-05"
                elif element.type_code == "dateTime":
                    current[part] = "2024-02-05T13:28:17+01:00"
                elif element.type_code == "time":
                    current[part] = "13:28:17"
                elif element.type_code == "Identifier":
                    current[part] = {
                        "system": "urn:oid:2.16.578.1.12.4.1.4.1",
                        "value": "04021550123"
                    }
                elif element.type_code == "HumanName":
                    current[part] = {
                        "use": "official",
                        "family": "Olsen",
                        "given": ["Erik"]
                    }
                elif element.type_code == "Address":
                    current[part] = {
                        "use": "home",
                        "line": ["Storgata 55"],
                        "city": "Oslo",
                        "postalCode": "0182",
                        "country": "NO"
                    }
                elif element.type_code == "ContactPoint":
                    current[part] = {
                        "system": "phone",
                        "value": "+47 99887766",
                        "use": "work"
                    }
                elif element.type_code == "Period":
                    current[part] = {
                        "start": "2024-02-05",
                        "end": "2024-03-05"
                    }
                elif element.type_code == "Coding":
                    current[part] = {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                        "code": "MR",
                        "display": "Medical record number"
                    }
                elif element.type_code == "CodeableConcept":
                    current[part] = {
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "MR",
                            "display": "Medical record number"
                        }],
                        "text": "Medical record number"
                    }
                elif element.type_code == "Reference":
                    current[part] = {
                        "reference": f"Organization/example",
                        "display": "Example Organization"
                    }
                else:
                    current[part] = f"Example {element.type_code}"
            else:
                if part not in current:
                    current[part] = {}
                current = current[part]
    
    return example

class FHIRResourceAnalyzer:
    FHIR_BASE_URL = "http://hl7.org/fhir/R4"
    
    def __init__(self, profile_path: str, base_definitions_dir: str = "base_definitions"):
        self.profile_path = profile_path
        self.base_definitions_dir = Path(base_definitions_dir)
        self.base_definitions_dir.mkdir(exist_ok=True)
        
        self.profile_data = self._load_profile()
        self.base_resource_type = self._get_base_resource_type()
        self.base_definition = self._load_base_definition()
    
    def _get_base_resource_type(self) -> str:
        base_url = self.profile_data.get('baseDefinition', '')
        return base_url.split('/')[-1]
    
    def _load_profile(self) -> dict:
        with open(self.profile_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_base_definition(self) -> dict:
        base_file = self.base_definitions_dir / f"{self.base_resource_type}.json"
        if not base_file.exists():
            url = f"{self.FHIR_BASE_URL}/StructureDefinition/{self.base_resource_type}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                with open(base_file, 'w', encoding='utf-8') as f:
                    json.dump(response.json(), f, indent=2)
            except requests.exceptions.RequestException as e:
                print(f"Kunne ikke laste base-definisjon: {e}")
                return {}
                
        with open(base_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_elements(self) -> List[FHIRElementInfo]:
        # Hent baseprofilens elementer
        base_elements = self.base_definition.get('snapshot', {}).get('element', [])
        base_dict = {elem['path']: elem for elem in base_elements}
        
        # Hent profilens elementer
        profile_elements = self.profile_data.get('snapshot', {}).get('element', [])
        profile_dict = {elem['path']: elem for elem in profile_elements}
        
        analyzed_elements = []
        
        for base_elem in base_elements:
            path = base_elem['path']
            if '.' not in path:
                continue
            
            profile_elem = profile_dict.get(path, {})
            
            # Hent base-info
            base_min = base_elem.get('min', 0)
            base_max = base_elem.get('max', '*')
            base_type = base_elem.get('type', [{}])[0].get('code', '')
            
            # Sjekk for endringer i profil
            changes = []
            
            if 'min' in profile_elem and profile_elem['min'] != base_min:
                changes.append(f"min: {base_min}→{profile_elem['min']}")
                
            if 'max' in profile_elem and profile_elem['max'] != base_max:
                changes.append(f"max: {base_max}→{profile_elem['max']}")
                
            profile_type = profile_elem.get('type', [{}])[0].get('code', '') if profile_elem.get('type') else base_type
            if profile_type != base_type:
                changes.append(f"type: {base_type}→{profile_type}")
                
            if profile_elem.get('mustSupport'):
                changes.append("MS")
                
            if profile_elem.get('fixedValue'):
                changes.append("fixed")
                
            if profile_elem.get('pattern'):
                changes.append("pattern")
    
            # Bruk profilkardinalitet kun dersom den er endret, ellers vis basekardinalitet
            if (profile_elem.get('min', base_min) != base_min) or (profile_elem.get('max', base_max) != base_max):
                cardinality = f"{profile_elem.get('min', base_min)}..{profile_elem.get('max', base_max)}"
            else:
                cardinality = f"{base_min}..{base_max}"
            
            display_path = path.split('.')[-1] if '.' in path else path
            
            element_info = FHIRElementInfo(
                path=display_path,
                type_code=base_type,
                cardinality=cardinality,
                changes=", ".join(changes) if changes else "-"
            )
            analyzed_elements.append(element_info)
            
        return analyzed_elements

def analyze_profile(path: str):
    analyzer = FHIRResourceAnalyzer(path)
    elements = analyzer.analyze_elements()
    
    table_data = [(e.path, e.type_code, e.cardinality, e.changes) for e in elements]
    
    # Skriv ut profiloverskrift
    print(f"\n\n# {analyzer.profile_data.get('title', analyzer.profile_data.get('name', 'Ukjent'))}")
    print(f"Base: {analyzer.base_resource_type}")
    
    # Skriv ut tabellen
    print("\n## Elementer")
    print("| Element | Type | Kardinalitet | Endringer |")
    print("|---------|------|--------------|------------|")
    for elem, type_code, card, changes in table_data:
        print(f"| {elem} | {type_code} | {card} | {changes} |")
    
    # Generer og skriv ut eksempel
    print("\n## Eksempel")
    print("```json")
    example = generate_example(analyzer.base_resource_type, elements)
    print(json.dumps(example, indent=2, ensure_ascii=False))
    print("```")
    print("\n")

def get_structure_definitions(directory: str) -> List[str]:
    return [str(p) for p in Path(directory).glob("StructureDefinition-*.json")]

def get_profile_path() -> str:
    parser = argparse.ArgumentParser(description='Analyser FHIR-profil')
    parser.add_argument('path', nargs='?', help='Sti til FHIR-profil eller mappe')
    args = parser.parse_args()

    path = args.path or input(f"\nAngi sti til FHIR-profil [trykk Enter for {DEFAULT_PATH}]: ").strip() or DEFAULT_PATH
    
    if not os.path.exists(path):
        print(f"Finner ikke: {path}")
        return None
        
    return path

if __name__ == '__main__':
    path = get_profile_path()
    if path:
        if os.path.isdir(path):
            profiles = get_structure_definitions(path)
            for profile in profiles:
                try:
                    analyze_profile(profile)
                except Exception as e:
                    print(f"Feil ved analyse av {profile}: {e}")
        else:
            analyze_profile(path)
