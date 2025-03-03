import json
import os
import requests
from dataclasses import dataclass
from typing import Dict, Optional, List, Set, Tuple
from urllib.parse import urljoin

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
    'lmdi-practitionerrole': 'Helsepersonellrolle',
    # Legg til flere mappinger basert på filnavnene
    'lmdi-adresse': 'Adresse',
    'lmdi-diagnose': 'Diagnose',
    'lmdi-institusjonsopphold': 'Institusjonsopphold',
    'lmdi-legemiddel': 'Legemiddel',
    'lmdiLegemiddelrekvirering': 'Legemiddelrekvirering',
    'lmdLegemiddeladministrering': 'Legemiddeladministrering',
    'episode': 'Episode'  # Lagt til denne mappingen
}

# Liste over standard FHIR-elementer som skal ekskluderes
STANDARD_ELEMENTS = {
    'id', 'meta', 'implicitRules', 'language', 'text', 'contained', 
    'extension', 'modifierExtension', 'resourceType'
}

# Base URL for documentation links
LMDI_DOCS_BASE_URL = "https://hl7norway.github.io/LMDI/currentbuild/StructureDefinition-"
FHIR_DOCS_BASE_URL = "https://hl7.org/fhir/R4/"

# Base URL for FHIR R4 resources
FHIR_R4_BASE_URL = "http://hl7.org/fhir/R4/"

# Cache for storing fetched resource definitions
RESOURCE_DEFINITION_CACHE = {}

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

@dataclass
class ElementCardinality:
    min: int
    max: str  # Can be a number or "*"

@dataclass
class FHIRAttribute:
    name: str
    type: str
    cardinality: str
    path: str
    slice_name: Optional[str] = None  # Add slice_name field

class FHIRStructure:
    def __init__(self, name: str):
        self.name = name
        self.references: Dict[str, FHIRReference] = {}
        # Keep track of zero cardinality paths
        self.zero_cardinality_paths: Set[str] = set()
        # Store the base type for stereotypes
        self.base_type: str = ""
        # Store cardinality for each path
        self.element_cardinalities: Dict[str, ElementCardinality] = {}
        # Store attributes (fields) for this structure
        self.attributes: List[FHIRAttribute] = []
        # Store id for linking to documentation
        self.id: str = ""
        # Flag to indicate if this is a local profile or fetched from FHIR base
        self.is_local_profile: bool = True

def combine_cardinality(parent: ElementCardinality, child: ElementCardinality) -> ElementCardinality:
    """Combine parent and child cardinality to get effective cardinality."""
    # For minimum cardinality:
    # - If parent is 0, child can occur 0 times (regardless of child's min)
    # - If parent min > 0, then we need at least parent_min * child_min instances
    combined_min = 0 if parent.min == 0 else parent.min * child.min
    
    # For maximum cardinality:
    # - If either is unlimited (*), the result depends on the other
    # - If parent is 0, the result is 0 (impossible path)
    # - Otherwise, multiply the max values
    if parent.min == 0 and parent.max == "0":
        combined_max = "0"
    elif parent.max == "*" and child.max == "*":
        combined_max = "*"
    elif parent.max == "*":
        combined_max = "*"  # parent allows unlimited, child limits each parent
    elif child.max == "*":
        combined_max = "*"  # unlimited instances of child per each parent
    else:
        # Numeric multiplication of maximums
        try:
            p_max = int(parent.max)
            c_max = int(child.max)
            combined_max = str(p_max * c_max)
        except ValueError:
            # Fallback for any parsing issues
            combined_max = "*"
    
    return ElementCardinality(min=combined_min, max=combined_max)

def calculate_path_cardinality(path: str, element_cardinalities: Dict[str, ElementCardinality]) -> ElementCardinality:
    """Calculate the effective cardinality for a path by combining all parent cardinalities."""
    # Start with a default of exactly 1
    result = ElementCardinality(min=1, max="1")
    
    # Split the path and build up each segment
    parts = path.split('.')
    current_path = ""
    
    for i, part in enumerate(parts):
        # Skip the first part as it's the resource itself
        if i == 0:
            current_path = part
            continue
            
        # Build the path for this segment
        if current_path:
            current_path = f"{current_path}.{part}"
        else:
            current_path = part
            
        # If we have cardinality for this path, combine it
        if current_path in element_cardinalities:
            result = combine_cardinality(result, element_cardinalities[current_path])
    
    return result

