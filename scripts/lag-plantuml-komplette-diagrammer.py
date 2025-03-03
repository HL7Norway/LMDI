import os
import json
import sys
from collections import OrderedDict

def log_warning(message):
    print(f"[WARNING] {message}", file=sys.stderr)

def find_structure_definitions(path):
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files 
        if file.startswith('StructureDefinition-') and file.endswith('.json')
    ]

def parse_structure_definition(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def build_profile_mapping(structures):
    profile_map = {}
    for struct in structures:
        # Bare resources
        if struct.get('kind') == 'resource':
            # Legg til i map for URL -> Name
            profile_map[struct.get('url')] = struct.get('name', 'Unknown')
    log_warning(f"Built profile mapping with {len(profile_map)} entries.")
    return profile_map

def clean_type_name(type_name):
    # Fjerner eventuelle "http://hl7.org/fhirpath/System." prefikser
    return type_name.replace("http://hl7.org/fhirpath/System.", "")

def extract_resources_and_references(structures, profile_map):
    resources = OrderedDict()
    references = {}

    for struct in structures:
        if struct.get('kind') != 'resource':
            continue

        profile_name = struct.get('name', 'Unknown')
        base_resource = struct.get('type')

        # Finn alle path’er (fra differensialen) som har max=0:
        turned_off_paths = set()
        for element in struct.get('differential', {}).get('element', []):
            if element.get('max') == '0':
                turned_off_paths.add(element['path'])

        def is_descendant_of_turned_off(path):
            """
            Returnerer True hvis en forfader av path finnes i turned_off_paths.
            F.eks. hvis path er 'Condition.extension.valueReference'
            og 'Condition.extension' står i turned_off_paths, 
            skal vi hoppe over hele greina.
            """
            parts = path.split('.')
            # Sjekk alle "del paths": Condition, Condition.extension, Condition.extension.valueReference
            for i in range(1, len(parts) + 1):
                ancestor = '.'.join(parts[:i])
                if ancestor in turned_off_paths:
                    return True
            return False

        # For å samle attributtnavn for UML
        attributes = []
        seen_attributes = set()

        # Gå gjennom snapshot-elementene
        for element in struct.get('snapshot', {}).get('element', []):
            path = element.get('path', '')
            if is_descendant_of_turned_off(path):
                # Hele under-treet er skrudd av -> skip
                continue

            # For UML-diagrammet: attributtnavn = siste del av pathen
            attribute = path.split('.')[-1]

            # Hoppe over root-selv (Condition vs Condition.id, Condition.code etc.)
            # f.eks. path=Condition => attribute=Condition
            if attribute == base_resource:
                continue

            # Hent type
            element_type = ', '.join(
                clean_type_name(t.get('code', 'Unknown'))
                for t in element.get('type', [])
            )

            # Filtrer ut duplikater i UML
            if attribute and attribute not in seen_attributes:
                seen_attributes.add(attribute)
                attributes.append(f"{attribute} : {element_type}")

                # Hvis type er Reference(...), så lagre kobling for UML-pil
                if 'type' in element:
                    for t in element['type']:
                        if t.get('code') == 'Reference' and 'targetProfile' in t:
                            for target_url in t['targetProfile']:
                                target_name = profile_map.get(
                                    target_url,
                                    target_url.split('/')[-1]  # fallback
                                )
                                if target_name:
                                    references.setdefault(profile_name, []).append(
                                        (attribute, element_type, target_name)
                                    )
                                else:
                                    log_warning(
                                        f"Dropped reference from {profile_name}.{attribute} "
                                        f"to {target_url} (unknown target)."
                                    )

        resources[profile_name] = attributes

    return resources, references

def generate_plantuml(resources, references):
    output = ['@startuml']
    # Tegn klasser for hver resource
    for resource_name, attributes in resources.items():
        output.append(f'class "{resource_name}" {{')
        for attr in attributes:
            output.append(f'  + {attr}')
        output.append('}\n')

    # Tegn piler for references
    for source, targets in references.items():
        for attribute, element_type, target in targets:
            output.append(f'"{source}" --> "{target}" : {attribute} ({element_type})')

    output.append('@enduml')
    return '\n'.join(output)

def main():
    # Hent mappe/filsti
    path = sys.argv[1] if len(sys.argv) > 1 else input("Oppgi sti til StructureDefinition-filer eller mappe: ")
    structure_files = find_structure_definitions(path)
    if not structure_files:
        log_warning("Ingen StructureDefinition-filer funnet.")
        return

    # Les inn alle StructureDefinition-JSON
    structures = [parse_structure_definition(f) for f in structure_files]

    # Bygg oversikt over URL -> ressurstype (til UML-lenker)
    profile_map = build_profile_mapping(structures)

    # Ekstraher ressurser (klasser) og referanser (piler)
    resources, refs = extract_resources_and_references(structures, profile_map)

    # Generer PlantUML
    plantuml = generate_plantuml(resources, refs)
    print(plantuml)

    log_warning("PlantUML generation completed.")

if __name__ == '__main__':
    main()
