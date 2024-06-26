// Eksempel inline/contained

Alias: $SCT = http://snomed.info/sct

Instance: Administrering-10
InstanceOf: MedicationAdministration
Description: "Utfyllende eksempel, f.eks. om alt rapporteres som én melding. Bruker contained - bundle er å foretrekke for melding."
* status = #completed
* medicationReference = Reference(Medisin-10)
* subject = Reference(Pasient-20)
* context = Reference(Institusjonsopphold-2-Sykehjem)
* performer[0].actor = Reference(Helsepersonell-10)
* performer[+].actor = Reference(RolleHelsepersonell-10)
* effectiveDateTime = "2024-05-28T13:14:00Z"
* contained[+] = Medisin-10
* contained[+] = Pasient-20
* contained[+] = Helsepersonell-10
* contained[+] = RolleHelsepersonell-10
* contained[+] = Institusjonsopphold-2-Sykehjem
* contained[+] = Organisasjon-2-Eldrehjem

Instance: Medisin-10
InstanceOf: Medication
Usage: #inline
* code.coding[0].system = "http://dmp.no/fhir/NamingSystem/festLegemiddelDose"
* code.coding[=] = #ID_48BD33D2-2838-4B81-8225-02391B7A4516
* code.coding[=].display = "Oxycodone Orifarm mikst oppl 1 mg/ml"
* code.coding[+].system = $SCT
* code.coding[=] = #414984009
* code.coding[=].display = "Product containing oxycodone (medicinal product)"
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

Instance: RolleHelsepersonell-10
InstanceOf: PractitionerRole
Usage: #inline
// TODO #14 Dårlig kodeverk for PractitionerRole fra no-basis-PractitionerRole
* identifier.system = "urn:oid:2.16.578.1.12.4.1.1.9034"
* identifier.value = #9

Instance: Institusjonsopphold-2-Sykehjem
InstanceOf: EpisodeOfCare
Description: "Eksempel på institusjonsopphold med EpisodeOfCare"
Usage: #inline
* status = #active
* patient = Reference(Pasient-20)
* managingOrganization = Reference(Organisasjon-2-Eldrehjem)
* period.start = "2019-04-01"

Instance: Organisasjon-2-Eldrehjem
InstanceOf: Organization
Description: "Eksempel på organisasjon - Primærhelsetjeneste"
Usage: #inline
* identifier.system = "urn:oid:2.16.578.1.12.4.1.4.101"
* identifier.value = "1234567890"
* name = "Lykkedalen eldrehjem"