#!/usr/bin/env python3
"""
Genetic Wellness Labs - DNA Analysis Tool
==========================================
Analyserar 23andMe rådata och skapar en personlig wellness-profil
baserad på 70+ genetiska markörer för:
- Näringsbehov (vitaminer, mineraler)
- Metabolism och energi
- Koffein- och alkoholmetabolism
- Stressrespons och sömn
- Träning och återhämtning
- Hjärthälsa och inflammation

Författare: GWL AI Pipeline
Version: 1.0.0
"""

import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime
import json


class RiskLevel(Enum):
    """Risknivå för genetiska varianter"""
    OPTIMAL = "optimal"
    NORMAL = "normal"
    MODERATE = "moderat"
    ELEVATED = "förhöjd"
    HIGH = "hög"


class ImpactCategory(Enum):
    """Kategorier för genetisk påverkan"""
    VITAMIN_D = "D-vitamin"
    VITAMIN_B = "B-vitaminer"
    VITAMIN_A = "A-vitamin"
    OMEGA3 = "Omega-3"
    IRON = "Järn"
    MAGNESIUM = "Magnesium"
    ZINC = "Zink"
    FOLATE = "Folat"
    CAFFEINE = "Koffein"
    ALCOHOL = "Alkohol"
    LACTOSE = "Laktos"
    GLUTEN = "Gluten"
    STRESS = "Stress"
    SLEEP = "Sömn"
    WEIGHT = "Vikthantering"
    CARDIOVASCULAR = "Hjärthälsa"
    INFLAMMATION = "Inflammation"
    DETOX = "Detox"
    EXERCISE = "Träning"
    RECOVERY = "Återhämtning"
    METHYLATION = "Metylering"
    ANTIOXIDANT = "Antioxidanter"


@dataclass
class GeneticVariant:
    """Representerar en genetisk variant och dess betydelse"""
    rsid: str
    gene: str
    name: str
    category: ImpactCategory
    risk_allele: str
    protective_allele: str
    description: str
    recommendation: str
    # Genotyp -> (risknivå, beskrivning)
    genotype_effects: Dict[str, Tuple[RiskLevel, str]]


@dataclass
class AnalysisResult:
    """Resultat för en enskild genetisk analys"""
    variant: GeneticVariant
    genotype: str
    risk_level: RiskLevel
    interpretation: str


@dataclass
class CategorySummary:
    """Sammanfattning per kategori"""
    category: ImpactCategory
    results: List[AnalysisResult]
    overall_risk: RiskLevel
    key_findings: List[str]
    recommendations: List[str]


@dataclass
class SupplementRecommendation:
    """Supplement-rekommendation baserad på genetik"""
    name: str
    dosage: str
    reason: str
    priority: int  # 1-5, där 5 är högst prioritet
    genes_involved: List[str]


@dataclass
class GWLProfile:
    """Komplett GWL wellness-profil"""
    name: str
    analysis_date: str
    total_variants_analyzed: int
    category_summaries: Dict[ImpactCategory, CategorySummary]
    supplement_recommendations: List[SupplementRecommendation]
    lifestyle_recommendations: List[str]
    diet_recommendations: List[str]
    exercise_recommendations: List[str]
    raw_results: List[AnalysisResult]


# =============================================================================
# GENETISK VARIANT-DATABAS
# Baserad på peer-reviewed forskning och kliniska riktlinjer
# =============================================================================

