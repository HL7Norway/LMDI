import os
import sys
import json
from typing import Dict, List, Set, Optional
from dataclasses import dataclass

COMPLEX_TYPES = {
    'Identifier',
    'Address',
    'CodeableConcept',
    'Period',
    'HumanName',
    'ContactPoint',
    'Reference'
}

SKIP_ELEMENTS = {
    'id',
    'meta',
    'implicitRules',
    'language',
    'contained',
    'modifierExtension',
    'extension'
}

@dataclass
class FHIRElement:
    name: str
    type: str
    cardinality: str
    path: str
    is_complex: bool = False
    is_reference: bool = False

class FHIRStructure:
    def __init__(self, name: str):
        self.name = name
        self.elements: Dict[str, FHIRElement] = {}
        self.complex_types: Dict[str, Dict[str, FHIRElement]] = {}
        self.references: Dict[str, FHIRElement] = {}

def should_skip_element(path: str) -> bool:
    """Check if element should be skipped in the diagram."""
    element_name = path.split('.')[-1]
    return element_name in SKIP_ELEMENTS

def is_complex_type(type_info: List[dict]) -> bool:
    """Determine if a type is complex."""
    if not type_info:
        return False
    return type_info[0]['code'] in COMPLEX_TYPES

def parse_element_definition(element: dict) -> Optional[FHIRElement]:
    """Parse a FHIR element definition."""
    path = element.get('path', '')
    if should_skip_element(path):
        return None
        
    # Check if element is disabled
    if element.get('max') == '0':
        return None
        
    # Get type information
    type_info = element.get('type', [])
    if not type_info:
        return None
        
    name = path.split('.')[-1]
    base_type = type_info[0]['code']
    min_value = element.get('min', 0)
    max_value = element.get('max', '*')
    cardinality = f"{min_value}..{max_value}"
    
    # Handle references
    if base_type == 'Reference':
        target_profile = type_info[0].get('targetProfile', [None])[0]
        if target_profile:
            type_name = target_profile.split('/')[-1]
            return FHIRElement(
                name=name,
                type=type_name,
                cardinality=cardinality,
                path=path,
                is_reference=True
            )
            
    return FHIRElement(
        name=name,
        type=base_type,
        cardinality=cardinality,
        path=path,
        is_complex=is_complex_type(type_info)
    )

def parse_structure_definition(profile_json: dict) -> FHIRStructure:
    """Parse a FHIR StructureDefinition."""
    structure = FHIRStructure(profile_json['name'])
    
    # Process each element
    snapshot_elements = profile_json.get('snapshot', {}).get('element', [])
    for element in snapshot_elements:
        parsed_element = parse_element_definition(element)
        if not parsed_element:
            continue
            
        path_parts = parsed_element.path.split('.')
        if len(path_parts) == 1:  # Skip resource root
            continue
            
        if parsed_element.is_reference:
            if parsed_element.name == 'partOf':
                structure.references[parsed_element.name] = parsed_element
        elif parsed_element.is_complex:
            base_path = '.'.join(path_parts[:-1])
            if base_path not in structure.complex_types:
                structure.complex_types[base_path] = {}
            structure.complex_types[base_path][parsed_element.path] = parsed_element
        else:
            structure.elements[parsed_element.path] = parsed_element
    
    return structure

def generate_plantuml(structure: FHIRStructure) -> str:
    """Generate PlantUML class diagram."""
    uml = ["@startuml"]
    uml.append("""
skinparam class {
    BackgroundColor White
    ArrowColor Black
    BorderColor Black
}
""")
    
    # Define main resource class
    uml.append(f"class {structure.name} {{")
    for element in structure.elements.values():
        if '.' not in element.path:  # Only show top-level elements
            uml.append(f"    +{element.name}: {element.type} {element.cardinality}")
    uml.append("}")
    
    # Define complex type classes and relationships
    for base_path, elements in structure.complex_types.items():
        type_name = base_path.split('.')[-1].capitalize()
        if elements:  # Only create class if it has elements
            uml.append(f"class {type_name} <<DataType>> {{")
            for element in elements.values():
                local_name = element.path.split('.')[-1]
                uml.append(f"    +{local_name}: {element.type} {element.cardinality}")
            uml.append("}")
            
            # Add aggregation relationship
            first_element = next(iter(elements.values()))
            uml.append(f'{structure.name} o-- "{first_element.cardinality}" {type_name}')
    
    # Add reference relationship (partOf)
    if 'partOf' in structure.references:
        ref = structure.references['partOf']
        uml.append(f'{structure.name} "{ref.cardinality}" -- {ref.type} : "partOf"')
    
    uml.append("@enduml")
    return "\n".join(uml)

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_profile.json>")
        return
        
    profile_path = sys.argv[1]
    if not os.path.exists(profile_path):
        print(f"Error: Profile file {profile_path} does not exist")
        return
    
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile_json = json.load(f)
            
        structure = parse_structure_definition(profile_json)
        plantuml = generate_plantuml(structure)
        print("\nGenerated PlantUML diagram:")
        print(plantuml)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()