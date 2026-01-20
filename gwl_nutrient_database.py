#!/usr/bin/env python3
"""
GWL Nutrient Database - Komplett näringsdatabas med doseringsinfo
==================================================================

Innehåller för varje näringsämne:
- RDI (Recommended Daily Intake) - officiella rekommendationer
- Optimal daglig dos - baserat på forskning
- UL (Upper Tolerable Limit) - övre gräns innan biverkningar
- LD50 - toxisk dos (för medvetenhet)
- Bristsymptom
- Överdossymptom
- Interaktioner med läkemedel
- Bästa källor (kost och tillskott)
- Genetiska modifieringar (vilka gener påverkar behovet)
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class NutrientCategory(Enum):
    VITAMIN_FAT_SOLUBLE = "Fettlösliga vitaminer"
    VITAMIN_WATER_SOLUBLE = "Vattenlösliga vitaminer"
    MINERAL_MACRO = "Makromineraler"
    MINERAL_TRACE = "Spårmineraler"
    FATTY_ACID = "Fettsyror"
    AMINO_ACID = "Aminosyror"
    OTHER = "Övrigt"

class PopulationGroup(Enum):
    ADULT_MALE = "Vuxen man (19-50)"
    ADULT_FEMALE = "Vuxen kvinna (19-50)"
    PREGNANT = "Gravid"
    LACTATING = "Ammande"
    ELDERLY = "Äldre (65+)"
    CHILD = "Barn"

@dataclass
class DoseInfo:
    """Doseringsinformation för en population"""
    population: PopulationGroup
    rdi: float                    # Recommended Daily Intake (officiellt)
    optimal_low: float            # Optimal dos - nedre gräns
    optimal_high: float           # Optimal dos - övre gräns
    ul: float                     # Upper Tolerable Limit
    unit: str                     # Enhet (mg, mcg, IE, g)

@dataclass
class GeneticModifier:
    """Hur en gen påverkar behovet"""
    gene: str
    rsid: str
    risk_genotype: str
    effect: str                   # Hur genotypen påverkar behovet
    dose_adjustment: str          # Konkret dosjustering

@dataclass
class DrugInteraction:
    """Interaktion med läkemedel"""
    drug_class: str
    examples: List[str]
    interaction: str
    recommendation: str

@dataclass
class Nutrient:
    """Komplett näringsämne"""
    name: str
    category: NutrientCategory

    # Grundläggande info
    description: str
    primary_functions: List[str]

    # Dosering
    doses: List[DoseInfo]
    therapeutic_range: str        # Terapeutiskt intervall för specifika tillstånd
    ld50_info: str               # Toxicitetsinformation

    # Bristsymptom
    deficiency_symptoms: List[str]
    deficiency_diseases: List[str]
    deficiency_risk_factors: List[str]

    # Överdossymptom
    excess_symptoms: List[str]
    toxicity_threshold: str

    # Källor
    food_sources: List[str]
    supplement_forms: List[str]
    best_form: str               # Bästa tillskottsformen
    absorption_tips: List[str]

    # Genetik
    genetic_modifiers: List[GeneticModifier]

    # Interaktioner
    drug_interactions: List[DrugInteraction]
    nutrient_interactions: List[str]

    # Timing
    best_time: str
    with_food: bool

    # Referenser
    references: List[str]


# =============================================================================
# NUTRIENT DATABASE
# =============================================================================

NUTRIENT_DATABASE: Dict[str, Nutrient] = {

    # =========================================================================
    # VITAMIN D
    # =========================================================================
    "vitamin_d": Nutrient(
        name="Vitamin D (D3/Kolekalciferol)",
        category=NutrientCategory.VITAMIN_FAT_SOLUBLE,

        description="""
Vitamin D är egentligen ett hormon som reglerar över 1000 gener i kroppen.
Det produceras i huden vid UVB-exponering och omvandlas i lever och njurar
till aktiv form (1,25-dihydroxyvitamin D). Kritiskt för kalciumupptag,
immunförsvar, muskelfunktion och mental hälsa.
        """.strip(),

        primary_functions=[
            "Kalciumabsorption i tarmen (ökar upptaget 10-40x)",
            "Benhälsa och skelettmineralisering",
            "Immunsystemreglering (både aktivering och dämpning)",
            "Muskelfunktion och styrka",
            "Celldelning och differentiering",
            "Insulinsekretion och blodsockerreglering",
            "Hjärt-kärlhälsa",
            "Neurologisk funktion och mental hälsa"
        ],

        doses=[
            DoseInfo(PopulationGroup.ADULT_MALE, rdi=400, optimal_low=2000, optimal_high=4000, ul=4000, unit="IE"),
            DoseInfo(PopulationGroup.ADULT_FEMALE, rdi=400, optimal_low=2000, optimal_high=4000, ul=4000, unit="IE"),
            DoseInfo(PopulationGroup.PREGNANT, rdi=600, optimal_low=2000, optimal_high=4000, ul=4000, unit="IE"),
            DoseInfo(PopulationGroup.ELDERLY, rdi=800, optimal_low=2000, optimal_high=5000, ul=4000, unit="IE"),
        ],

        therapeutic_range="""
BLODVÄRDEN (25-OH-D):
- Brist: <30 nmol/L (12 ng/mL) - associerat med rakit/osteomalaci
- Insufficiens: 30-50 nmol/L (12-20 ng/mL)
- Adekvat: 50-75 nmol/L (20-30 ng/mL) - officiell rekommendation
- Optimal: 75-125 nmol/L (30-50 ng/mL) - stöds av forskning
- Möjlig överskott: >150 nmol/L (60 ng/mL)
- Toxicitet: >375 nmol/L (150 ng/mL)

