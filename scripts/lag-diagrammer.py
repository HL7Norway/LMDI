import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class FHIRProfileParser:
    def __init__(self):
        self.references: Dict[str, List[Tuple[str, str, str]]] = {}
        
    def parse_file(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Skip if file contains Instance definitions
        if content.strip().startswith('Instance:'):
            return
            
        # Get profile name and parent
        profile_match = re.search(r'^Profile:\s*(\w+)', content, re.MULTILINE)
        if not profile_match:
            return
            
        profile_name = profile_match.group(1)
        self.references[profile_name] = []
        
        # Find zero cardinality elements
        zero_elements = set()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '0..0' in line:
                elem_match = re.search(r'\*\s+(\w+)', line)
                if elem_match:
                    zero_elements.add(elem_match.group(1))
        
        # Parse references and cardinalities
        for i, line in enumerate(lines):
            if 'Reference(' in line and 'only' in line:
                elem_match = re.search(r'\*\s+(\w+)', line)
                ref_match = re.search(r'Reference\((\w+)\)', line)
                
                if elem_match and ref_match:
                    element = elem_match.group(1)
                    if element not in zero_elements:
                        target = ref_match.group(1)
                        
                        # Look for cardinality in nearby lines
                        cardinality = "0..1"  # default
                        for j in range(max(0, i-2), min(len(lines), i+3)):
                            card_match = re.search(rf'\*\s+{element}\s+(\d+\.\.[0-9*]+)', lines[j])
                            if card_match:
                                cardinality = card_match.group(1)
                                break
                                
                        self.references[profile_name].append((target, element, cardinality))

    def generate_plantuml(self) -> str:
        uml = ["@startuml", 
               'skinparam class {',
               '    BackgroundColor White',
               '    ArrowColor Black',
               '    BorderColor Black',
               '}',
               "title FHIR Resource References\n"]
        
        # Define classes
        classes = set()
        for profile in self.references:
            classes.add(profile)
            for ref in self.references[profile]:
                classes.add(ref[0])
        
        for cls in sorted(classes):
            uml.append(f"class {cls}")
        uml.append("")
        
        # Add relationships
        for profile, refs in self.references.items():
            for target, element, cardinality in refs:
                uml.append(f'{profile} --> "{element}" {target} : {cardinality}')
        
        uml.extend(["", "@enduml"])
        return "\n".join(uml)

def main():
    default_path = r"C:\dev\LMDI\LMDI\input\fsh\profiles"
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input(f"Enter path to FSH file or directory [{default_path}]: ").strip()
        if not path:
            path = default_path
    
    parser = FHIRProfileParser()
    
    if os.path.isfile(path):
        parser.parse_file(path)
    elif os.path.isdir(path):
        for file in Path(path).glob("*.fsh"):
            parser.parse_file(str(file))
            print(f"Processed: {file}")
    else:
        print(f"Error: Path {path} does not exist")
        return
    
    plantuml = parser.generate_plantuml()
    print(plantuml)

if __name__ == "__main__":
    main()