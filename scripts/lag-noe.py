#!/usr/bin/env python3

import argparse
import json
import sys
import os
from typing import Dict, List, Any, Optional

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="List all elements from a FHIR Structure Definition's snapshot."
    )
    parser.add_argument(
        "path", 
        help="Path to the FHIR Structure Definition JSON file"
    )
    parser.add_argument(
        "format", 
        nargs="?",
        choices=["simple", "detailed", "tree", "references"], 
        default="simple",
        help="Output format (simple, detailed, tree, or references)"
    )
    parser.add_argument(
        "--filter", 
        help="Filter elements by path (e.g. 'Patient.name')"
    )
    return parser.parse_args()

def load_fhir_structure_definition(path: str) -> Dict:
    """Load FHIR Structure Definition from JSON file."""
    try:
        # Print file path for debugging
        print(f"Attempting to load file: {path}")
        print(f"File exists: {os.path.exists(path)}")
        
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading file: {str(e)}")
        sys.exit(1)

def extract_snapshot_elements(structure_definition: Dict) -> List[Dict]:
    """Extract all elements from the snapshot section of a FHIR Structure Definition."""
    # Print structure keys for debugging
    print(f"Structure definition keys: {list(structure_definition.keys())}")
    
    if "snapshot" not in structure_definition:
        print("Error: Structure Definition does not contain a snapshot section.")
        sys.exit(1)
    
    if "element" not in structure_definition["snapshot"]:
        print("Error: Snapshot section does not contain elements.")
        sys.exit(1)
    
    return structure_definition["snapshot"]["element"]

def filter_elements_by_path(elements: List[Dict], path_filter: str) -> List[Dict]:
    """Filter elements by path prefix."""
    if not path_filter:
        return elements
    
    return [elem for elem in elements if elem.get("path", "").startswith(path_filter)]

def format_simple_output(elements: List[Dict]) -> None:
    """Print elements in a simple format."""
    for elem in elements:
        path = elem.get("path", "unknown")
        type_info = ""
        if "type" in elem and elem["type"]:
            types = [t.get("code", "unknown") for t in elem["type"]]
            type_info = f" ({', '.join(types)})"
        
        cardinality = f"[{elem.get('min', '?')}..{elem.get('max', '?')}]"
        print(f"{path} {cardinality}{type_info}")

def format_detailed_output(elements: List[Dict]) -> None:
    """Print elements in a detailed format."""
    for elem in elements:
        path = elem.get("path", "unknown")
        print(f"Path: {path}")
        
        if "definition" in elem:
            print(f"  Definition: {elem['definition']}")
        
        if "min" in elem or "max" in elem:
            cardinality = f"[{elem.get('min', '?')}..{elem.get('max', '?')}]"
            print(f"  Cardinality: {cardinality}")
        
        if "type" in elem and elem["type"]:
            types = [t.get("code", "unknown") for t in elem["type"]]
            print(f"  Types: {', '.join(types)}")
            
            # Print type targets for Reference types
            for t in elem["type"]:
                if t.get("code") == "Reference" and "targetProfile" in t:
                    target_profiles = t["targetProfile"]
                    if isinstance(target_profiles, list):
                        targets = [p.split("/")[-1] for p in target_profiles]
                        print(f"  References to: {', '.join(targets)}")
                    else:
                        target = target_profiles.split("/")[-1]
                        print(f"  References to: {target}")
        
        print()  # Empty line between elements

def get_all_resource_paths(elements: List[Dict]) -> Dict[str, List[str]]:
    """Get all paths and parent-child relationships."""
    # Map from resource name to parent paths
    resource_paths = {}
    
    # First, gather all the resource paths
    for elem in elements:
        path = elem.get("path", "")
        if not path:
            continue
        
        parts = path.split(".")
        resource = parts[0]
        
        if resource not in resource_paths:
            resource_paths[resource] = []
        
        resource_paths[resource].append(path)
    
    return resource_paths

