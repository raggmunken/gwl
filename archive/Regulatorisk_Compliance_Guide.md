# REGULATORISK COMPLIANCE-GUIDE
## Genetic Wellness Labs AB
### Fullständig svensk och EU-lagstiftning

**Version:** 1.0
**Datum:** Januari 2026
**Gäller för:** DNA-testning + Kosttillskott-prenumeration + Dietist-konsultationer

---

## ⚠️ EXECUTIVE SUMMARY - KRITISKA COMPLIANCE-KRAV

### **AKUTA RISKER ATT HANTERA:**

| Risk | Konsekvens om missad | Prioritet | Åtgärd |
|------|---------------------|-----------|--------|
| **DNA-test utan CE-märkning** | Böter, försäljningsförbud | 🔴 **KRITISK** | Avgör om IVDR gäller |
| **Genetiska data utan GDPR-skydd** | 4% av omsättning i böter | 🔴 **KRITISK** | DPO + Samtycke |
| **Medicinska påståenden** | Marknadsstörningsavgift 4% | 🔴 **KRITISK** | Granska ALL copy |
| **Ingen patientförsäkring** | Personligt ansvar vid skada | 🟠 **HÖG** | Teckna försäkring |
| **Felaktig märkning kosttillskott** | Försäljningsförbud | 🟠 **HÖG** | Följ checklista |

---

## 📋 INNEHÅLLSFÖRTECKNING

1. DNA-testning och IVDR
2. GDPR och genetiska data
3. Kosttillskott-reglering
4. Dietist-verksamhet
5. Marknadsföring och hälsopåståenden
6. E-handel och konsumenträtt
7. Implementation Roadmap
8. Kostnadsuppskattning för compliance
9. Checklistor och mallar

---

## 1. DNA-TESTNING OCH IVDR

### 🎯 HUVUDFRÅGA: Är vårt DNA-test en medicinteknisk produkt?

**EU IVDR (2017/746) gäller för in vitro-diagnostiska medicintekniska produkter.**

### **BESLUTSTRÄ D:**

```
Gör DNA-testet medicinska påståenden?
│
├─ JA (diagnostiserar, förutsäger sjukdom, behandlingsrekommendationer)
│  └─> MEDICINTEKNISK PRODUKT under IVDR
│     ├─ Kräver CE-märkning
│     ├─ Klass C troligen (genetiska tester)
│     ├─ Deadline: Maj 2026
│     ├─ Kostnad: 500K-2M SEK
│     └─ Tid: 12-24 månader
│
└─ NEJ (endast "wellness-information", intressant genetisk info)
   └─> MÖJLIGEN utanför IVDR som "wellness-produkt"
      ├─ INGEN CE-märkning krävs
      ├─ Kostnad: 0 SEK
      ├─ MEN: Gråzon, EU är striktare än USA
      └─ Risk: Läkemedelsverket kan ändå klassificera som IVD
```

### **REKOMMENDATION: WELLNESS-POSITIONERING**

För att undvika IVDR-kraven (spara 500K-2M SEK och 12-24 månader):

**GÖR:**
- ✅ Marknadsför som "wellness och livsstilsinformation"
- ✅ "Intressant genetisk information om näringsämnen"
- ✅ "Kan ge indikationer om hur din kropp kan reagera på..."
- ✅ Dietist använder resultaten som ETT av flera verktyg

**GÖR INTE:**
- ❌ "Diagnostiserar" något
- ❌ "Förutsäger risker för sjukdomar"
- ❌ "Behandlar" eller "förebygger" medicinska tillstånd
- ❌ "Din DNA visar att du HAR brist på..."

**Exempel på godkänd copywriting:**
> "Vårt DNA-test analyserar genetiska variationer relaterade till hur kroppen kan metabolisera näringsämnen. Resultaten granskas av en legitimerad dietist som använder informationen tillsammans med din livsstil och kostvanor för att skapa personliga kosttillskotts-rekommendationer."

**INTE:**
> "Vårt DNA-test diagnostiserar dina nutritionsbrister och visar vilka vitaminer du saknar."

### **OM NI VÄLJER WELLNESS-VÄGEN:**

**Juridisk backup:**
1. **Konsultera advokat** specialiserad på medicinteknisk rätt (kostnad: 30-50K)
2. **Dokumentera beslutet** varför ni anser produkten faller utanför IVDR
3. **Ha beredskap** om Läkemedelsverket ifrågasätter

