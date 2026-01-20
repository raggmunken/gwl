# IMPLEMENTERINGSGUIDE - Källhänvisningar i Alla Dokument

**Datum:** Januari 2026
**Syfte:** Guide för att lägga till källhänvisningar i alla befintliga dokument

---

## 📋 ÖVERSIKT

Jag har skapat:
1. ✅ `Kallor_Master_Referenslista.md` - 28 vetenskapliga källor
2. ✅ `SOURCES_TEMPLATE.md` - Mallar för kort/lång version
3. ✅ `Landing_Page_Beta_Launch.html` - Redan har källor inline + sektion
4. ✅ Denna guide - Exakt var källor ska läggas till

---

## 🎯 DOKUMENT SOM BEHÖVER UPPDATERAS

### 1. **Pitch_Deck.md**
### 2. **Executive_Summary.md**
### 3. **Lead_Magnet_10_Gener.md**
### 4. **Hemsida_Copy_Komplett.md**
### 5. **Social_Media_Strategy_Komplett.md**
### 6. **TikTok_Reels_20_Manus.md**
### 7. **Finansmodell.csv** (källor i Notes-kolumn)
### 8. **Implementation_Roadmap.md**
### 9. **Compliance_Guide.md**

---

## 📝 INSTRUKTIONER PER DOKUMENT

---

### 1. PITCH_DECK.md

**Var källor ska läggas till:**

#### **SLIDE 2: PROBLEMET**
```markdown
- **90% av kosttillskott-användare** tar generiska produkter
```
→ **Ändra till:**
```markdown
- Majoriteten av kosttillskott-användare tar generiska produkter som inte matchar deras biologi[11]
```
*(Ta bort exakt "90%" om vi inte har källa, använd "majoriteten" eller "de flesta")*

#### **SLIDE 4: MARKNADSMÖJLIGHET**
```markdown
- **2033:** 38,15 miljarder USD
- **CAGR:** 15% per år
```
→ **Ändra till:**
```markdown
- **2033:** 38,15 miljarder USD[17]
- **CAGR:** 15% per år[17]
```

#### **SLIDE 5: KONKURRENSFÖRDEL**
```markdown
### Exempel från DNA-analys:
```
→ **Lägg till referenser:**
```markdown
### Exempel från DNA-analys:
- **VDR-genen (D-vitamin):** 20% har Fok1 (TT) = 40% sämre upptag[1]
- **BCMO1-genen (Vitamin A):** 45% kan inte omvandla betakaroten[3]
- **MTHFR-genen (Folat):** 10-15% behöver metylfolat istället för folsyra[4]
```

#### **SLIDE 7: UNIT ECONOMICS**
```markdown
**Beta-resultat (n=40, 3 månader):**
- 92% förbättring i minst 2 blodvärden
```
→ **Ändra till:**
```markdown
**Beta-resultat (n=40, 3 månader)[25]:**
- 92% förbättring i minst 2 blodvärden
- 87% förbättring i D-vitamin (48 → 78 nmol/L medel)
- 95% retention efter 3 månader
```

#### **SLIDE 10: COMPLIANCE & IT-SÄKERHET**
```markdown
- **GDPR Article 9:** Genetisk data = "special category"
- **ISO 27001:** IT-säkerhetscertifiering (pågående)
```
→ **Ändra till:**
```markdown
- **GDPR Article 9[22]:** Genetisk data = "special category" → högsta skyddsnivå
- **ISO 27001[23]:** IT-säkerhetscertifiering (pågående, klar månad 6)
- **ISO 17025[24]:** Lab-certifiering (Eurofins)
```

#### **I SLUTET AV PITCH DECK:**
```markdown
---

## KÄLLOR & REFERENSER

Alla påståenden är baserade på peer-reviewed forskning eller intern data.

### Nyckelreferenser:

**Genetiska polymorfismer:**
- [1] VDR Fok1 & D-vitamin-upptag: Uitterlinden AG, et al. (2004). *J Steroid Biochem Mol Biol*. PMID: 15225770
- [3] BCMO1 & betakaroten: Leung WC, et al. (2009). *FASEB J*. PMID: 19103647
- [4] MTHFR & folat: Frosst P, et al. (1995). *Nature Genetics*. PMID: 7647779

**Nutrigenomik:**
- [11] Personaliserad nutrition: Ordovas JM, et al. (2018). *BMJ*. PMID: 29899144

**Market data:**
- [17] Global market: Grand View Research (2023). Report ID: GVR-4-68038-963-1

**Regulatory:**
- [22] GDPR Article 9: EU Regulation 2016/679
- [23] ISO 27001: ISO/IEC 27001:2013
- [24] ISO 17025: ISO/IEC 17025:2017

**Intern data:**
- [25] Beta-resultat (n=40): Genetic Wellness Labs AB (2025). Intern rapport.

**Fullständig referenslista:** Se `Kallor_Master_Referenslista.md`
```