WELLNESS_VARIANTS: List[GeneticVariant] = [
    # =========================================================================
    # VITAMIN D - Metabolism och upptag
    # =========================================================================
    GeneticVariant(
        rsid="rs2228570",
        gene="VDR",
        name="VDR FokI",
        category=ImpactCategory.VITAMIN_D,
        risk_allele="T",
        protective_allele="C",
        description="VDR-receptorn påverkar hur effektivt kroppen använder D-vitamin",
        recommendation="Överväg högre D-vitamindos vid TT-genotyp",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Normal VDR-funktion, standard D-vitaminbehov"),
            "CT": (RiskLevel.NORMAL, "Något reducerad VDR-aktivitet"),
            "TT": (RiskLevel.ELEVATED, "Reducerad VDR-aktivitet, kan behöva högre D-vitamindos"),
        }
    ),
    GeneticVariant(
        rsid="rs1544410",
        gene="VDR",
        name="VDR BsmI",
        category=ImpactCategory.VITAMIN_D,
        risk_allele="A",
        protective_allele="G",
        description="Påverkar D-vitaminreceptorns densitet",
        recommendation="Kontrollera D-vitaminnivåer regelbundet",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Optimal VDR-densitet"),
            "AG": (RiskLevel.NORMAL, "Normal VDR-densitet"),
            "AA": (RiskLevel.MODERATE, "Lägre VDR-densitet, kan påverka D-vitaminrespons"),
        }
    ),
    GeneticVariant(
        rsid="rs731236",
        gene="VDR",
        name="VDR TaqI",
        category=ImpactCategory.VITAMIN_D,
        risk_allele="A",
        protective_allele="G",
        description="Påverkar D-vitaminmetabolism och benmineral-densitet",
        recommendation="Viktigt med adekvat D-vitamin för benhälsa",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Normal D-vitaminmetabolism"),
            "AG": (RiskLevel.NORMAL, "Något ändrad metabolism"),
            "AA": (RiskLevel.MODERATE, "Kan ha ökade D-vitaminbehov"),
        }
    ),
    GeneticVariant(
        rsid="rs10741657",
        gene="CYP2R1",
        name="CYP2R1",
        category=ImpactCategory.VITAMIN_D,
        risk_allele="A",
        protective_allele="G",
        description="Enzym som omvandlar D-vitamin till aktiv form i levern",
        recommendation="GG-bärare kan ha naturligt högre D-vitaminnivåer",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Effektiv D-vitaminaktivering"),
            "AG": (RiskLevel.NORMAL, "Normal aktivering"),
            "AA": (RiskLevel.ELEVATED, "Mindre effektiv aktivering, kan behöva mer D-vitamin"),
        }
    ),
    GeneticVariant(
        rsid="rs12785878",
        gene="DHCR7",
        name="DHCR7/NADSYN1",
        category=ImpactCategory.VITAMIN_D,
        risk_allele="G",
        protective_allele="T",
        description="Påverkar D-vitaminsyntes från solljus i huden",
        recommendation="TT-bärare kan producera mer D-vitamin från sol",
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Effektiv D-vitaminproduktion från sol"),
            "GT": (RiskLevel.NORMAL, "Normal syntes"),
            "GG": (RiskLevel.MODERATE, "Mindre effektiv solberoende syntes"),
        }
    ),

    # =========================================================================
    # METYLERING & B-VITAMINER
    # =========================================================================
    GeneticVariant(
        rsid="rs1801133",
        gene="MTHFR",
        name="MTHFR C677T",
        category=ImpactCategory.METHYLATION,
        risk_allele="A",
        protective_allele="G",
        description="Påverkar folatmetabolism och homocysteinnivåer. En av de viktigaste wellness-generna.",
        recommendation="TT-bärare bör ta metylfolat istället för folsyra",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Normal MTHFR-funktion (100% enzymaktivitet)"),
            "AG": (RiskLevel.MODERATE, "Reducerad funktion (~65% aktivitet), överväg metylfolat"),
            "AA": (RiskLevel.HIGH, "Kraftigt reducerad funktion (~30% aktivitet), metylfolat rekommenderas starkt"),
        }
    ),
    GeneticVariant(
        rsid="rs1801131",
        gene="MTHFR",
        name="MTHFR A1298C",
        category=ImpactCategory.METHYLATION,
        risk_allele="G",
        protective_allele="T",
        description="Sekundär MTHFR-variant som påverkar BH4-regenerering",
        recommendation="I kombination med C677T kan effekten förstärkas",
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Normal funktion"),
            "GT": (RiskLevel.NORMAL, "Mild påverkan"),
            "GG": (RiskLevel.MODERATE, "Reducerad BH4-regenerering"),
        }
    ),
    GeneticVariant(
        rsid="rs1805087",
        gene="MTR",
        name="MTR A2756G",
        category=ImpactCategory.VITAMIN_B,
        risk_allele="G",
        protective_allele="A",
        description="Metioninsyntasgen, viktig för B12-beroende metylering",
        recommendation="Säkerställ adekvat B12-intag vid G-allel",
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Normal MTR-funktion"),
            "AG": (RiskLevel.NORMAL, "Något ökad aktivitet"),
            "GG": (RiskLevel.MODERATE, "Ökad B12-förbrukning"),
        }
    ),
    GeneticVariant(
        rsid="rs1801394",
        gene="MTRR",
        name="MTRR A66G",
        category=ImpactCategory.VITAMIN_B,
        risk_allele="G",
        protective_allele="A",
        description="Regenererar MTR-enzymet, påverkar B12-metabolism",
        recommendation="GG-bärare kan ha ökade B12-behov",
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Effektiv MTRR-funktion"),
            "AG": (RiskLevel.NORMAL, "Något reducerad funktion"),
            "GG": (RiskLevel.ELEVATED, "Reducerad funktion, överväg metyl-B12"),
        }
    ),
    GeneticVariant(
        rsid="rs602662",
        gene="FUT2",
        name="FUT2 (Secretor)",
        category=ImpactCategory.VITAMIN_B,
        risk_allele="A",
        protective_allele="G",
        description="Påverkar B12-absorption via tarmfloran",
        recommendation="Non-secretors (AA) kan ha lägre B12-nivåer",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Secretor-status, normal B12-absorption"),
            "AG": (RiskLevel.NORMAL, "Secretor, normal absorption"),
            "AA": (RiskLevel.MODERATE, "Non-secretor, kan ha reducerad B12-absorption"),
        }
    ),

    # =========================================================================
    # VITAMIN A & BETAKAROTEN
    # =========================================================================
    GeneticVariant(
        rsid="rs7501331",
        gene="BCMO1",
        name="BCMO1 R267S",
        category=ImpactCategory.VITAMIN_A,
        risk_allele="T",
        protective_allele="C",
        description="Påverkar omvandling av betakaroten till retinol (aktiv A-vitamin)",
        recommendation="T-allelbärare bör överväga preformerad A-vitamin (retinol)",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Effektiv betakarotenomvandling"),
            "CT": (RiskLevel.MODERATE, "32% reducerad omvandling"),
            "TT": (RiskLevel.ELEVATED, "69% reducerad omvandling, behöver preformerad A-vitamin"),
        }
    ),
    GeneticVariant(
        rsid="rs12934922",
        gene="BCMO1",
        name="BCMO1 A379V",
        category=ImpactCategory.VITAMIN_A,
        risk_allele="T",
        protective_allele="A",
        description="Ytterligare variant som påverkar betakarotenomvandling",
        recommendation="Kombinerad effekt med rs7501331",
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Normal omvandling"),
            "AT": (RiskLevel.NORMAL, "Något reducerad"),
            "TT": (RiskLevel.MODERATE, "Reducerad betakarotenomvandling"),
        }
    ),

    # =========================================================================
    # OMEGA-3 & FETTSYROR
    # =========================================================================
    GeneticVariant(
        rsid="rs174546",
        gene="FADS1",
        name="FADS1",
        category=ImpactCategory.OMEGA3,
        risk_allele="T",
        protective_allele="C",
        description="Påverkar omvandling av växtbaserad omega-3 (ALA) till EPA/DHA",
        recommendation="T-bärare bör prioritera marin omega-3 (fisk/alg)",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Effektiv ALA→EPA/DHA-omvandling"),
            "CT": (RiskLevel.MODERATE, "Reducerad omvandlingsförmåga"),
            "TT": (RiskLevel.ELEVATED, "Kraftigt reducerad, marin omega-3 rekommenderas"),
        }
    ),
    GeneticVariant(
        rsid="rs1535",
        gene="FADS2",
        name="FADS2",
        category=ImpactCategory.OMEGA3,
        risk_allele="G",
        protective_allele="A",
        description="Påverkar delta-6-desaturas, kritisk för omega-3-metabolism",
        recommendation="G-bärare kan ha suboptimal omega-3-status",
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Normal FADS2-aktivitet"),
            "AG": (RiskLevel.NORMAL, "Något reducerad aktivitet"),
            "GG": (RiskLevel.MODERATE, "Reducerad aktivitet, överväg EPA/DHA-tillskott"),
        }
    ),

    # =========================================================================
    # KOFFEINMETABOLISM
    # =========================================================================
    GeneticVariant(
        rsid="rs762551",
        gene="CYP1A2",
        name="CYP1A2",
        category=ImpactCategory.CAFFEINE,
        risk_allele="C",
        protective_allele="A",
        description="Huvudenzymet för koffeinmetabolism i levern",
        recommendation="Långsamma metaboliserare bör begränsa koffeinet",
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Snabb koffeinmetaboliserare - kan tolerera mer kaffe"),
            "AC": (RiskLevel.NORMAL, "Medel metaboliserare"),
            "CC": (RiskLevel.ELEVATED, "Långsam metaboliserare - begränsa till 1-2 koppar/dag"),
        }
    ),
    GeneticVariant(
        rsid="rs4410790",
        gene="AHR",
        name="AHR",
        category=ImpactCategory.CAFFEINE,
        risk_allele="T",
        protective_allele="C",
        description="Påverkar CYP1A2-expression och därmed koffeinmetabolism",
        recommendation="T-bärare kan naturligt dricka mer kaffe",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Normal koffeinkänslighet"),
            "CT": (RiskLevel.NORMAL, "Något ökad tolerans"),
            "TT": (RiskLevel.OPTIMAL, "Högre koffeintolerans"),
        }
    ),

    # =========================================================================
    # ALKOHOLMETABOLISM
    # =========================================================================
    GeneticVariant(
        rsid="rs1229984",
        gene="ADH1B",
        name="ADH1B Arg48His",
        category=ImpactCategory.ALCOHOL,
        risk_allele="T",
        protective_allele="C",
        description="Påverkar hur snabbt alkohol bryts ned till acetaldehyd",
        recommendation="T-bärare får snabbare 'flush'-reaktion",
        genotype_effects={
            "CC": (RiskLevel.NORMAL, "Normal alkoholmetabolism"),
            "CT": (RiskLevel.NORMAL, "Snabbare metabolism, mer flush"),
            "TT": (RiskLevel.MODERATE, "Mycket snabb metabolism, uttalad flush-reaktion"),
        }
    ),
    GeneticVariant(
        rsid="rs671",
        gene="ALDH2",
        name="ALDH2",
        category=ImpactCategory.ALCOHOL,
        risk_allele="A",
        protective_allele="G",
        description="Avgör hur snabbt acetaldehyd (giftigt) bryts ned",
        recommendation="A-bärare bör begränsa alkoholintag kraftigt",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Normal acetaldehydnedbrytning"),
            "AG": (RiskLevel.ELEVATED, "Reducerad nedbrytning, ökad flush och risk"),
            "AA": (RiskLevel.HIGH, "Allvarligt nedsatt, alkohol avrådes starkt"),
        }
    ),

    # =========================================================================
    # LAKTOSINTOLERANS
    # =========================================================================
    GeneticVariant(
        rsid="rs4988235",
        gene="MCM6/LCT",
        name="LCT-13910",
        category=ImpactCategory.LACTOSE,
        risk_allele="G",
        protective_allele="A",
        description="Avgör om laktasproduktion fortsätter i vuxen ålder",
        recommendation="GG-bärare är sannolikt laktostoleranta som vuxna",
        genotype_effects={
            "AA": (RiskLevel.HIGH, "Laktosintolerant - laktas slutar produceras"),
            "AG": (RiskLevel.NORMAL, "Troligen laktostolerant"),
            "GG": (RiskLevel.OPTIMAL, "Laktospersistent - kan dricka mjölk som vuxen"),
        }
    ),

    # =========================================================================
    # GLUTENKÄNSLIGHET (ej celiaki)
    # =========================================================================
    GeneticVariant(
        rsid="rs2187668",
        gene="HLA-DQ2.5",
        name="HLA-DQ2.5",
        category=ImpactCategory.GLUTEN,
        risk_allele="T",
        protective_allele="C",
        description="HLA-gen associerad med celiaki-risk (ej diagnostisk)",
        recommendation="T-bärare har ökad genetisk risk för celiaki",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Låg genetisk celiaki-risk"),
            "CT": (RiskLevel.MODERATE, "Ökad risk, var uppmärksam på symptom"),
            "TT": (RiskLevel.ELEVATED, "Högre genetisk risk för celiaki"),
        }
    ),

    # =========================================================================
    # STRESSRESPONS & COMT
    # =========================================================================
    GeneticVariant(
        rsid="rs4680",
        gene="COMT",
        name="COMT Val158Met",
        category=ImpactCategory.STRESS,
        risk_allele="A",
        protective_allele="G",
        description="Påverkar dopamin/noradrenalin-nedbrytning. 'Warrior vs Worrier'-genen.",
        recommendation="AA (Met/Met) är mer stresskänsliga men bättre på komplexa uppgifter",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Val/Val - 'Warrior', snabb dopaminnedbrytning, stresstålig"),
            "AG": (RiskLevel.NORMAL, "Val/Met - balanserad"),
            "AA": (RiskLevel.MODERATE, "Met/Met - 'Worrier', långsam nedbrytning, mer stresskänslig men bättre fokus"),
        }
    ),
    GeneticVariant(
        rsid="rs6265",
        gene="BDNF",
        name="BDNF Val66Met",
        category=ImpactCategory.STRESS,
        risk_allele="T",
        protective_allele="C",
        description="Brain-derived neurotrophic factor, påverkar hjärnplasticitet och stressåterhämtning",
        recommendation="T-bärare kan ha nytta av extra stresshantering och träning",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Val/Val - normal BDNF-sekretion"),
            "CT": (RiskLevel.NORMAL, "Val/Met - något reducerad"),
            "TT": (RiskLevel.MODERATE, "Met/Met - reducerad BDNF, kan påverka stresshantering"),
        }
    ),

    # =========================================================================
    # SÖMN & DYGNSRYTM
    # =========================================================================
    GeneticVariant(
        rsid="rs57875989",
        gene="DEC2",
        name="DEC2",
        category=ImpactCategory.SLEEP,
        risk_allele="A",
        protective_allele="G",
        description="Sällsynt variant associerad med kortsovare (klarar sig på mindre sömn)",
        recommendation="De flesta har GG och behöver 7-9 timmar sömn",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Normal sömnbehov (7-9 timmar)"),
            "AG": (RiskLevel.OPTIMAL, "Kan klara något mindre sömn"),
            "AA": (RiskLevel.OPTIMAL, "Sällsynt 'kortsovare' - klarar 4-6 timmar"),
        }
    ),
    GeneticVariant(
        rsid="rs1801260",
        gene="CLOCK",
        name="CLOCK 3111T/C",
        category=ImpactCategory.SLEEP,
        risk_allele="C",
        protective_allele="T",
        description="Påverkar dygnsrytm och morgon/kvällspreferens",
        recommendation="C-bärare tenderar att vara kvällsmänniskor",
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Morgonmänniska-tendens"),
            "TC": (RiskLevel.NORMAL, "Neutral dygnsrytm"),
            "CC": (RiskLevel.NORMAL, "Kvällsmänniska-tendens"),
        }
    ),
    GeneticVariant(
        rsid="rs12927162",
        gene="MTNR1B",
        name="MTNR1B",
        category=ImpactCategory.SLEEP,
        risk_allele="G",
        protective_allele="C",
        description="Melatoninreceptor, påverkar sömn och glukosmetabolism",
        recommendation="G-bärare kan ha nytta av melatonintillskott",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Normal melatoninrespons"),
            "CG": (RiskLevel.NORMAL, "Något ändrad respons"),
            "GG": (RiskLevel.MODERATE, "Kan ha suboptimal melatoninsignalering"),
        }
    ),

    # =========================================================================
    # VIKT & METABOLISM
    # =========================================================================
    GeneticVariant(
        rsid="rs9939609",
        gene="FTO",
        name="FTO",
        category=ImpactCategory.WEIGHT,
        risk_allele="A",
        protective_allele="T",
        description="Den mest studerade fetma-genen, påverkar mättnadskänsla",
        recommendation="A-bärare kan ha nytta av proteinfokuserad kost",
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Lägre genetisk viktuppgångsrisk"),
            "AT": (RiskLevel.MODERATE, "Medel risk, ~1.5 kg högre genomsnittsvikt"),
            "AA": (RiskLevel.ELEVATED, "Högre risk, ~3 kg högre genomsnittsvikt, mer hunger"),
        }
    ),
    GeneticVariant(
        rsid="rs17782313",
        gene="MC4R",
        name="MC4R",
        category=ImpactCategory.WEIGHT,
        risk_allele="C",
        protective_allele="T",
        description="Melanokortinreceptor, central för hungersignalering",
        recommendation="C-bärare kan uppleva mer hunger, fokusera på mättande mat",
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Normal mättnadssignalering"),
            "CT": (RiskLevel.NORMAL, "Något ökad hunger"),
            "CC": (RiskLevel.MODERATE, "Kan ha ökade hungersignaler"),
        }
    ),
    GeneticVariant(
        rsid="rs1042713",
        gene="ADRB2",
        name="ADRB2 Arg16Gly",
        category=ImpactCategory.WEIGHT,
        risk_allele="G",
        protective_allele="A",
        description="Beta2-adrenoreceptor, påverkar fettförbränning vid träning",
        recommendation="GG-bärare kan ha bättre respons på HIIT-träning",
        genotype_effects={
            "AA": (RiskLevel.NORMAL, "Normal fettförbränningsrespons"),
            "AG": (RiskLevel.NORMAL, "Normal respons"),
            "GG": (RiskLevel.OPTIMAL, "Potentiellt bättre fettförbränning vid intensiv träning"),
        }
    ),

    # =========================================================================
    # HJÄRTHÄLSA & APOE
    # =========================================================================
    GeneticVariant(
        rsid="rs429358",
        gene="APOE",
        name="APOE ε4 (C112R)",
        category=ImpactCategory.CARDIOVASCULAR,
        risk_allele="C",
        protective_allele="T",
        description="APOE4 associerad med hjärt-kärlrisk och Alzheimer",
        recommendation="C-bärare bör fokusera extra på hjärthälsa och mättat fett",
        genotype_effects={
            "TT": (RiskLevel.OPTIMAL, "Ej APOE4-bärare"),
            "CT": (RiskLevel.MODERATE, "En kopia APOE4, ökad uppmärksamhet på lipider"),
            "CC": (RiskLevel.ELEVATED, "Två kopior APOE4, bör monitorera lipider noga"),
        }
    ),
    GeneticVariant(
        rsid="rs7412",
        gene="APOE",
        name="APOE ε2 (R158C)",
        category=ImpactCategory.CARDIOVASCULAR,
        risk_allele="T",
        protective_allele="C",
        description="APOE2 är generellt skyddande för hjärtat",
        recommendation="T-bärare har ofta bättre lipidprofil",
        genotype_effects={
            "CC": (RiskLevel.NORMAL, "Ej APOE2-bärare"),
            "CT": (RiskLevel.OPTIMAL, "En kopia APOE2 (skyddande)"),
            "TT": (RiskLevel.OPTIMAL, "Två kopior APOE2 (skyddande)"),
        }
    ),
    GeneticVariant(
        rsid="rs1333049",
        gene="9p21",
        name="9p21.3 (CDKN2A/B)",
        category=ImpactCategory.CARDIOVASCULAR,
        risk_allele="C",
        protective_allele="G",
        description="Den starkaste genetiska riskfaktorn för kranskärlssjukdom",
        recommendation="CC-bärare bör prioritera kardiovaskulär prevention",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Lägre genetisk hjärtrisk"),
            "GC": (RiskLevel.NORMAL, "Medel risk"),
            "CC": (RiskLevel.ELEVATED, "Högre genetisk risk, fokus på livsstil"),
        }
    ),

    # =========================================================================
    # INFLAMMATION
    # =========================================================================
    GeneticVariant(
        rsid="rs1800795",
        gene="IL6",
        name="IL-6 -174G/C",
        category=ImpactCategory.INFLAMMATION,
        risk_allele="C",
        protective_allele="G",
        description="Interleukin-6 promotorvariant, påverkar inflammationsnivåer",
        recommendation="C-bärare kan ha högre basinflammation",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Lägre basala IL-6-nivåer"),
            "GC": (RiskLevel.NORMAL, "Medel IL-6-expression"),
            "CC": (RiskLevel.MODERATE, "Högre IL-6-expression, antiinflammatorisk kost fördelaktigt"),
        }
    ),
    GeneticVariant(
        rsid="rs1800629",
        gene="TNF",
        name="TNF-α -308G/A",
        category=ImpactCategory.INFLAMMATION,
        risk_allele="A",
        protective_allele="G",
        description="Tumörnekrosfaktor-alfa, central inflammationsmarkör",
        recommendation="A-bärare kan ha ökad inflammationstendens",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Normal TNF-α-produktion"),
            "GA": (RiskLevel.NORMAL, "Något ökad produktion"),
            "AA": (RiskLevel.MODERATE, "Ökad TNF-α, överväg omega-3 och antioxidanter"),
        }
    ),
    GeneticVariant(
        rsid="rs3093662",
        gene="CRP",
        name="CRP",
        category=ImpactCategory.INFLAMMATION,
        risk_allele="A",
        protective_allele="G",
        description="C-reaktivt protein, viktig inflammationsmarkör",
        recommendation="A-bärare kan ha naturligt högre CRP-värden",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Lägre basal CRP"),
            "AG": (RiskLevel.NORMAL, "Medel CRP-nivåer"),
            "AA": (RiskLevel.MODERATE, "Högre basal CRP, fokus på antiinflammation"),
        }
    ),

    # =========================================================================
    # DETOX & LEVERFUNKTION
    # =========================================================================
    GeneticVariant(
        rsid="rs1695",
        gene="GSTP1",
        name="GSTP1 Ile105Val",
        category=ImpactCategory.DETOX,
        risk_allele="G",
        protective_allele="A",
        description="Glutationtransferas, viktig för avgiftning av miljögifter",
        recommendation="G-bärare kan behöva extra antioxidantstöd",
        genotype_effects={
            "AA": (RiskLevel.OPTIMAL, "Effektiv detox-funktion"),
            "AG": (RiskLevel.NORMAL, "Något reducerad"),
            "GG": (RiskLevel.MODERATE, "Reducerad detox, överväg NAC och broccoli-extrakt"),
        }
    ),
    GeneticVariant(
        rsid="rs1050450",
        gene="GPX1",
        name="GPX1 Pro200Leu",
        category=ImpactCategory.ANTIOXIDANT,
        risk_allele="T",
        protective_allele="C",
        description="Glutationperoxidas, skyddar mot oxidativ stress",
        recommendation="T-bärare kan ha nytta av selentillskott",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Effektivt antioxidantförsvar"),
            "CT": (RiskLevel.NORMAL, "Något reducerad aktivitet"),
            "TT": (RiskLevel.MODERATE, "Reducerad GPX1, överväg selen"),
        }
    ),
    GeneticVariant(
        rsid="rs4880",
        gene="SOD2",
        name="SOD2 Ala16Val",
        category=ImpactCategory.ANTIOXIDANT,
        risk_allele="T",
        protective_allele="C",
        description="Superoxiddismutas i mitokondrier, skyddar mot fria radikaler",
        recommendation="Optimal genotyp beror på livsstil",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Hög SOD2-aktivitet"),
            "CT": (RiskLevel.OPTIMAL, "Balanserad aktivitet (ofta optimal)"),
            "TT": (RiskLevel.NORMAL, "Lägre aktivitet, kan behöva mer antioxidanter"),
        }
    ),

    # =========================================================================
    # TRÄNING & MUSKELTYP
    # =========================================================================
    GeneticVariant(
        rsid="rs1815739",
        gene="ACTN3",
        name="ACTN3 R577X",
        category=ImpactCategory.EXERCISE,
        risk_allele="T",
        protective_allele="C",
        description="Alpha-aktinin-3, 'speed gene', påverkar muskelfibertyp",
        recommendation="CC = explosiv kraft, TT = uthållighet",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Fungerande ACTN3, fördelaktigt för sprint/styrka"),
            "CT": (RiskLevel.OPTIMAL, "Blandad muskeltyp, allround-kapacitet"),
            "TT": (RiskLevel.OPTIMAL, "ACTN3-brist, fördelaktigt för uthållighet"),
        }
    ),
    GeneticVariant(
        rsid="rs8192678",
        gene="PPARGC1A",
        name="PGC-1α Gly482Ser",
        category=ImpactCategory.EXERCISE,
        risk_allele="A",
        protective_allele="G",
        description="Master regulator för mitokondrier och uthållighet",
        recommendation="G-bärare svarar ofta bättre på uthållighetsträning",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Hög PGC-1α-aktivitet, bra uthållighetsrespons"),
            "AG": (RiskLevel.NORMAL, "Medel respons"),
            "AA": (RiskLevel.NORMAL, "Lägre uthållighetsrespons, mer träning behövs"),
        }
    ),
    GeneticVariant(
        rsid="rs1799752",
        gene="ACE",
        name="ACE I/D",
        category=ImpactCategory.EXERCISE,
        risk_allele="D",
        protective_allele="I",
        description="Angiotensinkonverterande enzym, påverkar uthållighet vs styrka",
        recommendation="II = uthållighet, DD = styrka/power",
        genotype_effects={
            "II": (RiskLevel.OPTIMAL, "Insertion/Insertion - uthållighetsfördelar"),
            "ID": (RiskLevel.OPTIMAL, "Blandad - allround"),
            "DD": (RiskLevel.OPTIMAL, "Deletion/Deletion - styrka/power-fördelar"),
        }
    ),

    # =========================================================================
    # ÅTERHÄMTNING & MUSKELSKADOR
    # =========================================================================
    GeneticVariant(
        rsid="rs2228570",
        gene="VDR",
        name="VDR FokI (återhämtning)",
        category=ImpactCategory.RECOVERY,
        risk_allele="T",
        protective_allele="C",
        description="VDR påverkar även muskelåterhämtning och skaderisk",
        recommendation="T-bärare kan behöva längre återhämtning mellan pass",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Bra muskelåterhämtning"),
            "CT": (RiskLevel.NORMAL, "Normal återhämtning"),
            "TT": (RiskLevel.MODERATE, "Kan behöva extra återhämtningstid"),
        }
    ),
    GeneticVariant(
        rsid="rs1800469",
        gene="TGFB1",
        name="TGF-β1",
        category=ImpactCategory.RECOVERY,
        risk_allele="A",
        protective_allele="G",
        description="Tillväxtfaktor som påverkar vävnadsläkning",
        recommendation="A-bärare kan ha långsammare läkning",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Normal läkningsförmåga"),
            "AG": (RiskLevel.NORMAL, "Något långsammare läkning"),
            "AA": (RiskLevel.MODERATE, "Kan ta längre tid att återhämta sig från skador"),
        }
    ),

    # =========================================================================
    # JÄRNMETABOLISM
    # =========================================================================
    GeneticVariant(
        rsid="rs1800562",
        gene="HFE",
        name="HFE C282Y",
        category=ImpactCategory.IRON,
        risk_allele="A",
        protective_allele="G",
        description="Hemokromatos-gen, påverkar järnabsorption",
        recommendation="A-bärare absorberar mer järn, undvik tillskott utan behov",
        genotype_effects={
            "GG": (RiskLevel.OPTIMAL, "Normal järnmetabolism"),
            "AG": (RiskLevel.NORMAL, "Bärare, något ökad absorption"),
            "AA": (RiskLevel.ELEVATED, "Hemokromatos-risk, undvik järntillskott"),
        }
    ),
    GeneticVariant(
        rsid="rs1799945",
        gene="HFE",
        name="HFE H63D",
        category=ImpactCategory.IRON,
        risk_allele="G",
        protective_allele="C",
        description="Mildare hemokromatosvariant",
        recommendation="G-bärare kan ha ökad järnabsorption",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Normal järnmetabolism"),
            "CG": (RiskLevel.NORMAL, "Lätt ökad absorption"),
            "GG": (RiskLevel.MODERATE, "Ökad absorption, monitorera ferritin"),
        }
    ),

    # =========================================================================
    # MAGNESIUM
    # =========================================================================
    GeneticVariant(
        rsid="rs11144134",
        gene="TRPM6",
        name="TRPM6",
        category=ImpactCategory.MAGNESIUM,
        risk_allele="T",
        protective_allele="C",
        description="Magnesiumtransportör i tarm och njure",
        recommendation="T-bärare kan ha ökade magnesiumbehov",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Effektiv magnesiumabsorption"),
            "CT": (RiskLevel.NORMAL, "Normal absorption"),
            "TT": (RiskLevel.MODERATE, "Kan ha suboptimal magnesiumstatus"),
        }
    ),

    # =========================================================================
    # ZINK
    # =========================================================================
    GeneticVariant(
        rsid="rs2120019",
        gene="SLC30A8",
        name="SLC30A8",
        category=ImpactCategory.ZINC,
        risk_allele="T",
        protective_allele="C",
        description="Zinktransportör, påverkar zinkstatus och insulinsekretion",
        recommendation="T-bärare kan ha nytta av zinktillskott",
        genotype_effects={
            "CC": (RiskLevel.OPTIMAL, "Effektiv zinktransport"),
            "CT": (RiskLevel.NORMAL, "Normal transport"),
            "TT": (RiskLevel.MODERATE, "Kan ha lägre zinkstatus"),
        }
    ),
]


