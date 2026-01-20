"""
GWL Lifestyle Planner
=====================
Generates personalized meal plans and supplement protocols based on DNA analysis.

Usage:
    python gwl_lifestyle_planner.py GWL_Profil_Name_Date.json

Genetic Wellness Labs - Nutrigenomics Platform
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum

# =============================================================================
# DATA STRUCTURES
# =============================================================================

class MealTime(Enum):
    BREAKFAST = "frukost"
    LUNCH = "lunch"
    DINNER = "middag"
    SNACK = "mellanmal"

class SupplementTiming(Enum):
    MORNING_EMPTY = "morgon, tom mage"
    MORNING_WITH_FOOD = "morgon, med mat"
    WITH_LARGEST_MEAL = "med storsta maltid"
    EVENING_BEFORE_BED = "kvall, 30-60 min fore laggdags"
    DIVIDED_DOSES = "delad dos, morgon + kvall"

@dataclass
class Supplement:
    """Ett tillskott med dosering och timing"""
    name: str
    dose: str
    timing: SupplementTiming
    priority: str  # critical, high, moderate, low
    reason: str
    genes: List[str]
    take_with: List[str] = field(default_factory=list)
    avoid_with: List[str] = field(default_factory=list)
    drug_interactions: List[str] = field(default_factory=list)
    notes: str = ""

@dataclass
class MealRecommendation:
    """En maltidsrekommendation"""
    meal_time: MealTime
    foods_to_emphasize: List[str]
    foods_to_avoid: List[str]
    example_meals: List[str]
    notes: str = ""

@dataclass
class LifestylePlan:
    """Komplett livsstilsplan"""
    name: str
    generated_date: str
    genetic_summary: Dict[str, str]

    # Supplement protocol
    supplements_morning: List[Supplement]
    supplements_with_meals: List[Supplement]
    supplements_evening: List[Supplement]

    # Meal plan
    breakfast_recommendations: MealRecommendation
    lunch_recommendations: MealRecommendation
    dinner_recommendations: MealRecommendation
    snack_recommendations: MealRecommendation

    # Weekly focus
    weekly_meal_plan: Dict[str, Dict[str, str]]

    # Important warnings
    critical_warnings: List[str]

    # General lifestyle
    lifestyle_recommendations: List[str]

    # Genetic explanations (what each profile means)
    genetic_explanations: Dict[str, Dict[str, str]] = field(default_factory=dict)

# =============================================================================
# GENETIC PROFILE EXPLANATIONS
# =============================================================================

GENETIC_PROFILE_EXPLANATIONS = {
    "MTHFR_impaired": {
        "name": "MTHFR (Metylentetrahydrofolatreduktas)",
        "what_it_is": """MTHFR är ett enzym som omvandlar folat (vitamin B9) till dess aktiva form,
metylfolat (5-MTHF). Metylfolat är avgörande för metyleringscykeln - en fundamental
biokemisk process som påverkar DNA-reparation, neurotransmittorproduktion,
avgiftning och över 200 andra reaktioner i kroppen.""",
        "what_variant_means": """Du har en genetisk variant som minskar MTHFR-enzymets aktivitet
med 30-70%. Detta innebär att din kropp har svårare att:
• Omvandla syntetisk folsyra till användbart metylfolat
• Producera tillräckligt med SAMe (kroppens huvudmetyldonator)
• Hålla homocystein på hälsosamma nivåer
• Tillverka neurotransmittorer som serotonin och dopamin""",
        "why_recommendation": """Därför rekommenderas:
• METYLFOLAT istället för folsyra - du kan använda det direkt
• B12 som metylkobalamin - arbetar tillsammans med metylfolat
• B2 (riboflavin) - kofaktor som MTHFR-enzymet behöver
• UNDVIK syntetisk folsyra - kan blockera receptorer utan att ge nytta
• UNDVIK lustgas vid operation - inaktiverar B12 och förvärrar metyleringsproblem"""
    },

    "COMT_slow": {
        "name": "COMT Långsam (Met/Met - 'Worrier')",
        "what_it_is": """COMT (Katekol-O-metyltransferas) är ett enzym som bryter ner
katekolaminer - dopamin, adrenalin och noradrenalin. Det bryter även ner
östrogen och vissa gifter. COMT använder SAMe (från metyleringscykeln)
för att göra detta.""",
        "what_variant_means": """Du har den 'långsamma' varianten (Met/Met) som ger 3-4 gånger
lägre enzymaktivitet. Detta betyder:

FÖRDELAR:
• Högre dopaminnivåer = bättre fokus och arbetsminne under lugna förhållanden
• Bättre smärthantering
• Kan prestera bra i förutsägbara situationer

NACKDELAR:
• Dopamin och adrenalin stannar längre = känsligare för stress
• Kan känna dig överstimulerad av koffein, stress, stimulantia
• Långsammare nedbrytning av östrogen
• Mer benägen för ångest under press""",
        "why_recommendation": """Därför rekommenderas:
• UNDVIK EGCG/grönt te-extrakt - hämmar COMT ytterligare, kan orsaka ångest
• Begränsa koffein (<200mg/dag) - du är känsligare för stimulantia
• L-Theanin - balanserar dopamin, ger lugn utan sedation
• Magnesium - COMT-kofaktor, lugnande för nervsystemet
• Stresshantering kritisk - meditation, yoga hjälper dig hantera högt dopamin
• DIM för östrogenstöd - hjälper bryta ner östrogen via alternativ väg"""
    },

    "COMT_fast": {
        "name": "COMT Snabb (Val/Val - 'Warrior')",
        "what_it_is": """COMT (Katekol-O-metyltransferas) bryter ner dopamin, adrenalin och
noradrenalin. Du har den 'snabba' varianten som arbetar 3-4 gånger snabbare
än den långsamma varianten.""",
        "what_variant_means": """Du har den snabba varianten (Val/Val) som betyder:

FÖRDELAR:
• Bättre stresshantering - adrenalin rensas snabbt
• Presterar bra under press ('warrior' fenotyp)
• Mindre benägen för ångest
• Snabbare återhämtning från stress

NACKDELAR:
• Lägre basala dopaminnivåer kan ge sämre fokus i lugna situationer
• Kan behöva mer stimulans för att känna motivation
• Risk för att söka sensation/stimulans""",
        "why_recommendation": """Därför rekommenderas:
• L-Tyrosin - aminosyra som är byggsten för dopamin
• Proteinrik frukost - ger tyrosin för dopaminproduktion
• Kaffe är OK för dig - du metaboliserar katekolaminer snabbt
• Du kan hantera stress bättre, men behöver fokusstrategier i lugna miljöer"""
    },

    "APOE4_carrier": {
        "name": "APOE e4 (Apolipoprotein E4)",
        "what_it_is": """APOE är ett protein som transporterar fett och kolesterol i blodet och
hjärnan. Det finns tre varianter: e2, e3 (vanligast), och e4. APOE4 är den
evolutionärt äldsta varianten, utvecklad när människor var jägare-samlare
med helt annan kost och livsstil.""",
        "what_variant_means": """Du bär på APOE e4-allelen vilket innebär:

ÖKAD RISK FÖR:
• Alzheimers sjukdom (e4/e4: 10-15x, e3/e4: 2-3x ökad risk)
• Hjärt-kärlsjukdom
• Högre LDL-kolesterol som svar på mättat fett
• Sämre reparation av hjärnceller

VARFÖR e4 FINNS:
• Fördelaktig i infektionsrik miljö (bättre immunförsvar)
• Bra för fasta och lågkalorikost (effektiv fettmetabolism)
• Men missmatchad med modern diet med mycket mättat fett

VIKTIGT:
• Genetik är inte öde - livsstil har ENORM påverkan
• e4-bärare som lever hälsosamt kan ha LÄGRE risk än e3-bärare med ohälsosam livsstil""",
        "why_recommendation": """Därför rekommenderas:
• MÄTTAT FETT <7% av kalorier - din kropp svarar starkt negativt
• OMEGA-3 HÖGDOS (2-3g EPA/DHA) - neuroprotektion, antiinflammation
• MCT-olja - alternativ energikälla för hjärnan (ketoner)
• Medelhavsbaserad kost - bevisat skyddande för e4-bärare
• UNDVIK alkohol - e4 + alkohol = extra hjärnskada
• Aerob träning 30+ min/dag - KRITISKT för kognitiv hälsa
• Tidig screening från 50 års ålder"""
    },

    "FADS_low": {
        "name": "FADS1/FADS2 Låg Aktivitet",
        "what_it_is": """FADS1 och FADS2 (Fettsyradesaturas) är enzymer som omvandlar
växtbaserat omega-3 (ALA från linfrö, chiafrön, valnötter) till de aktiva
formerna EPA och DHA som kroppen använder för hjärna, ögon, hjärta och
antiinflammatoriska processer.""",
        "what_variant_means": """Du har genetiska varianter som ger låg FADS-aktivitet:

VAD DET BETYDER:
• Du kan INTE effektivt omvandla ALA (växtomega-3) till EPA/DHA
• Konverteringsgraden kan vara så låg som 0.5-5% istället för normala 5-15%
• Att äta linfrö och chiafrön ger dig nästan ingen EPA/DHA
• Du är beroende av direkt EPA/DHA från fisk eller tillskott

KONSEKVENSER OM EJ ÅTGÄRDAT:
• Ökad inflammation
• Sämre hjärnfunktion
• Torr hud, torra ögon
• Högre risk för hjärt-kärlsjukdom
• Sämre immunförsvar""",
        "why_recommendation": """Därför rekommenderas:
• FET FISK minst 3 ggr/vecka - lax, makrill, sardiner, sill (direkt EPA/DHA)
• FISKOLJA/ALGEOLJA dagligen 2-3g - du MÅSTE ha förformad EPA/DHA
• FÖRLITA DIG INTE på växtomega-3 - det fungerar inte för dig
• För vegetarianer: Algbaserad omega-3 (DHA+EPA) är OBLIGATORISKT
• Minska omega-6 (solrosolja) - minskar inflammatorisk konkurrens"""
    },

    "VDR_impaired": {
        "name": "VDR (Vitamin D-receptor) / CYP2R1",
        "what_it_is": """VDR är receptorn som vitamin D binder till för att utöva sina effekter
i cellerna. CYP2R1 är enzymet i levern som omvandlar D-vitamin till dess
cirkulerande form (25-OH-D). Vitamin D är inte bara ett vitamin utan fungerar
som ett hormon som påverkar över 2000 gener.""",
        "what_variant_means": """Du har genetiska varianter som påverkar D-vitaminmetabolismen:

VAD DET KAN BETYDA:
• Lägre respons på samma mängd D-vitamin
• Svårare att nå optimala blodnivåer (75-125 nmol/L)
• Kan behöva 25-50% högre dos för samma effekt
• Större behov av kofaktorer (K2, magnesium)

VARFÖR D-VITAMIN ÄR VIKTIGT:
• Immunförsvar (förebygger infektioner)
• Benhälsa (kalciumupptag)
• Muskelfunktion
• Mental hälsa (depression kopplat till lågt D)
• Kan påverka 5-10% av alla gener""",
        "why_recommendation": """Därför rekommenderas:
• HÖGRE DOS D3 (3000-5000 IE/dag) - du behöver mer för samma effekt
• K2 (MK-7) ALLTID MED D3 - styr kalcium till skelett, inte kärl
• Magnesium - krävs för att aktivera D-vitamin (25-hydroxylering)
• Testa blodnivåer 2x/år - sikta på 75-100 nmol/L
• Solexponering 15-20 min/dag utan solskydd (när möjligt)
• Ta med FET MÅLTID - D-vitamin är fettlösligt"""
    },

    "CYP1A2_slow": {
        "name": "CYP1A2 Långsam Koffeinmetabolism",
        "what_it_is": """CYP1A2 är ett leverenzym som bryter ner koffein. Det ansvarar för
~95% av koffeinmetabolismen. Koffein har en halveringstid på 3-7 timmar
beroende på din CYP1A2-aktivitet.""",
        "what_variant_means": """Du är en 'långsam metaboliserare' av koffein:

VAD DET BETYDER:
• Koffein stannar längre i ditt system (längre halveringstid)
• En kopp kaffe kl 14 kan påverka sömnen kl 22
• Större risk för biverkningar: hjärtklappning, ångest, sömnstörning
• Ökad risk för hjärtinfarkt vid hög koffeinkonsumtion (>3 koppar/dag)

GENETISK FÖRKLARING:
• AC eller CC genotyp på rs762551
• Enzymet arbetar långsammare
• Samma dos koffein ger dig högre och längre exponering""",
        "why_recommendation": """Därför rekommenderas:
• MAX 1-2 koppar kaffe/dag
• INGET koffein efter kl 14 (eller tidigare om sömnproblem)
• Välj grönt te (lägre koffein, L-theanin balanserar)
• Koffeinfritt kaffe om du vill ha smaken
• UNDVIK energidrycker
• Räkna med att koffein påverkar dig ~8-10 timmar"""
    },

    "CYP1A2_fast": {
        "name": "CYP1A2 Snabb Koffeinmetabolism",
        "what_it_is": """Du har hög CYP1A2-enzymaktivitet som bryter ner koffein snabbt.""",
        "what_variant_means": """Du är en 'snabb metaboliserare' av koffein:

VAD DET BETYDER:
• Koffein rensas snabbt från ditt system
• Du kan dricka kaffe på kvällen utan sömnpåverkan (för många)
• Kaffe kan till och med vara HJÄRTSKYDDANDE för dig
• Lägre risk för koffeinrelaterade biverkningar""",
        "why_recommendation": """Därför rekommenderas:
• Kaffe är OK för dig (upp till 4 koppar/dag kan vara skyddande)
• Du kan tolerera koffein senare på dagen
• Men lyssna fortfarande på din kropp - genetik är bara en faktor"""
    },

    "inflammation_high": {
        "name": "Pro-inflammatorisk Genetisk Profil (IL-6/TNF-α)",
        "what_it_is": """IL-6 (Interleukin-6) och TNF-α (Tumörnekrosfaktor-alfa) är cytokiner -
signalmolekyler som styr inflammation. Viss inflammation är nödvändig för
läkning och immunförsvar, men kronisk låggradig inflammation ('inflammaging')
är kopplat till de flesta kroniska sjukdomar.""",
        "what_variant_means": """Du har genetiska varianter som ger högre basal inflammation:

VAD DET BETYDER:
• Dina gener programmerar för högre IL-6 och/eller TNF-α produktion
• Du har troligen kronisk låggradig inflammation
• Starkare inflammatoriskt svar på triggers (stress, dålig kost, infektioner)

ÖKAD RISK FÖR:
• Hjärt-kärlsjukdom (inflammation = åderförkalkning)
• Typ 2-diabetes (inflammation stör insulinkänslighet)
• Depression (inflammation påverkar hjärnan)
• Autoimmuna tendenser
• Snabbare åldrande

TRIGGERS SOM FÖRVÄRRAR:
• Socker, raffinerade kolhydrater
• Omega-6 oljor (solros, majs, soja)
• Stress
• Dålig sömn
• Visceralt bukfett""",
        "why_recommendation": """Därför rekommenderas:
• OMEGA-3 HÖGDOS (2-3g EPA) - direkt antiinflammatoriskt
• Kurkumin med piperin - naturlig COX-2/NF-κB hämmare
• ELIMINERA socker och raffinerade kolhydrater
• MINSKA omega-6 (byt solrosolja mot olivolja)
• Anti-inflammatoriska livsmedel dagligen: fet fisk, bär, grönt te, ingefära
• Träning (antiinflammatoriskt vid måttlig intensitet)
• Sömn 7-9h (brist ökar inflammation dramatiskt)"""
    },

    "estrogen_metabolism_impaired": {
        "name": "Östrogenmetabolism (CYP1B1 + COMT)",
        "what_it_is": """Östrogen bryts ner i levern via två steg:
1. Fas I (CYP1B1, CYP1A1): Omvandlar östrogen till metaboliter (2-OH, 4-OH, 16-OH)
2. Fas II (COMT): Metylerar och inaktiverar dessa metaboliter

4-OH-östrogen är potentiellt cancerframkallande, medan 2-OH är säkrare.""",
        "what_variant_means": """Du har en ogynnsam kombination:
• CYP1B1-variant: Producerar MER av den skadliga 4-OH-östrogen metaboliten
• COMT slow: Bryter ner 4-OH-östrogen LÅNGSAMMARE

KONSEKVENS:
• 4-OH-östrogen ackumuleras
• 4-OH-östrogen kan skada DNA (quinon-bildning)
• Ökad risk för östrogenkänsliga cancerformer
• Viktigare att stödja 2-OH-vägen istället

GÄLLER SÄRSKILT:
• Kvinnor (högre östrogennivåer)
• Vid HRT/p-piller
• Vid övervikt (fettvävnad producerar östrogen)""",
        "why_recommendation": """Därför rekommenderas:
• DIM (Diindolylmetan) 100-200mg/dag - skiftar metabolism till säkra 2-OH-vägen
• KORSBLOMMIGA GRÖNSAKER DAGLIGEN: broccoli, blomkål, grönkål, rucola, brysselkål
• Broccoligroddar - extra högt I3C/DIM-innehåll
• Fiber - binder och eliminerar östrogen via tarmen
• Linfrön - lignaner stödjer hälsosam östrogenbalans
• Diskutera med läkare vid HRT/p-piller
• Undvik plastförpackningar (BPA = xenoöstrogen)
• Begränsa alkohol (ökar östrogen)"""
    },

    "HFE_iron_risk": {
        "name": "HFE (Järnmetabolism / Hemokromatos-risk)",
        "what_it_is": """HFE-genen styr hur mycket järn kroppen absorberar från maten.
Mutationer kan leda till för hög järnabsorption (hereditär hemokromatos)
vilket orsakar järninlagring i organ.""",
        "what_variant_means": """Du har HFE-varianter som kan öka järnupptaget:

POTENTIELLA KONSEKVENSER:
• Gradvis järnansamling i lever, hjärta, bukspottkörtel
• Ökad oxidativ stress (järn är pro-oxidant)
• Risk för organskador vid obehandlad hemokromatos

VIKTIGT:
• Heterozygot (en kopia) = oftast mild, men bör monitoreras
• Homozygot (två kopior) = signifikant risk, kräver uppföljning""",
        "why_recommendation": """Därför rekommenderas:
• Testa ferritin och transferrinmättnad regelbundet
• BEGRÄNSA rött kött (hemjärn absorberas lätt)
• Te eller kaffe MED måltider - hämmar järnupptag
• UNDVIK C-vitamin tillsammans med järnrika måltider (ökar upptag)
• Överväg blodgivning om ferritin är förhöjt
• Diskutera med läkare för regelbunden monitorering"""
    },

    "detox_support": {
        "name": "Avgiftningskapacitet (GST-enzymer)",
        "what_it_is": """Glutathion S-transferaser (GSTM1, GSTT1, GSTP1) är fas II-avgiftningsenzymer
som kopplar glutathion till toxiner för att göra dem vattenlösliga och
utsöndringsbara. De skyddar mot oxidativ stress, tungmetaller, cancerframkallande
ämnen och läkemedelsmetaboliter.""",
        "what_variant_means": """Du har varianter som minskar avgiftningskapaciteten:

GSTM1 null (saknas helt): ~50% av befolkningen
GSTT1 null (saknas helt): ~20% av befolkningen
GSTP1 varianter: Reducerad aktivitet

KONSEKVENSER:
• Långsammare avgiftning av miljögifter
• Ökad känslighet för oxidativ stress
• Potentiellt sämre tolerans för vissa läkemedel
• Viktigare att stödja andra avgiftningsvägar""",
        "why_recommendation": """Därför rekommenderas:
• NAC (N-Acetyl Cystein) 600-1200mg - prekursor till glutathion
• Korsblommiga grönsaker - aktiverar alternativa avgiftningsvägar
• Lök, vitlök - svavelföreningar stödjer avgiftning
• Minimera toxinexponering (ekologiskt när möjligt, filtrera vatten)
• Undvik onödiga läkemedel
• Svettning (bastu, träning) - eliminerar vissa toxiner via huden
• Fiber - binder toxiner i tarmen"""
    }
}

# =============================================================================
# GENETIC FOOD DATABASE
# =============================================================================

# Foods based on genetic variants
GENETIC_FOOD_RECOMMENDATIONS = {
    # MTHFR - Methylation support
    "MTHFR_impaired": {
        "emphasize": [
            "Morkgrona bladgronsaker (spenat, grankol, mangold)",
            "Linser och bonor (naturlig folat)",
            "Avokado",
            "Sparris",
            "Broccoli",
            "Lever (rik pa B-vitaminer)",
            "Agg (kolin for metylering)",
            "Biffar fran grasbetade djur (B12)"
        ],
        "avoid": [
            "Berikade livsmedel med syntetisk folsyra",
            "Vitt brod (ofta berikat)",
            "Frukosflingor (ofta berikade)",
            "Alkohol (forsamrar metylering)"
        ]
    },

    # COMT slow (Met/Met) - Catecholamine sensitivity
    "COMT_slow": {
        "emphasize": [
            "Magnesiumrika livsmedel (pumpakaernor, mork choklad)",
            "L-theanin-kallor (gront te - INTE gront te-extrakt)",
            "Komplexa kolhydrater for stabilt blodskocker",
            "Protein vid varje maltid",
            "Lugnade orter (kamomill, lavendel)",
            "Omega-3 rik fisk (lax, makrill)"
        ],
        "avoid": [
            "Gront te-extrakt/EGCG-tillskott (COMT-hammare)",
            "Hog koffein (>200mg/dag)",
            "Tyraminrika livsmedel om kansllig (lagrad ost, vin)",
            "Stimulerande livsmedel pa kvallen"
        ]
    },

    # COMT fast (Val/Val) - May benefit from more stimulation
    "COMT_fast": {
        "emphasize": [
            "Proteinrika frukostlar (agg, yoghurt)",
            "Tyrosinrika livsmedel (kyckling, kalkon, mandel)",
            "Kaffe ar OK (upp till 3-4 koppar)",
            "Gront te for fokus"
        ],
        "avoid": []
    },

    # APOE4 - Cardiovascular and Alzheimer's risk
    "APOE4_carrier": {
        "emphasize": [
            "Fet fisk 3+ ganger/vecka (omega-3 kritiskt)",
            "MCT-olja eller kokosolja (alternativ hjarnenergi)",
            "Olivolja som huvudfettkalla",
            "Blabor och morkla bar (antioxidanter)",
            "Valnotter (DHA)",
            "Kurkuma med svartpeppar",
            "Medelhavsbaserad kost"
        ],
        "avoid": [
            "Mattat fett fran kott (<7% av kalorier)",
            "Transfetter",
            "Processad mat",
            "Alkohol (begransad eller undvik helt)",
            "Friterad mat",
            "Hogt sokrintag"
        ]
    },

    # FADS1/FADS2 low activity - Can't convert ALA to EPA/DHA
    "FADS_low": {
        "emphasize": [
            "Direkt EPA/DHA - fet fisk obligatoriskt 3+ ggr/vecka",
            "Fiskolja-tillskott dagligen",
            "Algbaserad omega-3 for vegetarianer",
            "Lax, makrill, sardiner, anjovis, sill"
        ],
        "avoid": [
            "Forlita dig INTE pa vaxtbaserad omega-3 (linfro, chia)",
            "ALA konverteras inte effektivt"
        ]
    },

    # VDR variants - Vitamin D metabolism
    "VDR_impaired": {
        "emphasize": [
            "Fet fisk (D-vitamin)",
            "Aggula",
            "Svamp (UV-exponerad)",
            "D-vitaminberikat livsmedel",
            "Solexponering 15-20 min/dag (nar mojligt)"
        ],
        "avoid": []
    },

    # CYP1A2 slow - Caffeine sensitive
    "CYP1A2_slow": {
        "emphasize": [
            "Koffeinfritt kaffe",
            "Ortte",
            "Gront te (lagre koffein)"
        ],
        "avoid": [
            "Kaffe efter kl 14",
            "Energidrycker",
            "Hog koffeindos (>200mg/dag)"
        ]
    },

    # CYP1A2 fast - Can handle caffeine
    "CYP1A2_fast": {
        "emphasize": [
            "Kaffe ar OK (upp till 4 koppar/dag)",
            "Kaffe kan vara skyddande for kardiovaskulart"
        ],
        "avoid": []
    },

    # IL-6/TNF-alpha inflammation
    "inflammation_high": {
        "emphasize": [
            "Anti-inflammatoriska livsmedel",
            "Fet fisk (omega-3)",
            "Kurkuma + svartpeppar",
            "Ingefara",
            "Blabor och morkla bar",
            "Olivolja (extra virgin)",
            "Morkgrona bladgronsaker",
            "Valnotter"
        ],
        "avoid": [
            "Socker och raffinerade kolhydrater",
            "Omega-6 rika oljor (solrosolja, majolja)",
            "Processad mat",
            "Transfetter",
            "Rott kott (begransat)",
            "Alkohol"
        ]
    },

    # CYP1B1 + COMT slow - Estrogen metabolism concern
    "estrogen_metabolism_impaired": {
        "emphasize": [
            "Korsblommiga gronsaker DAGLIGEN (broccoli, blomkal, grankol, rucola)",
            "DIM-rika livsmedel (broccoli groddar)",
            "I3C-kallor",
            "Fiberrika livsmedel (binder ostrogen)",
            "Linfroon (lignaner)"
        ],
        "avoid": [
            "Soja i stora mangder (fytoostrogener)",
            "Alkohol (okar ostrogen)",
            "Plastkemikalier (BPA, ftalater)"
        ]
    },

    # HFE variants - Iron metabolism
    "HFE_iron_risk": {
        "emphasize": [
            "Begransat rott kott",
            "Te eller kaffe med maltider (hammar jarnupptag)"
        ],
        "avoid": [
            "Hog jarnrikt kott",
            "C-vitamin med jarnrika maltider"
        ]
    },

    # BCMO1 - Beta-carotene conversion
    "BCMO1_impaired": {
        "emphasize": [
            "Fardigt A-vitamin (retinol) fran lever, agg, mejeriprodukter",
            "Torskleverolja",
            "Kott fran grasbetade djur"
        ],
        "avoid": [
            "Forlita dig INTE bara pa betakaroten (morotter, sotpotatis)"
        ]
    },

    # General detox support
    "detox_support": {
        "emphasize": [
            "Korsblommiga gronsaker (aktiverar fas II-enzymer)",
            "Lok och vitlok (svavelforeningar)",
            "Citrusfrukter (naringenin, d-limonen)",
            "Rodbeta (betain for metylering)",
            "Persilja och koriander"
        ],
        "avoid": [
            "Grilat/brant kott (heterocykliska aminer)",
            "Processad mat med tillsatser"
        ]
    }
}

# =============================================================================
# SUPPLEMENT DATABASE
# =============================================================================

SUPPLEMENT_DATABASE = {
    # Methylation support
    "methylfolate": Supplement(
        name="Metylfolat (5-MTHF)",
        dose="400-800 mcg",
        timing=SupplementTiming.MORNING_WITH_FOOD,
        priority="critical",
        reason="MTHFR-variant - behovs aktiv folat",
        genes=["MTHFR"],
        take_with=["B12 (metylkobalamin)", "B6 (P5P)", "B2 (riboflavin)"],
        avoid_with=["Syntetisk folsyra"],
        drug_interactions=["Metotrexat - konsultera lakare"]
    ),

    "methylcobalamin": Supplement(
        name="Metylkobalamin (B12)",
        dose="500-1000 mcg",
        timing=SupplementTiming.MORNING_WITH_FOOD,
        priority="high",
        reason="Stodjer metyleringscykeln",
        genes=["MTHFR", "MTR", "MTRR"],
        take_with=["Metylfolat", "B6"],
        avoid_with=["Hog dos C-vitamin >1000mg (ta 2 timmar isár)"],
        drug_interactions=["Metformin - B12-brist vanligt"]
    ),

    "riboflavin": Supplement(
        name="Riboflavin (B2)",
        dose="25-50 mg",
        timing=SupplementTiming.MORNING_WITH_FOOD,
        priority="high",
        reason="MTHFR-kofaktor",
        genes=["MTHFR"],
        take_with=["Andra B-vitaminer"],
        avoid_with=[],
        drug_interactions=[]
    ),

    # Vitamin D
    "vitamin_d3": Supplement(
        name="D3-vitamin (kolecalciferol)",
        dose="2000-4000 IE",
        timing=SupplementTiming.MORNING_WITH_FOOD,
        priority="high",
        reason="VDR-variant - behover hogre dos",
        genes=["VDR", "CYP2R1"],
        take_with=["K2 (MK-7)", "Magnesium", "Fett (maltid)"],
        avoid_with=["Hog dos A-vitamin >10000 IE"],
        drug_interactions=["Tiaziddiuretika - okat kalciumrisk"]
    ),

    "vitamin_k2": Supplement(
        name="K2-vitamin (MK-7)",
        dose="100-200 mcg",
        timing=SupplementTiming.MORNING_WITH_FOOD,
        priority="moderate",
        reason="Styr kalcium till skelett (ej artarer)",
        genes=["VDR"],
        take_with=["D3-vitamin", "Fett"],
        avoid_with=[],
        drug_interactions=["Warfarin - HAL K-vitamin STABILT, ej undvik"]
    ),

    # Omega-3
    "omega3_epa_dha": Supplement(
        name="Omega-3 (EPA/DHA)",
        dose="2000-3000 mg",
        timing=SupplementTiming.WITH_LARGEST_MEAL,
        priority="critical",
        reason="FADS-variant/Inflammation - direkt EPA/DHA kravs",
        genes=["FADS1", "FADS2", "IL6", "TNF", "APOE"],
        take_with=["Fet maltid (okar upptag)", "E-vitamin"],
        avoid_with=["Hog omega-6"],
        drug_interactions=["Warfarin/blodformande - overvaka INR vid >3g/dag"],
        notes="rTG-form bast. EPA:DHA 2:1 for inflammation."
    ),

    # Magnesium
    "magnesium_glycinate": Supplement(
        name="Magnesium (glycinat)",
        dose="300-400 mg elemental",
        timing=SupplementTiming.EVENING_BEFORE_BED,
        priority="high",
        reason="Stodjer D-vitamin aktivering, COMT-kofaktor, somn",
        genes=["VDR", "COMT"],
        take_with=["B6 (okar cellulart upptag)", "Taurin"],
        avoid_with=["Kalcium >500mg", "Zink >30mg", "Jarn >25mg (ta 2h isár)"],
        drug_interactions=["Antibiotika (tetracyklin, fluorokinolon) - 2-4h isár"]
    ),

    # L-Theanine for COMT slow
    "l_theanine": Supplement(
        name="L-Theanin",
        dose="200-400 mg",
        timing=SupplementTiming.DIVIDED_DOSES,
        priority="moderate",
        reason="COMT slow - stodjer lugn utan sedation",
        genes=["COMT"],
        take_with=["Magnesium (kvall)", "Kaffe (morgon, 2:1 ratio)"],
        avoid_with=[],
        drug_interactions=["Blodtryckmedicin - kan sanka BT ytterligare"]
    ),

    # DIM for estrogen
    "dim": Supplement(
        name="DIM (Diindolylmetan)",
        dose="100-200 mg",
        timing=SupplementTiming.MORNING_WITH_FOOD,
        priority="high",
        reason="CYP1B1+COMT - stodjer ostrogen 2-OH-vag",
        genes=["CYP1B1", "COMT"],
        take_with=["Mat", "B-vitaminer"],
        avoid_with=[],
        drug_interactions=["Hormoner - konsultera lakare vid HRT"]
    ),

    # NAC for detox
    "nac": Supplement(
        name="NAC (N-Acetyl Cystein)",
        dose="600-1200 mg",
        timing=SupplementTiming.MORNING_EMPTY,
        priority="moderate",
        reason="Glutation-prekursor, detox-stod",
        genes=["GSTP1", "GSTM1", "GSTT1"],
        take_with=["C-vitamin", "Glycin"],
        avoid_with=["Ta ej med mat (aminosyrekonkurrens)"],
        drug_interactions=["Nitroglycerid - forsiktighet"]
    ),

    # CoQ10
    "coq10": Supplement(
        name="CoQ10 (Ubiquinol)",
        dose="100-200 mg",
        timing=SupplementTiming.MORNING_WITH_FOOD,
        priority="moderate",
        reason="Mitokondriell energi, hjarthalsa",
        genes=["APOE"],
        take_with=["Fet maltid", "E-vitamin"],
        avoid_with=[],
        drug_interactions=["Statiner - CoQ10 ofta uttomd"]
    ),

    # Curcumin
    "curcumin": Supplement(
        name="Kurkumin (med peperin)",
        dose="500-1000 mg",
        timing=SupplementTiming.WITH_LARGEST_MEAL,
        priority="moderate",
        reason="Anti-inflammatoriskt, neuroprotektivt",
        genes=["IL6", "TNF", "APOE"],
        take_with=["Svartpeppar (piperin)", "Fett"],
        avoid_with=[],
        drug_interactions=["Blodformande (naturlig antiplatelet-effekt)"]
    ),

    # Zinc
    "zinc": Supplement(
        name="Zink (pikolinat)",
        dose="15-30 mg",
        timing=SupplementTiming.EVENING_BEFORE_BED,
        priority="moderate",
        reason="Immunfunktion, enzymer",
        genes=[],
        take_with=["Koppar 1-2mg (vid langvarig anvandning)"],
        avoid_with=["Kalcium", "Jarn", "Magnesium (ta 2h isár)", "Fytater"],
        drug_interactions=["Antibiotika - 2-4h isár"]
    ),

    # Selenium
    "selenium": Supplement(
        name="Selen (selenometionin)",
        dose="100-200 mcg",
        timing=SupplementTiming.MORNING_WITH_FOOD,
        priority="moderate",
        reason="Tyreoideafunktion, antioxidant",
        genes=[],
        take_with=["E-vitamin", "Jod (synergi)"],
        avoid_with=[],
        drug_interactions=["Cisplatin - undvik under behandling"]
    ),

    # Tyrosine for COMT fast
    "l_tyrosine": Supplement(
        name="L-Tyrosin",
        dose="500-1000 mg",
        timing=SupplementTiming.MORNING_EMPTY,
        priority="moderate",
        reason="COMT fast - stodjer dopaminsyntes",
        genes=["COMT"],
        take_with=["B6", "C-vitamin", "Koppar"],
        avoid_with=["Andra aminosyror (absorption)", "Proteinrik maltid"],
        drug_interactions=["MAO-hammare - UNDVIK", "Levotyroxin - overvaka"]
    )
}

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def determine_genetic_profile(analysis: Dict) -> Dict[str, bool]:
    """Bestam genetiska profiler fran analysresultat."""
    profiles = {
        "MTHFR_impaired": False,
        "COMT_slow": False,
        "COMT_fast": False,
        "APOE4_carrier": False,
        "FADS_low": False,
        "VDR_impaired": False,
        "CYP1A2_slow": False,
        "CYP1A2_fast": False,
        "inflammation_high": False,
        "estrogen_metabolism_impaired": False,
        "HFE_iron_risk": False,
        "detox_support": False
    }

    raw_genotypes = analysis.get("raw_genotypes", {})
    haplotypes = analysis.get("haplotypes", [])
    analyzed_snps = analysis.get("analyzed_snps", [])
    gene_interactions = analysis.get("gene_interactions", [])

    # MTHFR status from haplotypes
    for hap in haplotypes:
        if isinstance(hap, dict):
            gene = hap.get("gene", "")
            haplotype = hap.get("haplotype", "")
            risk = hap.get("risk_level", "")

            if gene == "MTHFR":
                if "TT" in haplotype or "Compound" in haplotype or risk in ["Significantly Increased", "High"]:
                    profiles["MTHFR_impaired"] = True
                elif "CT" in haplotype or "MATTLIG" in str(risk).upper():
                    profiles["MTHFR_impaired"] = True

            if gene == "APOE":
                if "e4" in haplotype.lower():
                    profiles["APOE4_carrier"] = True

    # Check analyzed SNPs
    for snp in analyzed_snps:
        if isinstance(snp, dict):
            gene = snp.get("gene", "")
            genotype = snp.get("genotype", "")
            risk = snp.get("risk_level", "")

            # COMT
            if gene == "COMT":
                if genotype == "AA":  # Met/Met
                    profiles["COMT_slow"] = True
                elif genotype == "GG":  # Val/Val
                    profiles["COMT_fast"] = True

            # FADS1
            if gene == "FADS1":
                if genotype == "TT":
                    profiles["FADS_low"] = True

            # VDR/CYP2R1
            if gene in ["VDR", "CYP2R1"]:
                if risk not in ["Normal", "Protective", "Skyddande"]:
                    profiles["VDR_impaired"] = True

            # CYP1A2
            if gene == "CYP1A2":
                if genotype == "CC":
                    profiles["CYP1A2_slow"] = True
                elif genotype == "AA":
                    profiles["CYP1A2_fast"] = True

            # IL-6, TNF
            if gene in ["IL6", "TNF"]:
                if risk not in ["Normal", "Protective"]:
                    profiles["inflammation_high"] = True

            # CYP1B1
            if gene == "CYP1B1":
                if "G" in genotype:
                    profiles["estrogen_metabolism_impaired"] = True

            # HFE
            if gene == "HFE":
                if risk not in ["Normal", "Protective"]:
                    profiles["HFE_iron_risk"] = True

            # Detox genes
            if gene in ["GSTP1", "GSTM1", "GSTT1"]:
                if risk not in ["Normal", "Protective"]:
                    profiles["detox_support"] = True

    # Check gene interactions
    for interaction in gene_interactions:
        if isinstance(interaction, dict):
            name = interaction.get("name", "")
            if "CYP1B1" in name and "COMT" in name:
                profiles["estrogen_metabolism_impaired"] = True
            if "IL-6" in name and "TNF" in name:
                profiles["inflammation_high"] = True

    return profiles

def generate_supplement_protocol(profiles: Dict[str, bool], analysis: Dict) -> Tuple[List[Supplement], List[Supplement], List[Supplement]]:
    """Generera tillskottsprotokoll baserat pa genetisk profil."""
    morning_supplements = []
    meal_supplements = []
    evening_supplements = []

    # MTHFR support
    if profiles["MTHFR_impaired"]:
        supp = SUPPLEMENT_DATABASE["methylfolate"]
        supp = Supplement(**{**asdict(supp), "dose": "800-1500 mcg" if "TT" in str(analysis) else "400-800 mcg"})
        morning_supplements.append(supp)
        morning_supplements.append(SUPPLEMENT_DATABASE["methylcobalamin"])
        morning_supplements.append(SUPPLEMENT_DATABASE["riboflavin"])

    # VDR/Vitamin D support
    if profiles["VDR_impaired"]:
        supp = SUPPLEMENT_DATABASE["vitamin_d3"]
        supp = Supplement(**{**asdict(supp), "dose": "3000-5000 IE"})
        morning_supplements.append(supp)
        morning_supplements.append(SUPPLEMENT_DATABASE["vitamin_k2"])
    else:
        # Standard D-vitamin
        morning_supplements.append(SUPPLEMENT_DATABASE["vitamin_d3"])
        morning_supplements.append(SUPPLEMENT_DATABASE["vitamin_k2"])

    # Omega-3 - critical for several profiles
    if profiles["APOE4_carrier"]:
        supp = SUPPLEMENT_DATABASE["omega3_epa_dha"]
        supp = Supplement(**{**asdict(supp), "dose": "3000-4000 mg (2:1 EPA:DHA)", "priority": "critical"})
        meal_supplements.append(supp)
    elif profiles["FADS_low"] or profiles["inflammation_high"]:
        supp = SUPPLEMENT_DATABASE["omega3_epa_dha"]
        supp = Supplement(**{**asdict(supp), "dose": "2000-3000 mg", "priority": "critical"})
        meal_supplements.append(supp)
    else:
        meal_supplements.append(SUPPLEMENT_DATABASE["omega3_epa_dha"])

    # Magnesium - most people benefit
    evening_supplements.append(SUPPLEMENT_DATABASE["magnesium_glycinate"])

    # COMT slow support
    if profiles["COMT_slow"]:
        evening_supplements.append(SUPPLEMENT_DATABASE["l_theanine"])
        # Adjust magnesium priority
        for s in evening_supplements:
            if s.name == "Magnesium (glycinat)":
                s.priority = "high"

    # COMT fast support
    if profiles["COMT_fast"]:
        morning_supplements.append(SUPPLEMENT_DATABASE["l_tyrosine"])

    # Estrogen metabolism support
    if profiles["estrogen_metabolism_impaired"]:
        morning_supplements.append(SUPPLEMENT_DATABASE["dim"])

    # Inflammation support
    if profiles["inflammation_high"]:
        meal_supplements.append(SUPPLEMENT_DATABASE["curcumin"])

    # Detox support
    if profiles["detox_support"]:
        morning_supplements.append(SUPPLEMENT_DATABASE["nac"])

    # APOE4 specific
    if profiles["APOE4_carrier"]:
        morning_supplements.append(SUPPLEMENT_DATABASE["coq10"])

    # General - zinc and selenium
    evening_supplements.append(SUPPLEMENT_DATABASE["zinc"])
    morning_supplements.append(SUPPLEMENT_DATABASE["selenium"])

    # Remove duplicates based on name
    def dedupe(supplements):
        seen = set()
        result = []
        for s in supplements:
            if s.name not in seen:
                seen.add(s.name)
                result.append(s)
        return result

    return dedupe(morning_supplements), dedupe(meal_supplements), dedupe(evening_supplements)

def generate_meal_recommendations(profiles: Dict[str, bool]) -> Tuple[MealRecommendation, MealRecommendation, MealRecommendation, MealRecommendation]:
    """Generera maltidsrekommendationer baserat pa genetisk profil."""

    # Aggregate foods to emphasize and avoid
    all_emphasize = set()
    all_avoid = set()

    for profile_name, is_active in profiles.items():
        if is_active and profile_name in GENETIC_FOOD_RECOMMENDATIONS:
            recs = GENETIC_FOOD_RECOMMENDATIONS[profile_name]
            all_emphasize.update(recs.get("emphasize", []))
            all_avoid.update(recs.get("avoid", []))

    # Always add detox support foods
    all_emphasize.update(GENETIC_FOOD_RECOMMENDATIONS["detox_support"]["emphasize"])

    # Generate meal-specific recommendations
    breakfast = MealRecommendation(
        meal_time=MealTime.BREAKFAST,
        foods_to_emphasize=[
            "Agg (kolin, B-vitaminer)",
            "Avokado (halsosamt fett, K)",
            "Spenat eller grankol (folat)",
            "Bar (antioxidanter)",
            "Havregrot med notter (fiber, magnesium)"
        ],
        foods_to_avoid=[f for f in all_avoid if "frukostflingor" in f.lower() or "brod" in f.lower() or "energidryck" in f.lower()],
        example_meals=[
            "Rorod agg med spenat och avokado",
            "Grekisk yoghurt med bar, valnotter och honung",
            "Smoothie med grankol, blabor, proteinpulver och linfro",
            "Havregrot med kanelpumpakaernor och mandlar"
        ],
        notes="Ta D3+K2 och B-vitaminer med frukosten."
    )

    lunch = MealRecommendation(
        meal_time=MealTime.LUNCH,
        foods_to_emphasize=[
            "Gronsaker - minst halva tallriken",
            "Proteinrik kalla (fisk, kyckling, agg, bonor)",
            "Korsblommiga gronsaker (broccoli, blomkal)",
            "Olivolja som dressing",
            "Komplexa kolhydrater (sötpotatis, quinoa)"
        ],
        foods_to_avoid=[f for f in all_avoid if "processad" in f.lower() or "socker" in f.lower()],
        example_meals=[
            "Laxsallad med avokado, rodbeta och olivolja",
            "Kycklingwok med broccoli, paprika och quinoa",
            "Linssoppa med grankol och citron",
            "Buddha bowl med rostade gronsaker, hummus och feta"
        ],
        notes="Storsta maltiden - ta Omega-3 har."
    )

    dinner = MealRecommendation(
        meal_time=MealTime.DINNER,
        foods_to_emphasize=[
            "Fisk (lax, makrill) minst 3 ggr/vecka",
            "Morkgrona gronsaker",
            "Lugnade kryddor (kurkuma, ingefara)",
            "Magnesiumrika livsmedel (mork choklad, pumpakaernor)"
        ],
        foods_to_avoid=[f for f in all_avoid if "alkohol" in f.lower() or "koffein" in f.lower() or "stimulerande" in f.lower()],
        example_meals=[
            "Ugnsbakad lax med sparris och sotpotatis",
            "Kycklinggryta med kurkuma, kokosmjolk och spenat",
            "Makrill med rostad blomkal och tahini",
            "Vegetarisk curry med kikarter och grankol"
        ],
        notes="Undvik tunga maltider 3h fore laggdags. Ta magnesium och zink efter middagen."
    )

    snack = MealRecommendation(
        meal_time=MealTime.SNACK,
        foods_to_emphasize=[
            "Notter (valnotter, mandlar, brasilnotter)",
            "Bar (blabor, hallonmorkachoklad)",
            "Gronsakssticks med hummus",
            "Gront te eller ortte"
        ],
        foods_to_avoid=[f for f in all_avoid if "socker" in f.lower() or "processad" in f.lower()],
        example_meals=[
            "En handfull valnotter + en handfull blabor",
            "Selleri med mandelsmorolja och gront te",
            "2 rutor mark choklad (>70%) + brasilnotter",
            "Avokado med havssalt och citron"
        ],
        notes="Mellanmal stabiliserar blodsockret. Undvik socker."
    )

    return breakfast, lunch, dinner, snack

def generate_weekly_meal_plan(profiles: Dict[str, bool]) -> Dict[str, Dict[str, str]]:
    """Generera en veckoplan for maltider."""

    # Base weekly plan - emphasizing fish for omega-3
    fish_days = ["Måndag", "Onsdag", "Fredag"]
    if profiles["APOE4_carrier"] or profiles["FADS_low"]:
        fish_days = ["Måndag", "Onsdag", "Fredag", "Söndag"]  # Extra fish

    weekly_plan = {
        "Måndag": {
            "frukost": "Rorod agg med spenat, avokado och pumpakaernor",
            "lunch": "Linsallad med broccoli, rodbeta, feta och olivolja",
            "middag": "Ugnsbakad lax med sparris och sotpotatis"
        },
        "Tisdag": {
            "frukost": "Havregrot med blabor, valnotter och kanel",
            "lunch": "Kycklingwok med broccoli, paprika och quinoa",
            "middag": "Vegetarisk linscurry med spenat och fullkornsris"
        },
        "Onsdag": {
            "frukost": "Smoothie: grankol, blabor, banan, mandelmjolk, linfro",
            "lunch": "Sallad med rostade kikarter, avokado och citronvinagrette",
            "middag": "Grillad makrill med rostad blomkal och tahini"
        },
        "Torsdag": {
            "frukost": "Agg-muffins med spenat och getost",
            "lunch": "Buddha bowl med quinoa, rostade gronsaker och hummus",
            "middag": "Kycklinggryta med kurkuma, kokosmjolk och grankol"
        },
        "Fredag": {
            "frukost": "Grekisk yoghurt med granola, bar och valnotter",
            "lunch": "Linssoppa med citron och persilja",
            "middag": "Sardiner pa rostad surdegsbrod med avokado och tomat"
        },
        "Lördag": {
            "frukost": "Pannkakor av bananoch agg med bar och mandelsmorolja",
            "lunch": "Sallad nicoise med agg och gront te",
            "middag": "Hemmagjord taco med svarta bonor, avokadosaslotpotatis"
        },
        "Söndag": {
            "frukost": "Agg benedict med rokt lax och spenat",
            "lunch": "Kyckling- och gronsakswok med cashewnotter",
            "middag": "Ugnsrostad kyckling med rotfrukter och grankol"
        }
    }

    # Adjust for APOE4 - add extra fish on Sunday
    if profiles["APOE4_carrier"]:
        weekly_plan["Söndag"]["middag"] = "Grillad havorre med medelhavsgronsaker och olivolja"

    return weekly_plan

def generate_critical_warnings(profiles: Dict[str, bool], analysis: Dict) -> List[str]:
    """Generera kritiska varningar baserat pa genetik."""
    warnings = []

    drug_alerts = analysis.get("drug_alerts", [])

    # Drug warnings from analysis
    for alert in drug_alerts:
        if isinstance(alert, dict):
            drug = alert.get("drug", "")
            action = alert.get("action", "")
            if "UNDVIK" in action.upper() or drug.lower() in ["warfarin", "clopidogrel"]:
                warnings.append(f"LAKEMEDEL: {drug} - {action}")

    # MTHFR warning
    if profiles["MTHFR_impaired"]:
        warnings.append("MTHFR: UNDVIK syntetisk folsyra. Valj metylfolat. UNDVIK lustgas vid operation.")

    # COMT slow warning
    if profiles["COMT_slow"]:
        warnings.append("COMT: Undvik gront te-extrakt/EGCG-tillskott. Var forskrikt med stimulantia och hog koffeindos.")

    # APOE4 warning
    if profiles["APOE4_carrier"]:
        warnings.append("APOE e4: KRITISKT begransat mattat fett (<7%). Undvik alkohol. Omega-3 hogdos obligatoriskt.")

    # Estrogen warning
    if profiles["estrogen_metabolism_impaired"]:
        warnings.append("OSTROGEN: Var forsiktig vid HRT/p-piller. Diskutera med lakare. DIM och korsblommiga dagligen.")

    return warnings

# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_lifestyle_plan(analysis: Dict) -> LifestylePlan:
    """Generera komplett livsstilsplan fran DNA-analys."""

    name = analysis.get("name", "Anonym")

    # Determine genetic profile
    profiles = determine_genetic_profile(analysis)

    # Generate genetic summary
    genetic_summary = {}
    for profile, is_active in profiles.items():
        if is_active:
            readable_name = profile.replace("_", " ").title()
            genetic_summary[readable_name] = "Ja"

    # Generate supplement protocol
    morning, meals, evening = generate_supplement_protocol(profiles, analysis)

    # Generate meal recommendations
    breakfast, lunch, dinner, snack = generate_meal_recommendations(profiles)

    # Generate weekly plan
    weekly_plan = generate_weekly_meal_plan(profiles)

    # Generate warnings
    warnings = generate_critical_warnings(profiles, analysis)

    # Lifestyle recommendations
    lifestyle_recs = [
        "Solexponering 15-20 min/dag (utan solskydd) for D-vitamin",
        "Regelbunden styrketraning 2-3 ggr/vecka",
        "7-9 timmars somn per natt",
        "Stresshantering dagligen (meditation, djupandning, promenader)",
        "Begransat skarmtid 1h fore laggdags",
        "Rikligt vatten (2-3 liter/dag)"
    ]

    if profiles["COMT_slow"]:
        lifestyle_recs.insert(0, "COMT: Prioritera stresshantering hogt. Yoga och meditation sarskilt fordelaktigt.")

    if profiles["APOE4_carrier"]:
        lifestyle_recs.insert(0, "APOE e4: Regelbunden aerob traning 30+ min/dag for kognitiv halsa.")

    # Get explanations for active profiles
    genetic_explanations = {}
    for profile, is_active in profiles.items():
        if is_active and profile in GENETIC_PROFILE_EXPLANATIONS:
            genetic_explanations[profile] = GENETIC_PROFILE_EXPLANATIONS[profile]

    return LifestylePlan(
        name=name,
        generated_date=datetime.now().isoformat(),
        genetic_summary=genetic_summary,
        supplements_morning=morning,
        supplements_with_meals=meals,
        supplements_evening=evening,
        breakfast_recommendations=breakfast,
        lunch_recommendations=lunch,
        dinner_recommendations=dinner,
        snack_recommendations=snack,
        weekly_meal_plan=weekly_plan,
        critical_warnings=warnings,
        lifestyle_recommendations=lifestyle_recs,
        genetic_explanations=genetic_explanations
    )

def generate_markdown_report(plan: LifestylePlan) -> str:
    """Generera Markdown-rapport."""
    lines = [
        f"# GWL Livsstilsplan: {plan.name}",
        f"**Genererad:** {plan.generated_date[:10]}",
        "",
        "---",
        "",
        "## Genetisk Sammanfattning",
        ""
    ]

    if plan.genetic_summary:
        for profile, status in plan.genetic_summary.items():
            lines.append(f"- **{profile}:** {status}")
    else:
        lines.append("- Inga specifika riskprofiler identifierade")
    lines.append("")

    # Critical warnings
    if plan.critical_warnings:
        lines.append("## VIKTIGA VARNINGAR")
        lines.append("")
        for warning in plan.critical_warnings:
            lines.append(f"- {warning}")
        lines.append("")

    # Genetic explanations
    if plan.genetic_explanations:
        lines.append("---")
        lines.append("")
        lines.append("## DINA GENETISKA PROFILER - VAD DE BETYDER")
        lines.append("")
        lines.append("*Nedan förklaras vad varje identifierad genetisk profil innebär för dig.*")
        lines.append("")

        for profile_key, explanation in plan.genetic_explanations.items():
            lines.append(f"### {explanation['name']}")
            lines.append("")

            lines.append("**Vad är detta?**")
            lines.append("")
            for paragraph in explanation['what_it_is'].strip().split('\n\n'):
                lines.append(paragraph.strip())
                lines.append("")

            lines.append("**Vad din variant innebär:**")
            lines.append("")
            for paragraph in explanation['what_variant_means'].strip().split('\n\n'):
                lines.append(paragraph.strip())
                lines.append("")

            lines.append("**Varför dessa rekommendationer?**")
            lines.append("")
            for paragraph in explanation['why_recommendation'].strip().split('\n\n'):
                lines.append(paragraph.strip())
                lines.append("")

            lines.append("---")
            lines.append("")

    # Supplement Protocol
    lines.append("---")
    lines.append("")
    lines.append("## TILLSKOTTSPROTOKOLL")
    lines.append("")

    # Morning
    lines.append("### Morgon (med frukost)")
    lines.append("")
    lines.append("| Tillskott | Dos | Prioritet | Anledning |")
    lines.append("|-----------|-----|-----------|-----------|")
    for supp in plan.supplements_morning:
        lines.append(f"| **{supp.name}** | {supp.dose} | {supp.priority.upper()} | {supp.reason} |")
    lines.append("")

    # With meals
    lines.append("### Med storsta maltid (lunch/middag)")
    lines.append("")
    lines.append("| Tillskott | Dos | Prioritet | Anledning |")
    lines.append("|-----------|-----|-----------|-----------|")
    for supp in plan.supplements_with_meals:
        lines.append(f"| **{supp.name}** | {supp.dose} | {supp.priority.upper()} | {supp.reason} |")
    lines.append("")

    # Evening
    lines.append("### Kvall (fore laggdags)")
    lines.append("")
    lines.append("| Tillskott | Dos | Prioritet | Anledning |")
    lines.append("|-----------|-----|-----------|-----------|")
    for supp in plan.supplements_evening:
        lines.append(f"| **{supp.name}** | {supp.dose} | {supp.priority.upper()} | {supp.reason} |")
    lines.append("")

    # Supplement interactions
    lines.append("### Viktiga interaktioner")
    lines.append("")
    all_supps = plan.supplements_morning + plan.supplements_with_meals + plan.supplements_evening
    for supp in all_supps:
        if supp.drug_interactions:
            for interaction in supp.drug_interactions:
                lines.append(f"- **{supp.name}:** {interaction}")
    lines.append("")

    # Meal Plan
    lines.append("---")
    lines.append("")
    lines.append("## MALTIDSPLAN")
    lines.append("")

    # Breakfast
    lines.append("### Frukost")
    lines.append("")
    lines.append("**Betonanar:**")
    for food in plan.breakfast_recommendations.foods_to_emphasize:
        lines.append(f"- {food}")
    lines.append("")
    if plan.breakfast_recommendations.foods_to_avoid:
        lines.append("**Undvik:**")
        for food in plan.breakfast_recommendations.foods_to_avoid:
            lines.append(f"- {food}")
        lines.append("")
    lines.append("**Exempel:**")
    for meal in plan.breakfast_recommendations.example_meals:
        lines.append(f"- {meal}")
    lines.append("")

    # Lunch
    lines.append("### Lunch")
    lines.append("")
    lines.append("**Betona:**")
    for food in plan.lunch_recommendations.foods_to_emphasize:
        lines.append(f"- {food}")
    lines.append("")
    lines.append("**Exempel:**")
    for meal in plan.lunch_recommendations.example_meals:
        lines.append(f"- {meal}")
    lines.append("")

    # Dinner
    lines.append("### Middag")
    lines.append("")
    lines.append("**Betona:**")
    for food in plan.dinner_recommendations.foods_to_emphasize:
        lines.append(f"- {food}")
    lines.append("")
    if plan.dinner_recommendations.foods_to_avoid:
        lines.append("**Undvik:**")
        for food in plan.dinner_recommendations.foods_to_avoid:
            lines.append(f"- {food}")
        lines.append("")
    lines.append("**Exempel:**")
    for meal in plan.dinner_recommendations.example_meals:
        lines.append(f"- {meal}")
    lines.append("")

    # Weekly plan
    lines.append("---")
    lines.append("")
    lines.append("## VECKOPLAN")
    lines.append("")
    lines.append("| Dag | Frukost | Lunch | Middag |")
    lines.append("|-----|---------|-------|--------|")
    for day, meals in plan.weekly_meal_plan.items():
        frukost = meals.get("frukost", "")[:40] + "..." if len(meals.get("frukost", "")) > 40 else meals.get("frukost", "")
        lunch = meals.get("lunch", "")[:40] + "..." if len(meals.get("lunch", "")) > 40 else meals.get("lunch", "")
        middag = meals.get("middag", "")[:40] + "..." if len(meals.get("middag", "")) > 40 else meals.get("middag", "")
        lines.append(f"| **{day}** | {frukost} | {lunch} | {middag} |")
    lines.append("")

    # Lifestyle
    lines.append("---")
    lines.append("")
    lines.append("## LIVSSTILSREKOMMENDATIONER")
    lines.append("")
    for rec in plan.lifestyle_recommendations:
        lines.append(f"- {rec}")
    lines.append("")

    # Daily schedule
    lines.append("---")
    lines.append("")
    lines.append("## DAGLIG RUTIN")
    lines.append("")
    lines.append("```")
    lines.append("MORGON (07:00-08:00)")
    lines.append("  - Solljus 15 min (utan solskydd)")
    lines.append("  - Frukost")
    lines.append("  - Tillskott: " + ", ".join([s.name for s in plan.supplements_morning[:3]]))
    lines.append("")
    lines.append("LUNCH (12:00-13:00)")
    lines.append("  - Storsta maltiden")
    lines.append("  - Tillskott: " + ", ".join([s.name for s in plan.supplements_with_meals]))
    lines.append("")
    lines.append("EFTERMIDDAG (15:00-16:00)")
    lines.append("  - Mellanmal")
    lines.append("  - Promenad 20-30 min")
    lines.append("")
    lines.append("MIDDAG (18:00-19:00)")
    lines.append("  - Lattare an lunch")
    lines.append("  - Minst 3h fore laggdags")
    lines.append("")
    lines.append("KVALL (21:00-22:00)")
    lines.append("  - Tillskott: " + ", ".join([s.name for s in plan.supplements_evening]))
    lines.append("  - Undvik skarmar")
    lines.append("  - Avslappning")
    lines.append("```")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("*Genererad av Genetic Wellness Labs - Nutrigenomics Platform*")
    lines.append("")
    lines.append("**Disclaimer:** Denna plan ar endast for informationsandamal och ersatter inte medicinsk radgivning. Konsultera alltid lakare innan du borjar med nya tillskott, sarskilt om du tar lakemedel.")

    return '\n'.join(lines)

def save_lifestyle_plan(plan: LifestylePlan, output_dir: str = "."):
    """Spara livsstilsplan."""
    base_name = f"GWL_Livsstilsplan_{plan.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"

    # Markdown
    md_path = os.path.join(output_dir, f"{base_name}.md")
    md_content = generate_markdown_report(plan)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Sparade Markdown: {md_path}")

    # JSON
    json_path = os.path.join(output_dir, f"{base_name}.json")

    def convert(obj):
        if hasattr(obj, '__dataclass_fields__'):
            d = asdict(obj)
            # Convert enums
            for k, v in d.items():
                if isinstance(v, Enum):
                    d[k] = v.value
            return d
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, list):
            return [convert(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        return obj

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(convert(plan), f, indent=2, ensure_ascii=False, default=str)
    print(f"Sparade JSON: {json_path}")

    return md_path, json_path

# =============================================================================
# MAIN
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description='GWL Lifestyle Planner - Maltids- och tillskottsplan fran DNA')
    parser.add_argument('analysis_file', nargs='?', help='JSON-fil fran gwl_analyzer.py')
    parser.add_argument('--output', '-o', default='.', help='Output directory')
    parser.add_argument('--demo', action='store_true', help='Kor demo med exempeldata')

    args = parser.parse_args()

    if args.demo:
        # Demo mode with sample data
        print("\n" + "="*60)
        print("GWL LIFESTYLE PLANNER - DEMO")
        print("="*60)

        demo_analysis = {
            "name": "Demo Person",
            "analyzed_snps": [
                {"gene": "COMT", "genotype": "AA", "risk_level": "Lätt förhöjd"},
                {"gene": "CYP1B1", "genotype": "CG", "risk_level": "Lätt förhöjd"},
                {"gene": "FADS1", "genotype": "CT", "risk_level": "Normal"},
                {"gene": "IL6", "genotype": "CG", "risk_level": "Lätt förhöjd"},
                {"gene": "VDR", "genotype": "Aa", "risk_level": "Lätt förhöjd"}
            ],
            "haplotypes": [
                {"gene": "APOE", "haplotype": "e3/e3", "risk_level": "Normal"},
                {"gene": "MTHFR", "haplotype": "CT/AA", "risk_level": "Lätt förhöjd"}
            ],
            "gene_interactions": [
                {"name": "CYP1B1 hog + COMT Met/Met", "genes": ["CYP1B1", "COMT"]}
            ],
            "drug_alerts": [
                {"drug": "SSRI", "action": "Ökad känslighet"},
                {"drug": "Warfarin", "action": "Reducerad metabolism"}
            ],
            "raw_genotypes": {}
        }

        plan = generate_lifestyle_plan(demo_analysis)
        save_lifestyle_plan(plan, args.output)

        print("\nDemo-plan genererad!")
        return

    if not args.analysis_file:
        parser.print_help()
        print("\nAnvandning:")
        print("  python gwl_lifestyle_planner.py GWL_Profil_Namn_Datum.json")
        print("  python gwl_lifestyle_planner.py --demo")
        return

    if not os.path.exists(args.analysis_file):
        print(f"Error: Filen hittades inte: {args.analysis_file}")
        return

    print("\n" + "="*60)
    print("GWL LIFESTYLE PLANNER")
    print("="*60)

    # Load analysis
    print(f"Laddar analys: {args.analysis_file}")
    with open(args.analysis_file, 'r', encoding='utf-8') as f:
        analysis = json.load(f)

    # Generate plan
    print("Genererar livsstilsplan...")
    plan = generate_lifestyle_plan(analysis)

    # Print summary
    print(f"\nGenetisk profil for {plan.name}:")
    for profile, status in plan.genetic_summary.items():
        print(f"  - {profile}")

    print(f"\nTillskott morgon: {len(plan.supplements_morning)}")
    print(f"Tillskott maltid: {len(plan.supplements_with_meals)}")
    print(f"Tillskott kvall: {len(plan.supplements_evening)}")

    if plan.critical_warnings:
        print(f"\nKRITISKA VARNINGAR: {len(plan.critical_warnings)}")
        for w in plan.critical_warnings[:3]:
            print(f"  ! {w[:60]}...")

    # Save
    save_lifestyle_plan(plan, args.output)

    print("\nKlar!")

if __name__ == "__main__":
    main()
