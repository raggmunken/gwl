"""
GWL Biological Pathways Database
================================
Biologiska pathways med involverade gener och näringsämnen.
Inkluderar metylering, detoxifiering, inflammation, antioxidant och neurotransmittorer.

Genetic Wellness Labs - Nutrigenomics Platform
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

# =============================================================================
# ENUMS
# =============================================================================

class PathwayCategory(Enum):
    METHYLATION = "Metylering"
    DETOXIFICATION_PHASE1 = "Detoxifiering Fas I"
    DETOXIFICATION_PHASE2 = "Detoxifiering Fas II"
    ANTIOXIDANT = "Antioxidantförsvar"
    INFLAMMATION = "Inflammation"
    NEUROTRANSMITTER = "Neurotransmittorer"
    LIPID_METABOLISM = "Lipidmetabolism"
    HORMONE = "Hormonmetabolism"
    MITOCHONDRIAL = "Mitokondriefunktion"
    CIRCADIAN = "Dygnsrytm"

class PathwayStatus(Enum):
    OPTIMAL = "Optimal funktion"
    SUBOPTIMAL = "Suboptimal funktion"
    IMPAIRED = "Nedsatt funktion"
    SEVERELY_IMPAIRED = "Kraftigt nedsatt funktion"

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class PathwayGene:
    """Gen som ingår i en pathway"""
    gene: str
    rsids: List[str]
    role: str
    effect_of_variants: str
    key_cofactors: List[str]

@dataclass
class PathwayNutrient:
    """Näringsämne som stödjer en pathway"""
    nutrient: str
    role: str
    dose_range: str
    timing: str
    notes: str

@dataclass
class PathwayMetabolite:
    """Metabolit som kan mätas för att bedöma pathway-funktion"""
    name: str
    optimal_range: str
    high_indicates: str
    low_indicates: str
    test_type: str

@dataclass
class BiologicalPathway:
    """Komplett beskrivning av en biologisk pathway"""
    name: str
    category: PathwayCategory
    description: str
    key_functions: List[str]
    genes: List[PathwayGene]
    supporting_nutrients: List[PathwayNutrient]
    inhibitors: List[str]
    metabolites: List[PathwayMetabolite]
    upstream_pathways: List[str]
    downstream_pathways: List[str]
    clinical_relevance: List[str]
    references: List[str]

# =============================================================================
# METHYLATION CYCLE
# =============================================================================

METHYLATION_CYCLE = BiologicalPathway(
    name="Metyleringscykeln",
    category=PathwayCategory.METHYLATION,
    description="Central one-carbon metabolism som reglerar DNA-metylering, "
                "neurotransmittorsyntes, histonmodifiering och över 200 enzymatiska reaktioner.",
    key_functions=[
        "DNA-metylering och genreglering",
        "Neurotransmittorsyntes (dopamin, serotonin, noradrenalin)",
        "Myelinsyntes och nervhälsa",
        "Kreatinsyntes för energi",
        "Karnitinsyntes för fettsyremetabolism",
        "Fosfatidylkolinsyntes för cellmembran",
        "Homocysteinreglering"
    ],
    genes=[
        PathwayGene(
            gene="MTHFR",
            rsids=["rs1801133", "rs1801131"],
            role="Omvandlar 5,10-metylenTHF till 5-metylTHF (aktiv folat)",
            effect_of_variants="677TT: ~30% aktivitet, förhöjt homocystein",
            key_cofactors=["Riboflavin (B2)"]
        ),
        PathwayGene(
            gene="MTR",
            rsids=["rs1805087"],
            role="Metioninsyntetas - överför metyl från folat till homocystein",
            effect_of_variants="AG/GG: Reducerad aktivitet, B12-beroende",
            key_cofactors=["B12 (metylkobalamin)", "5-MTHF"]
        ),
        PathwayGene(
            gene="MTRR",
            rsids=["rs1801394"],
            role="Regenererar MTR-enzymet genom B12-reduktion",
            effect_of_variants="AG/GG: Långsammare MTR-regenerering",
            key_cofactors=["B12", "SAMe"]
        ),
        PathwayGene(
            gene="BHMT",
            rsids=["rs3733890"],
            role="Alternativ metylering via betain (trimethylglycin)",
            effect_of_variants="Varianter påverkar betain-pathway",
            key_cofactors=["Betain (TMG)", "Zink"]
        ),
        PathwayGene(
            gene="MAT1A",
            rsids=["rs10498817"],
            role="Syntetiserar SAMe från metionin",
            effect_of_variants="Varianter påverkar SAMe-produktion",
            key_cofactors=["ATP", "Magnesium"]
        ),
        PathwayGene(
            gene="COMT",
            rsids=["rs4680"],
            role="Förbrukar SAMe vid nedbrytning av katekolaminer",
            effect_of_variants="Met/Met: Låg aktivitet, SAMe ackumuleras",
            key_cofactors=["SAMe", "Magnesium"]
        ),
        PathwayGene(
            gene="CBS",
            rsids=["rs234706"],
            role="Transsulfureringsvägen - homocystein till cystein",
            effect_of_variants="Varianter påverkar glutationsyntes",
            key_cofactors=["B6 (P5P)", "Serin"]
        ),
        PathwayGene(
            gene="AHCY",
            rsids=["rs819147"],
            role="Hydrolyserar SAH till homocystein",
            effect_of_variants="Varianter påverkar metyleringscykelhastighet",
            key_cofactors=["Zink"]
        )
    ],
    supporting_nutrients=[
        PathwayNutrient(
            nutrient="Metylfolat (5-MTHF)",
            role="Primär metyldonator via MTHFR-vägen",
            dose_range="400-1000 mcg/dag (upp till 15mg vid MTHFR-mutation)",
            timing="Morgon med mat",
            notes="Startdos låg vid COMT Met/Met för att undvika övermetylering"
        ),
        PathwayNutrient(
            nutrient="Metylkobalamin (B12)",
            role="Kofaktor för MTR, metylöverföring",
            dose_range="1000-5000 mcg/dag",
            timing="Morgon, sublingualt",
            notes="Adenosylkobalamin för mitokondriestöd"
        ),
        PathwayNutrient(
            nutrient="P5P (Pyridoxal-5-fosfat)",
            role="Aktiv B6 för CBS och transaminaser",
            dose_range="25-100 mg/dag",
            timing="Med måltid",
            notes="Undvik höga doser vid perifer neuropati"
        ),
        PathwayNutrient(
            nutrient="Riboflavin (B2)",
            role="Kofaktor för MTHFR",
            dose_range="25-100 mg/dag",
            timing="Med mat",
            notes="Stabiliserar MTHFR 677TT-enzymet"
        ),
        PathwayNutrient(
            nutrient="Betain (TMG)",
            role="Alternativ metyldonator via BHMT",
            dose_range="500-3000 mg/dag",
            timing="Med måltid",
            notes="Användbart vid MTHFR-mutation"
        ),
        PathwayNutrient(
            nutrient="Magnesium",
            role="Kofaktor för MAT och COMT",
            dose_range="200-400 mg/dag",
            timing="Kväll",
            notes="Glycinat eller treonat för bäst absorption"
        ),
        PathwayNutrient(
            nutrient="Zink",
            role="Kofaktor för BHMT och AHCY",
            dose_range="15-30 mg/dag",
            timing="Med mat, ej med järn",
            notes="Balansera med koppar 1:10-15"
        )
    ],
    inhibitors=[
        "Folsyra (syntetisk) - blockerar folatreceptorer hos MTHFR-mutanter",
        "Aluminium - hämmar flera metylerande enzymer",
        "Arsenikexponering",
        "Alkohol - utarmar B-vitaminer",
        "Protonpumpshämmare - minskar B12-absorption",
        "Metformin - minskar B12-absorption",
        "Lustgas (N2O) - inaktiverar B12",
        "Höga doser niacin - förbrukar metylgrupper",
        "Bisfenol A (BPA) - stör DNA-metylering"
    ],
    metabolites=[
        PathwayMetabolite(
            name="Homocystein",
            optimal_range="5-8 umol/L",
            high_indicates="MTHFR-mutation, B12/folat-brist, CBS-nedreglering",
            low_indicates="CBS-uppreglering, övermetylering",
            test_type="Blodprov (serum)"
        ),
        PathwayMetabolite(
            name="SAMe/SAH-kvot",
            optimal_range=">4:1",
            high_indicates="God metyleringskapacitet",
            low_indicates="Metyleringsstress",
            test_type="Specialanalys"
        ),
        PathwayMetabolite(
            name="Methylmalonsyra (MMA)",
            optimal_range="<270 nmol/L",
            high_indicates="Funktionell B12-brist",
            low_indicates="Adekvat B12",
            test_type="Urin eller blod"
        ),
        PathwayMetabolite(
            name="Folat (RBC)",
            optimal_range=">400 ng/mL",
            high_indicates="God folatstatus",
            low_indicates="Folatbrist eller MTHFR-problem",
            test_type="Blodprov"
        )
    ],
    upstream_pathways=["Folatcykeln", "B12-metabolism"],
    downstream_pathways=[
        "Transsulfureringsvägen (glutationsyntes)",
        "Kreatinsyntes",
        "Neurotransmittorsyntes",
        "DNA-metylering",
        "Fosfolipidsyntes"
    ],
    clinical_relevance=[
        "Kardiovaskulär sjukdom (homocystein)",
        "Depression och ångest (neurotransmittorer)",
        "Neurologiska sjukdomar",
        "Cancer (DNA-metylering)",
        "Autoimmunitet",
        "Fertilitetsproblem",
        "Graviditetskomplikationer (neuralrörsdefekter)"
    ],
    references=[
        "PMID: 24935961 - Methylation pathway overview",
        "PMID: 28125025 - MTHFR and homocysteine",
        "PMID: 24825598 - Methylfolate clinical use",
        "PMID: 22158061 - SAMe metabolism"
    ]
)

# =============================================================================
# TRANSSULFURATION PATHWAY
# =============================================================================

TRANSSULFURATION_PATHWAY = BiologicalPathway(
    name="Transsulfureringsvägen",
    category=PathwayCategory.METHYLATION,
    description="Konverterar homocystein till cystein och vidare till glutation. "
                "Kritisk för antioxidantförsvar och avgiftning.",
    key_functions=[
        "Cystein- och glutationsyntes",
        "Homocysteinreglering",
        "Taurinproduktion",
        "Sulfatproduktion för fas II-detox",
        "Vätesulfidproduktion (gasotransmittor)"
    ],
    genes=[
        PathwayGene(
            gene="CBS",
            rsids=["rs234706", "rs1801181"],
            role="Cystationin-beta-syntas - första steget i transsulfurering",
            effect_of_variants="Uppreglering: snabb homocysteinförbrukning, ammoniak-ackumulering",
            key_cofactors=["B6 (P5P)", "Serin", "Hem"]
        ),
        PathwayGene(
            gene="CTH",
            rsids=["rs1021737"],
            role="Cystationas - klyver cystationin till cystein",
            effect_of_variants="Varianter påverkar cysteinproduktion",
            key_cofactors=["B6 (P5P)"]
        ),
        PathwayGene(
            gene="GCLC",
            rsids=["rs17883901"],
            role="Gamma-glutamylcystein-syntas - hastighetsbegränsande för glutation",
            effect_of_variants="Varianter påverkar glutationproduktion",
            key_cofactors=["ATP", "Cystein", "Glutamat"]
        ),
        PathwayGene(
            gene="GCLM",
            rsids=["rs41303970"],
            role="Modulatorisk subenhet för GCLC",
            effect_of_variants="Varianter påverkar glutationkapacitet",
            key_cofactors=["Glycin"]
        ),
        PathwayGene(
            gene="GSS",
            rsids=["rs2273684"],
            role="Glutationsyntas - slutsteget i glutationsyntes",
            effect_of_variants="Varianter påverkar glutationproduktion",
            key_cofactors=["ATP", "Glycin"]
        )
    ],
    supporting_nutrients=[
        PathwayNutrient(
            nutrient="NAC (N-acetylcystein)",
            role="Cysteinprekursor för glutation",
            dose_range="600-1800 mg/dag",
            timing="Mellan måltider",
            notes="Kan öka kopparutsöndring vid långvarig användning"
        ),
        PathwayNutrient(
            nutrient="Glycin",
            role="Glutationprekursor",
            dose_range="3-5 g/dag",
            timing="Kväll (sömnstöd)",
            notes="Kollagenpulver är bra källa"
        ),
        PathwayNutrient(
            nutrient="Glutamin",
            role="Glutamatprekursor för glutation",
            dose_range="5-10 g/dag",
            timing="Mellan måltider",
            notes="Försiktighet vid histaminintolerans"
        ),
        PathwayNutrient(
            nutrient="Selen",
            role="Kofaktor för glutationperoxidaser",
            dose_range="100-200 mcg/dag",
            timing="Med mat",
            notes="Selenometionin är fördelaktigt"
        ),
        PathwayNutrient(
            nutrient="P5P (B6)",
            role="Kofaktor för CBS och CTH",
            dose_range="25-50 mg/dag",
            timing="Med mat",
            notes="Kritiskt för hela transsulfureringsvägen"
        ),
        PathwayNutrient(
            nutrient="Alpha-liponsyra",
            role="Regenererar glutation, tungmetallkelering",
            dose_range="300-600 mg/dag",
            timing="Tom mage",
            notes="R-alfa-liponsyra är mest bioaktiv"
        ),
        PathwayNutrient(
            nutrient="Taurin",
            role="Slutprodukt och antioxidant",
            dose_range="500-2000 mg/dag",
            timing="Mellan måltider",
            notes="Viktig för gallsyrakonjugering"
        )
    ],
    inhibitors=[
        "Paracetamol (förbrukar glutation)",
        "Alkohol",
        "Tungmetaller (kvicksilver, bly, arsenik)",
        "Oxidativ stress",
        "Proteinbrist (aminosyrabrist)"
    ],
    metabolites=[
        PathwayMetabolite(
            name="Glutation (GSH/GSSG-kvot)",
            optimal_range="GSH/GSSG > 100:1",
            high_indicates="God antioxidantkapacitet",
            low_indicates="Oxidativ stress, utarmning",
            test_type="Blodprov (speciallab)"
        ),
        PathwayMetabolite(
            name="Cystein",
            optimal_range="250-375 umol/L",
            high_indicates="God CBS-funktion eller NAC-tillskott",
            low_indicates="CBS-hämning eller glutationdränering",
            test_type="Plasma-aminosyraprofil"
        ),
        PathwayMetabolite(
            name="Taurin",
            optimal_range="45-130 umol/L",
            high_indicates="God transsulfurering",
            low_indicates="CBS/CTH-problem, B6-brist",
            test_type="Plasma-aminosyraprofil"
        ),
        PathwayMetabolite(
            name="Sulfat (urin)",
            optimal_range="Individuellt",
            high_indicates="Aktiv CBS-väg",
            low_indicates="Transsulfureringsproblem",
            test_type="Organiska syror (urin)"
        )
    ],
    upstream_pathways=["Metyleringscykeln"],
    downstream_pathways=[
        "Glutationkonjugering (fas II)",
        "Sulfatkonjugering (fas II)",
        "Taurinmetabolism",
        "Vätesulfidproduktion"
    ],
    clinical_relevance=[
        "Oxidativ stress-relaterade sjukdomar",
        "Kemisk känslighet",
        "Kronisk inflammation",
        "Leverhälsa och detox",
        "Neurologiska sjukdomar (Parkinson, Alzheimer)",
        "Autismspektrumstörningar"
    ],
    references=[
        "PMID: 23747864 - Transsulfuration pathway",
        "PMID: 22020109 - CBS polymorphisms",
        "PMID: 24488579 - Glutathione in health and disease",
        "PMID: 17190852 - NAC clinical applications"
    ]
)

# =============================================================================
# PHASE I DETOXIFICATION (CYP450)
# =============================================================================

PHASE1_DETOX = BiologicalPathway(
    name="Fas I Detoxifiering (Cytokrom P450)",
    category=PathwayCategory.DETOXIFICATION_PHASE1,
    description="Cytokrom P450-enzymer som oxiderar, reducerar och hydrolyserar xenobiotika "
                "och endogena substrat för vidare konjugering i fas II.",
    key_functions=[
        "Oxidation av läkemedel och toxiner",
        "Hydroxylering av steroider",
        "Epoxidation av PAH (polycykliska aromatiska kolväten)",
        "N-dealkylering och O-dealkylering",
        "Aktivering av prokarcninogener"
    ],
    genes=[
        PathwayGene(
            gene="CYP1A1",
            rsids=["rs1048943", "rs4646903"],
            role="Metaboliserar PAH, östrogen, koffein",
            effect_of_variants="Ökad aktivitet: ökad karcinogenaktivering",
            key_cofactors=["Hem", "NADPH", "O2"]
        ),
        PathwayGene(
            gene="CYP1A2",
            rsids=["rs762551", "rs2069514"],
            role="Koffein, östrogen, aromatiska aminer",
            effect_of_variants="AA: Snabb metabolism, CC: Långsam",
            key_cofactors=["Hem", "Riboflavin"]
        ),
        PathwayGene(
            gene="CYP1B1",
            rsids=["rs1056836"],
            role="Östrogen hydroxylering till 4-OH-E2 (genotoxisk)",
            effect_of_variants="Varianter ökar 4-OH-östrogen",
            key_cofactors=["Hem"]
        ),
        PathwayGene(
            gene="CYP2C9",
            rsids=["rs1799853", "rs1057910"],
            role="Warfarin, NSAID, losartan",
            effect_of_variants="*2/*3: Kraftigt reducerad aktivitet",
            key_cofactors=["Hem"]
        ),
        PathwayGene(
            gene="CYP2C19",
            rsids=["rs4244285", "rs12248560"],
            role="PPI, clopidogrel, antidepressiva",
            effect_of_variants="*2: Null, *17: Ökad aktivitet",
            key_cofactors=["Hem"]
        ),
        PathwayGene(
            gene="CYP2D6",
            rsids=["rs3892097", "rs16947", "rs1065852"],
            role="~25% av alla läkemedel, kodein, tamoxifen",
            effect_of_variants="*4: Null, xN: Ultra-snabb",
            key_cofactors=["Hem"]
        ),
        PathwayGene(
            gene="CYP2E1",
            rsids=["rs2031920", "rs6413432"],
            role="Etanol, paracetamol, bensen",
            effect_of_variants="Induceras av alkohol, producerar ROS",
            key_cofactors=["Hem"]
        ),
        PathwayGene(
            gene="CYP3A4",
            rsids=["rs2740574", "rs35599367"],
            role="~50% av alla läkemedel, steroider",
            effect_of_variants="Varianter påverkar läkemedelsmetabolism",
            key_cofactors=["Hem"]
        )
    ],
    supporting_nutrients=[
        PathwayNutrient(
            nutrient="B-vitaminkomplex",
            role="Kofaktorer för CYP450-funktioner",
            dose_range="Aktiva former, 1-2x/dag",
            timing="Morgon",
            notes="Riboflavin särskilt viktigt"
        ),
        PathwayNutrient(
            nutrient="Järn",
            role="Hem-syntes för CYP450",
            dose_range="Endast vid brist",
            timing="Tom mage med C-vitamin",
            notes="Överskott ökar oxidativ stress"
        ),
        PathwayNutrient(
            nutrient="Magnesium",
            role="Kofaktor för många reaktioner",
            dose_range="200-400 mg/dag",
            timing="Kväll",
            notes="Kritiskt vid hög toxinbelastning"
        ),
        PathwayNutrient(
            nutrient="Indol-3-karbinol / DIM",
            role="Modulerar CYP1-enzymer, ökar 2-OH-östrogen",
            dose_range="DIM 100-200 mg/dag",
            timing="Med måltid",
            notes="Korsblommiga grönsaker är naturlig källa"
        ),
        PathwayNutrient(
            nutrient="Quercetin",
            role="Hämmar CYP3A4 och CYP1A2",
            dose_range="500-1000 mg/dag",
            timing="Mellan måltider",
            notes="Kan öka läkemedelskoncentrationer"
        )
    ],
    inhibitors=[
        "Grapefrukt (CYP3A4-hämmare)",
        "Johannesört (CYP3A4-inducerare)",
        "Tungmetaller",
        "Organiska lösningsmedel",
        "Höga doser kuramin (CYP3A4-inducerare)"
    ],
    metabolites=[
        PathwayMetabolite(
            name="4-OH-östrogen / 2-OH-östrogen kvot",
            optimal_range="<1.0 (2-OH ska dominera)",
            high_indicates="CYP1B1-dominans, ökad cancerrisk",
            low_indicates="Balanserad östrogennedbrytning",
            test_type="Östrogenmetabolit-test (urin)"
        ),
        PathwayMetabolite(
            name="D-glukaric acid",
            optimal_range="Individuellt",
            high_indicates="Ökad fas I-aktivitet",
            low_indicates="Låg fas I-aktivitet",
            test_type="Organiska syror (urin)"
        )
    ],
    upstream_pathways=["Näringsupptag", "Hem-syntes"],
    downstream_pathways=["Fas II Detoxifiering"],
    clinical_relevance=[
        "Läkemedelsinteraktioner",
        "Kemisk känslighet",
        "Hormonberoende cancer",
        "Alkoholmetabolism",
        "Paracetamoltoxicitet"
    ],
    references=[
        "PMID: 26465333 - CYP450 pharmacogenomics",
        "PMID: 17192767 - Detoxification pathways",
        "PMID: 23295013 - CYP1B1 and estrogen",
        "PMID: 16825041 - DIM and estrogen metabolism"
    ]
)

# =============================================================================
# PHASE II DETOXIFICATION (CONJUGATION)
# =============================================================================

PHASE2_DETOX = BiologicalPathway(
    name="Fas II Detoxifiering (Konjugering)",
    category=PathwayCategory.DETOXIFICATION_PHASE2,
    description="Konjugeringsreaktioner som gör fas I-metaboliter vattenlösliga för utsöndring. "
                "Inkluderar glutation-, glukuronid-, sulfat-, acetat- och aminosyrakonjugering.",
    key_functions=[
        "Glutationkonjugering (tungmetaller, elektrofiler)",
        "Glukuronidering (hormoner, billirubin, läkemedel)",
        "Sulfatkonjugering (steroider, neurotransmittorer)",
        "Acetylering (aromatiska aminer, hydraziner)",
        "Aminosyrakonjugering (bensoesyra, gallsyror)",
        "Metylering av toxiner"
    ],
    genes=[
        PathwayGene(
            gene="GSTM1",
            rsids=["Deletion"],
            role="Glutationtransferas mu - elektrofila toxiner",
            effect_of_variants="Null genotyp (50% av kaukasier): ingen aktivitet",
            key_cofactors=["Glutation"]
        ),
        PathwayGene(
            gene="GSTT1",
            rsids=["Deletion"],
            role="Glutationtransferas theta - halogenerade föreningar",
            effect_of_variants="Null genotyp (20%): ingen aktivitet",
            key_cofactors=["Glutation"]
        ),
        PathwayGene(
            gene="GSTP1",
            rsids=["rs1695", "rs1138272"],
            role="Glutationtransferas pi - främst i lungor",
            effect_of_variants="Ile105Val: Reducerad aktivitet för vissa substrat",
            key_cofactors=["Glutation"]
        ),
        PathwayGene(
            gene="UGT1A1",
            rsids=["rs8175347"],
            role="Glukuronidering av bilirubin",
            effect_of_variants="*28 (7 TA repeats): Gilberts syndrom, långsam konjugering",
            key_cofactors=["UDP-glukuronsyra"]
        ),
        PathwayGene(
            gene="SULT1A1",
            rsids=["rs9282861"],
            role="Sulfatkonjugering av fenoliska föreningar",
            effect_of_variants="*2: Reducerad aktivitet, termolabilt enzym",
            key_cofactors=["PAPS (sulfatdonator)"]
        ),
        PathwayGene(
            gene="NAT2",
            rsids=["rs1801280", "rs1799930", "rs1799931"],
            role="N-acetyltransferas - aromatiska aminer, isoniazid",
            effect_of_variants="Långsam/snabb acetylator-fenotyp",
            key_cofactors=["Acetyl-CoA"]
        ),
        PathwayGene(
            gene="NQO1",
            rsids=["rs1800566"],
            role="Quinon-reduktas - skyddar mot kinoner",
            effect_of_variants="*2: Protein degraderas, ökad kinontoxicitet",
            key_cofactors=["FAD", "NADH"]
        ),
        PathwayGene(
            gene="PON1",
            rsids=["rs662", "rs854560"],
            role="Paraoxonas - hydrolyserar organofosfater, oxiderade lipider",
            effect_of_variants="Varianter påverkar pesticidkänslighet",
            key_cofactors=["Kalcium"]
        )
    ],
    supporting_nutrients=[
        PathwayNutrient(
            nutrient="NAC / Glutation",
            role="Substrat för glutationkonjugering",
            dose_range="NAC 600-1800 mg eller liposomalt GSH 250-500 mg",
            timing="Mellan måltider",
            notes="Kritiskt vid GSTM1/GSTT1 null"
        ),
        PathwayNutrient(
            nutrient="Glycin",
            role="Aminosyrakonjugering",
            dose_range="3-5 g/dag",
            timing="Kväll",
            notes="Vanligt bristämne vid hög toxinbelastning"
        ),
        PathwayNutrient(
            nutrient="Taurin",
            role="Gallsyrakonjugering",
            dose_range="500-2000 mg/dag",
            timing="Mellan måltider",
            notes="Stödjer även fas I"
        ),
        PathwayNutrient(
            nutrient="Kalcium-D-glukarat",
            role="Stödjer glukuronidering, hämmar beta-glukuronidas",
            dose_range="500-1500 mg/dag",
            timing="Med mat",
            notes="Finns i citrusfrukter, korsblommiga"
        ),
        PathwayNutrient(
            nutrient="Sulfat (MSM/sulforafan)",
            role="Sulfatdonator för SULT-enzymer",
            dose_range="MSM 1000-3000 mg eller sulforafan 10-50 mg",
            timing="Med mat",
            notes="Korsblommiga grönsaker är bästa källa"
        ),
        PathwayNutrient(
            nutrient="Molybden",
            role="Kofaktor för sulfitoxidas",
            dose_range="75-250 mcg/dag",
            timing="Med mat",
            notes="Viktigt vid sulfitintolerans"
        ),
        PathwayNutrient(
            nutrient="B-vitaminkomplex",
            role="Acetylering och metylering",
            dose_range="Aktiva former 1-2x/dag",
            timing="Morgon",
            notes="B5 särskilt för Acetyl-CoA"
        )
    ],
    inhibitors=[
        "Beta-glukuronidas (tarmbakterier) - reverserar glukuronidering",
        "Aspirin (hämmar glukuronidering)",
        "Paracetamol (uttömmer glutation)",
        "Låg proteinkost (aminosyrabrist)",
        "Sulfitexponering (överbelastar SULT)"
    ],
    metabolites=[
        PathwayMetabolite(
            name="Merkaptursyror (urin)",
            optimal_range="Individuellt",
            high_indicates="Aktiv glutationkonjugering",
            low_indicates="GST-brist eller glutationbrist",
            test_type="Organiska syror"
        ),
        PathwayMetabolite(
            name="Bilirubin (okonjugerat)",
            optimal_range="<17 umol/L",
            high_indicates="UGT1A1-mutation (Gilberts)",
            low_indicates="Normal glukuronidering",
            test_type="Leverprover"
        ),
        PathwayMetabolite(
            name="Sulfat/kreatinin-kvot",
            optimal_range="Individuellt",
            high_indicates="Aktiv sulfatkonjugering",
            low_indicates="Sulfatbrist",
            test_type="Urinanalys"
        )
    ],
    upstream_pathways=["Fas I Detoxifiering", "Glutationsyntes"],
    downstream_pathways=["Biliär utsöndring", "Renal utsöndring"],
    clinical_relevance=[
        "Kemisk känslighet (MCS)",
        "Läkemedelsbiverkningar",
        "Gilberts syndrom",
        "Cancerkänslighet (GSTM1/GSTT1 null)",
        "Pesticidintolerens",
        "Histaminintolerens"
    ],
    references=[
        "PMID: 17192767 - Phase II detoxification",
        "PMID: 17408518 - GST polymorphisms and disease",
        "PMID: 19189288 - UGT1A1 Gilbert syndrome",
        "PMID: 23147091 - NAT2 acetylator status"
    ]
)

# =============================================================================
# INFLAMMATION PATHWAY
# =============================================================================

INFLAMMATION_PATHWAY = BiologicalPathway(
    name="Inflammationsreglering",
    category=PathwayCategory.INFLAMMATION,
    description="Balans mellan pro-inflammatoriska och anti-inflammatoriska signaler. "
                "Inkluderar eikosanoid-syntes, cytokiner och NF-kB-signalering.",
    key_functions=[
        "Prostaglandin- och leukotriensyntes",
        "Cytokinproduktion (IL-1, IL-6, TNF-alfa)",
        "NF-kB-signalering",
        "Resolviner och protektiner (resolution)",
        "Histaminfrisättning"
    ],
    genes=[
        PathwayGene(
            gene="IL6",
            rsids=["rs1800795"],
            role="Interleukin-6 - central pro-inflammatorisk cytokin",
            effect_of_variants="GG: Lägre IL-6, CC: Högre IL-6",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="TNF",
            rsids=["rs1800629"],
            role="Tumornekrosfaktor alfa - akut inflammation",
            effect_of_variants="AA/AG: Ökad TNF-produktion",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="IL1B",
            rsids=["rs16944", "rs1143634"],
            role="Interleukin-1 beta - pyrogen och inflammatorisk",
            effect_of_variants="Varianter påverkar IL-1 nivåer",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="CRP",
            rsids=["rs1205", "rs3093077"],
            role="C-reaktivt protein - inflammationsmarkör",
            effect_of_variants="Varianter påverkar basala CRP-nivåer",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="COX2 (PTGS2)",
            rsids=["rs20417", "rs5275"],
            role="Prostaglandinsyntas 2 - inducerbar, inflammation",
            effect_of_variants="Varianter påverkar COX-2-expression",
            key_cofactors=["Arakidonsyra", "Hem"]
        ),
        PathwayGene(
            gene="FADS1/FADS2",
            rsids=["rs174546", "rs174547", "rs1535"],
            role="Fettsyradesaturaser - omega-6/3 konvertering",
            effect_of_variants="Varianter påverkar AA/EPA-produktion",
            key_cofactors=["Zink", "Magnesium", "B-vitaminer"]
        ),
        PathwayGene(
            gene="ALOX5",
            rsids=["rs2115819"],
            role="5-lipoxygenas - leukotriensynteas",
            effect_of_variants="Varianter påverkar leukotrienproduktion",
            key_cofactors=["Järn", "Kalcium"]
        )
    ],
    supporting_nutrients=[
        PathwayNutrient(
            nutrient="Omega-3 (EPA/DHA)",
            role="Anti-inflammatoriska eikosanoider, resolviner",
            dose_range="2-4 g EPA+DHA/dag vid inflammation",
            timing="Med måltid",
            notes="Hög EPA:DHA kvot (2:1) för inflammation"
        ),
        PathwayNutrient(
            nutrient="Kurkumin",
            role="Hämmar NF-kB, COX-2, 5-LOX",
            dose_range="500-2000 mg/dag (biooptimerad form)",
            timing="Med fett",
            notes="Piperin eller liposomal form ökar absorption 20x"
        ),
        PathwayNutrient(
            nutrient="SPM (Specialized Pro-resolving Mediators)",
            role="Aktiv resolution av inflammation",
            dose_range="1-2 g SPM-aktiva oljor",
            timing="Med mat",
            notes="Från fiskolja eller direkt SPM-tillskott"
        ),
        PathwayNutrient(
            nutrient="Vitamin D3",
            role="Immunmodulerande, minskar IL-6",
            dose_range="2000-5000 IE/dag (nivåbaserat)",
            timing="Med fettrik måltid",
            notes="Mål: 75-125 nmol/L"
        ),
        PathwayNutrient(
            nutrient="Zink",
            role="Hämmar NF-kB, stödjer immunfunktion",
            dose_range="15-30 mg/dag",
            timing="Med mat",
            notes="Balansera med koppar"
        ),
        PathwayNutrient(
            nutrient="Quercetin",
            role="Mastcellstabilisator, antihistamin, NF-kB-hämmare",
            dose_range="500-1000 mg/dag",
            timing="Mellan måltider",
            notes="Synergistiskt med bromelain"
        ),
        PathwayNutrient(
            nutrient="Boswellia (AKBA)",
            role="5-LOX-hämmare, minskar leukotriener",
            dose_range="300-500 mg/dag (standardiserad)",
            timing="Med mat",
            notes="Särskilt effektivt vid ledproblem"
        )
    ],
    inhibitors=[
        "Omega-6-överskott (arakidonsyra)",
        "Raffinerat socker (ökar IL-6)",
        "Transfetter",
        "Kronisk stress (kortisol -> IL-6)",
        "Sömnbrist",
        "Visceralt fett (producerar cytokiner)",
        "Tarmpermeabilitet (LPS läckage)"
    ],
    metabolites=[
        PathwayMetabolite(
            name="hs-CRP",
            optimal_range="<1.0 mg/L (optimalt <0.5)",
            high_indicates="Systemisk låggradig inflammation",
            low_indicates="Låg inflammatorisk belastning",
            test_type="Blodprov"
        ),
        PathwayMetabolite(
            name="AA/EPA-kvot",
            optimal_range="<3:1 (optimalt 1.5-2:1)",
            high_indicates="Pro-inflammatorisk fettsyraprofil",
            low_indicates="Anti-inflammatorisk profil",
            test_type="Fettsyraprofil (blod)"
        ),
        PathwayMetabolite(
            name="IL-6",
            optimal_range="<3 pg/mL",
            high_indicates="Aktiv inflammation",
            low_indicates="Kontrollerad inflammation",
            test_type="Cytokinpanel"
        ),
        PathwayMetabolite(
            name="Ferritin",
            optimal_range="30-150 ng/mL",
            high_indicates="Inflammation eller järnöverskott",
            low_indicates="Järnbrist",
            test_type="Blodprov"
        )
    ],
    upstream_pathways=["Fettsyrametabolism", "Tarmhälsa"],
    downstream_pathways=["Oxidativ stress", "Insulinresistens"],
    clinical_relevance=[
        "Hjärt-kärlsjukdom",
        "Autoimmuna sjukdomar",
        "Metabolt syndrom",
        "Depression",
        "Neurodegeneration",
        "Cancer"
    ],
    references=[
        "PMID: 26567432 - Inflammation and chronic disease",
        "PMID: 28900017 - Omega-3 and inflammation",
        "PMID: 28881837 - Curcumin mechanisms",
        "PMID: 24526425 - Resolution of inflammation"
    ]
)

# =============================================================================
# ANTIOXIDANT DEFENSE
# =============================================================================

ANTIOXIDANT_PATHWAY = BiologicalPathway(
    name="Antioxidantförsvar",
    category=PathwayCategory.ANTIOXIDANT,
    description="Enzymatiska och icke-enzymatiska system som neutraliserar reaktiva syreradikaler (ROS) "
                "och skyddar mot oxidativ stress.",
    key_functions=[
        "Superoxiddismutation (O2- -> H2O2)",
        "Katalas (H2O2 -> H2O + O2)",
        "Glutationperoxidas (lipidperoxider, H2O2)",
        "Tioredoxinsystemet",
        "NRF2-aktivering (antioxidant response element)"
    ],
    genes=[
        PathwayGene(
            gene="SOD2",
            rsids=["rs4880"],
            role="Mangan-superoxiddismuteras - mitokondriellt försvar",
            effect_of_variants="CC (Val/Val): Lägre aktivitet, ökad ROS",
            key_cofactors=["Mangan"]
        ),
        PathwayGene(
            gene="CAT",
            rsids=["rs1001179"],
            role="Katalas - nedbryter väteperoxid",
            effect_of_variants="TT: Reducerad katalasaktivitet",
            key_cofactors=["Järn (hem)"]
        ),
        PathwayGene(
            gene="GPX1",
            rsids=["rs1050450"],
            role="Glutationperoxidas 1 - cytoplasmatisk",
            effect_of_variants="TT (Pro/Pro): Lägre aktivitet",
            key_cofactors=["Selen"]
        ),
        PathwayGene(
            gene="NFE2L2 (NRF2)",
            rsids=["rs6721961", "rs35652124"],
            role="Master regulator för antioxidantgener",
            effect_of_variants="Varianter påverkar NRF2-aktivering",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="KEAP1",
            rsids=["rs1048290"],
            role="Negativ regulator av NRF2",
            effect_of_variants="Varianter påverkar NRF2-hämning",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="PRDX1",
            rsids=["rs2773250"],
            role="Peroxiredoxin 1 - tioredoxinsystemet",
            effect_of_variants="Varianter påverkar peroxid-reducering",
            key_cofactors=["Tioredoxin"]
        )
    ],
    supporting_nutrients=[
        PathwayNutrient(
            nutrient="Selen",
            role="Kofaktor för GPX, tioredoxinreduktas",
            dose_range="100-200 mcg/dag",
            timing="Med mat",
            notes="Selenometionin är bäst upptag"
        ),
        PathwayNutrient(
            nutrient="Zink",
            role="Kofaktor för SOD1 (cytoplasmatisk)",
            dose_range="15-30 mg/dag",
            timing="Med mat",
            notes="Cu-Zn SOD kräver koppar också"
        ),
        PathwayNutrient(
            nutrient="Koppar",
            role="Kofaktor för SOD1 och ceruloplasmin",
            dose_range="1-2 mg/dag",
            timing="Med mat, ej med zink",
            notes="Balansera Zn:Cu 10-15:1"
        ),
        PathwayNutrient(
            nutrient="Mangan",
            role="Kofaktor för SOD2 (mitokondriell)",
            dose_range="2-5 mg/dag",
            timing="Med mat",
            notes="Från fullkorn och nötter"
        ),
        PathwayNutrient(
            nutrient="Vitamin E (blandade tokotrienoler)",
            role="Fettlöslig antioxidant, skyddar membraner",
            dose_range="200-400 IE/dag",
            timing="Med fettrik måltid",
            notes="Gamma-tokotrienol mest potent"
        ),
        PathwayNutrient(
            nutrient="Vitamin C",
            role="Vattenlöslig antioxidant, regenererar E-vitamin",
            dose_range="500-2000 mg/dag (delad dos)",
            timing="Flera gånger dagligen",
            notes="Liposomalt ökar cellupptag"
        ),
        PathwayNutrient(
            nutrient="Alpha-liponsyra",
            role="Universal antioxidant, regenererar C & E",
            dose_range="300-600 mg/dag",
            timing="Tom mage",
            notes="R-ALA är biologiskt aktiv"
        ),
        PathwayNutrient(
            nutrient="Sulforafan",
            role="Potent NRF2-aktivator",
            dose_range="10-50 mg/dag (eller broccoligroddar)",
            timing="Med mat",
            notes="Myrosinas krävs för aktivering"
        ),
        PathwayNutrient(
            nutrient="Astaxantin",
            role="Kraftig singlet oxygen quencher",
            dose_range="4-12 mg/dag",
            timing="Med fett",
            notes="6000x starkare än C-vitamin"
        ),
        PathwayNutrient(
            nutrient="CoQ10 (ubiquinol)",
            role="Mitokondriell antioxidant, elektronbärare",
            dose_range="100-300 mg/dag",
            timing="Med fettrik måltid",
            notes="Ubiquinol är reducerad form"
        )
    ],
    inhibitors=[
        "Tungmetaller (kvicksilver, kadmium, bly)",
        "Bekämpningsmedel",
        "Alkohol (genererar ROS)",
        "Rökning",
        "UV-strålning",
        "Kronisk inflammation",
        "Mitokondriell dysfunktion",
        "Hyperglykemi"
    ],
    metabolites=[
        PathwayMetabolite(
            name="8-OHdG (8-hydroxydeoxyguanosin)",
            optimal_range="Lågt",
            high_indicates="DNA-oxidativ skada",
            low_indicates="Bra antioxidantskydd",
            test_type="Urin"
        ),
        PathwayMetabolite(
            name="F2-isoprostaner",
            optimal_range="Lågt",
            high_indicates="Lipidperoxidation",
            low_indicates="Skyddade membraner",
            test_type="Urin/plasma"
        ),
        PathwayMetabolite(
            name="TBARS/MDA",
            optimal_range="Lågt",
            high_indicates="Lipidperoxidation",
            low_indicates="God lipidstatus",
            test_type="Plasma"
        ),
        PathwayMetabolite(
            name="GSH/GSSG-kvot",
            optimal_range=">100:1",
            high_indicates="God redoxbalans",
            low_indicates="Oxidativ stress",
            test_type="Blod (speciallab)"
        )
    ],
    upstream_pathways=["Mitokondriefunktion", "Glutationsyntes"],
    downstream_pathways=["DNA-reparation", "Apoptos-reglering"],
    clinical_relevance=[
        "Åldrande",
        "Neurodegeneration",
        "Hjärt-kärlsjukdom",
        "Cancer",
        "Diabetes",
        "Katarakt och makuladegeneration"
    ],
    references=[
        "PMID: 28245145 - NRF2 and antioxidant defense",
        "PMID: 25514928 - SOD2 polymorphisms",
        "PMID: 24675093 - Selenium and GPX",
        "PMID: 27573378 - Sulforaphane and NRF2"
    ]
)

# =============================================================================
# NEUROTRANSMITTER PATHWAYS
# =============================================================================

NEUROTRANSMITTER_PATHWAY = BiologicalPathway(
    name="Neurotransmittorsyntes",
    category=PathwayCategory.NEUROTRANSMITTER,
    description="Syntes och nedbrytning av dopamin, serotonin, noradrenalin, GABA och acetylkolin.",
    key_functions=[
        "Dopaminsyntes (tyrosin -> L-DOPA -> dopamin)",
        "Serotoninsyntes (tryptofan -> 5-HTP -> serotonin)",
        "Noradrenalinsyntes (dopamin -> noradrenalin)",
        "GABA-syntes (glutamat -> GABA)",
        "Acetylkolinsyntes"
    ],
    genes=[
        PathwayGene(
            gene="TH",
            rsids=["rs10770141"],
            role="Tyrosinhydroxylas - hastighetsbegränsande för dopamin",
            effect_of_variants="Varianter påverkar dopaminsyntes",
            key_cofactors=["BH4", "Järn", "O2"]
        ),
        PathwayGene(
            gene="DDC (AADC)",
            rsids=["rs921451"],
            role="Aromatisk aminosyradekarboxylas - L-DOPA->dopamin, 5-HTP->serotonin",
            effect_of_variants="Varianter påverkar dekarboxylering",
            key_cofactors=["P5P (B6)"]
        ),
        PathwayGene(
            gene="DBH",
            rsids=["rs1611115", "rs1108580"],
            role="Dopamin-beta-hydroxylas - dopamin->noradrenalin",
            effect_of_variants="TT: Lägre DBH, högre dopamin/noradrenalin-kvot",
            key_cofactors=["Koppar", "Askorbinsyra"]
        ),
        PathwayGene(
            gene="TPH2",
            rsids=["rs4570625"],
            role="Tryptofanhydroxylas 2 - hastighetsbegränsande för serotonin i CNS",
            effect_of_variants="TT: Lägre serotoninsyntes",
            key_cofactors=["BH4", "Järn"]
        ),
        PathwayGene(
            gene="COMT",
            rsids=["rs4680"],
            role="Bryter ned dopamin, noradrenalin, östrogen",
            effect_of_variants="Met/Met: Långsam nedbrytning, högre prefrontal dopamin",
            key_cofactors=["SAMe", "Magnesium"]
        ),
        PathwayGene(
            gene="MAO-A",
            rsids=["rs6323"],
            role="Monoaminoxidas A - serotonin, noradrenalin, dopamin",
            effect_of_variants="T-allel: Högre aktivitet",
            key_cofactors=["FAD (riboflavin)"]
        ),
        PathwayGene(
            gene="MAO-B",
            rsids=["rs1799836"],
            role="Monoaminoxidas B - främst dopamin, fenylethylamin",
            effect_of_variants="Varianter påverkar dopaminnedbrytning",
            key_cofactors=["FAD"]
        ),
        PathwayGene(
            gene="GAD1",
            rsids=["rs3749034"],
            role="Glutamatdekarboxylas - glutamat->GABA",
            effect_of_variants="Varianter påverkar GABA-syntes",
            key_cofactors=["P5P (B6)"]
        ),
        PathwayGene(
            gene="SLC6A4 (SERT)",
            rsids=["rs25531", "5-HTTLPR"],
            role="Serotonintransportör - återupptag av serotonin",
            effect_of_variants="Korta allelen: Lägre SERT, högre synaptiskt serotonin",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="BDNF",
            rsids=["rs6265"],
            role="Brain-derived neurotrophic factor - neuroplasticitet",
            effect_of_variants="Met-bärare: Reducerad BDNF-sekretion",
            key_cofactors=[]
        )
    ],
    supporting_nutrients=[
        PathwayNutrient(
            nutrient="Tyrosin",
            role="Dopamin/noradrenalinprekursor",
            dose_range="500-2000 mg/dag",
            timing="Morgon, tom mage",
            notes="Undvik vid hypertyreos, melanom"
        ),
        PathwayNutrient(
            nutrient="5-HTP",
            role="Serotoninprekursor (kringgår TPH)",
            dose_range="50-200 mg/dag",
            timing="Kväll eller vid behov",
            notes="Kombinera ej med SSRI, ta med B6"
        ),
        PathwayNutrient(
            nutrient="Tryptofan",
            role="Serotoninprekursor (via TPH)",
            dose_range="500-2000 mg/dag",
            timing="Kväll med kolhydrater",
            notes="Konkurrerar med andra aminosyror"
        ),
        PathwayNutrient(
            nutrient="P5P (B6)",
            role="Kofaktor för DDC och GAD (dopamin, serotonin, GABA)",
            dose_range="25-50 mg/dag",
            timing="Med mat",
            notes="Undvik höga doser (>100mg) - neuropatirisk"
        ),
        PathwayNutrient(
            nutrient="BH4 eller folat/B12",
            role="Kofaktor för TH och TPH",
            dose_range="Metylfolat 400-1000 mcg + B12 1000 mcg",
            timing="Morgon",
            notes="BH4-tillskott vid behov (GCH1-mutation)"
        ),
        PathwayNutrient(
            nutrient="Magnesium",
            role="COMT-kofaktor, NMDA-receptormodulator",
            dose_range="200-400 mg/dag",
            timing="Kväll",
            notes="Treonat för CNS-penetration"
        ),
        PathwayNutrient(
            nutrient="Zink",
            role="Modulerar NMDA/GABA-receptorer",
            dose_range="15-30 mg/dag",
            timing="Med mat",
            notes="Lågt zink associerat med depression"
        ),
        PathwayNutrient(
            nutrient="Omega-3 (DHA)",
            role="Membranfluiditet, BDNF-expression",
            dose_range="1-2 g DHA/dag",
            timing="Med måltid",
            notes="DHA viktigare än EPA för hjärnan"
        ),
        PathwayNutrient(
            nutrient="Fosfolipiid-komplex (PS, PC)",
            role="Cellmembranfunktion, acetylkolin",
            dose_range="PS 100-300 mg, PC 500-1000 mg",
            timing="Med mat",
            notes="Äggula och lecithin är bra källor"
        ),
        PathwayNutrient(
            nutrient="GABA eller L-Theanin",
            role="Direkt GABA eller GABA-liknande effekt",
            dose_range="GABA 100-500 mg, L-theanin 100-200 mg",
            timing="Vid behov eller kväll",
            notes="L-theanin passerar BBB bättre"
        )
    ],
    inhibitors=[
        "Kronisk stress (kortisolhämmar BH4-syntes)",
        "Inflammation (kynureninvägen stjäl tryptofan)",
        "Proteinbrist (aminosyrabrist)",
        "Järnbrist (TH och TPH kräver järn)",
        "B-vitaminbrist",
        "Tungmetaller (kvicksilver, bly)",
        "Sömnbrist"
    ],
    metabolites=[
        PathwayMetabolite(
            name="Homovanillinsyra (HVA)",
            optimal_range="Individuellt",
            high_indicates="Hög dopaminomsättning",
            low_indicates="Låg dopaminsyntes/omsättning",
            test_type="Organiska syror (urin)"
        ),
        PathwayMetabolite(
            name="5-HIAA (5-hydroxiindolättiksyra)",
            optimal_range="Individuellt",
            high_indicates="Hög serotonin omsättning",
            low_indicates="Låg serotoninsyntes",
            test_type="Organiska syror (urin)"
        ),
        PathwayMetabolite(
            name="VMA (vanillylmandelsyra)",
            optimal_range="Individuellt",
            high_indicates="Hög noradrenalin/adrenalin omsättning",
            low_indicates="Låg katekolaminsyntes",
            test_type="Organiska syror (urin)"
        ),
        PathwayMetabolite(
            name="Kynurenin/tryptofan-kvot",
            optimal_range="Låg",
            high_indicates="Inflammationsdriven tryptofanbortledning",
            low_indicates="God serotoninpotential",
            test_type="Aminosyraprofil"
        )
    ],
    upstream_pathways=["Metyleringscykeln (BH4, SAMe)", "Aminosyratillgång"],
    downstream_pathways=["Signalering", "Sömn-vakenhet", "Stressrespons"],
    clinical_relevance=[
        "Depression",
        "Ångest",
        "ADHD",
        "Parkinson",
        "Schizofreni",
        "Sömnstörningar",
        "Fibromyalgi"
    ],
    references=[
        "PMID: 17008817 - COMT and cognition",
        "PMID: 18923578 - Serotonin pathway genetics",
        "PMID: 27067767 - BDNF and mental health",
        "PMID: 25773858 - Dopamine system genetics"
    ]
)

# =============================================================================
# BH4 CYCLE (Tetrahydrobiopterin)
# =============================================================================

BH4_PATHWAY = BiologicalPathway(
    name="Tetrahydrobiopterin (BH4)-cykeln",
    category=PathwayCategory.NEUROTRANSMITTER,
    description="BH4 är essentiell kofaktor för aminosyrahydroxylaser (neurotransmittorsyntes) "
                "och kväveoxidsyntetas. Regenereras via DHFR och DHPR.",
    key_functions=[
        "Kofaktor för TH (dopaminsyntes)",
        "Kofaktor för TPH (serotoninsyntes)",
        "Kofaktor för PAH (fenylalaninnedbrytning)",
        "Kofaktor för NOS (kväveoxidproduktion)",
        "Antioxidant"
    ],
    genes=[
        PathwayGene(
            gene="GCH1",
            rsids=["rs998259", "rs841"],
            role="GTP-cyklohydrolas 1 - hastighetsbegränsande för BH4-syntes",
            effect_of_variants="Varianter påverkar BH4-produktion, smärtkänslighet",
            key_cofactors=["GTP", "Zink"]
        ),
        PathwayGene(
            gene="SPR",
            rsids=["rs11248056"],
            role="Sepiapterinreduktas - BH4-syntes",
            effect_of_variants="Varianter kan orsaka dopa-responsiv dystoni",
            key_cofactors=["NADPH"]
        ),
        PathwayGene(
            gene="QDPR (DHPR)",
            rsids=["rs2237030"],
            role="Quinoid dihydropteridinreduktas - regenererar BH4 från BH2",
            effect_of_variants="Varianter påverkar BH4-regenerering",
            key_cofactors=["NADH"]
        ),
        PathwayGene(
            gene="PTS",
            rsids=["rs2070270"],
            role="6-pyruvoyltetrahydropterinsyntetas - BH4-syntes",
            effect_of_variants="Brist kan ge hyperfenylalaninemi",
            key_cofactors=[]
        )
    ],
    supporting_nutrients=[
        PathwayNutrient(
            nutrient="Metylfolat + B12",
            role="Stödjer DHFR (dihydrofolatreduktas som kan reducera BH2)",
            dose_range="Folat 400-1000 mcg, B12 1000 mcg",
            timing="Morgon",
            notes="Indirekt BH4-stöd"
        ),
        PathwayNutrient(
            nutrient="Vitamin C",
            role="Skyddar BH4 från oxidation",
            dose_range="500-1000 mg/dag",
            timing="Flera gånger dagligen",
            notes="Viktigt vid oxidativ stress"
        ),
        PathwayNutrient(
            nutrient="Zink",
            role="Kofaktor för GCH1",
            dose_range="15-30 mg/dag",
            timing="Med mat",
            notes="Essentiellt för BH4-syntes"
        ),
        PathwayNutrient(
            nutrient="Alfa-liponsyra",
            role="Skyddar BH4, regenererar antioxidanter",
            dose_range="300-600 mg/dag",
            timing="Tom mage",
            notes="R-ALA är mer bioaktiv"
        ),
        PathwayNutrient(
            nutrient="Sapropterin (BH4-tillskott)",
            role="Direkt BH4-ersättning",
            dose_range="Läkemedel - receptbelagt",
            timing="Med mat",
            notes="Används vid PKU och vissa GCH1-mutationer"
        )
    ],
    inhibitors=[
        "Oxidativ stress (oxiderar BH4 till BH2)",
        "Inflammation (förstör BH4)",
        "Peroxinitrit (från NO)",
        "Aluminium",
        "Högt fenylalanin"
    ],
    metabolites=[
        PathwayMetabolite(
            name="BH4/BH2-kvot",
            optimal_range="Hög (BH4 ska dominera)",
            high_indicates="Fungerande BH4-metabolism",
            low_indicates="Oxidativ stress, bristande regenerering",
            test_type="Specialanalys"
        ),
        PathwayMetabolite(
            name="Neopterin",
            optimal_range="Lågt-måttligt",
            high_indicates="Immunaktivering, BH4-förbrukning",
            low_indicates="Normal status",
            test_type="Urin/serum"
        ),
        PathwayMetabolite(
            name="Biopterin",
            optimal_range="Individuellt",
            high_indicates="BH4 oxiderat eller GCH1 uppreglerad",
            low_indicates="BH4-brist möjlig",
            test_type="Urin"
        )
    ],
    upstream_pathways=["GTP-metabolism", "Folatcykeln"],
    downstream_pathways=["Dopaminsyntes", "Serotoninsyntes", "Kväveoxidproduktion"],
    clinical_relevance=[
        "PKU (fenylketonuri)",
        "Atypisk hyperfenylalaninemi",
        "Dopa-responsiv dystoni",
        "Depression",
        "Parkinson",
        "Endoteldysfunktion",
        "Smärtkänslighet"
    ],
    references=[
        "PMID: 20196730 - BH4 and neurotransmitters",
        "PMID: 23543003 - GCH1 polymorphisms and pain",
        "PMID: 26190156 - BH4 deficiencies",
        "PMID: 24735095 - BH4 and vascular function"
    ]
)

# =============================================================================
# CIRCADIAN RHYTHM
# =============================================================================

CIRCADIAN_PATHWAY = BiologicalPathway(
    name="Dygnsrytm (Circadian rhythm)",
    category=PathwayCategory.CIRCADIAN,
    description="Biologisk klocka som reglerar sömn-vakenhet, hormonsekretion, metabolism "
                "och genexpression över 24-timmarscykel.",
    key_functions=[
        "Sömn-vakenhetscykel",
        "Melatonin- och kortisolrytm",
        "Kroppstemperaturreglering",
        "Celldelning och DNA-reparation",
        "Metabolisk reglering"
    ],
    genes=[
        PathwayGene(
            gene="CLOCK",
            rsids=["rs1801260", "rs3736544"],
            role="Central transkriptionsfaktor för circadian rytm",
            effect_of_variants="C-allel rs1801260: Kvällsmänniska, sämre sömnkvalitet",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="PER2",
            rsids=["rs2304672"],
            role="Period-protein - negativ feedback loop",
            effect_of_variants="Varianter associerade med sömnfasförskjutning",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="PER3",
            rsids=["rs57875989"],
            role="Period 3 - sömnbehov och kronotyp",
            effect_of_variants="5-repeat allel: Högre sömnbehov, morgonmänniska",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="CRY1",
            rsids=["rs2287161"],
            role="Cryptochrome 1 - ljuskänslig, negativ feedback",
            effect_of_variants="Varianter påverkar ljuskänslighet",
            key_cofactors=["FAD (blåljusabsorption)"]
        ),
        PathwayGene(
            gene="AANAT",
            rsids=["rs3760138"],
            role="Arylalkylamin-N-acetyltransferas - melatoninsyntes",
            effect_of_variants="Varianter påverkar melatoninproduktion",
            key_cofactors=["Acetyl-CoA", "Tryptofan"]
        ),
        PathwayGene(
            gene="ASMT",
            rsids=["rs4446909", "rs5989681"],
            role="Acetylserotonin-O-metyltransferas - slutsteg melatonin",
            effect_of_variants="Varianter associerade med lägre melatonin",
            key_cofactors=["SAMe"]
        ),
        PathwayGene(
            gene="MTNR1A",
            rsids=["rs2119882"],
            role="Melatoninreceptor 1A",
            effect_of_variants="Varianter påverkar melatoninkänslighet",
            key_cofactors=[]
        ),
        PathwayGene(
            gene="MTNR1B",
            rsids=["rs10830963"],
            role="Melatoninreceptor 1B - glukosmetabolism",
            effect_of_variants="G-allel: Ökad typ 2-diabetesrisk, försämrad glukostolerans",
            key_cofactors=[]
        )
    ],
    supporting_nutrients=[
        PathwayNutrient(
            nutrient="Melatonin",
            role="Direkt sömnhormon-supplementering",
            dose_range="0.5-5 mg vid sänggående",
            timing="30-60 min före sömn",
            notes="Lägre dos ofta effektivare, undvik vid autoimmunitet"
        ),
        PathwayNutrient(
            nutrient="Tryptofan",
            role="Melatoninprekursor",
            dose_range="500-1000 mg kväll",
            timing="1-2 timmar före sömn",
            notes="Ta med kolhydrater för bättre CNS-upptag"
        ),
        PathwayNutrient(
            nutrient="Magnesium",
            role="GABA-receptormodulator, muskelavslappning",
            dose_range="200-400 mg kväll",
            timing="1-2 timmar före sömn",
            notes="Glycinat eller treonat för avslappning"
        ),
        PathwayNutrient(
            nutrient="Glycin",
            role="Inhibitorisk neurotransmittor, sänker kroppstemperatur",
            dose_range="3 g före sömn",
            timing="30 min före sömn",
            notes="Förbättrar sömnkvalitet"
        ),
        PathwayNutrient(
            nutrient="Vitamin D3",
            role="Reglerar circadian gener, sovrum bör vara mörkt",
            dose_range="Morgon 2000-5000 IE",
            timing="Endast morgon (kan störa sömn kvällstid)",
            notes="Aldrig ta D-vitamin kvällstid"
        ),
        PathwayNutrient(
            nutrient="B6 (P5P)",
            role="Kofaktor för melatoninsyntes",
            dose_range="25-50 mg",
            timing="Kväll med tryptofan",
            notes="Kan öka drömaktivitet"
        ),
        PathwayNutrient(
            nutrient="L-theanin",
            role="Alfa-vågor, avslappning utan sedation",
            dose_range="100-200 mg",
            timing="Kväll vid behov",
            notes="Kan kombineras med melatonin"
        )
    ],
    inhibitors=[
        "Blått ljus på kvällen (skärmar, LED)",
        "Koffein (halveringstid 5-6 timmar)",
        "Alkohol (stör REM-sömn)",
        "Sen måltid (aktiverar metabolism)",
        "Oregelbundna sömntider",
        "Skiftarbete",
        "Jetlag"
    ],
    metabolites=[
        PathwayMetabolite(
            name="Melatonin (saliv kväll)",
            optimal_range="Hög kvällstid (>30 pg/mL)",
            high_indicates="God melatoninproduktion",
            low_indicates="AANAT/ASMT-problem, ljusexponering",
            test_type="Salivprov 22:00"
        ),
        PathwayMetabolite(
            name="6-sulfatoxymelatonin (morgonurin)",
            optimal_range="Individuellt",
            high_indicates="God melatoninproduktion natten",
            low_indicates="Låg melatoninsyntes",
            test_type="Morgonurin"
        ),
        PathwayMetabolite(
            name="Kortisol awakening response (CAR)",
            optimal_range="50-100% ökning inom 30 min efter uppvaknande",
            high_indicates="Normal HPA-axelrespons",
            low_indicates="HPA-dysfunktion, binjureutmattning",
            test_type="Salivkortisol (morgon x4)"
        )
    ],
    upstream_pathways=["Serotoninsyntes (för melatonin)", "HPA-axel"],
    downstream_pathways=["Metabolisk reglering", "Immunfunktion", "DNA-reparation"],
    clinical_relevance=[
        "Sömnlöshet",
        "Skiftarbetssyndrom",
        "Jetlag",
        "Säsongsbunden depression (SAD)",
        "Typ 2-diabetes (MTNR1B)",
        "Cancer (melatonins skyddande effekt)"
    ],
    references=[
        "PMID: 25349248 - Circadian clock genes",
        "PMID: 23680664 - Melatonin and sleep",
        "PMID: 22158061 - PER3 and sleep",
        "PMID: 27695767 - MTNR1B and diabetes"
    ]
)

# =============================================================================
# COMPLETE PATHWAY DATABASE
# =============================================================================

PATHWAY_DATABASE: Dict[str, BiologicalPathway] = {
    "methylation_cycle": METHYLATION_CYCLE,
    "transsulfuration": TRANSSULFURATION_PATHWAY,
    "phase1_detox": PHASE1_DETOX,
    "phase2_detox": PHASE2_DETOX,
    "inflammation": INFLAMMATION_PATHWAY,
    "antioxidant": ANTIOXIDANT_PATHWAY,
    "neurotransmitter": NEUROTRANSMITTER_PATHWAY,
    "bh4_cycle": BH4_PATHWAY,
    "circadian": CIRCADIAN_PATHWAY
}

# =============================================================================
# PATHWAY ANALYSIS FUNCTIONS
# =============================================================================

def get_pathway(pathway_id: str) -> Optional[BiologicalPathway]:
    """Hämta en specifik pathway."""
    return PATHWAY_DATABASE.get(pathway_id.lower())

def get_all_pathways() -> List[str]:
    """Lista alla tillgängliga pathways."""
    return list(PATHWAY_DATABASE.keys())

def get_pathways_by_category(category: PathwayCategory) -> List[BiologicalPathway]:
    """Hämta alla pathways inom en kategori."""
    return [p for p in PATHWAY_DATABASE.values() if p.category == category]

def find_gene_in_pathways(gene: str) -> List[Tuple[str, BiologicalPathway, PathwayGene]]:
    """Hitta alla pathways där en gen förekommer."""
    results = []
    for pathway_id, pathway in PATHWAY_DATABASE.items():
        for pg in pathway.genes:
            if pg.gene.upper() == gene.upper():
                results.append((pathway_id, pathway, pg))
    return results

def find_nutrient_in_pathways(nutrient: str) -> List[Tuple[str, BiologicalPathway, PathwayNutrient]]:
    """Hitta alla pathways där ett näringsämne är relevant."""
    results = []
    nutrient_lower = nutrient.lower()
    for pathway_id, pathway in PATHWAY_DATABASE.items():
        for pn in pathway.supporting_nutrients:
            if nutrient_lower in pn.nutrient.lower():
                results.append((pathway_id, pathway, pn))
    return results

def get_all_pathway_snps() -> Dict[str, List[str]]:
    """Samla alla SNPs från alla pathways för hämtning."""
    snps_by_gene = {}
    for pathway in PATHWAY_DATABASE.values():
        for gene in pathway.genes:
            if gene.gene not in snps_by_gene:
                snps_by_gene[gene.gene] = []
            for rsid in gene.rsids:
                if rsid not in snps_by_gene[gene.gene] and rsid != "Deletion":
                    snps_by_gene[gene.gene].append(rsid)
    return snps_by_gene

def assess_pathway_status(pathway_id: str, genetic_variants: Dict[str, str]) -> Dict:
    """
    Bedöm en pathways status baserat på genetiska varianter.

    Args:
        pathway_id: Pathway att analysera
        genetic_variants: Dict med rsid -> genotyp

    Returns:
        Dict med status, påverkade gener, och rekommendationer
    """
    pathway = get_pathway(pathway_id)
    if not pathway:
        return {"error": f"Pathway '{pathway_id}' hittades inte"}

    affected_genes = []
    recommendations = []
    severity_scores = []

    for gene in pathway.genes:
        for rsid in gene.rsids:
            if rsid in genetic_variants:
                genotype = genetic_variants[rsid]
                affected_genes.append({
                    "gene": gene.gene,
                    "rsid": rsid,
                    "genotype": genotype,
                    "effect": gene.effect_of_variants,
                    "cofactors": gene.key_cofactors
                })
                # Enkel severity-scoring (kan göras mer sofistikerad)
                if "null" in gene.effect_of_variants.lower() or "ingen" in gene.effect_of_variants.lower():
                    severity_scores.append(3)
                elif "reducerad" in gene.effect_of_variants.lower():
                    severity_scores.append(2)
                else:
                    severity_scores.append(1)

    # Beräkna övergripande status
    if not affected_genes:
        status = PathwayStatus.OPTIMAL
    elif max(severity_scores) >= 3 or sum(severity_scores) >= 5:
        status = PathwayStatus.SEVERELY_IMPAIRED
    elif max(severity_scores) >= 2 or sum(severity_scores) >= 3:
        status = PathwayStatus.IMPAIRED
    else:
        status = PathwayStatus.SUBOPTIMAL

    # Samla relevanta näringsämnen
    for gene_info in affected_genes:
        for cofactor in gene_info["cofactors"]:
            for nutrient in pathway.supporting_nutrients:
                if cofactor.lower() in nutrient.nutrient.lower():
                    recommendations.append(nutrient)

    return {
        "pathway": pathway.name,
        "status": status.value,
        "affected_genes": affected_genes,
        "recommended_nutrients": list(set(n.nutrient for n in recommendations)),
        "inhibitors_to_avoid": pathway.inhibitors,
        "relevant_metabolites": [m.name for m in pathway.metabolites],
        "clinical_relevance": pathway.clinical_relevance
    }

# =============================================================================
# MAIN / TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GWL BIOLOGICAL PATHWAYS DATABASE")
    print("=" * 70)

    print(f"\nAntal pathways: {len(PATHWAY_DATABASE)}")

    for pathway_id, pathway in PATHWAY_DATABASE.items():
        print(f"\n{pathway.name}:")
        print(f"  Kategori: {pathway.category.value}")
        print(f"  Gener: {len(pathway.genes)}")
        print(f"  Näringsämnen: {len(pathway.supporting_nutrients)}")
        print(f"  Metaboliter: {len(pathway.metabolites)}")

    # Samla alla SNPs
    print("\n" + "-" * 70)
    print("Alla pathway-SNPs för hämtning:")
    print("-" * 70)

    all_snps = get_all_pathway_snps()
    total_snps = 0
    for gene, snps in sorted(all_snps.items()):
        print(f"{gene}: {', '.join(snps)}")
        total_snps += len(snps)

    print(f"\nTotalt antal unika SNPs: {total_snps}")

    # Test pathway-sökning
    print("\n" + "-" * 70)
    print("TEST: Hitta MTHFR i pathways")
    print("-" * 70)

    mthfr_pathways = find_gene_in_pathways("MTHFR")
    for pathway_id, pathway, gene in mthfr_pathways:
        print(f"- {pathway.name}: {gene.role}")

    # Test näringsämne-sökning
    print("\n" + "-" * 70)
    print("TEST: Hitta magnesium i pathways")
    print("-" * 70)

    mg_pathways = find_nutrient_in_pathways("Magnesium")
    for pathway_id, pathway, nutrient in mg_pathways:
        print(f"- {pathway.name}: {nutrient.role}")

    print("\n" + "=" * 70)
    print("Databas laddad!")
    print("=" * 70)