def should_include_as_attribute(path: str, type_info: List[dict]) -> bool:
    """Determine if an element should be included as a class attribute."""
    # Get the parts of the path
    parts = path.split('.')
    if len(parts) != 2:  # Only include direct children of the resource (depth 1)
        return False
        
    element_name = parts[-1]
    
    # Check if it's a standard element that should be excluded
    if element_name in STANDARD_ELEMENTS:
        return False
    
    # Include polymorphic fields (fields ending with [x])
    # instead of filtering them out as before
    
    # Check if it's a reference - we'll represent these as relationships
    for type_def in type_info:
        if type_def.get('code') == 'Reference':
            return False
            
    return True

def parse_element_definition(elements: List[dict], structure: FHIRStructure) -> None:
    """Parse FHIR element definitions for references, cardinalities, and attributes."""
    # First pass - collect all path cardinalities
    for element in elements:
        path = element.get('path', '')
        
        # Skip if path doesn't have minimum segments
        if not path or path.count('.') < 0:
            continue
            
        # Extract cardinality
        min_value = element.get('min', 0)
        max_value = element.get('max', '*')
        
        # Store the cardinality for this path
        structure.element_cardinalities[path] = ElementCardinality(
            min=int(min_value), 
            max=max_value
        )
        
        # If this is a zero cardinality element, mark it
        if max_value == '0':
            structure.zero_cardinality_paths.add(path)
            print(f"Identified zero cardinality path: {path}")
    
    # Second pass - process references and attributes with correct combined cardinality
    for element in elements:
        path = element.get('path', '')
        
        # Skip if path doesn't have minimum segments (resource.element)
        if not path or path.count('.') < 1:
            continue
            
        # Check if this path or any parent has zero cardinality
        skip_element = False
        for zero_path in structure.zero_cardinality_paths:
            if path == zero_path or path.startswith(zero_path + '.'):
                skip_element = True
                print(f"Skipping {path} - path or parent has zero cardinality")
                break
                
        if skip_element:
            continue
        
        # Process different type structures
        type_info = element.get('type', [])
        
        # Calculate the effective cardinality for this path
        effective_cardinality = calculate_path_cardinality(path, structure.element_cardinalities)
        cardinality_str = f"{effective_cardinality.min}..{effective_cardinality.max}"
        
        # Process as an attribute if it meets criteria
        if should_include_as_attribute(path, type_info):
            # Get the element name (last part of the path)
            element_name = path.split('.')[-1]
            
            # Get the type name - use the first type if multiple exist
            type_name = "unknown"
            if type_info:
                # For polymorphic fields, use a special format
                if element_name.endswith('[x]'):
                    # List all possible types
                    types = [t.get('code', 'unknown') for t in type_info]
                    type_name = ' | '.join(types)
                else:
                    type_name = type_info[0].get('code', 'unknown')
            
            # Check for slice information
            slice_name = None
            slicing_info = element.get('sliceName')
            if slicing_info:
                slice_name = slicing_info
            
            # Also look for slicing in the element definition
            if not slice_name and 'slicing' in element:
                slice_name = "sliced"
                
            # Create and add the attribute
            attribute = FHIRAttribute(
                name=element_name,
                type=type_name,
                cardinality=cardinality_str,
                path=path,
                slice_name=slice_name
            )
            structure.attributes.append(attribute)
            print(f"Added attribute: {element_name}: {type_name} [{cardinality_str}]{' slice: ' + slice_name if slice_name else ''}")
        
        # Process references
        for type_def in type_info:
            code = type_def.get('code')
            
            # Handle direct references
            if code == 'Reference':
                target_profiles = type_def.get('targetProfile', [])
                if not target_profiles:
                    continue
                
                # Process all target profiles in the list
                for target_profile in target_profiles:
                    # Skip if target is an Extension
                    if 'Extension' in target_profile:
                        print(f"Skipping {path} - references Extension")
                        continue
                        
                    # Extract the target type from the profile URL
                    target_type = target_profile.split('/')[-1]
                    if target_type.startswith('StructureDefinition-'):
                        target_type = target_type[len('StructureDefinition-'):]
                        
                    # For nested paths, use the full path in the reference name
                    source_part = path.split('.')[0]
                    
                    # Get the full path without the resource name for the reference name
                    # This keeps all the path elements for the relationship name
                    if '.' in path:
                        # Get everything after the resource name (the first segment)
                        friendly_name = path[len(source_part)+1:]
                        # Remove any [x] from the path segments
                        friendly_name = friendly_name.replace('[x]', '')
                    else:
                        friendly_name = path
                        # Remove any [x] if present in the resource name itself
                        friendly_name = friendly_name.replace('[x]', '')
                    
                    # Create unique reference key when there are multiple targets
                    ref_key = f"{friendly_name}_to_{target_type}" if len(target_profiles) > 1 else friendly_name
                    
                    reference = FHIRReference(
                        source=source_part,
                        target=target_type,
                        name=friendly_name,
                        cardinality=cardinality_str
                    )
                    structure.references[ref_key] = reference
                    print(f"Found reference: {source_part} -- {friendly_name} --> {target_type} [{cardinality_str}]")