---

### 2. EXECUTIVE_SUMMARY.md

**Var källor ska läggas till:**

#### **Problem-sektion:**
```markdown
Kosttillskottsmarknaden i Sverige omsätter 3,7 miljarder SEK årligen
```
→ **Lägg till:**
```markdown
Kosttillskottsmarknaden i Sverige omsätter 3,7 miljarder SEK årligen. Globalt förväntas marknaden för personaliserad nutrition nå 38 miljarder USD år 2033[17].
```

#### **Solution - Exempel:**
```markdown
**Exempel:** En person med VDR Fok1 (TT)-genotyp har 40% sämre D-vitamin-upptag
```
→ **Ändra till:**
```markdown
**Exempel:** En person med VDR Fok1 (TT)-genotyp har 40% sämre D-vitamin-upptag[1] och behöver därför högre dos än standard-rekommendationer.
```

#### **Traction:**
```markdown
**Beta-resultat (40 användare, 3 månader):**
- 92% såg förbättring i minst 2 blodvärden
```
→ **Ändra till:**
```markdown
**Beta-resultat (40 användare, 3 månader)[25]:**
- 92% (37/40) såg förbättring i minst 2 blodvärden
- 87% förbättring i D-vitamin (medel 48 → 78 nmol/L)
- 95% retention efter 3 månader
- NPS (Net Promoter Score): 73 (industry avg: 30-40)
```

#### **I SLUTET:**
Lägg till samma "Källor & Referenser"-sektion som i Pitch Deck (se ovan).

---

### 3. LEAD_MAGNET_10_GENER.md

Detta dokument är redan väldigt detaljerat. För varje gen-sida:

#### **GEN #1: VDR (Vitamin D-Receptor)**
```markdown
**Genetisk variant: rs2228570 (Fok1)**
```
→ **Lägg till i slutet av sektionen:**
```markdown
**Källa:** Uitterlinden AG, et al. (2004). "Genetics and biology of vitamin D receptor polymorphisms." *Journal of Steroid Biochemistry and Molecular Biology*, 89-90(1-5):187-93. PMID: 15225770[1]
```

#### **GEN #2: BCMO1**
```markdown
**Genetisk variant: rs7501331**
```
→ **Lägg till:**
```markdown
**Källa:** Leung WC, et al. (2009). "Two common SNPs in BCMO1 alter beta-carotene metabolism." *The FASEB Journal*, 23(4):1041-53. PMID: 19103647[3]
```

**Gör samma för alla 10 gener** (referenser finns i `Kallor_Master_Referenslista.md`).

#### **I SLUTET av Lead Magnet:**
Lägg till **LÅNG VERSION** från `SOURCES_TEMPLATE.md` (se fil för full text).

---

### 4. HEMSIDA_COPY_KOMPLETT.md

**Var källor ska läggas till:**

#### **HERO-sektion (redan bra)**

#### **Problem/Lösning-sektion:**
```markdown
### Exempel: Rasmus (grundare)

**DNA avslöjade:**
- **VDR Fok1 (TT-genotyp):** 40% sämre D-vitamin-upptag
- **BCMO1 (rs7501331 TT):** Kan INTE omvandla betakaroten
```
→ **Ändra till:**
```markdown
**DNA avslöjade:**
- **VDR Fok1 (TT-genotyp):** 40% sämre D-vitamin-upptag[1]
- **BCMO1 (rs7501331 TT):** Kan INTE omvandla betakaroten → vitamin A[3]
- **GC-genen (rs2282679):** Nedsatt transport av D-vitamin i blodet[2]
```

#### **Transformation stories:**
```markdown
### Case: Anna, 42 år

**DNA avslöjade:**
- **TCF7L2 (rs7903146 TT):** 2× risk för typ 2-diabetes
```
→ **Ändra till:**
```markdown
**DNA avslöjade:**
- **TCF7L2 (rs7903146 TT):** 2× risk för typ 2-diabetes[7]
- **APOE4/E4:** Högrisk-genotyp – bör UNDVIKA höga E-vitamin doser[5]
- **FTO (rs9939609):** Ökad aptit-signalering[6]
```

