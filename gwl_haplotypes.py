"""
GWL Haplotypes & Diplotypes Database
=====================================
Haplotyper och diplotyper för kliniskt viktiga gener.
Inkluderar APOE, CYP2D6, CYP2C19, CYP2C9, HLA och andra.

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

class HaplotypeCategory(Enum):
    LIPID_METABOLISM = "Lipidmetabolism"
    DRUG_METABOLISM = "Läkemedelsmetabolism"
    IMMUNE_SYSTEM = "Immunsystem"
    NUTRIENT_METABOLISM = "Näringsämnesmetabolism"
    METHYLATION = "Metylering"
    NEUROTRANSMITTER = "Neurotransmittorer"
    DETOXIFICATION = "Detoxifiering"

class MetabolizerStatus(Enum):
    ULTRA_RAPID = "Ultra-snabb metaboliserare"
    RAPID = "Snabb metaboliserare"
    NORMAL = "Normal metaboliserare"
    INTERMEDIATE = "Intermediär metaboliserare"
    POOR = "Långsam metaboliserare"

class ClinicalSignificance(Enum):
    HIGH = "Hög klinisk betydelse"
    MODERATE = "Måttlig klinisk betydelse"
    LOW = "Låg klinisk betydelse"
    RESEARCH = "Forskningsnivå"

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SNPDefinition:
    """Definition av en SNP som ingår i en haplotyp"""
    rsid: str
    ref_allele: str
    alt_allele: str
    chromosome: str
    position: int
    gene: str
    description: str

@dataclass
class Haplotype:
    """En specifik haplotyp (kombination av alleler på samma kromosom)"""
    name: str
    gene: str
    alleles: Dict[str, str]  # rsid -> allel
    frequency_eur: float
    frequency_eas: float
    frequency_afr: float
    frequency_sas: float
    frequency_amr: float
    functional_effect: str
    clinical_significance: ClinicalSignificance

@dataclass
class Diplotype:
    """Diplotyp (kombination av två haplotyper)"""
    haplotype1: str
    haplotype2: str
    phenotype: str
    metabolizer_status: Optional[MetabolizerStatus]
    clinical_recommendations: List[str]
    nutrient_implications: List[str]
    drug_implications: List[str]

@dataclass
class HaplotypeGene:
    """Komplett haplotyp-gen med alla varianter och diplotyper"""
    gene: str
    category: HaplotypeCategory
    description: str
    snps: List[SNPDefinition]
    haplotypes: List[Haplotype]
    diplotypes: List[Diplotype]
    clinical_guidelines: List[str]
    references: List[str]

# =============================================================================
# APOE - APOLIPOPROTEIN E
# =============================================================================

APOE_SNPS = [
    SNPDefinition(
        rsid="rs429358",
        ref_allele="T",
        alt_allele="C",
        chromosome="19",
        position=44908684,
        gene="APOE",
        description="APOE Cys112Arg - Skiljer e4 från e2/e3"
    ),
    SNPDefinition(
        rsid="rs7412",
        ref_allele="C",
        alt_allele="T",
        chromosome="19",
        position=44908822,
        gene="APOE",
        description="APOE Arg158Cys - Skiljer e2 från e3/e4"
    )
]

APOE_HAPLOTYPES = [
    Haplotype(
        name="e2",
        gene="APOE",
        alleles={"rs429358": "T", "rs7412": "T"},
        frequency_eur=0.08,
        frequency_eas=0.10,
        frequency_afr=0.04,
        frequency_sas=0.05,
        frequency_amr=0.06,
        functional_effect="Sänkt LDL-clearance, högre triglycerider",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="e3",
        gene="APOE",
        alleles={"rs429358": "T", "rs7412": "C"},
        frequency_eur=0.77,
        frequency_eas=0.85,
        frequency_afr=0.65,
        frequency_sas=0.82,
        frequency_amr=0.78,
        functional_effect="Normal lipidmetabolism (referens)",
        clinical_significance=ClinicalSignificance.LOW
    ),
    Haplotype(
        name="e4",
        gene="APOE",
        alleles={"rs429358": "C", "rs7412": "C"},
        frequency_eur=0.15,
        frequency_eas=0.09,
        frequency_afr=0.27,
        frequency_sas=0.11,
        frequency_amr=0.14,
        functional_effect="Ökad LDL-kolesterol, ökad Alzheimer-risk",
        clinical_significance=ClinicalSignificance.HIGH
    )
]

APOE_DIPLOTYPES = [
    Diplotype(
        haplotype1="e2", haplotype2="e2",
        phenotype="APOE e2/e2",
        metabolizer_status=None,
        clinical_recommendations=[
            "Risk för typ III hyperlipidemi vid metabolt syndrom",
            "Övervaka triglycerider regelbundet",
            "Lägre Alzheimer-risk"
        ],
        nutrient_implications=[
            "Begränsa mättat fett",
            "Omega-3 särskilt viktigt för TG-kontroll",
            "Fibrer hjälper lipidprofil"
        ],
        drug_implications=[
            "Statinrespons kan vara annorlunda",
            "Fibrater kan vara mer effektiva än statiner"
        ]
    ),
    Diplotype(
        haplotype1="e2", haplotype2="e3",
        phenotype="APOE e2/e3",
        metabolizer_status=None,
        clinical_recommendations=[
            "Generellt fördelaktig genotyp",
            "Lägre LDL än genomsnitt",
            "Något förhöjda triglycerider möjligt"
        ],
        nutrient_implications=[
            "Balanserad kost räcker oftast",
            "Omega-3 fördelaktigt"
        ],
        drug_implications=[
            "Normal statinrespons förväntas"
        ]
    ),
    Diplotype(
        haplotype1="e2", haplotype2="e4",
        phenotype="APOE e2/e4",
        metabolizer_status=None,
        clinical_recommendations=[
            "Komplex genotyp - e4-risk delvis motverkad av e2",
            "Övervaka både LDL och triglycerider",
            "Måttligt förhöjd Alzheimer-risk"
        ],
        nutrient_implications=[
            "Medelhavsdieten rekommenderas",
            "Omega-3 för både hjärna och lipider",
            "Antioxidanter viktiga"
        ],
        drug_implications=[
            "Individualiserad statinbehandling"
        ]
    ),
    Diplotype(
        haplotype1="e3", haplotype2="e3",
        phenotype="APOE e3/e3",
        metabolizer_status=None,
        clinical_recommendations=[
            "Vanligaste genotypen (ca 60% av befolkningen)",
            "Normal lipidmetabolism",
            "Referens-genotyp"
        ],
        nutrient_implications=[
            "Standardrekommendationer gäller",
            "Balanserad kost"
        ],
        drug_implications=[
            "Normal respons på lipidsänkande läkemedel"
        ]
    ),
    Diplotype(
        haplotype1="e3", haplotype2="e4",
        phenotype="APOE e3/e4",
        metabolizer_status=None,
        clinical_recommendations=[
            "Förhöjd LDL-kolesterol",
            "2-3x ökad Alzheimer-risk",
            "Proaktiv hjärt-kärlprevention rekommenderas"
        ],
        nutrient_implications=[
            "Strikt begränsning av mättat fett",
            "Hög dos omega-3 (EPA/DHA 2-3g/dag)",
            "Antioxidanter: E-vitamin, C-vitamin, flavonoider",
            "B-vitaminer för homocysteinkontroll",
            "Kurkumin kan vara neuroprotektivt"
        ],
        drug_implications=[
            "God statinrespons",
            "Överväg tidigare behandlingsstart"
        ]
    ),
    Diplotype(
        haplotype1="e4", haplotype2="e4",
        phenotype="APOE e4/e4",
        metabolizer_status=None,
        clinical_recommendations=[
            "HÖGSTA RISK-GENOTYP",
            "10-15x ökad Alzheimer-risk",
            "Kraftigt förhöjd LDL-kolesterol",
            "Intensiv kardiovaskulär prevention",
            "Kognitiv uppföljning rekommenderas"
        ],
        nutrient_implications=[
            "KRITISKT: Minimera mättat fett (<7% av energi)",
            "Omega-3 högdos: EPA 2g + DHA 1g dagligen",
            "MCT-olja för hjärnenergi (ketoner)",
            "Fosfolipid-form omega-3 (krill) penetrerar BBB bättre",
            "Vitamin E (blandade tokotrienoler) 200-400 IE",
            "B12 + folat + B6 för homocystein",
            "Lejonmanksvamp (Hericium) för nervtillväxt",
            "Fosfatidylserin 100-300mg",
            "Undvik alkohol helt eller nästan helt"
        ],
        drug_implications=[
            "Utmärkt statinrespons - överväg tidig behandling",
            "PCSK9-hämmare vid otillräcklig effekt",
            "Undvik antikolinergika"
        ]
    )
]

APOE_GENE = HaplotypeGene(
    gene="APOE",
    category=HaplotypeCategory.LIPID_METABOLISM,
    description="Apolipoprotein E - Central roll i lipidtransport och hjärnhälsa. "
                "Tre huvudalleler (e2, e3, e4) ger 6 möjliga genotyper.",
    snps=APOE_SNPS,
    haplotypes=APOE_HAPLOTYPES,
    diplotypes=APOE_DIPLOTYPES,
    clinical_guidelines=[
        "APOE e4 är den starkaste genetiska riskfaktorn för sent debuterande Alzheimer",
        "e4-bärare har 20-25% sämre LDL-receptorfunktion",
        "Livsstilsfaktorer kan modulera genetisk risk signifikant",
        "APOE-genotypning rekommenderas vid familjär hyperlipidemi"
    ],
    references=[
        "PMID: 23571587 - APOE and Alzheimer disease meta-analysis",
        "PMID: 31727829 - APOE e4 and cardiovascular disease",
        "PMID: 30664783 - Dietary interventions in APOE e4 carriers",
        "PMID: 28768150 - APOE genotype and response to statins"
    ]
)

# =============================================================================
# CYP2D6 - CYTOCHROME P450 2D6
# =============================================================================

CYP2D6_SNPS = [
    SNPDefinition(
        rsid="rs3892097",
        ref_allele="C",
        alt_allele="T",
        chromosome="22",
        position=42128945,
        gene="CYP2D6",
        description="CYP2D6*4 - Splicing defekt, ingen aktivitet"
    ),
    SNPDefinition(
        rsid="rs5030655",
        ref_allele="T",
        alt_allele="del",
        chromosome="22",
        position=42127941,
        gene="CYP2D6",
        description="CYP2D6*6 - Frameshift, ingen aktivitet"
    ),
    SNPDefinition(
        rsid="rs16947",
        ref_allele="G",
        alt_allele="A",
        chromosome="22",
        position=42126611,
        gene="CYP2D6",
        description="CYP2D6*2 - Normal-ökad aktivitet"
    ),
    SNPDefinition(
        rsid="rs1065852",
        ref_allele="C",
        alt_allele="T",
        chromosome="22",
        position=42129770,
        gene="CYP2D6",
        description="CYP2D6*10 - Reducerad aktivitet"
    ),
    SNPDefinition(
        rsid="rs28371706",
        ref_allele="C",
        alt_allele="T",
        chromosome="22",
        position=42129819,
        gene="CYP2D6",
        description="CYP2D6*17 - Reducerad aktivitet (vanlig i Afrika)"
    ),
    SNPDefinition(
        rsid="rs5030867",
        ref_allele="A",
        alt_allele="G",
        chromosome="22",
        position=42127803,
        gene="CYP2D6",
        description="CYP2D6*14 - Ingen aktivitet"
    )
]

CYP2D6_HAPLOTYPES = [
    Haplotype(
        name="*1",
        gene="CYP2D6",
        alleles={"rs3892097": "C", "rs16947": "G", "rs1065852": "C"},
        frequency_eur=0.36,
        frequency_eas=0.25,
        frequency_afr=0.50,
        frequency_sas=0.40,
        frequency_amr=0.45,
        functional_effect="Normal enzymaktivitet (referens)",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="*2",
        gene="CYP2D6",
        alleles={"rs3892097": "C", "rs16947": "A", "rs1065852": "C"},
        frequency_eur=0.25,
        frequency_eas=0.15,
        frequency_afr=0.20,
        frequency_sas=0.18,
        frequency_amr=0.20,
        functional_effect="Normal till ökad aktivitet",
        clinical_significance=ClinicalSignificance.MODERATE
    ),
    Haplotype(
        name="*4",
        gene="CYP2D6",
        alleles={"rs3892097": "T", "rs16947": "G", "rs1065852": "C"},
        frequency_eur=0.22,
        frequency_eas=0.01,
        frequency_afr=0.02,
        frequency_sas=0.08,
        frequency_amr=0.12,
        functional_effect="INGEN enzymaktivitet (null-allel)",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="*10",
        gene="CYP2D6",
        alleles={"rs3892097": "C", "rs16947": "G", "rs1065852": "T"},
        frequency_eur=0.02,
        frequency_eas=0.45,
        frequency_afr=0.05,
        frequency_sas=0.08,
        frequency_amr=0.05,
        functional_effect="Reducerad aktivitet (instabilt enzym)",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="*17",
        gene="CYP2D6",
        alleles={"rs28371706": "T"},
        frequency_eur=0.01,
        frequency_eas=0.01,
        frequency_afr=0.20,
        frequency_sas=0.02,
        frequency_amr=0.03,
        functional_effect="Reducerad aktivitet",
        clinical_significance=ClinicalSignificance.MODERATE
    ),
    Haplotype(
        name="*xN",
        gene="CYP2D6",
        alleles={},  # CNV - genkopior
        frequency_eur=0.02,
        frequency_eas=0.01,
        frequency_afr=0.05,
        frequency_sas=0.03,
        frequency_amr=0.03,
        functional_effect="Multipla genkopior - ultra-snabb metabolism",
        clinical_significance=ClinicalSignificance.HIGH
    )
]

CYP2D6_DIPLOTYPES = [
    Diplotype(
        haplotype1="*1", haplotype2="*1",
        phenotype="CYP2D6 *1/*1",
        metabolizer_status=MetabolizerStatus.NORMAL,
        clinical_recommendations=[
            "Normal CYP2D6-metabolism",
            "Standarddoser av CYP2D6-substrat"
        ],
        nutrient_implications=[
            "Normal metabolism av växtalkaloider",
            "Standard koffein-metabolism"
        ],
        drug_implications=[
            "Standarddos kodein -> morfin konvertering",
            "Normal tamoxifen -> endoxifen aktivering",
            "Standarddoser antidepressiva (SSRI, TCA)"
        ]
    ),
    Diplotype(
        haplotype1="*1", haplotype2="*4",
        phenotype="CYP2D6 *1/*4",
        metabolizer_status=MetabolizerStatus.INTERMEDIATE,
        clinical_recommendations=[
            "Intermediär metabolism",
            "Överväg dosreduktion för känsliga substrat"
        ],
        nutrient_implications=[
            "Något långsammare metabolsim av vissa växtföreningar"
        ],
        drug_implications=[
            "Reducerad kodein-effekt möjlig",
            "Antidepressiva: starta lågt, titrera försiktigt",
            "Tamoxifen: överväg alternativ eller CYP2D6-hämmare"
        ]
    ),
    Diplotype(
        haplotype1="*4", haplotype2="*4",
        phenotype="CYP2D6 *4/*4",
        metabolizer_status=MetabolizerStatus.POOR,
        clinical_recommendations=[
            "LÅNGSAM METABOLISERARE - ingen CYP2D6-aktivitet",
            "Undvik prodrugs som kräver CYP2D6-aktivering",
            "Risk för biverkningar vid standarddoser"
        ],
        nutrient_implications=[
            "Försiktighet med höga doser växtextrakt",
            "Kan ackumulera alkaloider"
        ],
        drug_implications=[
            "UNDVIK KODEIN - ingen smärtlindring, risk för biverkningar",
            "UNDVIK TRAMADOL - ineffektivt",
            "Tamoxifen ineffektivt - välj aromatashämmare",
            "Reducera dos: venlafaxin, metoprolol, flekainid",
            "Risk för toxicitet: TCA, atomoxetin"
        ]
    ),
    Diplotype(
        haplotype1="*1", haplotype2="*xN",
        phenotype="CYP2D6 *1/*xN",
        metabolizer_status=MetabolizerStatus.ULTRA_RAPID,
        clinical_recommendations=[
            "ULTRA-SNABB METABOLISERARE",
            "Ökad dos kan behövas för effekt",
            "Risk för toxicitet vid prodrugs"
        ],
        nutrient_implications=[
            "Snabb nedbrytning av växtalkaloider",
            "Kan behöva högre doser av vissa växtextrakt"
        ],
        drug_implications=[
            "VARNING KODEIN - risk för morfinöverdos, speciellt hos barn",
            "UNDVIK TRAMADOL - risk för toxicitet",
            "Tamoxifen: god aktivering men övervaka",
            "Ökad dos kan behövas: antidepressiva, antipsykotika",
            "Ondansetron kan vara ineffektivt"
        ]
    ),
    Diplotype(
        haplotype1="*10", haplotype2="*10",
        phenotype="CYP2D6 *10/*10",
        metabolizer_status=MetabolizerStatus.INTERMEDIATE,
        clinical_recommendations=[
            "Intermediär metabolism (vanlig i Ostasien)",
            "Dosanpassning behövs för känsliga läkemedel"
        ],
        nutrient_implications=[
            "Långsammare metabolsim - försiktighet med alkaloider"
        ],
        drug_implications=[
            "Reducerad kodeineffekt",
            "Antidepressiva: lägre startdos",
            "Tamoxifen: överväg högre dos eller alternativ"
        ]
    )
]

CYP2D6_GENE = HaplotypeGene(
    gene="CYP2D6",
    category=HaplotypeCategory.DRUG_METABOLISM,
    description="Cytokrom P450 2D6 - Metaboliserar ~25% av alla läkemedel. "
                "Högpolymorf gen med över 100 kända alleler. Copy number variations vanliga.",
    snps=CYP2D6_SNPS,
    haplotypes=CYP2D6_HAPLOTYPES,
    diplotypes=CYP2D6_DIPLOTYPES,
    clinical_guidelines=[
        "FDA och EMA rekommenderar CYP2D6-testning för kodein hos barn",
        "CPIC guidelines finns för >20 läkemedel",
        "CNV-analys krävs för fullständig fenotyp",
        "Genotyp-fenotyp korrelation ~90% för extremfenotyper"
    ],
    references=[
        "PMID: 31562822 - CPIC Guideline for CYP2D6 and Codeine",
        "PMID: 28002639 - CYP2D6 Allele Nomenclature",
        "PMID: 23486447 - CPIC Guideline for Tamoxifen and CYP2D6",
        "PMID: 32185396 - CYP2D6 and Antidepressants"
    ]
)

# =============================================================================
# CYP2C19 - CYTOCHROME P450 2C19
# =============================================================================

CYP2C19_SNPS = [
    SNPDefinition(
        rsid="rs4244285",
        ref_allele="G",
        alt_allele="A",
        chromosome="10",
        position=94781859,
        gene="CYP2C19",
        description="CYP2C19*2 - Splicing defekt, ingen aktivitet"
    ),
    SNPDefinition(
        rsid="rs4986893",
        ref_allele="G",
        alt_allele="A",
        chromosome="10",
        position=94780653,
        gene="CYP2C19",
        description="CYP2C19*3 - Stopkodon, ingen aktivitet"
    ),
    SNPDefinition(
        rsid="rs12248560",
        ref_allele="C",
        alt_allele="T",
        chromosome="10",
        position=94761900,
        gene="CYP2C19",
        description="CYP2C19*17 - Ökad transkription, snabb metabolism"
    )
]

CYP2C19_HAPLOTYPES = [
    Haplotype(
        name="*1",
        gene="CYP2C19",
        alleles={"rs4244285": "G", "rs4986893": "G", "rs12248560": "C"},
        frequency_eur=0.63,
        frequency_eas=0.38,
        frequency_afr=0.68,
        frequency_sas=0.55,
        frequency_amr=0.55,
        functional_effect="Normal enzymaktivitet (referens)",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="*2",
        gene="CYP2C19",
        alleles={"rs4244285": "A", "rs4986893": "G", "rs12248560": "C"},
        frequency_eur=0.15,
        frequency_eas=0.30,
        frequency_afr=0.17,
        frequency_sas=0.32,
        frequency_amr=0.12,
        functional_effect="INGEN enzymaktivitet (null-allel)",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="*3",
        gene="CYP2C19",
        alleles={"rs4244285": "G", "rs4986893": "A", "rs12248560": "C"},
        frequency_eur=0.01,
        frequency_eas=0.05,
        frequency_afr=0.01,
        frequency_sas=0.02,
        frequency_amr=0.01,
        functional_effect="INGEN enzymaktivitet (null-allel)",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="*17",
        gene="CYP2C19",
        alleles={"rs4244285": "G", "rs4986893": "G", "rs12248560": "T"},
        frequency_eur=0.21,
        frequency_eas=0.02,
        frequency_afr=0.18,
        frequency_sas=0.12,
        frequency_amr=0.15,
        functional_effect="ÖKAD enzymaktivitet (gain-of-function)",
        clinical_significance=ClinicalSignificance.HIGH
    )
]

CYP2C19_DIPLOTYPES = [
    Diplotype(
        haplotype1="*1", haplotype2="*1",
        phenotype="CYP2C19 *1/*1",
        metabolizer_status=MetabolizerStatus.NORMAL,
        clinical_recommendations=[
            "Normal CYP2C19-metabolism",
            "Standarddoser av CYP2C19-substrat"
        ],
        nutrient_implications=[
            "Normal metabolism av växtföreningar"
        ],
        drug_implications=[
            "Standarddos clopidogrel",
            "Standarddos PPI (omeprazol, pantoprazol)",
            "Standarddos vissa SSRI (escitalopram, citalopram)"
        ]
    ),
    Diplotype(
        haplotype1="*1", haplotype2="*2",
        phenotype="CYP2C19 *1/*2",
        metabolizer_status=MetabolizerStatus.INTERMEDIATE,
        clinical_recommendations=[
            "Intermediär metabolism",
            "Överväg dosanpassning för känsliga substrat"
        ],
        nutrient_implications=[
            "Något långsammare metabolism"
        ],
        drug_implications=[
            "Clopidogrel: reducerad effekt möjlig - överväg prasugrel/ticagrelor",
            "PPI: standarddos oftast OK",
            "SSRI: överväg lägre dos"
        ]
    ),
    Diplotype(
        haplotype1="*2", haplotype2="*2",
        phenotype="CYP2C19 *2/*2",
        metabolizer_status=MetabolizerStatus.POOR,
        clinical_recommendations=[
            "LÅNGSAM METABOLISERARE",
            "Betydande dosanpassning krävs"
        ],
        nutrient_implications=[
            "Försiktighet med höga doser växtextrakt",
            "Kan ackumulera vissa föreningar"
        ],
        drug_implications=[
            "UNDVIK CLOPIDOGREL - använd prasugrel eller ticagrelor",
            "PPI: reducerad dos, alternativt rabeprazol",
            "SSRI: halverad startdos (escitalopram, citalopram, sertralin)",
            "Vorikonazol: reducerad dos"
        ]
    ),
    Diplotype(
        haplotype1="*1", haplotype2="*17",
        phenotype="CYP2C19 *1/*17",
        metabolizer_status=MetabolizerStatus.RAPID,
        clinical_recommendations=[
            "Snabb metabolism",
            "Kan behöva ökad dos för effekt"
        ],
        nutrient_implications=[
            "Snabbare nedbrytning av vissa växtföreningar"
        ],
        drug_implications=[
            "Clopidogrel: god aktivering",
            "PPI: kan behöva högre dos vid reflux",
            "SSRI: kan behöva högre dos för effekt"
        ]
    ),
    Diplotype(
        haplotype1="*17", haplotype2="*17",
        phenotype="CYP2C19 *17/*17",
        metabolizer_status=MetabolizerStatus.ULTRA_RAPID,
        clinical_recommendations=[
            "ULTRA-SNABB METABOLISERARE",
            "Ökad dos behövs ofta för effekt"
        ],
        nutrient_implications=[
            "Snabb nedbrytning av växtföreningar"
        ],
        drug_implications=[
            "Clopidogrel: utmärkt aktivering (blödningsrisk?)",
            "PPI: kan behöva dubbel dos",
            "SSRI: kan behöva högre dos, sämre effekt vid standarddos"
        ]
    )
]

CYP2C19_GENE = HaplotypeGene(
    gene="CYP2C19",
    category=HaplotypeCategory.DRUG_METABOLISM,
    description="Cytokrom P450 2C19 - Metaboliserar protonpumpshämmare, clopidogrel, "
                "och flera antidepressiva. Stor interetnisk variation.",
    snps=CYP2C19_SNPS,
    haplotypes=CYP2C19_HAPLOTYPES,
    diplotypes=CYP2C19_DIPLOTYPES,
    clinical_guidelines=[
        "FDA black box warning på clopidogrel för CYP2C19 poor metabolizers",
        "CPIC guidelines rekommenderar alternativ trombocythämmare",
        "*2 allelen är mycket vanlig i Asien (30%)",
        "*17 ger ökad transkription och är vanlig i Europa (21%)"
    ],
    references=[
        "PMID: 23698643 - CPIC Guideline for CYP2C19 and Clopidogrel",
        "PMID: 25974703 - CYP2C19 and PPIs",
        "PMID: 26417955 - CYP2C19 Genotype-Guided Antiplatelet Therapy"
    ]
)

# =============================================================================
# CYP2C9 - CYTOCHROME P450 2C9
# =============================================================================

CYP2C9_SNPS = [
    SNPDefinition(
        rsid="rs1799853",
        ref_allele="C",
        alt_allele="T",
        chromosome="10",
        position=94942290,
        gene="CYP2C9",
        description="CYP2C9*2 - Arg144Cys, reducerad aktivitet (~70%)"
    ),
    SNPDefinition(
        rsid="rs1057910",
        ref_allele="A",
        alt_allele="C",
        chromosome="10",
        position=94981296,
        gene="CYP2C9",
        description="CYP2C9*3 - Ile359Leu, kraftigt reducerad aktivitet (~20%)"
    )
]

CYP2C9_HAPLOTYPES = [
    Haplotype(
        name="*1",
        gene="CYP2C9",
        alleles={"rs1799853": "C", "rs1057910": "A"},
        frequency_eur=0.79,
        frequency_eas=0.96,
        frequency_afr=0.88,
        frequency_sas=0.85,
        frequency_amr=0.87,
        functional_effect="Normal enzymaktivitet (referens)",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="*2",
        gene="CYP2C9",
        alleles={"rs1799853": "T", "rs1057910": "A"},
        frequency_eur=0.13,
        frequency_eas=0.01,
        frequency_afr=0.03,
        frequency_sas=0.10,
        frequency_amr=0.08,
        functional_effect="Reducerad aktivitet (~70% av normal)",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="*3",
        gene="CYP2C9",
        alleles={"rs1799853": "C", "rs1057910": "C"},
        frequency_eur=0.07,
        frequency_eas=0.03,
        frequency_afr=0.02,
        frequency_sas=0.05,
        frequency_amr=0.05,
        functional_effect="Kraftigt reducerad aktivitet (~20% av normal)",
        clinical_significance=ClinicalSignificance.HIGH
    )
]

CYP2C9_DIPLOTYPES = [
    Diplotype(
        haplotype1="*1", haplotype2="*1",
        phenotype="CYP2C9 *1/*1",
        metabolizer_status=MetabolizerStatus.NORMAL,
        clinical_recommendations=[
            "Normal CYP2C9-metabolism",
            "Standarddoser av warfarin, NSAID"
        ],
        nutrient_implications=[
            "Normal metabolism av omega-6 till eikosanoider"
        ],
        drug_implications=[
            "Standarddos warfarin (5-7 mg/dag typiskt)",
            "Normal NSAID-metabolism",
            "Standarddos losartan, fenytoin"
        ]
    ),
    Diplotype(
        haplotype1="*1", haplotype2="*2",
        phenotype="CYP2C9 *1/*2",
        metabolizer_status=MetabolizerStatus.INTERMEDIATE,
        clinical_recommendations=[
            "Intermediär metabolism",
            "Måttlig dosreduktion kan behövas"
        ],
        nutrient_implications=[
            "Något långsammare arakidonsyremetabolism"
        ],
        drug_implications=[
            "Warfarin: ~15-20% dosreduktion",
            "NSAID: standarddos oftast OK",
            "Överväg lägre dos fenytoin"
        ]
    ),
    Diplotype(
        haplotype1="*1", haplotype2="*3",
        phenotype="CYP2C9 *1/*3",
        metabolizer_status=MetabolizerStatus.INTERMEDIATE,
        clinical_recommendations=[
            "Intermediär metabolism",
            "Dosreduktion rekommenderas"
        ],
        nutrient_implications=[
            "Långsammare metabolism av vissa växtföreningar"
        ],
        drug_implications=[
            "Warfarin: ~25-30% dosreduktion",
            "NSAID: överväg lägre dos",
            "Fenytoin: lägre startdos"
        ]
    ),
    Diplotype(
        haplotype1="*2", haplotype2="*2",
        phenotype="CYP2C9 *2/*2",
        metabolizer_status=MetabolizerStatus.INTERMEDIATE,
        clinical_recommendations=[
            "Intermediär metabolism",
            "Signifikant dosreduktion kan behövas"
        ],
        nutrient_implications=[
            "Långsammare arakidonsyremetabolism"
        ],
        drug_implications=[
            "Warfarin: ~30-40% dosreduktion",
            "NSAID: lägre dos, övervaka GI-biverkningar",
            "Fenytoin: lägre dos med nivåmonitorering"
        ]
    ),
    Diplotype(
        haplotype1="*2", haplotype2="*3",
        phenotype="CYP2C9 *2/*3",
        metabolizer_status=MetabolizerStatus.POOR,
        clinical_recommendations=[
            "LÅNGSAM METABOLISERARE",
            "Kraftig dosreduktion krävs"
        ],
        nutrient_implications=[
            "Signifikant långsammare metabolism"
        ],
        drug_implications=[
            "Warfarin: ~50% dosreduktion, täta INR-kontroller",
            "NSAID: reducerad dos, kort behandlingstid",
            "Fenytoin: kraftigt reducerad dos"
        ]
    ),
    Diplotype(
        haplotype1="*3", haplotype2="*3",
        phenotype="CYP2C9 *3/*3",
        metabolizer_status=MetabolizerStatus.POOR,
        clinical_recommendations=[
            "MYCKET LÅNGSAM METABOLISERARE",
            "Drastisk dosreduktion eller alternativt läkemedel"
        ],
        nutrient_implications=[
            "Försiktighet med alla CYP2C9-substrat"
        ],
        drug_implications=[
            "Warfarin: ~70-80% dosreduktion (1-2 mg/dag), överväg DOAC",
            "NSAID: undvik om möjligt, risk för GI-blödning",
            "Fenytoin: alternativ antiepileptika kan vara säkrare"
        ]
    )
]

CYP2C9_GENE = HaplotypeGene(
    gene="CYP2C9",
    category=HaplotypeCategory.DRUG_METABOLISM,
    description="Cytokrom P450 2C9 - Metaboliserar warfarin, NSAID, losartan och fenytoin. "
                "Kritisk för warfarindosering.",
    snps=CYP2C9_SNPS,
    haplotypes=CYP2C9_HAPLOTYPES,
    diplotypes=CYP2C9_DIPLOTYPES,
    clinical_guidelines=[
        "CYP2C9 + VKORC1 + ålder + BMI förklarar ~55% av warfarindos-variationen",
        "FDA rekommenderar genotypning före warfarinstart",
        "CPIC och DPWG har doseringsriktlinjer",
        "*2 och *3 är vanligast i Europa"
    ],
    references=[
        "PMID: 28198005 - CPIC Guideline for Warfarin",
        "PMID: 19228618 - CYP2C9 and NSAID metabolism",
        "PMID: 24827397 - Pharmacogenomics of warfarin"
    ]
)

# =============================================================================
# VKORC1 - VITAMIN K EPOXIDE REDUCTASE
# =============================================================================

VKORC1_SNPS = [
    SNPDefinition(
        rsid="rs9923231",
        ref_allele="G",
        alt_allele="A",
        chromosome="16",
        position=31096368,
        gene="VKORC1",
        description="VKORC1 -1639G>A - Reducerad genexpression"
    )
]

VKORC1_HAPLOTYPES = [
    Haplotype(
        name="G (High dose)",
        gene="VKORC1",
        alleles={"rs9923231": "G"},
        frequency_eur=0.42,
        frequency_eas=0.10,
        frequency_afr=0.90,
        frequency_sas=0.25,
        frequency_amr=0.55,
        functional_effect="Normal VKORC1-expression, högre warfarinbehov",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="A (Low dose)",
        gene="VKORC1",
        alleles={"rs9923231": "A"},
        frequency_eur=0.58,
        frequency_eas=0.90,
        frequency_afr=0.10,
        frequency_sas=0.75,
        frequency_amr=0.45,
        functional_effect="Reducerad VKORC1-expression, lägre warfarinbehov",
        clinical_significance=ClinicalSignificance.HIGH
    )
]

VKORC1_DIPLOTYPES = [
    Diplotype(
        haplotype1="G (High dose)", haplotype2="G (High dose)",
        phenotype="VKORC1 GG",
        metabolizer_status=None,
        clinical_recommendations=[
            "Högre warfarindos behövs",
            "Normal K-vitamin-känslighet"
        ],
        nutrient_implications=[
            "Standard K-vitaminintag OK",
            "Gröna grönsaker påverkar INR normalt"
        ],
        drug_implications=[
            "Warfarin: högre dos (6-8 mg/dag typiskt)",
            "Normal respons på K-vitamin-beroende faktorer"
        ]
    ),
    Diplotype(
        haplotype1="G (High dose)", haplotype2="A (Low dose)",
        phenotype="VKORC1 GA",
        metabolizer_status=None,
        clinical_recommendations=[
            "Intermediär warfarinkänslighet",
            "Standarddosering som utgångspunkt"
        ],
        nutrient_implications=[
            "Konsistent K-vitaminintag viktigt"
        ],
        drug_implications=[
            "Warfarin: standarddos som start (4-6 mg/dag)",
            "Normal titreringsperiod"
        ]
    ),
    Diplotype(
        haplotype1="A (Low dose)", haplotype2="A (Low dose)",
        phenotype="VKORC1 AA",
        metabolizer_status=None,
        clinical_recommendations=[
            "HÖG WARFARINKÄNSLIGHET",
            "Låg startdos krävs",
            "Ökad blödningsrisk vid standarddos"
        ],
        nutrient_implications=[
            "K-vitaminrikt kostintag kan vara svårt att balansera",
            "Undvik stora variationer i K-vitaminintag",
            "Försiktighet med K-vitamintillskott"
        ],
        drug_implications=[
            "Warfarin: låg startdos (2-3 mg/dag)",
            "Täta INR-kontroller initialt",
            "Överväg DOAC som alternativ"
        ]
    )
]

VKORC1_GENE = HaplotypeGene(
    gene="VKORC1",
    category=HaplotypeCategory.DRUG_METABOLISM,
    description="Vitamin K-epoxidreduktas - Målenzymet för warfarin. "
                "rs9923231 påverkar genexpression och warfarinkänslighet.",
    snps=VKORC1_SNPS,
    haplotypes=VKORC1_HAPLOTYPES,
    diplotypes=VKORC1_DIPLOTYPES,
    clinical_guidelines=[
        "VKORC1 är den viktigaste genetiska faktorn för warfarindos",
        "A-allelen är mycket vanlig i Asien (90%)",
        "Kombinera med CYP2C9 för optimal dosering",
        "Kliniska algoritmer finns för dosprediktion"
    ],
    references=[
        "PMID: 28198005 - CPIC Guideline for Warfarin",
        "PMID: 16902421 - VKORC1 haplotypes and warfarin",
        "PMID: 19755853 - Pharmacogenetics-based warfarin dosing"
    ]
)

# =============================================================================
# MTHFR - METHYLENETETRAHYDROFOLATE REDUCTASE
# =============================================================================

MTHFR_SNPS = [
    SNPDefinition(
        rsid="rs1801133",
        ref_allele="G",
        alt_allele="A",
        chromosome="1",
        position=11856378,
        gene="MTHFR",
        description="MTHFR C677T (Ala222Val) - Termolabilt enzym"
    ),
    SNPDefinition(
        rsid="rs1801131",
        ref_allele="T",
        alt_allele="G",
        chromosome="1",
        position=11854476,
        gene="MTHFR",
        description="MTHFR A1298C (Glu429Ala) - Reducerad aktivitet"
    )
]

MTHFR_HAPLOTYPES = [
    Haplotype(
        name="677C-1298A",
        gene="MTHFR",
        alleles={"rs1801133": "G", "rs1801131": "T"},
        frequency_eur=0.50,
        frequency_eas=0.45,
        frequency_afr=0.65,
        frequency_sas=0.55,
        frequency_amr=0.40,
        functional_effect="Normal enzymaktivitet (referens)",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="677T-1298A",
        gene="MTHFR",
        alleles={"rs1801133": "A", "rs1801131": "T"},
        frequency_eur=0.32,
        frequency_eas=0.30,
        frequency_afr=0.10,
        frequency_sas=0.15,
        frequency_amr=0.45,
        functional_effect="Termolabilt enzym, ~70% aktivitet",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="677C-1298C",
        gene="MTHFR",
        alleles={"rs1801133": "G", "rs1801131": "G"},
        frequency_eur=0.18,
        frequency_eas=0.25,
        frequency_afr=0.25,
        frequency_sas=0.30,
        frequency_amr=0.15,
        functional_effect="Reducerad aktivitet, ~60%",
        clinical_significance=ClinicalSignificance.MODERATE
    )
]

MTHFR_DIPLOTYPES = [
    Diplotype(
        haplotype1="677C-1298A", haplotype2="677C-1298A",
        phenotype="MTHFR 677CC/1298AA (Wildtyp)",
        metabolizer_status=None,
        clinical_recommendations=[
            "Normal MTHFR-aktivitet",
            "Standard folatbehov"
        ],
        nutrient_implications=[
            "Folsyra omvandlas normalt",
            "Standarddos B-vitaminer räcker"
        ],
        drug_implications=[
            "Normal respons på metotrexat",
            "Standarddosering folsyra vid graviditet"
        ]
    ),
    Diplotype(
        haplotype1="677C-1298A", haplotype2="677T-1298A",
        phenotype="MTHFR 677CT/1298AA (Heterozygot C677T)",
        metabolizer_status=None,
        clinical_recommendations=[
            "Lätt reducerad aktivitet (~85%)",
            "Oftast inga kliniska konsekvenser"
        ],
        nutrient_implications=[
            "Metylfolat kan vara fördelaktigt",
            "B12 viktigt för metyleringsbalans"
        ],
        drug_implications=[
            "Normal metotrexatrespons",
            "Standarddos folsyra oftast OK"
        ]
    ),
    Diplotype(
        haplotype1="677T-1298A", haplotype2="677T-1298A",
        phenotype="MTHFR 677TT (Homozygot C677T)",
        metabolizer_status=None,
        clinical_recommendations=[
            "SIGNIFIKANT REDUCERAD AKTIVITET (~30%)",
            "Förhöjt homocystein vanligt",
            "Övervaka folat- och B12-status"
        ],
        nutrient_implications=[
            "ANVÄND ENDAST METYLFOLAT (5-MTHF)",
            "Undvik syntetisk folsyra (pteroylmonoglutaminsyra)",
            "Metylkobalamin (B12) istället för cyanokobalamin",
            "B6 (P5P-form) stödjer transsulfureringsvägen",
            "Betain (TMG) som alternativ metyldonator",
            "Riboflavin (B2) stabiliserar enzymet"
        ],
        drug_implications=[
            "Metotrexat: ökad toxicitetsrisk, lägre dos",
            "N2O (lustgas): undvik vid operation",
            "5-fluorouracil: modifierad dosering kan behövas"
        ]
    ),
    Diplotype(
        haplotype1="677C-1298C", haplotype2="677C-1298C",
        phenotype="MTHFR 1298CC (Homozygot A1298C)",
        metabolizer_status=None,
        clinical_recommendations=[
            "Måttligt reducerad aktivitet (~60%)",
            "Mindre påverkan än 677TT"
        ],
        nutrient_implications=[
            "Metylfolat kan vara fördelaktigt",
            "BH4-kofaktor kan påverkas",
            "B-vitaminkomplex rekommenderas"
        ],
        drug_implications=[
            "Normal metotrexatrespons oftast"
        ]
    ),
    Diplotype(
        haplotype1="677T-1298A", haplotype2="677C-1298C",
        phenotype="MTHFR 677CT/1298AC (Compound Heterozygot)",
        metabolizer_status=None,
        clinical_recommendations=[
            "COMPOUND HETEROZYGOT",
            "Likvärdig med 677TT i effekt",
            "Förhöjt homocystein möjligt"
        ],
        nutrient_implications=[
            "ENDAST METYLFOLAT rekommenderas",
            "Metylkobalamin (B12)",
            "B6 i P5P-form",
            "Riboflavin (B2) som kofaktor"
        ],
        drug_implications=[
            "Metotrexat: försiktighet, överväg lägre dos",
            "Undvik N2O vid narkos"
        ]
    )
]

MTHFR_GENE = HaplotypeGene(
    gene="MTHFR",
    category=HaplotypeCategory.METHYLATION,
    description="Metylentetrahydrofolatreduktas - Centralt enzym i folatcykeln och metylering. "
                "C677T och A1298C är de viktigaste varianterna.",
    snps=MTHFR_SNPS,
    haplotypes=MTHFR_HAPLOTYPES,
    diplotypes=MTHFR_DIPLOTYPES,
    clinical_guidelines=[
        "677TT är associerat med 25% förhöjt homocystein",
        "Compound heterozygot (677CT/1298AC) har liknande effekt som 677TT",
        "Metylfolat kringgår MTHFR-enzymet",
        "677TT är vanligare i Sydeuropa och Latinamerika"
    ],
    references=[
        "PMID: 24935961 - MTHFR polymorphisms and disease",
        "PMID: 17109754 - MTHFR C677T and folate",
        "PMID: 28125025 - MTHFR and homocysteine metabolism",
        "PMID: 24825598 - Methylfolate vs folic acid"
    ]
)

# =============================================================================
# HLA-B*57:01 - ABACAVIR HYPERSENSITIVITY
# =============================================================================

HLA_B5701_SNPS = [
    SNPDefinition(
        rsid="rs2395029",
        ref_allele="G",
        alt_allele="T",
        chromosome="6",
        position=31381296,
        gene="HLA-B",
        description="Tag-SNP för HLA-B*57:01"
    )
]

HLA_B5701_HAPLOTYPES = [
    Haplotype(
        name="HLA-B*57:01 negative",
        gene="HLA-B",
        alleles={"rs2395029": "G"},
        frequency_eur=0.94,
        frequency_eas=0.99,
        frequency_afr=0.99,
        frequency_sas=0.97,
        frequency_amr=0.97,
        functional_effect="Normal - ingen abacaviröverkänslighet",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="HLA-B*57:01 positive",
        gene="HLA-B",
        alleles={"rs2395029": "T"},
        frequency_eur=0.06,
        frequency_eas=0.01,
        frequency_afr=0.01,
        frequency_sas=0.03,
        frequency_amr=0.03,
        functional_effect="Bärare - risk för abacaviröverkänslighet",
        clinical_significance=ClinicalSignificance.HIGH
    )
]

HLA_B5701_DIPLOTYPES = [
    Diplotype(
        haplotype1="HLA-B*57:01 negative", haplotype2="HLA-B*57:01 negative",
        phenotype="HLA-B*57:01 Negativ",
        metabolizer_status=None,
        clinical_recommendations=[
            "Låg risk för abacaviröverkänslighet",
            "Abacavir kan användas om indicerat"
        ],
        nutrient_implications=[],
        drug_implications=[
            "Abacavir: kan användas med standardövervakning"
        ]
    ),
    Diplotype(
        haplotype1="HLA-B*57:01 positive", haplotype2="HLA-B*57:01 negative",
        phenotype="HLA-B*57:01 Positiv (heterozygot)",
        metabolizer_status=None,
        clinical_recommendations=[
            "KONTRAINDIKATION FÖR ABACAVIR",
            "Risk för allvarlig överkänslighetsreaktion",
            "Välj alternativt antiretroviralt läkemedel"
        ],
        nutrient_implications=[],
        drug_implications=[
            "ABACAVIR KONTRAINDICERAT",
            "Använd alternativ: tenofovir, emtricitabin"
        ]
    ),
    Diplotype(
        haplotype1="HLA-B*57:01 positive", haplotype2="HLA-B*57:01 positive",
        phenotype="HLA-B*57:01 Positiv (homozygot)",
        metabolizer_status=None,
        clinical_recommendations=[
            "STARK KONTRAINDIKATION FÖR ABACAVIR",
            "Hög risk för allvarlig överkänslighetsreaktion"
        ],
        nutrient_implications=[],
        drug_implications=[
            "ABACAVIR STRIKT KONTRAINDICERAT"
        ]
    )
]

HLA_B5701_GENE = HaplotypeGene(
    gene="HLA-B*57:01",
    category=HaplotypeCategory.IMMUNE_SYSTEM,
    description="HLA-B*57:01 - Genetisk markör för abacaviröverkänslighet. "
                "Obligatorisk testning före abacavirbehandling.",
    snps=HLA_B5701_SNPS,
    haplotypes=HLA_B5701_HAPLOTYPES,
    diplotypes=HLA_B5701_DIPLOTYPES,
    clinical_guidelines=[
        "FDA och EMA kräver HLA-B*57:01-test före abacavir",
        "~5-8% av kaukasier är bärare",
        "~100% av bärare får reaktion vid exponering",
        "Kostnadseffektiv screening etablerad"
    ],
    references=[
        "PMID: 18192778 - HLA-B*5701 Screening for Abacavir Hypersensitivity",
        "PMID: 24847164 - CPIC Guideline for Abacavir and HLA-B*57:01"
    ]
)

# =============================================================================
# SLCO1B1 - STATIN MYOPATHY
# =============================================================================

SLCO1B1_SNPS = [
    SNPDefinition(
        rsid="rs4149056",
        ref_allele="T",
        alt_allele="C",
        chromosome="12",
        position=21178615,
        gene="SLCO1B1",
        description="SLCO1B1 *5 (Val174Ala) - Reducerad statintransport"
    )
]

SLCO1B1_HAPLOTYPES = [
    Haplotype(
        name="*1a/*1b",
        gene="SLCO1B1",
        alleles={"rs4149056": "T"},
        frequency_eur=0.85,
        frequency_eas=0.85,
        frequency_afr=0.98,
        frequency_sas=0.90,
        frequency_amr=0.90,
        functional_effect="Normal transportfunktion",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="*5/*15/*17",
        gene="SLCO1B1",
        alleles={"rs4149056": "C"},
        frequency_eur=0.15,
        frequency_eas=0.15,
        frequency_afr=0.02,
        frequency_sas=0.10,
        frequency_amr=0.10,
        functional_effect="Reducerad statintransport till lever",
        clinical_significance=ClinicalSignificance.HIGH
    )
]

SLCO1B1_DIPLOTYPES = [
    Diplotype(
        haplotype1="*1a/*1b", haplotype2="*1a/*1b",
        phenotype="SLCO1B1 TT (Normal funktion)",
        metabolizer_status=None,
        clinical_recommendations=[
            "Normal statintransport",
            "Standarddoser av statiner"
        ],
        nutrient_implications=[
            "CoQ10 supplementering ändå fördelaktigt vid statinbruk"
        ],
        drug_implications=[
            "Simvastatin: upp till 40mg OK",
            "Alla statiner vid standarddos"
        ]
    ),
    Diplotype(
        haplotype1="*1a/*1b", haplotype2="*5/*15/*17",
        phenotype="SLCO1B1 TC (Intermediär)",
        metabolizer_status=None,
        clinical_recommendations=[
            "4x ökad myopatirisk",
            "Överväg lägre statindos eller alternativ"
        ],
        nutrient_implications=[
            "CoQ10 100-200mg rekommenderas starkt",
            "Vitamin D optimering kan minska muskelbesvär"
        ],
        drug_implications=[
            "Simvastatin: max 20mg/dag",
            "Överväg pravastatin eller rosuvastatin (lägre risk)",
            "Övervaka CK vid muskelbesvär"
        ]
    ),
    Diplotype(
        haplotype1="*5/*15/*17", haplotype2="*5/*15/*17",
        phenotype="SLCO1B1 CC (Nedsatt funktion)",
        metabolizer_status=None,
        clinical_recommendations=[
            "16x ÖKAD MYOPATIRISK",
            "Undvik simvastatin",
            "Lägre dos av andra statiner"
        ],
        nutrient_implications=[
            "CoQ10 200-300mg dagligen",
            "D-vitamin: säkerställ >75 nmol/L",
            "Magnesium för muskelfunktion"
        ],
        drug_implications=[
            "UNDVIK SIMVASTATIN",
            "UNDVIK ATORVASTATIN HÖGDOS",
            "Pravastatin: säkrast alternativ",
            "Rosuvastatin: max 20mg",
            "Överväg PCSK9-hämmare vid FH"
        ]
    )
]

SLCO1B1_GENE = HaplotypeGene(
    gene="SLCO1B1",
    category=HaplotypeCategory.DRUG_METABOLISM,
    description="Organisk anjontransportör 1B1 - Transporterar statiner till levern. "
                "rs4149056 ökar myopatirisk dramatiskt.",
    snps=SLCO1B1_SNPS,
    haplotypes=SLCO1B1_HAPLOTYPES,
    diplotypes=SLCO1B1_DIPLOTYPES,
    clinical_guidelines=[
        "FDA begränsar simvastatin 80mg pga myopatirisk",
        "CPIC guideline finns för simvastatin",
        "rs4149056 CC har 16x ökad myopatirisk",
        "Pravastatin och rosuvastatin påverkas mindre"
    ],
    references=[
        "PMID: 28027320 - CPIC Guideline for Simvastatin and SLCO1B1",
        "PMID: 18650507 - SLCO1B1 and statin-induced myopathy",
        "PMID: 21730106 - Statin pharmacogenetics"
    ]
)

# =============================================================================
# COMT - CATECHOL-O-METHYLTRANSFERASE
# =============================================================================

COMT_SNPS = [
    SNPDefinition(
        rsid="rs4680",
        ref_allele="G",
        alt_allele="A",
        chromosome="22",
        position=19963748,
        gene="COMT",
        description="COMT Val158Met - Enzymaktivitet och stabilitet"
    )
]

COMT_HAPLOTYPES = [
    Haplotype(
        name="Val (G)",
        gene="COMT",
        alleles={"rs4680": "G"},
        frequency_eur=0.50,
        frequency_eas=0.70,
        frequency_afr=0.65,
        frequency_sas=0.55,
        frequency_amr=0.55,
        functional_effect="Hög COMT-aktivitet, snabb katekolaminmetabolism",
        clinical_significance=ClinicalSignificance.HIGH
    ),
    Haplotype(
        name="Met (A)",
        gene="COMT",
        alleles={"rs4680": "A"},
        frequency_eur=0.50,
        frequency_eas=0.30,
        frequency_afr=0.35,
        frequency_sas=0.45,
        frequency_amr=0.45,
        functional_effect="Låg COMT-aktivitet, långsam katekolaminmetabolism",
        clinical_significance=ClinicalSignificance.HIGH
    )
]

COMT_DIPLOTYPES = [
    Diplotype(
        haplotype1="Val (G)", haplotype2="Val (G)",
        phenotype="COMT Val/Val (GG)",
        metabolizer_status=MetabolizerStatus.RAPID,
        clinical_recommendations=[
            "'Warrior' fenotyp - stresstålig men lägre prefrontal dopamin",
            "Bättre smärttolerans",
            "Kan hantera akut stress väl"
        ],
        nutrient_implications=[
            "Magnesium viktigt (COMT-kofaktor)",
            "Tyrosin kan behövas för dopaminsupport",
            "SAMe-cykling kräver B-vitaminer",
            "Grönt te/EGCG hämmar COMT (kan öka dopamin)"
        ],
        drug_implications=[
            "Snabb nedbrytning av levodopa",
            "Kan behöva högre dos COMT-substrat",
            "Östrogen metaboliseras snabbt"
        ]
    ),
    Diplotype(
        haplotype1="Val (G)", haplotype2="Met (A)",
        phenotype="COMT Val/Met (GA)",
        metabolizer_status=MetabolizerStatus.INTERMEDIATE,
        clinical_recommendations=[
            "Balanserad fenotyp",
            "Intermediär stresshantering och kognition"
        ],
        nutrient_implications=[
            "Balanserat behov",
            "Magnesium och B-vitaminer standard"
        ],
        drug_implications=[
            "Normal respons på de flesta läkemedel"
        ]
    ),
    Diplotype(
        haplotype1="Met (A)", haplotype2="Met (A)",
        phenotype="COMT Met/Met (AA)",
        metabolizer_status=MetabolizerStatus.POOR,
        clinical_recommendations=[
            "'Worrier' fenotyp - ökad prefrontal dopamin",
            "Bättre kognitiv funktion vid vila",
            "Ökad smärtkänslighet",
            "Ökad ångestkänslighet vid stress"
        ],
        nutrient_implications=[
            "UNDVIK höga doser grönt te/EGCG (kan höja dopamin för mycket)",
            "Magnesium för COMT-funktion",
            "B-vitaminer stödjer SAMe-cykling",
            "Adaptogener kan hjälpa stresshantering",
            "Omega-3 för hjärnhälsa"
        ],
        drug_implications=[
            "Långsam östrogennedbrytning - risk vid HRT",
            "Kan behöva lägre dos levodopa",
            "Ökad känslighet för stimulantia",
            "Överväg lägre dos ADHD-medicin"
        ]
    )
]

COMT_GENE = HaplotypeGene(
    gene="COMT",
    category=HaplotypeCategory.NEUROTRANSMITTER,
    description="Katekol-O-metyltransferas - Bryter ned dopamin, noradrenalin och östrogen. "
                "Val158Met påverkar enzymaktivitet 3-4 gånger.",
    snps=COMT_SNPS,
    haplotypes=COMT_HAPLOTYPES,
    diplotypes=COMT_DIPLOTYPES,
    clinical_guidelines=[
        "Met/Met har 3-4x lägre enzymaktivitet än Val/Val",
        "'Warrior vs Worrier' - trade-off mellan stressresistens och kognition",
        "COMT påverkar även östrogenmetabolism",
        "Interagerar med MTHFR för SAMe-tillgång"
    ],
    references=[
        "PMID: 17008817 - COMT Val158Met and cognition",
        "PMID: 19081561 - COMT and stress response",
        "PMID: 21385469 - COMT and pain sensitivity",
        "PMID: 17696763 - COMT and estrogen metabolism"
    ]
)

# =============================================================================
# COMPLETE HAPLOTYPE DATABASE
# =============================================================================

HAPLOTYPE_DATABASE: Dict[str, HaplotypeGene] = {
    "APOE": APOE_GENE,
    "CYP2D6": CYP2D6_GENE,
    "CYP2C19": CYP2C19_GENE,
    "CYP2C9": CYP2C9_GENE,
    "VKORC1": VKORC1_GENE,
    "MTHFR": MTHFR_GENE,
    "HLA-B*57:01": HLA_B5701_GENE,
    "SLCO1B1": SLCO1B1_GENE,
    "COMT": COMT_GENE
}

# =============================================================================
# HAPLOTYPE DETERMINATION FUNCTIONS
# =============================================================================

def determine_apoe_haplotype(rs429358: str, rs7412: str) -> str:
    """
    Bestäm APOE-haplotyp baserat på rs429358 och rs7412.

    rs429358 (C/T) och rs7412 (C/T) kombinationer:
    - e2: T-T (rs429358=T, rs7412=T)
    - e3: T-C (rs429358=T, rs7412=C)
    - e4: C-C (rs429358=C, rs7412=C)
    """
    # Hantera båda strängar
    combinations = []

    for a1 in rs429358:
        for a2 in rs7412:
            if a1 == 'T' and a2 == 'T':
                combinations.append('e2')
            elif a1 == 'T' and a2 == 'C':
                combinations.append('e3')
            elif a1 == 'C' and a2 == 'C':
                combinations.append('e4')

    if len(combinations) == 2:
        combinations.sort()  # e2 < e3 < e4
        return f"{combinations[0]}/{combinations[1]}"
    elif len(combinations) == 1:
        return f"{combinations[0]}/{combinations[0]}"
    else:
        return "Okänd"

def determine_mthfr_status(rs1801133: str, rs1801131: str) -> Dict[str, any]:
    """
    Bestäm MTHFR compound status baserat på C677T och A1298C.

    rs1801133 (G>A): G=C (normal), A=T (variant)
    rs1801131 (T>G): T=A (normal), G=C (variant)
    """
    # Räkna varianter
    c677t_variants = rs1801133.count('A')  # A = T-allel
    a1298c_variants = rs1801131.count('G')  # G = C-allel

    # Bestäm genotyp
    c677t_genotype = {0: "CC", 1: "CT", 2: "TT"}[c677t_variants]
    a1298c_genotype = {0: "AA", 1: "AC", 2: "CC"}[a1298c_variants]

    # Bestäm klinisk betydelse
    if c677t_variants == 2:
        severity = "Signifikant reducerad aktivitet (~30%)"
        recommendation = "ENDAST metylfolat. Undvik folsyra."
    elif c677t_variants == 1 and a1298c_variants >= 1:
        severity = "Compound heterozygot - reducerad aktivitet (~40-50%)"
        recommendation = "Metylfolat rekommenderas starkt"
    elif a1298c_variants == 2:
        severity = "Måttligt reducerad aktivitet (~60%)"
        recommendation = "Metylfolat fördelaktigt"
    elif c677t_variants == 1:
        severity = "Lätt reducerad aktivitet (~85%)"
        recommendation = "Standard eller metylfolat"
    else:
        severity = "Normal aktivitet"
        recommendation = "Standardrekommendationer"

    return {
        "c677t": c677t_genotype,
        "a1298c": a1298c_genotype,
        "phenotype": f"MTHFR {c677t_genotype}/{a1298c_genotype}",
        "severity": severity,
        "recommendation": recommendation
    }

def determine_cyp2d6_activity_score(diplotype: str) -> float:
    """
    Beräkna CYP2D6 activity score baserat på diplotyp.

    Activity scores:
    - *1, *2: 1.0 (normal)
    - *9, *10, *17, *29, *41: 0.5 (reducerad)
    - *3, *4, *5, *6: 0 (null)
    - *1xN, *2xN: 2.0+ (ultra-rapid)
    """
    activity_values = {
        "*1": 1.0,
        "*2": 1.0,
        "*9": 0.5,
        "*10": 0.5,
        "*17": 0.5,
        "*29": 0.5,
        "*41": 0.5,
        "*3": 0,
        "*4": 0,
        "*5": 0,
        "*6": 0,
        "*xN": 2.0  # Förenklad - egentligen varierande
    }

    parts = diplotype.replace("CYP2D6 ", "").split("/")
    total = 0

    for part in parts:
        part = part.strip()
        if part in activity_values:
            total += activity_values[part]
        elif "xN" in part:
            total += 2.0
        else:
            total += 1.0  # Default normal

    return total

def get_metabolizer_status_from_score(score: float) -> MetabolizerStatus:
    """Bestäm metaboliseringsstatus från activity score."""
    if score >= 2.25:
        return MetabolizerStatus.ULTRA_RAPID
    elif score >= 1.25:
        return MetabolizerStatus.NORMAL
    elif score >= 0.25:
        return MetabolizerStatus.INTERMEDIATE
    else:
        return MetabolizerStatus.POOR

# =============================================================================
# LOOKUP FUNCTIONS
# =============================================================================

def get_haplotype_gene(gene: str) -> Optional[HaplotypeGene]:
    """Hämta haplotypinformation för en gen."""
    return HAPLOTYPE_DATABASE.get(gene.upper())

def get_all_haplotype_genes() -> List[str]:
    """Lista alla gener med haplotypdata."""
    return list(HAPLOTYPE_DATABASE.keys())

def get_diplotype_recommendations(gene: str, diplotype: str) -> Optional[Diplotype]:
    """Hämta rekommendationer för en specifik diplotyp."""
    gene_data = HAPLOTYPE_DATABASE.get(gene.upper())
    if not gene_data:
        return None

    for dt in gene_data.diplotypes:
        if dt.phenotype.lower() == diplotype.lower():
            return dt

    return None

def find_relevant_snps_for_haplotypes() -> Dict[str, List[str]]:
    """Returnera alla SNPs som behövs för haplotypbestämning."""
    snps_by_gene = {}

    for gene_name, gene_data in HAPLOTYPE_DATABASE.items():
        snps_by_gene[gene_name] = [snp.rsid for snp in gene_data.snps]

    return snps_by_gene

# =============================================================================
# MAIN / TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GWL HAPLOTYPES & DIPLOTYPES DATABASE")
    print("=" * 70)

    print(f"\nAntal gener med haplotypdata: {len(HAPLOTYPE_DATABASE)}")
    print("\nGener:")
    for gene_name, gene_data in HAPLOTYPE_DATABASE.items():
        print(f"\n{gene_name}:")
        print(f"  Kategori: {gene_data.category.value}")
        print(f"  Antal SNPs: {len(gene_data.snps)}")
        print(f"  Antal haplotyper: {len(gene_data.haplotypes)}")
        print(f"  Antal diplotyper: {len(gene_data.diplotypes)}")

    print("\n" + "-" * 70)
    print("SNPs som behövs för haplotypbestämning:")
    print("-" * 70)

    all_snps = find_relevant_snps_for_haplotypes()
    for gene, snps in all_snps.items():
        print(f"{gene}: {', '.join(snps)}")

    # Test APOE
    print("\n" + "-" * 70)
    print("TEST: APOE-haplotypbestämning")
    print("-" * 70)

    test_cases = [
        ("TC", "CT"),  # e3/e4
        ("TT", "CC"),  # e3/e3
        ("TT", "TT"),  # e2/e2
        ("CC", "CC"),  # e4/e4
    ]

    for rs429358, rs7412 in test_cases:
        result = determine_apoe_haplotype(rs429358, rs7412)
        print(f"rs429358={rs429358}, rs7412={rs7412} -> APOE {result}")

    # Test MTHFR
    print("\n" + "-" * 70)
    print("TEST: MTHFR-statusbestämning")
    print("-" * 70)

    mthfr_tests = [
        ("GG", "TT"),  # Wildtyp
        ("GA", "TT"),  # C677T het
        ("AA", "TT"),  # C677T hom
        ("GG", "GG"),  # A1298C hom
        ("GA", "TG"),  # Compound het
    ]

    for rs1801133, rs1801131 in mthfr_tests:
        result = determine_mthfr_status(rs1801133, rs1801131)
        print(f"rs1801133={rs1801133}, rs1801131={rs1801131}")
        print(f"  -> {result['phenotype']}: {result['severity']}")

    print("\n" + "=" * 70)
    print("Databas laddad och testad!")
    print("=" * 70)