DOSERING VID BRIST:
- Mild brist: 2000-4000 IE/dag i 8-12 veckor
- Måttlig brist: 5000-10000 IE/dag i 8-12 veckor (under övervakning)
- Svår brist: Läkarsupervision, ofta 50000 IE/vecka
        """.strip(),

        ld50_info="""
LD50: Inte fastställt för människor.
TOXISK DOS: >10,000 IE/dag under längre perioder KAN orsaka hyperkalcemi.
RAPPORTERADE TOXICITETSFALL: Oftast >40,000-100,000 IE/dag i månader.
SÄKERHETSMARGINAL: Bred - det krävs extrema doser för toxicitet.
RISK: Hyperkalcemi (förhöjt kalcium) som kan skada njurar och hjärta.
        """.strip(),

        deficiency_symptoms=[
            "Trötthet och energibrist",
            "Muskelsvaghet och värk",
            "Benvärk (särskilt rygg, höfter, ben)",
            "Nedsatt immunförsvar (frekventa infektioner)",
            "Nedstämdhet, depression (särskilt vintertid)",
            "Försämrad sårläkning",
            "Håravfall",
            "Försämrad kognitiv funktion"
        ],

        deficiency_diseases=[
            "Rakit (barn) - skelettdeformiteter",
            "Osteomalaci (vuxna) - mjuka ben",
            "Osteoporos - benskörhet",
            "Sekundär hyperparatyreoidism"
        ],

        deficiency_risk_factors=[
            "Skandinaviskt klimat (oktober-mars)",
            "Mörkare hudton (mer melanin blockerar UVB)",
            "Äldre ålder (tunnare hud, sämre omvandling)",
            "Övervikt (D-vitamin lagras i fett)",
            "Inomhusvistelse/solskydd",
            "Vegansk kost",
            "Malabsorption (Crohn, celiaki)",
            "Njur- eller leversjukdom"
        ],

        excess_symptoms=[
            "Hyperkalcemi: illamående, kräkningar, förstoppning",
            "Polyuri (ökad urinering) och törst",
            "Njursten",
            "Förvirring, desorientering",
            "Hjärtarytmier (allvarligt)",
            "Njursvikt (vid långvarig toxicitet)"
        ],

        toxicity_threshold="Generellt >10,000 IE/dag under månader. Individuell variation finns.",

        food_sources=[
            "Fet fisk (lax, makrill, sill): 400-1000 IE/100g",
            "Torskleverolja: 1360 IE/matsked",
            "Äggula: 40 IE/ägg",
            "Berikade mejeriprodukter: 40-100 IE/portion",
            "Svamp (UV-exponerad): varierande",
            "Lever: 50 IE/100g"
        ],

        supplement_forms=[
            "D3 (kolekalciferol) - rekommenderas, naturlig form",
            "D2 (ergokalciferol) - växtbaserad, mindre effektiv",
            "Kalcitriol (aktiv form) - receptbelagt för njursjuka"
        ],

        best_form="D3 (kolekalciferol) i oljebaserad kapsel för bäst absorption. MCT-olja eller olivolja som bärare.",

        absorption_tips=[
            "Ta med fetrik måltid (ökar absorption 50%)",
            "Undvik att ta tillsammans med fiber/fytater",
            "Magnesium behövs för aktivering",
            "Vitamin K2 rekommenderas för att dirigera kalcium till ben"
        ],

        genetic_modifiers=[
            GeneticModifier(
                gene="VDR",
                rsid="rs2228570",
                risk_genotype="TT (f/f)",
                effect="Mindre aktiv D-vitaminreceptor, sämre respons på D-vitamin",
                dose_adjustment="Kan behöva 25-50% högre dos för samma serumnivåer"
            ),
            GeneticModifier(
                gene="CYP2R1",
                rsid="rs10741657",
                risk_genotype="AA",
                effect="Reducerad 25-hydroxylering i lever (aktivering av D-vitamin)",
                dose_adjustment="Systematiskt högre dos krävs. Kontrollera 25(OH)D regelbundet."
            ),
            GeneticModifier(
                gene="GC",
                rsid="rs2282679",
                risk_genotype="CC",
                effect="Lägre vitamin D-bindande protein = lägre totalt 25(OH)D",
                dose_adjustment="Blodtest kan ge falskt låga värden. Överväg fritt 25(OH)D-test."
            ),
            GeneticModifier(
                gene="DHCR7",
                rsid="rs12785878",
                risk_genotype="GG",
                effect="Reducerad D-vitaminsyntes i huden vid solexponering",
                dose_adjustment="Mer beroende av kost/tillskott. Sol ger mindre effekt."
            ),
        ],

        drug_interactions=[
            DrugInteraction(
                drug_class="Kortikosteroider",
                examples=["Prednisolon", "Betametason"],
                interaction="Minskar kalciumabsorption, ökar D-vitaminbehov",
                recommendation="Överväg 1000-2000 IE extra under behandling"
            ),
            DrugInteraction(
                drug_class="Antiepileptika",
                examples=["Fenytoin", "Karbamazepin", "Fenobarbital"],
                interaction="Ökar D-vitaminnedbrytning via CYP450",
                recommendation="Kan behöva 2-4x normal dos. Monitorera 25(OH)D."
            ),
            DrugInteraction(
                drug_class="Kolesterolsänkare (gallsyrabindare)",
                examples=["Kolestyramin", "Kolestipol"],
                interaction="Minskar absorption av fettlösliga vitaminer",
                recommendation="Ta D-vitamin 2 timmar före eller 4-6 timmar efter"
            ),
            DrugInteraction(
                drug_class="Orlistat",
                examples=["Xenical", "Alli"],
                interaction="Minskar fettabsorption och därmed D-vitaminabsorption",
                recommendation="Ta D-vitamin vid annan tidpunkt, överväg högre dos"
            ),
            DrugInteraction(
                drug_class="Hjärtglykosider",
                examples=["Digoxin"],
                interaction="D-vitamin ökar kalcium, förstärker digoxineffekt/toxicitet",
                recommendation="Var försiktig med höga D-vitamindoser. Monitorera kalcium."
            ),
        ],

        nutrient_interactions=[
            "MAGNESIUM - krävs för att aktivera D-vitamin (brist vanlig)",
            "VITAMIN K2 - dirigerar kalcium till ben istället för artärer",
            "KALCIUM - D-vitamin ökar absorption, ta inte megadoser kalcium",
            "VITAMIN A - hög dos A-vitamin kan motverka D-vitamin",
            "ZINK - D-vitamin ökar zinkbehov"
        ],

        best_time="Morgon eller lunch med fetrik måltid. Undvik kvällen (kan störa melatonin).",
        with_food=True,

        references=[
            "Holick MF. Vitamin D deficiency. N Engl J Med. 2007;357(3):266-81",
            "Heaney RP. Vitamin D in health and disease. Clin J Am Soc Nephrol. 2008;3(5):1535-41",
            "Ross AC et al. The 2011 report on dietary reference intakes for calcium and vitamin D. 2011",
            "Vieth R. Vitamin D supplementation: cholecalciferol, calcifediol, and calcitriol. Eur J Clin Nutr. 2020"
        ]
    ),

    # =========================================================================
    # OMEGA-3 (EPA/DHA)
    # =========================================================================
    "omega3": Nutrient(
        name="Omega-3 (EPA/DHA)",
        category=NutrientCategory.FATTY_ACID,

        description="""
