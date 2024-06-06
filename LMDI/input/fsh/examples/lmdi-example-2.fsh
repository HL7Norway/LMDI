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
* identifier.value = "FEST-XXX-9e6c620b-5d09-4f27-9ee1-b108e7f338ab"