**Kontakter:**
- Advokat: [Setterwalls](https://www.setterwalls.se/) specialiserar sig på Life Science
- Konsult: [MedTech Advise](https://www.medtechadvise.se/)

---

### **LABORATORIEKRAV (OAVSETT IVDR-STATUS)**

**OBLIGATORISKT: Använd ISO-ackrediterat labb**

**ISO 17025:2018** - För icke-medicinska tester:
- Ackreditering från Swedac eller motsvarande EU-organ
- Kvalitetssäkring och spårbarhet
- Validerade analysmetoder
- Kompetent personal

**Svenska ISO 17025-ackrediterade DNA-labb:**
- [NGI Sweden](https://ngisweden.scilifelab.se/) - Genotypning och sekvensering
- [Clinical Genomics](https://www.clinicalgenomics.se/) - Klinisk genetik
- [SciLifeLab](https://www.scilifelab.se/) - Forskningslabb

**Kostnad:**
- DNA-analys per prov: 400-800 SEK (volymberoende)
- Uppsättningsavgift: 50-100K (initialt partnerskapavtal)

**VIKTIGT: Personuppgiftsbiträdesavtal (PUB)**
- Måste finnas skriftligt avtal med labbet
- Labbet = personuppgiftsbiträde
- Ni = personuppgiftsansvarig
- Mall finns i Bilaga A

---

### **DOKUMENTATION SOM MÅSTE FINNAS:**

1. **Riskbedömning** varför produkten (om wellness) faller utanför IVDR
2. **Laboratoriekontrakt** med ISO-ackrediterat labb
3. **Personuppgiftsbiträdesavtal** med labbet
4. **Validering** av DNA-analysmetod (från labbet)
5. **Kvalitetssäkringsdokumentation**

**Kostnad för dokumentation:** 50-100K (konsult + advokat)
**Tid:** 2-3 månader

---

## 2. GDPR OCH GENETISKA DATA

### 🔴 KRITISKT: Genetiska data = Särskilda personuppgifter

**GDPR Artikel 9:** Behandling av genetiska data är **FÖRBJUDEN** utom vid uttryckligt samtycke.

### **OBLIGATORISKA ÅTGÄRDER:**

#### **1. UTTRYCKLIGT SAMTYCKE**

**Krav på samtycket:**
- Frivilligt (verkligt val)
- Specifikt (för exakt ändamål)
- Informerat (full information först)
- Otvetydigt (aktiv handling, ej förkryssad)
- Dokumenterat (kunna bevisa)
- Återkallbart (enkelt ta tillbaka)

**Mall för samtyckestext (se Bilaga B):**

**INFORMATIONSKRAV INNAN SAMTYCKE:**
1. Vem som är personuppgiftsansvarig (Genetic Wellness Labs AB)
2. Exakt vad genetiska data används till
3. Vilka som har tillgång (labb, dietist)
4. Hur länge data sparas (X år)
5. Överföring till tredje part (labb inom EU)
6. Rätt att återkalla samtycke
7. Rätt till radering
8. Kontaktuppgifter till DPO

**Implementering:**
- Samtyckesformulär i onboarding-flödet
- Separat checkbox för genetiska data (ej bundlad med andra villkor)
- Spara tidsstämpel och IP för samtycke
- Bekräftelse via e-post

---

#### **2. DATASKYDDSOMBUD (DPO) - TROLIGEN OBLIGATORISKT**

**IMY:s bedömning:**
Företag som behandlar känsliga personuppgifter (genetiska data) i "stor omfattning" måste utse DPO.

**"Stor omfattning" för er verksamhet:**
- År 1: 340 kunder → Gråzon
- År 2: 720 kunder → Troligen JA
- År 3: 1440 kunder → Definitivt JA

**REKOMMENDATION: Utse DPO från dag 1**

**Varför?**
- Visar att ni tar GDPR på allvar (bra för investerare)
- Undviker böter (IMY kan bötfälla retroaktivt)
- Professionell hantering av genetiska data

**Alternativ:**

| Alternativ | Kostnad | För/Nackdelar |
|-----------|---------|---------------|
| **Extern DPO (konsult)** | 10-20K/mån | ✅ Expertis, ❌ Dyrare |
| **Deltids-intern DPO** | Lön 20K/mån + utbildning 50K | ✅ Billigare, ❌ Mindre expertis |
| **DPO-as-a-Service** | 5-10K/mån | ✅ Skalbart, ✅ Professionellt |

**Rekommenderad leverantör:**
- [GDPR Advisor](https://www.gdpradvisor.se/) - DPO-as-a-Service 8-12K/mån
- [DPO Sweden](https://dposweden.se/) - Specialist på healthtech

**DPO:s ansvar:**
- Informera och ge råd om GDPR
- Övervaka efterlevnad
- Vara kontaktpunkt för IMY
- Samarbeta med IMY vid inspektioner
- Riskbedömningar och DPIA (Data Protection Impact Assessment)

**Anmälan till IMY:**
- DPO:s namn och kontaktuppgifter anmäls via [IMY:s webbformulär](https://www.imy.se/)
- Kostnad: Gratis
- Tid: 5 minuter

---

#### **3. KONSEKVENSBEDÖMNING (DPIA)**

**Obligatoriskt enligt GDPR Artikel 35:**

När behandling av personuppgifter "sannolikt medför hög risk" krävs en DPIA.

**Genetiska data = Hög risk → DPIA KRÄVS**

**Vad är DPIA?**
- Data Protection Impact Assessment
- Systematisk analys av risker med databehandlingen
- Åtgärder för att minska risker

**Innehåll i DPIA:**
1. Beskrivning av behandlingen och ändamål
2. Bedömning av nödvändighet och proportionalitet
3. Bedömning av risker för individers rättigheter
4. Åtgärder för att hantera riskerna

**Vem gör DPIA?**
- Personuppgiftsansvarig (ni) tillsammans med DPO
- Kan anlita extern konsult

**Kostnad:** 30-80K för professionell DPIA
**Tid:** 4-8 veckor

**VIKTIGT:** DPIA måste göras INNAN ni börjar behandla genetiska data!

---

#### **4. DATALAGRING OCH RADERING**

**Lagringsminimering (GDPR Artikel 5.1e):**
- Data får inte sparas längre än nödvändigt
- Sätt specifika lagringsfrister

**Rekommenderade lagringsfrister:**

| Datatyp | Lagringsfrist | Motivering |
|---------|---------------|------------|
| **Genetisk rådata** | 3 år efter sista kontakt | Möjlighet till reanalys om ny vetenskap |
| **Analysresultat** | 5 år | Uppföljning och historik |
| **Dietist-journal** | 10 år | Patientdatalagen krav |
| **Beställningsdata** | 7 år | Bokföringslagen |
| **Marknadsföringssamtycke** | Tills återkallat | |

**Rutiner för radering:**
- Automatisk gallring efter lagringsfrister
- Manuell granskning kvartalsvis
- När kund begär radering: 30 dagar max
- Loggning av alla raderingar

**"Rätten att bli glömd" (GDPR Artikel 17):**

Kund kan begära radering om:
- Data inte längre behövs
- Samtycke återkallas
- Data behandlats olagligt
- Ingen legal grund längre finns

**Undantag från radering:**
- Juridisk skyldighet (bokföringslagen 7 år)
- Patientjournal (10 år enligt patientdatalagen)

**IMPLEMENTERING:**
- Funktion i kundkonto: "Radera min data"
- Process: Manuell granskning → Radering inom 30 dagar → Bekräftelse
- Spara logg att radering genomförts (enligt bokföringslag)

---

#### **5. SÄKERHETSÅTGÄRDER**

**GDPR Artikel 32:** Lämpliga tekniska och organisatoriska åtgärder.

**Tekniska åtgärder:**
- ✅ Kryptering av genetiska data (AES-256)
- ✅ Pseudonymisering (ID-nummer istället för personnummer i databas)
- ✅ Backup (daglig, krypterad, geografiskt separerad)
- ✅ Åtkomstloggning (vem såg vad när)
- ✅ 2FA (tvåfaktorsautentisering) för alla användare
- ✅ HTTPS (SSL-certifikat)
- ✅ Säker filöverföring till labb (SFTP eller krypterad e-post)

**Organisatoriska åtgärder:**
- ✅ Behörighetsstyrning (minsta behörighet-principen)
- ✅ Sekretessavtal med all personal
- ✅ GDPR-utbildning för all personal (årligen)
- ✅ Incidenthanteringsplan
- ✅ Regelbundna säkerhetsrevisioner

**Kostnad för säkerhet:**
- IT-säkerhetskonsult: 50-100K (initial setup)
- Löpande: 10-20K/mån (säkerhetsövervakning)

---

#### **6. PERSONUPPGIFTSINCIDENT (DATA BREACH)**

**Vad räknas som incident?**
- Obehörig åtkomst till genetiska data
- Förlust av data (ej backup)
- Läckage (e-post till fel person)
- Hackerattack

**SKYLDIGHETER:**

**Till IMY:**
- Anmäla inom **72 timmar** om incident kan medföra risk
- För genetiska data = nästan alltid risk
- Blankett: [IMY:s anmälan om personuppgiftsincident](https://www.imy.se/)

**Till drabbade personer:**
- Informera "utan onödigt dröjsmål" om hög risk
- Beskriva vad som hänt och vilka åtgärder ni vidtar

**Sanktioner vid underlåtenhet:**
- Böter: Upp till 10 miljoner EUR eller 2% av global omsättning

**FÖRBEREDELSE:**
- Incidenthanteringsplan (mall i Bilaga C)
- Kontaktuppgifter till DPO och IMY lättillgängliga
- Årlig övning av incidenthantering

---

### **SAMMANFATTNING GDPR-KOSTNADER:**

| Åtgärd | Engångskostnad | Löpande kostnad/år |
|--------|----------------|-------------------|
| DPO (extern) | 0 | 100-150K |
| DPIA (konsekvensbedömning) | 50-80K | 0 (uppdatering vid ändringar) |
| IT-säkerhet (setup) | 80-120K | 120-200K |
| GDPR-advokat | 50K | 20K |
| **TOTALT ÅR 1** | **180-250K** | **240-370K** |

---

## 3. KOSTTILLSKOTT-REGLERING

### ✅ GODA NYHETER: Ingen notifiering krävs i Sverige!

Livsmedelsverket har inget notifieringssystem för kosttillskott.

**MEN:** Kontroll i efterhand - Livsmedelsverket kan inspektera och förbjuda.

---

### **MÄRKNINGSKRAV (OBLIGATORISKT)**

**Enligt Livsmedelsverket:**

**På förpackningen MÅSTE finnas:**

1. ☑ Produktnamn + "kosttillskott" tydligt
2. ☑ Ingrediensförteckning (i fallande ordning)
3. ☑ Rekommenderad daglig dos
4. ☑ **Varning:** "Rekommenderad dos bör inte överskridas"
5. ☑ **Upplysning:** "Kosttillskott bör inte användas som alternativ till en varierad kost"
6. ☑ **Upplysning:** "Bör förvaras oåtkomligt för barn"
7. ☑ Mängd näringsämnen per daglig dos (med % av DRI)
8. ☑ Näringsdeklaration (enligt EU 1169/2011)
9. ☑ Hållbarhetstid ("Bäst före...")
10. ☑ Förvaringsanvisningar
11. ☑ Namn och adress på livsmedelsföretagare
12. ☑ Ursprungsland (om relevant)
13. ☑ Allergener (om finns)

**Språk:** SVENSKA (eller svenska + engelska)

**Textstorlek:** Minst 1,2 mm (för huvudinformation)

---

### **NÄRINGSDEKLARATION (OBLIGATORISK)**

**Format:**

```
Näringsinnehåll per daglig dos (2 kapslar):
Vitamin D3: 25 μg (500% av DRI*)
Omega-3 (EPA+DHA): 500 mg (-**)
Magnesium: 200 mg (53% av DRI*)

*Dagligt referensintag
**Inget fastställt referensintag
```

**DRI (Dagligt Referensintag):**
- Lista finns i [EU-förordning 1169/2011 bilaga XIII](https://eur-lex.europa.eu/legal-content/SV/TXT/?uri=CELEX%3A02011R1169-20180101)

---

### **HEALTH CLAIMS - HÄLSOPÅSTÅENDEN**

🔴 **KRITISKT: Endast GODKÄNDA påståenden får användas!**

**EU-förordning 1924/2006:**

**Lista över godkända påståenden:**
[EU:s register](https://ec.europa.eu/food/safety/labelling-and-nutrition/nutrition-and-health-claims/eu-register_en)

**Exempel på TILLÅTNA påståenden:**

| Näringsämne | Godkänt påstående |
|-------------|------------------|
| Vitamin D | "Bidrar till immunsystemets normala funktion" |
| Folat | "Bidrar till normal blodbildning" |
| Kalcium | "Bidrar till att bibehålla normal bentäthet" |
| Omega-3 (DHA) | "Bidrar till att bibehålla normal hjärnfunktion" |
| Magnesium | "Bidrar till att minska trötthet och utmattning" |

**FÖRBJUDNA påståenden:**

❌ "Behandlar diabetes"
❌ "Botar hjärtsjukdom"
❌ "Förebygger cancer"
❌ "Garanterad viktminskning"
❌ "Stärker immunförsvaret" (för brett, ej godkänt)
❌ "Probiotika" (ännu ej godkänt i EU)

**Krav för att använda godkänt påstående:**
- Produkten måste innehålla tillräcklig mängd av ämnet
- Måste ange mängden på förpackningen
- Påståendet måste vara exakt som i EU-listan (ej omformulerat)

---

### **PRENUMERATION AV KOSTTILLSKOTT**

**Konsumentverkets krav:**

**MÅSTE vara tydligt FÖRE köp:**
1. ☑ Att det är prenumeration (ej engångsköp)
2. ☑ Pris per månad (SEK/mån)
3. ☑ Totalt pris per faktureringsperiod
4. ☑ Bindningstid (om finns)
5. ☑ Hur man säger upp
6. ☑ Uppsägningstid
7. ☑ När första leveransen kommer
8. ☑ När nästa leverans kommer

**Exempel på godkänd text:**

> **Prenumeration: 695 SEK per månad**
> - Ingen bindningstid
> - Du kan när som helst pausa eller avsluta
> - Första leveransen: Inom 5 arbetsdagar
> - Kommande leveranser: Varje månad
> - Uppsägning: Senast 5 dagar före nästa leverans
> - Kontakt: support@geneticwellness.se

**FÖRBJUDET:**

❌ "Gratis provmånad" om det egentligen startar prenumeration
❌ "Kampanj" som döljer att det är prenumeration
❌ Förkrissad box "Ja, jag vill prenumerera"
❌ Svår att hitta uppsägningsinformation

---

### **SÄKERHET OCH KVALITET**

**Livsmedelsverkets krav:**

1. **GMP (Good Manufacturing Practice):**
   - Tillverkare måste följa GMP
   - EU-regler: Förordning (EG) nr 852/2004
   - Tillverkare ska vara registrerad hos livsmedelsverket

2. **Spårbarhet:**
   - Ni måste kunna spåra varje batch
   - Batchnummer på förpackning
   - Register över leverantörer

3. **Farliga ämnen:**
   - Inga otillåtna växter
   - Inga förbjudna substanser
   - Kontaminanter under gränsvärden

**ÅTGÄRD:**
- Använd ENDAST EU-godkända tillverkare
- Begär GMP-certifikat
- Krav på COA (Certificate of Analysis) för varje batch
- Spara dokumentation i 5 år

---

### **SAMMANFATTNING KOSTTILLSKOTT-KOSTNADER:**

| Åtgärd | Kostnad |
|--------|---------|
| Märkningsdesign (grafisk designer) | 20-40K |
| Regulatorisk granskning av märkning | 15-30K (konsult) |
| Översättning labels till svenska | 5-10K |
| Health claims-granskning (alla produkter) | 20K |
| **TOTALT (engång)** | **60-100K** |

**Löpande:**
- Kvalitetssäkring och COA-granskning: 5K/år per produkt

---

## 4. DIETIST-VERKSAMHET

### **LEGITIMERAD VS ICKE-LEGITIMERAD**

**"Dietist" är skyddad titel enligt patientsäkerhetslagen.**

**Endast legitimerad dietist får:**
- Kalla sig "dietist"
- Arbeta inom sjukvården
- Utfärda remisser
- Behandla medicinska tillstånd (diabetes, obesitas, etc.)

**Icke-legitimerad får:**
- Kalla sig "kostrådgivare", "nutritionist", "hälsocoach"
- Ge kosträd till FRISKA personer
- Arbeta med wellness

---

### 🟢 **REKOMMENDATION: ANVÄND LEGITIMERAD DIETIST**

**Varför?**
1. Högre trovärdighet (viktig för premium-positionering)
2. Bredare kundgrupp (kan hantera kunder med hälsoproblem)
3. Juridiskt säkrare (om kund visar sig ha dold sjukdom)
4. Bättre för investerarpitch

**Legitimation:**
- Söks hos Socialstyrelsen
- Kräver universitetsutbildning (180-240 hp dietistprogram)
- Kostnad: 990 SEK
- Handläggningstid: 3 veckor

---

### **PATIENTJOURNAL (OBLIGATORISKT FÖR LEGITIMERAD DIETIST)**

**Patientdatalagen (2008:355):**

Legitimerad dietist MÅSTE föra patientjournal - gäller även privat verksamhet.

**Journalen ska innehålla:**
1. Patientens identitet (personnummer eller samordningsnummer)
2. Tidpunkt för kontakt
3. Anledning till kontakt (anamnes)
4. Bedömning och kostdiagnos
5. Planerad och genomförd åtgärd (kostråd)
6. Information som getts till patient
7. Uppföljning och resultat
8. Namn och legitimation på dietist

**Tidskrav:**
- Dokumentation så snart som möjligt efter kontakt
- Senast när annan vårdpersonal kan behöva informationen

**Bevarandetid:**
- Minst 10 år efter sista anteckningen
- För barn: Till 10 år efter 18 år

---

### **JOURNALSYSTEM (KRAV)**

**Måste ha:**
- GDPR-kompatibelt
- Behörighetsstyrning (endast dietist ser patientjournal)
- Loggning av åtkomst
- Kryptering
- Backup
- Spårbarhet

**Rekommenderade system:**

| System | Kostnad | För/Nackdelar |
|--------|---------|---------------|
| [Cosmic](https://cosmic.se/) | 300-500 SEK/patient/år | ✅ Svensk, ✅ GDPR, ✅ Dietist-anpassat |
| [Treserva](https://www.treserva.se/) | 200 SEK/patient/år | ✅ Billigare, ❌ Mindre specialiserat |
| [Visiba Care](https://visibacare.com/) | 400 SEK/patient/år | ✅ Videointegration, ✅ GDPR |

**Setup-kostnad:** 10-30K (integration med er plattform)
**Löpande:** 200-500 SEK/patient/år

---

### **PATIENTFÖRSÄKRING (OBLIGATORISK)**

**Patientsäkerhetslagen (2010:659):**

Privat vårdgivare MÅSTE ha patientförsäkring.

**Gäller för legitimerad dietist i privat verksamhet: JA**

**Vad täcker patientförsäkringen?**
- Ersättning till patient vid patientskada
- Skada som uppstått i vården och kunde ha undvikits
- Omfattar fel diagnos, felbehandling, komplikationer

**Försäkringsbolag:**
- [If Patientförsäkring](https://www.if.se/foretag/forsakringar/ansvarsforsakring/patientforsakring)
- [Folksam Patientförsäkring](https://www.folksam.se/foretag/forsakringar/ovrigt/patientforsakring)
- [Länsförsäkringar](https://www.lansforsakringar.se/foretag/forsakring/ovrigt/)

**Kostnad:**
- Årspremie: 15-30K beroende på omsättning
- Självrisk: 0-50K

**Annan relevant försäkring:**
- Yrkesansvarsförsäkring (professional indemnity): 10-20K/år
- Allmän företagsförsäkring: 5-15K/år

---

### **TELEMEDICIN OCH VIDEOKONSULTATION**

✅ **Fullt tillåtet för dietist-konsultationer!**

**Inget särskilt tillstånd krävs.**

**MEN:**
- Samma regler som fysiska besök
- Journalföring MÅSTE ske
- Patientförsäkring täcker även videokonsultation
- Legitimation krävs

**Tekniska krav:**
- GDPR-säker videolösning
- Rekommenderas: Inte vanlig Zoom/Skype (osäkert)
- Bättre: [Visiba Care](https://visibacare.com/), [Capio Go](https://capioGo.se/), [Min Doktor](https://www.mindoktor.se/) (plattformar för vårdgivare)

**Kostnad:**
- GDPR-säker videolösning: 50-100 SEK/session
- Alternativt fast 2-5K/mån

---

### **SAMMANFATTNING DIETIST-KOSTNADER:**

| Åtgärd | Engångskostnad | Löpande kostnad/år |
|--------|----------------|-------------------|
| Legitimerad dietist lön | 0 | 456K (38K/mån × 12) |
| Legitimation (Socialstyrelsen) | 990 SEK | 0 |
| Journalsystem (setup) | 15K | 240K (1000 pat × 240 SEK) |
| Patientförsäkring | 0 | 20K |
| Videokonsultation-plattform | 5K | 30K |
| Fortbildning (legitimationskrav) | 0 | 10K |
| **TOTALT ÅR 1** | **20K** | **756K** |

---

## 5. MARKNADSFÖRING OCH HÄLSOPÅSTÅENDEN

### 🔴 **HÖGSTA RISK: Marknadsstörningsavgift upp till 4% av omsättning**

**Marknadsföringslagen (2008:486):**

### **GRUNDREGLER:**

1. **Sanningsplikt**: Allt ni säger måste vara sant
2. **Bevisbörda**: NI måste kunna bevisa alla påståenden
3. **Inte vilseledande**: Får inte ge felaktig information
4. **Identifierbar**: Reklam måste märkas som reklam

---

### **FÖRBJUDNA PÅSTÅENDEN**

❌ **DNA-test:**
- "Diagnostiserar din näringsbrist"
- "Förutsäger risk för sjukdomar"
- "98% accuracy" (om ni inte kan bevisa)
- "Visar vad du saknar"

❌ **Kosttillskott:**
- "Behandlar diabetes"
- "Botar hjärtsjukdomar"
- "Garanterad viktminskning på 10 kg"
- "Stärker ditt immunförsvar" (för brett, ej godkänt påstående)

❌ **Allmänt:**
- "Godkänt av läkare" (om inte sant och bevisbart)
- "Vetenskapligt bevisat" (utan att faktiskt ha studier)
- "Bäst i Sverige" (subjektivt, obevisbart)

---

### **TILLÅTNA PÅSTÅENDEN (EXEMPEL)**

✅ **DNA-test:**
- "Vårt DNA-test analyserar genetiska variationer relaterade till näringsämnesomsättning"
- "Kan ge information om hur din kropp kan metabolisera vissa vitaminer"
- "Resultaten används av dietist för personliga rekommendationer"

✅ **Kosttillskott:**
- "Innehåller vitamin D som bidrar till immunsystemets normala funktion" (godkänt health claim)
- "Personligt sammansatta kosttillskott baserat på din profil"
- "Prenumeration med månatliga leveranser"

✅ **Allmänt:**
- "Granskad av legitimerad dietist"
- "ISO-certifierat laboratorium"
- "GDPR-säker hantering av genetiska data"

---

### **AKTUELLT EXEMPEL: ZINZINO (2025)**

**Konsumentverket har ärenden mot Zinzino för:**
- Aggressiv marknadsföring (nätverksförsäljning)
- Vilseledande medicinska påståenden om omega-3-produkter
- Otillåtna health claims

**Sanktion:**
- Förbud mot fortsatt marknadsföring
- **Marknadsstörningsavgift: Potentiellt 4% av omsättning**

**LÄRDOM:** Konsumentverket granskar aktivt kosttillskottsmarknaden!

---

### **MARKNADSFÖRING I SOCIALA MEDIER**

**Influencer-samarbeten MÅSTE märkas:**

Enligt Konsumentverket:
- #annons, #reklam, #sponsrad MÅSTE användas
- Gäller även om ni ger gratis produkter
- Influencern ansvarar, men NI har yttersta ansvaret

**Korrekt märkning:**
```
Instagram-inlägg:
"Jag har testat @geneticwellness DNA-test och älskar det!
Mina personliga kosttillskott kommer varje månad. 🧬

#annons #samarbete"
```

**Felaktig märkning:**
```
"Helt fantastisk DNA-test som ALLA borde göra!
Check out @geneticwellness ❤️"

(Inget #annons = bryter mot marknadsföringslagen)
```

---

### **GRANSKNING AV MARKNADSFÖRINGSMATERIAL**

**OBLIGATORISKT: Låt regulatorisk expert granska ALL copy innan publicering**

**Vad ska granskas:**
- ☑ Landningssida
- ☑ Produktbeskrivningar
- ☑ E-postmarknadsföring
- ☑ Annonser (Facebook, Google, Instagram)
- ☑ Influencer-briefs
- ☑ Pitch deck (om innehåller påståenden som används externt)

**Kostnad:**
- Regulatorisk konsult: 150-300 SEK/tim
- Granskning av alla texter: 30-60K (engång)
- Löpande: 10K/år för nya texter

---

### **SAMMANFATTNING MARKNADSFÖRING-KOSTNADER:**

| Åtgärd | Kostnad |
|--------|---------|
| Regulatorisk granskning av all copy | 40-80K (engång) |
| Löpande granskning (nya kampanjer) | 10-20K/år |
| Juridisk backup vid Konsumentverket-ärende | 50-150K (vid behov) |

---

## 6. E-HANDEL OCH KONSUMENTRÄTT

### **DISTANSAVTALSLAGEN (2005:59)**

**Informationskrav FÖRE köp (obligatoriskt):**

På produktsidan MÅSTE finnas:
1. ☑ Företagets namn
2. ☑ Organisationsnummer
3. ☑ Adress (besöksadress eller postadress)
4. ☑ E-postadress
5. ☑ Telefonnummer
6. ☑ Produktens huvudsakliga egenskaper
7. ☑ Totalpris inkl. moms
8. ☑ Leveranskostnader
9. ☑ Betalningsvillkor
10. ☑ Leveranstid
11. ☑ Information om ångerrätt (se nedan)
12. ☑ Kostnaden för att returnera
13. ☑ För prenumeration: Pris per period, uppsägningstid

---

### **ÅNGERRÄTT - KRITISKT FÖR DNA-TEST**

**Huvudregel:** 14 dagars ångerrätt vid distansköp

**UNDANTAG (ångerrätt gäller INTE):**

Enligt distansavtalslagen 18§:
> "Varor med bruten försegling som inte lämpligen kan återlämnas av hälso- eller hygienskäl om förseglingen brutits av konsumenten."

**Tillämpning på DNA-test:**
- DNA-test med salivprov = **personlig hygienprodukt**
- Om kund brutit försegling och använt test: **INGEN ångerrätt**
- Om obrutet: Ångerrätt gäller

**KRITISKT: Ni MÅSTE informera om undantaget FÖRE köp!**

**Mall för produktsida:**

> **Ångerrätt:**
>
> Enligt distansavtalslagen har du 14 dagars ångerrätt från den dag du mottog produkten.
>
> **Undantag för DNA-test:** DNA-testet är en personlig hygienprodukt. När du har brutit förseglingen och använt testet kan produkten inte returneras av hälso- och hygienskäl. Oöppnade DNA-test kan returneras inom 14 dagar.
>
> **Kosttillskott:** Normal ångerrätt gäller. Du kan returnera öppnade eller oöppnade kosttillskott inom 14 dagar. Du står för returfrakt.
>
> **Dietist-konsultation:** Ingen ångerrätt efter att konsultationen genomförts (enligt distansavtalslagen 18§ om fullgjorda tjänster).

**Om ni INTE informerar om undantaget:**
- Kunden kan få upp till 1 år på sig att ångra sig
- Ni riskerar att behöva återbetala även använt test

---

### **ÅNGERRÄTT PÅ PRENUMERATION**

**Första leveransen:**
- Normal ångerrätt gäller (14 dagar)
- Kunden kan avsluta prenumeration

**Kommande leveranser:**
- Ej ångerrätt (avtalet redan ingånget)
- Uppsägningsregler enligt era villkor gäller

**Rekommenderad uppsägningsregel:**
> "Du kan när som helst pausa eller avsluta din prenumeration. Uppsägning måste ske senast 5 dagar före nästa leverans. Uppsägning görs via ditt konto eller genom att kontakta kundtjänst."

---

### **KONSUMENTKÖPLAGEN (2022:260)**

**Gäller vid FEL i vara:**

**Konsumentens rättigheter:**
1. Reklamation inom 3 år
2. Kräva avhjälpande (reparation)
3. Kräva omleverans
4. Kräva prisavdrag
5. Kräva hävning (pengarna tillbaka)

**Relevant för DNA-test:**
- Om DNA-testet inte fungerar tekniskt: Reklamationsrätt
- Om analysen inte levereras: Tydligt fel
- Om labb gör fel: Omleverans (nytt test)

**Relevant för kosttillskott:**
- Om produkten är felaktig (fel innehåll, förväxling)
- Om förpackning skadad vid leverans

**ÅTGÄRD:**
- Tydlig reklamationspolicy på sajten
- E-postadress för reklamationer
- Hantera reklamationer inom 2-3 veckor (konsumentverkets rekommendation)

---

### **SAMMANFATTNING E-HANDEL-KOSTNADER:**

| Åtgärd | Kostnad |
|--------|---------|
| Juridisk granskning av användarvillkor | 20-40K |
| Uppdatering av produktsidor (compliance) | 10-20K |
| Löpande juridisk rådgivning | 10K/år |
| **TOTALT (engång)** | **40-80K** |

---

## 7. IMPLEMENTATION ROADMAP

### **TIDSLINJE FÖR COMPLIANCE**

```
📅 FÖRE BOLAGSSTART (Månad -1 till 0):
┌────────────────────────────────────────────┐
│ ☐ Anlita regulatorisk advokat              │
│ ☐ Beslut: Wellness-positionering eller IVD │
│ ☐ Utforma GDPR-samtyckesprocess            │
│ ☐ Skriva användarvillkor                   │
│ ☐ Granska all marknadsföringsmaterial      │
└────────────────────────────────────────────┘
Kostnad: 150-250K
Tid: 4-8 veckor
```

```
📅 MÅNAD 0-3 (Bolagsstart till Pre-launch):
┌────────────────────────────────────────────┐
│ ☐ Registrera bolag                         │
│ ☐ Utse DPO (Data Protection Officer)       │
│ ☐ Genomföra DPIA (konsekvensbedömning)     │
│ ☐ Teckna avtal med ISO-labb                │
│ ☐ PUB-avtal med labb                       │
│ ☐ Anställ/kontraktera legitimerad dietist  │
│ ☐ Teckna patientförsäkring                 │
│ ☐ Implementera journalsystem               │
│ ☐ Implementera GDPR-säkerhet i plattform   │
│ ☐ Märkningsdesign kosttillskott            │
└────────────────────────────────────────────┘
Kostnad: 300-450K
Tid: 3 månader
```

```
📅 MÅNAD 3-6 (Pre-launch till MVP-lansering):
┌────────────────────────────────────────────┐
│ ☐ Beta-test av samtyckesprocess            │
│ ☐ Testa GDPR-flöden (radering, export)     │
│ ☐ Granska landningssida (regulatorisk)     │
│ ☐ Säkerhetsgranskning av plattform         │
│ ☐ Första kosttillskotts-batch tillverkad   │
│ ☐ COA-granskning för batch                 │
└────────────────────────────────────────────┘
Kostnad: 50-100K
Tid: 3 månader
```

```
📅 MÅNAD 6+ (Efter MVP-lansering):
┌────────────────────────────────────────────┐
│ ☐ Kvartalsvis GDPR-översyn                 │
│ ☐ Årlig säkerhetsrevision                  │
│ ☐ Förnya patientförsäkring                 │
│ ☐ DPO-rapportering till IMY                │
│ ☐ Granska nya marknadsföringsmaterial      │
│ ☐ Uppdatera DPIA vid ändringar             │
└────────────────────────────────────────────┘
Kostnad: 100-200K/år
Löpande
```

---

### **KRITISK VÄGEN - KAN EJ SKIPPAS:**

| Vecka | Aktivitet | Blockerar vad? |
|-------|-----------|----------------|
| **Vecka 1-2** | Anlita advokat | Allt annat |
| **Vecka 3-4** | Beslut om wellness/IVD | Marknadsföring, lab-avtal |
| **Vecka 5-6** | DPIA + DPO | MVP-utveckling (GDPR) |
| **Vecka 7-8** | Lab-avtal + PUB | DNA-test kan ej erbjudas |
| **Vecka 9-10** | Patientförsäkring | Dietist kan ej starta |
| **Vecka 11-12** | Märkningsdesign | Kosttillskott kan ej säljas |

**Total tid kritiska vägen: 12 veckor (3 månader)**

---

## 8. KOSTNADSUPPSKATTNING FÖR COMPLIANCE

### **SAMMANLAGD KOSTNADSTABELL**

| Kategori | Engångskostnad | År 1 löpande | År 2+ löpande |
|----------|----------------|--------------|---------------|
| **1. DNA-testning & IVDR** |||
| Advokat (wellness-bedömning) | 30-50K | - | - |
| Lab-avtal (setup) | 50-100K | - | - |
| PUB-avtal | 10K | - | - |
| **2. GDPR** |||
| DPO (extern) | - | 100-150K | 100-150K |
| DPIA | 50-80K | - | 20K (uppdatering) |
| IT-säkerhet (setup) | 80-120K | - | - |
| IT-säkerhet (löpande) | - | 120-200K | 120-200K |
| GDPR-advokat | 50K | 20K | 20K |
| **3. Kosttillskott** |||
| Märkningsdesign | 30K | - | - |
| Regulatorisk granskning | 20K | 10K | 10K |
| Health claims-granskning | 20K | - | - |
| **4. Dietist** |||
| Legitimerad dietist lön | - | 456K | 456K |
| Journalsystem (setup) | 15K | - | - |
| Journalsystem (löpande) | - | 50K | 100K |
| Patientförsäkring | - | 20K | 20K |
| Videokonsultation-plattform | 5K | 30K | 30K |
| **5. Marknadsföring** |||
| Copy-granskning (initial) | 50K | - | - |
| Löpande granskning | - | 15K | 15K |
| **6. E-handel** |||
| Användarvillkor (juridisk) | 30K | - | - |
| Produktsida-uppdateringar | 15K | 10K | 10K |
| **TOTALT** | **455-615K** | **831-1 041K** | **881-1 091K** |

---

### **BUDGETERING I FINANSMODELLEN**

**Nuvarande finansmodell Opex År 1: 531K**

**Compliance-kostnader:**
- Engång: 455-615K
- Löpande år 1: 831-1 041K
- **TOTAL ÅR 1: 1 286-1 656K**

**GAP: ~755K till 1 125K** som saknas i nuvarande budget!

---

### **LÖSNING: UPPDATERAD KAPITALBEHOV**

**Alternativ 1: Öka Seed Round**
- Nuvarande: 1,2M för 12%
- Nytt: **1,8M för 12%** (lägger till 600K för compliance)
- Används till: 455K engångskostnader + 145K extra buffer

**Alternativ 2: Fasad compliance (riskabelt)**
- Gör minimum år 1 (GDPR + Dietist obligatoriskt)
- Skjuter upp märkning och vissa advokattjänster
- Risk: Kan behöva fixa retroaktivt om Livsmedelsverket/Konsumentverket granskar

**Alternativ 3: Inkludera i Serie Seed Extension**
- Seed Round 1: 1,2M (som planerat)
- Behåll lean år 1, skjut vissa compliance-kostnader
- Serie Seed Extension: 1,8M (istället för 1,5M)
- Använder 300K till kvarvarande compliance

---

### **REKOMMENDATION:**

**Kör Alternativ 1: Öka Seed till 1,8M**

**Rationale:**
- Compliance är INTE valfritt
- Risken att skippa är för stor (böter, försäljningsförbud)
- Investerare förstår att regulatoriska kostnader finns
- Bättre att ha för mycket kapital än för lite

**Uppdaterad pitch:**
> "Vi söker 1,8M för 12% equity. 600K av detta går till regulatorisk compliance (GDPR, IVDR-bedömning, patientförsäkring, etc.) vilket är nödvändigt för vår verksamhet med genetiska data och hälsoprodukter. Detta säkerställer att vi är fullt compliant från dag 1 och undviker framtida böter och försäljningsförbud."

---

## 9. CHECKLISTOR OCH MALLAR

### **✅ PRE-LAUNCH COMPLIANCE CHECKLIST**

**DNA-testning:**
- [ ] Beslut dokumenterat: Wellness-produkt eller IVD
- [ ] Om IVD: CE-märkning påbörjad
- [ ] Om wellness: Juridisk bedömning dokumenterad
- [ ] Kontrakt tecknat med ISO-ackrediterat labb
- [ ] PUB-avtal (personuppgiftsbiträde) med labb undertecknat
- [ ] Lab-certifikat verifierat (ISO 17025 eller 15189)

**GDPR:**
- [ ] DPO utsedd och anmäld till IMY
- [ ] DPIA (konsekvensbedömning) genomförd
- [ ] Samtyckesblankett för genetiska data skapad
- [ ] Integritetspolicy skriven och publicerad
- [ ] Rutiner för radering dokumenterade
- [ ] IT-säkerhetsåtgärder implementerade (kryptering, 2FA, backup)
- [ ] PUB-avtal med alla underleverantörer
- [ ] Incidenthanteringsplan skriven

**Kosttillskott:**
- [ ] Märkning designad enligt Livsmedelsverkets krav
- [ ] Näringsdeklaration korrekt
- [ ] Endast godkända health claims används
- [ ] Tillverkare har GMP-certifikat
- [ ] COA (Certificate of Analysis) för första batch granskad
- [ ] Batchnummer-system implementerat
- [ ] Spårbarhet dokumenterad

**Dietist:**
- [ ] Legitimerad dietist anställd/kontrakterad
- [ ] Legitimationsintyg verifierat (Socialstyrelsen)
- [ ] Journalsystem implementerat och GDPR-säkrat
- [ ] Patientförsäkring tecknad
- [ ] Videokonsultation-plattform GDPR-säker
- [ ] Sekretessavtal undertecknat av dietist

**Marknadsföring:**
- [ ] All copy granskad av regulatorisk expert
- [ ] Inga medicinska påståenden
- [ ] Endast godkända health claims
- [ ] Influencer-samarbeten har #annons-märkning
- [ ] Bevisbörda: Alla påståenden kan styrkas

**E-handel:**
- [ ] Alla obligatoriska uppgifter på produktsida
- [ ] Ångerrätts-information tydlig (inkl. undantag för DNA-test)
- [ ] Prenumerationsvillkor tydliga
- [ ] Användarvillkor juridiskt granskade
- [ ] Reklamationspolicy publicerad

---

## 10. KONTAKTER OCH RESURSER

### **MYNDIGHETER:**

| Myndighet | Område | Kontakt |
|-----------|--------|---------|
| **Läkemedelsverket** | Medicinteknik, IVDR | registrator@lakemedelsverket.se, 018-17 46 00 |
| **IMY (Integritetsskyddsmyndigheten)** | GDPR | imy@imy.se, 08-657 61 00 |
| **Livsmedelsverket** | Kosttillskott | livsmedelsverket@slv.se, 018-17 55 00 |
| **Socialstyrelsen** | Dietist-legitimation, patientjournaler | socialstyrelsen@socialstyrelsen.se, 075-247 30 00 |
| **Konsumentverket** | Marknadsföring, konsumenträtt | konsumentverket@konsumentverket.se, 08-429 05 00 |
| **Swedac** | Ackreditering | info@swedac.se, 010-774 10 00 |

---

### **REKOMMENDERADE JURISTER/KONSULTER:**

| Område | Företag | Specialitet | Kontakt |
|--------|---------|-------------|---------|
| **Medicinteknisk rätt** | Setterwalls Advokatbyrå | Life Science & IVDR | www.setterwalls.se |
| **GDPR** | Advokatfirman Vinge | Dataskydd | www.vinge.se |
| **GDPR-konsult** | GDPR Advisor | DPO-as-a-Service | www.gdpradvisor.se |
| **Kosttillskott** | Livsmedelsjuristerna | Livsmedelsrätt | www.livsmedelsjuristerna.se |
| **Marknadsföring** | Advokatfirman Delphi | Marknadsrätt | www.delphi.se |

**Uppskattade kostnader:**
- Initial konsultation: 3-5K/tim
- IVDR-bedömning: 80-150K
- GDPR-compliance: 100-200K
- Marknadsföringsgranskning: 30-60K

---

### **ANVÄNDBARA VERKTYG:**

| Verktyg | Syfte | Kostnad |
|---------|-------|---------|
| **[Termly](https://termly.io/)** | Generera integritetspolicy, cookies-policy | Gratis-99 USD/mån |
| **[iubenda](https://www.iubenda.com/)** | GDPR-compliance verktyg | €27/mån |
| **[OneTrust](https://www.onetrust.com/)** | Enterprise GDPR-hantering | Offert (dyrt) |
| **[Securitas GDPR](https://gdpr.securitas.se/)** | DPIA-mallar | Gratis |

---

## BILAGA A: PERSONUPPGIFTSBITRÄDESAVTAL (PUB) - MALL

*[Se separat dokument: PUB_Avtal_Mall_Labb.md]*

---

## BILAGA B: SAMTYCKESFORMULÄR FÖR GENETISKA DATA - MALL

*[Se separat dokument: GDPR_Samtycke_Mall.md]*

---

## BILAGA C: INCIDENTHANTERINGSPLAN - MALL

*[Se separat dokument: Incidenthanteringsplan_Mall.md]*

---

## SAMMANFATTNING

### **KRITISKA TAKEAWAYS:**

1. **DNA-test:** Avgör OM det är medicinteknisk produkt (spara 500K-2M + 12-24 mån)
2. **GDPR:** DPO + DPIA är troligen OBLIGATORISKT (kostnad 150K/år)
3. **Kosttillskott:** Ingen notifiering, MEN märkning och health claims KRITISKT
4. **Dietist:** Legitimerad + patientförsäkring + journalsystem (kostnad 750K/år)
5. **Marknadsföring:** Granska ALL copy - risk för 4% avgift vid fel
6. **E-handel:** Ångerrätt DNA-test har undantag - MÅSTE informeras

### **TOTAL COMPLIANCE-KOSTNAD ÅR 1:**
- **Engång:** 455-615K
- **Löpande:** 831-1 041K
- **TOTALT:** **1,3-1,7M SEK**

### **ÅTGÄRD:**
**Öka Seed från 1,2M till 1,8M för att täcka compliance-kostnader.**

---

**Dokument skapat:** Januari 2026
**Version:** 1.0
**Nästa granskning:** Vid regulatoriska uppdateringar eller före MVP-lansering

---

**DISCLAIMER:** Detta dokument är en guide baserad på tillgänglig information januari 2026. Det ersätter INTE juridisk rådgivning. Konsultera alltid specialist-advokat innan ni fattar regulatoriska beslut.