EPA (eikosapentaensyra) och DHA (dokosahexaensyra) är långa omega-3-fettsyror
som är essentiella för hjärna, hjärta och inflammation. Kroppen kan INTE
effektivt omvandla växtbaserad ALA (linfrö, chia) till EPA/DHA - omvandlingen
är endast 5-15% för EPA och <5% för DHA. Personer med FADS1/FADS2-varianter
har ännu sämre omvandling.
        """.strip(),

        primary_functions=[
            "Hjärnfunktion (60% av hjärnans fett är DHA)",
            "Antiinflammatorisk effekt (konkurrerar med omega-6)",
            "Hjärt-kärlhälsa (triglyceridsänkning, blodtryck)",
            "Ögonhälsa (DHA i näthinnan)",
            "Cellmembranfluiditet",
            "Neurotransmission och mental hälsa",
            "Fosterutveckling (hjärna och ögon)"
        ],

        doses=[
            DoseInfo(PopulationGroup.ADULT_MALE, rdi=250, optimal_low=1000, optimal_high=3000, ul=5000, unit="mg EPA+DHA"),
            DoseInfo(PopulationGroup.ADULT_FEMALE, rdi=250, optimal_low=1000, optimal_high=3000, ul=5000, unit="mg EPA+DHA"),
            DoseInfo(PopulationGroup.PREGNANT, rdi=300, optimal_low=1000, optimal_high=3000, ul=5000, unit="mg EPA+DHA"),
        ],

        therapeutic_range="""
PREVENTIV DOS: 500-1000 mg EPA+DHA/dag
KARDIOVASKULÄR: 1000-2000 mg EPA+DHA/dag
TRIGLYCERIDSÄNKNING: 2000-4000 mg EPA+DHA/dag (medicinsk indikation)
DEPRESSION/ÅNGEST: 1000-2000 mg EPA (EPA>DHA ratio)
INFLAMMATION: 2000-3000 mg EPA+DHA/dag

OMEGA-3 INDEX (erytrocytmembran):
- <4%: Hög risk (associerad med hjärt-kärlsjukdom)
- 4-8%: Intermediär
- >8%: Optimal (skyddande, japansk/koreansk population)
        """.strip(),

        ld50_info="""
