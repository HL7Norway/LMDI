import os
import sys
import re
import uuid
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET
from xml.dom import minidom

class FHIRProfileParser:
    def __init__(self):
        self.references: Dict[str, List[Tuple[str, str, str]]] = {}
        self.namespaces = {
            "xmi": "http://www.omg.org/XMI",
            "uml": "http://www.omg.org/spec/UML/20131001",
            "ea": "http://www.sparxsystems.com/ns/ea"
        }

    def parse_file(self, file_path: str) -> None:
        """Parse en FSH-fil for FHIR-profiler og referanser."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Hopp over filer som inneholder instanser
        if content.strip().startswith('Instance:'):
            return

        # Finn profilnavn
        profile_match = re.search(r'^Profile:\s*(\w+)', content, re.MULTILINE)
        if not profile_match:
            return

        profile_name = profile_match.group(1)
        self.references[profile_name] = []

        # Finn elementer med kardinalitet 0..0
        zero_elements = set()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '0..0' in line:
                elem_match = re.search(r'\*\s+(\w+)', line)
                if elem_match:
                    zero_elements.add(elem_match.group(1))

        # Parse referanser og kardinaliteter
        for i, line in enumerate(lines):
            if 'Reference(' in line and 'only' in line:
                elem_match = re.search(r'\*\s+(\w+)', line)
                ref_match = re.search(r'Reference\((\w+)\)', line)

                if elem_match and ref_match:
                    element = elem_match.group(1)
                    if element not in zero_elements:
                        target = ref_match.group(1)
                        cardinality = "0..1"  # Standardkardinalitet
                        for j in range(max(0, i-2), min(len(lines), i+3)):
                            card_match = re.search(rf'\*\s+{element}\s+(\d+\.\.[0-9*]+)', lines[j])
                            if card_match:
                                cardinality = card_match.group(1)
                                break
                        self.references[profile_name].append((target, element, cardinality))

    def generate_xmi(self) -> ET.Element:
        """Generer en XMI-fil med UML-klasser, assosiasjoner og diagram."""
        # Registrer namespaces for korrekt prefiksbruk
        for prefix, uri in self.namespaces.items():
            ET.register_namespace(prefix, uri)

        # Opprett rot-element med namespaces
        xmi = ET.Element(ET.QName(self.namespaces["xmi"], "XMI"), 
                        attrib={
                            "version": "2.1",
                            ET.QName(self.namespaces["xmi"], "id"): f"root_{uuid.uuid4()}"
                        },
                        nsmap=self.namespaces)

        # Opprett modell
        model = ET.SubElement(xmi, ET.QName(self.namespaces["uml"], "Model"), 
                            attrib={
                                ET.QName(self.namespaces["xmi"], "id"): f"model_{uuid.uuid4()}",
                                "name": "FHIR Profiles"
                            })

        # Opprett pakke
        package = ET.SubElement(model, ET.QName(self.namespaces["uml"], "PackagedElement"),
                              attrib={
                                  ET.QName(self.namespaces["xmi"], "type"): "uml:Package",
                                  ET.QName(self.namespaces["xmi"], "id"): f"pkg_{uuid.uuid4()}",
                                  "name": "FHIR Resources"
                              })

        # Opprett klasser
        classes = {}
        for profile in self.references:
            class_id = f"cls_{uuid.uuid4()}"
            classes[profile] = class_id
            ET.SubElement(package, ET.QName(self.namespaces["uml"], "PackagedElement"),
                        attrib={
                            ET.QName(self.namespaces["xmi"], "type"): "uml:Class",
                            ET.QName(self.namespaces["xmi"], "id"): class_id,
                            "name": profile
                        })

        # Opprett assosiasjoner
        for source, refs in self.references.items():
            for target, element, cardinality in refs:
                assoc_id = f"assoc_{uuid.uuid4()}"
                association = ET.SubElement(package, ET.QName(self.namespaces["uml"], "PackagedElement"),
                                          attrib={
                                              ET.QName(self.namespaces["xmi"], "type"): "uml:Association",
                                              ET.QName(self.namespaces["xmi"], "id"): assoc_id
                                          })

                # Kildeende
                ET.SubElement(association, ET.QName(self.namespaces["uml"], "memberEnd"),
                            attrib={
                                ET.QName(self.namespaces["xmi"], "idref"): classes[source]
                            })

                # Målende
                owned_end = ET.SubElement(association, ET.QName(self.namespaces["uml"], "ownedEnd"),
                                        attrib={
                                            ET.QName(self.namespaces["xmi"], "type"): "uml:Property",
                                            ET.QName(self.namespaces["xmi"], "id"): f"end_{uuid.uuid4()}",
                                            "name": element,
                                            "type": classes[target],
                                            "association": assoc_id
                                        })
                upper = "1" if cardinality == "0..1" else cardinality.split('..')[-1]
                ET.SubElement(owned_end, ET.QName(self.namespaces["uml"], "upperValue"),
                            attrib={"value": upper})

        # Opprett diagram
        diagram = ET.SubElement(package, ET.QName(self.namespaces["uml"], "PackagedElement"),
                              attrib={
                                  ET.QName(self.namespaces["xmi"], "type"): "uml:Diagram",
                                  ET.QName(self.namespaces["xmi"], "id"): f"diag_{uuid.uuid4()}",
                                  "name": "FHIR Resources Diagram"
                              })
        diagram.set(ET.QName(self.namespaces["ea"], "diagramType"), "Class")
        diagram.set(ET.QName(self.namespaces["ea"], "guid"), str(uuid.uuid4()))

        # Plasser elementer på diagrammet
        x_pos, y_pos = 100, 100
        for i, (cls_name, cls_id) in enumerate(classes.items()):
            diagram_object = ET.SubElement(diagram, ET.QName(self.namespaces["ea"], "DiagramObject"),
                                        attrib={
                                            ET.QName(self.namespaces["xmi"], "id"): f"dobj_{uuid.uuid4()}",
                                            ET.QName(self.namespaces["ea"], "geometry"): f"Left={x_pos};Top={y_pos};Right={x_pos+200};Bottom={y_pos+100};",
                                            ET.QName(self.namespaces["ea"], "element"): cls_id
                                        })
            if i % 2 == 0:
                x_pos += 300
                y_pos = 100
            else:
                y_pos += 150

        return xmi

def main():
    """Hovedfunksjon for å parse FSH-filer og generere XMI."""
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

    # Generer XMI
    xmi_root = parser.generate_xmi()
    xml_str = ET.tostring(xmi_root, encoding="utf-8", method="xml")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

    # Skriv XMI til fil
    output_path = os.path.join(os.path.dirname(path), "fhir_diagram.xmi")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"XMI-fil generert: {output_path}")

if __name__ == "__main__":
    main()