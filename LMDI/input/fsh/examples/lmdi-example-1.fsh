// Eksempel inline/contained

Alias: $SCT = http://snomed.info/sct

Instance: Administrering-10
InstanceOf: MedicationAdministration
Description: "Utfyllende eksempel"
* status = #completed
* medicationReference = Reference(Medisin-10)
* subject = Reference(Pasient-20)
* performer.actor = Reference(Helsepersonell-10)
* effectiveDateTime = "2024-05-28"
* contained[+] = Medisin-10
* contained[+] = Pasient-20
* contained[+] = Helsepersonell-10

Instance: Medisin-10
InstanceOf: Medication
Usage: #inline
* identifier.value = "FEST-XXX-9e6c620b-5d09-4f27-9ee1-b108e7f338ab"
* code.coding.system = $SCT
* code.coding = #430127000
* code.coding.display = "Oxycodone-containing product in oral dose form"
* code.text = "Oxycodone"

Instance: Pasient-20
InstanceOf: Patient
Description: "Eksempel på pasient med fødselsnummer"
Usage: #inline
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.1"
* identifier.value = "13031353453"
* name.family = "Kopter"
* name.given = "Rosa Eli"

Instance: Helsepersonell-10
InstanceOf: Practitioner
Usage: #inline
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.4"
* identifier.value = "9144900"
* name.family = "Lin"
* name.given = "Rita"