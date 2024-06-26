// Eksempel inline/contained, minimalt, logiske referanser

Instance: Administrering-30
InstanceOf: MedicationAdministration
Description: "Utfyllende eksempel - minimalt, logiske referanser"
* status = #completed
* medicationReference.identifier.system = "uri:eu:spor:idmp:mpid:dummy"
* medicationReference.identifier.value = "1a38f25a8791fc3270e7c388f2031eee"
* subject = Reference(https://fhi.no/fhir/lmdi/pasient/12345678)
* context = Reference(uuid:69fb46ff-8874-4cda-bc6a-53ea6933026a)
* performer.actor.identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"
* performer.actor.identifier.value = "9144900"
* effectiveDateTime = "2024-05-28"
* dosage.route.coding.system = "http://snomed.info/sct"
* dosage.route.coding.code = #47625008
* dosage.route.coding.display = "Intravenous route (qualifier value)"
* dosage.dose.value = 100.0
* dosage.dose.system = "http://unitsofmeasure.org"
* dosage.dose.code = #mg