def parse_structure_definition(profile_json: dict, filename: str) -> Optional[FHIRStructure]:
    """Parse a FHIR StructureDefinition for resource references and attributes."""
    # Debug output
    print(f"Parsing file: {filename}")
    print(f"Resource kind: {profile_json.get('kind')}")
    print(f"Resource type: {profile_json.get('type')}")
    print(f"Resource id: {profile_json.get('id')}")
    print(f"Resource name: {profile_json.get('name')}")
    
    # Check if this is a profile or resource
    if profile_json.get('kind') not in ['resource', 'complex-type']:
        print(f"Skipping {filename} - not a resource or complex-type")
        return None
        
    # Store the original resource ID for documentation links
    resource_id = profile_json.get('id', '')
    
    # Prioritize name > id > type for the structure name
    resource_name = None
    for field in ['name', 'id', 'type']:
        if profile_json.get(field):
            value = profile_json.get(field)
            # Check if we have a mapping for this value
            if value in RESOURCE_NAME_MAPPING:
                resource_name = RESOURCE_NAME_MAPPING[value]
                break
            else:
                resource_name = value
                break
    
    if not resource_name:
        # Fallback to the basename of file without extension if no name/id/type
        resource_name = os.path.splitext(os.path.basename(filename))[0]
        if resource_name.startswith('StructureDefinition-'):
            resource_name = resource_name[len('StructureDefinition-'):]
            
    print(f"Using structure name: {resource_name}")
    
    structure = FHIRStructure(resource_name)
    
    # Store the original ID for documentation links
    structure.id = resource_id
    
    # Determine if this is a local profile or fetched from FHIR base
    # Check if filename contains "fetched-" which indicates it's from FHIR base
    structure.is_local_profile = not filename.startswith("fetched-")
    
    # Store the base type
    structure.base_type = profile_json.get('baseDefinition', '').split('/')[-1]
    if structure.base_type.startswith('StructureDefinition-'):
        structure.base_type = structure.base_type[len('StructureDefinition-'):]
    print(f"Base type: {structure.base_type}")
    
    # Check both snapshot and differential
    elements = (profile_json.get('snapshot', {}).get('element', []) or 
               profile_json.get('differential', {}).get('element', []))
    
    # Process all elements
    parse_element_definition(elements, structure)
    
    return structure

