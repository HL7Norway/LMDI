import json
from dataclasses import dataclass
from typing import Dict, Optional

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
    structure = FHIRStructure(profile_json['name'])
    
    for element in profile_json.get('snapshot', {}).get('element', []):
        reference = parse_element_definition(element)
        if reference:
            structure.references[reference.name] = reference
    
    return structure

def generate_plantuml(structure: FHIRStructure) -> str:
    """Generate PlantUML with only resource types and references."""
    uml = [
        "@startuml",
        "skinparam class { BackgroundColor White ArrowColor Black BorderColor Black }",
        f"class {structure.name}"
    ]
    
    for ref in structure.references.values():
        uml.append(f'{ref.source} "{ref.cardinality}" -- {ref.target} : "{ref.name}"')
    
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