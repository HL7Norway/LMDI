// Eksempel inline/contained, minimalt

Instance: Administrering-20
InstanceOf: MedicationAdministration
Description: "Utfyllende eksempel - andre referanser"
* status = #completed
* medicationReference = Reference(medisin-91171f8e-b615-41ba-881a-87b8e8075611)
* subject = Reference(https://fhi.no/fhir/lmdi/pasient/12345678)
* context = Reference(uuid:9b62d7e8-df64-47b7-9fe1-38bc45795d82)
* performer.actor = Reference(https://fhir.npr.no/helsepersonell/1234567890)
* effectiveDateTime = "2024-05-28"
* dosage.text = "100 mg"
* dosage.dose.value = 100.0
* dosage.dose.unit = "mg"
* dosage.dose.system = "http://unitsofmeasure.org"
* dosage.dose.code = #mg
* contained[+] = medisin-91171f8e-b615-41ba-881a-87b8e8075611

Instance: medisin-91171f8e-b615-41ba-881a-87b8e8075611
InstanceOf: Medication
Usage: #inline
* code.coding.system = "http://dmp.no/fhir/NamingSystem/festLegemiddelPakning"
* code.coding.code = #ID_00B35335-0DF7-4C98-8A0A-1148F4599D21
* code.coding.display = "Botox pulv til inj væske, oppl 50 E"
