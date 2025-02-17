import json
import os
from dataclasses import dataclass
from typing import Dict, Optional, List, Set

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
    'lmdi-practitionerrole': 'Helsepersonellrolle',
    # Legg til flere mappinger basert på filnavnene
    'lmdi-adresse': 'Adresse',
    'lmdi-diagnose': 'Diagnose',
    'lmdi-institusjonsopphold': 'Institusjonsopphold',
    'lmdi-legemiddel': 'Legemiddel',
    'lmdiLegemiddelrekvirering': 'Legemiddelrekvirering',
    'lmdLegemiddeladministrering': 'Legemiddeladministrering'
}

def get_resource_name(resource_id: str) -> str:
    """Oversetter resource ID til navn hvis det finnes i mappingen."""
    # Strip any StructureDefinition- prefix if present
    if resource_id.startswith('StructureDefinition-'):
        resource_id = resource_id[len('StructureDefinition-'):]
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
    path = element.get('path', '')
    
    # Skip hvis path ikke er direkte under roten
    if path.count('.') != 1:
        return None
        
    # Skip hvis kardinalitet er 0..0
    max_value = element.get('max', '*')
    if max_value == '0':
        print(f"Skipping {path} - max cardinality is 0")
        return None
        
    # Skip Extension fields
    if path.endswith('extension') or path.endswith('modifierExtension'):
        print(f"Skipping {path} - extension field")
        return None
        
    type_info = element.get('type', [])
    if not type_info or type_info[0].get('code') != 'Reference':
        return None
        
    target_profiles = type_info[0].get('targetProfile', [])
    if not target_profiles:
        return None
        
    # Skip hvis target er en Extension
    target_profile = target_profiles[0]
    if 'Extension' in target_profile:
        print(f"Skipping {path} - references Extension")
        return None
        
    # Get the first target profile
    target_profile = target_profiles[0]
    name = path.split('.')[-1]
    
    # Extract the target type from the profile URL
    target_type = target_profile.split('/')[-1]
    if target_type.startswith('StructureDefinition-'):
        target_type = target_type[len('StructureDefinition-'):]
        
    cardinality = f"{element.get('min', 0)}..{element.get('max', '*')}"
    
    return FHIRReference(
        source=path.split('.')[0],
        target=target_type,
        name=name,
        cardinality=cardinality
    )

def parse_structure_definition(profile_json: dict, filename: str) -> Optional[FHIRStructure]:
    """Parse a FHIR StructureDefinition for resource references."""
    # Debug output
    print(f"Parsing file: {filename}")
    print(f"Resource kind: {profile_json.get('kind')}")
    print(f"Resource type: {profile_json.get('type')}")
    print(f"Resource id: {profile_json.get('id')}")
    
    # Check if this is a profile or resource
    if profile_json.get('kind') not in ['resource', 'complex-type']:
        print(f"Skipping {filename} - not a resource or complex-type")
        return None
        
    resource_type = profile_json.get('type', '')
    profile_id = profile_json.get('id', '')
    
    # Use basename of file without extension if no id
    if not profile_id:
        profile_id = os.path.splitext(os.path.basename(filename))[0]
        if profile_id.startswith('StructureDefinition-'):
            profile_id = profile_id[len('StructureDefinition-'):]
    
    structure_name = profile_id if profile_id in RESOURCE_NAME_MAPPING else resource_type
    print(f"Using structure name: {structure_name}")
    
    structure = FHIRStructure(structure_name)
    
    # Check both snapshot and differential
    elements = (profile_json.get('snapshot', {}).get('element', []) or 
               profile_json.get('differential', {}).get('element', []))
    
    for element in elements:
        reference = parse_element_definition(element)
        if reference:
            print(f"Found reference: {reference}")
            structure.references[reference.name] = reference
    
    return structure

def find_structure_definitions(path: str) -> List[str]:
    """Finn alle StructureDefinition-*.json filer i angitt sti."""
    structure_files = []
    
    if os.path.isfile(path):
        return [path] if os.path.basename(path).startswith('StructureDefinition-') else []
        
    for root, _, files in os.walk(path):
        for file in files:
            if file.startswith('StructureDefinition-') and file.endswith('.json'):
                full_path = os.path.join(root, file)
                structure_files.append(full_path)
                print(f"Found file: {full_path}")
                
    return structure_files

def generate_plantuml(structures: List[FHIRStructure]) -> str:
    """Generate PlantUML for multiple structures."""
    uml = [
        "@startuml",
        "",
        "hide empty members",
        "skinparam class {",
        "    BackgroundColor White",
        "    ArrowColor Black",
        "    BorderColor Black",
        "}",
        ""
    ]
    
    # Add all classes first
    defined_classes = set()
    for structure in structures:
        structure_name = get_resource_name(structure.name)
        if structure_name not in defined_classes:
            uml.append(f"class {structure_name}")
            defined_classes.add(structure_name)
            
        # Add referenced classes that aren't already defined
        for ref in structure.references.values():
            target_name = get_resource_name(ref.target)
            if target_name not in defined_classes:
                uml.append(f"class {target_name}")
                defined_classes.add(target_name)
    
    uml.append("")  # Empty line after classes
    
    # Add all relationships
    for structure in structures:
        source_name = get_resource_name(structure.name)
        for ref in structure.references.values():
            target_name = get_resource_name(ref.target)
            uml.append(f'{source_name} "{ref.cardinality}" -- {target_name} : "{ref.name}"')
    
    uml.extend(["", "@enduml"])
    return "\n".join(uml)

def main(path: str) -> str:
    """
    Hovedfunksjon som håndterer både enkeltfiler og mapper.
    Returns PlantUML-diagrammet som en streng.
    """
    structure_files = find_structure_definitions(path)
    if not structure_files:
        raise ValueError(f"Ingen StructureDefinition-filer funnet i {path}")
    
    print(f"Found {len(structure_files)} structure definition files")
    
    structures = []
    for file_path in structure_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                profile_json = json.load(f)
            
            structure = parse_structure_definition(profile_json, file_path)
            if structure:
                structures.append(structure)
                print(f"Successfully parsed {file_path}")
            else:
                print(f"No valid structure found in {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            
    if not structures:
        raise ValueError("No valid profiles found in files")
    
    print(f"Successfully parsed {len(structures)} structures")
    return generate_plantuml(structures)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <path-to-file-or-directory>")
        sys.exit(1)
        
    try:
        print(main(sys.argv[1]))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)