def is_child_path(parent_path: str, potential_child_path: str) -> bool:
    """Check if potential_child_path is a direct or indirect child of parent_path."""
    if not potential_child_path.startswith(parent_path):
        return False
    
    # If parent is "Resource" and child is "Resource.x", that's a child
    if parent_path == potential_child_path:
        return False
    
    # If parent is "A.B" and child is "A.B.C", that's a child
    # If parent is "A.B" and child is "A.BC", that's not a child
    parent_parts = parent_path.split(".")
    child_parts = potential_child_path.split(".")
    
    if len(child_parts) <= len(parent_parts):
        return False
    
    for i in range(len(parent_parts)):
        if parent_parts[i] != child_parts[i]:
            return False
    
    return True

def collect_child_elements(elements: List[Dict], parent_path: str) -> List[Dict]:
    """Collect all child elements of a given parent path."""
    child_elements = []
    
    for elem in elements:
        path = elem.get("path", "")
        if is_child_path(parent_path, path):
            child_elements.append(elem)
    
    return child_elements

def has_disabled_parent(path: str, elements: List[Dict]) -> bool:
    """Check if any parent element in the path is disabled (max=0)."""
    parts = path.split('.')
    for i in range(1, len(parts)):
        parent_path = '.'.join(parts[:i])
        for elem in elements:
            if elem.get('path') == parent_path and elem.get('max') == '0':
                return True
    return False

def format_references_output(elements: List[Dict]) -> None:
    """Print only elements that can be References and what they can reference."""
    reference_count = 0
    processed_paths = set()
    
    # Sort elements by path to ensure parent paths are processed before children
    sorted_elements = sorted(elements, key=lambda e: e.get("path", ""))
    
    for elem in sorted_elements:
        if "type" not in elem or not elem["type"]:
            continue
            
        path = elem.get("path", "unknown")
        
        # Skip if already processed (prevents duplicates from child reference scanning)
        if path in processed_paths:
            continue
        
        # Check if this element has max=0 or any parent is disabled
        if elem.get("max") == "0" or has_disabled_parent(path, elements):
            continue
            
        # Check if any of the types is a Reference
        reference_types = [t for t in elem["type"] if t.get("code") == "Reference"]
        
        # If this element is a reference, process it
        if reference_types:
            reference_count += 1
            cardinality = f"[{elem.get('min', '?')}..{elem.get('max', '?')}]"
            
            print(f"Path: {path} {cardinality}")
            
            # Extract all possible reference targets
            all_targets = []
            for ref_type in reference_types:
                if "targetProfile" in ref_type:
                    target_profiles = ref_type["targetProfile"]
                    if isinstance(target_profiles, list):
                        # Multiple target profiles
                        for profile in target_profiles:
                            # Extract the resource name from the URL
                            resource_name = extract_resource_name(profile)
                            all_targets.append(resource_name)
                    else:
                        # Single target profile
                        resource_name = extract_resource_name(target_profiles)
                        all_targets.append(resource_name)
            
            if all_targets:
                print(f"  References to: {', '.join(all_targets)}")
            else:
                print("  References to: Any resource (no specific target profiles)")
                
            print()  # Empty line between elements
            processed_paths.add(path)
        
        # Now check for references in child elements
        child_elements = collect_child_elements(elements, path)
        for child_elem in child_elements:
            if "type" not in child_elem or not child_elem["type"]:
                continue
                
            child_path = child_elem.get("path", "unknown")
            
            # Skip if already processed
            if child_path in processed_paths:
                continue
                
            # Skip if child has max=0 or any parent is disabled
            if child_elem.get("max") == "0" or has_disabled_parent(child_path, elements):
                continue
                
            # Check if any of the child types is a Reference
            child_reference_types = [t for t in child_elem["type"] if t.get("code") == "Reference"]
            
            if child_reference_types:
                reference_count += 1
                child_cardinality = f"[{child_elem.get('min', '?')}..{child_elem.get('max', '?')}]"
                
                print(f"Path: {child_path} {child_cardinality}")
                
                # Extract all possible reference targets
                child_targets = []
                for ref_type in child_reference_types:
                    if "targetProfile" in ref_type:
                        target_profiles = ref_type["targetProfile"]
                        if isinstance(target_profiles, list):
                            # Multiple target profiles
                            for profile in target_profiles:
                                # Extract the resource name from the URL
                                resource_name = extract_resource_name(profile)
                                child_targets.append(resource_name)
                        else:
                            # Single target profile
                            resource_name = extract_resource_name(target_profiles)
                            child_targets.append(resource_name)
                
                if child_targets:
                    print(f"  References to: {', '.join(child_targets)}")
                else:
                    print("  References to: Any resource (no specific target profiles)")
                    
                print()  # Empty line between elements
                processed_paths.add(child_path)
    
    if reference_count == 0:
        print("No reference elements found in this structure definition.")

