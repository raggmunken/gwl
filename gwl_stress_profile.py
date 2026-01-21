#!/usr/bin/env python3
"""
GWL Stress Profile Generator
=============================
Analyzes HPA-axis and stress response genetics.

Explains WHY someone handles stress the way they do:
- Acute stress response (fight/flight)
- Cortisol sensitivity
- Recovery and resilience
- Trauma vulnerability

Key systems:
- HPA-axis: CRHR1, FKBP5, NR3C1
- Catecholamines: COMT, DBH, MAOA
- Protective factors: NPY, BDNF

Genetic Wellness Labs - Nutrigenomics Platform
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum


class StressLevel(Enum):
    VERY_RESILIENT = 1
    RESILIENT = 2
    NORMAL = 3
    SENSITIVE = 4
    VERY_SENSITIVE = 5


@dataclass
class StressProfile:
    """Complete stress response profile."""
    overall_type: str
    acute_stress_handling: StressLevel
    cortisol_sensitivity: StressLevel
    recovery_speed: str
    trauma_vulnerability: StressLevel

    hpa_axis_findings: List[str]
    catecholamine_findings: List[str]
    protective_factors: List[str]
    risk_factors: List[str]

    coping_recommendations: List[str]
    lifestyle_recommendations: List[str]
    supplement_recommendations: List[str]

    contributing_genes: List[Tuple[str, str, str]]


def analyze_stress_profile(genotypes: Dict[str, str]) -> StressProfile:
    """
    Analyze stress response genetics.

    Key genes analyzed:
    - COMT (rs4680): Catecholamine clearance
    - FKBP5 (rs1360780, rs3800373): Cortisol sensitivity
    - CRHR1 (rs110402): CRH receptor
    - NR3C1 (rs6190, rs41423247): Glucocorticoid receptor
    - NR3C2: Mineralocorticoid receptor
    - NPY (rs16147): Stress resilience
    - BDNF (rs6265): Neuroplasticity
    - MAOA (rs6323): Monoamine oxidase A
    """

    hpa_findings = []
    catecholamine_findings = []
    protective = []
    risks = []
    genes = []

    acute_score = 0  # -2 to +2, positive = better handling
    cortisol_score = 0  # positive = more sensitive
    recovery_score = 0  # positive = faster
    trauma_score = 0  # positive = more vulnerable

    # =========================================================================
    # COMT - Critical for acute stress response
    # =========================================================================
    comt = genotypes.get('rs4680', '').upper()
    if comt:
        if comt in ['AA', 'A/A']:  # Met/Met - slow COMT
            acute_score -= 1
            recovery_score -= 1
            catecholamine_findings.append("COMT Met/Met: Långsam stresshormon-nedbrytning")
            catecholamine_findings.append("'Worrier'-typ: Bättre kognition i lugn, sämre under akut stress")
            catecholamine_findings.append("Högre dopamin/noradrenalin-nivåer vid stress")
            risks.append("Längre återhämtningstid efter stress")
            genes.append(("COMT", comt, "Långsam katekol-nedbrytning"))
        elif comt in ['GG', 'G/G']:  # Val/Val - fast COMT
            acute_score += 1
            recovery_score += 1
            catecholamine_findings.append("COMT Val/Val: Snabb stresshormon-nedbrytning")
            catecholamine_findings.append("'Warrior'-typ: Presterar bra under press")
            protective.append("Snabb återhämtning efter akut stress")
            genes.append(("COMT", comt, "Snabb katekol-nedbrytning"))
        else:  # Heterozygot
            catecholamine_findings.append("COMT Val/Met: Balanserad stressrespons")
            genes.append(("COMT", comt, "Balanserad"))

    # =========================================================================
    # FKBP5 - Cortisol sensitivity regulator (CRITICAL for trauma)
    # =========================================================================
    fkbp5_main = genotypes.get('rs1360780', '').upper()
    if fkbp5_main:
        if fkbp5_main in ['TT', 'T/T']:
            cortisol_score += 2
            trauma_score += 2
            hpa_findings.append("FKBP5 rs1360780 T/T: Starkt ökad kortisolkänslighet")
            hpa_findings.append("HPA-axeln har svårare att stänga av efter stress")
            risks.append("Ökad PTSD-risk efter traumatiska händelser")
            risks.append("Förlängd kortisolrespons")
            genes.append(("FKBP5", fkbp5_main, "Hög kortisolkänslighet"))
        elif fkbp5_main in ['CT', 'TC', 'C/T', 'T/C']:
            cortisol_score += 1
            trauma_score += 1
            hpa_findings.append("FKBP5 rs1360780 C/T: Något ökad kortisolkänslighet")
            genes.append(("FKBP5", fkbp5_main, "Måttligt ökad kortisolkänslighet"))
        else:  # CC
            hpa_findings.append("FKBP5 rs1360780 C/C: Normal kortisolreglering")
            protective.append("Normal HPA-axel-feedback")
            genes.append(("FKBP5", fkbp5_main, "Normal"))

    fkbp5_2 = genotypes.get('rs3800373', '').upper()
    if fkbp5_2:
        genes.append(("FKBP5", fkbp5_2, "HPA-axel feedback variant"))

    fkbp5_3 = genotypes.get('rs9470080', '').upper()
    if fkbp5_3:
        if fkbp5_3 in ['TT', 'T/T']:
            trauma_score += 1
            risks.append("FKBP5 rs9470080 T/T: Ytterligare ökad ångest/depression-risk")
            genes.append(("FKBP5", fkbp5_3, "Ångest/depression-risk"))

    # =========================================================================
    # CRHR1 - CRH receptor (initiates stress response)
    # =========================================================================
    crhr1 = genotypes.get('rs110402', '').upper()
    if crhr1:
        if crhr1 in ['GG', 'G/G']:
            hpa_findings.append("CRHR1 rs110402 G/G: Skyddande variant mot depression")
            protective.append("CRHR1 G/G: Minskad risk för stressrelaterad depression")
            trauma_score -= 1
            genes.append(("CRHR1", crhr1, "Skyddande"))
        elif crhr1 in ['AA', 'A/A']:
            hpa_findings.append("CRHR1 rs110402 A/A: Kan ha starkare stressrespons")
            genes.append(("CRHR1", crhr1, "Starkare stressrespons"))

    crhr1_2 = genotypes.get('rs242924', '').upper()
    if crhr1_2:
        genes.append(("CRHR1", crhr1_2, "Kortisolreaktivitet"))

    # =========================================================================
    # NR3C1 - Glucocorticoid receptor
    # =========================================================================
    nr3c1_bcli = genotypes.get('rs41423247', '').upper()
    if nr3c1_bcli:
        if nr3c1_bcli in ['GG', 'G/G']:
            cortisol_score += 1
            hpa_findings.append("NR3C1 BclI G/G: Ökad kortisolkänslighet")
            hpa_findings.append("Kan leda till mer bukfett och metabola effekter av stress")
            genes.append(("NR3C1", nr3c1_bcli, "Ökad GR-känslighet"))
        else:
            genes.append(("NR3C1", nr3c1_bcli, "Normal GR-känslighet"))

    nr3c1_er = genotypes.get('rs6190', '').upper()
    if nr3c1_er:
        genes.append(("NR3C1", nr3c1_er, "ER22/23EK variant"))

    nr3c1_beta = genotypes.get('rs6198', '').upper()
    if nr3c1_beta:
        if nr3c1_beta in ['GG', 'G/G']:
            hpa_findings.append("NR3C1 9beta G/G: Ökad GR-beta = kortisolresistens")
            hpa_findings.append("Kan leda till kronisk inflammation")
            risks.append("Ökad inflammationsbenägenhet vid kronisk stress")
            genes.append(("NR3C1", nr3c1_beta, "Kortisolresistens/inflammation"))

    # =========================================================================
    # NPY - Neuropeptide Y (stress resilience factor)
    # =========================================================================
    npy = genotypes.get('rs16147', '').upper()
    if npy:
        if npy in ['TT', 'T/T']:
            acute_score += 1
            trauma_score -= 1
            hpa_findings.append("NPY rs16147 T/T: Högt NPY-uttryck")
            protective.append("Högt NPY: Naturligt stressskydd, 'stressresiliens-genen'")
            protective.append("Används av specialstyrkor - skyddar mot PTSD")
            genes.append(("NPY", npy, "Hög stressresiliens"))
        elif npy in ['CC', 'C/C']:
            trauma_score += 1
            hpa_findings.append("NPY rs16147 C/C: Lägre NPY-uttryck")
            risks.append("Lägre naturligt stressskydd")
            genes.append(("NPY", npy, "Lägre stressresiliens"))
        else:
            genes.append(("NPY", npy, "Intermediär"))

    # =========================================================================
    # BDNF - Brain-derived neurotrophic factor
    # =========================================================================
    bdnf = genotypes.get('rs6265', '').upper()
    if bdnf:
        if bdnf in ['CT', 'TC', 'C/T', 'T/C', 'AG', 'GA', 'A/G', 'G/A']:
            recovery_score -= 1
            trauma_score += 1
            hpa_findings.append("BDNF Val66Met (hetero): Något reducerad neuroplasticitet")
            risks.append("Långsammare återhämtning från stress/trauma")
            genes.append(("BDNF", bdnf, "Reducerad neuroplasticitet"))
        elif bdnf in ['TT', 'T/T', 'AA', 'A/A']:
            recovery_score -= 1
            trauma_score += 1
            hpa_findings.append("BDNF Met/Met: Reducerad BDNF-frisättning vid aktivitet")
            risks.append("Minskad förmåga att 'omprogrammera' stressrespons")
            genes.append(("BDNF", bdnf, "Låg BDNF"))
        else:  # Val/Val (CC or GG depending on notation)
            protective.append("BDNF Val/Val: Normal neuroplasticitet")
            genes.append(("BDNF", bdnf, "Normal neuroplasticitet"))

    # =========================================================================
    # MAOA - Monoamine oxidase A
    # =========================================================================
    maoa = genotypes.get('rs6323', '').upper()
    if maoa:
        if maoa in ['TT', 'T/T']:
            catecholamine_findings.append("MAOA T/T: Hög MAO-A aktivitet")
            catecholamine_findings.append("Snabb nedbrytning av serotonin/dopamin/NE")
            genes.append(("MAOA", maoa, "Hög aktivitet"))
        elif maoa in ['GG', 'G/G']:
            catecholamine_findings.append("MAOA G/G: Låg MAO-A aktivitet")
            catecholamine_findings.append("Längre kvarvarande av monoaminer")
            risks.append("Kan vara mer reaktiv på provokation")
            genes.append(("MAOA", maoa, "Låg aktivitet - 'warrior gene'"))

    # =========================================================================
    # Determine overall type
    # =========================================================================

    # Calculate levels
    if acute_score >= 2:
        acute_handling = StressLevel.VERY_RESILIENT
    elif acute_score >= 1:
        acute_handling = StressLevel.RESILIENT
    elif acute_score <= -2:
        acute_handling = StressLevel.VERY_SENSITIVE
    elif acute_score <= -1:
        acute_handling = StressLevel.SENSITIVE
    else:
        acute_handling = StressLevel.NORMAL

    if cortisol_score >= 2:
        cortisol_sens = StressLevel.VERY_SENSITIVE
    elif cortisol_score >= 1:
        cortisol_sens = StressLevel.SENSITIVE
    elif cortisol_score <= -1:
        cortisol_sens = StressLevel.RESILIENT
    else:
        cortisol_sens = StressLevel.NORMAL

    if recovery_score >= 1:
        recovery = "Snabb"
    elif recovery_score <= -1:
        recovery = "Långsam"
    else:
        recovery = "Normal"

    if trauma_score >= 2:
        trauma_vuln = StressLevel.VERY_SENSITIVE
    elif trauma_score >= 1:
        trauma_vuln = StressLevel.SENSITIVE
    elif trauma_score <= -1:
        trauma_vuln = StressLevel.RESILIENT
    else:
        trauma_vuln = StressLevel.NORMAL

    # Determine overall type
    if acute_handling in [StressLevel.RESILIENT, StressLevel.VERY_RESILIENT] and \
       cortisol_sens in [StressLevel.NORMAL, StressLevel.RESILIENT]:
        overall_type = "STRESS-RESILIENT (Warrior)"
    elif cortisol_sens in [StressLevel.SENSITIVE, StressLevel.VERY_SENSITIVE] and \
         trauma_vuln in [StressLevel.SENSITIVE, StressLevel.VERY_SENSITIVE]:
        overall_type = "STRESS-SENSITIV (Needs Protection)"
    elif acute_handling == StressLevel.SENSITIVE and recovery == "Långsam":
        overall_type = "SLOW PROCESSOR (Worrier)"
    else:
        overall_type = "BALANSERAD"

    # =========================================================================
    # Generate recommendations
    # =========================================================================

    coping = []
    lifestyle = []
    supplements = []

    # Based on acute stress handling
    if acute_handling in [StressLevel.SENSITIVE, StressLevel.VERY_SENSITIVE]:
        coping.append("Förbered dig mentalt inför stressiga situationer")
        coping.append("Använd 'box breathing' (4-4-4-4) vid akut stress")
        coping.append("Bygg in pauser mellan stressiga aktiviteter")

    # Based on cortisol sensitivity
    if cortisol_sens in [StressLevel.SENSITIVE, StressLevel.VERY_SENSITIVE]:
        lifestyle.append("PRIORITERA SÖMN: 7-9 timmar, kortisol regleras under sömn")
        lifestyle.append("MORGONRUTIN: Undvik stress första timmen efter uppvaknande")
        lifestyle.append("TRÄNING: Måttlig intensitet, undvik överträning")
        lifestyle.append("KOST: Balanserat blodsocker minskar kortisolspikar")
        supplements.append("Ashwagandha (KSM-66): Sänker kortisol, stödjer HPA-axeln")
        supplements.append("Fosfatidylserin: Kan dämpa kortisolrespons")
        supplements.append("Magnesium: Kritiskt för stresshantering")

    # Based on recovery speed
    if recovery == "Långsam":
        coping.append("Schemalägg återhämtning efter stressiga perioder")
        coping.append("Begränsa antal stressorer per dag")
        lifestyle.append("ÅTERHÄMTNING: Mer tid mellan intensiva aktiviteter")
        lifestyle.append("NATUR: Tid i naturen snabbar på återhämtning")

    # Based on trauma vulnerability
    if trauma_vuln in [StressLevel.SENSITIVE, StressLevel.VERY_SENSITIVE]:
        coping.append("Bygg starkt socialt stöd - skyddsfaktor nr 1")
        coping.append("Överväg profylaktisk terapi vid stora livsförändringar")
        coping.append("Undvik att 'härda ut' - sök hjälp tidigt vid trauma")
        lifestyle.append("MINDFULNESS: Regelbunden meditation stärker stresstolerans")
        supplements.append("Omega-3 (EPA/DHA): Stödjer BDNF och neuroplasticitet")

    # COMT-specific
    if comt in ['AA', 'A/A']:
        supplements.append("SAMe eller metylerade B-vitaminer: Stödjer COMT-funktion")
        lifestyle.append("KOFFEIN: Max 1-2 koppar, ej efter kl 14")

    # General
    if not coping:
        coping.append("Du har generellt god stresshanteringsförmåga")
        coping.append("Fokusera på att bibehålla goda vanor")

    if not lifestyle:
        lifestyle.append("Regelbunden motion")
        lifestyle.append("God sömnhygien")
        lifestyle.append("Sociala kontakter")

    if not supplements:
        supplements.append("Magnesium: Grundläggande för stresshantering")
        supplements.append("B-vitaminkomplex: Stödjer nervsystemet")

    return StressProfile(
        overall_type=overall_type,
        acute_stress_handling=acute_handling,
        cortisol_sensitivity=cortisol_sens,
        recovery_speed=recovery,
        trauma_vulnerability=trauma_vuln,
        hpa_axis_findings=hpa_findings,
        catecholamine_findings=catecholamine_findings,
        protective_factors=protective,
        risk_factors=risks,
        coping_recommendations=coping,
        lifestyle_recommendations=lifestyle,
        supplement_recommendations=supplements,
        contributing_genes=genes
    )


def stress_level_to_bar(level: StressLevel) -> str:
    """Convert stress level to visual bar."""
    bars = {
        StressLevel.VERY_RESILIENT: "[#####] Mycket resilient",
        StressLevel.RESILIENT: "[####-] Resilient",
        StressLevel.NORMAL: "[###--] Normal",
        StressLevel.SENSITIVE: "[##---] Känslig",
        StressLevel.VERY_SENSITIVE: "[#----] Mycket känslig"
    }
    return bars.get(level, "[???]")


def format_stress_report(profile: StressProfile) -> str:
    """Format the stress profile as a readable report."""

    lines = []
    lines.append("=" * 70)
    lines.append("STRESSPROFIL")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"ÖVERGRIPANDE TYP: {profile.overall_type}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("STRESSRESPONS-ÖVERSIKT")
    lines.append("-" * 70)
    lines.append(f"  Akut stresshantering:  {stress_level_to_bar(profile.acute_stress_handling)}")
    lines.append(f"  Kortisolkänslighet:    {stress_level_to_bar(profile.cortisol_sensitivity)}")
    lines.append(f"  Återhämtningshastighet: {profile.recovery_speed}")
    lines.append(f"  Trauma-sårbarhet:       {stress_level_to_bar(profile.trauma_vulnerability)}")
    lines.append("")

    if profile.contributing_genes:
        lines.append("-" * 70)
        lines.append("GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.contributing_genes:
            lines.append(f"  {gene} ({genotype}): {effect}")
        lines.append("")

    if profile.hpa_axis_findings:
        lines.append("-" * 70)
        lines.append("HPA-AXEL (Kortisol-systemet)")
        lines.append("-" * 70)
        for finding in profile.hpa_axis_findings:
            lines.append(f"  - {finding}")
        lines.append("")

    if profile.catecholamine_findings:
        lines.append("-" * 70)
        lines.append("KATEKOLAMINER (Dopamin/Noradrenalin/Adrenalin)")
        lines.append("-" * 70)
        for finding in profile.catecholamine_findings:
            lines.append(f"  - {finding}")
        lines.append("")

    if profile.protective_factors:
        lines.append("-" * 70)
        lines.append("SKYDDSFAKTORER")
        lines.append("-" * 70)
        for factor in profile.protective_factors:
            lines.append(f"  + {factor}")
        lines.append("")

    if profile.risk_factors:
        lines.append("-" * 70)
        lines.append("RISKFAKTORER")
        lines.append("-" * 70)
        for factor in profile.risk_factors:
            lines.append(f"  ! {factor}")
        lines.append("")

    lines.append("-" * 70)
    lines.append("REKOMMENDATIONER: COPING-STRATEGIER")
    lines.append("-" * 70)
    for rec in profile.coping_recommendations:
        lines.append(f"  - {rec}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("REKOMMENDATIONER: LIVSSTIL")
    lines.append("-" * 70)
    for rec in profile.lifestyle_recommendations:
        lines.append(f"  - {rec}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("REKOMMENDATIONER: KOSTTILLSKOTT")
    lines.append("-" * 70)
    for rec in profile.supplement_recommendations:
        lines.append(f"  - {rec}")
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
        print("Usage: python gwl_stress_profile.py <genome_file>")
        sys.exit(1)

    genome_file = sys.argv[1]
    print(f"Loading genome from {genome_file}...")
    genotypes = load_genome_snps(genome_file)

    print("Generating stress profile...")
    profile = analyze_stress_profile(genotypes)

    report = format_stress_report(profile)
    print(report)