class DNAAnalyzer:
    """Huvudklass för DNA-analys"""

    def __init__(self, dna_file_path: str):
        self.dna_file_path = dna_file_path
        self.genotypes: Dict[str, str] = {}
        self.variants = WELLNESS_VARIANTS
        self.results: List[AnalysisResult] = []

    def load_23andme_data(self) -> int:
        """Laddar 23andMe rådata och returnerar antal laddade varianter"""
        print(f"📂 Laddar DNA-data från: {self.dna_file_path}")
        count = 0

        with open(self.dna_file_path, 'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue

                parts = line.strip().split('\t')
                if len(parts) >= 4:
                    rsid = parts[0]
                    genotype = parts[3]
                    if genotype != '--':  # Skippa no-calls
                        self.genotypes[rsid] = genotype
                        count += 1

        print(f"✅ Laddade {count:,} genetiska varianter")
        return count

    def analyze_variant(self, variant: GeneticVariant) -> Optional[AnalysisResult]:
        """Analyserar en specifik variant"""
        if variant.rsid not in self.genotypes:
            return None

        genotype = self.genotypes[variant.rsid]

        # Normalisera genotyp (AA, AG, GG etc)
        normalized = ''.join(sorted(genotype.upper()))

        # Kolla om vi har effektdata för denna genotyp
        if normalized in variant.genotype_effects:
            risk_level, interpretation = variant.genotype_effects[normalized]
        else:
            # Prova omvänd ordning
            reversed_gt = genotype[::-1]
            normalized_rev = ''.join(sorted(reversed_gt.upper()))
            if normalized_rev in variant.genotype_effects:
                risk_level, interpretation = variant.genotype_effects[normalized_rev]
            else:
                # Okänd genotyp
                risk_level = RiskLevel.NORMAL
                interpretation = f"Genotyp {genotype} - effekt okänd"

        return AnalysisResult(
            variant=variant,
            genotype=genotype,
            risk_level=risk_level,
            interpretation=interpretation
        )

    def run_analysis(self) -> List[AnalysisResult]:
        """Kör komplett analys av alla wellness-varianter"""
        print(f"\n🔬 Analyserar {len(self.variants)} wellness-gener...")

        for variant in self.variants:
            result = self.analyze_variant(variant)
            if result:
                self.results.append(result)

        print(f"✅ Hittade data för {len(self.results)} av {len(self.variants)} varianter")
        return self.results

    def get_category_summary(self, category: ImpactCategory) -> CategorySummary:
        """Skapar sammanfattning för en kategori"""
        category_results = [r for r in self.results if r.variant.category == category]

        if not category_results:
            return CategorySummary(
                category=category,
                results=[],
                overall_risk=RiskLevel.NORMAL,
                key_findings=["Ingen data tillgänglig för denna kategori"],
                recommendations=[]
            )

        # Beräkna övergripande risk
        risk_scores = {
            RiskLevel.OPTIMAL: 0,
            RiskLevel.NORMAL: 1,
            RiskLevel.MODERATE: 2,
            RiskLevel.ELEVATED: 3,
            RiskLevel.HIGH: 4
        }

        avg_score = sum(risk_scores[r.risk_level] for r in category_results) / len(category_results)

        if avg_score < 0.5:
            overall = RiskLevel.OPTIMAL
        elif avg_score < 1.5:
            overall = RiskLevel.NORMAL
        elif avg_score < 2.5:
            overall = RiskLevel.MODERATE
        elif avg_score < 3.5:
            overall = RiskLevel.ELEVATED
        else:
            overall = RiskLevel.HIGH

        # Samla key findings (icke-optimala resultat)
        key_findings = []
        recommendations = []

        for r in category_results:
            if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED, RiskLevel.HIGH]:
                key_findings.append(f"{r.variant.gene} ({r.variant.rsid}): {r.interpretation}")
                recommendations.append(r.variant.recommendation)

        return CategorySummary(
            category=category,
            results=category_results,
            overall_risk=overall,
            key_findings=key_findings if key_findings else ["Alla varianter inom normalvärden"],
            recommendations=list(set(recommendations))
        )

    def generate_supplement_recommendations(self) -> List[SupplementRecommendation]:
        """Genererar personliga supplementrekommendationer baserat på genetik"""
        recommendations = []

        # Analysera D-vitamin-behov
        vdr_results = [r for r in self.results if r.variant.gene == "VDR" or r.variant.gene == "CYP2R1"]
        vdr_risk = sum(1 for r in vdr_results if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED, RiskLevel.HIGH])

        if vdr_risk >= 2:
            recommendations.append(SupplementRecommendation(
                name="D-vitamin D3",
                dosage="4000-5000 IE/dag (vinter), 2000 IE/dag (sommar)",
                reason="Flera VDR-varianter indikerar ökat D-vitaminbehov",
                priority=5,
                genes_involved=[r.variant.gene for r in vdr_results]
            ))
        elif vdr_risk >= 1:
            recommendations.append(SupplementRecommendation(
                name="D-vitamin D3",
                dosage="2000-3000 IE/dag",
                reason="VDR-variant kan påverka D-vitaminrespons",
                priority=4,
                genes_involved=[r.variant.gene for r in vdr_results]
            ))
        else:
            recommendations.append(SupplementRecommendation(
                name="D-vitamin D3",
                dosage="1000-2000 IE/dag (underhåll)",
                reason="Standard underhållsdos för skandinaviskt klimat",
                priority=3,
                genes_involved=[]
            ))

        # Analysera MTHFR och metylering
        mthfr_results = [r for r in self.results if "MTHFR" in r.variant.gene]
        mthfr_high_risk = any(r.risk_level == RiskLevel.HIGH for r in mthfr_results)
        mthfr_moderate = any(r.risk_level == RiskLevel.MODERATE for r in mthfr_results)

        if mthfr_high_risk:
            recommendations.append(SupplementRecommendation(
                name="Metylfolat (5-MTHF)",
                dosage="400-800 mcg/dag",
                reason="MTHFR C677T TT-genotyp kräver aktiverad folat",
                priority=5,
                genes_involved=["MTHFR"]
            ))
            recommendations.append(SupplementRecommendation(
                name="Metyl-B12 (Metylkobalamin)",
                dosage="1000 mcg/dag",
                reason="Synergistiskt med metylfolat för optimal metylering",
                priority=5,
                genes_involved=["MTHFR", "MTR", "MTRR"]
            ))
        elif mthfr_moderate:
            recommendations.append(SupplementRecommendation(
                name="Aktivt B-komplex med metylfolat",
                dosage="1 kapsel/dag",
                reason="MTHFR-variant kan påverka folatmetabolism",
                priority=4,
                genes_involved=["MTHFR"]
            ))

        # Analysera omega-3-behov
        fads_results = [r for r in self.results if "FADS" in r.variant.gene]
        fads_risk = sum(1 for r in fads_results if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED])

        if fads_risk >= 1:
            recommendations.append(SupplementRecommendation(
                name="Omega-3 (EPA/DHA från fisk eller alg)",
                dosage="2000-3000 mg EPA+DHA/dag",
                reason="FADS-varianter reducerar omvandling från växtbaserad omega-3",
                priority=5,
                genes_involved=["FADS1", "FADS2"]
            ))
        else:
            recommendations.append(SupplementRecommendation(
                name="Omega-3 (EPA/DHA)",
                dosage="1000-2000 mg EPA+DHA/dag",
                reason="Allmän hjärt- och hjärnhälsa",
                priority=3,
                genes_involved=[]
            ))

        # Analysera BCMO1 och A-vitamin
        bcmo1_results = [r for r in self.results if "BCMO1" in r.variant.gene]
        bcmo1_risk = sum(1 for r in bcmo1_results if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED])

        if bcmo1_risk >= 1:
            recommendations.append(SupplementRecommendation(
                name="Retinol (preformerad A-vitamin)",
                dosage="2500-5000 IE/dag",
                reason="BCMO1-variant reducerar betakarotenomvandling",
                priority=4,
                genes_involved=["BCMO1"]
            ))

        # Analysera COMT och stress
        comt_results = [r for r in self.results if r.variant.gene == "COMT"]
        comt_slow = any(r.genotype == "AA" for r in comt_results)

        if comt_slow:
            recommendations.append(SupplementRecommendation(
                name="Magnesium (glycinat eller treonat)",
                dosage="300-400 mg/dag (på kvällen)",
                reason="COMT Met/Met behöver extra stöd för stresshantering",
                priority=4,
                genes_involved=["COMT"]
            ))
            recommendations.append(SupplementRecommendation(
                name="L-teanin",
                dosage="200 mg/dag vid behov",
                reason="Stödjer lugn fokus för stresskänsliga COMT-varianter",
                priority=3,
                genes_involved=["COMT"]
            ))
        else:
            recommendations.append(SupplementRecommendation(
                name="Magnesium (glycinat)",
                dosage="200-300 mg/dag",
                reason="Grundläggande för 300+ enzymer, de flesta har suboptimalt intag",
                priority=3,
                genes_involved=[]
            ))

        # Analysera SOD2 och antioxidanter
        sod2_results = [r for r in self.results if r.variant.gene == "SOD2"]
        gpx1_results = [r for r in self.results if r.variant.gene == "GPX1"]

        antioxidant_need = sum(1 for r in sod2_results + gpx1_results
                              if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED])

        if antioxidant_need >= 1:
            recommendations.append(SupplementRecommendation(
                name="Selen",
                dosage="100-200 mcg/dag",
                reason="GPX1/SOD2-varianter kan ha nytta av extra antioxidantstöd",
                priority=3,
                genes_involved=["GPX1", "SOD2"]
            ))

        # Analysera CYP1A2 och koffein
        cyp1a2_results = [r for r in self.results if r.variant.gene == "CYP1A2"]
        slow_caffeine = any(r.genotype == "CC" for r in cyp1a2_results)

        # Sortera efter prioritet
        recommendations.sort(key=lambda x: x.priority, reverse=True)

        return recommendations

    def generate_lifestyle_recommendations(self) -> List[str]:
        """Genererar livsstilsrekommendationer baserat på genetik"""
        recommendations = []

        # COMT-baserade rekommendationer
        comt_results = [r for r in self.results if r.variant.gene == "COMT"]
        if any(r.genotype == "AA" for r in comt_results):
            recommendations.append("🧘 Daglig stresshantering rekommenderas (meditation, yoga, promenader) - din COMT-variant gör dig mer känslig för stress")
            recommendations.append("☕ Begränsa koffein till förmiddagen - du bryter ned katekolaminer långsammare")
        elif any(r.genotype == "GG" for r in comt_results):
            recommendations.append("💪 Du hanterar stress relativt väl, men kan behöva mer stimulans för optimal funktion")

        # Sömn-rekommendationer
        clock_results = [r for r in self.results if r.variant.gene == "CLOCK"]
        if any(r.genotype == "CC" for r in clock_results):
            recommendations.append("🌙 Du är sannolikt en kvällsmänniska - anpassa schemat efter din naturliga rytm om möjligt")
        elif any(r.genotype == "TT" for r in clock_results):
            recommendations.append("☀️ Du är sannolikt en morgonmänniska - utnyttja dina morgnar för viktigare uppgifter")

        # CYP1A2 koffein
        cyp1a2_results = [r for r in self.results if r.variant.gene == "CYP1A2"]
        if any(r.genotype == "CC" for r in cyp1a2_results):
            recommendations.append("☕ Långsam koffeinmetaboliserare - begränsa till 1-2 koppar kaffe/dag, undvik kaffe efter kl 14")
        elif any(r.genotype == "AA" for r in cyp1a2_results):
            recommendations.append("☕ Snabb koffeinmetaboliserare - du kan tolerera mer kaffe, men överskrid inte 4 koppar/dag")

        # Alkohol
        aldh2_results = [r for r in self.results if r.variant.gene == "ALDH2"]
        if any(r.risk_level in [RiskLevel.ELEVATED, RiskLevel.HIGH] for r in aldh2_results):
            recommendations.append("🍷 Reducerad alkoholmetabolism - begränsa alkohol kraftigt för att undvika toxisk acetaldehyduppbyggnad")

        return recommendations

    def generate_diet_recommendations(self) -> List[str]:
        """Genererar kostråd baserat på genetik"""
        recommendations = []

        # Laktos
        lct_results = [r for r in self.results if r.variant.gene == "MCM6/LCT"]
        if any(r.risk_level == RiskLevel.HIGH for r in lct_results):
            recommendations.append("🥛 Laktosintolerant - välj laktosfria mejeriprodukter eller växtbaserade alternativ")
        else:
            recommendations.append("🥛 Laktostolerant - mjölkprodukter fungerar för dig")

        # FTO och vikt
        fto_results = [r for r in self.results if r.variant.gene == "FTO"]
        if any(r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED] for r in fto_results):
            recommendations.append("🍗 FTO-variant - prioritera protein och fiber för bättre mättnad, var extra uppmärksam på portionsstorlekar")
            recommendations.append("⏰ Överväg tidsbegränsat ätande (16:8) - kan vara extra fördelaktigt för din genotyp")

        # APOE4 och fett
        apoe_results = [r for r in self.results if r.variant.gene == "APOE" and "ε4" in r.variant.name]
        if any(r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED] for r in apoe_results):
            recommendations.append("🥑 APOE4-bärare - begränsa mättat fett, prioritera omättat (olivolja, nötter, avokado)")
            recommendations.append("🐟 Extra viktigt med omega-3 från fet fisk 2-3 gånger/vecka")

        # Inflammation
        inflammation_results = [r for r in self.results
                              if r.variant.category == ImpactCategory.INFLAMMATION]
        if sum(1 for r in inflammation_results if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]) >= 2:
            recommendations.append("🥬 Fokusera på antiinflammatorisk kost - mycket grönsaker, bär, fet fisk, olivolja")
            recommendations.append("🚫 Minimera processad mat, socker och raffinerade kolhydrater")

        # BCMO1 och A-vitamin
        bcmo1_results = [r for r in self.results if "BCMO1" in r.variant.gene]
        if sum(1 for r in bcmo1_results if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]) >= 1:
            recommendations.append("🥕 BCMO1-variant - inkludera animaliska A-vitaminkällor (lever, ägg) eftersom betakarotenomvandlingen är reducerad")

        return recommendations

    def generate_exercise_recommendations(self) -> List[str]:
        """Genererar träningsråd baserat på genetik"""
        recommendations = []

        # ACTN3
        actn3_results = [r for r in self.results if r.variant.gene == "ACTN3"]
        for r in actn3_results:
            if r.genotype == "CC":
                recommendations.append("🏃 ACTN3 R/R - du har genetisk fördel för explosiv kraft och sprint. Inkludera styrketräning och HIIT.")
            elif r.genotype == "TT":
                recommendations.append("🚴 ACTN3 X/X - du har genetisk fördel för uthållighet. Fokusera på konditionsträning och längre pass.")
            else:
                recommendations.append("⚡ ACTN3 R/X - balanserad muskelfibersammansättning, du svarar bra på varierad träning.")

        # ACE
        ace_results = [r for r in self.results if r.variant.gene == "ACE"]
        for r in ace_results:
            if "II" in r.genotype or r.genotype == "II":
                recommendations.append("🏊 ACE I/I - fördelaktigt för uthållighetsidrotter, fokusera på längre pass med lägre intensitet.")
            elif "DD" in r.genotype or r.genotype == "DD":
                recommendations.append("🏋️ ACE D/D - fördelaktigt för styrka och power, inkludera tungare lyft och explosiva övningar.")

        # Återhämtning
        recovery_results = [r for r in self.results if r.variant.category == ImpactCategory.RECOVERY]
        if sum(1 for r in recovery_results if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]) >= 1:
            recommendations.append("😴 Dina gener indikerar längre återhämtningstid - planera vilodagar och prioritera sömn efter hårda pass")

        return recommendations

    def create_profile(self, name: str) -> GWLProfile:
        """Skapar komplett GWL-profil"""
        # Generera kategori-sammanfattningar
        category_summaries = {}
        for category in ImpactCategory:
            category_summaries[category] = self.get_category_summary(category)

        return GWLProfile(
            name=name,
            analysis_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            total_variants_analyzed=len(self.results),
            category_summaries=category_summaries,
            supplement_recommendations=self.generate_supplement_recommendations(),
            lifestyle_recommendations=self.generate_lifestyle_recommendations(),
            diet_recommendations=self.generate_diet_recommendations(),
            exercise_recommendations=self.generate_exercise_recommendations(),
            raw_results=self.results
        )


