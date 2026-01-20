"""
GWL Epistasis Database
======================
Gen-gen interaktioner där effekten av en gen beror på en annan gen.
Inkluderar additiva, synergistiska och antagonistiska interaktioner.

Genetic Wellness Labs - Nutrigenomics Platform
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum

# =============================================================================
# ENUMS
# =============================================================================

class InteractionType(Enum):
    ADDITIVE = "Additiv - Effekterna summeras"
    SYNERGISTIC = "Synergistisk - Effekten större än summan"
    ANTAGONISTIC = "Antagonistisk - Generna motverkar varandra"
    EPISTATIC = "Epistatisk - En gen maskerar en annan"
    MODIFIER = "Modifierande - En gen ändrar effekten av en annan"
    COMPENSATORY = "Kompensatorisk - En gen kompenserar för en annan"

class ClinicalImpact(Enum):
    CRITICAL = "Kritisk - Kräver omedelbar uppmärksamhet"
    HIGH = "Hög klinisk betydelse"
    MODERATE = "Måttlig klinisk betydelse"
    LOW = "Låg klinisk betydelse"
    PROTECTIVE = "Skyddande interaktion"

class Category(Enum):
    METHYLATION = "Metylering"
    DETOXIFICATION = "Detoxifiering"
    INFLAMMATION = "Inflammation"
    NEUROTRANSMITTER = "Neurotransmittorer"
    CARDIOVASCULAR = "Kardiovaskulär"
    DRUG_METABOLISM = "Läkemedelsmetabolism"
    NUTRIENT_METABOLISM = "Näringsämnesmetabolism"
    ANTIOXIDANT = "Antioxidantförsvar"
    HORMONE = "Hormonmetabolism"

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class GeneVariant:
    """En genetisk variant som ingår i en interaktion"""
    gene: str
    rsid: str
    risk_allele: str
    effect: str

@dataclass
class CombinationPhenotype:
    """Fenotyp för en specifik kombination av varianter"""
    genotype_combination: Dict[str, str]  # gene -> genotype
    phenotype: str
    effect_magnitude: str
    clinical_implications: List[str]
    nutrient_recommendations: List[str]
    lifestyle_recommendations: List[str]

@dataclass
class GeneGeneInteraction:
    """Komplett gen-gen interaktion"""
    name: str
    category: Category
    genes: List[GeneVariant]
    interaction_type: InteractionType
    clinical_impact: ClinicalImpact
    description: str
    mechanism: str
    combination_phenotypes: List[CombinationPhenotype]
    testing_recommendations: List[str]
    references: List[str]

# =============================================================================
# METHYLATION EPISTASIS
# =============================================================================

MTHFR_COMPOUND = GeneGeneInteraction(
    name="MTHFR C677T + A1298C Compound",
    category=Category.METHYLATION,
    genes=[
        GeneVariant(
            gene="MTHFR",
            rsid="rs1801133",
            risk_allele="A (T-allel i amino)",
            effect="C677T - Termolabilt enzym"
        ),
        GeneVariant(
            gene="MTHFR",
            rsid="rs1801131",
            risk_allele="G (C-allel i amino)",
            effect="A1298C - Reducerad aktivitet"
        )
    ],
    interaction_type=InteractionType.SYNERGISTIC,
    clinical_impact=ClinicalImpact.HIGH,
    description="Compound heterozygot (677CT/1298AC) har liknande effekt som 677TT homozygot. "
                "Detta är viktigt att identifiera eftersom det ofta missas.",
    mechanism="Båda mutationerna reducerar MTHFR-aktivitet via olika mekanismer. "
              "677T skapar termolabilt enzym som förlorar riboflavin-kofaktor vid 37C. "
              "1298C påverkar regulatorisk domän och BH4-regenerering.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"rs1801133": "GG", "rs1801131": "TT"},
            phenotype="Wildtyp - Normal MTHFR",
            effect_magnitude="100% aktivitet",
            clinical_implications=["Normal folatmetabolism", "Inga specifika åtgärder behövs"],
            nutrient_recommendations=["Standard B-vitaminkomplex"],
            lifestyle_recommendations=["Inga specifika"]
        ),
        CombinationPhenotype(
            genotype_combination={"rs1801133": "GA", "rs1801131": "TT"},
            phenotype="Heterozygot C677T",
            effect_magnitude="~65-85% aktivitet",
            clinical_implications=["Lätt reducerad metyleringskapacitet", "Oftast asymptomatisk"],
            nutrient_recommendations=["Metylfolat kan vara fördelaktigt", "B12 som metylkobalamin"],
            lifestyle_recommendations=["Balanserad kost med gröna bladgrönsaker"]
        ),
        CombinationPhenotype(
            genotype_combination={"rs1801133": "AA", "rs1801131": "TT"},
            phenotype="Homozygot C677T",
            effect_magnitude="~30% aktivitet",
            clinical_implications=[
                "Signifikant reducerad metyleringskapacitet",
                "Förhöjt homocystein vanligt",
                "Ökad risk: neural tube defects, CVD, depression"
            ],
            nutrient_recommendations=[
                "ENDAST metylfolat (5-MTHF) 400-1000 mcg",
                "Metylkobalamin 1000-5000 mcg",
                "Riboflavin (B2) 25-50 mg stabiliserar enzymet",
                "P5P (B6) 25-50 mg",
                "Betain (TMG) som alternativ metyldonator"
            ],
            lifestyle_recommendations=[
                "Undvik folsyraberikade livsmedel",
                "Undvik lustgas vid operation",
                "Övervaka homocystein årligen"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs1801133": "GG", "rs1801131": "GG"},
            phenotype="Homozygot A1298C",
            effect_magnitude="~60% aktivitet",
            clinical_implications=["Måttligt reducerad aktivitet", "Mindre påverkan på homocystein än 677TT"],
            nutrient_recommendations=["Metylfolat fördelaktigt", "B-vitaminkomplex"],
            lifestyle_recommendations=["God kost med folatrika livsmedel"]
        ),
        CombinationPhenotype(
            genotype_combination={"rs1801133": "GA", "rs1801131": "TG"},
            phenotype="COMPOUND HETEROZYGOT (677CT/1298AC)",
            effect_magnitude="~40-50% aktivitet - LIKVÄRDIG MED 677TT",
            clinical_implications=[
                "KRITISKT: Ofta missat vid testning",
                "Kliniskt ekvivalent med 677TT",
                "Förhöjt homocystein",
                "Nedsatt BH4-regenerering kan påverka neurotransmittorer"
            ],
            nutrient_recommendations=[
                "Metylfolat OBLIGATORISKT",
                "Metylkobalamin hög dos",
                "Riboflavin för enzymstabilisering",
                "P5P för alternativ transsulfurering",
                "Överväg SAMe-tillskott vid depression"
            ],
            lifestyle_recommendations=[
                "Samma försiktighet som vid 677TT",
                "Undvik syntetisk folsyra",
                "Undvik lustgas"
            ]
        )
    ],
    testing_recommendations=[
        "Testa ALLTID både rs1801133 OCH rs1801131",
        "Compound heterozygot är kliniskt lika viktig som 677TT",
        "Mät homocystein vid alla MTHFR-varianter"
    ],
    references=[
        "PMID: 24935961 - MTHFR compound heterozygotes",
        "PMID: 17109754 - C677T and A1298C interaction",
        "PMID: 18579210 - MTHFR and homocysteine"
    ]
)

MTHFR_MTR_MTRR = GeneGeneInteraction(
    name="MTHFR + MTR + MTRR Methylation Triad",
    category=Category.METHYLATION,
    genes=[
        GeneVariant(
            gene="MTHFR",
            rsid="rs1801133",
            risk_allele="A",
            effect="Reducerad 5-MTHF-produktion"
        ),
        GeneVariant(
            gene="MTR",
            rsid="rs1805087",
            risk_allele="G",
            effect="A2756G - Reducerad metioninsyntetas"
        ),
        GeneVariant(
            gene="MTRR",
            rsid="rs1801394",
            risk_allele="G",
            effect="A66G - Reducerad MTR-regenerering"
        )
    ],
    interaction_type=InteractionType.SYNERGISTIC,
    clinical_impact=ClinicalImpact.HIGH,
    description="Dessa tre gener bildar kärnan i folatcykeln. Multipla varianter skapar "
                "kumulativ påverkan på metyleringskapaciteten.",
    mechanism="MTHFR producerar 5-MTHF, MTR använder det för att metylera homocystein, "
              "och MTRR regenererar MTR. Problem i alla tre ger kraftigt reducerad metylering.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={
                "rs1801133": "AA",  # MTHFR 677TT
                "rs1805087": "GG",  # MTR 2756GG
                "rs1801394": "GG"   # MTRR 66GG
            },
            phenotype="Triple homozygot - MAXIMAL PÅVERKAN",
            effect_magnitude="Kraftigt reducerad metyleringskapacitet",
            clinical_implications=[
                "KRITISK metyleringsnedsättning",
                "Högt homocystein troligt",
                "Ökad risk: CVD, depression, neural tube defects",
                "B12-brist kan utvecklas trots adekvat intag"
            ],
            nutrient_recommendations=[
                "Metylfolat HÖGDOS (1-5 mg)",
                "Metylkobalamin + Adenosylkobalamin 5000+ mcg",
                "Riboflavin 50-100 mg",
                "Betain (TMG) 1-3 g",
                "SAMe kan övervägas"
            ],
            lifestyle_recommendations=[
                "Regelbunden homocysteinövervakning",
                "Undvik alla MTHFR-hämmare",
                "Överväg IV-B12 vid allvarlig brist"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={
                "rs1801133": "GA",
                "rs1805087": "AG",
                "rs1801394": "AG"
            },
            phenotype="Triple heterozygot",
            effect_magnitude="Måttligt reducerad kapacitet",
            clinical_implications=[
                "Kumulativ men kompenserbbar påverkan",
                "Förhöjt homocystein möjligt",
                "Ökad B12-förbrukning"
            ],
            nutrient_recommendations=[
                "Metylfolat 400-1000 mcg",
                "Metylkobalamin 1000-2500 mcg",
                "B-vitaminkomplex med aktiva former"
            ],
            lifestyle_recommendations=[
                "God kost med metyldonatorer",
                "Årlig homocysteinkontroll"
            ]
        )
    ],
    testing_recommendations=[
        "Testa hela metyleringskedjan, inte bara MTHFR",
        "Inkludera funktionella markörer (homocystein, MMA, folat)",
        "Överväg COMT och CBS för komplett bild"
    ],
    references=[
        "PMID: 28125025 - Methylation pathway genetics",
        "PMID: 16757948 - MTR and MTRR polymorphisms",
        "PMID: 23571587 - Combined methylation gene effects"
    ]
)

COMT_MTHFR = GeneGeneInteraction(
    name="COMT + MTHFR SAMe Axis",
    category=Category.METHYLATION,
    genes=[
        GeneVariant(
            gene="COMT",
            rsid="rs4680",
            risk_allele="A (Met)",
            effect="Val158Met - Långsam katekolaminnedbrytning"
        ),
        GeneVariant(
            gene="MTHFR",
            rsid="rs1801133",
            risk_allele="A (T)",
            effect="C677T - Reducerad 5-MTHF"
        )
    ],
    interaction_type=InteractionType.MODIFIER,
    clinical_impact=ClinicalImpact.MODERATE,
    description="COMT förbrukar SAMe vid katekolaminnedbrytning. MTHFR påverkar SAMe-produktionen. "
                "Kombinationen avgör metyleringsbalans och neurotransmittornivåer.",
    mechanism="COMT Met/Met (långsam) ackumulerar dopamin men förbrukar mindre SAMe. "
              "MTHFR TT producerar mindre SAMe. Kombinationen avgör balansen mellan "
              "dopaminnivåer och metyleringskapacitet.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"rs4680": "AA", "rs1801133": "AA"},
            phenotype="Dubbel Met/Met + 677TT",
            effect_magnitude="Komplext - hög dopamin, låg SAMe",
            clinical_implications=[
                "Låg COMT + Låg MTHFR = Högt dopamin men SAMe-brist",
                "Risk för ångest och övermetyleringskänslighet",
                "Paradox: kan få problem av höga doser metylfolat"
            ],
            nutrient_recommendations=[
                "FÖRSIKTIGT med metylfolat - börja MYCKET lågt (50-100 mcg)",
                "Riboflavin för MTHFR-stabilisering",
                "Magnesium som COMT-kofaktor",
                "UNDVIK höga doser SAMe",
                "UNDVIK grönt te/EGCG (hämmar COMT)"
            ],
            lifestyle_recommendations=[
                "Stresshantering kritisk",
                "Meditation och andningsövningar",
                "Undvik stimulantia"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs4680": "GG", "rs1801133": "AA"},
            phenotype="Val/Val + 677TT",
            effect_magnitude="Snabb COMT + Låg MTHFR = SAMe-brist + lågt dopamin",
            clinical_implications=[
                "Risk för depression och låg motivation",
                "Snabb SAMe-förbrukning med låg produktion",
                "Kan tolerera metylering bättre än Met/Met"
            ],
            nutrient_recommendations=[
                "Metylfolat kan tolereras i normala doser",
                "SAMe-tillskott kan vara fördelaktigt",
                "Tyrosin för dopaminstöd",
                "B-vitaminkomplex"
            ],
            lifestyle_recommendations=[
                "Motion ökar BDNF och dopamin",
                "Kalla bad för noradrenalin"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs4680": "AA", "rs1801133": "GG"},
            phenotype="Met/Met + Normal MTHFR",
            effect_magnitude="Långsam COMT med adekvat SAMe",
            clinical_implications=[
                "Högt dopamin med tillräcklig SAMe",
                "Bästa kombinationen för kognitiv funktion",
                "Men ökad ångestkänslighet vid stress"
            ],
            nutrient_recommendations=[
                "Balanserat B-vitaminkomplex",
                "Magnesium för stresshantering",
                "L-theanin vid ångest"
            ],
            lifestyle_recommendations=[
                "Stresshantering viktigt",
                "Undvik överdriven koffeinbelastning"
            ]
        )
    ],
    testing_recommendations=[
        "Kombinera COMT och MTHFR för metyleringsprotokoll",
        "Mät katekolaminer vid komplex presentation",
        "Individualisera metyleringstillskott baserat på kombination"
    ],
    references=[
        "PMID: 17008817 - COMT and cognition",
        "PMID: 19081561 - COMT-MTHFR interaction",
        "PMID: 22158061 - SAMe metabolism"
    ]
)

# =============================================================================
# DETOXIFICATION EPISTASIS
# =============================================================================

GST_NULL_COMBINATION = GeneGeneInteraction(
    name="GSTM1 + GSTT1 Double Null",
    category=Category.DETOXIFICATION,
    genes=[
        GeneVariant(
            gene="GSTM1",
            rsid="Deletion",
            risk_allele="Null (0/0)",
            effect="Ingen GSTM1-aktivitet"
        ),
        GeneVariant(
            gene="GSTT1",
            rsid="Deletion",
            risk_allele="Null (0/0)",
            effect="Ingen GSTT1-aktivitet"
        )
    ],
    interaction_type=InteractionType.SYNERGISTIC,
    clinical_impact=ClinicalImpact.HIGH,
    description="Dubbel null för glutationtransferaser skapar kraftigt nedsatt fas II-detox "
                "av elektrofila toxiner, PAH, och reaktiva metaboliter från fas I.",
    mechanism="GSTM1 och GSTT1 konjugerar olika substrat men överlappar delvis. "
              "Dubbel null ger minimal skyddande glutationkonjugering mot miljötoxiner.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"GSTM1": "null", "GSTT1": "null"},
            phenotype="Dubbel GST Null",
            effect_magnitude="MINIMAL glutationkonjugering",
            clinical_implications=[
                "KRAFTIGT ökad känslighet för miljötoxiner",
                "Ökad cancerrisk vid exponering (lungcancer, blåscancer)",
                "Sämre tolerans för kemikalier och bekämpningsmedel",
                "Ökad känslighet för cigarettrök och luftföroreningar"
            ],
            nutrient_recommendations=[
                "NAC 600-1200 mg x 2/dag för glutationstöd",
                "Liposomalt glutation 500 mg/dag",
                "Alpha-liponsyra 300-600 mg/dag",
                "Sulforafan (broccoligroddar) dagligen",
                "Selen 200 mcg/dag",
                "Glycin 3-5 g/dag"
            ],
            lifestyle_recommendations=[
                "UNDVIK rökning och passiv rökning",
                "Minimera exponering för bekämpningsmedel",
                "Ät ekologiskt där möjligt",
                "Luftrenare i hemmet",
                "Undvik grillad/rökt mat"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"GSTM1": "present", "GSTT1": "null"},
            phenotype="GSTT1 Null (GSTM1 present)",
            effect_magnitude="Partiell nedsättning",
            clinical_implications=[
                "Nedsatt detox av halogenerade föreningar",
                "GSTM1 kompenserar delvis"
            ],
            nutrient_recommendations=[
                "NAC 600 mg x 1-2/dag",
                "Glutationstöd"
            ],
            lifestyle_recommendations=[
                "Undvik klorerat vatten och halogenerade lösningsmedel"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"GSTM1": "null", "GSTT1": "present"},
            phenotype="GSTM1 Null (GSTT1 present)",
            effect_magnitude="Partiell nedsättning - PAH och aflatoxin",
            clinical_implications=[
                "Nedsatt detox av PAH (polycykliska aromatiska kolväten)",
                "Ökad lungcancerrisk vid rökning"
            ],
            nutrient_recommendations=[
                "NAC och glutation",
                "Sulforafan",
                "I3C/DIM"
            ],
            lifestyle_recommendations=[
                "Undvik grillad mat och cigarettrök",
                "Minimera PAH-exponering"
            ]
        )
    ],
    testing_recommendations=[
        "GST-deletion kräver copy number analysis, inte standard SNP-test",
        "Kombinera med GSTP1 rs1695 för komplett bild",
        "Överväg NQO1 rs1800566 för kinondetox"
    ],
    references=[
        "PMID: 17408518 - GST polymorphisms and cancer",
        "PMID: 16014699 - GSTM1/GSTT1 null and lung cancer",
        "PMID: 19779474 - GST and detoxification"
    ]
)

CYP1B1_COMT_ESTROGEN = GeneGeneInteraction(
    name="CYP1B1 + COMT Estrogen Metabolism",
    category=Category.HORMONE,
    genes=[
        GeneVariant(
            gene="CYP1B1",
            rsid="rs1056836",
            risk_allele="G (Val)",
            effect="Leu432Val - Ökad 4-OH-estradiol produktion"
        ),
        GeneVariant(
            gene="COMT",
            rsid="rs4680",
            risk_allele="A (Met)",
            effect="Val158Met - Långsam östrogenmetylering"
        )
    ],
    interaction_type=InteractionType.SYNERGISTIC,
    clinical_impact=ClinicalImpact.HIGH,
    description="CYP1B1 hydroxylerar östrogen till genotoxisk 4-OH-E2. COMT metylerar och "
                "inaktiverar denna. Hög CYP1B1 + Låg COMT = ackumulering av DNA-skadande östrogen.",
    mechanism="4-hydroxiestradiol kan oxideras till kinonestrogener som skapar DNA-addukter. "
              "COMT ska skyddande metylera dessa till inaktiva metoxyestrogener. "
              "Om COMT är långsam ackumuleras genotoxiska metaboliter.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"rs1056836": "GG", "rs4680": "AA"},
            phenotype="Hög CYP1B1 + Långsam COMT - HÖGSTA RISK",
            effect_magnitude="Maximal 4-OH-estradiol ackumulering",
            clinical_implications=[
                "ÖKAD RISK för östrogenberoende cancer (bröst, livmoder, prostata)",
                "DNA-skada från kinonestrogener",
                "Viktigt vid HRT-beslut"
            ],
            nutrient_recommendations=[
                "DIM/I3C för att skifta till 2-OH-väg (200 mg DIM/dag)",
                "Sulforafan för NQO1-induktion",
                "Kalcium-D-glukarat för glukuronidstöd",
                "Resveratrol hämmar CYP1B1",
                "Magnesium för COMT-kofaktor",
                "Metylfolat + B12 för SAMe-produktion"
            ],
            lifestyle_recommendations=[
                "Överväg försiktighet med HRT",
                "Undvik xenoöstrogener (plast, pesticider)",
                "Regelbunden mammografi/screening",
                "Korsblommiga grönsaker dagligen"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs1056836": "CC", "rs4680": "GG"},
            phenotype="Normal CYP1B1 + Snabb COMT - LÄGSTA RISK",
            effect_magnitude="Minimal 4-OH ackumulering",
            clinical_implications=[
                "Fördelaktig östrogenmetabolism",
                "Snabb inaktivering av alla metaboliter"
            ],
            nutrient_recommendations=[
                "Standardrekommendationer"
            ],
            lifestyle_recommendations=[
                "Inga specifika åtgärder behövs"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs1056836": "GG", "rs4680": "GG"},
            phenotype="Hög CYP1B1 + Snabb COMT",
            effect_magnitude="Hög produktion men snabb inaktivering",
            clinical_implications=[
                "COMT kompenserar delvis för CYP1B1",
                "Måttligt förhöjd risk"
            ],
            nutrient_recommendations=[
                "DIM för att skifta till 2-OH-väg",
                "Överväg antioxidantstöd"
            ],
            lifestyle_recommendations=[
                "Korsblommiga grönsaker"
            ]
        )
    ],
    testing_recommendations=[
        "Urin-östrogenmetabolit-test (DUTCH-test eller liknande)",
        "Mät 2-OH/4-OH-kvot och metyleringsgrad",
        "Viktigt före HRT-beslut"
    ],
    references=[
        "PMID: 17696763 - COMT and estrogen metabolism",
        "PMID: 23295013 - CYP1B1 and breast cancer",
        "PMID: 16825041 - DIM and estrogen",
        "PMID: 19155377 - Estrogen metabolites and cancer"
    ]
)

# =============================================================================
# INFLAMMATION EPISTASIS
# =============================================================================

IL6_TNF_CRP = GeneGeneInteraction(
    name="IL-6 + TNF-a Inflammatory Axis",
    category=Category.INFLAMMATION,
    genes=[
        GeneVariant(
            gene="IL6",
            rsid="rs1800795",
            risk_allele="C",
            effect="-174G>C - Högre IL-6-produktion"
        ),
        GeneVariant(
            gene="TNF",
            rsid="rs1800629",
            risk_allele="A",
            effect="-308G>A - Högre TNF-alfa-produktion"
        )
    ],
    interaction_type=InteractionType.SYNERGISTIC,
    clinical_impact=ClinicalImpact.HIGH,
    description="IL-6 och TNF-alfa är centrala pro-inflammatoriska cytokiner. "
                "Dubbla högproducerande genotyper skapar kronisk låggradig inflammation.",
    mechanism="TNF-alfa aktiverar NF-kB som ökar IL-6. IL-6 stimulerar akutfasproteiner "
              "(CRP, fibrinogen). Positiv feedback loop vid kronisk aktivering.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"rs1800795": "CC", "rs1800629": "AA"},
            phenotype="Dubbel högproducent - MAXIMAL INFLAMMATION",
            effect_magnitude="Kraftigt förhöjd inflammatorisk respons",
            clinical_implications=[
                "Kronisk låggradig inflammation sannolikt",
                "Ökad risk: CVD, diabetes, depression, neurodegeneration",
                "CRP troligen förhöjt",
                "Inflammationsdriven åldrande (inflammaging)"
            ],
            nutrient_recommendations=[
                "Omega-3 HÖGDOS: EPA 2-3 g/dag + DHA 1 g/dag",
                "Kurkumin (biooptimerad) 1000-2000 mg/dag",
                "SPM (Specialized Pro-resolving Mediators)",
                "Vitamin D3 till nivå >75 nmol/L",
                "Quercetin 500-1000 mg/dag",
                "Boswellia för LOX-hämning"
            ],
            lifestyle_recommendations=[
                "Anti-inflammatorisk kost (Medelhavsdieten)",
                "Eliminera raffinerade kolhydrater och socker",
                "Undvik omega-6-överskott",
                "Regelbunden motion (minskar IL-6 kroniskt)",
                "Stresshantering (kortisol -> inflammation)",
                "Sömnoptimering"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs1800795": "GG", "rs1800629": "GG"},
            phenotype="Dubbel lågproducent",
            effect_magnitude="Normal inflammatorisk respons",
            clinical_implications=[
                "Normal cytokinproduktion",
                "Standardrisk"
            ],
            nutrient_recommendations=[
                "Standardrekommendationer"
            ],
            lifestyle_recommendations=[
                "Hälsosam livsstil"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs1800795": "CC", "rs1800629": "GG"},
            phenotype="IL-6 hög, TNF normal",
            effect_magnitude="Förhöjd IL-6",
            clinical_implications=[
                "Ökad CRP och akutfasrespons",
                "Måttligt förhöjd inflammatorisk risk"
            ],
            nutrient_recommendations=[
                "Omega-3 och kurkumin",
                "Vitamin D optimering"
            ],
            lifestyle_recommendations=[
                "Anti-inflammatorisk kost"
            ]
        )
    ],
    testing_recommendations=[
        "Mät hs-CRP som funktionell markör",
        "Cytokinpanel om indicerat",
        "AA/EPA-kvot i blod"
    ],
    references=[
        "PMID: 26567432 - IL-6 and chronic disease",
        "PMID: 15673800 - TNF and IL-6 interaction",
        "PMID: 24526425 - Resolution of inflammation"
    ]
)

FADS_IL6 = GeneGeneInteraction(
    name="FADS1/2 + IL-6 Omega/Inflammation Axis",
    category=Category.INFLAMMATION,
    genes=[
        GeneVariant(
            gene="FADS1",
            rsid="rs174546",
            risk_allele="T",
            effect="Reducerad delta-5-desaturas"
        ),
        GeneVariant(
            gene="IL6",
            rsid="rs1800795",
            risk_allele="C",
            effect="Förhöjd IL-6-produktion"
        )
    ],
    interaction_type=InteractionType.MODIFIER,
    clinical_impact=ClinicalImpact.MODERATE,
    description="FADS-generna styr konvertering av omega-6 till arakidonsyra och omega-3 till "
                "EPA/DHA. I kombination med IL-6-varianter påverkas inflammationsprofilen.",
    mechanism="Höga FADS-aktivitet ökar AA-produktion (pro-inflammatorisk). "
              "Kombinerat med hög IL-6-genotyp skapas pro-inflammatorisk miljö. "
              "Låg FADS behöver preformerad EPA/DHA.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"rs174546": "CC", "rs1800795": "CC"},
            phenotype="Hög FADS + Hög IL-6",
            effect_magnitude="Pro-inflammatorisk",
            clinical_implications=[
                "Hög AA-produktion + Hög cytokinproduktion",
                "Ökad kardiovaskulär risk",
                "Omega-6-restriktion extra viktig"
            ],
            nutrient_recommendations=[
                "Omega-3 HÖGDOS direkt som EPA/DHA",
                "MINSKA omega-6-intag kraftigt",
                "AA/EPA-kvot bör vara <3:1",
                "Anti-inflammatoriska tillskott"
            ],
            lifestyle_recommendations=[
                "Undvik vegetabiliska oljor rika på omega-6",
                "Fisk 3-4 ggr/vecka minimum"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs174546": "TT", "rs1800795": "CC"},
            phenotype="Låg FADS + Hög IL-6",
            effect_magnitude="Komplex - låg konvertering men hög inflammation",
            clinical_implications=[
                "Mindre AA-produktion men fortfarande hög IL-6",
                "MÅSTE få preformerad EPA/DHA",
                "Vegetariska omega-3-källor (ALA) ineffektiva"
            ],
            nutrient_recommendations=[
                "Algolja eller fiskolja OBLIGATORISKT",
                "ALA (linfröolja) konverteras INTE tillräckligt",
                "Anti-inflammatoriska tillskott"
            ],
            lifestyle_recommendations=[
                "Fisk eller algbaserade omega-3-tillskott dagligen"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs174546": "TT", "rs1800795": "GG"},
            phenotype="Låg FADS + Normal IL-6",
            effect_magnitude="Omega-3-brist utan inflammation",
            clinical_implications=[
                "Risk för omega-3-brist",
                "Normal inflammatorisk respons"
            ],
            nutrient_recommendations=[
                "Preformerad EPA/DHA viktig",
                "Vegetarianer MÅSTE supplementera med algolja"
            ],
            lifestyle_recommendations=[
                "Regelbundet fiskintag eller tillskott"
            ]
        )
    ],
    testing_recommendations=[
        "Fettsyraprofil i blod (AA, EPA, DHA)",
        "Beräkna omega-6/omega-3-kvot",
        "hs-CRP som inflammationsmarkör"
    ],
    references=[
        "PMID: 20194237 - FADS polymorphisms",
        "PMID: 28900017 - Omega-3 and inflammation",
        "PMID: 18936471 - FADS and fatty acid composition"
    ]
)

# =============================================================================
# CARDIOVASCULAR EPISTASIS
# =============================================================================

APOE_CETP = GeneGeneInteraction(
    name="APOE + CETP Lipid Metabolism",
    category=Category.CARDIOVASCULAR,
    genes=[
        GeneVariant(
            gene="APOE",
            rsid="rs429358+rs7412",
            risk_allele="e4",
            effect="Ökad LDL, ökad kardiovaskulär risk"
        ),
        GeneVariant(
            gene="CETP",
            rsid="rs708272",
            risk_allele="A (TaqIB B2)",
            effect="Lägre CETP-aktivitet, högre HDL"
        )
    ],
    interaction_type=InteractionType.MODIFIER,
    clinical_impact=ClinicalImpact.MODERATE,
    description="CETP överför kolesterol från HDL till LDL/VLDL. Kombinationen med APOE "
                "påverkar den totala lipidprofilen och kardiovaskulär risk.",
    mechanism="APOE e4 ökar LDL. Låg CETP (B2/B2) ökar HDL. Kombinationen kan delvis "
              "modifiera APOE e4-risken genom förbättrad HDL.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"APOE": "e4/e4", "rs708272": "GG"},
            phenotype="APOE e4/e4 + Hög CETP",
            effect_magnitude="HÖGSTA kardiovaskulär risk",
            clinical_implications=[
                "Högt LDL + Lågt HDL",
                "Maximal aterogen profil",
                "Aggressiv intervention behövs"
            ],
            nutrient_recommendations=[
                "Omega-3 högdos",
                "Minimera mättat fett",
                "Lösliga fibrer",
                "Växtsteriner"
            ],
            lifestyle_recommendations=[
                "Strikt kost med mättat fett <7%",
                "Regelbunden motion",
                "Statinbehandling ofta indicerad"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"APOE": "e4/e4", "rs708272": "AA"},
            phenotype="APOE e4/e4 + Låg CETP",
            effect_magnitude="Högt LDL men kompensatoriskt högt HDL",
            clinical_implications=[
                "Delvis skyddande kombination",
                "HDL kan delvis kompensera för LDL",
                "Fortfarande förhöjd risk men bättre än dubbelt ogynnsam"
            ],
            nutrient_recommendations=[
                "Omega-3",
                "Måttlig mättat fett-restriktion",
                "Motion för HDL-optimering"
            ],
            lifestyle_recommendations=[
                "Bibehåll HDL genom motion och kost",
                "Undvik rökning som sänker HDL"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"APOE": "e3/e3", "rs708272": "AA"},
            phenotype="Normal APOE + Låg CETP",
            effect_magnitude="Fördelaktig lipidprofil",
            clinical_implications=[
                "Normal LDL + Högt HDL",
                "Låg kardiovaskulär risk"
            ],
            nutrient_recommendations=[
                "Standardrekommendationer"
            ],
            lifestyle_recommendations=[
                "Hälsosam livsstil räcker"
            ]
        )
    ],
    testing_recommendations=[
        "Komplett lipidprofil inkl. partikelstorlek",
        "APOE-genotypning",
        "ApoB och Lp(a) för bättre riskbedömning"
    ],
    references=[
        "PMID: 31727829 - APOE and cardiovascular disease",
        "PMID: 17292832 - CETP polymorphisms",
        "PMID: 22215923 - APOE-CETP interaction"
    ]
)

# =============================================================================
# NEUROTRANSMITTER EPISTASIS
# =============================================================================

COMT_MAO_A = GeneGeneInteraction(
    name="COMT + MAO-A Catecholamine Metabolism",
    category=Category.NEUROTRANSMITTER,
    genes=[
        GeneVariant(
            gene="COMT",
            rsid="rs4680",
            risk_allele="A (Met)",
            effect="Långsam katekolaminnedbrytning"
        ),
        GeneVariant(
            gene="MAO-A",
            rsid="rs6323",
            risk_allele="T",
            effect="Högre MAO-A-aktivitet"
        )
    ],
    interaction_type=InteractionType.COMPENSATORY,
    clinical_impact=ClinicalImpact.MODERATE,
    description="COMT och MAO-A är båda involverade i katekolaminnedbrytning. "
                "De kan delvis kompensera för varandra.",
    mechanism="COMT metylerar katekolaminer extraneuronalt, MAO-A oxiderar dem intraneuronalt. "
              "Låg COMT + Hög MAO-A kan ge normal total nedbrytning men med förändrad profil.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"rs4680": "AA", "rs6323": "TT"},
            phenotype="Långsam COMT + Snabb MAO-A",
            effect_magnitude="Partiell kompensation",
            clinical_implications=[
                "MAO-A kompenserar delvis för låg COMT",
                "Fortfarande förhöjt prefrontalt dopamin",
                "Bättre balans än dubbelt långsam"
            ],
            nutrient_recommendations=[
                "Balanserat approach",
                "Magnesium för COMT",
                "Riboflavin för MAO"
            ],
            lifestyle_recommendations=[
                "Stresshantering"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs4680": "AA", "rs6323": "CC"},
            phenotype="Långsam COMT + Långsam MAO-A",
            effect_magnitude="DUBBELT LÅNGSAM",
            clinical_implications=[
                "Ackumulering av dopamin, noradrenalin, serotonin",
                "Ökad ångestkänslighet",
                "Överkänslighet för stimulantia",
                "Risk för överväldigande vid stress"
            ],
            nutrient_recommendations=[
                "UNDVIK höga doser tyrosin eller 5-HTP",
                "Magnesium",
                "L-theanin för balans",
                "UNDVIK grönt te (COMT-hämmare)"
            ],
            lifestyle_recommendations=[
                "Undvik stimulantia",
                "Stressreduktion kritisk",
                "Regelbunden sömn"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs4680": "GG", "rs6323": "CC"},
            phenotype="Snabb COMT + Långsam MAO-A",
            effect_magnitude="Komplex profil",
            clinical_implications=[
                "Snabb extraneuronal + långsam intraneuronal",
                "Lågt dopamin extracellulärt, högre intracellulärt"
            ],
            nutrient_recommendations=[
                "Balanserat stöd"
            ],
            lifestyle_recommendations=[
                "Standardrekommendationer"
            ]
        )
    ],
    testing_recommendations=[
        "Katekolaminmetaboliter (HVA, VMA, 5-HIAA)",
        "Kombinera med BDNF för komplett bild"
    ],
    references=[
        "PMID: 17008817 - COMT and cognition",
        "PMID: 18578540 - MAO-A genetics",
        "PMID: 21385469 - COMT-MAO interaction"
    ]
)

BDNF_COMT = GeneGeneInteraction(
    name="BDNF + COMT Neuroplasticity",
    category=Category.NEUROTRANSMITTER,
    genes=[
        GeneVariant(
            gene="BDNF",
            rsid="rs6265",
            risk_allele="A (Met)",
            effect="Val66Met - Reducerad BDNF-sekretion"
        ),
        GeneVariant(
            gene="COMT",
            rsid="rs4680",
            risk_allele="A (Met)",
            effect="Långsam dopaminnedbrytning"
        )
    ],
    interaction_type=InteractionType.MODIFIER,
    clinical_impact=ClinicalImpact.MODERATE,
    description="BDNF styr neuroplasticitet och COMT påverkar prefrontal dopamin. "
                "Kombinationen påverkar kognitiv funktion och stressrespons.",
    mechanism="BDNF Met reducerar aktivitetsberoende BDNF-frisättning. "
              "COMT Met ökar prefrontalt dopamin men minskar stressresistens. "
              "Dubbla Met kan ge ökad kognitiv kapacitet men sårbarhet.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"rs6265": "AA", "rs4680": "AA"},
            phenotype="Dubbel Met/Met - Sårbar Tänkare",
            effect_magnitude="Hög kognition + Hög sårbarhet",
            clinical_implications=[
                "God kognitiv baskapacitet",
                "Reducerad neuroplasticitet",
                "Ökad känslighet för stress och trauma",
                "Depression- och ångestrisk vid livsbelastning"
            ],
            nutrient_recommendations=[
                "Omega-3 (DHA) för BDNF-stöd",
                "Magnesium",
                "Lion's Mane för nervtillväxt",
                "Undvik övermetylerare"
            ],
            lifestyle_recommendations=[
                "Motion KRITISK (ökar BDNF)",
                "Sömnoptimering",
                "Stresshantering",
                "Kognitiv träning"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs6265": "GG", "rs4680": "AA"},
            phenotype="Normal BDNF + Långsam COMT",
            effect_magnitude="God kognition med bevarat BDNF",
            clinical_implications=[
                "God kognitiv kapacitet",
                "Normal neuroplasticitet",
                "Ångestkänslig vid stress men resilient"
            ],
            nutrient_recommendations=[
                "Magnesium",
                "Balanserat stöd"
            ],
            lifestyle_recommendations=[
                "Motion bibehåller BDNF",
                "Stresshantering"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs6265": "GG", "rs4680": "GG"},
            phenotype="Normal BDNF + Snabb COMT (Warrior)",
            effect_magnitude="Stresstålig, lärandeeffektiv",
            clinical_implications=[
                "God stresshantering",
                "Effektivt lärande",
                "Lägre basalt dopamin"
            ],
            nutrient_recommendations=[
                "Tyrosin vid behov",
                "Balanserat stöd"
            ],
            lifestyle_recommendations=[
                "Motion och utmaningar"
            ]
        )
    ],
    testing_recommendations=[
        "Kombinera med SLC6A4 (serotonintransportör) för komplett bild",
        "Bedöm livshändelser och stressnivå"
    ],
    references=[
        "PMID: 27067767 - BDNF and mental health",
        "PMID: 16914770 - BDNF-COMT interaction",
        "PMID: 19136964 - BDNF and neuroplasticity"
    ]
)

# =============================================================================
# DRUG METABOLISM EPISTASIS
# =============================================================================

CYP2D6_CYP3A4 = GeneGeneInteraction(
    name="CYP2D6 + CYP3A4 Drug Metabolism",
    category=Category.DRUG_METABOLISM,
    genes=[
        GeneVariant(
            gene="CYP2D6",
            rsid="rs3892097",
            risk_allele="T (*4)",
            effect="Null-allel, ingen CYP2D6-aktivitet"
        ),
        GeneVariant(
            gene="CYP3A4",
            rsid="rs35599367",
            risk_allele="T (*22)",
            effect="Reducerad CYP3A4-aktivitet"
        )
    ],
    interaction_type=InteractionType.SYNERGISTIC,
    clinical_impact=ClinicalImpact.HIGH,
    description="CYP2D6 och CYP3A4 metaboliserar tillsammans ~75% av alla läkemedel. "
                "Dubbla nedsättningar kan ge kraftigt ökade läkemedelskoncentrationer.",
    mechanism="Många läkemedel har alternativa metabolismvägar via CYP2D6 och CYP3A4. "
              "Om båda är nedsatta finns ingen backup-väg.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"CYP2D6": "*4/*4", "CYP3A4": "*22/*22"},
            phenotype="Dubbel poor metabolizer",
            effect_magnitude="MINIMAL läkemedelsmetabolism",
            clinical_implications=[
                "KRITISK för läkemedelssäkerhet",
                "Kraftigt ökade plasmakoncentrationer",
                "Risk för toxicitet vid standarddoser",
                "Många läkemedel behöver kraftig dosreduktion"
            ],
            nutrient_recommendations=[
                "Grapefrukt och CYP-hämmare KONTRAINDICERADE",
                "CoQ10 om statiner används"
            ],
            lifestyle_recommendations=[
                "Läkemedelsgenomgång med farmakogenetisk expertis",
                "Alltid börja med lägsta dos",
                "Tät övervakning vid nya läkemedel"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"CYP2D6": "*1/*1", "CYP3A4": "*1/*1"},
            phenotype="Dubbel normal metabolizer",
            effect_magnitude="Normal läkemedelsmetabolism",
            clinical_implications=[
                "Standarddoser fungerar",
                "Normal respons förväntas"
            ],
            nutrient_recommendations=[
                "Standardrekommendationer"
            ],
            lifestyle_recommendations=[
                "Undvik CYP-interaktioner"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"CYP2D6": "*1xN/*1xN", "CYP3A4": "*1/*1"},
            phenotype="Ultra-rapid CYP2D6 + Normal CYP3A4",
            effect_magnitude="Snabb metabolism av CYP2D6-substrat",
            clinical_implications=[
                "Risk för ökad toxicitet av prodrugs (kodein)",
                "Kan behöva högre doser av aktiva läkemedel"
            ],
            nutrient_recommendations=[
                "Försiktighet med prodrugs"
            ],
            lifestyle_recommendations=[
                "Undvik kodein och tramadol"
            ]
        )
    ],
    testing_recommendations=[
        "Komplett farmakogenetisk panel före polyfarmaci",
        "Inkludera CYP2C19, CYP2C9, SLCO1B1",
        "Använd läkemedelsinteraktionsdatabaser"
    ],
    references=[
        "PMID: 26465333 - CYP450 pharmacogenomics",
        "PMID: 28002639 - CYP2D6 allele nomenclature",
        "PMID: 23689640 - CYP3A4 polymorphisms"
    ]
)

# =============================================================================
# NUTRIENT METABOLISM EPISTASIS
# =============================================================================

VDR_CYP2R1 = GeneGeneInteraction(
    name="VDR + CYP2R1 Vitamin D Axis",
    category=Category.NUTRIENT_METABOLISM,
    genes=[
        GeneVariant(
            gene="VDR",
            rsid="rs2228570",
            risk_allele="A (f-allel)",
            effect="FokI - Kortare, mer aktiv receptor"
        ),
        GeneVariant(
            gene="CYP2R1",
            rsid="rs10741657",
            risk_allele="A",
            effect="Reducerad 25-hydroxylering av D-vitamin"
        )
    ],
    interaction_type=InteractionType.MODIFIER,
    clinical_impact=ClinicalImpact.MODERATE,
    description="CYP2R1 konverterar D3 till 25(OH)D. VDR avgör hur cellerna svarar. "
                "Kombinationen bestämmer totalt D-vitaminbehov och respons.",
    mechanism="Låg CYP2R1 aktivitet sänker 25(OH)D-nivåer. VDR-varianter ändrar receptorkänslighet. "
              "Dubbla ogynnsamma varianter kan ge D-vitaminbrist trots normalt intag.",
    combination_phenotypes=[
        CombinationPhenotype(
            genotype_combination={"rs2228570": "AA", "rs10741657": "AA"},
            phenotype="Reducerad hydroxylering + VDR-variant",
            effect_magnitude="Ökad D-vitaminförbrukning",
            clinical_implications=[
                "Högre D-vitaminbehov",
                "Risk för brist trots normalt intag",
                "Kan behöva högre målnivå"
            ],
            nutrient_recommendations=[
                "D3 3000-5000 IE/dag (nivåstyrt)",
                "Mål: 25(OH)D >100 nmol/L",
                "K2 (MK-7) för kalciumdirigering",
                "Magnesium som D-vitaminkofaktor"
            ],
            lifestyle_recommendations=[
                "Solexponering",
                "Regelbunden D-vitamintestning"
            ]
        ),
        CombinationPhenotype(
            genotype_combination={"rs2228570": "GG", "rs10741657": "GG"},
            phenotype="Normal hydroxylering + Normal VDR",
            effect_magnitude="Standard D-vitaminbehov",
            clinical_implications=[
                "Normal D-vitaminmetabolism"
            ],
            nutrient_recommendations=[
                "Standarddos D3 1000-2000 IE",
                "Nivåkontroll årligen"
            ],
            lifestyle_recommendations=[
                "Solexponering"
            ]
        )
    ],
    testing_recommendations=[
        "Mät 25(OH)D regelbundet",
        "VDR-polymorfismer kan förklara varierande respons",
        "Överväg 1,25(OH)2D vid komplex klinik"
    ],
    references=[
        "PMID: 25051316 - VDR polymorphisms",
        "PMID: 20541252 - CYP2R1 and vitamin D",
        "PMID: 23601626 - Vitamin D genetics"
    ]
)

# =============================================================================
# COMPLETE EPISTASIS DATABASE
# =============================================================================

EPISTASIS_DATABASE: Dict[str, GeneGeneInteraction] = {
    "mthfr_compound": MTHFR_COMPOUND,
    "mthfr_mtr_mtrr": MTHFR_MTR_MTRR,
    "comt_mthfr": COMT_MTHFR,
    "gst_null": GST_NULL_COMBINATION,
    "cyp1b1_comt": CYP1B1_COMT_ESTROGEN,
    "il6_tnf": IL6_TNF_CRP,
    "fads_il6": FADS_IL6,
    "apoe_cetp": APOE_CETP,
    "comt_maoa": COMT_MAO_A,
    "bdnf_comt": BDNF_COMT,
    "cyp2d6_cyp3a4": CYP2D6_CYP3A4,
    "vdr_cyp2r1": VDR_CYP2R1
}

# =============================================================================
# EPISTASIS ANALYSIS FUNCTIONS
# =============================================================================

def get_interaction(interaction_id: str) -> Optional[GeneGeneInteraction]:
    """Hämta en specifik gen-gen-interaktion."""
    return EPISTASIS_DATABASE.get(interaction_id.lower())

def get_all_interactions() -> List[str]:
    """Lista alla tillgängliga interaktioner."""
    return list(EPISTASIS_DATABASE.keys())

def get_interactions_by_category(category: Category) -> List[GeneGeneInteraction]:
    """Hämta alla interaktioner inom en kategori."""
    return [i for i in EPISTASIS_DATABASE.values() if i.category == category]

def get_interactions_by_gene(gene: str) -> List[GeneGeneInteraction]:
    """Hitta alla interaktioner som involverar en specifik gen."""
    results = []
    gene_upper = gene.upper()
    for interaction in EPISTASIS_DATABASE.values():
        for g in interaction.genes:
            if g.gene.upper() == gene_upper:
                results.append(interaction)
                break
    return results

def get_interactions_by_rsid(rsid: str) -> List[GeneGeneInteraction]:
    """Hitta alla interaktioner som involverar en specifik SNP."""
    results = []
    for interaction in EPISTASIS_DATABASE.values():
        for g in interaction.genes:
            if g.rsid.lower() == rsid.lower():
                results.append(interaction)
                break
    return results

def get_all_epistasis_snps() -> Set[str]:
    """Samla alla unika SNPs från alla interaktioner."""
    snps = set()
    for interaction in EPISTASIS_DATABASE.values():
        for gene in interaction.genes:
            if gene.rsid != "Deletion" and not gene.rsid.startswith("rs429358"):
                snps.add(gene.rsid)
    return snps

def analyze_epistasis(genotypes: Dict[str, str]) -> List[Dict]:
    """
    Analysera epistatiska interaktioner baserat på genotyper.

    Args:
        genotypes: Dict med rsid -> genotyp

    Returns:
        Lista med matchande interaktioner och deras fenotyper
    """
    results = []

    for interaction_id, interaction in EPISTASIS_DATABASE.items():
        # Kontrollera om vi har data för alla gener i interaktionen
        matched_genes = {}
        for gene in interaction.genes:
            if gene.rsid in genotypes:
                matched_genes[gene.rsid] = genotypes[gene.rsid]

        if len(matched_genes) >= 2:  # Minst 2 gener för interaktion
            # Hitta matchande fenotyp
            for phenotype in interaction.combination_phenotypes:
                match = True
                for rsid, expected_gt in phenotype.genotype_combination.items():
                    if rsid in matched_genes:
                        # Enkel matchning (kan göras mer sofistikerad)
                        if matched_genes[rsid] != expected_gt:
                            match = False
                            break
                    elif rsid not in matched_genes and rsid not in ["APOE", "GSTM1", "GSTT1", "CYP2D6", "CYP3A4"]:
                        match = False
                        break

                if match:
                    results.append({
                        "interaction": interaction.name,
                        "category": interaction.category.value,
                        "type": interaction.interaction_type.value,
                        "impact": interaction.clinical_impact.value,
                        "phenotype": phenotype.phenotype,
                        "effect": phenotype.effect_magnitude,
                        "clinical_implications": phenotype.clinical_implications,
                        "nutrient_recommendations": phenotype.nutrient_recommendations,
                        "lifestyle_recommendations": phenotype.lifestyle_recommendations
                    })
                    break

    return results

def get_critical_interactions() -> List[GeneGeneInteraction]:
    """Hämta alla interaktioner med kritisk eller hög klinisk betydelse."""
    return [i for i in EPISTASIS_DATABASE.values()
            if i.clinical_impact in [ClinicalImpact.CRITICAL, ClinicalImpact.HIGH]]

# =============================================================================
# MAIN / TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GWL EPISTASIS DATABASE")
    print("=" * 70)

    print(f"\nAntal gen-gen-interaktioner: {len(EPISTASIS_DATABASE)}")

    print("\nInteraktioner per kategori:")
    for category in Category:
        interactions = get_interactions_by_category(category)
        if interactions:
            print(f"  {category.value}: {len(interactions)}")

    print("\n" + "-" * 70)
    print("Alla interaktioner:")
    print("-" * 70)

    for interaction_id, interaction in EPISTASIS_DATABASE.items():
        print(f"\n{interaction.name}:")
        print(f"  Kategori: {interaction.category.value}")
        print(f"  Typ: {interaction.interaction_type.value}")
        print(f"  Klinisk betydelse: {interaction.clinical_impact.value}")
        print(f"  Gener: {', '.join(g.gene for g in interaction.genes)}")
        print(f"  Fenotyper: {len(interaction.combination_phenotypes)}")

    # Test - hitta interaktioner för COMT
    print("\n" + "-" * 70)
    print("TEST: Interaktioner som involverar COMT")
    print("-" * 70)

    comt_interactions = get_interactions_by_gene("COMT")
    for interaction in comt_interactions:
        print(f"- {interaction.name}: {interaction.interaction_type.value}")

    # Samla alla SNPs
    print("\n" + "-" * 70)
    print("Alla unika SNPs för epistasisanalys:")
    print("-" * 70)

    all_snps = get_all_epistasis_snps()
    print(f"Antal SNPs: {len(all_snps)}")
    print(f"SNPs: {', '.join(sorted(all_snps))}")

    # Test epistasisanalys
    print("\n" + "-" * 70)
    print("TEST: Epistasisanalys med exempelgenotyper")
    print("-" * 70)

    test_genotypes = {
        "rs1801133": "AA",  # MTHFR 677TT
        "rs1801131": "TT",  # MTHFR 1298AA
        "rs4680": "AA",      # COMT Met/Met
        "rs1800795": "CC",   # IL-6 hög
        "rs1800629": "AA"    # TNF hög
    }

    results = analyze_epistasis(test_genotypes)
    for r in results:
        print(f"\n{r['interaction']}:")
        print(f"  Fenotyp: {r['phenotype']}")
        print(f"  Effekt: {r['effect']}")
        print(f"  Implikationer: {r['clinical_implications'][:2]}...")

    print("\n" + "=" * 70)
    print("Databas laddad!")
    print("=" * 70)