def fetch_fhir_resource_definition(resource_type: str) -> Optional[dict]:
    """
    Hent ressursdefinisjon fra FHIR R4 API hvis den ikke finnes i cachen.
    """
    # Check if already in cache
    if resource_type in RESOURCE_DEFINITION_CACHE:
        return RESOURCE_DEFINITION_CACHE[resource_type]

    # FHIR R4 URL format is different - it follows a pattern like:
    # http://hl7.org/fhir/R4/organization.html for the HTML
    # http://hl7.org/fhir/R4/organization.profile.json for the JSON
    
    # Convert to lowercase for the URL
    resource_type_lower = resource_type.lower()
    
    # Format the URL for the resource definition
    url = urljoin(FHIR_R4_BASE_URL, f"{resource_type_lower}.profile.json")
    
    try:
        print(f"Fetching FHIR resource definition for {resource_type} from {url}")
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            RESOURCE_DEFINITION_CACHE[resource_type] = data
            return data
        else:
            print(f"Failed to fetch resource definition for {resource_type}: HTTP {response.status_code}")
            # Try alternate URL format as fallback
            alt_url = urljoin(FHIR_R4_BASE_URL, f"StructureDefinition-{resource_type}.json")
            print(f"Trying alternate URL: {alt_url}")
            alt_response = requests.get(alt_url)
            if alt_response.status_code == 200:
                data = alt_response.json()
                RESOURCE_DEFINITION_CACHE[resource_type] = data
                return data
            return None
            
    except Exception as e:
        print(f"Error fetching resource definition for {resource_type}: {str(e)}")
        return None

def get_documentation_url(structure: FHIRStructure) -> str:
    """Generate documentation URL for the structure."""
    if structure.is_local_profile:
        # Local profile - link to LMDI documentation
        return f"{LMDI_DOCS_BASE_URL}{structure.id}.html"
    else:
        # FHIR base resource - link to HL7 documentation
        # Using lowercase ID for FHIR base URLs
        return f"{FHIR_DOCS_BASE_URL}{structure.id.lower()}.html"

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

def get_structure_for_resource_type(resource_type: str, structures: List[FHIRStructure]) -> Optional[FHIRStructure]:
    """
    Find a structure for the given resource type from the list of structures,
    or fetch it from FHIR R4 API if not found.
    """
    # First look in existing structures
    for structure in structures:
        if structure.name == resource_type or get_resource_name(structure.name) == resource_type:
            return structure
    
    # If not found, try to fetch and parse from FHIR R4 API
    profile_json = fetch_fhir_resource_definition(resource_type)
    if profile_json:
        # Create a new structure from the fetched definition
        structure = parse_structure_definition(profile_json, f"fetched-{resource_type}")
        if structure:
            # Mark as not a local profile since it was fetched
            structure.is_local_profile = False
            
            # Set ID to lowercase resource name for FHIR base links
            structure.id = resource_type.lower()
            
            # Add to our list of structures
            structures.append(structure)
            return structure
    
    # Could not find or fetch the structure
    return None