LD50: Ej fastställt - extremt säkert.
PRAKTISK ÖVRE GRÄNS: 5000 mg/dag utan medicinsk övervakning.
HÖGA DOSER (>3000 mg): Kan påverka blodkoagulation, relevant vid blodförtunnande.
EFSA BEDÖMNING: Upp till 5g/dag EPA+DHA är säkert för vuxna.
FDA GRAS: Up till 3g/dag från tillskott + kost.
        """.strip(),

        deficiency_symptoms=[
            "Torr, fjällande hud",
            "Torrt, sprött hår",
            "Mjuka/spröda naglar",
            "Trötthet och koncentrationssvårigheter",
            "Depression och humörsvängningar",
            "Ledvärk och stelhet",
            "Försämrat minne",
            "Försämrad syn (särskilt mörkerseende)"
        ],

        deficiency_diseases=[
            "Ökad kardiovaskulär risk",
            "Kognitiv nedgång",
            "Depression",
            "Torr ögonsjukdom",
            "Ökad inflammatorisk börda"
        ],

        deficiency_risk_factors=[
            "Vegansk/vegetarisk kost utan algbaserat tillskott",
            "Lågt fiskintag (<2 portioner/vecka)",
            "FADS1/FADS2-genvarianter (reducerad omvandling)",
            "Hög omega-6-konsumtion (konkurrerar om samma enzymer)",
            "Malabsorption (celiaki, Crohn, pankreasinsufficiens)"
        ],

        excess_symptoms=[
            "Fisksmaknande rapningar (vanligt men ofarligt)",
            "Mag-tarmbesvär (illamående, diarré)",
            "Ökad blödningstendens vid mycket höga doser",
            "Försämrad immunfunktion vid extrema doser (>10g/dag)"
        ],

        toxicity_threshold="Generellt säkert upp till 5000 mg/dag. >3000 mg/dag vid blodförtunnande = diskutera med läkare.",

        food_sources=[
            "Vild lax: 1500-2000 mg/100g",
            "Makrill: 1500-1800 mg/100g",
            "Sardiner: 1400 mg/100g",
            "Sill/Strömming: 1200-1700 mg/100g",
            "Ansjovis: 1400 mg/100g",
            "Odlad lax: 1000-1500 mg/100g",
            "Tonfisk (färsk): 300-1000 mg/100g",
            "Alger (vissa arter): varierande"
        ],

        supplement_forms=[
            "Triglyceridform (TG) - naturlig form, bäst absorption",
            "Etylesterform (EE) - koncentrerad men sämre absorption",
            "Fosfolipidform (krillolja) - god biotillgänglighet",
            "Algolja (vegansk) - DHA-dominant"
        ],

        best_form="Triglyceridform (rTG/TG) från molekylärdestillerad fiskolja eller algolja för veganer. EPA:DHA ratio beror på mål.",

        absorption_tips=[
            "Ta med fetrik måltid (ökar absorption 3x)",
            "Triglyceridform absorberas bättre än etylester",
            "Dela upp dosen om >2000 mg (t.ex. morgon + kväll)",
            "Förvara mörkt och svalt (undvik oxidation)"
        ],

        genetic_modifiers=[
            GeneticModifier(
                gene="FADS1",
                rsid="rs174546",
                risk_genotype="TT",
                effect="Kraftigt reducerad ALA→EPA→DHA-omvandling",
                dose_adjustment="MÅSTE få EPA/DHA direkt från fisk/alg. ALA (linfrö) räcker inte."
            ),
            GeneticModifier(
                gene="FADS2",
                rsid="rs1535",
                risk_genotype="GG",
                effect="Reducerad delta-6-desaturas (första steget)",
                dose_adjustment="Dubbel riskallel med FADS1 = starkt behov av marin omega-3."
            ),
        ],

        drug_interactions=[
            DrugInteraction(
                drug_class="Blodförtunnande",
                examples=["Warfarin", "Eliquis", "Xarelto", "Aspirin"],
                interaction="Omega-3 har mild blodförtunnande effekt",
                recommendation=">3000 mg/dag: Diskutera med läkare. Kan behöva INR-justering vid warfarin."
            ),
            DrugInteraction(
                drug_class="Blodtrycksmedicin",
                examples=["ACE-hämmare", "Betablockerare"],
                interaction="Additiv blodtryckssänkande effekt",
                recommendation="Positiv interaktion, men monitorera blodtryck"
            ),
            DrugInteraction(
                drug_class="Statiner",
                examples=["Atorvastatin", "Simvastatin"],
                interaction="Additiv lipidsänkande effekt",
                recommendation="Synergistisk effekt - ofta kombineras kliniskt"
            ),
        ],

        nutrient_interactions=[
            "VITAMIN E - skyddar omega-3 från oxidation, ta gärna tillsammans",
            "OMEGA-6 - konkurrerar om samma enzymer, håll ratio nere (mål: 1:1-4:1)",
            "ASTAXANTIN - potent antioxidant som skyddar omega-3",
            "VITAMIN D - synergistisk effekt för inflammation"
        ],

        best_time="Med måltid (frukost eller middag). Dela dos om >2000 mg.",
        with_food=True,

        references=[
            "Harris WS. The omega-3 index as a risk factor for coronary heart disease. Am J Clin Nutr. 2008",
            "Calder PC. Omega-3 fatty acids and inflammatory processes. Nutrients. 2010",
            "Mozaffarian D. Fish intake, contaminants, and human health. JAMA. 2006",
            "Schuchardt JP. Bioavailability of omega-3 fatty acids. Prostaglandins Leukot Essent Fatty Acids. 2011"
        ]
    ),

    # =========================================================================
    # MAGNESIUM
    # =========================================================================
    "magnesium": Nutrient(
        name="Magnesium",
        category=NutrientCategory.MINERAL_MACRO,

        description="""
Magnesium är kofaktor i >600 enzymatiska reaktioner. Kritiskt för energiproduktion
(ATP), proteinsyntes, muskel- och nervfunktion, blodtrycksreglering och
blodsockerkontroll. Även nödvändigt för D-vitaminaktivering.
Brist är MYCKET vanligt (uppskattningsvis 50-80% får inte RDI).
        """.strip(),

        primary_functions=[
            "Energiproduktion (ATP kräver Mg för aktivitet)",
            "Muskelavslappning (motverkar kalciums kontraktion)",
            "Nervfunktion och neurotransmission",
            "Blodtrycksreglering",
            "Blodsockerkontroll och insulinkänslighet",
            "DNA/RNA-syntes",
            "Proteinsyntes",
            "D-vitaminaktivering",
            "COMT-enzymfunktion (katekolaminnedbrytning)"
        ],

        doses=[
            DoseInfo(PopulationGroup.ADULT_MALE, rdi=350, optimal_low=400, optimal_high=600, ul=350, unit="mg (tillskott)"),
            DoseInfo(PopulationGroup.ADULT_FEMALE, rdi=280, optimal_low=300, optimal_high=500, ul=350, unit="mg (tillskott)"),
            DoseInfo(PopulationGroup.PREGNANT, rdi=360, optimal_low=400, optimal_high=500, ul=350, unit="mg (tillskott)"),
            DoseInfo(PopulationGroup.ELDERLY, rdi=350, optimal_low=400, optimal_high=600, ul=350, unit="mg (tillskott)"),
        ],

        therapeutic_range="""
OBS: UL gäller endast TILLSKOTT, inte magnesium från mat.

BLODVÄRDEN (serum-Mg):
- Normal: 0.75-1.0 mmol/L
- Suboptimal: 0.75-0.85 mmol/L (funktionell brist möjlig)
- Brist: <0.75 mmol/L
OBS: Serum-Mg är dålig markör - endast 1% finns i blodet!

