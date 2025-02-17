import json
from dataclasses import dataclass
from typing import Dict, Optional

RESOURCE_NAME_MAPPING = {
    'lmdi-bundle': 'LegemiddelregisterBundle',
    'lmdi-condition': 'Diagnose',
    'lmdi-episodeofcare': 'Institusjonsopphold',
    'lmdi-medication': 'Legemiddel',
    'lmdi-medicationadministration': 'Legemiddeladministrering',
    'lmdi-medicationrequest': 'Legemiddelrekvirering',
    'lmdi-organization': 'Organisasjon',
    'lmdi-patient': 'Pasient',
    'lmdi-practitioner': 'Helsepersonell',
    'lmdi-practitionerrole': 'Helsepersonellrolle'
}

def get_resource_name(resource_id: str) -> str:
    """Oversetter resource ID til navn hvis det finnes i mappingen."""
    return RESOURCE_NAME_MAPPING.get(resource_id, resource_id)

@dataclass
class FHIRReference:
    source: str
    target: str
    name: str
    cardinality: str

class FHIRStructure:
    def __init__(self, name: str):
        self.name = name
        self.references: Dict[str, FHIRReference] = {}

def parse_element_definition(element: dict) -> Optional[FHIRReference]:
    """Parse a FHIR element definition for references only."""
    # Skip if max cardinality is 0 or if it's not a direct resource element
    path = element.get('path', '')
    if element.get('max') == '0' or path.count('.') != 1:
        return None
        
    type_info = element.get('type', [])
    if not type_info or type_info[0]['code'] != 'Reference':
        return None
        
    target_profile = type_info[0].get('targetProfile', [None])[0]
    if not target_profile:
        return None
        
    name = path.split('.')[-1]
    target_type = target_profile.split('/')[-1]
    cardinality = f"{element.get('min', 0)}..{element.get('max', '*')}"
    
    return FHIRReference(
        source=path.split('.')[0],
        target=target_type,
        name=name,
        cardinality=cardinality
    )

def parse_structure_definition(profile_json: dict) -> FHIRStructure:
    """Parse a FHIR StructureDefinition for resource references."""
    # Hent base-ressurstypen fra type-feltet
    resource_type = profile_json.get('type', '')
    
    # Finn id-en fra profilen
    profile_id = profile_json.get('id', '')
    
    # Bruk enten den mappede id-en eller ressurstypen
    structure_name = profile_id if profile_id in RESOURCE_NAME_MAPPING else resource_type
    
    structure = FHIRStructure(structure_name)
    
    for element in profile_json.get('snapshot', {}).get('element', []):
        reference = parse_element_definition(element)
        if reference:
            structure.references[reference.name] = reference
    
    return structure


def generate_plantuml(structure: FHIRStructure) -> str:
    """Generate PlantUML with only resource types and references."""
    structure_name = get_resource_name(structure.name)
    
    uml = [
        "@startuml",
        "",  # Tom linje etter @startuml
        "hide empty members",
        "skinparam class {",  # Åpne krøllparentes på egen linje
        "    BackgroundColor White",  # Innrykk for bedre lesbarhet
        "    ArrowColor Black",
        "    BorderColor Black",
        "}",
        "",  # Tom linje etter skinparam
        f"class {structure_name}",
        ""  # Tom linje etter class-definisjon
    ]
    
    for ref in structure.references.values():
        source_name = structure_name
        target_name = get_resource_name(ref.target)
        uml.append(f'{source_name} "{ref.cardinality}" -- {target_name} : "{ref.name}"')
    
    uml.append("")  # Tom linje før @enduml
    uml.append("@enduml")
    return "\n".join(uml)

def main(profile_path: str):
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_json = json.load(f)
        
    structure = parse_structure_definition(profile_json)
    return generate_plantuml(structure)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(main(sys.argv[1]))