def generate_plantuml(structures: List[FHIRStructure]) -> str:
    """Generate PlantUML for multiple structures with attributes."""
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
    
    # Track classes with relationships
    classes_with_relationships = set()
    
    # First collect all classes involved in relationships
    for structure in structures:
        source_name = get_resource_name(structure.name)
        if structure.references:  # If this structure has outgoing references
            classes_with_relationships.add(source_name)
            
        # Mark all target classes as having relationships
        for ref in structure.references.values():
            target_name = get_resource_name(ref.target)
            classes_with_relationships.add(target_name)
    
    # Add classes that have relationships
    defined_classes = set()
    base_types = {}  # Store base types for stereotypes
    
    # Extract base types from structures
    for structure in structures:
        structure_name = get_resource_name(structure.name)
        if structure_name in classes_with_relationships:
            # Get base type from the structure
            if hasattr(structure, 'base_type') and structure.base_type:
                base_type = structure.base_type.split('/')[-1]  # Extract last part if it's a URL
                base_types[structure_name] = get_resource_name(base_type)
            else:
                # Default to Resource if no base type is specified
                base_types[structure_name] = "Resource"
    
    # First add classes we have direct definitions for
    for structure in structures:
        structure_name = get_resource_name(structure.name)
        if structure_name in classes_with_relationships and structure_name not in defined_classes:
            base_type = base_types.get(structure_name, "")
            
            # Start class definition with URL link
            doc_url = get_documentation_url(structure)
            display_name = structure_name
            
            if base_type:
                uml.append(f'class {structure_name} <<{base_type}>> [[{doc_url} {display_name} _blank]] {{')
            else:
                uml.append(f'class {structure_name} [[{doc_url} {display_name} _blank]] {{')
                
            # Add attributes
            # Group attributes by name to handle slices
            grouped_attributes = {}
            for attr in structure.attributes:
                if attr.name not in grouped_attributes:
                    grouped_attributes[attr.name] = []
                grouped_attributes[attr.name].append(attr)
                
            # Sort attributes by name for consistent output
            for attr_name, attr_list in sorted(grouped_attributes.items()):
                if len(attr_list) == 1:
                    # Just a regular attribute, no slices
                    attr = attr_list[0]
                    uml.append(f'    {attr.name} : {attr.type} [{attr.cardinality}]')
                else:
                    # Multiple attributes with the same name (slices)
                    for i, attr in enumerate(attr_list):
                        slice_info = f" ({attr.slice_name})" if attr.slice_name else f" (slice {i+1})"
                        uml.append(f'    {attr.name}{slice_info} : {attr.type} [{attr.cardinality}]')
                
            # Close class definition
            uml.append('}')
            defined_classes.add(structure_name)
    
    # Now handle referenced classes that don't have a direct structure definition
    referenced_classes = classes_with_relationships - defined_classes
    for class_name in sorted(referenced_classes):
        # Try to get or fetch the structure for this class
        structure = get_structure_for_resource_type(class_name, structures)
        
        if structure:
            # We found or fetched a definition, use it
            base_type = base_types.get(class_name, "")
            
            # Start class definition with URL link
            doc_url = get_documentation_url(structure)
            display_name = class_name
            
            if base_type:
                uml.append(f'class {class_name} <<{base_type}>> [[{doc_url} {display_name} _blank]] {{')
            else:
                uml.append(f'class {class_name} [[{doc_url} {display_name} _blank]] {{')
                
            # Add attributes
            # Group attributes by name to handle slices
            grouped_attributes = {}
            for attr in structure.attributes:
                if attr.name not in grouped_attributes:
                    grouped_attributes[attr.name] = []
                grouped_attributes[attr.name].append(attr)
                
            # Sort attributes by name for consistent output
            for attr_name, attr_list in sorted(grouped_attributes.items()):
                if len(attr_list) == 1:
                    # Just a regular attribute, no slices
                    attr = attr_list[0]
                    uml.append(f'    {attr.name} : {attr.type} [{attr.cardinality}]')
                else:
                    # Multiple attributes with the same name (slices)
                    for i, attr in enumerate(attr_list):
                        slice_info = f" ({attr.slice_name})" if attr.slice_name else f" (slice {i+1})"
                        uml.append(f'    {attr.name}{slice_info} : {attr.type} [{attr.cardinality}]')
                
            # Close class definition
            uml.append('}')
        else:
            # We could not find or fetch a definition, just add an empty class
            base_type = base_types.get(class_name, "Resource")
            
            # For unknown resources, use a general URL to the resource type
            doc_url = f"{FHIR_DOCS_BASE_URL}{class_name.lower()}.html"
            display_name = class_name
            
            uml.append(f'class {class_name} <<{base_type}>> [[{doc_url} {display_name} _blank]] {{')
            uml.append('}')
        
        defined_classes.add(class_name)
    
    uml.append("")  # Empty line after classes
    
    # Add all relationships
    for structure in structures:
        source_name = get_resource_name(structure.name)
        for ref in structure.references.values():
            target_name = get_resource_name(ref.target)
            uml.append(f'{source_name} "{ref.cardinality}" --> {target_name} : "{ref.name}"')
    
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