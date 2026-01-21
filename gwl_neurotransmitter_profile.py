#!/usr/bin/env python3
"""
GWL Neurotransmitter Profile Generator
======================================
Analyzes genetic variants to create comprehensive neurotransmitter profiles.

Explains WHY someone has certain tendencies:
- Dopamine: Motivation, focus, reward, ADHD tendencies
- Serotonin: Mood stability, anxiety, impulsivity
- GABA: Calm, anxiety resistance, stress tolerance
- Norepinephrine: Alertness, attention, fight-or-flight

Genetic Wellness Labs - Nutrigenomics Platform
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class Level(Enum):
    VERY_LOW = 1
    LOW = 2
    NORMAL = 3
    HIGH = 4
    VERY_HIGH = 5


@dataclass
class NeurotransmitterScore:
    """Score for a single neurotransmitter system."""
    name: str
    baseline_level: Level
    sensitivity: Level
    clearance_speed: str  # "slow", "normal", "fast"
    key_findings: List[str]
    recommendations: List[str]
    contributing_genes: List[Tuple[str, str, str]]  # (gene, genotype, effect)


@dataclass
class NeurotransmitterProfile:
    """Complete neurotransmitter profile."""
    dopamine: NeurotransmitterScore
    serotonin: NeurotransmitterScore
    gaba: NeurotransmitterScore
    norepinephrine: NeurotransmitterScore
    overall_type: str
    personality_traits: List[str]
    adhd_risk_factors: List[str]
    optimization_strategies: List[str]


# =============================================================================
# DOPAMINE ANALYSIS
# =============================================================================

def analyze_dopamine(genotypes: Dict[str, str]) -> NeurotransmitterScore:
    """
    Analyze dopamine system genetics.

    Key genes:
    - COMT (rs4680): Dopamine breakdown - Met/Met = slow = HIGH dopamine
    - DRD2 (rs1800497): Receptor density - A1+ = fewer receptors
    - DRD4 (rs1800955): Novelty seeking
    - DAT1/SLC6A3: Dopamine reuptake
    - DBH: Dopamine to norepinephrine conversion
    - TH: Dopamine synthesis
    """
    findings = []
    recommendations = []
    genes = []

    baseline_score = 0  # -2 to +2 scale
    sensitivity_score = 0
    clearance = "normal"

    # COMT Val158Met (rs4680) - MOST IMPORTANT
    comt = genotypes.get('rs4680', '').upper()
    if comt:
        if comt in ['AA', 'A/A']:  # Met/Met - slow COMT
            baseline_score += 2
            clearance = "slow"
            findings.append("COMT Met/Met: Långsam dopaminnedbrytning = HÖGA dopaminnivåer")
            findings.append("'Worrier'-typ: Bättre kognition men känsligare för stress")
            recommendations.append("Undvik överstimulering (koffein, intensiv träning sent)")
            recommendations.append("Prioritera stresshantering och återhämtning")
            recommendations.append("Magnesium och B-vitaminer stödjer COMT")
            genes.append(("COMT", comt, "Långsam nedbrytning - Hög dopamin"))
        elif comt in ['GG', 'G/G']:  # Val/Val - fast COMT
            baseline_score -= 1
            clearance = "fast"
            findings.append("COMT Val/Val: Snabb dopaminnedbrytning = lägre dopaminnivåer")
            findings.append("'Warrior'-typ: Stresstålig men kan behöva mer stimulans")
            recommendations.append("Kan tolerera mer stimulans och intensiv träning")
            recommendations.append("Tyrosin/L-DOPA kan stödja dopaminproduktion")
            genes.append(("COMT", comt, "Snabb nedbrytning - Normal/låg dopamin"))
        else:  # AG - heterozygot
            findings.append("COMT Val/Met: Balanserad dopaminnedbrytning")
            genes.append(("COMT", comt, "Balanserad nedbrytning"))

    # DRD2 Taq1A (rs1800497)
    drd2 = genotypes.get('rs1800497', '').upper()
    if drd2:
        if drd2 in ['AA', 'A/A', 'TT', 'T/T']:  # A1/A1 - reduced receptors
            sensitivity_score -= 2
            findings.append("DRD2 A1/A1: Färre D2-receptorer = behöver mer stimulans för belöning")
            findings.append("Ökad risk för beroendebeteende")
            recommendations.append("Var medveten om beroendetendenser")
            recommendations.append("Fokusera på naturliga dopaminhöjare: träning, musik, mål")
            genes.append(("DRD2", drd2, "Låg receptordensitet"))
        elif drd2 in ['GG', 'G/G', 'CC', 'C/C']:  # A2/A2 - normal receptors
            findings.append("DRD2 A2/A2: Normal D2-receptordensitet")
            genes.append(("DRD2", drd2, "Normal receptordensitet"))
        else:
            findings.append("DRD2 A1/A2: Något reducerad D2-receptordensitet")
            sensitivity_score -= 1
            genes.append(("DRD2", drd2, "Något reducerad receptordensitet"))

    # DRD2 C957T (rs6277)
    drd2_c957t = genotypes.get('rs6277', '').upper()
    if drd2_c957t:
        if drd2_c957t in ['TT', 'T/T']:
            findings.append("DRD2 C957T TT: Ökad D2-receptortillgänglighet")
            sensitivity_score += 1
            genes.append(("DRD2", drd2_c957t, "Ökad receptortillgänglighet"))

    # DRD4 (rs1800955) - Novelty seeking
    drd4 = genotypes.get('rs1800955', '').upper()
    if drd4:
        if drd4 in ['CC', 'C/C']:
            findings.append("DRD4 -521 CC: Lägre DRD4-uttryck = ökad nyhetssökande")
            recommendations.append("Kanalisera nyhetssökande till produktiva aktiviteter")
            genes.append(("DRD4", drd4, "Novelty seeking-tendens"))

    # DAT1/SLC6A3 (rs27072)
    dat1 = genotypes.get('rs27072', '').upper()
    if dat1:
        if dat1 in ['TT', 'T/T']:
            findings.append("DAT1: Ökad dopamintransportör = snabbare clearance")
            if clearance == "slow":
                clearance = "normal"
            else:
                clearance = "fast"
            genes.append(("DAT1", dat1, "Ökad dopamin-reuptake"))

    # DBH (rs1611115)
    dbh = genotypes.get('rs1611115', '').upper()
    if dbh:
        if dbh in ['TT', 'T/T']:
            findings.append("DBH -1021 TT: Låg DBH = mer dopamin, mindre noradrenalin")
            baseline_score += 1
            genes.append(("DBH", dbh, "Låg DA→NE konvertering"))
        elif dbh in ['CC', 'C/C']:
            findings.append("DBH -1021 CC: Hög DBH = snabb dopamin→noradrenalin")
            baseline_score -= 1
            genes.append(("DBH", dbh, "Hög DA→NE konvertering"))

    # DARPP-32 (rs907094)
    darpp = genotypes.get('rs907094', '').upper()
    if darpp:
        genes.append(("DARPP-32", darpp, "Dopaminsignalering"))

    # Calculate levels
    if baseline_score >= 2:
        baseline = Level.HIGH
    elif baseline_score >= 1:
        baseline = Level.HIGH
    elif baseline_score <= -2:
        baseline = Level.LOW
    elif baseline_score <= -1:
        baseline = Level.LOW
    else:
        baseline = Level.NORMAL

    if sensitivity_score >= 1:
        sensitivity = Level.HIGH
    elif sensitivity_score <= -1:
        sensitivity = Level.LOW
    else:
        sensitivity = Level.NORMAL

    return NeurotransmitterScore(
        name="Dopamin",
        baseline_level=baseline,
        sensitivity=sensitivity,
        clearance_speed=clearance,
        key_findings=findings,
        recommendations=recommendations,
        contributing_genes=genes
    )


# =============================================================================
# SEROTONIN ANALYSIS
# =============================================================================

def analyze_serotonin(genotypes: Dict[str, str]) -> NeurotransmitterScore:
    """
    Analyze serotonin system genetics.

    Key genes:
    - SLC6A4 (5-HTTLPR, rs25531): Serotonin transporter
    - TPH2 (rs4570625): Serotonin synthesis
    - HTR1A (rs6295): 5-HT1A autoreceptor
    - HTR2A (rs6311, rs6313): 5-HT2A receptor
    - MAOA (rs6323): Serotonin breakdown
    """
    findings = []
    recommendations = []
    genes = []

    baseline_score = 0
    sensitivity_score = 0
    clearance = "normal"

    # SLC6A4/5-HTTLPR (rs25531)
    sert = genotypes.get('rs25531', '').upper()
    if sert:
        if sert in ['AA', 'A/A']:  # Short/short or La/La depending on interpretation
            findings.append("SERT: Reducerad serotonintransportör")
            findings.append("Kan vara känsligare för stress och negativa upplevelser")
            sensitivity_score += 1
            recommendations.append("Extra fokus på stresshantering")
            recommendations.append("Regelbunden träning ökar serotonin naturligt")
            genes.append(("SLC6A4", sert, "Känsligare för miljöpåverkan"))

    # TPH2 (rs4570625) - Serotonin synthesis
    tph2 = genotypes.get('rs4570625', '').upper()
    if tph2:
        if tph2 in ['TT', 'T/T']:
            baseline_score -= 1
            findings.append("TPH2 T/T: Kan ha lägre serotoninsyntes")
            recommendations.append("Säkerställ tillräcklig tryptofan i kosten")
            genes.append(("TPH2", tph2, "Reducerad serotoninsyntes"))
        elif tph2 in ['GG', 'G/G']:
            findings.append("TPH2 G/G: Normal serotoninsyntes")
            genes.append(("TPH2", tph2, "Normal syntes"))

    # HTR1A (rs6295) - Autoreceptor
    htr1a = genotypes.get('rs6295', '').upper()
    if htr1a:
        if htr1a in ['GG', 'G/G']:
            findings.append("HTR1A G/G: Fler 5-HT1A autorecept. = lägre serotoninfrisättning")
            baseline_score -= 1
            findings.append("Ökad risk för ångest och depression")
            recommendations.append("SSRI kan vara mer effektiva vid behov")
            genes.append(("HTR1A", htr1a, "Lägre serotoninfrisättning"))
        elif htr1a in ['CC', 'C/C']:
            findings.append("HTR1A C/C: Färre autorecept. = bättre serotoninsignalering")
            baseline_score += 1
            genes.append(("HTR1A", htr1a, "Bättre serotoninsignalering"))

    # HTR2A (rs6311)
    htr2a = genotypes.get('rs6311', '').upper()
    if htr2a:
        if htr2a in ['AA', 'A/A']:
            findings.append("HTR2A -1438 A/A: Ökad 5-HT2A-receptortäthet")
            sensitivity_score += 1
            genes.append(("HTR2A", htr2a, "Ökad receptortäthet"))

    # HTR2A (rs6313) - T102C
    htr2a_t102c = genotypes.get('rs6313', '').upper()
    if htr2a_t102c:
        genes.append(("HTR2A", htr2a_t102c, "T102C variant"))

    # MAOA (rs6323)
    maoa = genotypes.get('rs6323', '').upper()
    if maoa:
        if maoa in ['TT', 'T/T']:
            findings.append("MAOA T/T: Högre MAO-A aktivitet = snabbare serotoninnedbrytning")
            clearance = "fast"
            genes.append(("MAOA", maoa, "Snabb nedbrytning"))
        elif maoa in ['GG', 'G/G']:
            findings.append("MAOA G/G: Lägre MAO-A aktivitet = långsammare nedbrytning")
            clearance = "slow"
            genes.append(("MAOA", maoa, "Långsam nedbrytning"))

    # Calculate levels
    if baseline_score >= 1:
        baseline = Level.HIGH
    elif baseline_score <= -1:
        baseline = Level.LOW
    else:
        baseline = Level.NORMAL

    if sensitivity_score >= 1:
        sensitivity = Level.HIGH
    elif sensitivity_score <= -1:
        sensitivity = Level.LOW
    else:
        sensitivity = Level.NORMAL

    # Add general recommendations
    if not recommendations:
        recommendations.append("Regelbunden motion ökar serotonin naturligt")
        recommendations.append("Solljus och ljusterapi kan hjälpa")
    recommendations.append("Omega-3 (EPA/DHA) stödjer serotoninsystemet")

    return NeurotransmitterScore(
        name="Serotonin",
        baseline_level=baseline,
        sensitivity=sensitivity,
        clearance_speed=clearance,
        key_findings=findings if findings else ["Inga betydande serotonin-varianter hittade"],
        recommendations=recommendations,
        contributing_genes=genes
    )


# =============================================================================
# GABA ANALYSIS
# =============================================================================

def analyze_gaba(genotypes: Dict[str, str]) -> NeurotransmitterScore:
    """
    Analyze GABA system genetics.

    Key genes:
    - GABRA2 (rs279858, rs567926): GABA-A receptor alpha-2
    - GABRG2 (rs211037): GABA-A receptor gamma-2
    - GAD1 (rs3749034): Glutamate to GABA enzyme
    - GAD2: GABA synthesis
    """
    findings = []
    recommendations = []
    genes = []

    baseline_score = 0
    sensitivity_score = 0

    # GABRA2 (rs279858)
    gabra2 = genotypes.get('rs279858', '').upper()
    if gabra2:
        if gabra2 in ['AA', 'A/A']:
            findings.append("GABRA2 A/A: Förändrad GABA-A receptor = ökad ångestrisk")
            findings.append("Ökad risk för alkoholberoende")
            baseline_score -= 1
            recommendations.append("Var försiktig med alkohol - ökad beroendetrigg")
            recommendations.append("L-theanin och magnesium kan stödja GABA")
            genes.append(("GABRA2", gabra2, "Förändrad GABA-receptor"))
        else:
            genes.append(("GABRA2", gabra2, "Normal variant"))

    # GABRA2 (rs567926)
    gabra2_2 = genotypes.get('rs567926', '').upper()
    if gabra2_2:
        genes.append(("GABRA2", gabra2_2, "Ångest/impulsivitet-variant"))

    # GABRG2 (rs211037)
    gabrg2 = genotypes.get('rs211037', '').upper()
    if gabrg2:
        if gabrg2 in ['TT', 'T/T']:
            findings.append("GABRG2 T/T: Förändrad GABA-A gamma-2 = ökad ångestkänslighet")
            sensitivity_score += 1
            genes.append(("GABRG2", gabrg2, "Ökad ångestkänslighet"))
        else:
            genes.append(("GABRG2", gabrg2, "Normal variant"))

    # GAD1 (rs3749034)
    gad1 = genotypes.get('rs3749034', '').upper()
    if gad1:
        genes.append(("GAD1", gad1, "GABA-syntesenzym"))
        # Note: specific effects depend on variant

    # Calculate levels
    if baseline_score >= 1:
        baseline = Level.HIGH
    elif baseline_score <= -1:
        baseline = Level.LOW
    else:
        baseline = Level.NORMAL

    if sensitivity_score >= 1:
        sensitivity = Level.HIGH
    else:
        sensitivity = Level.NORMAL

    # General recommendations
    if baseline == Level.LOW or sensitivity == Level.HIGH:
        recommendations.append("Andningsövningar och meditation stärker GABA-systemet")
        recommendations.append("Överväg GABA-stödjande kosttillskott (L-theanin, taurin)")
        recommendations.append("Yoga och tai chi ökar GABA naturligt")

    return NeurotransmitterScore(
        name="GABA",
        baseline_level=baseline,
        sensitivity=sensitivity,
        clearance_speed="normal",
        key_findings=findings if findings else ["Inga betydande GABA-varianter hittade"],
        recommendations=recommendations if recommendations else ["GABA-systemet verkar normalt"],
        contributing_genes=genes
    )


# =============================================================================
# NOREPINEPHRINE ANALYSIS
# =============================================================================

def analyze_norepinephrine(genotypes: Dict[str, str]) -> NeurotransmitterScore:
    """
    Analyze norepinephrine system genetics.

    Key genes:
    - DBH (rs1611115, rs6271): Dopamine beta-hydroxylase
    - SLC6A2/NET (rs5569, rs2242446): Norepinephrine transporter
    - ADRA2A (rs1800544): Alpha-2A adrenergic receptor
    - COMT: Also breaks down NE
    """
    findings = []
    recommendations = []
    genes = []

    baseline_score = 0
    sensitivity_score = 0
    clearance = "normal"

    # DBH (rs1611115) - Primary NE synthesis
    dbh = genotypes.get('rs1611115', '').upper()
    if dbh:
        if dbh in ['TT', 'T/T']:
            baseline_score -= 1
            findings.append("DBH -1021 T/T: Låg DBH-aktivitet = lägre noradrenalinnivåer")
            findings.append("Kan påverka uppmärksamhet och fokus")
            recommendations.append("Koffeein kan tillfälligt öka noradrenalin")
            genes.append(("DBH", dbh, "Låg NE-produktion"))
        elif dbh in ['CC', 'C/C']:
            baseline_score += 1
            findings.append("DBH -1021 C/C: Hög DBH = effektiv noradrenalinproduktion")
            genes.append(("DBH", dbh, "Hög NE-produktion"))

    # DBH (rs6271) - Arg535Cys
    dbh_r535c = genotypes.get('rs6271', '').upper()
    if dbh_r535c:
        genes.append(("DBH", dbh_r535c, "Arg535Cys variant"))

    # NET/SLC6A2 (rs5569)
    net = genotypes.get('rs5569', '').upper()
    if net:
        if net in ['GG', 'G/G']:
            findings.append("NET G1287G: Normal noradrenalin-reuptake")
            genes.append(("NET", net, "Normal reuptake"))
        else:
            genes.append(("NET", net, "Variant"))

    # NET (rs2242446) - ADHD association
    net_adhd = genotypes.get('rs2242446', '').upper()
    if net_adhd:
        if net_adhd in ['TT', 'T/T']:
            findings.append("NET T-182T: Associerad med ADHD och uppmärksamhetssvårigheter")
            recommendations.append("Strukturerad miljö och rutiner hjälper")
            genes.append(("NET", net_adhd, "ADHD-association"))

    # ADRA2A (rs1800544)
    adra2a = genotypes.get('rs1800544', '').upper()
    if adra2a:
        if adra2a in ['GG', 'G/G']:
            findings.append("ADRA2A -1291 G/G: Kan påverka uppmärksamhet/fokus")
            genes.append(("ADRA2A", adra2a, "Uppmärksamhets-variant"))
        elif adra2a in ['CC', 'C/C']:
            findings.append("ADRA2A -1291 C/C: Normal alfa-2A-receptorfunktion")
            genes.append(("ADRA2A", adra2a, "Normal funktion"))

    # COMT affects NE too
    comt = genotypes.get('rs4680', '').upper()
    if comt:
        if comt in ['AA', 'A/A']:
            findings.append("COMT Met/Met påverkar även noradrenalin (långsam nedbrytning)")
            clearance = "slow"
        elif comt in ['GG', 'G/G']:
            clearance = "fast"

    # Calculate levels
    if baseline_score >= 1:
        baseline = Level.HIGH
    elif baseline_score <= -1:
        baseline = Level.LOW
    else:
        baseline = Level.NORMAL

    return NeurotransmitterScore(
        name="Noradrenalin",
        baseline_level=baseline,
        sensitivity=Level.NORMAL,
        clearance_speed=clearance,
        key_findings=findings if findings else ["Inga betydande NE-varianter hittade"],
        recommendations=recommendations if recommendations else ["Noradrenalinsystemet verkar balanserat"],
        contributing_genes=genes
    )


# =============================================================================
# COMPLETE PROFILE GENERATION
# =============================================================================

def determine_personality_type(dopamine: NeurotransmitterScore,
                                serotonin: NeurotransmitterScore,
                                gaba: NeurotransmitterScore,
                                norepinephrine: NeurotransmitterScore) -> Tuple[str, List[str]]:
    """Determine overall personality type based on neurotransmitter profile."""

    traits = []

    # Dopamine-driven traits
    if dopamine.baseline_level in [Level.HIGH, Level.VERY_HIGH]:
        if dopamine.clearance_speed == "slow":
            traits.append("Analytisk och detaljorienterad")
            traits.append("Kan tendera till överanalys och oro")
        traits.append("Kreativ problemlösare")
    elif dopamine.baseline_level in [Level.LOW, Level.VERY_LOW]:
        traits.append("Söker stimulans och nya upplevelser")
        traits.append("Risk-tolerant")

    if dopamine.sensitivity == Level.LOW:
        traits.append("Behöver starkare belöningar för motivation")

    # Serotonin-driven traits
    if serotonin.baseline_level in [Level.HIGH, Level.VERY_HIGH]:
        traits.append("Generellt positivt sinnelag")
        traits.append("God impulsivitetskontroll")
    elif serotonin.baseline_level in [Level.LOW, Level.VERY_LOW]:
        traits.append("Kan vara känslig för negativa upplevelser")

    if serotonin.sensitivity == Level.HIGH:
        traits.append("Djupt empatisk och känslig för andras känslor")

    # GABA-driven traits
    if gaba.baseline_level in [Level.LOW, Level.VERY_LOW]:
        traits.append("Kan uppleva ångest lättare")
        traits.append("Svårare att 'stänga av' hjärnan")
    elif gaba.baseline_level in [Level.HIGH, Level.VERY_HIGH]:
        traits.append("Naturligt lugn under press")

    # Norepinephrine-driven traits
    if norepinephrine.baseline_level in [Level.HIGH, Level.VERY_HIGH]:
        traits.append("Alert och fokuserad")
        traits.append("Kan vara hypervaksam")
    elif norepinephrine.baseline_level in [Level.LOW, Level.VERY_LOW]:
        traits.append("Kan ha svårt med ihållande uppmärksamhet")

    # Determine overall type
    high_da = dopamine.baseline_level in [Level.HIGH, Level.VERY_HIGH]
    slow_comt = dopamine.clearance_speed == "slow"

    if high_da and slow_comt:
        overall_type = "ANALYTIKER / WORRIER"
        traits.insert(0, "Kognitiv fördel i lugna miljöer")
        traits.insert(1, "Känslig för stress och överstimulering")
    elif not high_da and dopamine.sensitivity == Level.LOW:
        overall_type = "SENSATION SEEKER"
        traits.insert(0, "Behöver stimulans och spänning")
        traits.insert(1, "Riskerar understimulering och uttråkning")
    elif dopamine.clearance_speed == "fast":
        overall_type = "WARRIOR / PERFORMER"
        traits.insert(0, "Presterar under press")
        traits.insert(1, "Snabb återhämtning från stress")
    else:
        overall_type = "BALANSERAD"
        traits.insert(0, "Flexibel och anpassningsbar")

    return overall_type, traits


def identify_adhd_risk_factors(genotypes: Dict[str, str],
                                dopamine: NeurotransmitterScore,
                                norepinephrine: NeurotransmitterScore) -> List[str]:
    """Identify genetic factors that may contribute to ADHD-like traits."""

    risk_factors = []

    # COMT Met/Met can contribute to ADHD symptoms through different mechanism
    comt = genotypes.get('rs4680', '').upper()
    if comt in ['AA', 'A/A']:
        risk_factors.append("COMT Met/Met: Hög dopamin i PFC men känsligare för stress → kan likna ADHD vid stress")

    # DRD4 - strongly associated with ADHD
    drd4 = genotypes.get('rs1800955', '').upper()
    if drd4 in ['CC', 'C/C']:
        risk_factors.append("DRD4 -521 CC: Novelty-seeking och impulsivitet")

    # DAT1 variants
    dat1 = genotypes.get('rs27072', '').upper()
    if dat1:
        risk_factors.append(f"DAT1 variant ({dat1}): Påverkar dopamin-clearance i striatum")

    # DBH low activity
    dbh = genotypes.get('rs1611115', '').upper()
    if dbh in ['TT', 'T/T']:
        risk_factors.append("DBH -1021 TT: Låg noradrenalin kan påverka fokus")

    # NET variants
    net = genotypes.get('rs2242446', '').upper()
    if net in ['TT', 'T/T']:
        risk_factors.append("NET T-182T: Direkt ADHD-association")

    # SNAP25
    snap25 = genotypes.get('rs3785143', '').upper()
    if snap25:
        risk_factors.append(f"SNAP25 ({snap25}): Synaptisk vesikelgen kopplad till ADHD")

    # ADRA2A
    adra2a = genotypes.get('rs1800544', '').upper()
    if adra2a in ['GG', 'G/G']:
        risk_factors.append("ADRA2A -1291 GG: Uppmärksamhets-variant")

    if not risk_factors:
        risk_factors.append("Inga starka genetiska ADHD-riskfaktorer identifierade")

    return risk_factors


def generate_optimization_strategies(dopamine: NeurotransmitterScore,
                                     serotonin: NeurotransmitterScore,
                                     gaba: NeurotransmitterScore,
                                     norepinephrine: NeurotransmitterScore) -> List[str]:
    """Generate personalized optimization strategies."""

    strategies = []

    # Based on dopamine profile
    if dopamine.baseline_level in [Level.HIGH, Level.VERY_HIGH] and dopamine.clearance_speed == "slow":
        strategies.append("KOST: Undvik för mycket protein på morgonen (kan överstimulera)")
        strategies.append("TRÄNING: Måttlig intensitet, undvik HIIT sent på dagen")
        strategies.append("SÖMN: Extra viktigt med wind-down-rutin (hjärnan har svårt att stänga av)")
        strategies.append("KOFFEIN: Begränsa till max 1-2 koppar, ej efter kl 14")
        strategies.append("TILLSKOTT: Magnesium, B6, och SAMe kan stödja COMT")
    elif dopamine.baseline_level in [Level.LOW, Level.VERY_LOW] or dopamine.sensitivity == Level.LOW:
        strategies.append("KOST: Proteinrik frukost med tyrosin (ägg, kött, fisk)")
        strategies.append("TRÄNING: Intensiv träning kan höja dopamin naturligt")
        strategies.append("RUTINER: Sätt upp tydliga mål och belöningssystem")
        strategies.append("TILLSKOTT: L-tyrosin eller Mucuna pruriens kan hjälpa")

    # Based on serotonin profile
    if serotonin.baseline_level in [Level.LOW, Level.VERY_LOW]:
        strategies.append("LJUS: 30 min dagsljus/morgonljus dagligen")
        strategies.append("KOST: Kolhydrater hjälper tryptofan nå hjärnan")
        strategies.append("MOTION: Regelbunden aerob träning ökar serotonin")
        strategies.append("TILLSKOTT: 5-HTP eller tryptofan (rådgör med läkare)")

    # Based on GABA profile
    if gaba.baseline_level == Level.LOW or gaba.sensitivity == Level.HIGH:
        strategies.append("ANDNING: Djupandning och 4-7-8-andning dagligen")
        strategies.append("YOGA: Visat öka GABA-nivåer med 27%")
        strategies.append("KOST: Fermenterade livsmedel (kimchi, kefir) stödjer GABA")
        strategies.append("TILLSKOTT: L-theanin, taurin, eller GABA")

    # Based on norepinephrine profile
    if norepinephrine.baseline_level == Level.LOW:
        strategies.append("FOKUS: Kalla duschar/bad kan höja noradrenalin akut")
        strategies.append("STRESS: Kontrollerad stressexponering (Wim Hof-metoden)")
    elif norepinephrine.baseline_level == Level.HIGH:
        strategies.append("ÅTERHÄMTNING: Prioritera parasympatisk aktivering")
        strategies.append("UNDVIK: För mycket koffein och stimulantia")

    if not strategies:
        strategies.append("Ditt neurotransmittorprofil är relativt balanserad")
        strategies.append("Fokusera på grundläggande hälsorutiner: sömn, kost, motion")

    return strategies


def generate_neurotransmitter_profile(genotypes: Dict[str, str]) -> NeurotransmitterProfile:
    """Generate complete neurotransmitter profile from genotypes."""

    # Analyze each system
    dopamine = analyze_dopamine(genotypes)
    serotonin = analyze_serotonin(genotypes)
    gaba = analyze_gaba(genotypes)
    norepinephrine = analyze_norepinephrine(genotypes)

    # Determine overall type and traits
    overall_type, traits = determine_personality_type(dopamine, serotonin, gaba, norepinephrine)

    # Identify ADHD risk factors
    adhd_factors = identify_adhd_risk_factors(genotypes, dopamine, norepinephrine)

    # Generate optimization strategies
    strategies = generate_optimization_strategies(dopamine, serotonin, gaba, norepinephrine)

    return NeurotransmitterProfile(
        dopamine=dopamine,
        serotonin=serotonin,
        gaba=gaba,
        norepinephrine=norepinephrine,
        overall_type=overall_type,
        personality_traits=traits,
        adhd_risk_factors=adhd_factors,
        optimization_strategies=strategies
    )


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

def level_to_bar(level: Level) -> str:
    """Convert level to visual bar."""
    bars = {
        Level.VERY_LOW: "[#----]",
        Level.LOW: "[##---]",
        Level.NORMAL: "[###--]",
        Level.HIGH: "[####-]",
        Level.VERY_HIGH: "[#####]"
    }
    return bars.get(level, "[???]")


def level_to_swedish(level: Level) -> str:
    """Convert level to Swedish text."""
    names = {
        Level.VERY_LOW: "Mycket låg",
        Level.LOW: "Låg",
        Level.NORMAL: "Normal",
        Level.HIGH: "Hög",
        Level.VERY_HIGH: "Mycket hög"
    }
    return names.get(level, "Okänd")


def format_neurotransmitter_report(profile: NeurotransmitterProfile) -> str:
    """Format the profile as a readable report."""

    lines = []
    lines.append("=" * 70)
    lines.append("NEUROTRANSMITTOR-PROFIL")
    lines.append("=" * 70)
    lines.append("")

    # Overall type
    lines.append(f"ÖVERGRIPANDE TYP: {profile.overall_type}")
    lines.append("")

    # Personality traits
    lines.append("PERSONLIGHETSDRAG:")
    for trait in profile.personality_traits[:6]:
        lines.append(f"  - {trait}")
    lines.append("")

    # Individual neurotransmitters
    for nt in [profile.dopamine, profile.serotonin, profile.gaba, profile.norepinephrine]:
        lines.append("-" * 70)
        lines.append(f"{nt.name.upper()}")
        lines.append("-" * 70)
        lines.append(f"  Baseline:    {level_to_bar(nt.baseline_level)} {level_to_swedish(nt.baseline_level)}")
        lines.append(f"  Känslighet:  {level_to_bar(nt.sensitivity)} {level_to_swedish(nt.sensitivity)}")
        lines.append(f"  Clearance:   {nt.clearance_speed}")
        lines.append("")

        if nt.contributing_genes:
            lines.append("  GENER:")
            for gene, genotype, effect in nt.contributing_genes:
                lines.append(f"    {gene} ({genotype}): {effect}")
            lines.append("")

        if nt.key_findings:
            lines.append("  FYND:")
            for finding in nt.key_findings[:4]:
                lines.append(f"    - {finding}")
            lines.append("")

    # ADHD risk factors
    lines.append("-" * 70)
    lines.append("ADHD-RELATERADE FAKTORER")
    lines.append("-" * 70)
    for factor in profile.adhd_risk_factors:
        lines.append(f"  - {factor}")
    lines.append("")

    # Optimization strategies
    lines.append("-" * 70)
    lines.append("OPTIMERINGSSTRATEGIER")
    lines.append("-" * 70)
    for strategy in profile.optimization_strategies:
        lines.append(f"  - {strategy}")
    lines.append("")

    lines.append("=" * 70)

    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from gwl_snp_fetcher import load_genome_snps

    if len(sys.argv) < 2:
        print("Usage: python gwl_neurotransmitter_profile.py <genome_file>")
        sys.exit(1)

    genome_file = sys.argv[1]
    print(f"Loading genome from {genome_file}...")
    genotypes = load_genome_snps(genome_file)

    print("Generating neurotransmitter profile...")
    profile = generate_neurotransmitter_profile(genotypes)

    report = format_neurotransmitter_report(profile)
    print(report)
