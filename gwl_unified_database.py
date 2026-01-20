"""
GWL Unified Database
====================
EN CENTRAL DATABAS som samlar ALL genetisk data på ett ställe.
Detta är den enda filen som behöver uppdateras när ny data hämtas.

När du kör analysen med din 23andMe-fil, läser systemet från denna databas.

INNEHÅLLER:
- 100+ SNPs från alla kategorier
- Haplotypinformation (APOE, CYP2D6, CYP2C19, MTHFR, etc.)
- Gen-gen interaktioner (epistasis)
- Farmakogenomik (läkemedelsinteraktioner)
- Populationsfrekvenser
- Pathway-kopplingar
- Närings- och livsstilsrekommendationer

Genetic Wellness Labs - Nutrigenomics Platform
"""

import sys
import io

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set, Any
from enum import Enum

# =============================================================================
# MASTER ENUMS
# =============================================================================

class Category(Enum):
    METHYLATION = "Metylering"
    VITAMIN_D = "D-vitamin"
    OMEGA3 = "Omega-3"
    STRESS_MOOD = "Stress & Humör"
    CAFFEINE = "Koffein"
    SLEEP = "Sömn"
    IRON = "Järn"
    ANTIOXIDANT = "Antioxidant"
    INFLAMMATION = "Inflammation"
    DETOX_PHASE1 = "Detox Fas I"
    DETOX_PHASE2 = "Detox Fas II"
    BONE_HEALTH = "Benhälsa"
    BLOOD_PRESSURE = "Blodtryck"
    OBESITY = "Vikt"
    HISTAMINE = "Histamin"
    BLOOD_SUGAR = "Blodsocker"
    THYROID = "Sköldkörtel"
    MUSCLE = "Muskel"
    IMMUNE = "Immunsystem"
    SKIN = "Hud"
    CARDIOVASCULAR = "Kardiovaskulär"
    PHARMACOGENOMICS = "Farmakogenomik"
    BH4_CYCLE = "BH4-cykel"
    NEUROTRANSMITTER = "Neurotransmittorer"
    CIRCADIAN = "Dygnsrytm"
    HORMONE = "Hormonmetabolism"

class RiskLevel(Enum):
    PROTECTIVE = "Skyddande"
    NORMAL = "Normal"
    SLIGHTLY_INCREASED = "Lätt förhöjd"
    MODERATELY_INCREASED = "Måttligt förhöjd"
    SIGNIFICANTLY_INCREASED = "Betydligt förhöjd"
    HIGH = "Hög"

class ActionPriority(Enum):
    CRITICAL = 1  # Måste åtgärdas
    HIGH = 2      # Bör åtgärdas
    MODERATE = 3  # Rekommenderas
    LOW = 4       # Kan övervägas
    INFO = 5      # Information endast

# =============================================================================
# MASTER DATA CLASS - EN SNP, ALL INFO
# =============================================================================

@dataclass
class UnifiedSNP:
    """Komplett information om en SNP - ALLT på ett ställe"""

    # Grundläggande info
    rsid: str
    gene: str
    chromosome: str
    position: int
    ref_allele: str
    alt_allele: str

    # Kategorisering
    categories: List[Category]

    # Genotyp-effekter
    genotype_effects: Dict[str, Dict[str, Any]]  # genotyp -> {risk, effect, description}

    # Näringsrekommendationer per genotyp
    nutrient_recommendations: Dict[str, List[Dict[str, str]]]  # genotyp -> [{nutrient, dose, reason}]

    # Livsstilsrekommendationer per genotyp
    lifestyle_recommendations: Dict[str, List[str]]  # genotyp -> [rekommendationer]

    # Läkemedelsinteraktioner (om relevant)
    drug_interactions: Dict[str, List[Dict[str, str]]]  # genotyp -> [{drug, action, note}]

    # Pathway-kopplingar
    pathways: List[str]

    # Gen-gen interaktioner (rsids som interagerar med denna)
    interacts_with: List[str]

    # Haplotyp-info (om del av haplotyp)
    haplotype_gene: Optional[str]  # T.ex. "APOE", "CYP2D6"
    haplotype_role: Optional[str]  # Vad denna SNP bidrar med i haplotypen

    # Population frequencies
    frequencies: Dict[str, float]  # population -> alt_allele_freq

    # Referenser
    pmids: List[str]

    # Klinisk signifikans
    clinical_significance: str
    evidence_level: str  # "Strong", "Moderate", "Preliminary"

# =============================================================================
# UNIFIED DATABASE - ALLA SNPs
# =============================================================================

