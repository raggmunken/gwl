"""
GWL Pharmacogenomics Database
=============================
Farmakogenomisk databas med gen-läkemedel interaktioner baserad på
CPIC (Clinical Pharmacogenetics Implementation Consortium) guidelines.

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

class EvidenceLevel(Enum):
    LEVEL_1A = "1A - Stark evidens, CPIC guideline"
    LEVEL_1B = "1B - Stark evidens, action required"
    LEVEL_2A = "2A - Måttlig evidens, action recommended"
    LEVEL_2B = "2B - Måttlig evidens, action optional"
    LEVEL_3 = "3 - Teoretisk/mindre evidens"
    LEVEL_4 = "4 - Forskningsnivå"

class DrugCategory(Enum):
    CARDIOVASCULAR = "Kardiovaskulära"
    PSYCHIATRIC = "Psykiatriska"
    PAIN = "Smärta"
    ONCOLOGY = "Onkologi"
    ANTIINFECTIVE = "Antiinfektiva"
    GASTROINTESTINAL = "Gastrointestinala"
    IMMUNOSUPPRESSANT = "Immunosuppressiva"
    ENDOCRINE = "Endokrina"
    NEUROLOGICAL = "Neurologiska"
    OTHER = "Övriga"

class ActionType(Enum):
    USE_ALTERNATIVE = "Använd alternativt läkemedel"
    DOSE_REDUCTION = "Dosreduktion krävs"
    DOSE_INCREASE = "Dosökning kan behövas"
    STANDARD_DOSE = "Standarddos OK"
    AVOID = "Undvik läkemedlet"
    CAUTION = "Försiktighet"
    MONITOR = "Extra övervakning"
    NO_ACTION = "Ingen åtgärd behövs"

class MetabolizerPhenotype(Enum):
    ULTRA_RAPID = "Ultra-snabb metaboliserare (UM)"
    RAPID = "Snabb metaboliserare (RM)"
    NORMAL = "Normal metaboliserare (NM)"
    INTERMEDIATE = "Intermediär metaboliserare (IM)"
    POOR = "Långsam metaboliserare (PM)"
    INDETERMINATE = "Obestämd"

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class DrugGenePair:
    """En gen-läkemedel-interaktion"""
    drug_name: str
    generic_name: str
    drug_category: DrugCategory
    gene: str
    rsids: List[str]
    evidence_level: EvidenceLevel
    cpic_guideline: Optional[str]
    phenotype_recommendations: Dict[MetabolizerPhenotype, Dict]  # phenotype -> {action, dose_adj, alternatives, notes}
    mechanism: str
    clinical_consequences: List[str]
    references: List[str]

@dataclass
class GeneAlleleTable:
    """Allel-till-fenotyp-tabell för en gen"""
    gene: str
    functional_alleles: Dict[str, str]  # allel -> funktion (Normal, Decreased, No function)
    diplotype_to_phenotype: Dict[str, MetabolizerPhenotype]  # diplotype -> phenotype
    activity_scores: Dict[str, float]  # allel -> activity score

# =============================================================================
# CYP2D6 ALLELE TABLE
# =============================================================================

CYP2D6_ALLELES = GeneAlleleTable(
    gene="CYP2D6",
    functional_alleles={
        "*1": "Normal function",
        "*2": "Normal function",
        "*2A": "Normal function",
        "*3": "No function",
        "*4": "No function",
        "*5": "No function (gene deletion)",
        "*6": "No function",
        "*7": "No function",
        "*8": "No function",
        "*9": "Decreased function",
        "*10": "Decreased function",
        "*11": "No function",
        "*12": "No function",
        "*14": "No function",
        "*17": "Decreased function",
        "*29": "Decreased function",
        "*41": "Decreased function",
        "*xN": "Increased function (gene duplication)"
    },
    diplotype_to_phenotype={
        "*1/*1": MetabolizerPhenotype.NORMAL,
        "*1/*2": MetabolizerPhenotype.NORMAL,
        "*2/*2": MetabolizerPhenotype.NORMAL,
        "*1/*4": MetabolizerPhenotype.INTERMEDIATE,
        "*1/*10": MetabolizerPhenotype.INTERMEDIATE,
        "*1/*41": MetabolizerPhenotype.INTERMEDIATE,
        "*4/*4": MetabolizerPhenotype.POOR,
        "*4/*5": MetabolizerPhenotype.POOR,
        "*5/*5": MetabolizerPhenotype.POOR,
        "*10/*10": MetabolizerPhenotype.INTERMEDIATE,
        "*1/*1xN": MetabolizerPhenotype.ULTRA_RAPID,
        "*1/*2xN": MetabolizerPhenotype.ULTRA_RAPID,
        "*2/*2xN": MetabolizerPhenotype.ULTRA_RAPID
    },
    activity_scores={
        "*1": 1.0,
        "*2": 1.0,
        "*3": 0,
        "*4": 0,
        "*5": 0,
        "*6": 0,
        "*9": 0.5,
        "*10": 0.25,  # Lower activity in Asian populations
        "*17": 0.5,
        "*29": 0.5,
        "*41": 0.5,
        "*xN": 2.0  # Per extra copy
    }
)

CYP2C19_ALLELES = GeneAlleleTable(
    gene="CYP2C19",
    functional_alleles={
        "*1": "Normal function",
        "*2": "No function",
        "*3": "No function",
        "*4": "No function",
        "*5": "No function",
        "*6": "No function",
        "*7": "No function",
        "*8": "No function",
        "*17": "Increased function"
    },
    diplotype_to_phenotype={
        "*1/*1": MetabolizerPhenotype.NORMAL,
        "*1/*2": MetabolizerPhenotype.INTERMEDIATE,
        "*1/*3": MetabolizerPhenotype.INTERMEDIATE,
        "*1/*17": MetabolizerPhenotype.RAPID,
        "*2/*2": MetabolizerPhenotype.POOR,
        "*2/*3": MetabolizerPhenotype.POOR,
        "*3/*3": MetabolizerPhenotype.POOR,
        "*17/*17": MetabolizerPhenotype.ULTRA_RAPID,
        "*2/*17": MetabolizerPhenotype.INTERMEDIATE  # Special case
    },
    activity_scores={
        "*1": 1.0,
        "*2": 0,
        "*3": 0,
        "*17": 1.5
    }
)

CYP2C9_ALLELES = GeneAlleleTable(
    gene="CYP2C9",
    functional_alleles={
        "*1": "Normal function",
        "*2": "Decreased function",
        "*3": "Decreased function",
        "*5": "Decreased function",
        "*6": "No function",
        "*8": "Decreased function",
        "*11": "Decreased function"
    },
    diplotype_to_phenotype={
        "*1/*1": MetabolizerPhenotype.NORMAL,
        "*1/*2": MetabolizerPhenotype.INTERMEDIATE,
        "*1/*3": MetabolizerPhenotype.INTERMEDIATE,
        "*2/*2": MetabolizerPhenotype.INTERMEDIATE,
        "*2/*3": MetabolizerPhenotype.POOR,
        "*3/*3": MetabolizerPhenotype.POOR
    },
    activity_scores={
        "*1": 1.0,
        "*2": 0.5,
        "*3": 0.25,
        "*5": 0.5,
        "*6": 0,
        "*8": 0.5
    }
)

# =============================================================================
# DRUG-GENE PAIRS: PAIN MEDICATIONS
# =============================================================================

CODEINE_CYP2D6 = DrugGenePair(
    drug_name="Kodein",
    generic_name="codeine",
    drug_category=DrugCategory.PAIN,
    gene="CYP2D6",
    rsids=["rs3892097", "rs1065852", "rs16947", "rs28371706"],
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for CYP2D6 and Codeine Therapy",
    phenotype_recommendations={
        MetabolizerPhenotype.ULTRA_RAPID: {
            "action": ActionType.AVOID,
            "dose_adjustment": "UNDVIK kodein",
            "alternatives": ["Morfin", "Oxykodon", "Icke-opioid analgetika"],
            "notes": "LIVSHOTANDE RISK - Snabb konvertering till morfin kan ge andningsdepression, "
                     "speciellt hos barn. KONTRAINDICERAT."
        },
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos",
            "alternatives": [],
            "notes": "Normal effekt förväntas"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.CAUTION,
            "dose_adjustment": "Standarddos, överväg alternativ vid otillräcklig effekt",
            "alternatives": ["Morfin", "Oxykodon"],
            "notes": "Reducerad analgetisk effekt möjlig"
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.USE_ALTERNATIVE,
            "dose_adjustment": "UNDVIK kodein - ingen effekt",
            "alternatives": ["Morfin", "Oxykodon", "Tapentadol"],
            "notes": "Ingen konvertering till aktiv metabolit (morfin). Ineffektivt som analgetikum."
        }
    },
    mechanism="Kodein är en prodrug som kräver CYP2D6-medierad O-demetylering till morfin för "
              "analgetisk effekt. ~10% av kodein konverteras normalt.",
    clinical_consequences=[
        "UM: Snabb morfinbildning -> överdos, andningsdepression, dödsfall rapporterade",
        "PM: Ingen morfinbildning -> ingen smärtlindring",
        "FDA Black Box Warning för barn med obstruktiv sömnapné efter tonsillektomi"
    ],
    references=[
        "PMID: 31562822 - CPIC Guideline for CYP2D6 and Codeine",
        "PMID: 27997040 - Codeine and CYP2D6 FDA warning",
        "PMID: 23486447 - CPIC Codeine Update"
    ]
)

TRAMADOL_CYP2D6 = DrugGenePair(
    drug_name="Tramadol",
    generic_name="tramadol",
    drug_category=DrugCategory.PAIN,
    gene="CYP2D6",
    rsids=["rs3892097", "rs1065852", "rs16947"],
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for CYP2D6 and Opioids",
    phenotype_recommendations={
        MetabolizerPhenotype.ULTRA_RAPID: {
            "action": ActionType.AVOID,
            "dose_adjustment": "UNDVIK tramadol",
            "alternatives": ["Morfin i låg dos", "Icke-opioid analgetika"],
            "notes": "Risk för andningsdepression och kramper pga snabb O-desmetyltramadol-bildning"
        },
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos",
            "alternatives": [],
            "notes": "Normal effekt"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.CAUTION,
            "dose_adjustment": "Kan behöva dosökning eller alternativ",
            "alternatives": ["Morfin", "Oxykodon"],
            "notes": "Reducerad effekt möjlig"
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.USE_ALTERNATIVE,
            "dose_adjustment": "UNDVIK tramadol",
            "alternatives": ["Morfin", "Oxykodon", "Tapentadol"],
            "notes": "Ineffektivt - minimal konvertering till aktiv metabolit"
        }
    },
    mechanism="Tramadol konverteras via CYP2D6 till O-desmetyltramadol (M1) som har "
              "200x högre affinitet för my-opioidreceptorn.",
    clinical_consequences=[
        "UM: Risk för toxicitet, kramper, serotoninsyndrom",
        "PM: Otillräcklig smärtlindring"
    ],
    references=[
        "PMID: 31562822 - CPIC Guideline for CYP2D6 and Codeine/Tramadol",
        "PMID: 25974703 - Tramadol pharmacogenetics"
    ]
)

# =============================================================================
# DRUG-GENE PAIRS: CARDIOVASCULAR
# =============================================================================

CLOPIDOGREL_CYP2C19 = DrugGenePair(
    drug_name="Clopidogrel (Plavix)",
    generic_name="clopidogrel",
    drug_category=DrugCategory.CARDIOVASCULAR,
    gene="CYP2C19",
    rsids=["rs4244285", "rs4986893", "rs12248560"],
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for CYP2C19 and Clopidogrel Therapy",
    phenotype_recommendations={
        MetabolizerPhenotype.ULTRA_RAPID: {
            "action": ActionType.CAUTION,
            "dose_adjustment": "Standarddos, överväg blödningsrisk",
            "alternatives": [],
            "notes": "God aktivering men möjlig ökad blödningsrisk"
        },
        MetabolizerPhenotype.RAPID: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos",
            "alternatives": [],
            "notes": "God aktivering"
        },
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos 75 mg/dag",
            "alternatives": [],
            "notes": "Normal effekt"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.USE_ALTERNATIVE,
            "dose_adjustment": "ÖVERVÄG ALTERNATIV",
            "alternatives": ["Prasugrel (Efient)", "Ticagrelor (Brilique)"],
            "notes": "Reducerad trombocythämning, ökad risk för hjärtinfarkt och stent-trombos"
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.USE_ALTERNATIVE,
            "dose_adjustment": "UNDVIK clopidogrel",
            "alternatives": ["Prasugrel (Efient)", "Ticagrelor (Brilique)"],
            "notes": "KRAFTIGT REDUCERAD EFFEKT - FDA Black Box Warning. "
                     "Signifikant ökad risk för stent-trombos och MACE."
        }
    },
    mechanism="Clopidogrel är en prodrug som kräver CYP2C19-medierad aktivering. "
              "Två steg: clopidogrel -> 2-oxo-clopidogrel -> aktiv tiolmetabolit.",
    clinical_consequences=[
        "PM/IM: Otillräcklig trombocythämning, ökad risk för stent-trombos efter PCI",
        "FDA Black Box Warning för poor metabolizers",
        "Prasugrel och ticagrelor påverkas inte av CYP2C19"
    ],
    references=[
        "PMID: 23698643 - CPIC Guideline for CYP2C19 and Clopidogrel",
        "PMID: 26417955 - CYP2C19 and cardiovascular outcomes",
        "PMID: 19106084 - Clopidogrel and CYP2C19"
    ]
)

WARFARIN_CYP2C9_VKORC1 = DrugGenePair(
    drug_name="Warfarin (Waran)",
    generic_name="warfarin",
    drug_category=DrugCategory.CARDIOVASCULAR,
    gene="CYP2C9/VKORC1",
    rsids=["rs1799853", "rs1057910", "rs9923231"],
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for Pharmacogenetics-Guided Warfarin Dosing",
    phenotype_recommendations={
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Använd farmakogenetisk dosalgoritm",
            "alternatives": [],
            "notes": "CYP2C9 *1/*1 + VKORC1 GG: ~5-7 mg/dag"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.DOSE_REDUCTION,
            "dose_adjustment": "15-40% dosreduktion",
            "alternatives": ["DOAC (apixaban, rivaroxaban)"],
            "notes": "CYP2C9 *1/*2 eller *1/*3: Reducerad clearance"
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.DOSE_REDUCTION,
            "dose_adjustment": "50-80% dosreduktion",
            "alternatives": ["DOAC (apixaban, rivaroxaban, dabigatran)"],
            "notes": "CYP2C9 *3/*3: Kraftigt reducerad dos (~1.5-2 mg/dag). "
                     "VKORC1 AA ytterligare reduktion. Överväg DOAC."
        }
    },
    mechanism="Warfarin metaboliseras primärt av CYP2C9 (S-warfarin, aktiv). "
              "VKORC1 är målenzymet - rs9923231 AA ökar känsligheten.",
    clinical_consequences=[
        "CYP2C9 + VKORC1 förklarar ~40% av dosvariationen",
        "PM: Ökad blödningsrisk vid standarddos",
        "Farmakogenetiska dosalgoritmer (warfarindosing.org)"
    ],
    references=[
        "PMID: 28198005 - CPIC Guideline for Warfarin",
        "PMID: 19755853 - Pharmacogenetics-based warfarin dosing",
        "PMID: 24827397 - Warfarin pharmacogenomics"
    ]
)

SIMVASTATIN_SLCO1B1 = DrugGenePair(
    drug_name="Simvastatin (Zocord)",
    generic_name="simvastatin",
    drug_category=DrugCategory.CARDIOVASCULAR,
    gene="SLCO1B1",
    rsids=["rs4149056"],
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for SLCO1B1 and Simvastatin",
    phenotype_recommendations={
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos upp till 40 mg/dag",
            "alternatives": [],
            "notes": "TT genotyp: Normal transportfunktion"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.DOSE_REDUCTION,
            "dose_adjustment": "Max 20 mg simvastatin",
            "alternatives": ["Pravastatin", "Rosuvastatin"],
            "notes": "TC genotyp: 4x ökad myopatirisk. Undvik högdos."
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.USE_ALTERNATIVE,
            "dose_adjustment": "UNDVIK simvastatin",
            "alternatives": ["Pravastatin (säkrast)", "Rosuvastatin"],
            "notes": "CC genotyp: 16x ökad myopatirisk. Simvastatin kontraindicerat. "
                     "Pravastatin påverkas inte."
        }
    },
    mechanism="SLCO1B1 transporterar statiner till levern. rs4149056 CC reducerar transportfunktion "
              "vilket ger förhöjda plasmakoncentrationer och ökad muskelexponering.",
    clinical_consequences=[
        "CC: 16x ökad risk för myopati vid 80 mg simvastatin",
        "FDA begränsar simvastatin 80 mg för nya patienter",
        "Pravastatin och rosuvastatin har lägre risk"
    ],
    references=[
        "PMID: 28027320 - CPIC Guideline for SLCO1B1 and Simvastatin",
        "PMID: 18650507 - SLCO1B1 and statin-induced myopathy",
        "PMID: 21730106 - Statin pharmacogenetics"
    ]
)

METOPROLOL_CYP2D6 = DrugGenePair(
    drug_name="Metoprolol (Seloken)",
    generic_name="metoprolol",
    drug_category=DrugCategory.CARDIOVASCULAR,
    gene="CYP2D6",
    rsids=["rs3892097", "rs1065852", "rs16947"],
    evidence_level=EvidenceLevel.LEVEL_2A,
    cpic_guideline=None,
    phenotype_recommendations={
        MetabolizerPhenotype.ULTRA_RAPID: {
            "action": ActionType.CAUTION,
            "dose_adjustment": "Kan behöva högre dos eller alternativ",
            "alternatives": ["Bisoprolol (CYP3A4)", "Atenolol (renal)"],
            "notes": "Snabb elimination - otillräcklig effekt möjlig"
        },
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos",
            "alternatives": [],
            "notes": "Normal effekt"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.MONITOR,
            "dose_adjustment": "Standarddos, övervaka",
            "alternatives": [],
            "notes": "Lätt förhöjda koncentrationer"
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.DOSE_REDUCTION,
            "dose_adjustment": "50% dosreduktion eller alternativ",
            "alternatives": ["Bisoprolol", "Atenolol", "Carvedilol"],
            "notes": "3-5x högre plasmakoncentration. Risk för bradykardi och hypotension."
        }
    },
    mechanism="Metoprolol metaboliseras primärt av CYP2D6 genom alfa-hydroxylering. "
              "PM har kraftigt förhöjda plasmakoncentrationer.",
    clinical_consequences=[
        "PM: Ökad risk för bradykardi, hypotension, trötthet",
        "Bisoprolol metaboliseras av CYP3A4 - bättre alternativ för PM"
    ],
    references=[
        "PMID: 20083681 - Metoprolol and CYP2D6",
        "PMID: 18058047 - Beta-blocker pharmacogenetics"
    ]
)

# =============================================================================
# DRUG-GENE PAIRS: PSYCHIATRIC
# =============================================================================

ESCITALOPRAM_CYP2C19 = DrugGenePair(
    drug_name="Escitalopram (Cipralex)",
    generic_name="escitalopram",
    drug_category=DrugCategory.PSYCHIATRIC,
    gene="CYP2C19",
    rsids=["rs4244285", "rs12248560"],
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for CYP2C19 and SSRIs",
    phenotype_recommendations={
        MetabolizerPhenotype.ULTRA_RAPID: {
            "action": ActionType.USE_ALTERNATIVE,
            "dose_adjustment": "Överväg alternativ SSRI",
            "alternatives": ["Sertralin", "Fluoxetin"],
            "notes": "Risk för terapisvikt pga snabb metabolism"
        },
        MetabolizerPhenotype.RAPID: {
            "action": ActionType.DOSE_INCREASE,
            "dose_adjustment": "Kan behöva högre dos (15-20 mg)",
            "alternatives": [],
            "notes": "Snabbare elimination"
        },
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos 10 mg",
            "alternatives": [],
            "notes": "Normal effekt"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.CAUTION,
            "dose_adjustment": "Standarddos eller 50% reduktion",
            "alternatives": [],
            "notes": "Överväg lägre startdos"
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.DOSE_REDUCTION,
            "dose_adjustment": "50% dosreduktion (5 mg startdos)",
            "alternatives": ["Sertralin", "Fluoxetin"],
            "notes": "2x högre plasmakoncentration. Risk för biverkningar."
        }
    },
    mechanism="Escitalopram N-demetyleras primärt av CYP2C19. S-demetylet har lägre aktivitet.",
    clinical_consequences=[
        "PM: Ökad risk för QTc-förlängning vid högre koncentrationer",
        "UM: Risk för behandlingssvikt"
    ],
    references=[
        "PMID: 25974703 - CPIC Guideline for SSRIs",
        "PMID: 23754190 - Escitalopram and CYP2C19"
    ]
)

SERTRALIN_CYP2C19 = DrugGenePair(
    drug_name="Sertralin (Zoloft)",
    generic_name="sertraline",
    drug_category=DrugCategory.PSYCHIATRIC,
    gene="CYP2C19",
    rsids=["rs4244285", "rs12248560"],
    evidence_level=EvidenceLevel.LEVEL_2A,
    cpic_guideline="CPIC Guideline for CYP2C19 and SSRIs",
    phenotype_recommendations={
        MetabolizerPhenotype.ULTRA_RAPID: {
            "action": ActionType.MONITOR,
            "dose_adjustment": "Kan behöva dosökning",
            "alternatives": [],
            "notes": "Mindre påverkan än escitalopram"
        },
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos",
            "alternatives": [],
            "notes": "Normal effekt"
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.CAUTION,
            "dose_adjustment": "Börja lågt (25 mg), titrera försiktigt",
            "alternatives": [],
            "notes": "Måttlig påverkan - sertralin har multipla metabolismvägar"
        }
    },
    mechanism="Sertralin metaboliseras av CYP2C19, CYP2D6 och CYP3A4. Mindre beroende av enskild CYP.",
    clinical_consequences=[
        "Mindre CYP2C19-beroende än escitalopram/citalopram",
        "Bättre val för patienter med CYP2C19 PM"
    ],
    references=[
        "PMID: 25974703 - CPIC Guideline for SSRIs"
    ]
)

AMITRIPTYLIN_CYP2D6_CYP2C19 = DrugGenePair(
    drug_name="Amitriptylin (Saroten)",
    generic_name="amitriptyline",
    drug_category=DrugCategory.PSYCHIATRIC,
    gene="CYP2D6/CYP2C19",
    rsids=["rs3892097", "rs4244285", "rs12248560"],
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for CYP2D6/CYP2C19 and TCAs",
    phenotype_recommendations={
        MetabolizerPhenotype.ULTRA_RAPID: {
            "action": ActionType.USE_ALTERNATIVE,
            "dose_adjustment": "Överväg alternativ eller dosökning",
            "alternatives": ["SNRI", "SSRI", "Annan TCA"],
            "notes": "Risk för terapisvikt vid standarddos"
        },
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos",
            "alternatives": [],
            "notes": "Normal effekt"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.DOSE_REDUCTION,
            "dose_adjustment": "25% dosreduktion",
            "alternatives": [],
            "notes": "Förhöjda koncentrationer av amitriptylin och nortriptylin"
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.USE_ALTERNATIVE,
            "dose_adjustment": "50% dosreduktion eller alternativ",
            "alternatives": ["SNRI", "SSRI"],
            "notes": "Kraftigt förhöjda koncentrationer. Risk för kardiotoxicitet, antikolinerga biverkningar."
        }
    },
    mechanism="Amitriptylin N-demetyleras av CYP2C19 till nortriptylin, som hydroxyleras av CYP2D6. "
              "Båda påverkar total exposition.",
    clinical_consequences=[
        "CYP2D6 PM: Förhöjt nortriptylin -> risk för toxicitet",
        "CYP2C19 PM: Förhöjt amitriptylin",
        "Dubbel PM: Kraftigt ökad risk för biverkningar"
    ],
    references=[
        "PMID: 27997040 - CPIC Guideline for TCAs",
        "PMID: 32185396 - TCA pharmacogenomics"
    ]
)

# =============================================================================
# DRUG-GENE PAIRS: ONCOLOGY
# =============================================================================

TAMOXIFEN_CYP2D6 = DrugGenePair(
    drug_name="Tamoxifen (Nolvadex)",
    generic_name="tamoxifen",
    drug_category=DrugCategory.ONCOLOGY,
    gene="CYP2D6",
    rsids=["rs3892097", "rs1065852", "rs16947", "rs28371706"],
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for CYP2D6 and Tamoxifen",
    phenotype_recommendations={
        MetabolizerPhenotype.ULTRA_RAPID: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos 20 mg",
            "alternatives": [],
            "notes": "Effektiv aktivering till endoxifen"
        },
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos 20 mg",
            "alternatives": [],
            "notes": "Normal endoxifenbildning"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.CAUTION,
            "dose_adjustment": "Överväg dosökning till 40 mg eller alternativ",
            "alternatives": ["Aromatashämmare (AI) för postmenopausal"],
            "notes": "Reducerade endoxifennivåer. Överväg plasma-endoxifenmätning."
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.USE_ALTERNATIVE,
            "dose_adjustment": "UNDVIK tamoxifen",
            "alternatives": [
                "Aromatashämmare (letrozol, anastrozol) för postmenopausala",
                "Ovarektomi + AI för premenopausala"
            ],
            "notes": "KRAFTIGT REDUCERAD EFFEKT. Minimal endoxifenbildning. "
                     "Ökad risk för bröstcancerrecidiv."
        }
    },
    mechanism="Tamoxifen konverteras via CYP2D6 till endoxifen (aktiv metabolit) som har "
              "100x högre affinitet för östrogenreceptorn.",
    clinical_consequences=[
        "PM: 50% ökad risk för bröstcancerrecidiv",
        "Undvik CYP2D6-hämmare: paroxetin, fluoxetin, bupropion",
        "Endoxifennivåer kan mätas för dosjustering"
    ],
    references=[
        "PMID: 23486447 - CPIC Guideline for Tamoxifen",
        "PMID: 29385237 - Tamoxifen and CYP2D6",
        "PMID: 20544677 - CYP2D6 and breast cancer outcomes"
    ]
)

FLUOROURACIL_DPYD = DrugGenePair(
    drug_name="5-Fluorouracil (5-FU)",
    generic_name="fluorouracil",
    drug_category=DrugCategory.ONCOLOGY,
    gene="DPYD",
    rsids=["rs3918290", "rs55886062", "rs67376798", "rs75017182"],
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for DPYD and Fluoropyrimidines",
    phenotype_recommendations={
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos",
            "alternatives": [],
            "notes": "Normal DPD-aktivitet"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.DOSE_REDUCTION,
            "dose_adjustment": "50% dosreduktion",
            "alternatives": [],
            "notes": "Reducerad DPD-aktivitet. Ökad toxicitetsrisk."
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.AVOID,
            "dose_adjustment": "UNDVIK fluoropyrimidiner",
            "alternatives": ["Alternativ kemoterapi beroende på cancertyp"],
            "notes": "LIVSHOTANDE TOXICITET. Komplett DPD-brist. "
                     "Risk för allvarlig neutropeni, diarré, stomatit, encephalopati, död."
        }
    },
    mechanism="Dihydropyrimidindehydrogenas (DPD) inaktiverar >80% av 5-FU. "
              "DPD-brist ger kraftigt förhöjd exposition.",
    clinical_consequences=[
        "DPD-brist: 10-20% mortalitet vid standarddos",
        "EMA kräver DPYD-testning före fluoropyrimidinbehandling",
        "rs3918290 (*2A): Komplett funktionsbortfall"
    ],
    references=[
        "PMID: 29152729 - CPIC Guideline for DPYD",
        "PMID: 28795450 - DPYD testing clinical utility"
    ]
)

# =============================================================================
# DRUG-GENE PAIRS: ANTIINFECTIVE
# =============================================================================

ABACAVIR_HLA_B5701 = DrugGenePair(
    drug_name="Abacavir (Ziagen)",
    generic_name="abacavir",
    drug_category=DrugCategory.ANTIINFECTIVE,
    gene="HLA-B*57:01",
    rsids=["rs2395029"],  # Tag-SNP
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for Abacavir and HLA-B*57:01",
    phenotype_recommendations={
        MetabolizerPhenotype.NORMAL: {  # HLA-B*57:01 negative
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos",
            "alternatives": [],
            "notes": "HLA-B*57:01 negativ - abacavir kan användas"
        },
        MetabolizerPhenotype.POOR: {  # HLA-B*57:01 positive
            "action": ActionType.AVOID,
            "dose_adjustment": "KONTRAINDICERAT",
            "alternatives": ["Tenofovir", "Emtricitabin"],
            "notes": "HLA-B*57:01 POSITIV - UNDVIK abacavir. "
                     "Risk för potentiellt livshotande överkänslighetsreaktion."
        }
    },
    mechanism="HLA-B*57:01 presenterar abacavir-modifierade självpeptider för T-celler, "
              "vilket utlöser immunmedierad överkänslighetsreaktion.",
    clinical_consequences=[
        "HLA-B*57:01 positiva: ~100% risk för reaktion vid exponering",
        "FDA och EMA kräver HLA-B*57:01-test före abacavirstart",
        "Kostnadseffektiv screening etablerad"
    ],
    references=[
        "PMID: 24847164 - CPIC Guideline for Abacavir",
        "PMID: 18192778 - HLA-B*5701 screening RCT"
    ]
)

# =============================================================================
# DRUG-GENE PAIRS: GASTROINTESTINAL
# =============================================================================

OMEPRAZOL_CYP2C19 = DrugGenePair(
    drug_name="Omeprazol (Losec)",
    generic_name="omeprazole",
    drug_category=DrugCategory.GASTROINTESTINAL,
    gene="CYP2C19",
    rsids=["rs4244285", "rs12248560"],
    evidence_level=EvidenceLevel.LEVEL_2A,
    cpic_guideline="CPIC Guideline for CYP2C19 and PPIs",
    phenotype_recommendations={
        MetabolizerPhenotype.ULTRA_RAPID: {
            "action": ActionType.DOSE_INCREASE,
            "dose_adjustment": "Ökad dos eller alternativ",
            "alternatives": ["Rabeprazol (mindre CYP2C19-beroende)", "Esomeprazol"],
            "notes": "Snabb elimination - kan behöva dubbeldos eller bytt till rabeprazol"
        },
        MetabolizerPhenotype.RAPID: {
            "action": ActionType.MONITOR,
            "dose_adjustment": "Standarddos, övervaka effekt",
            "alternatives": [],
            "notes": "Kan behöva högre dos"
        },
        MetabolizerPhenotype.NORMAL: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos",
            "alternatives": [],
            "notes": "Normal effekt"
        },
        MetabolizerPhenotype.INTERMEDIATE: {
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos - god effekt",
            "alternatives": [],
            "notes": "Förbättrad effekt jämfört med NM"
        },
        MetabolizerPhenotype.POOR: {
            "action": ActionType.CAUTION,
            "dose_adjustment": "Lägre dos räcker (10-20 mg)",
            "alternatives": [],
            "notes": "Förlängd verkan. Överväg dosreduktion vid långtidsbehandling."
        }
    },
    mechanism="PPI metaboliseras primärt av CYP2C19. PM har 4-10x högre AUC.",
    clinical_consequences=[
        "PM: Bättre H. pylori-eradikering",
        "UM: Risk för behandlingssvikt vid reflux",
        "Rabeprazol minst påverkat av CYP2C19"
    ],
    references=[
        "PMID: 25974703 - CYP2C19 and PPIs",
        "PMID: 17707196 - PPI pharmacogenetics"
    ]
)

# =============================================================================
# DRUG-GENE PAIRS: IMMUNOSUPPRESSANTS
# =============================================================================

TACROLIMUS_CYP3A5 = DrugGenePair(
    drug_name="Tacrolimus (Prograf)",
    generic_name="tacrolimus",
    drug_category=DrugCategory.IMMUNOSUPPRESSANT,
    gene="CYP3A5",
    rsids=["rs776746"],
    evidence_level=EvidenceLevel.LEVEL_1A,
    cpic_guideline="CPIC Guideline for CYP3A5 and Tacrolimus",
    phenotype_recommendations={
        MetabolizerPhenotype.NORMAL: {  # CYP3A5 expresser (*1/*1 eller *1/*3)
            "action": ActionType.DOSE_INCREASE,
            "dose_adjustment": "1.5-2x standarddos",
            "alternatives": [],
            "notes": "CYP3A5 *1 expresser - snabb metabolism, behöver högre dos"
        },
        MetabolizerPhenotype.INTERMEDIATE: {  # *1/*3
            "action": ActionType.DOSE_INCREASE,
            "dose_adjustment": "1.5x standarddos",
            "alternatives": [],
            "notes": "Intermediate expresser"
        },
        MetabolizerPhenotype.POOR: {  # CYP3A5 *3/*3 (non-expresser)
            "action": ActionType.STANDARD_DOSE,
            "dose_adjustment": "Standarddos",
            "alternatives": [],
            "notes": "CYP3A5 non-expresser (*3/*3) - standarddos räcker"
        }
    },
    mechanism="CYP3A5 *1 ger funktionellt enzym som metaboliserar tacrolimus. "
              "*3/*3 (vanligast i kaukasier) ger ingen CYP3A5-expression.",
    clinical_consequences=[
        "*1 bärare: Snabbare clearance, behöver högre dos för terapeutiska nivåer",
        "Viktigt vid transplantation för att undvika rejektion",
        "CYP3A5 expression varierar mellan etniciteter"
    ],
    references=[
        "PMID: 25801146 - CPIC Guideline for CYP3A5 and Tacrolimus"
    ]
)

# =============================================================================
# COMPLETE PHARMACOGENOMICS DATABASE
# =============================================================================

PHARMACOGENOMICS_DATABASE: Dict[str, DrugGenePair] = {
    # Pain
    "codeine_cyp2d6": CODEINE_CYP2D6,
    "tramadol_cyp2d6": TRAMADOL_CYP2D6,

    # Cardiovascular
    "clopidogrel_cyp2c19": CLOPIDOGREL_CYP2C19,
    "warfarin_cyp2c9_vkorc1": WARFARIN_CYP2C9_VKORC1,
    "simvastatin_slco1b1": SIMVASTATIN_SLCO1B1,
    "metoprolol_cyp2d6": METOPROLOL_CYP2D6,

    # Psychiatric
    "escitalopram_cyp2c19": ESCITALOPRAM_CYP2C19,
    "sertralin_cyp2c19": SERTRALIN_CYP2C19,
    "amitriptylin_cyp2d6_cyp2c19": AMITRIPTYLIN_CYP2D6_CYP2C19,

    # Oncology
    "tamoxifen_cyp2d6": TAMOXIFEN_CYP2D6,
    "fluorouracil_dpyd": FLUOROURACIL_DPYD,

    # Antiinfective
    "abacavir_hla_b5701": ABACAVIR_HLA_B5701,

    # GI
    "omeprazol_cyp2c19": OMEPRAZOL_CYP2C19,

    # Immunosuppressant
    "tacrolimus_cyp3a5": TACROLIMUS_CYP3A5
}

ALLELE_TABLES: Dict[str, GeneAlleleTable] = {
    "CYP2D6": CYP2D6_ALLELES,
    "CYP2C19": CYP2C19_ALLELES,
    "CYP2C9": CYP2C9_ALLELES
}

# =============================================================================
# PHENOTYPE DETERMINATION FUNCTIONS
# =============================================================================

def calculate_cyp2d6_activity_score(allele1: str, allele2: str) -> float:
    """Beräkna CYP2D6 activity score från två alleler."""
    scores = CYP2D6_ALLELES.activity_scores
    score1 = scores.get(allele1, 1.0)
    score2 = scores.get(allele2, 1.0)
    return score1 + score2

def activity_score_to_phenotype(score: float, gene: str = "CYP2D6") -> MetabolizerPhenotype:
    """Konvertera activity score till fenotyp (CPIC standard)."""
    if gene == "CYP2D6":
        if score >= 2.25:
            return MetabolizerPhenotype.ULTRA_RAPID
        elif score >= 1.25:
            return MetabolizerPhenotype.NORMAL
        elif score >= 0.25:
            return MetabolizerPhenotype.INTERMEDIATE
        else:
            return MetabolizerPhenotype.POOR
    else:
        return MetabolizerPhenotype.INDETERMINATE

def determine_cyp2c19_phenotype(allele1: str, allele2: str) -> MetabolizerPhenotype:
    """Bestäm CYP2C19-fenotyp från diplotyp."""
    diplotype = f"{allele1}/{allele2}"
    alt_diplotype = f"{allele2}/{allele1}"

    phenotype = CYP2C19_ALLELES.diplotype_to_phenotype.get(diplotype)
    if not phenotype:
        phenotype = CYP2C19_ALLELES.diplotype_to_phenotype.get(alt_diplotype)

    return phenotype or MetabolizerPhenotype.INDETERMINATE

def determine_cyp2c9_phenotype(allele1: str, allele2: str) -> MetabolizerPhenotype:
    """Bestäm CYP2C9-fenotyp från diplotyp."""
    diplotype = f"{allele1}/{allele2}"
    alt_diplotype = f"{allele2}/{allele1}"

    phenotype = CYP2C9_ALLELES.diplotype_to_phenotype.get(diplotype)
    if not phenotype:
        phenotype = CYP2C9_ALLELES.diplotype_to_phenotype.get(alt_diplotype)

    return phenotype or MetabolizerPhenotype.INDETERMINATE

# =============================================================================
# LOOKUP FUNCTIONS
# =============================================================================

def get_drug_gene_pair(drug_id: str) -> Optional[DrugGenePair]:
    """Hämta en specifik läkemedel-gen-interaktion."""
    return PHARMACOGENOMICS_DATABASE.get(drug_id.lower())

def get_all_drug_gene_pairs() -> List[str]:
    """Lista alla tillgängliga läkemedel-gen-par."""
    return list(PHARMACOGENOMICS_DATABASE.keys())

def get_drugs_by_category(category: DrugCategory) -> List[DrugGenePair]:
    """Hämta alla läkemedel inom en kategori."""
    return [d for d in PHARMACOGENOMICS_DATABASE.values() if d.drug_category == category]

def get_drugs_by_gene(gene: str) -> List[DrugGenePair]:
    """Hitta alla läkemedel som påverkas av en specifik gen."""
    results = []
    gene_upper = gene.upper()
    for drug in PHARMACOGENOMICS_DATABASE.values():
        if gene_upper in drug.gene.upper():
            results.append(drug)
    return results

def get_high_evidence_interactions() -> List[DrugGenePair]:
    """Hämta alla interaktioner med stark evidens (CPIC Level 1A)."""
    return [d for d in PHARMACOGENOMICS_DATABASE.values()
            if d.evidence_level == EvidenceLevel.LEVEL_1A]

def get_critical_warnings(phenotype: MetabolizerPhenotype) -> List[Dict]:
    """Hämta alla kritiska varningar för en specifik fenotyp."""
    warnings = []
    for drug_id, drug in PHARMACOGENOMICS_DATABASE.items():
        if phenotype in drug.phenotype_recommendations:
            rec = drug.phenotype_recommendations[phenotype]
            if rec["action"] in [ActionType.AVOID, ActionType.USE_ALTERNATIVE]:
                warnings.append({
                    "drug": drug.drug_name,
                    "gene": drug.gene,
                    "action": rec["action"].value,
                    "alternatives": rec["alternatives"],
                    "notes": rec["notes"]
                })
    return warnings

def get_all_pgx_snps() -> Dict[str, List[str]]:
    """Samla alla SNPs för farmakogenomisk testning."""
    snps_by_gene = {}
    for drug in PHARMACOGENOMICS_DATABASE.values():
        # Hantera gener med "/" (t.ex. CYP2D6/CYP2C19)
        genes = drug.gene.replace(" ", "").split("/")
        for gene in genes:
            if gene not in snps_by_gene:
                snps_by_gene[gene] = []
            for rsid in drug.rsids:
                if rsid not in snps_by_gene[gene]:
                    snps_by_gene[gene].append(rsid)
    return snps_by_gene

def generate_pgx_report(genotypes: Dict[str, str]) -> List[Dict]:
    """
    Generera farmakogenomisk rapport baserat på genotyper.

    Args:
        genotypes: Dict med rsid -> genotyp

    Returns:
        Lista med läkemedelsrekommendationer
    """
    report = []

    for drug_id, drug in PHARMACOGENOMICS_DATABASE.items():
        # Kontrollera om vi har relevanta genotyper
        relevant_genotypes = {rsid: genotypes[rsid] for rsid in drug.rsids if rsid in genotypes}

        if relevant_genotypes:
            # Förenklad fenotypbestämning (i verkligheten mer komplex)
            # Här skulle man använda calculate_cyp2d6_activity_score etc.

            report.append({
                "drug": drug.drug_name,
                "category": drug.drug_category.value,
                "gene": drug.gene,
                "evidence": drug.evidence_level.value,
                "cpic_guideline": drug.cpic_guideline,
                "genotypes_found": relevant_genotypes,
                "mechanism": drug.mechanism,
                "clinical_consequences": drug.clinical_consequences,
                "note": "Fenotyp och rekommendation kräver diplotypbestämning"
            })

    return report

# =============================================================================
# MAIN / TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GWL PHARMACOGENOMICS DATABASE")
    print("=" * 70)

    print(f"\nAntal läkemedel-gen-par: {len(PHARMACOGENOMICS_DATABASE)}")

    print("\nLäkemedel per kategori:")
    for category in DrugCategory:
        drugs = get_drugs_by_category(category)
        if drugs:
            print(f"  {category.value}: {len(drugs)}")

    print("\n" + "-" * 70)
    print("CPIC Level 1A (stark evidens) interaktioner:")
    print("-" * 70)

    high_evidence = get_high_evidence_interactions()
    for drug in high_evidence:
        print(f"\n{drug.drug_name} ({drug.generic_name}):")
        print(f"  Gen: {drug.gene}")
        print(f"  Guideline: {drug.cpic_guideline}")

    print("\n" + "-" * 70)
    print("CYP2D6-påverkade läkemedel:")
    print("-" * 70)

    cyp2d6_drugs = get_drugs_by_gene("CYP2D6")
    for drug in cyp2d6_drugs:
        print(f"- {drug.drug_name}: {drug.phenotype_recommendations.get(MetabolizerPhenotype.POOR, {}).get('action', 'N/A')}")

    print("\n" + "-" * 70)
    print("Kritiska varningar för CYP2D6 Poor Metabolizer:")
    print("-" * 70)

    warnings = get_critical_warnings(MetabolizerPhenotype.POOR)
    for w in warnings:
        print(f"\n{w['drug']} ({w['gene']}):")
        print(f"  Åtgärd: {w['action']}")
        print(f"  Alternativ: {', '.join(w['alternatives']) if w['alternatives'] else 'Inga'}")

    print("\n" + "-" * 70)
    print("Alla SNPs för PGx-testning:")
    print("-" * 70)

    all_snps = get_all_pgx_snps()
    total = 0
    for gene, snps in sorted(all_snps.items()):
        print(f"{gene}: {', '.join(snps)}")
        total += len(snps)

    print(f"\nTotalt antal SNPs: {total}")

    # Test fenotypbestämning
    print("\n" + "-" * 70)
    print("TEST: CYP2D6 Activity Score beräkning")
    print("-" * 70)

    test_diplotypes = [
        ("*1", "*1"),    # Normal
        ("*1", "*4"),    # Intermediate
        ("*4", "*4"),    # Poor
        ("*1", "*1xN"),  # Ultra-rapid
        ("*10", "*10"),  # Intermediate (Asian)
    ]

    for a1, a2 in test_diplotypes:
        score = calculate_cyp2d6_activity_score(a1, a2)
        phenotype = activity_score_to_phenotype(score)
        print(f"CYP2D6 {a1}/{a2}: Score={score}, Fenotyp={phenotype.value}")

    print("\n" + "=" * 70)
    print("Databas laddad!")
    print("=" * 70)