DOSERING:
- Underhåll: 200-400 mg/dag
- Stress/träning: 400-600 mg/dag
- Kramper/sömn: 300-500 mg på kvällen
- Migrän (profylax): 400-600 mg/dag
        """.strip(),

        ld50_info="""
LD50 (oral, råtta): ~8000 mg/kg
HUMAN TOXICITET: Mycket ovanligt vid oral tillförsel hos friska.
NJURFUNKTION: Vid nedsatt njurfunktion kan Mg ackumuleras.
ÖVERDOS: Extremt sällsynt oralt - lösning är att sluta ta tillskott.
INTRAVENÖS: Kan vara farligt vid snabb infusion (hjärtstillestånd).
        """.strip(),

        deficiency_symptoms=[
            "Muskelkramper och ryckningar",
            "Sömnsvårigheter",
            "Ångest och nervositet",
            "Trötthet och svaghet",
            "Huvudvärk och migrän",
            "Förstoppning",
            "Hjärtklappning/arytmier",
            "Domningar och stickningar"
        ],

        deficiency_diseases=[
            "Hjärtarytmier",
            "Hypertension",
            "Diabetes typ 2 (insulinresistens)",
            "Osteoporos",
            "Migrän",
            "Depression"
        ],

        deficiency_risk_factors=[
            "Stress (ökar Mg-utsöndring)",
            "Hög alkoholkonsumtion",
            "Diabetes (ökad urinförlust)",
            "Mag-tarmsjukdomar",
            "Äldre ålder (sämre absorption)",
            "PPI-användning (magmedicin)",
            "Diuretika",
            "Intensiv träning (förlust via svett)",
            "Processad kost (lågt Mg-innehåll)"
        ],

        excess_symptoms=[
            "Diarré (vanligast - kroppens sätt att bli av med överskott)",
            "Illamående",
            "Buksmärta",
            "Vid extrem överdos/njursvikt: lågt blodtryck, andningssvårigheter"
        ],

        toxicity_threshold="Diarré uppstår vanligen vid >500-800 mg tillskott på en gång. Dela dos.",

        food_sources=[
            "Pumpafrön: 550 mg/100g",
            "Mandel: 270 mg/100g",
            "Mörk choklad (>70%): 230 mg/100g",
            "Cashewnötter: 260 mg/100g",
            "Spenat (kokt): 87 mg/100g",
            "Svarta bönor: 70 mg/100g",
            "Avokado: 29 mg/100g",
            "Banan: 27 mg/100g"
        ],

        supplement_forms=[
            "Magnesiumglycinat - hög biotillgänglighet, lugnande, milt för magen",
            "Magnesiumtreonat - korsar blod-hjärnbarriären, för kognition",
            "Magnesiumtaurat - för hjärt-kärlhälsa",
            "Magnesiumcitrat - god absorption, lätt laxerande",
            "Magnesiummalat - för energi och muskler",
            "Magnesiumoxid - billig men dålig absorption (4%)",
            "Magnesiumklorid - topikalt eller oralt"
        ],

        best_form="Glycinat för allmänt bruk och sömn. Treonat för kognition. Citrat om billigare behövs.",

        absorption_tips=[
            "Dela upp dosen (max 200-300 mg åt gången)",
            "Ta på kvällen för sömnstöd",
            "Undvik att ta med zink (konkurrerar)",
            "Undvik att ta med fytater/oxalater (spinat)",
            "B6 förbättrar cellupptag"
        ],

        genetic_modifiers=[
            GeneticModifier(
                gene="COMT",
                rsid="rs4680",
                risk_genotype="AA (Met/Met)",
                effect="Långsam COMT kräver mer magnesium som kofaktor",
                dose_adjustment="Met/Met-bärare har extra nytta av Mg för stresshantering (300-500 mg/dag)"
            ),
            GeneticModifier(
                gene="TRPM6",
                rsid="rs11144134",
                risk_genotype="TT",
                effect="Reducerad magnesiumabsorption i tarmen",
                dose_adjustment="Kan behöva högre dos eller bättre form (glycinat)"
            ),
        ],

        drug_interactions=[
            DrugInteraction(
                drug_class="Antibiotika (fluorokinoloner)",
                examples=["Ciprofloxacin", "Levofloxacin"],
                interaction="Magnesium minskar antibiotikaabsorption",
                recommendation="Ta Mg 2 timmar före eller 6 timmar efter"
            ),
            DrugInteraction(
                drug_class="Bisfosfonater",
                examples=["Alendronat", "Risedronat"],
                interaction="Magnesium minskar bisfosfonatabsorption",
                recommendation="Ta Mg minst 2 timmar efter bisfosfonat"
            ),
            DrugInteraction(
                drug_class="PPI (protonpumpshämmare)",
                examples=["Omeprazol", "Esomeprazol"],
                interaction="Långvarig PPI minskar Mg-absorption",
                recommendation="Överväg Mg-tillskott vid långvarig PPI-behandling"
            ),
            DrugInteraction(
                drug_class="Diuretika (loop/tiazid)",
                examples=["Furosemid", "Hydroklortiazid"],
                interaction="Ökar Mg-förlust via urin",
                recommendation="Mg-tillskott rekommenderas vid långvarig diuretikabehandling"
            ),
        ],

        nutrient_interactions=[
            "KALCIUM - balansera Mg:Ca (1:1 eller 1:2 ratio)",
            "D-VITAMIN - Mg krävs för D-vitaminaktivering",
            "B6 - förbättrar Mg:s cellupptag",
            "ZINK - konkurrerar om absorption (ta olika tider)",
            "KALIUM - Mg-brist kan orsaka kaliumförlust"
        ],

        best_time="Kväll, 1-2 timmar före sömn. Vid stress: dela morgon + kväll.",
        with_food=False,  # Kan tas med eller utan mat

        references=[
            "Rosanoff A. Magnesium supplements may enhance the effects of antihypertensive medications. J Clin Hypertens. 2011",
            "DiNicolantonio JJ. Subclinical magnesium deficiency: a principal driver of cardiovascular disease. Open Heart. 2018",
            "Razzaque MS. Magnesium: Are We Consuming Enough? Nutrients. 2018",
            "Workinger JL. Challenges in the Diagnosis of Magnesium Status. Nutrients. 2018"
        ]
    ),

    # =========================================================================
    # VITAMIN A (RETINOL)
    # =========================================================================
    "vitamin_a": Nutrient(
        name="Vitamin A (Retinol)",
        category=NutrientCategory.VITAMIN_FAT_SOLUBLE,

        description="""