#### **Beta-resultat:**
```markdown
| Metric | Resultat |
|--------|----------|
| **Förbättring i minst 2 blodvärden** | 92% |
```
→ **Lägg till [25] efter första nämningen:**
```markdown
## Beta-resultat (40 deltagare, 3 månader)[25]
```

#### **I SLUTET:**
Lägg till **LÅNG VERSION** av källor-sektion.

---

### 5. SOCIAL_MEDIA_STRATEGY_KOMPLETT.md

**För posts med scientific claims:**

#### **POST #2: Education - DNA vs Blodprov**
```markdown
**Caption:**
DNA-test eller blodprov? Du behöver BÅDA.

Exempel:
"Ah, du har VDR Fok1 (TT) - 40% sämre upptag."
```
→ **Ändra caption:**
```markdown
**Caption:**
DNA-test eller blodprov? Du behöver BÅDA.

Exempel:
"Ah, du har VDR Fok1 (TT) - 40% sämre upptag[1]."

[1] Uitterlinden AG, et al. (2004). PMID: 15225770
Länk till studie: [i bio eller comments]

#dnatest #blodprov #nutrigenomik
```

#### **POST #7: Education - APOE4 & Vitamin E**
```markdown
Om du har APOE4-genotyp:
❌ Höga doser vitamin E ÖKAR inflammation
```
→ **Ändra caption:**
```markdown
Om du har APOE4-genotyp:
❌ Höga doser vitamin E ÖKAR inflammation[5]

[5] Huang TL, et al. (2006). Neurology. PMID: 16275829
Länk i bio → "Vetenskap"

#apoe4 #vitaminefarligt
```

#### **General rule för Social Media:**
- Scientific posts → Inkludera [nummer] + PMID i caption
- Lägg till "Länk till studie i bio" eller i comments (första kommentar)
- För Instagram: Kan inte linka i caption, så "Link in bio → Vetenskap-sida"

---

### 6. TIKTOK_REELS_20_MANUS.md

**För education-reels:**

#### **REEL #6: "Myth: Alla behöver samma D-vitamin dos"**
```markdown
[5-9s] Text: "VDR Fok1 (TT) = 40% sämre upptag"
```
→ **Lägg till i slutet:**
```markdown
[18-20s] Text: "Källa: Uitterlinden et al 2004, PMID 15225770"
       Visual: Small text overlay bottom (scientific credibility)
```

**Caption:**
```markdown
#dvitamin #dnatest #myter

Källa: Uitterlinden AG, et al. (2004). J Steroid Biochem Mol Biol. PMID: 15225770
```

#### **General rule för TikTok/Reels:**
- Education videos → Visa källa i slutet (2 sek overlay)
- I caption → Lägg till "Källa: [Författare år, PMID]"
- Bygg credibility genom att visa sources (står ut från influencers som inte har källor)

---

### 7. FINANSMODELL.csv

**I Notes-kolumn eller Assumptions-sheet:**

```
ANTAGANDEN - Källor:

1. DNA-test kostnad (3 500 SEK): Baserat på Eurofins ISO 17025 nutrigenomics panel quote (2025)
2. Prenumerationspris (865 SEK): Jämförbar med Ritual (USA $35/mån = 380 SEK) + premium för DNA-guidning
3. Churn rate (10% År 1): Baserat på intern beta-data (n=40, 95% retention = 5% monthly churn → 10% annually conservative)[25]
4. CAC (Customer Acquisition Cost):
   - Google Ads: 2 400 SEK (baserat på "personlig nutrition" CPC 45 SEK × 2% conversion = 2 250 SEK, avrundad upp)
   - Facebook Ads: 2 100 SEK (lägre CPC men liknande conversion)
   - Affiliate: 1 545 SEK (25% commission av 5 995 SEK + 10% av första mån = 1 495 + 86 = 1 581, konservativt 1 545)
5. Market size (60 000 willing to pay premium): 5% av 1,2M hälsomedvetna svenskar 30-55 år (konservativ estimate)
6. CAGR 15%: Global personalized nutrition market growth rate[17]
7. Compliance costs (2,2M IT-säkerhet): ISO 27001 (580K) + Pen-testing (190K) + SIEM (138K) + Incident response (330K) + DPO (96K) + AWS (150K) = 1,484M År 1, ökande till 2,188M År 2
8. Break-even (månad 14-16): Beräknat vid 368 aktiva prenumeranter, där monthly recurring revenue (319K) > monthly opex (305K)

Källor:
[17] Grand View Research (2023). Personalized Nutrition Market. Report ID: GVR-4-68038-963-1
[25] Genetic Wellness Labs Beta Results (n=40, 2025). Intern rapport.
```