UNIFIED_DATABASE: Dict[str, UnifiedSNP] = {

    # =========================================================================
    # METHYLATION - MTHFR
    # =========================================================================

    "rs1801133": UnifiedSNP(
        rsid="rs1801133",
        gene="MTHFR",
        chromosome="1",
        position=11856378,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.METHYLATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal MTHFR-aktivitet (100%)", "description": "Wildtyp, normal folatmetabolism"},
            "GA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Reducerad aktivitet (~65%)", "description": "Heterozygot C677T, lätt reducerad metylering"},
            "AA": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "Kraftigt reducerad aktivitet (~30%)", "description": "Homozygot C677T, signifikant reducerad metylering, förhöjt homocystein"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "Folat", "dose": "400 mcg DFE/dag", "reason": "Standardbehov"}],
            "GA": [
                {"nutrient": "Metylfolat (5-MTHF)", "dose": "400-800 mcg/dag", "reason": "Aktiv form kringgår MTHFR"},
                {"nutrient": "Riboflavin (B2)", "dose": "25-50 mg/dag", "reason": "Stabiliserar MTHFR-enzymet"}
            ],
            "AA": [
                {"nutrient": "Metylfolat (5-MTHF)", "dose": "800-1500 mcg/dag", "reason": "OBLIGATORISKT - kringgår defekt MTHFR"},
                {"nutrient": "Metylkobalamin (B12)", "dose": "1000-5000 mcg/dag", "reason": "Krävs för MTR-funktion"},
                {"nutrient": "Riboflavin (B2)", "dose": "50-100 mg/dag", "reason": "Kritisk kofaktor, stabiliserar enzymet"},
                {"nutrient": "P5P (B6)", "dose": "25-50 mg/dag", "reason": "Stödjer transsulfureringsvägen"},
                {"nutrient": "Betain (TMG)", "dose": "500-3000 mg/dag", "reason": "Alternativ metyldonator via BHMT"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Balanserad kost med gröna bladgrönsaker"],
            "GA": ["Öka intag av folatrika livsmedel", "Undvik syntetisk folsyra i höga doser"],
            "AA": [
                "UNDVIK syntetisk folsyra helt (berikade livsmedel, multivitaminer)",
                "UNDVIK lustgas (N2O) vid operation - inaktiverar B12",
                "Undvik högt alkoholintag - utarmar B-vitaminer",
                "Kontrollera homocystein årligen"
            ]
        },
        drug_interactions={
            "AA": [
                {"drug": "Metotrexat", "action": "Ökad känslighet", "note": "Hämmar DHFR, förvärrar folatbrist"},
                {"drug": "Fenytoin", "action": "Ökad risk", "note": "Sänker folatnivåer"},
                {"drug": "Lustgas (N2O)", "action": "KONTRAINDICERAT", "note": "Inaktiverar B12, kan ge akut neurologisk skada"}
            ]
        },
        pathways=["Metyleringscykeln", "Folatcykeln", "Homocysteinmetabolism"],
        interacts_with=["rs1801131", "rs1805087", "rs1801394", "rs4680"],
        haplotype_gene="MTHFR",
        haplotype_role="C677T mutation - avgör MTHFR termostabilitet",
        frequencies={"EUR": 0.36, "EAS": 0.30, "AFR": 0.10, "SAS": 0.14, "AMR": 0.45},
        pmids=["24935961", "28125025", "18579210"],
        clinical_significance="Reducerad MTHFR-aktivitet leder till nedsatt produktion av 5-MTHF, den aktiva formen av folat som behövs för metylering av homocystein.",
        evidence_level="Strong"
    ),

    "rs1801131": UnifiedSNP(
        rsid="rs1801131",
        gene="MTHFR",
        chromosome="1",
        position=11854476,
        ref_allele="T",
        alt_allele="G",
        categories=[Category.METHYLATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.NORMAL, "effect": "Normal MTHFR", "description": "Wildtyp A1298A"},
            "TG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Lätt reducerad", "description": "Heterozygot A1298C"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Reducerad aktivitet (~60%)", "description": "Homozygot A1298C, påverkar BH4-regenerering"}
        },
        nutrient_recommendations={
            "TT": [{"nutrient": "Folat", "dose": "400 mcg/dag", "reason": "Standardbehov"}],
            "TG": [{"nutrient": "Metylfolat", "dose": "400-800 mcg/dag", "reason": "Aktiv form fördelaktigt"}],
            "GG": [
                {"nutrient": "Metylfolat", "dose": "800-1000 mcg/dag", "reason": "Behövs för reducerad aktivitet"},
                {"nutrient": "BH4-stöd", "dose": "Via folat/B12", "reason": "1298C påverkar BH4-regenerering"}
            ]
        },
        lifestyle_recommendations={
            "TT": ["Standardkost"],
            "TG": ["Folatrik kost"],
            "GG": ["Folatrik kost", "Undvik syntetisk folsyra"]
        },
        drug_interactions={},
        pathways=["Metyleringscykeln", "BH4-cykeln"],
        interacts_with=["rs1801133"],
        haplotype_gene="MTHFR",
        haplotype_role="A1298C mutation - påverkar regulatorisk domän och BH4",
        frequencies={"EUR": 0.30, "EAS": 0.20, "AFR": 0.10, "SAS": 0.25},
        pmids=["17109754", "24935961"],
        clinical_significance="A1298C påverkar MTHFR regulatoriska domän och kan försämra BH4-regenerering. Särskilt viktig i kombination med C677T (compound heterozygot).",
        evidence_level="Strong"
    ),

    # =========================================================================
    # METHYLATION - MTR, MTRR, BHMT
    # =========================================================================

    "rs1805087": UnifiedSNP(
        rsid="rs1805087",
        gene="MTR",
        chromosome="1",
        position=237048500,
        ref_allele="A",
        alt_allele="G",
        categories=[Category.METHYLATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.NORMAL, "effect": "Normal MTR", "description": "Wildtyp metioninsyntetas"},
            "AG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Lätt reducerad", "description": "Heterozygot A2756G"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Reducerad aktivitet", "description": "Homozygot, ökad B12-förbrukning"}
        },
        nutrient_recommendations={
            "AA": [{"nutrient": "B12", "dose": "500-1000 mcg/dag", "reason": "Standard"}],
            "AG": [{"nutrient": "Metylkobalamin", "dose": "1000-2500 mcg/dag", "reason": "Ökad förbrukning"}],
            "GG": [
                {"nutrient": "Metylkobalamin", "dose": "2500-5000 mcg/dag", "reason": "Kritisk kofaktor"},
                {"nutrient": "Metylfolat", "dose": "400-800 mcg/dag", "reason": "Substrat för MTR"}
            ]
        },
        lifestyle_recommendations={
            "AA": ["Standardkost"],
            "AG": ["B12-rika livsmedel"],
            "GG": ["B12-tillskott rekommenderas", "Överväg sublingual administration"]
        },
        drug_interactions={
            "GG": [{"drug": "Metformin", "action": "Försiktighet", "note": "Sänker B12-absorption"}]
        },
        pathways=["Metyleringscykeln"],
        interacts_with=["rs1801133", "rs1801394"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.20, "EAS": 0.10, "AFR": 0.35},
        pmids=["16757948", "28125025"],
        clinical_significance="MTR A2756G påverkar metioninsyntetas som överför metylgrupper från folat till homocystein.",
        evidence_level="Moderate"
    ),

    "rs1801394": UnifiedSNP(
        rsid="rs1801394",
        gene="MTRR",
        chromosome="5",
        position=7870973,
        ref_allele="A",
        alt_allele="G",
        categories=[Category.METHYLATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.NORMAL, "effect": "Normal MTRR", "description": "Wildtyp"},
            "AG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Lätt reducerad", "description": "Heterozygot A66G"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Reducerad MTR-regenerering", "description": "Homozygot, långsammare MTR-aktivering"}
        },
        nutrient_recommendations={
            "AA": [{"nutrient": "B12", "dose": "Standard", "reason": "Normal funktion"}],
            "AG": [{"nutrient": "B12", "dose": "1000-2000 mcg/dag", "reason": "Stödjer MTR-regenerering"}],
            "GG": [
                {"nutrient": "Metylkobalamin + Adenosylkobalamin", "dose": "2000-5000 mcg/dag", "reason": "Båda former kan behövas"},
                {"nutrient": "SAMe", "dose": "200-400 mg/dag", "reason": "Kan stödja MTR-regenerering"}
            ]
        },
        lifestyle_recommendations={
            "AA": ["Standardkost"],
            "AG": ["B12-rika livsmedel"],
            "GG": ["B12-tillskott", "Undvik PPI långvarigt"]
        },
        drug_interactions={},
        pathways=["Metyleringscykeln"],
        interacts_with=["rs1801133", "rs1805087"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.45, "EAS": 0.30, "AFR": 0.25},
        pmids=["16757948", "23571587"],
        clinical_significance="MTRR A66G påverkar enzym som regenererar MTR, vilket indirekt påverkar metyleringskapacitet.",
        evidence_level="Moderate"
    ),

    "rs3733890": UnifiedSNP(
        rsid="rs3733890",
        gene="BHMT",
        chromosome="5",
        position=78573621,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.METHYLATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal BHMT", "description": "Wildtyp"},
            "GA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Lätt påverkad", "description": "Heterozygot"},
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Reducerad betain-väg", "description": "Homozygot R239Q"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "GA": [{"nutrient": "Betain (TMG)", "dose": "500-1500 mg/dag", "reason": "Stödjer alternativ väg"}],
            "AA": [
                {"nutrient": "Betain (TMG)", "dose": "1000-3000 mg/dag", "reason": "Substrat för BHMT"},
                {"nutrient": "Zink", "dose": "15-30 mg/dag", "reason": "BHMT-kofaktor"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Standardkost"],
            "GA": ["Kolinrika livsmedel (ägg, lever)"],
            "AA": ["Betain via rödbetor, quinoa", "Kolinrika livsmedel"]
        },
        drug_interactions={},
        pathways=["Metyleringscykeln", "Alternativ metylering"],
        interacts_with=["rs1801133"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.30, "EAS": 0.15, "AFR": 0.20},
        pmids=["18579210"],
        clinical_significance="BHMT erbjuder alternativ metylering via betain, viktigt vid MTHFR-mutation.",
        evidence_level="Moderate"
    ),

    # =========================================================================
    # NEUROTRANSMITTERS - COMT, MAO, BDNF
    # =========================================================================

    "rs4680": UnifiedSNP(
        rsid="rs4680",
        gene="COMT",
        chromosome="22",
        position=19963748,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.STRESS_MOOD, Category.NEUROTRANSMITTER, Category.METHYLATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Snabb COMT (Val/Val) - Warrior", "description": "Hög enzymaktivitet, lågt prefrontalt dopamin, stresstålig"},
            "GA": {"risk": RiskLevel.NORMAL, "effect": "Intermediär (Val/Met)", "description": "Balanserad dopaminnedbrytning"},
            "AA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Långsam COMT (Met/Met) - Worrier", "description": "Låg enzymaktivitet, högt prefrontalt dopamin, ångestkänslig"}
        },
        nutrient_recommendations={
            "GG": [
                {"nutrient": "Tyrosin", "dose": "500-2000 mg/dag", "reason": "Stödjer dopaminproduktion"},
                {"nutrient": "SAMe", "dose": "200-400 mg/dag", "reason": "Kan tolerera metylering"}
            ],
            "GA": [{"nutrient": "Balanserat B-komplex", "dose": "Standard", "reason": "Balanserad approach"}],
            "AA": [
                {"nutrient": "Magnesium", "dose": "300-400 mg/dag", "reason": "COMT-kofaktor, lugnande"},
                {"nutrient": "L-Theanin", "dose": "100-200 mg/dag", "reason": "Modulerar dopamin, lugnande"},
                {"nutrient": "Försiktigt med metylfolat", "dose": "Börja lågt 100-200 mcg", "reason": "Risk för övermetylering"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Kan hantera stress bra", "Motion för dopaminboost"],
            "GA": ["Balanserad livsstil"],
            "AA": [
                "UNDVIK grönt te-extrakt/EGCG (COMT-hämmare)",
                "Stresshantering kritisk - meditation, yoga",
                "Undvik stimulantia och höga doser koffein",
                "Regelbunden sömn viktigt"
            ]
        },
        drug_interactions={
            "AA": [
                {"drug": "SSRI", "action": "Ökad känslighet", "note": "Kan få starkare effekt"},
                {"drug": "Stimulantia", "action": "Försiktighet", "note": "Risk för ångest/agitation"},
                {"drug": "Levodopa", "action": "Förlängd effekt", "note": "Långsammare nedbrytning"}
            ]
        },
        pathways=["Neurotransmittormetabolism", "Katekolaminnedbrytning", "Östrogenmetabolism", "Metyleringscykeln"],
        interacts_with=["rs1801133", "rs6323", "rs6265", "rs1056836"],
        haplotype_gene="COMT",
        haplotype_role="Val158Met - avgör COMT-aktivitet",
        frequencies={"EUR": 0.48, "EAS": 0.28, "AFR": 0.30, "SAS": 0.40},
        pmids=["17008817", "19081561", "21385469"],
        clinical_significance="COMT Val158Met är en av de mest studerade SNPs för personlighet och stressrespons. Met/Met ger hög kognitiv kapacitet men ökad ångestkänslighet.",
        evidence_level="Strong"
    ),

    "rs6323": UnifiedSNP(
        rsid="rs6323",
        gene="MAO-A",
        chromosome="X",
        position=43592790,
        ref_allele="G",
        alt_allele="T",
        categories=[Category.STRESS_MOOD, Category.NEUROTRANSMITTER],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal MAO-A", "description": "Standard monoaminomsättning"},
            "GT": {"risk": RiskLevel.NORMAL, "effect": "Intermediär", "description": "Heterozygot (endast kvinnor)"},
            "TT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Högre MAO-A", "description": "Snabbare serotonin/noradrenalin-nedbrytning"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "Standard B-komplex", "dose": "Standard", "reason": "Normal funktion"}],
            "GT": [{"nutrient": "Riboflavin (B2)", "dose": "25-50 mg/dag", "reason": "MAO-A-kofaktor"}],
            "TT": [
                {"nutrient": "5-HTP eller Tryptofan", "dose": "50-100 mg / 500-1000 mg", "reason": "Stödjer serotoninproduktion"},
                {"nutrient": "Riboflavin", "dose": "25-50 mg/dag", "reason": "FAD-kofaktor"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Standardrekommendationer"],
            "GT": ["Balanserad livsstil"],
            "TT": ["Regelbunden motion för serotoninstöd", "Ljusexponering morgon"]
        },
        drug_interactions={
            "TT": [
                {"drug": "MAO-hämmare", "action": "Starkare effekt", "note": "Lägre dos kan behövas"},
                {"drug": "SSRI", "action": "Normal", "note": "Kan behöva standarddos"}
            ]
        },
        pathways=["Neurotransmittormetabolism", "Serotoninnedbrytning"],
        interacts_with=["rs4680"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.40, "EAS": 0.30, "AFR": 0.45},
        pmids=["18578540", "21385469"],
        clinical_significance="MAO-A bryter ner serotonin, noradrenalin och dopamin. Varianter påverkar stämningsreglering och stressrespons.",
        evidence_level="Moderate"
    ),

    "rs6265": UnifiedSNP(
        rsid="rs6265",
        gene="BDNF",
        chromosome="11",
        position=27658369,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.STRESS_MOOD, Category.NEUROTRANSMITTER],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal BDNF (Val/Val)", "description": "Normal neuroplasticitet och BDNF-sekretion"},
            "GA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Reducerad BDNF (Val/Met)", "description": "Måttligt reducerad aktivitetsberoende sekretion"},
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Kraftigt reducerad (Met/Met)", "description": "Signifikant reducerad BDNF-sekretion, ökad depressionskänslighet"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "Omega-3 (DHA)", "dose": "1-2 g/dag", "reason": "Stödjer BDNF"}],
            "GA": [
                {"nutrient": "Omega-3 (DHA)", "dose": "2-3 g/dag", "reason": "Ökar BDNF-expression"},
                {"nutrient": "Curcumin", "dose": "500-1000 mg/dag", "reason": "Ökar BDNF"}
            ],
            "AA": [
                {"nutrient": "Omega-3 (DHA)", "dose": "2-4 g/dag", "reason": "KRITISKT för BDNF-stöd"},
                {"nutrient": "Lion's Mane", "dose": "500-1000 mg/dag", "reason": "Ökar NGF och neuroplasticitet"},
                {"nutrient": "Curcumin", "dose": "500-1000 mg/dag", "reason": "BDNF-stöd"},
                {"nutrient": "Zink", "dose": "15-30 mg/dag", "reason": "Stödjer BDNF-signalering"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Regelbunden motion"],
            "GA": ["Motion ökar BDNF", "Social interaktion"],
            "AA": [
                "MOTION KRITISKT - mest effektiva BDNF-boostern",
                "Sömnoptimering (BDNF ökar under sömn)",
                "Intermittent fasta kan öka BDNF",
                "Social kontakt och mental stimulering"
            ]
        },
        drug_interactions={},
        pathways=["Neuroplasticitet", "Synaptisk funktion"],
        interacts_with=["rs4680"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.20, "EAS": 0.45, "AFR": 0.02, "SAS": 0.18},
        pmids=["27067767", "16914770", "19136964"],
        clinical_significance="BDNF Val66Met påverkar aktivitetsberoende sekretion av BDNF, vilket påverkar neuroplasticitet och depressionskänslighet.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # APOE - CARDIOVASCULAR & ALZHEIMER
    # =========================================================================

    "rs429358": UnifiedSNP(
        rsid="rs429358",
        gene="APOE",
        chromosome="19",
        position=44908684,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.CARDIOVASCULAR, Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.NORMAL, "effect": "e2 eller e3 möjlig", "description": "Avgörs med rs7412"},
            "TC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "e4 heterozygot trolig", "description": "En kopia av e4"},
            "CC": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "e4 homozygot trolig", "description": "Två kopior av e4, kraftigt ökad risk"}
        },
        nutrient_recommendations={
            "TT": [{"nutrient": "Standard", "dose": "Standard", "reason": "Avgörs med full APOE-genotyp"}],
            "TC": [
                {"nutrient": "Omega-3 (DHA)", "dose": "2-4 g/dag", "reason": "Kritiskt vid APOE e4"},
                {"nutrient": "Vitamin E", "dose": "400 IE/dag", "reason": "Antioxidant för hjärnan"},
                {"nutrient": "Curcumin", "dose": "500-1000 mg/dag", "reason": "Anti-inflammatoriskt"}
            ],
            "CC": [
                {"nutrient": "Omega-3 (DHA)", "dose": "3-4 g/dag", "reason": "KRITISKT vid e4/e4"},
                {"nutrient": "Vitamin E (tokotrienoler)", "dose": "400 IE/dag", "reason": "Skyddar hjärnan"},
                {"nutrient": "Curcumin", "dose": "1000-2000 mg/dag", "reason": "Anti-inflammatoriskt"},
                {"nutrient": "Fosfatidylkolin", "dose": "1-2 g/dag", "reason": "Stödjer kolintransport"}
            ]
        },
        lifestyle_recommendations={
            "TT": ["Standardrekommendationer"],
            "TC": [
                "Minska mättat fett",
                "Medelhavskost rekommenderas",
                "Regelbunden motion",
                "Kognitiv stimulering"
            ],
            "CC": [
                "STRIKT mättat fett-restriktion",
                "Medelhavskost OBLIGATORISKT",
                "Undvik transfetter helt",
                "Regelbunden motion (minst 150 min/vecka)",
                "Kognitiv träning och social aktivitet",
                "Överväg regelbunden lipidprofil"
            ]
        },
        drug_interactions={
            "CC": [
                {"drug": "Statiner", "action": "Kan behövas tidigare", "note": "Diskutera med läkare"},
                {"drug": "HRT", "action": "Försiktighet", "note": "Ökad trombosrisk"}
            ]
        },
        pathways=["Lipidmetabolism", "Amyloid-clearance"],
        interacts_with=["rs7412", "rs708272"],
        haplotype_gene="APOE",
        haplotype_role="Avgör Cys112Arg position för APOE-isoform",
        frequencies={"EUR": 0.15, "EAS": 0.09, "AFR": 0.26, "SAS": 0.10},
        pmids=["31727829", "23571587"],
        clinical_significance="APOE rs429358 är en av två SNPs som bestämmer APOE-genotyp. C-allelen definierar e4-allelen som ökar risk för Alzheimer och hjärt-kärlsjukdom.",
        evidence_level="Strong"
    ),

    "rs7412": UnifiedSNP(
        rsid="rs7412",
        gene="APOE",
        chromosome="19",
        position=44908822,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.CARDIOVASCULAR, Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "e3 eller e4 möjlig", "description": "Avgörs med rs429358"},
            "CT": {"risk": RiskLevel.PROTECTIVE, "effect": "e2 heterozygot trolig", "description": "e2 är skyddande"},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "e2 homozygot trolig", "description": "Två kopior av skyddande e2"}
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Se full APOE-genotyp", "dose": "Varierar", "reason": "Beror på rs429358"}],
            "CT": [{"nutrient": "Standard", "dose": "Standard", "reason": "e2 är skyddande"}],
            "TT": [{"nutrient": "Standard", "dose": "Standard", "reason": "e2/e2 är skyddande, OBS risk för typ III hyperlipidemi"}]
        },
        lifestyle_recommendations={
            "CC": ["Se full APOE-genotyp"],
            "CT": ["Standardrekommendationer, e2 skyddar"],
            "TT": ["OBS: Risk för typ III hyperlipidemi vid högt fettintag", "Balanserat fettintag"]
        },
        drug_interactions={},
        pathways=["Lipidmetabolism"],
        interacts_with=["rs429358"],
        haplotype_gene="APOE",
        haplotype_role="Avgör Arg158Cys position för APOE-isoform",
        frequencies={"EUR": 0.08, "EAS": 0.10, "AFR": 0.12, "SAS": 0.06},
        pmids=["31727829", "23571587"],
        clinical_significance="APOE rs7412 är den andra SNP som bestämmer APOE-genotyp. T-allelen definierar e2-allelen som generellt är skyddande.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # VITAMIN D - VDR, CYP2R1
    # =========================================================================

    "rs2228570": UnifiedSNP(
        rsid="rs2228570",
        gene="VDR",
        chromosome="12",
        position=47879112,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.VITAMIN_D, Category.BONE_HEALTH, Category.IMMUNE],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal VDR (F/F)", "description": "Standardlängd receptor"},
            "GA": {"risk": RiskLevel.NORMAL, "effect": "Intermediär (F/f)", "description": "En kort och en standardreceptor"},
            "AA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Kort VDR (f/f)", "description": "Kortare, potentiellt mer aktiv receptor, kan behöva högre D-vitamin"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "D3", "dose": "1000-2000 IE/dag", "reason": "Standardbehov"}],
            "GA": [{"nutrient": "D3", "dose": "2000-3000 IE/dag", "reason": "Något ökat behov"}],
            "AA": [
                {"nutrient": "D3", "dose": "3000-5000 IE/dag", "reason": "Högre behov, mål >75 nmol/L"},
                {"nutrient": "K2 (MK-7)", "dose": "100-200 mcg/dag", "reason": "Dirigerar kalcium rätt"},
                {"nutrient": "Magnesium", "dose": "300-400 mg/dag", "reason": "D-vitamin-kofaktor"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Solexponering 15-20 min/dag"],
            "GA": ["Solexponering", "Överväg tillskott vintertid"],
            "AA": ["Regelbunden solexponering", "D-vitamintillskott året runt", "Kontrollera nivåer regelbundet"]
        },
        drug_interactions={},
        pathways=["D-vitaminmetabolism", "Kalciumhomeostas", "Immunreglering"],
        interacts_with=["rs10741657"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.40, "EAS": 0.55, "AFR": 0.25, "SAS": 0.35},
        pmids=["25051316", "23601626"],
        clinical_significance="VDR FokI påverkar receptorlängd och funktion. f-allelen ger kortare receptor som kan vara mer aktiv.",
        evidence_level="Moderate"
    ),

    "rs10741657": UnifiedSNP(
        rsid="rs10741657",
        gene="CYP2R1",
        chromosome="11",
        position=14913575,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.VITAMIN_D],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal 25-hydroxylering", "description": "Standard D-vitaminaktivering"},
            "GA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Lätt reducerad", "description": "Något lägre 25(OH)D"},
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Reducerad hydroxylering", "description": "Lägre 25(OH)D-nivåer trots normalt intag"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "D3", "dose": "1000-2000 IE/dag", "reason": "Standard"}],
            "GA": [{"nutrient": "D3", "dose": "2000-3000 IE/dag", "reason": "Kompensera för reducerad aktivering"}],
            "AA": [
                {"nutrient": "D3", "dose": "3000-5000 IE/dag", "reason": "Behöver högre dos för adekvata nivåer"},
                {"nutrient": "Kontrollera nivåer", "dose": "Regelbundet", "reason": "Individualisera dos"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Standardsolexponering"],
            "GA": ["Ökad solexponering eller tillskott"],
            "AA": ["Tillskott sannolikt nödvändigt", "Regelbunden nivåkontroll"]
        },
        drug_interactions={},
        pathways=["D-vitaminmetabolism"],
        interacts_with=["rs2228570"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.40, "EAS": 0.60, "AFR": 0.10, "SAS": 0.30},
        pmids=["20541252", "23601626"],
        clinical_significance="CYP2R1 aktiverar D-vitamin till 25(OH)D. Varianter kan leda till lägre nivåer trots adekvat intag.",
        evidence_level="Moderate"
    ),

    # =========================================================================
    # CAFFEINE - CYP1A2
    # =========================================================================

    "rs762551": UnifiedSNP(
        rsid="rs762551",
        gene="CYP1A2",
        chromosome="15",
        position=74749576,
        ref_allele="C",
        alt_allele="A",
        categories=[Category.CAFFEINE, Category.DETOX_PHASE1],
        genotype_effects={
            "AA": {"risk": RiskLevel.NORMAL, "effect": "Snabb koffeinmetabolism (*1A/*1A)", "description": "Kaffe ger kortare effekt, kan tolerera mer"},
            "AC": {"risk": RiskLevel.NORMAL, "effect": "Intermediär metabolism", "description": "Normal koffeinkänslighet"},
            "CC": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Långsam metabolism (*1F/*1F)", "description": "Koffein stannar längre, ökad hjärt-kärlrisk vid högt intag"}
        },
        nutrient_recommendations={
            "AA": [{"nutrient": "Koffein", "dose": "Kan tolerera 400+ mg/dag", "reason": "Snabb nedbrytning"}],
            "AC": [{"nutrient": "Koffein", "dose": "Max 300-400 mg/dag", "reason": "Normal metabolism"}],
            "CC": [
                {"nutrient": "Begränsa koffein", "dose": "Max 100-200 mg/dag", "reason": "Långsam nedbrytning, ökad hjärtrisk"},
                {"nutrient": "L-theanin", "dose": "100-200 mg med kaffe", "reason": "Balanserar koffeineffekt"}
            ]
        },
        lifestyle_recommendations={
            "AA": ["Kan njuta av kaffe utan problem", "Observera att effekten är kortare"],
            "AC": ["Måttligt kaffeintag (2-3 koppar/dag)"],
            "CC": [
                "BEGRÄNSA kaffe till 1-2 koppar/dag",
                "Undvik kaffe efter lunch (sömnpåverkan)",
                "Ökad risk för hjärtinfarkt vid >3 koppar/dag"
            ]
        },
        drug_interactions={
            "CC": [
                {"drug": "Teofyllin", "action": "Förlängd effekt", "note": "Dosreduktion kan behövas"},
                {"drug": "Klozapin", "action": "Ökade nivåer", "note": "CYP1A2-substrat"}
            ]
        },
        pathways=["CYP450 Fas I Detox"],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.68, "EAS": 0.65, "AFR": 0.40, "SAS": 0.55},
        pmids=["16522833", "18180400"],
        clinical_significance="CYP1A2 -163C>A avgör koffeinmetabolismhastighet. Långsamma metaboliserare har ökad risk för hjärt-kärlsjukdom vid högt kaffeintag.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # INFLAMMATION - IL-6, TNF, CRP
    # =========================================================================

    "rs1800795": UnifiedSNP(
        rsid="rs1800795",
        gene="IL6",
        chromosome="7",
        position=22727026,
        ref_allele="G",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Lägre IL-6", "description": "Normal inflammatorisk respons"},
            "GC": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Intermediär IL-6", "description": "Måttlig inflammatorisk benägenhet"},
            "CC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Högre IL-6", "description": "Ökad pro-inflammatorisk benägenhet"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "Omega-3", "dose": "1-2 g/dag", "reason": "Underhåll"}],
            "GC": [
                {"nutrient": "Omega-3", "dose": "2-3 g/dag", "reason": "Anti-inflammatoriskt"},
                {"nutrient": "Vitamin D", "dose": "2000-3000 IE/dag", "reason": "Immunmodulerande"}
            ],
            "CC": [
                {"nutrient": "Omega-3 (EPA)", "dose": "2-4 g EPA/dag", "reason": "KRITISKT anti-inflammatoriskt"},
                {"nutrient": "Curcumin", "dose": "1000-2000 mg/dag", "reason": "Hämmar IL-6"},
                {"nutrient": "Vitamin D", "dose": "3000-5000 IE/dag", "reason": "Sänker IL-6"},
                {"nutrient": "Quercetin", "dose": "500-1000 mg/dag", "reason": "NF-kB-hämmare"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Standardkost"],
            "GC": ["Anti-inflammatorisk kost", "Undvik raffinerat socker"],
            "CC": [
                "Anti-inflammatorisk kost OBLIGATORISKT",
                "Eliminera raffinerade kolhydrater och socker",
                "Minska omega-6, öka omega-3",
                "Regelbunden motion (sänker kronisk IL-6)",
                "Stresshantering (kortisol ökar IL-6)"
            ]
        },
        drug_interactions={},
        pathways=["Inflammation", "Cytokinproduktion"],
        interacts_with=["rs1800629", "rs174546"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.42, "EAS": 0.01, "AFR": 0.05, "SAS": 0.15},
        pmids=["26567432", "15673800"],
        clinical_significance="IL-6 -174G>C påverkar IL-6-produktion. C-allelen ger högre IL-6 och ökad inflammatorisk benägenhet.",
        evidence_level="Strong"
    ),

    "rs1800629": UnifiedSNP(
        rsid="rs1800629",
        gene="TNF",
        chromosome="6",
        position=31543031,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal TNF-alfa", "description": "Standard inflammatorisk respons"},
            "GA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Förhöjd TNF-alfa", "description": "Ökad inflammatorisk benägenhet"},
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Hög TNF-alfa", "description": "Kraftigt ökad pro-inflammatorisk benägenhet"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "GA": [
                {"nutrient": "Omega-3", "dose": "2-3 g/dag", "reason": "Sänker TNF"},
                {"nutrient": "Curcumin", "dose": "500-1000 mg/dag", "reason": "TNF-hämmare"}
            ],
            "AA": [
                {"nutrient": "Omega-3 (EPA)", "dose": "3-4 g/dag", "reason": "KRITISKT för TNF-kontroll"},
                {"nutrient": "Curcumin", "dose": "1000-2000 mg/dag", "reason": "Potent TNF-hämmare"},
                {"nutrient": "Resveratrol", "dose": "250-500 mg/dag", "reason": "Anti-inflammatoriskt"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Standardrekommendationer"],
            "GA": ["Anti-inflammatorisk kost"],
            "AA": [
                "Strikt anti-inflammatorisk kost",
                "Undvik alkohol (ökar TNF)",
                "Viktkontroll (fettväv producerar TNF)",
                "Regelbunden motion"
            ]
        },
        drug_interactions={},
        pathways=["Inflammation", "Cytokinproduktion", "NF-kB-signalering"],
        interacts_with=["rs1800795"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.15, "EAS": 0.03, "AFR": 0.12, "SAS": 0.08},
        pmids=["15673800", "26567432"],
        clinical_significance="TNF -308G>A påverkar TNF-alfa-produktion. A-allelen ger högre TNF och ökad inflammatorisk benägenhet.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # OMEGA-3 / FADS - Fatty acid metabolism
    # =========================================================================

    "rs174546": UnifiedSNP(
        rsid="rs174546",
        gene="FADS1",
        chromosome="11",
        position=61569830,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.OMEGA3, Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "Hög desaturas-aktivitet", "description": "Effektiv ALA->EPA konvertering, men även AA-produktion"},
            "CT": {"risk": RiskLevel.NORMAL, "effect": "Intermediär", "description": "Måttlig konvertering"},
            "TT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Låg desaturas-aktivitet", "description": "Dålig konvertering, behöver preformerad EPA/DHA"}
        },
        nutrient_recommendations={
            "CC": [
                {"nutrient": "Omega-3 (EPA/DHA)", "dose": "1-2 g/dag", "reason": "Kan konvertera men direkt EPA fördelaktigt"},
                {"nutrient": "Minska Omega-6", "dose": "Begränsa", "reason": "Hög konvertering ger även AA"}
            ],
            "CT": [
                {"nutrient": "Omega-3 (EPA/DHA)", "dose": "2-3 g/dag", "reason": "Kan inte förlita sig på konvertering"}
            ],
            "TT": [
                {"nutrient": "Omega-3 (EPA/DHA) direkt", "dose": "2-4 g/dag", "reason": "MÅSTE ha preformerad EPA/DHA"},
                {"nutrient": "ALA (linfröolja)", "dose": "Ineffektiv", "reason": "Konverteras inte tillräckligt"}
            ]
        },
        lifestyle_recommendations={
            "CC": ["Balansera omega-6/omega-3", "Minska vegetabiliska oljor"],
            "CT": ["Fisk 2-3 ggr/vecka eller tillskott"],
            "TT": [
                "Fisk 3-4 ggr/vecka ELLER dagligt tillskott",
                "Vegetarianer MÅSTE ta algolja",
                "ALA-källor (linfrö, valnötter) räcker INTE"
            ]
        },
        drug_interactions={},
        pathways=["Fettsyrametabolism", "Eikosanoidsyntes"],
        interacts_with=["rs1800795"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.33, "EAS": 0.62, "AFR": 0.02, "SAS": 0.25},
        pmids=["20194237", "18936471"],
        clinical_significance="FADS1 rs174546 påverkar delta-5-desaturasaktivitet som konverterar DGLA till AA och EPA till DHA.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # DETOX PHASE 1 - CYP450 enzymes
    # =========================================================================

    "rs1056836": UnifiedSNP(
        rsid="rs1056836",
        gene="CYP1B1",
        chromosome="2",
        position=38070683,
        ref_allele="C",
        alt_allele="G",
        categories=[Category.DETOX_PHASE1, Category.HORMONE],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "Normal CYP1B1 (Leu/Leu)", "description": "Standard östrogenhydroxylering"},
            "CG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Ökad aktivitet (Leu/Val)", "description": "Mer 4-OH-östrogen"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Hög aktivitet (Val/Val)", "description": "Hög 4-OH-östrogen (genotoxisk)"}
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "CG": [
                {"nutrient": "DIM (Diindolylmethane)", "dose": "100-200 mg/dag", "reason": "Skiftar till 2-OH-väg"}
            ],
            "GG": [
                {"nutrient": "DIM", "dose": "200-300 mg/dag", "reason": "KRITISKT för att minska 4-OH"},
                {"nutrient": "Sulforafan", "dose": "20-50 mg/dag", "reason": "Inducerar fas II för 4-OH-konjugering"},
                {"nutrient": "Resveratrol", "dose": "250-500 mg/dag", "reason": "Hämmar CYP1B1"}
            ]
        },
        lifestyle_recommendations={
            "CC": ["Standardkost med korsblommiga"],
            "CG": ["Korsblommiga grönsaker dagligen"],
            "GG": [
                "Korsblommiga grönsaker DAGLIGEN (broccoli, blomkål, kål)",
                "Undvik xenoöstrogener (plast, pesticider)",
                "Överväg östrogenmetabolit-test",
                "Diskutera HRT försiktigt med läkare"
            ]
        },
        drug_interactions={
            "GG": [
                {"drug": "HRT", "action": "Försiktighet", "note": "Ökad 4-OH-östrogen produktion"}
            ]
        },
        pathways=["CYP450 Fas I Detox", "Östrogenmetabolism"],
        interacts_with=["rs4680"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.40, "EAS": 0.15, "AFR": 0.65, "SAS": 0.30},
        pmids=["23295013", "16825041"],
        clinical_significance="CYP1B1 Leu432Val påverkar östrogen 4-hydroxylering. Val-allelen producerar mer genotoxisk 4-OH-östrogen.",
        evidence_level="Moderate"
    ),

    # =========================================================================
    # DETOX PHASE 2 - GST, NAT2, NQO1
    # =========================================================================

    "rs1695": UnifiedSNP(
        rsid="rs1695",
        gene="GSTP1",
        chromosome="11",
        position=67352689,
        ref_allele="A",
        alt_allele="G",
        categories=[Category.DETOX_PHASE2, Category.ANTIOXIDANT],
        genotype_effects={
            "AA": {"risk": RiskLevel.NORMAL, "effect": "Normal GSTP1 (Ile/Ile)", "description": "Standard glutationkonjugering"},
            "AG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Reducerad (Ile/Val)", "description": "Måttligt reducerad aktivitet"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Låg aktivitet (Val/Val)", "description": "Reducerad detox av vissa substrat"}
        },
        nutrient_recommendations={
            "AA": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "AG": [{"nutrient": "NAC", "dose": "600-1200 mg/dag", "reason": "Glutationstöd"}],
            "GG": [
                {"nutrient": "NAC", "dose": "1200-1800 mg/dag", "reason": "Kompensera för reducerad GST"},
                {"nutrient": "Liposomalt Glutation", "dose": "250-500 mg/dag", "reason": "Direkt glutationstöd"},
                {"nutrient": "Alpha-liponsyra", "dose": "300-600 mg/dag", "reason": "Regenererar glutation"}
            ]
        },
        lifestyle_recommendations={
            "AA": ["Standardrekommendationer"],
            "AG": ["Undvik onödig kemikalieexponering"],
            "GG": [
                "Minimera exponering för bekämpningsmedel",
                "Ät ekologiskt där möjligt",
                "Undvik rökning och passiv rökning"
            ]
        },
        drug_interactions={},
        pathways=["Glutationkonjugering", "Fas II Detox"],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.32, "EAS": 0.18, "AFR": 0.45, "SAS": 0.25},
        pmids=["17408518"],
        clinical_significance="GSTP1 Ile105Val påverkar glutationtransferas-aktivitet, viktigt för detox av elektrofila toxiner.",
        evidence_level="Moderate"
    ),

    "rs1800566": UnifiedSNP(
        rsid="rs1800566",
        gene="NQO1",
        chromosome="16",
        position=69711242,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.DETOX_PHASE2, Category.ANTIOXIDANT],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "Normal NQO1", "description": "Fungerande quinonreduktas"},
            "CT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Reducerad (Heterozygot *2)", "description": "Instabilt protein"},
            "TT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "Ingen NQO1 (*2/*2)", "description": "Protein degraderas, ingen skydd mot quinoner"}
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "CT": [
                {"nutrient": "Riboflavin (B2)", "dose": "25-50 mg/dag", "reason": "FAD-kofaktor för NQO1"}
            ],
            "TT": [
                {"nutrient": "Riboflavin", "dose": "50-100 mg/dag", "reason": "Kan stabilisera kvarvarande protein"},
                {"nutrient": "Vitamin C", "dose": "1000-2000 mg/dag", "reason": "Alternativ quinon-reduktion"},
                {"nutrient": "NAC", "dose": "600-1200 mg/dag", "reason": "Antioxidantskydd"}
            ]
        },
        lifestyle_recommendations={
            "CC": ["Standardrekommendationer"],
            "CT": ["Minska quinonexponering"],
            "TT": [
                "Undvik bensendrivna kemikalier",
                "Försiktighet med paracetamol (producerar quinoner)",
                "Antioxidantrik kost"
            ]
        },
        drug_interactions={
            "TT": [
                {"drug": "Benzen-exponering", "action": "Ökad toxicitet", "note": "Yrkesrelaterad risk"},
                {"drug": "Vissa cytostatika", "action": "Ökad toxicitet", "note": "Quinon-baserade läkemedel"}
            ]
        },
        pathways=["Quinonreduktion", "Fas II Detox"],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.22, "EAS": 0.45, "AFR": 0.12, "SAS": 0.30},
        pmids=["23147091"],
        clinical_significance="NQO1 *2 (Pro187Ser) gör proteinet instabilt. Homozygota *2/*2 saknar NQO1-funktion.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # PHARMACOGENOMICS - CYP2D6
    # =========================================================================

    "rs3892097": UnifiedSNP(
        rsid="rs3892097",
        gene="CYP2D6",
        chromosome="22",
        position=42128945,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.PHARMACOGENOMICS, Category.DETOX_PHASE1],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "Normal CYP2D6 (*1/*1)", "description": "Fungerande enzym"},
            "CT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Heterozygot *4", "description": "Intermediär metaboliserare"},
            "TT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "CYP2D6 *4/*4", "description": "POOR METABOLIZER - Null enzym"}
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "CT": [{"nutrient": "Standard", "dose": "Standard", "reason": "Intermediär funktion"}],
            "TT": [{"nutrient": "Standard", "dose": "Standard", "reason": "Ingen specifik näringspåverkan, MEN läkemedelsdosering kritisk"}]
        },
        lifestyle_recommendations={
            "CC": ["Standardrekommendationer"],
            "CT": ["Informera läkare om CYP2D6-status"],
            "TT": [
                "KRITISKT: Informera ALLTID läkare",
                "Bär farmakogenetiskt kort",
                "Undvik prodrugs som kräver CYP2D6-aktivering"
            ]
        },
        drug_interactions={
            "CT": [
                {"drug": "Kodein", "action": "Reducerad effekt", "note": "Minskad morfinbildning"},
                {"drug": "Tamoxifen", "action": "Reducerad effekt", "note": "Minskad endoxifen"}
            ],
            "TT": [
                {"drug": "Kodein", "action": "INEFFEKTIVT", "note": "Ingen morfinbildning"},
                {"drug": "Tramadol", "action": "INEFFEKTIVT", "note": "Ingen O-demetylering"},
                {"drug": "Tamoxifen", "action": "INEFFEKTIVT", "note": "Överväg alternativ"},
                {"drug": "Antidepressiva (vissa)", "action": "Ökad toxicitet", "note": "Sänkt dos behövs"},
                {"drug": "Metoprolol", "action": "Ökade nivåer", "note": "Risk för bradykardi"}
            ]
        },
        pathways=["CYP450 Fas I Detox", "Läkemedelsmetabolism"],
        interacts_with=["rs35599367"],
        haplotype_gene="CYP2D6",
        haplotype_role="*4 allele - splice defect, null allele",
        frequencies={"EUR": 0.22, "EAS": 0.01, "AFR": 0.06, "SAS": 0.08},
        pmids=["26465333", "28002639"],
        clinical_significance="CYP2D6*4 är den vanligaste null-allelen hos européer. Homozygota saknar CYP2D6-aktivitet.",
        evidence_level="Strong"
    ),

    "rs1065852": UnifiedSNP(
        rsid="rs1065852",
        gene="CYP2D6",
        chromosome="22",
        position=42130692,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "Normal CYP2D6", "description": "Fungerande enzym"},
            "CT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Heterozygot *10", "description": "Reducerad men ej null"},
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "CYP2D6 *10/*10", "description": "Kraftigt reducerad aktivitet (vanligt i Asien)"}
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "CT": [{"nutrient": "Standard", "dose": "Standard", "reason": "Intermediär funktion"}],
            "TT": [{"nutrient": "Standard", "dose": "Standard", "reason": "Läkemedelsdosering kritisk"}]
        },
        lifestyle_recommendations={
            "CC": ["Standardrekommendationer"],
            "CT": ["Informera läkare"],
            "TT": ["Informera läkare om CYP2D6-status", "Dosanpassning kan behövas"]
        },
        drug_interactions={
            "TT": [
                {"drug": "Kodein", "action": "Reducerad effekt", "note": "Lägre morfinbildning"},
                {"drug": "CYP2D6-substrat", "action": "Ökade nivåer", "note": "Dosreduktion kan behövas"}
            ]
        },
        pathways=["CYP450 Fas I Detox"],
        interacts_with=["rs3892097"],
        haplotype_gene="CYP2D6",
        haplotype_role="*10 allele - Pro34Ser, reducerad men ej null",
        frequencies={"EUR": 0.02, "EAS": 0.45, "AFR": 0.08, "SAS": 0.15},
        pmids=["26465333", "28002639"],
        clinical_significance="CYP2D6*10 ger reducerad men inte null aktivitet. Vanligaste nedsatta allelen i Ostasien.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # PHARMACOGENOMICS - CYP2C19
    # =========================================================================

    "rs4244285": UnifiedSNP(
        rsid="rs4244285",
        gene="CYP2C19",
        chromosome="10",
        position=94781859,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal CYP2C19 (*1)", "description": "Fungerande enzym"},
            "GA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Heterozygot *2", "description": "Intermediär metaboliserare"},
            "AA": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "CYP2C19 *2/*2", "description": "POOR METABOLIZER"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "GA": [{"nutrient": "Standard", "dose": "Standard", "reason": "Informera läkare"}],
            "AA": [{"nutrient": "Standard", "dose": "Standard", "reason": "Läkemedelsdosering kritisk"}]
        },
        lifestyle_recommendations={
            "GG": ["Standardrekommendationer"],
            "GA": ["Informera läkare"],
            "AA": ["KRITISKT: Informera läkare", "Särskilt viktigt vid hjärtsjukdom och PPI-användning"]
        },
        drug_interactions={
            "GA": [
                {"drug": "Clopidogrel", "action": "Reducerad effekt", "note": "Överväg alternativ"},
                {"drug": "PPI", "action": "Förlängd effekt", "note": "Dosreduktion kan behövas"}
            ],
            "AA": [
                {"drug": "Clopidogrel", "action": "TERAPISVIKT", "note": "CPIC rekommenderar alternativ (prasugrel, ticagrelor)"},
                {"drug": "PPI (omeprazol etc)", "action": "Kraftigt förlängd effekt", "note": "Lägre dos eller alternativ"},
                {"drug": "Escitalopram/Citalopram", "action": "Ökade nivåer", "note": "Dosreduktion rekommenderas"}
            ]
        },
        pathways=["CYP450 Fas I Detox"],
        interacts_with=["rs12248560"],
        haplotype_gene="CYP2C19",
        haplotype_role="*2 allele - splice defect, null",
        frequencies={"EUR": 0.15, "EAS": 0.30, "AFR": 0.17, "SAS": 0.35},
        pmids=["26465333", "21716271"],
        clinical_significance="CYP2C19*2 är en null-allel. Kritisk för clopidogrel-aktivering och PPI-metabolism.",
        evidence_level="Strong"
    ),

    "rs12248560": UnifiedSNP(
        rsid="rs12248560",
        gene="CYP2C19",
        chromosome="10",
        position=94761900,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "Normal CYP2C19", "description": "Standard aktivitet"},
            "CT": {"risk": RiskLevel.NORMAL, "effect": "Rapid metabolizer (*17)", "description": "Ökad enzymaktivitet"},
            "TT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Ultra-rapid (*17/*17)", "description": "Mycket snabb metabolism"}
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "CT": [{"nutrient": "Standard", "dose": "Standard", "reason": "Snabbare metabolism"}],
            "TT": [{"nutrient": "Standard", "dose": "Standard", "reason": "Mycket snabb metabolism"}]
        },
        lifestyle_recommendations={
            "CC": ["Standardrekommendationer"],
            "CT": ["Informera läkare"],
            "TT": ["Informera läkare", "Kan behöva högre doser av vissa läkemedel"]
        },
        drug_interactions={
            "CT": [
                {"drug": "Clopidogrel", "action": "Ökad effekt", "note": "Ökad blödningsrisk"},
                {"drug": "PPI", "action": "Reducerad effekt", "note": "Kan behöva högre dos"}
            ],
            "TT": [
                {"drug": "Clopidogrel", "action": "Kraftigt ökad effekt", "note": "Blödningsrisk"},
                {"drug": "PPI", "action": "Ineffektiva", "note": "Överväg alternativ syrahämmare"}
            ]
        },
        pathways=["CYP450 Fas I Detox"],
        interacts_with=["rs4244285"],
        haplotype_gene="CYP2C19",
        haplotype_role="*17 allele - ökad transkription",
        frequencies={"EUR": 0.22, "EAS": 0.03, "AFR": 0.18, "SAS": 0.15},
        pmids=["26465333", "21716271"],
        clinical_significance="CYP2C19*17 ger ökad enzymaktivitet. Kan leda till terapisvikt eller ökad toxicitet beroende på läkemedel.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # PHARMACOGENOMICS - CYP2C9, VKORC1 (Warfarin)
    # =========================================================================

    "rs1799853": UnifiedSNP(
        rsid="rs1799853",
        gene="CYP2C9",
        chromosome="10",
        position=94942290,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "Normal CYP2C9 (*1)", "description": "Standard aktivitet"},
            "CT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Heterozygot *2", "description": "Reducerad aktivitet (~70%)"},
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "CYP2C9 *2/*2", "description": "Kraftigt reducerad aktivitet"}
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "CT": [{"nutrient": "Stabil K-vitaminintag", "dose": "Konsekvent", "reason": "Viktigt vid warfarin"}],
            "TT": [{"nutrient": "Stabil K-vitaminintag", "dose": "Konsekvent", "reason": "KRITISKT vid warfarin"}]
        },
        lifestyle_recommendations={
            "CC": ["Standardrekommendationer"],
            "CT": ["Informera läkare", "Stabil kost vid warfarinbehandling"],
            "TT": ["KRITISKT: Informera läkare", "Warfarindosering måste anpassas"]
        },
        drug_interactions={
            "CT": [
                {"drug": "Warfarin", "action": "Reducerad metabolism", "note": "Lägre dos behövs"},
                {"drug": "NSAID", "action": "Ökade nivåer", "note": "Ökad GI-blödningsrisk"}
            ],
            "TT": [
                {"drug": "Warfarin", "action": "Kraftigt reducerad metabolism", "note": "Signifikant dosreduktion (~30%)"},
                {"drug": "NSAID", "action": "Förlängd effekt", "note": "Undvik om möjligt"}
            ]
        },
        pathways=["CYP450 Fas I Detox"],
        interacts_with=["rs1057910", "rs9923231"],
        haplotype_gene="CYP2C9",
        haplotype_role="*2 allele - Arg144Cys",
        frequencies={"EUR": 0.13, "EAS": 0.01, "AFR": 0.03, "SAS": 0.08},
        pmids=["26465333", "28198005"],
        clinical_significance="CYP2C9*2 ger reducerad enzymaktivitet. Viktigt för warfarin- och NSAID-dosering.",
        evidence_level="Strong"
    ),

    "rs9923231": UnifiedSNP(
        rsid="rs9923231",
        gene="VKORC1",
        chromosome="16",
        position=31096368,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal VKORC1", "description": "Standard warfarindos"},
            "GA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Reducerad VKORC1", "description": "Lägre warfarindos behövs"},
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Kraftigt reducerad VKORC1", "description": "Mycket låg warfarindos (~50% av normal)"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "Standard K-vitamin", "dose": "Konsekvent intag", "reason": "Vid warfarin"}],
            "GA": [{"nutrient": "Stabil K-vitaminintag", "dose": "Konsekvent", "reason": "Känsligare för variationer"}],
            "AA": [{"nutrient": "Stabil K-vitaminintag", "dose": "MYCKET konsekvent", "reason": "Extrem warfarinkänslighet"}]
        },
        lifestyle_recommendations={
            "GG": ["Standardrekommendationer vid warfarin"],
            "GA": ["Stabil kost", "Undvik stora variationer i K-vitamin"],
            "AA": ["KRITISKT: Mycket stabil kost", "Informera ALL vårdpersonal"]
        },
        drug_interactions={
            "GA": [
                {"drug": "Warfarin", "action": "Ökad känslighet", "note": "Lägre startdos (~25% reduktion)"}
            ],
            "AA": [
                {"drug": "Warfarin", "action": "Extrem känslighet", "note": "50% eller lägre dos, täta INR-kontroller"}
            ]
        },
        pathways=["K-vitamin-cykel", "Koagulation"],
        interacts_with=["rs1799853", "rs1057910"],
        haplotype_gene="VKORC1",
        haplotype_role="Promotorvariant - påverkar expression",
        frequencies={"EUR": 0.40, "EAS": 0.90, "AFR": 0.10, "SAS": 0.30},
        pmids=["26465333", "28198005"],
        clinical_significance="VKORC1 -1639G>A är den viktigaste genetiska faktorn för warfarinkänslighet.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # SLCO1B1 - Statin metabolism
    # =========================================================================

    "rs4149056": UnifiedSNP(
        rsid="rs4149056",
        gene="SLCO1B1",
        chromosome="12",
        position=21176804,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.PHARMACOGENOMICS, Category.CARDIOVASCULAR],
        genotype_effects={
            "TT": {"risk": RiskLevel.NORMAL, "effect": "Normal SLCO1B1 (*1a)", "description": "Standard statintransport"},
            "TC": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Reducerad (*5 het)", "description": "Intermediär statintransport"},
            "CC": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "SLCO1B1 *5/*5", "description": "Kraftigt reducerad transport, hög myopatirisk"}
        },
        nutrient_recommendations={
            "TT": [{"nutrient": "CoQ10", "dose": "100-200 mg/dag", "reason": "Stödjer vid statinbehandling"}],
            "TC": [
                {"nutrient": "CoQ10", "dose": "100-200 mg/dag", "reason": "Kompenserar statineffekt"}
            ],
            "CC": [
                {"nutrient": "CoQ10", "dose": "200-300 mg/dag", "reason": "KRITISKT vid statinbehandling"},
                {"nutrient": "Vitamin D", "dose": "Kontrollera nivå", "reason": "Associerat med myopati"}
            ]
        },
        lifestyle_recommendations={
            "TT": ["Standardrekommendationer"],
            "TC": ["Informera läkare", "Rapportera muskelsymtom"],
            "CC": [
                "KRITISKT: Informera läkare",
                "Undvik simvastatin >20 mg",
                "Rapportera ALLA muskelsymtom",
                "Alternativa statiner kan vara säkrare"
            ]
        },
        drug_interactions={
            "TC": [
                {"drug": "Simvastatin", "action": "Ökad myopatirisk", "note": "Max 20 mg/dag"},
                {"drug": "Atorvastatin", "action": "Försiktighet", "note": "Lägre dos"}
            ],
            "CC": [
                {"drug": "Simvastatin", "action": "HÖG myopatirisk", "note": "UNDVIK eller max 10 mg"},
                {"drug": "Atorvastatin", "action": "Ökad risk", "note": "Överväg pravastatin/rosuvastatin"}
            ]
        },
        pathways=["Hepatisk läkemedelstransport"],
        interacts_with=[],
        haplotype_gene="SLCO1B1",
        haplotype_role="*5 allele - Val174Ala",
        frequencies={"EUR": 0.15, "EAS": 0.12, "AFR": 0.02, "SAS": 0.08},
        pmids=["26465333", "22617227"],
        clinical_significance="SLCO1B1*5 reducerar hepatisk uptag av statiner, vilket ökar plasmakoncentration och myopatirisk.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # CIRCADIAN / SLEEP
    # =========================================================================

    "rs1801260": UnifiedSNP(
        rsid="rs1801260",
        gene="CLOCK",
        chromosome="4",
        position=56296055,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.SLEEP, Category.CIRCADIAN],
        genotype_effects={
            "TT": {"risk": RiskLevel.NORMAL, "effect": "Normal CLOCK", "description": "Standard dygnsrytm"},
            "TC": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Intermediär", "description": "Tendens till kvällsmänniska"},
            "CC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Kvällskronotyp", "description": "Kvällsmänniska, sämre sömnkvalitet"}
        },
        nutrient_recommendations={
            "TT": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal rytm"}],
            "TC": [{"nutrient": "Melatonin", "dose": "0.5-1 mg vid behov", "reason": "Stödjer insomning"}],
            "CC": [
                {"nutrient": "Melatonin", "dose": "0.5-3 mg", "reason": "Hjälper skifta rytm tidigare"},
                {"nutrient": "Magnesium", "dose": "300-400 mg kväll", "reason": "Stödjer sömn"},
                {"nutrient": "Glycin", "dose": "3 g före sömn", "reason": "Förbättrar sömnkvalitet"}
            ]
        },
        lifestyle_recommendations={
            "TT": ["Standardsömnhygien"],
            "TC": ["Regelbundna sömntider"],
            "CC": [
                "Morgonljus KRITISKT för att skifta rytm",
                "Undvik blått ljus kvällstid",
                "Konsekvent sömnschema även helger",
                "Undvik koffein efter lunch"
            ]
        },
        drug_interactions={},
        pathways=["Dygnsrytm", "Circadian klocka"],
        interacts_with=["rs57875989"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.28, "EAS": 0.10, "AFR": 0.15},
        pmids=["25349248", "23680664"],
        clinical_significance="CLOCK 3111T>C associeras med kvällskronotyp och sömnproblem.",
        evidence_level="Moderate"
    ),

    # =========================================================================
    # HISTAMINE - AOC1/DAO
    # =========================================================================

    "rs10156191": UnifiedSNP(
        rsid="rs10156191",
        gene="AOC1",
        chromosome="7",
        position=150547296,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.HISTAMINE],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "Normal DAO", "description": "Adekvat histaminnedbrytning"},
            "CT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Reducerad DAO", "description": "Måttligt nedsatt histaminnedbrytning"},
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Låg DAO-aktivitet", "description": "Histaminintolerans möjlig"}
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "CT": [{"nutrient": "Vitamin C", "dose": "500-1000 mg/dag", "reason": "Stödjer DAO"}],
            "TT": [
                {"nutrient": "DAO-tillskott", "dose": "Före histaminrika måltider", "reason": "Ersättningsterapi"},
                {"nutrient": "Vitamin C", "dose": "1000-2000 mg/dag", "reason": "DAO-kofaktor"},
                {"nutrient": "Vitamin B6", "dose": "25-50 mg/dag", "reason": "DAO-kofaktor"},
                {"nutrient": "Quercetin", "dose": "500-1000 mg/dag", "reason": "Mastcellstabilisator"}
            ]
        },
        lifestyle_recommendations={
            "CC": ["Standardkost"],
            "CT": ["Måttlighet med histaminrika livsmedel"],
            "TT": [
                "Låghistaminkost rekommenderas",
                "Undvik lagrade ostar, fermenterad mat, vin",
                "Färska livsmedel är bäst",
                "Ät fisk färsk eller djupfryst"
            ]
        },
        drug_interactions={
            "TT": [
                {"drug": "NSAID", "action": "Förvärrar histaminintolerans", "note": "Hämmar DAO"},
                {"drug": "Alkohol", "action": "Förvärrar", "note": "Hämmar DAO och innehåller histamin"}
            ]
        },
        pathways=["Histaminnedbrytning"],
        interacts_with=["rs1049793"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.20, "EAS": 0.10, "AFR": 0.15},
        pmids=["17490952"],
        clinical_significance="AOC1/DAO varianter kan orsaka histaminintolerans med symtom som huvudvärk, urtikaria, GI-besvär.",
        evidence_level="Moderate"
    ),

    # =========================================================================
    # ANTIOXIDANT - SOD2
    # =========================================================================

    "rs4880": UnifiedSNP(
        rsid="rs4880",
        gene="SOD2",
        chromosome="6",
        position=159692840,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.ANTIOXIDANT],
        genotype_effects={
            "TT": {"risk": RiskLevel.NORMAL, "effect": "Normal SOD2 (Val/Val)", "description": "Standard mitokondriell antioxidant"},
            "TC": {"risk": RiskLevel.NORMAL, "effect": "Intermediär (Val/Ala)", "description": "Balanserad funktion"},
            "CC": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Ala/Ala - Effektivare import men...", "description": "Kan öka oxidativ stress under vissa förhållanden"}
        },
        nutrient_recommendations={
            "TT": [{"nutrient": "Mangan", "dose": "2-5 mg/dag", "reason": "SOD2-kofaktor"}],
            "TC": [{"nutrient": "Antioxidantkomplex", "dose": "Standard", "reason": "Balanserat stöd"}],
            "CC": [
                {"nutrient": "Mangan", "dose": "2-5 mg/dag", "reason": "Kritisk SOD2-kofaktor"},
                {"nutrient": "Vitamin E", "dose": "200-400 IE/dag", "reason": "Membranantioxidant"},
                {"nutrient": "CoQ10", "dose": "100-200 mg/dag", "reason": "Mitokondriellt stöd"},
                {"nutrient": "Alpha-liponsyra", "dose": "300-600 mg/dag", "reason": "Mitokondriell antioxidant"}
            ]
        },
        lifestyle_recommendations={
            "TT": ["Standardrekommendationer"],
            "TC": ["Antioxidantrik kost"],
            "CC": [
                "Antioxidantrik kost VIKTIGT",
                "Undvik överdriven järnbelastning",
                "Motion men undvik extrem överträning"
            ]
        },
        drug_interactions={},
        pathways=["Antioxidantförsvar", "Mitokondriefunktion"],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.47, "EAS": 0.14, "AFR": 0.30},
        pmids=["25514928"],
        clinical_significance="SOD2 Ala16Val påverkar mitokondriell superoxiddismutas. Komplex genetik med paradoxala effekter.",
        evidence_level="Moderate"
    ),

    # =========================================================================
    # IRON / HFE
    # =========================================================================

    "rs1800562": UnifiedSNP(
        rsid="rs1800562",
        gene="HFE",
        chromosome="6",
        position=26092913,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.IRON],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal HFE", "description": "Standard järnreglering"},
            "GA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Heterozygot C282Y", "description": "Bärare, lätt ökad järnabsorption"},
            "AA": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "Homozygot C282Y", "description": "Hereditär hemokromatos - järnöverskott"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "Järn", "dose": "Vid behov", "reason": "Normal reglering"}],
            "GA": [{"nutrient": "Undvik järntillskott", "dose": "Om ej brist", "reason": "Ökad absorption"}],
            "AA": [
                {"nutrient": "INGET järntillskott", "dose": "KONTRAINDICERAT", "reason": "Risk för järnöverskott"},
                {"nutrient": "Undvik C-vitamin till måltid", "dose": "Separera", "reason": "Ökar järnabsorption"},
                {"nutrient": "Te/kaffe till måltid", "dose": "Kan hjälpa", "reason": "Minskar järnabsorption"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Standardrekommendationer"],
            "GA": ["Undvik järntillskott utan indikation", "Kontrollera ferritin periodiskt"],
            "AA": [
                "REGELBUNDEN ferritinkontroll",
                "Blodgivning kan vara behandling",
                "Undvik alkohol (leverbelastning)",
                "Undvik rått skaldjur (Vibrio vulnificus-risk)"
            ]
        },
        drug_interactions={
            "AA": [
                {"drug": "Järntillskott", "action": "KONTRAINDICERAT", "note": "Förvärrar järnöverskott"}
            ]
        },
        pathways=["Järnhomeostas"],
        interacts_with=["rs1799945"],
        haplotype_gene="HFE",
        haplotype_role="C282Y mutation - huvudmutation för hemokromatos",
        frequencies={"EUR": 0.06, "EAS": 0.00, "AFR": 0.01},
        pmids=["12461551"],
        clinical_significance="HFE C282Y är huvudorsaken till hereditär hemokromatos. Homozygota har hög risk för järnöverskott.",
        evidence_level="Strong"
    ),

    # =========================================================================
    # BH4 CYCLE
    # =========================================================================

    "rs998259": UnifiedSNP(
        rsid="rs998259",
        gene="GCH1",
        chromosome="14",
        position=54842629,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.BH4_CYCLE, Category.NEUROTRANSMITTER],
        genotype_effects={
            "GG": {"risk": RiskLevel.NORMAL, "effect": "Normal GCH1", "description": "Standard BH4-syntes"},
            "GA": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Reducerad GCH1", "description": "Något lägre BH4-produktion"},
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Låg GCH1", "description": "Reducerad BH4, kan påverka neurotransmittorer"}
        },
        nutrient_recommendations={
            "GG": [{"nutrient": "Standard", "dose": "Standard", "reason": "Normal funktion"}],
            "GA": [
                {"nutrient": "Zink", "dose": "15-30 mg/dag", "reason": "GCH1-kofaktor"},
                {"nutrient": "Folat/B12", "dose": "Aktiva former", "reason": "Indirekt BH4-stöd"}
            ],
            "AA": [
                {"nutrient": "Zink", "dose": "30 mg/dag", "reason": "KRITISK GCH1-kofaktor"},
                {"nutrient": "Vitamin C", "dose": "1000-2000 mg/dag", "reason": "Skyddar BH4 från oxidation"},
                {"nutrient": "Metylfolat + B12", "dose": "Aktiva former", "reason": "Stödjer BH4-regenerering"},
                {"nutrient": "Alpha-liponsyra", "dose": "300-600 mg/dag", "reason": "Antioxidant för BH4"}
            ]
        },
        lifestyle_recommendations={
            "GG": ["Standardrekommendationer"],
            "GA": ["Antioxidantrik kost"],
            "AA": ["Antioxidanter viktigt", "Stresshantering (stress förbrukar BH4)"]
        },
        drug_interactions={},
        pathways=["BH4-cykeln", "Tetrahydrobiopterin-syntes"],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.35, "EAS": 0.20, "AFR": 0.25},
        pmids=["23543003", "20196730"],
        clinical_significance="GCH1 är hastighetsbegränsande för BH4-syntes. Varianter kan påverka neurotransmittorsyntes och smärtkänslighet.",
        evidence_level="Moderate"
    ),

}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_snp(rsid: str) -> Optional[UnifiedSNP]:
    """Hämta en SNP från databasen."""
    return UNIFIED_DATABASE.get(rsid.lower()) or UNIFIED_DATABASE.get(rsid)

def get_all_rsids() -> List[str]:
    """Returnera alla rsids i databasen."""
    return list(UNIFIED_DATABASE.keys())

def get_snps_by_category(category: Category) -> List[UnifiedSNP]:
    """Hämta alla SNPs i en kategori."""
    return [snp for snp in UNIFIED_DATABASE.values() if category in snp.categories]

def get_snps_by_gene(gene: str) -> List[UnifiedSNP]:
    """Hämta alla SNPs för en gen."""
    gene_upper = gene.upper()
    return [snp for snp in UNIFIED_DATABASE.values() if snp.gene.upper() == gene_upper]

def analyze_genotype(rsid: str, genotype: str) -> Optional[Dict[str, Any]]:
    """
    Analysera en genotyp och returnera all relevant information.

    Args:
        rsid: SNP identifierare (t.ex. "rs1801133")
        genotype: Genotyp (t.ex. "AA", "AG", "GG")

    Returns:
        Dict med all analysdata eller None om SNP inte finns
    """
    snp = get_snp(rsid)
    if not snp:
        return None

    # Normalisera genotyp (sortera alleler alfabetiskt för konsistens)
    normalized_gt = "".join(sorted(genotype.upper()))

    # Hitta matchande effekt
    effect_data = snp.genotype_effects.get(normalized_gt)
    if not effect_data:
        # Prova omvänd ordning
        reversed_gt = genotype.upper()[::-1]
        effect_data = snp.genotype_effects.get(reversed_gt)

    if not effect_data:
        return {
            "rsid": rsid,
            "gene": snp.gene,
            "genotype": genotype,
            "status": "Okänd genotyp",
            "categories": [c.value for c in snp.categories]
        }

    return {
        "rsid": rsid,
        "gene": snp.gene,
        "genotype": genotype,
        "risk_level": effect_data.get("risk", RiskLevel.NORMAL).value if isinstance(effect_data.get("risk"), RiskLevel) else str(effect_data.get("risk", "Unknown")),
        "effect": effect_data.get("effect", ""),
        "description": effect_data.get("description", ""),
        "categories": [c.value for c in snp.categories],
        "nutrient_recommendations": snp.nutrient_recommendations.get(normalized_gt, []),
        "lifestyle_recommendations": snp.lifestyle_recommendations.get(normalized_gt, []),
        "drug_interactions": snp.drug_interactions.get(normalized_gt, []),
        "pathways": snp.pathways,
        "interacts_with": snp.interacts_with,
        "clinical_significance": snp.clinical_significance,
        "evidence_level": snp.evidence_level
    }

# =============================================================================
# HAPLOTYPE FUNCTIONS
# =============================================================================

def determine_apoe_genotype(rs429358_gt: str, rs7412_gt: str) -> Dict[str, Any]:
    """
    Bestäm APOE-genotyp från rs429358 och rs7412.

    APOE alleler:
    - e2: T-T (rs429358-rs7412)
    - e3: T-C
    - e4: C-C
    """
    # Räkna alleler
    e4_count = rs429358_gt.upper().count('C')
    e2_count = rs7412_gt.upper().count('T')

    # Bestäm diplotyp
    if e4_count == 2 and e2_count == 0:
        diplotype = "e4/e4"
        risk = "MYCKET HÖG"
        description = "Homozygot e4 - kraftigt ökad risk för Alzheimer och hjärt-kärlsjukdom"
    elif e4_count == 1 and e2_count == 0:
        diplotype = "e3/e4"
        risk = "FÖRHÖJD"
        description = "Heterozygot e4 - ökad risk för Alzheimer"
    elif e4_count == 0 and e2_count == 2:
        diplotype = "e2/e2"
        risk = "LÅG (men OBS typ III)"
        description = "Homozygot e2 - skyddande, men risk för typ III hyperlipidemi"
    elif e4_count == 0 and e2_count == 1:
        diplotype = "e2/e3"
        risk = "LÅG"
        description = "e2-bärare - generellt skyddande"
    elif e4_count == 1 and e2_count == 1:
        diplotype = "e2/e4"
        risk = "KOMPLEX"
        description = "Blandad genotyp - e4-risk delvis kompenserad av e2"
    else:
        diplotype = "e3/e3"
        risk = "NORMAL"
        description = "Vanligaste genotypen, normal risk"

    recommendations = []
    if "e4" in diplotype:
        recommendations = [
            "Medelhavskost rekommenderas starkt",
            "Omega-3 (DHA) 2-4 g/dag",
            "Regelbunden motion (minst 150 min/vecka)",
            "Kognitiv stimulering",
            "Överväg lipidprofil regelbundet"
        ]
    elif "e2/e2" in diplotype:
        recommendations = [
            "Balanserat fettintag",
            "Kontrollera lipider regelbundet (risk typ III)"
        ]

    return {
        "gene": "APOE",
        "diplotype": diplotype,
        "risk_level": risk,
        "description": description,
        "recommendations": recommendations
    }

def determine_mthfr_status(rs1801133_gt: str, rs1801131_gt: str) -> Dict[str, Any]:
    """
    Bestäm MTHFR-status från båda SNPs.
    """
    # C677T (rs1801133): G=C (normal), A=T (mutant)
    c677t_status = "CC" if rs1801133_gt.upper() == "GG" else "CT" if "A" in rs1801133_gt.upper() and "G" in rs1801133_gt.upper() else "TT"

    # A1298C (rs1801131): T=A (normal), G=C (mutant)
    a1298c_status = "AA" if rs1801131_gt.upper() == "TT" else "AC" if "T" in rs1801131_gt.upper() and "G" in rs1801131_gt.upper() else "CC"

    combined = f"{c677t_status}/{a1298c_status}"

    # Bestäm svårighetsgrad
    if c677t_status == "TT":
        severity = "ALLVARLIG"
        activity = "~30% aktivitet"
        description = "Homozygot C677T - kraftigt reducerad MTHFR"
    elif c677t_status == "CT" and a1298c_status == "AC":
        severity = "ALLVARLIG (Compound)"
        activity = "~40-50% aktivitet"
        description = "COMPOUND HETEROZYGOT - kliniskt ekvivalent med 677TT!"
    elif c677t_status == "CT":
        severity = "MÅTTLIG"
        activity = "~65% aktivitet"
        description = "Heterozygot C677T"
    elif a1298c_status == "CC":
        severity = "MÅTTLIG"
        activity = "~60% aktivitet"
        description = "Homozygot A1298C"
    elif a1298c_status == "AC":
        severity = "LÄTT"
        activity = "~80% aktivitet"
        description = "Heterozygot A1298C"
    else:
        severity = "NORMAL"
        activity = "100% aktivitet"
        description = "Wildtyp MTHFR"

    recommendations = []
    if severity in ["ALLVARLIG", "ALLVARLIG (Compound)"]:
        recommendations = [
            "Metylfolat (5-MTHF) OBLIGATORISKT 800-1500 mcg/dag",
            "Metylkobalamin (B12) 1000-5000 mcg/dag",
            "Riboflavin (B2) 50-100 mg/dag",
            "UNDVIK syntetisk folsyra helt",
            "UNDVIK lustgas vid operation",
            "Kontrollera homocystein regelbundet"
        ]
    elif severity == "MÅTTLIG":
        recommendations = [
            "Metylfolat fördelaktigt 400-800 mcg/dag",
            "B12 som metylkobalamin",
            "Undvik höga doser syntetisk folsyra"
        ]

    return {
        "gene": "MTHFR",
        "c677t": c677t_status,
        "a1298c": a1298c_status,
        "combined": combined,
        "severity": severity,
        "activity": activity,
        "description": description,
        "recommendations": recommendations
    }

# =============================================================================
# STATISTICS
# =============================================================================

def get_database_stats() -> Dict[str, Any]:
    """Returnera statistik om databasen."""
    stats = {
        "total_snps": len(UNIFIED_DATABASE),
        "genes": len(set(snp.gene for snp in UNIFIED_DATABASE.values())),
        "categories": {},
        "pathways": set(),
        "with_drug_interactions": 0,
        "with_haplotype_info": 0
    }

    for snp in UNIFIED_DATABASE.values():
        for cat in snp.categories:
            stats["categories"][cat.value] = stats["categories"].get(cat.value, 0) + 1
        stats["pathways"].update(snp.pathways)
        if any(snp.drug_interactions.values()):
            stats["with_drug_interactions"] += 1
        if snp.haplotype_gene:
            stats["with_haplotype_info"] += 1

    stats["pathways"] = len(stats["pathways"])
    return stats

# =============================================================================
# MAIN / TEST
# =============================================================================

if __name__ == "__main__":
    # Fix Windows encoding
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 70)
    print("GWL UNIFIED DATABASE")
    print("=" * 70)

    stats = get_database_stats()
    print(f"\nTotal SNPs: {stats['total_snps']}")
    print(f"Unika gener: {stats['genes']}")
    print(f"Pathways: {stats['pathways']}")
    print(f"Med läkemedelsinteraktioner: {stats['with_drug_interactions']}")
    print(f"Med haplotypinfo: {stats['with_haplotype_info']}")

    print("\nSNPs per kategori:")
    for cat, count in sorted(stats["categories"].items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    print("\n" + "-" * 70)
    print("Alla SNPs i databasen:")
    print("-" * 70)

    for rsid, snp in UNIFIED_DATABASE.items():
        print(f"{rsid} ({snp.gene}): {', '.join(c.value for c in snp.categories)}")

    # Test MTHFR-analys
    print("\n" + "-" * 70)
    print("TEST: MTHFR-analys")
    print("-" * 70)

    mthfr_result = determine_mthfr_status("AA", "TG")  # 677TT + 1298AC compound
    print(f"MTHFR Status: {mthfr_result['combined']}")
    print(f"Svårighetsgrad: {mthfr_result['severity']}")
    print(f"Aktivitet: {mthfr_result['activity']}")
    print(f"Beskrivning: {mthfr_result['description']}")

    # Test APOE-analys
    print("\n" + "-" * 70)
    print("TEST: APOE-analys")
    print("-" * 70)

    apoe_result = determine_apoe_genotype("TC", "CC")  # e3/e4
    print(f"APOE Diplotyp: {apoe_result['diplotype']}")
    print(f"Risknivå: {apoe_result['risk_level']}")
    print(f"Beskrivning: {apoe_result['description']}")

    print("\n" + "=" * 70)
    print("Databas laddad!")
    print("=" * 70)