Vitamin A finns i två former: retinol (preformerad, från djur) och karotenoider
som betakaroten (provitamin, från växter). BCMO1-genvarianter reducerar
omvandlingen av betakaroten till retinol med 30-70%, vilket innebär att
dessa personer MÅSTE få preformerat retinol från animaliska källor eller tillskott.
        """.strip(),

        primary_functions=[
            "Syn (särskilt mörkerseende, rodopsinproduktion)",
            "Immunförsvar (slemhinnebarriär)",
            "Celldelning och differentiering",
            "Reproduktiv hälsa",
            "Hudhälsa och epitelintegritet",
            "Genuttryck (retinoida receptorer)",
            "Embryonal utveckling"
        ],

        doses=[
            DoseInfo(PopulationGroup.ADULT_MALE, rdi=900, optimal_low=900, optimal_high=3000, ul=3000, unit="mcg RAE"),
            DoseInfo(PopulationGroup.ADULT_FEMALE, rdi=700, optimal_low=700, optimal_high=3000, ul=3000, unit="mcg RAE"),
            DoseInfo(PopulationGroup.PREGNANT, rdi=770, optimal_low=770, optimal_high=3000, ul=3000, unit="mcg RAE"),
        ],

        therapeutic_range="""
ENHETER:
- 1 mcg RAE (Retinol Activity Equivalent) = 1 mcg retinol
- 1 mcg RAE = 12 mcg betakaroten (med full omvandling)
- 1 IE = 0.3 mcg retinol

BLODVÄRDEN (serum-retinol):
- Brist: <0.70 µmol/L (20 µg/dL)
- Marginal: 0.70-1.05 µmol/L
- Normal: >1.05 µmol/L
- Toxisk: >3.5 µmol/L vid kroniskt högt intag

BCMO1-BÄRARE (rs7501331 CT/TT):
- Behöver preformerad retinol, inte betakaroten
- Dos: 2500-5000 IE retinol/dag (750-1500 mcg)
        """.strip(),

        ld50_info="""
AKUT TOXICITET: >300,000 IE (90,000 mcg) som engångsdos.
KRONISK TOXICITET: >25,000 IE/dag (7500 mcg) under månader/år.
GRAVIDITET: >10,000 IE/dag associerat med fosterskador - MAX 3000 mcg.
BETAKAROTEN: Ej toxiskt (lagras som orange pigment i huden = karotenemi).

