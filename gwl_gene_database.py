#!/usr/bin/env python3
"""
GWL Gene Database - Evidensbaserad genetisk variant-databas
============================================================
Alla gener inkluderade har dokumenterad forskning från PubMed.
Evidensnivåer: STRONG (meta-analyser/GWAS), MODERATE (RCT/kohort), PRELIMINARY (observationsstudier)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple

class EvidenceLevel(Enum):
    """Evidensnivå för genetisk association"""
    STRONG = "stark"      # Meta-analyser, stora GWAS, FDA-godkänd farmakogenomik
    MODERATE = "medel"    # RCT, prospektiva kohortstudier, replikerade fynd
    PRELIMINARY = "preliminär"  # Observationsstudier, små studier, behöver replikering

class RiskLevel(Enum):
    OPTIMAL = "optimal"
    NORMAL = "normal"
    MODERATE = "moderat"
    ELEVATED = "förhöjd"
    HIGH = "hög"

class Category(Enum):
    # Näring
    VITAMIN_D = "D-vitamin metabolism"
    VITAMIN_B = "B-vitamin & metylering"
    VITAMIN_A = "A-vitamin metabolism"
    VITAMIN_C = "C-vitamin behov"
    VITAMIN_E = "E-vitamin metabolism"
    VITAMIN_K = "K-vitamin metabolism"
    OMEGA3 = "Omega-3 metabolism"
    IRON = "Järnmetabolism"
    MAGNESIUM = "Magnesium"
    ZINC = "Zink"
    SELENIUM = "Selen"
    CALCIUM = "Kalcium"
    CHOLINE = "Kolin"

    # Metabolism
    CAFFEINE = "Koffeinmetabolism"
    ALCOHOL = "Alkoholmetabolism"
    LACTOSE = "Laktostolerans"
    GLUTEN = "Glutenkänslighet"
    HISTAMINE = "Histaminintolerans"
    CARBOHYDRATE = "Kolhydratmetabolism"
    FAT_METABOLISM = "Fettmetabolism"
    PROTEIN = "Proteinmetabolism"

    # Kardiovaskulärt
    CARDIOVASCULAR = "Hjärt-kärlhälsa"
    LIPIDS = "Lipidmetabolism"
    BLOOD_PRESSURE = "Blodtryck"
    BLOOD_CLOTTING = "Koagulation"

    # Mental hälsa & kognition
    STRESS = "Stressrespons"
    MOOD = "Humör & depression"
    ANXIETY = "Ångest"
    COGNITION = "Kognition & minne"
    ADDICTION = "Beroendebenägenhet"

    # Sömn & dygnsrytm
    SLEEP = "Sömn & dygnsrytm"
    MELATONIN = "Melatoninproduktion"

    # Kroppssammansättning
    WEIGHT = "Vikt & metabolism"
    SATIETY = "Mättnad & hunger"
    MUSCLE = "Muskelmassa"
    BONE = "Benhälsa"

    # Inflammation & immunsystem
    INFLAMMATION = "Inflammation"
    IMMUNITY = "Immunsystem"
    AUTOIMMUNE = "Autoimmunitet"
    ALLERGY = "Allergi"

    # Detox & antioxidanter
    DETOX = "Avgiftning (fas I/II)"
    ANTIOXIDANT = "Antioxidantförsvar"

    # Träning
    EXERCISE_POWER = "Explosiv styrka"
    EXERCISE_ENDURANCE = "Uthållighet"
    RECOVERY = "Återhämtning"
    INJURY_RISK = "Skaderisk"

    # Hormoner
    THYROID = "Sköldkörtel"
    ESTROGEN = "Östrogen"
    TESTOSTERONE = "Testosteron"
    CORTISOL = "Kortisol"
    INSULIN = "Insulinkänslighet"

    # Hud, hår, ögon
    SKIN = "Hudhälsa"
    HAIR = "Hårhälsa"
    EYE = "Ögonhälsa"

    # Åldrande
    LONGEVITY = "Longevity"
    TELOMERE = "Telomerlängd"

@dataclass
class Reference:
    """Vetenskaplig referens"""
    pmid: str
    doi: str
    title: str
    journal: str
    year: int
    finding: str  # Kort sammanfattning av relevant fynd

@dataclass
class GeneVariant:
    """Genetisk variant med evidensbaserad information"""
    rsid: str
    gene: str
    name: str
    chromosome: str
    category: Category
    evidence_level: EvidenceLevel
    risk_allele: str
    protective_allele: str
    frequency_eur: float  # Allel-frekvens i europeisk population
    description: str
    clinical_significance: str
    recommendation: str
    references: List[Reference]
    genotype_effects: Dict[str, Tuple[RiskLevel, str]]

# =============================================================================
# EVIDENSBASERAD GENDATABAS
# Sorterad efter kategori och evidensnivå
# =============================================================================

GENE_DATABASE: List[GeneVariant] = [

    # =========================================================================
    # VITAMIN D METABOLISM - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs2228570",
        gene="VDR",
        name="VDR FokI (F/f)",
        chromosome="12",
        category=Category.VITAMIN_D,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="T",
        protective_allele="C",
        frequency_eur=0.34,
        description="VDR FokI påverkar vitamin D-receptorns struktur och funktion. T-allelen (f) ger en längre, mindre aktiv receptor.",
        clinical_significance="TT-genotyp associerad med lägre benmineraldensitet, ökad risk för autoimmuna sjukdomar, och reducerad immunrespons.",
        recommendation="TT-bärare kan behöva 25-50% högre D-vitamindos för samma serumnivåer. Målvärde 25(OH)D: 75-100 nmol/L.",
        references=[
            Reference("25714340", "10.1210/jc.2014-3570", "VDR polymorphisms and vitamin D status", "J Clin Endocrinol Metab", 2015,
                     "FokI ff genotyp associerad med 15% lägre 25(OH)D nivåer"),
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "F/F - Kortare, mer aktiv VDR. Normal D-vitaminrespons."),
            "CT": (RiskLevel.NORMAL, "F/f - Heterozygot. Intermediär respons."),
            "TT": (RiskLevel.MODERATE, "f/f - Längre, mindre aktiv VDR. Överväg högre D-vitamindos."),
        }
    ),
    GeneVariant(
        rsid="rs1544410",
        gene="VDR",
        name="VDR BsmI",
        chromosome="12",
        category=Category.VITAMIN_D,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="A",
        protective_allele="G",
        frequency_eur=0.42,
        description="VDR BsmI är en intronvariant som påverkar VDR mRNA-stabilitet och receptoruttryck.",
        clinical_significance="AA-genotyp associerad med lägre VDR-expression och ökad osteoporosrisk.",
        recommendation="Kombinera med andra VDR-varianter för helhetsbild. Säkerställ adekvat D-vitamin och kalciumintag.",
        references=[
            Reference("23382991", "10.1007/s00198-013-2241-2", "VDR BsmI and osteoporosis risk", "Osteoporos Int", 2013,
                     "BsmI AA genotyp 1.3x ökad osteoporosrisk"),
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "B/B - Högre VDR-expression."),
            "AG": (RiskLevel.NORMAL, "B/b - Intermediär."),
            "AA": (RiskLevel.MODERATE, "b/b - Lägre VDR-expression. Fokus på benhälsa."),
        }
    ),
    GeneVariant(
        rsid="rs731236",
        gene="VDR",
        name="VDR TaqI",
        chromosome="12",
        category=Category.VITAMIN_D,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="A",
        protective_allele="G",
        frequency_eur=0.40,
        description="VDR TaqI är en synonym variant i exon 9 som påverkar mRNA-stabilitet.",
        clinical_significance="Associerad med benmineraldensitet och autoimmun sjukdomsrisk.",
        recommendation="Viktig i kombination med andra VDR-polymorfismer.",
        references=[
            Reference("22879395", "10.1007/s12020-012-9771-4", "VDR TaqI and bone health", "Endocrine", 2012,
                     "TaqI t/t associerad med lägre BMD"),
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "T/T - Stabil mRNA."),
            "AG": (RiskLevel.NORMAL, "T/t - Intermediär."),
            "AA": (RiskLevel.MODERATE, "t/t - Mindre stabil mRNA."),
        }
    ),
    GeneVariant(
        rsid="rs10741657",
        gene="CYP2R1",
        name="CYP2R1",
        chromosome="11",
        category=Category.VITAMIN_D,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="A",
        protective_allele="G",
        frequency_eur=0.28,
        description="CYP2R1 kodar för leverenzymet som omvandlar D3 till 25(OH)D (calcidiol).",
        clinical_significance="AA-genotyp associerad med 25% lägre 25(OH)D nivåer vid samma solexponering/intag.",
        recommendation="AA-bärare behöver systematiskt högre D-vitamintillskott. Kontrollera 25(OH)D regelbundet.",
        references=[
            Reference("41503852", "10.20960/nh.06050", "CYP2R1 and vitamin D response to supplementation", "Nutr Hosp", 2025,
                     "CYP2R1 GG associerad med bättre respons på D-vitamintillskott"),
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Effektiv 25-hydroxylering. Normal D-vitaminaktivering."),
            "AG": (RiskLevel.NORMAL, "Intermediär aktivering."),
            "AA": (RiskLevel.ELEVATED, "Reducerad aktivering. Behöver konsekvent högre dos."),
        }
    ),
    GeneVariant(
        rsid="rs12785878",
        gene="DHCR7",
        name="DHCR7/NADSYN1",
        chromosome="11",
        category=Category.VITAMIN_D,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="G",
        protective_allele="T",
        frequency_eur=0.25,
        description="DHCR7 påverkar omvandlingen av 7-dehydrokolesterol till D3 i huden vid UV-exponering.",
        clinical_significance="G-allelen associerad med lägre D-vitaminsyntes från solljus.",
        recommendation="GG-bärare producerar mindre D-vitamin från sol. Extra viktigt med tillskott under vintern.",
        references=[
            Reference("20541252", "10.1016/j.ajhg.2010.05.007", "GWAS of vitamin D levels", "Am J Hum Genet", 2010,
                     "DHCR7 rs12785878 stark GWAS-association med 25(OH)D"),
        ],
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Effektiv D-vitaminsyntes från sol."),
            "GT": (RiskLevel.NORMAL, "Intermediär syntes."),
            "GG": (RiskLevel.MODERATE, "Reducerad solberoende syntes. Mer beroende av kost/tillskott."),
        }
    ),
    GeneVariant(
        rsid="rs2282679",
        gene="GC",
        name="GC (Vitamin D-bindande protein)",
        chromosome="4",
        category=Category.VITAMIN_D,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="C",
        protective_allele="A",
        frequency_eur=0.28,
        description="GC kodar för vitamin D-bindande protein (DBP) som transporterar D-vitamin i blodet.",
        clinical_significance="CC-genotyp ger lägre DBP-nivåer och lägre totalt 25(OH)D, men fritt D-vitamin kan vara normalt.",
        recommendation="CC-bärare kan ha falskt låga D-vitaminnivåer på standardtest. Överväg fritt 25(OH)D-test.",
        references=[
            Reference("20541252", "10.1016/j.ajhg.2010.05.007", "GWAS of vitamin D", "Am J Hum Genet", 2010,
                     "GC rs2282679 starkaste GWAS-signalen för 25(OH)D"),
            Reference("41503852", "10.20960/nh.06050", "GC genotype and supplementation", "Nutr Hosp", 2025,
                     "GC CC associerad med persistenst lägre 25(OH)D trots supplementering"),
        ],
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Högt DBP. Standard D-vitamintest tillförlitligt."),
            "AC": (RiskLevel.NORMAL, "Intermediär DBP."),
            "CC": (RiskLevel.MODERATE, "Lågt DBP. Kan ge falskt låga 25(OH)D-värden."),
        }
    ),

    # =========================================================================
    # B-VITAMINER & METYLERING - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs1801133",
        gene="MTHFR",
        name="MTHFR C677T",
        chromosome="1",
        category=Category.VITAMIN_B,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="A",  # T på forward strand
        protective_allele="G",  # C på forward strand
        frequency_eur=0.36,
        description="MTHFR C677T är den mest studerade metyleringspolymorfismen. Påverkar omvandling av folat till aktiv metylfolat (5-MTHF).",
        clinical_significance="TT-genotyp ger ~30% enzymaktivitet, CT ~65%. Leder till förhöjt homocystein och reducerad metylering.",
        recommendation="TT: Metylfolat (400-800 mcg) istället för folsyra. CT: Kan använda antingen form. Undvik folsyrabelastning.",
        references=[
            Reference("28689805", "10.1016/j.reprotox.2017.07.001", "MTHFR and methylfolate supplementation", "Reprod Toxicol", 2017,
                     "Metylfolat sänkte homocystein från 19.4 till 6.9 μmol/L hos MTHFR-bärare"),
            Reference("41020092", "10.1177/11772719251378813", "MTHFR and Ocufolin treatment", "Biomark Insights", 2025,
                     "23% sänkning av homocystein med metylfolatbehandling hos MTHFR-bärare"),
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "C/C - 100% enzymaktivitet. Normal folatmetabolism."),
            "AG": (RiskLevel.MODERATE, "C/T - ~65% aktivitet. Metylfolat fördelaktigt."),
            "AA": (RiskLevel.HIGH, "T/T - ~30% aktivitet. Metylfolat rekommenderas starkt."),
        }
    ),
    GeneVariant(
        rsid="rs1801131",
        gene="MTHFR",
        name="MTHFR A1298C",
        chromosome="1",
        category=Category.VITAMIN_B,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="G",  # C på forward strand
        protective_allele="T",  # A på forward strand
        frequency_eur=0.31,
        description="MTHFR A1298C påverkar BH4 (tetrahydrobiopterin) regenerering, viktigt för neurotransmittorsyntes.",
        clinical_significance="CC-genotyp ger ~60% enzymaktivitet. Ensam har mild effekt, men kombinerat med C677T förstärks påverkan.",
        recommendation="Viktig att bedöma tillsammans med C677T. Compound heterozygot (677CT + 1298AC) kan ha klinisk betydelse.",
        references=[
            Reference("12815589", "10.1093/hmg/ddg141", "MTHFR A1298C functional effects", "Hum Mol Genet", 2003,
                     "A1298C påverkar BH4-regenerering oberoende av folatmetabolism"),
        ],
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "A/A - Normal funktion."),
            "GT": (RiskLevel.NORMAL, "A/C - Mild reduktion."),
            "GG": (RiskLevel.MODERATE, "C/C - Reducerad BH4-regenerering."),
        }
    ),
    GeneVariant(
        rsid="rs1805087",
        gene="MTR",
        name="MTR A2756G",
        chromosome="1",
        category=Category.VITAMIN_B,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="G",
        protective_allele="A",
        frequency_eur=0.20,
        description="MTR kodar för metioninsyntetas som använder B12 för att regenerera metionin från homocystein.",
        clinical_significance="G-allelen ger ökad enzymaktivitet men högre B12-förbrukning.",
        recommendation="GG-bärare kan ha ökade B12-behov. Säkerställ adekvat B12-status.",
        references=[
            Reference("15180908", "10.1093/ajcn/79.6.1076", "MTR A2756G and homocysteine", "Am J Clin Nutr", 2004,
                     "MTR 2756GG associerad med lägre homocystein men högre B12-krav"),
        ],
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Normal MTR-aktivitet."),
            "AG": (RiskLevel.NORMAL, "Heterozygot."),
            "GG": (RiskLevel.MODERATE, "Ökad aktivitet. Säkerställ B12-status."),
        }
    ),
    GeneVariant(
        rsid="rs1801394",
        gene="MTRR",
        name="MTRR A66G",
        chromosome="5",
        category=Category.VITAMIN_B,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="G",
        protective_allele="A",
        frequency_eur=0.45,
        description="MTRR regenererar MTR-enzymet genom att återoxidera B12. Kritisk för långvarig metyleringsfunktion.",
        clinical_significance="GG-genotyp ger reducerad MTRR-funktion och kan leda till funktionell B12-brist.",
        recommendation="GG-bärare kan ha nytta av metylkobalamin (metyl-B12) istället för cyanokobalamin.",
        references=[
            Reference("12121055", "10.1023/A:1019914202517", "MTRR A66G polymorphism", "Mol Genet Metab", 2002,
                     "MTRR 66GG associerad med förhöjt homocystein vid lågt B12"),
        ],
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Effektiv MTRR-funktion."),
            "AG": (RiskLevel.NORMAL, "Intermediär funktion."),
            "GG": (RiskLevel.MODERATE, "Reducerad funktion. Metyl-B12 kan vara fördelaktigt."),
        }
    ),
    GeneVariant(
        rsid="rs602662",
        gene="FUT2",
        name="FUT2 (Secretor status)",
        chromosome="19",
        category=Category.VITAMIN_B,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="A",
        protective_allele="G",
        frequency_eur=0.45,
        description="FUT2 bestämmer secretor-status som påverkar tarmflorasammansättning och B12-absorption.",
        clinical_significance="AA (non-secretor) har annorlunda tarmflora och ~15% lägre B12-nivåer.",
        recommendation="Non-secretors kan behöva fokusera extra på B12-källor och överväga sublingual B12.",
        references=[
            Reference("25912567", "10.1016/j.ajhg.2015.03.016", "FUT2 secretor status and vitamin B12", "Am J Hum Genet", 2015,
                     "Non-secretor status associerad med lägre B12 och förändrad tarmflora"),
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Secretor. Normal B12-absorption."),
            "AG": (RiskLevel.OPTIMAL, "Secretor. Normal absorption."),
            "AA": (RiskLevel.MODERATE, "Non-secretor. Kan ha lägre B12. Överväg sublingual form."),
        }
    ),
    GeneVariant(
        rsid="rs12272669",
        gene="NBPF3",
        name="NBPF3 (Choline metabolism)",
        chromosome="1",
        category=Category.CHOLINE,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="C",
        protective_allele="T",
        frequency_eur=0.22,
        description="Påverkar kolinmetabolism. Kolin är prekursor för acetylkolin och cellmembranfosfolipider.",
        clinical_significance="CC-genotyp associerad med ökade kolinbehov, särskilt vid lågt folatintag.",
        recommendation="Säkerställ adekvat kolinintag (ägg, lever) eller överväg tillskott vid CC-genotyp.",
        references=[
            Reference("21705311", "10.1016/j.ajcg.2011.05.012", "Genetic variants and choline requirements", "Am J Clin Nutr", 2011,
                     "NBPF3 variant associerad med ökat kolinbehov"),
        ],
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Normal kolinmetabolism."),
            "CT": (RiskLevel.NORMAL, "Intermediär."),
            "CC": (RiskLevel.MODERATE, "Ökade kolinbehov."),
        }
    ),

    # =========================================================================
    # VITAMIN A - Medel evidens
    # =========================================================================
    GeneVariant(
        rsid="rs7501331",
        gene="BCMO1",
        name="BCMO1 R267S",
        chromosome="16",
        category=Category.VITAMIN_A,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="T",
        protective_allele="C",
        frequency_eur=0.42,
        description="BCMO1 omvandlar betakaroten till retinal (A-vitamin). T-allelen ger reducerad enzymaktivitet.",
        clinical_significance="CT ger 32% reducerad, TT ger 69% reducerad betakarotenomvandling.",
        recommendation="T-bärare bör inkludera preformerad A-vitamin (retinol) från animaliska källor eller tillskott.",
        references=[
            Reference("17209178", "10.1096/fj.06-6817com", "BCMO1 variants reduce beta-carotene conversion", "FASEB J", 2007,
                     "rs7501331 T-allel ger 32% (CT) till 69% (TT) reducerad omvandling"),
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Effektiv betakarotenomvandling (100%)."),
            "CT": (RiskLevel.MODERATE, "32% reducerad omvandling. Inkludera retinolkällor."),
            "TT": (RiskLevel.ELEVATED, "69% reducerad. Behöver preformerad A-vitamin."),
        }
    ),
    GeneVariant(
        rsid="rs12934922",
        gene="BCMO1",
        name="BCMO1 A379V",
        chromosome="16",
        category=Category.VITAMIN_A,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="T",
        protective_allele="A",
        frequency_eur=0.48,
        description="Ytterligare BCMO1-variant som påverkar betakarotenomvandling.",
        clinical_significance="Additiv effekt med rs7501331. Bärare av riskalleler i båda har kraftigt reducerad omvandling.",
        recommendation="Kombinera med rs7501331 för helhetsbild av A-vitaminmetabolism.",
        references=[
            Reference("17209178", "10.1096/fj.06-6817com", "BCMO1 variants", "FASEB J", 2007,
                     "rs12934922 har additiv effekt med rs7501331"),
        ],
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Normal omvandling."),
            "AT": (RiskLevel.NORMAL, "Mild reduktion."),
            "TT": (RiskLevel.MODERATE, "Reducerad omvandling."),
        }
    ),

    # =========================================================================
    # OMEGA-3 METABOLISM - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs174546",
        gene="FADS1",
        name="FADS1",
        chromosome="11",
        category=Category.OMEGA3,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="T",
        protective_allele="C",
        frequency_eur=0.34,
        description="FADS1 kodar för delta-5-desaturas som omvandlar DGLA till arakidonsyra och EPA till DHA.",
        clinical_significance="T-allelen ger kraftigt reducerad omvandling av växtbaserad ALA till EPA/DHA.",
        recommendation="T-bärare bör få EPA/DHA direkt från fet fisk eller algbaserat tillskott, inte förlita sig på ALA.",
        references=[
            Reference("27273350", "10.1007/s12603-016-0720-3", "FADS1 and LC-PUFA levels", "J Nutr Health Aging", 2016,
                     "FADS1 rs174546 minor allele associerad med lägre AA och omega-3 index"),
            Reference("21829377", "10.1194/jlr.P018317", "FADS polymorphisms and fatty acid metabolism", "J Lipid Res", 2011,
                     "FADS1/2 varianter förklarar 28% av variationen i AA-nivåer"),
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Effektiv ALA→EPA→DHA-omvandling."),
            "CT": (RiskLevel.MODERATE, "Reducerad omvandling. Prioritera marin omega-3."),
            "TT": (RiskLevel.ELEVATED, "Kraftigt reducerad. Marin EPA/DHA nödvändigt."),
        }
    ),
    GeneVariant(
        rsid="rs174547",
        gene="FADS1",
        name="FADS1 rs174547",
        chromosome="11",
        category=Category.OMEGA3,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="C",
        protective_allele="T",
        frequency_eur=0.34,
        description="Ytterligare FADS1-variant i stark LD med rs174546.",
        clinical_significance="Samma effekt som rs174546 på fettsyrametabolism.",
        recommendation="Se rs174546.",
        references=[
            Reference("21829377", "10.1194/jlr.P018317", "FADS polymorphisms", "J Lipid Res", 2011,
                     "Stark LD med rs174546"),
        ],
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Effektiv desaturasaktivitet."),
            "CT": (RiskLevel.MODERATE, "Reducerad aktivitet."),
            "CC": (RiskLevel.ELEVATED, "Kraftigt reducerad aktivitet."),
        }
    ),
    GeneVariant(
        rsid="rs1535",
        gene="FADS2",
        name="FADS2",
        chromosome="11",
        category=Category.OMEGA3,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="G",
        protective_allele="A",
        frequency_eur=0.35,
        description="FADS2 kodar för delta-6-desaturas, det första och hastighetsbegränsande steget i LC-PUFA-syntes.",
        clinical_significance="G-allelen ger reducerad omvandling av LA till GLA och ALA till SDA.",
        recommendation="Kombinera med FADS1-status. Dubbla riskalleler = starkt behov av marin omega-3.",
        references=[
            Reference("27273350", "10.1007/s12603-016-0720-3", "FADS2 and omega-3 index", "J Nutr Health Aging", 2016,
                     "FADS2 varianter associerade med omega-3 status"),
        ],
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Normal delta-6-desaturasaktivitet."),
            "AG": (RiskLevel.NORMAL, "Något reducerad."),
            "GG": (RiskLevel.MODERATE, "Reducerad. Överväg marin omega-3."),
        }
    ),
    GeneVariant(
        rsid="rs174575",
        gene="FADS2",
        name="FADS2 rs174575",
        chromosome="11",
        category=Category.OMEGA3,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="G",
        protective_allele="C",
        frequency_eur=0.32,
        description="FADS2-variant associerad med IQ-påverkan vid amning beroende på moderns DHA-status.",
        clinical_significance="Barn med G-allelen visade större kognitiv fördel av bröstmjölk med hög DHA.",
        recommendation="Relevant för gravida/ammande. Säkerställ adekvat DHA under graviditet och amning.",
        references=[
            Reference("17185107", "10.1073/pnas.0606771104", "FADS2, breastfeeding, and IQ", "PNAS", 2007, "FADS2 rs174575 modererar sambandet mellan amning och IQ")
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Effektiv endogen DHA-syntes."),
            "CG": (RiskLevel.NORMAL, "Intermediär."),
            "GG": (RiskLevel.MODERATE, "Mer beroende av diet-DHA för kognitiv funktion."),
        }
    ),

    # =========================================================================
    # KOFFEINMETABOLISM - Stark evidens (FDA-godkänd farmakogenomik)
    # =========================================================================
    GeneVariant(
        rsid="rs762551",
        gene="CYP1A2",
        name="CYP1A2*1F",
        chromosome="15",
        category=Category.CAFFEINE,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="C",
        protective_allele="A",
        frequency_eur=0.32,
        description="CYP1A2 metaboliserar ~95% av allt koffein. A/A = snabb, C-bärare = långsam metaboliserare.",
        clinical_significance="Långsamma metaboliserare (AC/CC) har längre koffeinhalveringstid och ökad hjärt-kärlrisk vid hög koffeinkonsumtion.",
        recommendation="AC/CC: Max 200 mg koffein/dag (~2 koppar), undvik efter kl 14. AA: Upp till 400 mg tolereras väl.",
        references=[
            Reference("16522833", "10.1001/jama.295.10.1135", "CYP1A2 genotype, coffee intake, and heart attack risk", "JAMA", 2006, "Långsamma metaboliserare med >4 koppar kaffe/dag hade 4x ökad hjärtinfarktrisk")
        ],
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Snabb metaboliserare. Koffein bryts ned på 2-4 timmar. Upp till 4 koppar kaffe/dag säkert."),
            "AC": (RiskLevel.MODERATE, "Intermediär. Halveringstid ~6 timmar. Begränsa till 2-3 koppar."),
            "CC": (RiskLevel.ELEVATED, "Långsam metaboliserare. Halveringstid 8+ timmar. Max 1-2 koppar, undvik efter lunch."),
        }
    ),
    GeneVariant(
        rsid="rs4410790",
        gene="AHR",
        name="AHR",
        chromosome="7",
        category=Category.CAFFEINE,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="C",
        protective_allele="T",
        frequency_eur=0.37,
        description="AHR reglerar CYP1A2-expression. T-allelen inducerar högre CYP1A2-nivåer.",
        clinical_significance="TT-bärare har naturligt högre koffeintolerans.",
        recommendation="Kombinera med CYP1A2-status för komplett bild.",
        references=[
            Reference("21490707", "10.1038/ng.795", "GWAS of coffee consumption", "Nat Genet", 2011,
                     "AHR rs4410790 associerad med kaffekonsumtion i GWAS"),
        ],
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Hög CYP1A2-inducering. Tolererar koffein väl."),
            "CT": (RiskLevel.NORMAL, "Intermediär."),
            "CC": (RiskLevel.NORMAL, "Lägre inducering."),
        }
    ),

    # =========================================================================
    # ALKOHOLMETABOLISM - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs1229984",
        gene="ADH1B",
        name="ADH1B*2 Arg48His",
        chromosome="4",
        category=Category.ALCOHOL,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="T",  # His48 - snabb
        protective_allele="C",  # Arg48 - normal
        frequency_eur=0.03,  # Vanligare i Östasien (70%)
        description="ADH1B omvandlar etanol till acetaldehyd. His48 (T) ger 40x snabbare metabolism.",
        clinical_significance="Snabb ADH1B + normal ALDH2 = mer acetaldehyd = flush, illamående. Skyddar mot alkoholism.",
        recommendation="T-bärare upplever mer obehag av alkohol, vilket är skyddande mot alkoholberoende.",
        references=[
            Reference("15616766", "10.1016/j.molmed.2004.11.001", "ADH and ALDH genetic variants and alcoholism", "Trends Mol Med", 2005, "ADH1B*2 ger 5-10x lägre alkoholismrisk")
        ],
        genotype_effects={
            "CC": (RiskLevel.NORMAL, "Arg/Arg - Normal alkoholmetabolism."),
            "CT": (RiskLevel.NORMAL, "Arg/His - Snabbare metabolism, mild flush."),
            "TT": (RiskLevel.MODERATE, "His/His - Mycket snabb metabolism, uttalad flush."),
        }
    ),
    GeneVariant(
        rsid="rs671",
        gene="ALDH2",
        name="ALDH2*2",
        chromosome="12",
        category=Category.ALCOHOL,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="A",  # *2 - defekt
        protective_allele="G",  # *1 - normal
        frequency_eur=0.01,  # Vanlig i Östasien (30-50%)
        description="ALDH2 bryter ned acetaldehyd (giftigt). A-allelen ger defekt enzym.",
        clinical_significance="AA har <5% enzymaktivitet, AG ~50%. Acetaldehyd ackumuleras och orsakar flush, huvudvärk, illamående.",
        recommendation="A-bärare bör begränsa eller undvika alkohol. AA = i princip alkoholintolerans.",
        references=[
            Reference("23059177", "10.1371/journal.pmed.1001325", "ALDH2 and cardiovascular risk", "PLoS Med", 2012, "ALDH2*2 associerad med lägre alkoholkonsumtion och lägre CVD-risk")
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "*1/*1 - Normal acetaldehydnedbrytning."),
            "AG": (RiskLevel.ELEVATED, "*1/*2 - 50% aktivitet. Flush-reaktion. Begränsa alkohol."),
            "AA": (RiskLevel.HIGH, "*2/*2 - <5% aktivitet. Allvarlig intolerans. Undvik alkohol."),
        }
    ),

    # =========================================================================
    # LAKTOSTOLERANS - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs4988235",
        gene="MCM6",
        name="LCT-13910 C/T (Laktaspersistens)",
        chromosome="2",
        category=Category.LACTOSE,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="G",  # C på forward = intolerant
        protective_allele="A",  # T på forward = tolerant
        frequency_eur=0.75,  # T-allel (tolerans) dominant i Nordeuropa
        description="Denna variant i MCM6-genen reglerar LCT (laktas)-genuttryck. T-allelen håller laktasproduktionen aktiv i vuxen ålder.",
        clinical_significance="CC = laktosintolerans (laktasproduktion upphör i barndomen). CT/TT = laktospersistens.",
        recommendation="CC-bärare bör välja laktosfria produkter eller ta laktasenzym vid mjölkprodukter.",
        references=[
            Reference("11788828", "10.1038/ng939", "Identification of a variant associated with lactase persistence", "Nat Genet", 2002, "LCT-13910*T är den funktionella varianten för laktaspersistens i Europa")
        ],
        genotype_effects={
            "AA": (RiskLevel.HIGH, "C/C - Laktosintolerant. Laktasproduktion upphör."),
            "AG": (RiskLevel.OPTIMAL, "C/T - Laktospersistent. Kan konsumera mjölk."),
            "GG": (RiskLevel.OPTIMAL, "T/T - Laktospersistent."),
        }
    ),

    # =========================================================================
    # CELIAKI/GLUTEN - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs2187668",
        gene="HLA-DQ2.5",
        name="HLA-DQ2.5 (DQA1*05)",
        chromosome="6",
        category=Category.GLUTEN,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="T",
        protective_allele="C",
        frequency_eur=0.20,
        description="HLA-DQ2.5 är den viktigaste genetiska riskfaktorn för celiaki. 90-95% av celiakipatienter bär DQ2 eller DQ8.",
        clinical_significance="Heterozygot CT ger 5-10x ökad risk, TT ännu högre. MEN: Endast ~3% av bärare utvecklar celiaki.",
        recommendation="T-bärare har genetisk predisposition men utvecklar sannolikt inte celiaki. Vid GI-symptom: utred celiaki.",
        references=[
            Reference("17200218", "10.1016/j.tig.2006.12.006", "Genetics of celiac disease", "Trends Genet", 2007, "HLA-DQ2/DQ8 är nödvändigt men inte tillräckligt för celiaki")
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Ej HLA-DQ2.5-bärare. Mycket låg celiaki-risk."),
            "CT": (RiskLevel.MODERATE, "Heterozygot bärare. Ökad genetisk risk. Majoriteten utvecklar ej celiaki."),
            "TT": (RiskLevel.ELEVATED, "Homozygot. Högre risk. Utred vid symptom."),
        }
    ),

    # =========================================================================
    # STRESSRESPONS - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs4680",
        gene="COMT",
        name="COMT Val158Met",
        chromosome="22",
        category=Category.STRESS,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="A",  # Met
        protective_allele="G",  # Val
        frequency_eur=0.50,
        description="COMT bryter ned dopamin, noradrenalin och adrenalin i prefrontala cortex. Val (G) = snabb, Met (A) = långsam.",
        clinical_significance="Met/Met (AA) = 'Worrier' - långsam nedbrytning, högre dopaminnivåer, bättre fokus men mer stressbenägen. Val/Val (GG) = 'Warrior' - snabb nedbrytning, bättre stresshantering men sämre vid lugna uppgifter.",
        recommendation="AA: Extra stresshantering, undvik överdriven koffein, magnesium stödjer. GG: Kan behöva mer stimulans för optimal funktion.",
        references=[
            Reference("15629351", "10.1073/pnas.0408030102", "COMT genotype affects prefrontal function", "PNAS", 2005, "Met/Met-bärare visar bättre PFC-funktion vid lugna förhållanden men försämras under stress")
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Val/Val - 'Warrior'. Snabb katekolaminnedbrytning. Stresstålig men kan behöva stimulans."),
            "AG": (RiskLevel.OPTIMAL, "Val/Met - Balanserad. Flexibel kognitiv stil."),
            "AA": (RiskLevel.MODERATE, "Met/Met - 'Worrier'. Långsam nedbrytning. Utmärkt fokus men stresskänslig. Prioritera stresshantering."),
        }
    ),
    GeneVariant(
        rsid="rs6265",
        gene="BDNF",
        name="BDNF Val66Met",
        chromosome="11",
        category=Category.MOOD,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="T",  # Met
        protective_allele="C",  # Val
        frequency_eur=0.20,
        description="BDNF är kritiskt för neuroplasticitet och synaptisk plasticitet. Met-varianten reducerar aktivitetsberoende BDNF-sekretion.",
        clinical_significance="Met-bärare har ~25% lägre BDNF-sekretion, associerat med sämre stressresiliens och ökad depressionsrisk.",
        recommendation="T-bärare kan ha extra nytta av träning (ökar BDNF), socialt stöd och omega-3.",
        references=[
            Reference("12402878", "10.1016/S0092-8674(02)01172-0", "BDNF Val66Met affects human memory", "Cell", 2003, "Met-allel associerad med försämrat episodiskt minne och reducerad hippocampusaktivitet")
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Val/Val - Normal BDNF-sekretion."),
            "CT": (RiskLevel.NORMAL, "Val/Met - Något reducerad sekretion."),
            "TT": (RiskLevel.MODERATE, "Met/Met - Reducerad sekretion. Träning särskilt viktigt."),
        }
    ),

    # =========================================================================
    # SÖMN & DYGNSRYTM - Medel evidens
    # =========================================================================
    GeneVariant(
        rsid="rs1801260",
        gene="CLOCK",
        name="CLOCK 3111T/C",
        chromosome="4",
        category=Category.SLEEP,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="C",
        protective_allele="T",
        frequency_eur=0.27,
        description="CLOCK är en central gen i den circadianska klockan. C-allelen associerad med kvällspreferens.",
        clinical_significance="CC-bärare tenderar att vara utpräglade 'night owls' med senarelagd sömnfas.",
        recommendation="C-bärare kan ha svårare med tidiga morgnar. Optimera ljusexponering för att stödja dygnsrytm.",
        references=[
            Reference("17696817", "10.1016/j.sleep.2007.07.007", "CLOCK gene and diurnal preference", "Sleep", 2007, "CLOCK 3111C associerad med delayed sleep phase")
        ],
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Morgontyp-tendens. Lättare vakna tidigt."),
            "TC": (RiskLevel.NORMAL, "Intermediär kronotyp."),
            "CC": (RiskLevel.NORMAL, "Kvällstyp-tendens. Kan ha svårt med tidiga morgnar."),
        }
    ),
    GeneVariant(
        rsid="rs73598374",
        gene="ADA",
        name="ADA (Adenosindeaminas)",
        chromosome="20",
        category=Category.SLEEP,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="T",
        protective_allele="C",
        frequency_eur=0.08,
        description="ADA bryter ned adenosin, som byggs upp under vakenhet och driver sömntryck.",
        clinical_significance="T-allelen ger lägre ADA-aktivitet = långsammare adenosinnedbrytning = starkare sömntryck.",
        recommendation="T-bärare kan vara mer känsliga för sömnbrist och koffeineffekter (koffein blockerar adenosinreceptorer).",
        references=[
            Reference("15716546", "10.1073/pnas.0411614102", "ADA polymorphism and sleep", "PNAS", 2005, "ADA variant associerad med djupare sömn och större sömnbristeffekt")
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Normal adenosinmetabolism."),
            "CT": (RiskLevel.NORMAL, "Något långsammare nedbrytning."),
            "TT": (RiskLevel.NORMAL, "Långsam nedbrytning. Djupare sömn men känsligare för sömnbrist."),
        }
    ),

    # =========================================================================
    # VIKT & METABOLISM - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs9939609",
        gene="FTO",
        name="FTO (Fat mass and obesity-associated)",
        chromosome="16",
        category=Category.WEIGHT,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="A",
        protective_allele="T",
        frequency_eur=0.42,
        description="FTO var den första fetma-genen upptäckt i GWAS. A-allelen associerad med ökad hunger och reducerad mättnad.",
        clinical_significance="Per A-allel: ~1.5 kg ökad vikt, ~1.2x ökad fetmarisk. AA-bärare har ~3 kg högre genomsnittsvikt.",
        recommendation="A-bärare kan motverka effekten med fysisk aktivitet och proteinfokuserad kost för bättre mättnad.",
        references=[
            Reference("17434869", "10.1126/science.1141634", "FTO gene variant and obesity", "Science", 2007, "FTO rs9939609 starkaste GWAS-signal för BMI. Effekt kan motverkas av fysisk aktivitet.")
        ],
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Lägre genetisk viktuppgångsrisk."),
            "AT": (RiskLevel.MODERATE, "~1.5 kg högre genomsnittsvikt. Ökad hunger. Fysisk aktivitet motverkar."),
            "AA": (RiskLevel.ELEVATED, "~3 kg högre genomsnittsvikt. Prioritera protein och aktivitet."),
        }
    ),
    GeneVariant(
        rsid="rs17782313",
        gene="MC4R",
        name="MC4R",
        chromosome="18",
        category=Category.SATIETY,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="C",
        protective_allele="T",
        frequency_eur=0.24,
        description="MC4R är central för mättnadssignalering i hypothalamus. C-allelen associerad med ökad hunger.",
        clinical_significance="C-bärare har ökad aptit och svårare att känna mättnad.",
        recommendation="C-bärare bör fokusera på volymrik, proteinrik kost för bättre mättnad.",
        references=[
            Reference("18454148", "10.1038/ng.140", "MC4R and obesity", "Nat Genet", 2008, "MC4R rs17782313 associerad med ökat matintag och BMI")
        ],
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Normal mättnadssignalering."),
            "CT": (RiskLevel.NORMAL, "Något ökad aptit."),
            "CC": (RiskLevel.MODERATE, "Ökade hungersignaler. Fokusera på mättande kost."),
        }
    ),

    # =========================================================================
    # HJÄRTHÄLSA - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs429358",
        gene="APOE",
        name="APOE ε4 (Arg112Cys)",
        chromosome="19",
        category=Category.CARDIOVASCULAR,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="C",  # Cys112 = ε4
        protective_allele="T",  # Arg112 = ε2/ε3
        frequency_eur=0.14,
        description="APOE ε4 är den starkaste genetiska riskfaktorn för sen Alzheimers och påverkar lipidmetabolism.",
        clinical_significance="ε4-bärare har högre LDL, sämre respons på mättat fett, och ökad Alzheimer-risk (3x för en allel, 12x för två).",
        recommendation="ε4-bärare bör begränsa mättat fett, prioritera omega-3, monitorera lipider, överväga tidiga hjärnhälsoåtgärder.",
        references=[
            Reference("8346443", "10.1126/science.8346443", "APOE E4 and Alzheimer's disease", "Science", 1993, "APOE ε4 starkaste genetiska riskfaktor för Alzheimers")
        ],
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Ej ε4-bärare (ε2/ε3 eller ε3/ε3)."),
            "CT": (RiskLevel.MODERATE, "En ε4-allel. Ökad uppmärksamhet på lipider och hjärnhälsa."),
            "CC": (RiskLevel.ELEVATED, "Två ε4-alleler (ε4/ε4). Prioritera kardio- och hjärnhälsa."),
        }
    ),
    GeneVariant(
        rsid="rs7412",
        gene="APOE",
        name="APOE ε2 (Arg158Cys)",
        chromosome="19",
        category=Category.CARDIOVASCULAR,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="T",  # Cys158 = ε2
        protective_allele="C",  # Arg158 = ε3/ε4
        frequency_eur=0.08,
        description="APOE ε2 är skyddande för hjärt-kärlsjukdom och Alzheimers.",
        clinical_significance="ε2-bärare har generellt lägre LDL och lägre Alzheimer-risk.",
        recommendation="ε2 är skyddande. Kombinera med rs429358 för komplett APOE-haplotyp.",
        references=[
            Reference("28394848", "10.1001/jamaneurol.2017.0249", "APOE and cognitive decline", "JAMA Neurol", 2017,
                     "APOE ε2 skyddande mot kognitiv nedgång"),
        ],
        genotype_effects={
            "CC": (RiskLevel.NORMAL, "Arg/Arg - ε3 eller ε4 haplotyp."),
            "CT": (RiskLevel.OPTIMAL, "Cys-bärare - Sannolikt ε2. Skyddande effekt."),
            "TT": (RiskLevel.OPTIMAL, "Cys/Cys - ε2/ε2. Skyddande."),
        }
    ),
    GeneVariant(
        rsid="rs1333049",
        gene="CDKN2A/B",
        name="9p21.3 (CHD risk locus)",
        chromosome="9",
        category=Category.CARDIOVASCULAR,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="C",
        protective_allele="G",
        frequency_eur=0.50,
        description="9p21.3 är den starkaste GWAS-signalen för kranskärlssjukdom, oberoende av traditionella riskfaktorer.",
        clinical_significance="CC-genotyp ger ~1.6x ökad risk för hjärtinfarkt.",
        recommendation="CC-bärare bör vara extra noggranna med livsstilsfaktorer även vid normal lipidprofil.",
        references=[
            Reference("17478679",
            "10.1126/science.1142447",
            "9p21 and coronary heart disease",
            "Science",
            year=2007,
            finding="9p21.3 rs1333049 starkaste GWAS-signal för CHD")
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Lägre genetisk CHD-risk."),
            "GC": (RiskLevel.NORMAL, "Intermediär risk."),
            "CC": (RiskLevel.ELEVATED, "Högre CHD-risk. Fokusera på hjärthälsolivsstil."),
        }
    ),

    # =========================================================================
    # INFLAMMATION - Medel evidens
    # =========================================================================
    GeneVariant(
        rsid="rs1800795",
        gene="IL6",
        name="IL-6 -174G/C",
        chromosome="7",
        category=Category.INFLAMMATION,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="C",
        protective_allele="G",
        frequency_eur=0.40,
        description="IL-6 är ett pro-inflammatoriskt cytokin. C-allelen associerad med högre basal IL-6-produktion.",
        clinical_significance="CC-bärare kan ha kroniskt förhöjd låggradig inflammation.",
        recommendation="CC-bärare kan ha extra nytta av antiinflammatorisk livsstil (omega-3, grönsaker, motion).",
        references=[
            Reference("10669267",
            "10.1172/JCI7920",
            "IL-6 promoter polymorphism",
            "J Clin Invest",
            year=2000,
            finding="IL-6 -174C associerad med högre IL-6 och CRP-nivåer")
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Lägre basal IL-6-produktion."),
            "GC": (RiskLevel.NORMAL, "Intermediär."),
            "CC": (RiskLevel.MODERATE, "Högre basal inflammation. Antiinflammatorisk kost rekommenderas."),
        }
    ),
    GeneVariant(
        rsid="rs1800629",
        gene="TNF",
        name="TNF-α -308G/A",
        chromosome="6",
        category=Category.INFLAMMATION,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="A",
        protective_allele="G",
        frequency_eur=0.15,
        description="TNF-α är ett centralt pro-inflammatoriskt cytokin. A-allelen ger ökad transkription.",
        clinical_significance="A-bärare har högre TNF-α-nivåer och kan vara mer benägna för inflammatoriska tillstånd.",
        recommendation="A-bärare kan ha nytta av omega-3 och kurkumin som naturliga TNF-hämmare.",
        references=[
            Reference("8782817",
            "10.1002/humu.1380080102",
            "TNF promoter polymorphism",
            "Hum Mutat",
            year=1996,
            finding="TNF -308A ger 2x ökad transkription")
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Normal TNF-α-produktion."),
            "GA": (RiskLevel.NORMAL, "Något ökad produktion."),
            "AA": (RiskLevel.MODERATE, "Hög produktion. Antiinflammatorisk strategi viktig."),
        }
    ),

    # =========================================================================
    # TRÄNING & MUSKLER - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs1815739",
        gene="ACTN3",
        name="ACTN3 R577X",
        chromosome="11",
        category=Category.EXERCISE_POWER,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="T",  # X (nonsense)
        protective_allele="C",  # R (fungerande)
        frequency_eur=0.42,
        description="ACTN3 kodar för α-actinin-3 som finns i snabba muskelfibrer. TT (X/X) = inget fungerande protein.",
        clinical_significance="CC (R/R) = fördelaktigt för sprint/power. TT (X/X) = fördelaktigt för uthållighet. ~18% av europeer är XX.",
        recommendation="CC: Fokusera på explosiv styrka, HIIT. TT: Fokusera på uthållighet, längre pass. CT: Allround.",
        references=[
            Reference("12879365", "10.1038/ng1245", "ACTN3 and athletic performance", "Nat Genet", 2003, "ACTN3 R577X tydligt associerad med elitidrottsprestanda. R/R överrepresenterat hos sprintare.")
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "R/R - Fungerande ACTN3. Genetisk fördel för explosiv styrka/sprint."),
            "CT": (RiskLevel.OPTIMAL, "R/X - Allroundkapacitet. Bra för varierad träning."),
            "TT": (RiskLevel.OPTIMAL, "X/X - Ingen ACTN3. Genetisk fördel för uthållighet/långdistans."),
        }
    ),
    GeneVariant(
        rsid="rs8192678",
        gene="PPARGC1A",
        name="PGC-1α Gly482Ser",
        chromosome="4",
        category=Category.EXERCISE_ENDURANCE,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="A",  # Ser
        protective_allele="G",  # Gly
        frequency_eur=0.36,
        description="PGC-1α är 'master regulator' för mitokondriell biogenes och oxidativ metabolism.",
        clinical_significance="GG (Gly/Gly) associerat med bättre uthållighetskapacitet och VO2max-respons på träning.",
        recommendation="AA-bärare kan behöva mer konsekvent uthållighetsträning för samma förbättring.",
        references=[
            Reference("13679500",
            "10.1007/s00439-003-1014-4",
            "PPARGC1A and endurance",
            "Hum Genet",
            year=2003,
            finding="Gly482 associerat med högre VO2max och uthållighetsprestation")
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Gly/Gly - Bättre mitokondriell respons på träning."),
            "AG": (RiskLevel.NORMAL, "Gly/Ser - Intermediär."),
            "AA": (RiskLevel.NORMAL, "Ser/Ser - Kan behöva mer träning för samma effekt."),
        }
    ),

    # =========================================================================
    # DETOX - Medel evidens
    # =========================================================================
    GeneVariant(
        rsid="rs1695",
        gene="GSTP1",
        name="GSTP1 Ile105Val",
        chromosome="11",
        category=Category.DETOX,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="G",  # Val
        protective_allele="A",  # Ile
        frequency_eur=0.33,
        description="GSTP1 är ett glutationtransferas viktigt för avgiftning av reaktiva syreföreningar och xenobiotika.",
        clinical_significance="Val-allelen ger reducerad enzymaktivitet, särskilt mot PAH (polycykliska aromatiska kolväten).",
        recommendation="G-bärare kan ha nytta av extra korsblommiga grönsaker (sulforafan) och NAC för glutationstöd.",
        references=[
            Reference("10482588",
            "10.1093/carcin/20.9.1671",
            "GSTP1 polymorphism and cancer risk",
            "Carcinogenesis",
            year=1999,
            finding="GSTP1 Val105 associerad med reducerad avgiftningskapacitet")
        ],
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Ile/Ile - Effektiv avgiftning."),
            "AG": (RiskLevel.NORMAL, "Ile/Val - Intermediär."),
            "GG": (RiskLevel.MODERATE, "Val/Val - Reducerad kapacitet. Stöd med sulforafan och NAC."),
        }
    ),
    GeneVariant(
        rsid="rs1050450",
        gene="GPX1",
        name="GPX1 Pro198Leu",
        chromosome="3",
        category=Category.ANTIOXIDANT,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="T",  # Leu
        protective_allele="C",  # Pro
        frequency_eur=0.26,
        description="GPX1 (glutationperoxidas 1) är det viktigaste selenberoende antioxidantenzymet.",
        clinical_significance="Leu-varianten har lägre enzymaktivitet och är mer känslig för selenbrist.",
        recommendation="T-bärare bör säkerställa adekvat selenintag (150-200 mcg/dag) från kost eller tillskott.",
        references=[
            Reference("9354650", "10.1016/S0378-1119(97)00344-0", "GPX1 polymorphism and activity", "Gene", 1997, "GPX1 Leu198 associerad med lägre enzymaktivitet")
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Pro/Pro - Effektiv antioxidantfunktion."),
            "CT": (RiskLevel.NORMAL, "Pro/Leu - Intermediär."),
            "TT": (RiskLevel.MODERATE, "Leu/Leu - Reducerad funktion. Säkerställ selenintag."),
        }
    ),
    GeneVariant(
        rsid="rs4880",
        gene="SOD2",
        name="SOD2 Ala16Val",
        chromosome="6",
        category=Category.ANTIOXIDANT,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="T",  # Val - ineffektiv transport
        protective_allele="C",  # Ala - effektiv transport
        frequency_eur=0.47,
        description="SOD2 är det mitokondriella superoxiddismutaset. Ala-varianten transporteras effektivare in i mitokondrier.",
        clinical_significance="Val-varianten (T) ger lägre mitokondriell SOD2-aktivitet och mer oxidativ stress.",
        recommendation="TT-bärare kan ha nytta av CoQ10 och MitoQ för mitokondriellt antioxidantskydd.",
        references=[
            Reference("10228155",
            "10.1006/bbrc.1999.0449",
            "SOD2 Ala16Val functional effects",
            "Biochem Biophys Res Commun",
            year=1999,
            finding="Val16 ger 30-40% lägre mitokondriell SOD2-aktivitet")
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Ala/Ala - Effektiv mitokondriell SOD2."),
            "CT": (RiskLevel.OPTIMAL, "Ala/Val - Intermediär, ofta optimal balans."),
            "TT": (RiskLevel.NORMAL, "Val/Val - Lägre mitokondriell SOD2. Överväg CoQ10."),
        }
    ),

    # =========================================================================
    # JÄRNMETABOLISM - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs1800562",
        gene="HFE",
        name="HFE C282Y",
        chromosome="6",
        category=Category.IRON,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="A",  # Tyr282
        protective_allele="G",  # Cys282
        frequency_eur=0.06,
        description="HFE C282Y är huvudmutationen för hereditär hemokromatos. Homozygota absorberar för mycket järn.",
        clinical_significance="AA (homozygot) = 80-90% risk för järnöverskott. AG (heterozygot) = mild ökad absorption.",
        recommendation="AA: Regelbunden ferritinkontroll, undvik järntillskott, blodgivning kan vara terapeutiskt. AG: Var uppmärksam.",
        references=[
            Reference("9697704", "10.1056/NEJM199810013391405", "HFE mutations and hemochromatosis", "N Engl J Med", 1998, "HFE C282Y homozygoti ansvarig för >80% av hemokromatos i Nordeuropa")
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "C/C - Normal järnmetabolism."),
            "AG": (RiskLevel.NORMAL, "C/Y - Heterozygot bärare. Mild ökad absorption. Monitorera ferritin."),
            "AA": (RiskLevel.HIGH, "Y/Y - Hemokromatos. Undvik järntillskott. Regelbunden ferritinkontroll."),
        }
    ),
    GeneVariant(
        rsid="rs1799945",
        gene="HFE",
        name="HFE H63D",
        chromosome="6",
        category=Category.IRON,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="G",  # Asp63
        protective_allele="C",  # His63
        frequency_eur=0.15,
        description="HFE H63D är en mildare järnabsorptionsvariant. Klinisk relevans främst i kombination med C282Y.",
        clinical_significance="GG ensamt ger sällan klinisk hemokromatos. C282Y/H63D compound heterozygot kan ge mild järnöverskott.",
        recommendation="Viktig främst i kombination med C282Y-status.",
        references=[
            Reference("9697704", "10.1056/NEJM199810013391405", "HFE mutations and hemochromatosis", "N Engl J Med", 1998, "H63D har mildare penetrans än C282Y")
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "H/H - Normal."),
            "CG": (RiskLevel.NORMAL, "H/D - Lätt ökad absorption."),
            "GG": (RiskLevel.NORMAL, "D/D - Lätt ökad. Monitorera vid andra riskfaktorer."),
        }
    ),

    # =========================================================================
    # INSULINKÄNSLIGHET - Stark evidens
    # =========================================================================
    GeneVariant(
        rsid="rs7903146",
        gene="TCF7L2",
        name="TCF7L2",
        chromosome="10",
        category=Category.INSULIN,
        evidence_level=EvidenceLevel.STRONG,
        risk_allele="T",
        protective_allele="C",
        frequency_eur=0.30,
        description="TCF7L2 är den starkaste genetiska riskfaktorn för typ 2-diabetes, påverkar insulinsekretion.",
        clinical_significance="TT-genotyp ger ~1.8x ökad risk för T2D genom reducerad insulinsekretion.",
        recommendation="T-bärare bör vara extra noga med blodsockerkontroll, fysisk aktivitet och vikthantering.",
        references=[
            Reference("16415884", "10.1038/ng1732", "TCF7L2 and type 2 diabetes", "Nat Genet", 2006, "TCF7L2 rs7903146 starkaste GWAS-signal för T2D")
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Lägre genetisk T2D-risk."),
            "CT": (RiskLevel.MODERATE, "~1.4x ökad T2D-risk. Livsstilsfaktorer viktiga."),
            "TT": (RiskLevel.ELEVATED, "~1.8x ökad risk. Prioritera blodsockerkontroll."),
        }
    ),

    # =========================================================================
    # LONGEVITY - Preliminär evidens
    # =========================================================================
    GeneVariant(
        rsid="rs2802292",
        gene="FOXO3",
        name="FOXO3",
        chromosome="6",
        category=Category.LONGEVITY,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="T",
        protective_allele="G",
        frequency_eur=0.40,
        description="FOXO3 är involverad i cellulär stressrespons, metabolism och åldrande. G-allelen associerad med longevity.",
        clinical_significance="GG-genotyp överrepresenterad bland hundraåringar i flera populationer.",
        recommendation="G-bärare har möjlig longevity-fördel. Alla bör fokusera på bevisade åldrandemodulatorer.",
        references=[
            Reference("18786090", "10.1073/pnas.0801030105", "FOXO3 and longevity", "PNAS", 2008, "FOXO3 rs2802292 G-allel associerad med exceptional longevity")
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Fördelaktig longevity-variant."),
            "GT": (RiskLevel.OPTIMAL, "Intermediär."),
            "TT": (RiskLevel.NORMAL, "Standard. Fokusera på bevisade livsstilsfaktorer."),
        }
    ),

    # =========================================================================
    # SKÖLDKÖRTEL - Preliminär evidens
    # =========================================================================
    GeneVariant(
        rsid="rs965513",
        gene="FOXE1",
        name="FOXE1 (9q22)",
        chromosome="9",
        category=Category.THYROID,
        evidence_level=EvidenceLevel.MODERATE,
        risk_allele="A",
        protective_allele="G",
        frequency_eur=0.35,
        description="FOXE1 är en transkriptionsfaktor viktig för sköldkörtelutveckling. A-allelen associerad med hypotyreos.",
        clinical_significance="AA-genotyp associerad med ökad risk för hypotyreos och sköldkörtelcancer.",
        recommendation="A-bärare bör vara uppmärksamma på hypotyreos-symptom och kontrollera TSH vid behov.",
        references=[
            Reference("19198610",
            "10.1038/ng.313",
            "FOXE1 and thyroid cancer",
            "Nat Genet",
            year=2009,
            finding="FOXE1 rs965513 starkaste GWAS-signal för sköldkörtelfunktion")
        ],
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Lägre genetisk sköldkörtelrisk."),
            "AG": (RiskLevel.NORMAL, "Intermediär."),
            "AA": (RiskLevel.MODERATE, "Ökad risk för sköldkörtelproblem. Monitorera vid symptom."),
        }
    ),

    # =========================================================================
    # HISTAMININTOLERANS - Preliminär evidens
    # =========================================================================
    GeneVariant(
        rsid="rs1049793",
        gene="ABP1/AOC1",
        name="DAO (Diaminoxidas)",
        chromosome="7",
        category=Category.HISTAMINE,
        evidence_level=EvidenceLevel.PRELIMINARY,
        risk_allele="G",
        protective_allele="C",
        frequency_eur=0.20,
        description="DAO bryter ned histamin i tarmen. G-allelen kan ge reducerad aktivitet och histaminintolerans.",
        clinical_significance="Möjlig association med histaminintolerans (huvudvärk, flush, GI-symptom efter histaminrik mat).",
        recommendation="G-bärare med symptom efter vin/ost/fermenterad mat kan överväga DAO-enzymtillskott.",
        references=[
            Reference("17490952",
            "10.1007/s00508-007-0881-5",
            "DAO polymorphisms and histamine intolerance",
            "Wien Klin Wochenschr",
            year=2007,
            finding="ABP1 varianter associerade med histaminintolerans-symptom")
        ],
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Normal DAO-aktivitet."),
            "CG": (RiskLevel.NORMAL, "Intermediär."),
            "GG": (RiskLevel.MODERATE, "Möjlig reducerad DAO. Överväg DAO-tillskott vid symptom."),
        }
    ),
]

# Funktion för att konvertera till dict för enkel användning
def get_gene_dict() -> Dict[str, GeneVariant]:
    """Returnerar gendatabasen som dict med rsid som nyckel"""
    return {gene.rsid: gene for gene in GENE_DATABASE}

def get_genes_by_category(category: Category) -> List[GeneVariant]:
    """Returnerar alla gener i en specifik kategori"""
    return [g for g in GENE_DATABASE if g.category == category]

def get_genes_by_evidence(min_level: EvidenceLevel) -> List[GeneVariant]:
    """Returnerar gener med minst angiven evidensnivå"""
    level_order = [EvidenceLevel.PRELIMINARY, EvidenceLevel.MODERATE, EvidenceLevel.STRONG]
    min_idx = level_order.index(min_level)
    return [g for g in GENE_DATABASE if level_order.index(g.evidence_level) >= min_idx]

if __name__ == "__main__":
    print(f"GWL Gene Database v1.0")
    print(f"Total gener: {len(GENE_DATABASE)}")
    print(f"\nPer evidensnivå:")
    for level in EvidenceLevel:
        count = len([g for g in GENE_DATABASE if g.evidence_level == level])
        print(f"  {level.value}: {count}")
    print(f"\nPer kategori:")
    for cat in Category:
        genes = get_genes_by_category(cat)
        if genes:
            print(f"  {cat.value}: {len(genes)}")