def extract_resource_name(profile_url: str) -> str:
    """Extract resource name from a profile URL."""
    # Try to extract resource name from various URL formats
    # Format 1: http://hl7.org/fhir/StructureDefinition/Patient
    # Format 2: http://hl7.org/fhir/Profile/Patient
    # Format 3: urn:profile:Patient
    
    # First, split by '/' or ':' and get the last part
    parts = profile_url.split('/')
    if len(parts) > 1:
        last_part = parts[-1]
    else:
        parts = profile_url.split(':')
        last_part = parts[-1]
    
    # Handle fragments like Patient#fragment
    fragment_parts = last_part.split('#')
    return fragment_parts[0]

def build_element_tree(elements: List[Dict]) -> Dict[str, Any]:
    """Build a hierarchical tree of elements."""
    root = {}
    
    for elem in elements:
        path = elem.get("path", "")
        path_parts = path.split(".")
        
        # Skip elements without a proper path
        if not path_parts:
            continue
        
        current = root
        for i, part in enumerate(path_parts):
            if i == len(path_parts) - 1:
                # Last part - store the element
                current[part] = {
                    "element": elem,
                    "children": {}
                }
            else:
                # Not the last part - navigate or create path
                if part not in current:
                    current[part] = {
                        "element": None,
                        "children": {}
                    }
                current = current[part]["children"]
    
    return root

def print_element_tree(tree: Dict[str, Any], indent: int = 0, is_last: bool = True) -> None:
    """Print the element tree in a hierarchical format."""
    for i, (name, node) in enumerate(tree.items()):
        is_last_item = i == len(tree) - 1
        
        # Print the current node
        prefix = "    " * indent
        if indent > 0:
            if is_last:
                prefix = prefix[:-4] + "└── "
            else:
                prefix = prefix[:-4] + "├── "
        
        elem = node["element"]
        if elem:
            type_info = ""
            if "type" in elem and elem["type"]:
                types = [t.get("code", "unknown") for t in elem["type"]]
                type_info = f" ({', '.join(types)})"
            
            cardinality = f"[{elem.get('min', '?')}..{elem.get('max', '?')}]"
            print(f"{prefix}{name} {cardinality}{type_info}")
        else:
            print(f"{prefix}{name}")
        
        # Print children
        if node["children"]:
            child_indent = indent + 1
            print_element_tree(node["children"], child_indent, is_last_item)

def main():
    # Print command line arguments for debugging
    print(f"Command line arguments: {sys.argv}")
    
    args = parse_arguments()
    
    # Print parsed arguments
    print(f"Path: {args.path}")
    print(f"Format: {args.format}")
    print(f"Filter: {args.filter}")
    
    # Load the Structure Definition
    structure_definition = load_fhir_structure_definition(args.path)
    
    # Get resource type and version info
    resource_type = structure_definition.get("type", "Unknown")
    fhir_version = structure_definition.get("fhirVersion", "Unknown")
    
    print(f"Resource: {resource_type} (FHIR version: {fhir_version})")
    
    # Extract and filter elements
    elements = extract_snapshot_elements(structure_definition)
    if args.filter:
        elements = filter_elements_by_path(elements, args.filter)
        print(f"Filtered by: {args.filter}")
    
    print(f"Total elements: {len(elements)}")
    print()
    
    # Format and display elements
    if args.format == "simple":
        format_simple_output(elements)
    elif args.format == "detailed":
        format_detailed_output(elements)
    elif args.format == "tree":
        root_tree = build_element_tree(elements)
        print_element_tree(root_tree)
    elif args.format == "references":
        format_references_output(elements)

if __name__ == "__main__":
    main()