VARNING: Polar explorers dog av att äta isbjörnslever (300,000-900,000 IE/portion).
        """.strip(),

        deficiency_symptoms=[
            "Nattblindhet (tidig symptom)",
            "Torr, fjällande hud",
            "Torra ögon (xeroftalmi)",
            "Försämrat immunförsvar",
            "Dålig sårläkning",
            "Akne och hudproblem",
            "Ökad infektionskänslighet",
            "Bitot-fläckar (ögonvitor)"
        ],

        deficiency_diseases=[
            "Xeroftalmi (torr ögonsjukdom)",
            "Keratomalaci (hornhinneuppmjukning)",
            "Blindhet (i utvecklingsländer)",
            "Ökad infektionsdödlighet hos barn"
        ],

        deficiency_risk_factors=[
            "Vegansk/vegetarisk kost + BCMO1-variant",
            "Fettmalabsorption (celiaki, Crohn, pankreas)",
            "Leversjukdom",
            "Zinkbrist (krävs för A-vitaminmobilisering)",
            "Alkoholism",
            "BCMO1 rs7501331 T-allel (32-69% reducerad omvandling)"
        ],

        excess_symptoms=[
            "Huvudvärk (förhöjt intrakraniellt tryck)",
            "Illamående och kräkningar",
            "Synförändringar",
            "Hudförändringar (torr, fjällning)",
            "Håravfall",
            "Skelett/muskelvärk",
            "Leverskada (vid kronisk toxicitet)",
            "Fosterskador (teratogent)"
        ],

        toxicity_threshold="Akut: >300,000 IE. Kronisk: >25,000 IE/dag. Graviditet: undvik >10,000 IE/dag.",

        food_sources=[
            "Lever (nöt): 9000 mcg/100g (EXTREMT HÖG)",
            "Lever (kyckling): 3300 mcg/100g",
            "Leverpastej: 2000-8000 mcg/100g",
            "Äggula: 140 mcg/ägg",
            "Smör: 680 mcg/100g",
            "Ost (cheddar): 265 mcg/100g",
            "Fet fisk (ål): 1000 mcg/100g",
            "Mjölk (hel): 28 mcg/100mL"
        ],

        supplement_forms=[
            "Retinylpalmitat - stabil, vanligast i tillskott",
            "Retinylacetat - välabsorberad",
            "Retinol - ren form, mindre stabil",
            "Betakaroten - säkrare men kräver omvandling"
        ],

        best_form="Retinylpalmitat i låg dos (2500-5000 IE) för BCMO1-bärare. Betakaroten för icke-bärare.",

        absorption_tips=[
            "Ta med fetrik måltid (fettlöslig)",
            "Zink behövs för transport och användning",
            "Undvik mega-doser (toxiskt)",
            "Lever 1-2 ggr/månad ger god A-vitaminstatus"
        ],

        genetic_modifiers=[
            GeneticModifier(
                gene="BCMO1",
                rsid="rs7501331",
                risk_genotype="CT (32%) / TT (69%)",
                effect="Reducerad omvandling av betakaroten till retinol",
                dose_adjustment="CT: 32% reducering - inkludera retinolkällor. TT: 69% reducering - MÅSTE ha retinol."
            ),
            GeneticModifier(
                gene="BCMO1",
                rsid="rs12934922",
                risk_genotype="TT",
                effect="Additiv effekt med rs7501331",
                dose_adjustment="Om bärare av båda: nästan ingen betakaroten-omvandling."
            ),
        ],

        drug_interactions=[
            DrugInteraction(
                drug_class="Retinoider (akne)",
                examples=["Isotretinoin (Roaccutan)", "Tretinoin"],
                interaction="Additiv toxicitetsrisk",
                recommendation="UNDVIK A-vitamintillskott vid retinoidbehandling"
            ),
            DrugInteraction(
                drug_class="Blodförtunnande",
                examples=["Warfarin"],
                interaction="Höga doser A-vitamin kan förstärka warfarineffekt",
                recommendation="Undvik >3000 mcg/dag vid warfarinbehandling"
            ),
            DrugInteraction(
                drug_class="Orlistat",
                examples=["Xenical", "Alli"],
                interaction="Minskar absorption av fettlösliga vitaminer",
                recommendation="Ta A-vitamin vid annan tidpunkt"
            ),
        ],

        nutrient_interactions=[
            "ZINK - krävs för A-vitaminmobilisering från lever",
            "D-VITAMIN - höga doser A kan motverka D-vitamin",
            "E-VITAMIN - skyddar A-vitamin från oxidation",
            "FETT - krävs för absorption"
        ],

        best_time="Med fetrik måltid. Undvik tom mage.",
        with_food=True,

        references=[
            "Tang G. Bioconversion of dietary provitamin A carotenoids to vitamin A. Am J Clin Nutr. 2010",
            "Lietz G. BCMO1 common variants and beta-carotene conversion. FASEB J. 2012",
            "Ross AC. Vitamin A and retinoic acid in T cell-related immunity. Am J Clin Nutr. 2012"
        ]
    ),

    # =========================================================================
    # L-TEANIN
    # =========================================================================
    "l_theanine": Nutrient(
        name="L-Teanin",
        category=NutrientCategory.AMINO_ACID,

        description="""
L-teanin är en aminosyra som finns nästan uteslutande i te (Camellia sinensis).
Den korsar blod-hjärnbarriären och ökar alfa-hjärnvågor (associerade med
avslappnad vakenhet). Ger lugn utan dåsighet - perfekt för stresskänsliga
COMT Met/Met-bärare.
        """.strip(),

        primary_functions=[
            "Ökar alfa-hjärnvågor (avslappnad fokus)",
            "Modulerar GABA, serotonin, dopamin",
            "Reducerar stressrespons (kortisol)",
            "Förbättrar sömn utan sedering",
            "Förbättrar fokus kombinerat med koffein",
            "Skyddar neuroner (neuroprotektion)"
        ],

        doses=[
            DoseInfo(PopulationGroup.ADULT_MALE, rdi=0, optimal_low=100, optimal_high=400, ul=1200, unit="mg"),
            DoseInfo(PopulationGroup.ADULT_FEMALE, rdi=0, optimal_low=100, optimal_high=400, ul=1200, unit="mg"),
        ],

        therapeutic_range="""
INGEN RDI (inte essentiellt, men fördelaktigt).

DOSERING:
- Lugn fokus: 100-200 mg
- Stressreduktion: 200-400 mg
- Sömn: 200-400 mg 30-60 min före sänggående
- Med koffein (stack): 100-200 mg L-teanin + 50-100 mg koffein

COMT Met/Met-bärare: 200-400 mg/dag kan hjälpa mot koffeinångest och stress.
        """.strip(),

        ld50_info="""