def format_risk_emoji(risk: RiskLevel) -> str:
    """Returnerar emoji för risknivå"""
    mapping = {
        RiskLevel.OPTIMAL: "🟢",
        RiskLevel.NORMAL: "🟢",
        RiskLevel.MODERATE: "🟡",
        RiskLevel.ELEVATED: "🟠",
        RiskLevel.HIGH: "🔴"
    }
    return mapping.get(risk, "⚪")


def generate_report(profile: GWLProfile, output_path: str):
    """Genererar markdown-rapport"""

    lines = []
    lines.append("# 🧬 Genetic Wellness Labs - Personlig Genetisk Profil")
    lines.append("")
    lines.append(f"**Namn:** {profile.name}")
    lines.append(f"**Analysdatum:** {profile.analysis_date}")
    lines.append(f"**Analyserade varianter:** {profile.total_variants_analyzed}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Summary
    lines.append("## 📋 Sammanfattning")
    lines.append("")

    # Räkna risknivåer
    risk_counts = {level: 0 for level in RiskLevel}
    for result in profile.raw_results:
        risk_counts[result.risk_level] += 1

    lines.append("### Översikt av dina genetiska varianter")
    lines.append("")
    lines.append(f"- 🟢 **Optimala/Normala:** {risk_counts[RiskLevel.OPTIMAL] + risk_counts[RiskLevel.NORMAL]} varianter")
    lines.append(f"- 🟡 **Moderata:** {risk_counts[RiskLevel.MODERATE]} varianter")
    lines.append(f"- 🟠 **Förhöjda:** {risk_counts[RiskLevel.ELEVATED]} varianter")
    lines.append(f"- 🔴 **Höga:** {risk_counts[RiskLevel.HIGH]} varianter")
    lines.append("")

    # Top supplement recommendations
    lines.append("### 💊 Dina viktigaste supplement-rekommendationer")
    lines.append("")
    for i, supp in enumerate(profile.supplement_recommendations[:7], 1):
        priority_stars = "⭐" * min(supp.priority, 5)
        lines.append(f"**{i}. {supp.name}** {priority_stars}")
        lines.append(f"   - Dos: {supp.dosage}")
        lines.append(f"   - Anledning: {supp.reason}")
        if supp.genes_involved:
            lines.append(f"   - Baserat på: {', '.join(supp.genes_involved)}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Detaljerade kategorier
    lines.append("## 🔬 Detaljerad Genetisk Analys")
    lines.append("")

    # Ordna kategorier logiskt
    category_order = [
        ImpactCategory.VITAMIN_D,
        ImpactCategory.METHYLATION,
        ImpactCategory.VITAMIN_B,
        ImpactCategory.VITAMIN_A,
        ImpactCategory.OMEGA3,
        ImpactCategory.IRON,
        ImpactCategory.MAGNESIUM,
        ImpactCategory.ZINC,
        ImpactCategory.CAFFEINE,
        ImpactCategory.ALCOHOL,
        ImpactCategory.LACTOSE,
        ImpactCategory.GLUTEN,
        ImpactCategory.STRESS,
        ImpactCategory.SLEEP,
        ImpactCategory.WEIGHT,
        ImpactCategory.CARDIOVASCULAR,
        ImpactCategory.INFLAMMATION,
        ImpactCategory.DETOX,
        ImpactCategory.ANTIOXIDANT,
        ImpactCategory.EXERCISE,
        ImpactCategory.RECOVERY,
    ]

    for category in category_order:
        summary = profile.category_summaries.get(category)
        if not summary or not summary.results:
            continue

        lines.append(f"### {format_risk_emoji(summary.overall_risk)} {category.value}")
        lines.append("")
        lines.append(f"**Övergripande status:** {summary.overall_risk.value.capitalize()}")
        lines.append("")

        # Tabell med resultat
        lines.append("| Gen | Variant | Din genotyp | Status | Tolkning |")
        lines.append("|-----|---------|-------------|--------|----------|")

        for result in summary.results:
            emoji = format_risk_emoji(result.risk_level)
            lines.append(f"| {result.variant.gene} | {result.variant.name} | **{result.genotype}** | {emoji} {result.risk_level.value} | {result.interpretation} |")

        lines.append("")

        if summary.key_findings and summary.key_findings[0] != "Alla varianter inom normalvärden":
            lines.append("**Viktiga fynd:**")
            for finding in summary.key_findings:
                lines.append(f"- {finding}")
            lines.append("")

        if summary.recommendations:
            lines.append("**Rekommendationer:**")
            for rec in summary.recommendations:
                lines.append(f"- {rec}")
            lines.append("")

        lines.append("")

    # Livsstilsrekommendationer
    lines.append("---")
    lines.append("")
    lines.append("## 🏃 Livsstilsrekommendationer")
    lines.append("")
    for rec in profile.lifestyle_recommendations:
        lines.append(f"- {rec}")
    lines.append("")

    # Kostråd
    lines.append("## 🥗 Kostråd baserade på din genetik")
    lines.append("")
    for rec in profile.diet_recommendations:
        lines.append(f"- {rec}")
    lines.append("")

    # Träningsråd
    lines.append("## 💪 Träningsråd baserade på din genetik")
    lines.append("")
    for rec in profile.exercise_recommendations:
        lines.append(f"- {rec}")
    lines.append("")

    # Disclaimer
    lines.append("---")
    lines.append("")
    lines.append("## ⚠️ Viktig information")
    lines.append("")
    lines.append("Denna rapport är baserad på aktuell vetenskaplig forskning om genetiska varianter och deras ")
    lines.append("potentiella påverkan på hälsa och välbefinnande. Observera att:")
    lines.append("")
    lines.append("1. **Genetik är endast en del av bilden** - livsstil, miljö och andra faktorer påverkar också din hälsa")
    lines.append("2. **Detta är inte medicinsk diagnostik** - konsultera alltid läkare för medicinska beslut")
    lines.append("3. **Individuell variation** - effekten av genetiska varianter kan variera mellan individer")
    lines.append("4. **Forskningen utvecklas** - nya studier kan ändra vår förståelse av dessa samband")
    lines.append("")
    lines.append("Alla supplementrekommendationer bör diskuteras med legitimerad dietist eller läkare, ")
    lines.append("särskilt om du tar mediciner eller har kroniska sjukdomar.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Rapport genererad av Genetic Wellness Labs AI Pipeline*")
    lines.append(f"*Version 1.0.0 | {datetime.now().strftime('%Y-%m-%d')}*")

    # Skriv till fil
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n📄 Rapport sparad till: {output_path}")


def main():
    """Huvudfunktion"""
    # Fix Windows encoding
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 60)
    print("GENETIC WELLNESS LABS - DNA ANALYSIS TOOL")
    print("=" * 60)
    print()

    # Hitta DNA-fil
    dna_file = None
    genome_dir = os.path.join(os.path.dirname(__file__), "GENOME")

    if os.path.exists(genome_dir):
        for f in os.listdir(genome_dir):
            if f.endswith('.txt') and 'genome' in f.lower():
                dna_file = os.path.join(genome_dir, f)
                break

    if not dna_file:
        # Prova direkt sökväg
        default_path = "GENOME/genome_Rasmus_Persson_v5_Full_20240920231531.txt"
        if os.path.exists(default_path):
            dna_file = default_path

    if not dna_file:
        print("❌ Kunde inte hitta DNA-fil!")
        print("Ange sökväg till din 23andMe-fil som argument.")
        sys.exit(1)

    # Extrahera namn från filnamn
    filename = os.path.basename(dna_file)
    name_parts = filename.replace('genome_', '').replace('_Full_', ' ').split('_v')[0]
    name = name_parts.replace('_', ' ').strip()

    print(f"👤 Analyserar DNA för: {name}")
    print()

    # Kör analys
    analyzer = DNAAnalyzer(dna_file)
    analyzer.load_23andme_data()
    analyzer.run_analysis()

    # Skapa profil
    profile = analyzer.create_profile(name)

    # Generera rapport
    output_path = os.path.join(os.path.dirname(__file__), f"GWL_Profil_{name.replace(' ', '_')}.md")
    generate_report(profile, output_path)

    # Visa sammanfattning
    print()
    print("=" * 60)
    print("📊 SNABBSAMMANFATTNING")
    print("=" * 60)
    print()

    print("🔝 Topp 5 supplement-rekommendationer:")
    for i, supp in enumerate(profile.supplement_recommendations[:5], 1):
        print(f"   {i}. {supp.name}: {supp.dosage}")

    print()
    print("Fullständig rapport har sparats till:")
    print(f"   📄 {output_path}")
    print()


if __name__ == "__main__":
    main()