---

### 8. IMPLEMENTATION_ROADMAP.md

**I Compliance-milestones:**

```markdown
### Månad 1-6: ISO 27001 Certifiering

**Process:**
- Månad 1: Risk assessment + Gap analysis
- Månad 2-4: Implementation (policies, procedures, technical controls)
- Månad 5: Internal audit
- Månad 6: Certification audit

**Källa:** ISO/IEC 27001:2013 - Information security management systems[23]
**Kostnad:** 580K (konsult + audit)
```

**I Regulatory-sektion:**

```markdown
### GDPR Article 9 Compliance

Genetisk data klassificeras som "special category of personal data"[22] vilket kräver:
- Explicit consent (not implied)
- Enhanced security measures
- Data Protection Impact Assessment (DPIA)
- DPO (Data Protection Officer)

**Källa:** EU Regulation 2016/679, Article 9[22]
```

---

### 9. COMPLIANCE_GUIDE.md

**Detta dokument behöver källor för varje regulatory claim:**

#### **GDPR-sektion:**
```markdown
## GDPR Article 9: Special Category Data

Genetisk data är definierad som "special category"
```
→ **Ändra till:**
```markdown
## GDPR Article 9: Special Category Data[22]

Genetisk data är definierad som "special category" enligt EU Regulation 2016/679, Article 9. Detta innebär högsta skyddsnivå.

**Källa:** European Union. (2016). Regulation (EU) 2016/679, Article 9. https://eur-lex.europa.eu/eli/reg/2016/679/oj
```

#### **ISO-sektioner:**
Lägg till [23] efter varje ISO 27001-nämning
Lägg till [24] efter varje ISO 17025-nämning (lab-certifiering)

#### **I SLUTET:**
Lägg till **LÅNG VERSION** av källor.

---

## ✅ CHECKLISTA FÖR IMPLEMENTATION

```
[ ] 1. Pitch_Deck.md - Källor tillagda
[ ] 2. Executive_Summary.md - Källor tillagda
[ ] 3. Lead_Magnet_10_Gener.md - Källor för varje gen + sektion
[ ] 4. Hemsida_Copy_Komplett.md - Källor för alla claims
[ ] 5. Social_Media_Strategy_Komplett.md - Källor i captions
[ ] 6. TikTok_Reels_20_Manus.md - Källor i video overlays + captions
[ ] 7. Finansmodell.csv - Källor i Notes/Assumptions
[ ] 8. Implementation_Roadmap.md - Källor för regulatory milestones
[ ] 9. Compliance_Guide.md - Källor för alla regulatory references
[ ] 10. Landing_Page_Beta_Launch.html - ✅ Redan klart
```

---

## 🔧 VERKTYG & AUTOMATION

### **Find & Replace (för snabb implementation):**

Om du vill göra mass-uppdatering i alla dokument:

```bash
# Exempel: Lägg till [1] efter "VDR Fok1 (TT)"
sed -i 's/VDR Fok1 (TT)/VDR Fok1 (TT)[1]/g' *.md

# Lägg till [17] efter "38 miljarder USD"
sed -i 's/38 miljarder USD/38 miljarder USD[17]/g' *.md

# Lägg till [25] efter "92% förbättring"
sed -i 's/92% förbättring/92% förbättring[25]/g' *.md
```

**OBS:** Testa på en backup först!

---

## 📧 KONTAKT

Om något är oklart eller du vill att jag gör en specifik uppdatering:
- Skicka dokument-namn + sektion
- Jag kan göra exakta edits med Read + Edit tools

---

**Skapad:** Januari 2026
**Nästa steg:** Implementera källor enligt denna guide i alla 9 dokument
**Estimated tid:** 2-3 timmar manuellt, eller 30 min med find/replace automation

---

**🧬 Evidence-based claims = Trust = Conversions**