LD50: Extremt hög - ingen toxicitet rapporterad vid rimliga doser.
GRAS-STATUS: Generally Recognized As Safe av FDA upp till 250 mg/portion.
STUDIER: Upp till 900 mg/dag i veckor utan biverkningar.
SÄKERHETSMARGINAL: Mycket bred - svårt att överdosera.
        """.strip(),

        deficiency_symptoms=[
            "Ej essentiellt - inga bristsymptom"
        ],

        deficiency_diseases=[
            "Ej relevant - supplementeras för specifika fördelar"
        ],

        deficiency_risk_factors=[
            "Ej relevant"
        ],

        excess_symptoms=[
            "Huvudvärk (sällsynt vid höga doser)",
            "Mag-tarmbesvär (sällsynt)",
            "Dåsighet vid mycket höga doser"
        ],

        toxicity_threshold="Ingen etablerad övre gräns. Generellt säkert upp till 1200 mg/dag.",

        food_sources=[
            "Grönt te: 25-60 mg/kopp",
            "Svart te: 10-30 mg/kopp",
            "Vitt te: 20-40 mg/kopp",
            "Matcha: 30-50 mg/portion"
        ],

        supplement_forms=[
            "L-teanin (Suntheanine är välstuderat varumärke)",
            "Kapslar/tabletter",
            "Pulver"
        ],

        best_form="Suntheanine (patenterad form) eller annan ren L-teanin. Undvik D-teanin.",

        absorption_tips=[
            "Absorberas bra med eller utan mat",
            "Kombinera med koffein för synergistisk fokus utan jitter",
            "Effekt inom 30-60 minuter"
        ],

        genetic_modifiers=[
            GeneticModifier(
                gene="COMT",
                rsid="rs4680",
                risk_genotype="AA (Met/Met)",
                effect="Långsam katekolaminnedbrytning - stresskänslig",
                dose_adjustment="200-400 mg L-teanin kan hjälpa med stresshantering och koffeinbiverkningar"
            ),
        ],

        drug_interactions=[
            DrugInteraction(
                drug_class="Blodtrycksmedicin",
                examples=["ACE-hämmare", "Betablockerare"],
                interaction="Additiv blodtryckssänkning (mild)",
                recommendation="Generellt säkert, men monitorera om känslig"
            ),
            DrugInteraction(
                drug_class="Stimulantia",
                examples=["Metylfenidat", "Amfetamin"],
                interaction="Kan mildra biverkningar som ångest",
                recommendation="Ofta positiv kombination, diskutera med läkare"
            ),
        ],

        nutrient_interactions=[
            "KOFFEIN - synergistisk kombination för fokus utan jitter",
            "MAGNESIUM - båda stödjer avslappning, kompletterande"
        ],

        best_time="Vid behov: stress, fokus, eller 30-60 min före sömn.",
        with_food=False,

        references=[
            "Nobre AC. L-theanine, a natural constituent in tea, and its effect on mental state. Asia Pac J Clin Nutr. 2008",
            "Owen GN. The combined effects of L-theanine and caffeine on cognitive performance. Nutr Neurosci. 2008",
            "Kimura K. L-Theanine reduces psychological and physiological stress responses. Biol Psychol. 2007"
        ]
    ),
}

# =============================================================================
# HJÄLPFUNKTIONER
# =============================================================================

def get_nutrient(name: str) -> Optional[Nutrient]:
    """Hämta ett näringsämne"""
    return NUTRIENT_DATABASE.get(name.lower().replace("-", "_").replace(" ", "_"))

def get_dose_for_population(nutrient: Nutrient, population: PopulationGroup) -> Optional[DoseInfo]:
    """Hämta dos för specifik population"""
    for dose in nutrient.doses:
        if dose.population == population:
            return dose
    return None

def get_genetic_adjustment(nutrient: Nutrient, rsid: str, genotype: str) -> Optional[str]:
    """Kolla om en genotyp kräver dosjustering"""
    for mod in nutrient.genetic_modifiers:
        if mod.rsid == rsid and genotype in mod.risk_genotype:
            return mod.dose_adjustment
    return None

def format_nutrient_info(nutrient: Nutrient, genotype_info: Dict[str, str] = None) -> str:
    """Formatera komplett info om ett näringsämne"""
    lines = []
    lines.append(f"# {nutrient.name}")
    lines.append(f"\n{nutrient.description}")

    # Funktioner
    lines.append("\n## Primära funktioner")
    for func in nutrient.primary_functions:
        lines.append(f"- {func}")

    # Dosering
    lines.append("\n## Dosering")
    lines.append("| Population | RDI | Optimal | UL | Enhet |")
    lines.append("|------------|-----|---------|----|----|")
    for dose in nutrient.doses:
        lines.append(f"| {dose.population.value} | {dose.rdi} | {dose.optimal_low}-{dose.optimal_high} | {dose.ul} | {dose.unit} |")

    lines.append(f"\n### Terapeutiskt intervall\n{nutrient.therapeutic_range}")

    # Genetiska justeringar
    if genotype_info:
        lines.append("\n## Din genetiska justering")
        for mod in nutrient.genetic_modifiers:
            if mod.rsid in genotype_info:
                gt = genotype_info[mod.rsid]
                if gt in mod.risk_genotype or any(g in gt for g in mod.risk_genotype.split("/")):
                    lines.append(f"**{mod.gene} ({mod.rsid}): {gt}**")
                    lines.append(f"- Effekt: {mod.effect}")
                    lines.append(f"- Dosjustering: {mod.dose_adjustment}")

    # Toxicitet
    lines.append(f"\n## Toxicitet & säkerhet\n{nutrient.ld50_info}")

    # Bristsymptom
    lines.append("\n## Bristsymptom")
    for sym in nutrient.deficiency_symptoms:
        lines.append(f"- {sym}")

    # Källor
    lines.append("\n## Bästa källor")
    for src in nutrient.food_sources:
        lines.append(f"- {src}")

    lines.append(f"\n### Bästa tillskottsform\n{nutrient.best_form}")

    # Interaktioner
    if nutrient.drug_interactions:
        lines.append("\n## Läkemedelsinteraktioner")
        for inter in nutrient.drug_interactions:
            lines.append(f"### {inter.drug_class}")
            lines.append(f"- Läkemedel: {', '.join(inter.examples)}")
            lines.append(f"- Interaktion: {inter.interaction}")
            lines.append(f"- Rekommendation: {inter.recommendation}")

    lines.append(f"\n## Bästa tid att ta\n{nutrient.best_time}")

    return "\n".join(lines)


if __name__ == "__main__":
    print("GWL Nutrient Database")
    print("=" * 50)
    print(f"Näringsämnen i databasen: {len(NUTRIENT_DATABASE)}")
    print()
    for name, nutrient in NUTRIENT_DATABASE.items():
        print(f"- {nutrient.name}")
        doses = nutrient.doses[0] if nutrient.doses else None
        if doses:
            print(f"  RDI: {doses.rdi} {doses.unit}")
            print(f"  Optimal: {doses.optimal_low}-{doses.optimal_high} {doses.unit}")
            print(f"  UL: {doses.ul} {doses.unit}")
        print()
