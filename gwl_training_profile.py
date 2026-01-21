#!/usr/bin/env python3
"""
GWL Training Profile Generator
===============================
Analyzes genetic variants to recommend optimal training strategies.

Explains:
- Power vs Endurance genetic predisposition
- VO2max trainability
- Muscle fiber composition tendency
- Injury risk and recovery
- Optimal training frequency and intensity

Key genes:
- ACTN3: Power/sprint vs endurance
- ACE: Endurance capacity
- PPARGC1A: Mitochondrial biogenesis
- COL5A1, COL1A1: Tendon/ligament strength
- IL6, TNF: Recovery and inflammation

Genetic Wellness Labs - Nutrigenomics Platform
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum


class FiberType(Enum):
    POWER = "power"
    MIXED = "mixed"
    ENDURANCE = "endurance"


class TrainabilityLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class InjuryRisk(Enum):
    LOW = "low"
    MODERATE = "moderate"
    ELEVATED = "elevated"
    HIGH = "high"


@dataclass
class TrainingProfile:
    """Complete training genetics profile."""
    overall_type: str
    muscle_fiber_tendency: FiberType
    power_potential: TrainabilityLevel
    endurance_potential: TrainabilityLevel
    vo2max_trainability: TrainabilityLevel
    muscle_growth_potential: TrainabilityLevel

    tendon_injury_risk: InjuryRisk
    recovery_speed: str

    ideal_sports: List[str]
    training_recommendations: List[str]
    injury_prevention: List[str]
    recovery_strategies: List[str]

    power_genes: List[Tuple[str, str, str]]
    endurance_genes: List[Tuple[str, str, str]]
    injury_genes: List[Tuple[str, str, str]]
    recovery_genes: List[Tuple[str, str, str]]


def analyze_training_profile(genotypes: Dict[str, str]) -> TrainingProfile:
    """
    Analyze training-related genetics.

    Key genes:
    - ACTN3 (rs1815739): Alpha-actinin-3 - power gene
    - ACE (rs4646994, rs1799752): Endurance gene
    - PPARGC1A (rs8192678): PGC-1alpha - mitochondria
    - PPARA (rs4253778): Fat metabolism in exercise
    - ADRB2 (rs1042713): Beta-2 receptor
    - COL5A1 (rs12722): Tendon injury risk
    - COL1A1 (rs1800012): Collagen strength
    - IL6 (rs1800795): Recovery/inflammation
    - TNF (rs1800629): Inflammation
    - MSTN (rs1805086): Myostatin - muscle growth
    - VEGFA (rs2010963): Vascular adaptation
    - HIF1A (rs11549465): Altitude/endurance
    """

    power_genes = []
    endurance_genes = []
    injury_genes = []
    recovery_genes = []

    power_score = 0  # Higher = more power
    endurance_score = 0  # Higher = more endurance
    vo2max_score = 0
    muscle_score = 0
    injury_risk_score = 0
    recovery_score = 0  # Higher = faster recovery

    # =========================================================================
    # ACTN3 - The "Speed Gene" (rs1815739)
    # =========================================================================
    actn3 = genotypes.get('rs1815739', '').upper()
    if actn3:
        if actn3 in ['CC', 'C/C']:  # R/R - functional alpha-actinin-3
            power_score += 2
            power_genes.append(("ACTN3", actn3, "R/R - Fullt funktionellt alfa-actinin-3"))
            power_genes.append(("", "", "Optimal för explosiv kraft och sprint"))
        elif actn3 in ['TT', 'T/T']:  # X/X - no alpha-actinin-3
            endurance_score += 2
            endurance_genes.append(("ACTN3", actn3, "X/X - Saknar alfa-actinin-3"))
            endurance_genes.append(("", "", "Fördel för uthållighet, effektivare energi"))
        else:  # CT - heterozygot
            power_score += 1
            endurance_score += 1
            power_genes.append(("ACTN3", actn3, "R/X - Blandad profil"))

    # =========================================================================
    # ACE - Angiotensin Converting Enzyme (rs4646994/rs1799752)
    # =========================================================================
    ace = genotypes.get('rs4646994', '') or genotypes.get('rs1799752', '')
    ace = ace.upper()
    if ace:
        # II genotype = endurance, DD = power, ID = mixed
        if 'II' in ace or ace in ['II', 'I/I']:
            endurance_score += 2
            vo2max_score += 2
            endurance_genes.append(("ACE", ace, "I/I - Uthållighets-genotyp"))
            endurance_genes.append(("", "", "Bättre VO2max-respons på träning"))
        elif 'DD' in ace or ace in ['DD', 'D/D']:
            power_score += 1
            muscle_score += 1
            power_genes.append(("ACE", ace, "D/D - Kraft/muskeltillväxt-genotyp"))
        else:
            endurance_genes.append(("ACE", ace, "I/D - Blandad profil"))

    # Also check rs4343 as a tag SNP
    ace_tag = genotypes.get('rs4343', '').upper()
    if ace_tag:
        if ace_tag in ['AA', 'A/A']:
            endurance_score += 1
            endurance_genes.append(("ACE", ace_tag, "A/A - Uthållighetstendenser"))
        elif ace_tag in ['GG', 'G/G']:
            power_score += 1
            power_genes.append(("ACE", ace_tag, "G/G - Krafttendenser"))

    # =========================================================================
    # PPARGC1A - PGC-1alpha (rs8192678)
    # =========================================================================
    ppargc1a = genotypes.get('rs8192678', '').upper()
    if ppargc1a:
        if ppargc1a in ['GG', 'G/G']:  # Gly/Gly
            endurance_score += 1
            vo2max_score += 1
            endurance_genes.append(("PPARGC1A", ppargc1a, "Gly/Gly - Bättre mitokondriefunktion"))
        elif ppargc1a in ['AA', 'A/A']:  # Ser/Ser
            endurance_genes.append(("PPARGC1A", ppargc1a, "Ser/Ser - Något reducerad mitokondrie-biogenes"))
        else:
            endurance_genes.append(("PPARGC1A", ppargc1a, "Gly/Ser - Normal mitokondriefunktion"))

    # =========================================================================
    # PPARA (rs4253778)
    # =========================================================================
    ppara = genotypes.get('rs4253778', '').upper()
    if ppara:
        if ppara in ['CC', 'C/C']:
            endurance_score += 1
            endurance_genes.append(("PPARA", ppara, "C/C - Bättre fettoxidation"))
        else:
            endurance_genes.append(("PPARA", ppara, "G-bärare - Normal fettmetabolism"))

    # =========================================================================
    # ADRB2 - Beta-2 adrenergic receptor (rs1042713)
    # =========================================================================
    adrb2 = genotypes.get('rs1042713', '').upper()
    if adrb2:
        if adrb2 in ['GG', 'G/G']:  # Arg/Arg
            endurance_genes.append(("ADRB2", adrb2, "Arg/Arg - Bättre bronkdilation vid träning"))
        elif adrb2 in ['AA', 'A/A']:  # Gly/Gly
            endurance_genes.append(("ADRB2", adrb2, "Gly/Gly - Ökad lipolys"))

    # =========================================================================
    # VEGFA - Vascular adaptation (rs2010963)
    # =========================================================================
    vegfa = genotypes.get('rs2010963', '').upper()
    if vegfa:
        if vegfa in ['GG', 'G/G']:
            vo2max_score += 1
            endurance_genes.append(("VEGFA", vegfa, "G/G - Bättre kärlnybildning"))
        else:
            endurance_genes.append(("VEGFA", vegfa, "C-bärare - Normal kärlnybildning"))

    # =========================================================================
    # HIF1A - Hypoxia adaptation (rs11549465)
    # =========================================================================
    hif1a = genotypes.get('rs11549465', '').upper()
    if hif1a:
        if hif1a in ['CT', 'TC', 'C/T', 'T/C', 'TT', 'T/T']:
            endurance_score += 1
            endurance_genes.append(("HIF1A", hif1a, "Pro582Ser - Bättre syreuttag"))
            endurance_genes.append(("", "", "Fördel vid höghöjdsträning"))

    # =========================================================================
    # MSTN - Myostatin (rs1805086)
    # =========================================================================
    mstn = genotypes.get('rs1805086', '').upper()
    if mstn:
        if mstn in ['TT', 'T/T', 'AA', 'A/A']:
            muscle_score += 1
            power_genes.append(("MSTN", mstn, "Lägre myostatin = bättre muskeltillväxt"))

    # =========================================================================
    # INJURY RISK GENES
    # =========================================================================

    # COL5A1 (rs12722)
    col5a1 = genotypes.get('rs12722', '').upper()
    if col5a1:
        if col5a1 in ['TT', 'T/T']:
            injury_risk_score += 2
            injury_genes.append(("COL5A1", col5a1, "T/T - Ökad risk för senor-skador"))
            injury_genes.append(("", "", "Extra viktigt med uppvärmning och gradvis progression"))
        elif col5a1 in ['CC', 'C/C']:
            injury_genes.append(("COL5A1", col5a1, "C/C - Skyddande för senor"))
        else:
            injury_risk_score += 1
            injury_genes.append(("COL5A1", col5a1, "C/T - Något ökad senskaderisk"))

    # COL1A1 (rs1800012)
    col1a1 = genotypes.get('rs1800012', '').upper()
    if col1a1:
        if col1a1 in ['TT', 'T/T']:
            injury_genes.append(("COL1A1", col1a1, "T/T - Starkare kollagen"))
        elif col1a1 in ['GG', 'G/G']:
            injury_risk_score += 1
            injury_genes.append(("COL1A1", col1a1, "G/G - Något svagare kollagen"))

    # GDF5 (rs143383) - Osteoarthritis
    gdf5 = genotypes.get('rs143383', '').upper()
    if gdf5:
        if gdf5 in ['TT', 'T/T']:
            injury_risk_score += 1
            injury_genes.append(("GDF5", gdf5, "T/T - Ökad artrosrisk"))
            injury_genes.append(("", "", "Var försiktig med hög belastning på leder"))
        else:
            injury_genes.append(("GDF5", gdf5, "C-bärare - Lägre artrosrisk"))

    # MMP3 (rs679620)
    mmp3 = genotypes.get('rs679620', '').upper()
    if mmp3:
        if mmp3 in ['TT', 'T/T']:
            injury_risk_score += 1
            injury_genes.append(("MMP3", mmp3, "T/T - Ökad bindväv-nedbrytning"))

    # =========================================================================
    # RECOVERY GENES
    # =========================================================================

    # IL6 (rs1800795)
    il6 = genotypes.get('rs1800795', '').upper()
    if il6:
        if il6 in ['CC', 'C/C']:
            recovery_score += 1
            recovery_genes.append(("IL6", il6, "C/C - Lägre inflammation = snabbare återhämtning"))
        elif il6 in ['GG', 'G/G']:
            recovery_score -= 1
            recovery_genes.append(("IL6", il6, "G/G - Högre inflammation efter träning"))
            recovery_genes.append(("", "", "Kan behöva längre återhämtning"))

    # TNF (rs1800629)
    tnf = genotypes.get('rs1800629', '').upper()
    if tnf:
        if tnf in ['GG', 'G/G']:
            recovery_genes.append(("TNF", tnf, "G/G - Normal inflammationsrespons"))
        elif tnf in ['AA', 'A/A']:
            recovery_score -= 1
            recovery_genes.append(("TNF", tnf, "A/A - Högre TNF-produktion"))
            recovery_genes.append(("", "", "Längre återhämtning kan behövas"))

    # CRP (rs1205)
    crp = genotypes.get('rs1205', '').upper()
    if crp:
        if crp in ['TT', 'T/T']:
            recovery_genes.append(("CRP", crp, "T/T - Lägre CRP = mindre inflammation"))
        elif crp in ['CC', 'C/C']:
            recovery_genes.append(("CRP", crp, "C/C - Högre bas-CRP"))

    # =========================================================================
    # COMT for training intensity
    # =========================================================================
    comt = genotypes.get('rs4680', '').upper()
    if comt:
        if comt in ['AA', 'A/A']:  # Met/Met
            recovery_genes.append(("COMT", comt, "Met/Met - Känsligare för överträning"))
            recovery_genes.append(("", "", "Undvik för hög intensitet, prioritera återhämtning"))
            recovery_score -= 1
        elif comt in ['GG', 'G/G']:  # Val/Val
            recovery_genes.append(("COMT", comt, "Val/Val - Tåligare för hög intensitet"))
            recovery_score += 1

    # =========================================================================
    # Determine profiles
    # =========================================================================

    # Fiber type
    if power_score > endurance_score + 1:
        fiber_type = FiberType.POWER
    elif endurance_score > power_score + 1:
        fiber_type = FiberType.ENDURANCE
    else:
        fiber_type = FiberType.MIXED

    # Power potential
    if power_score >= 3:
        power_potential = TrainabilityLevel.VERY_HIGH
    elif power_score >= 2:
        power_potential = TrainabilityLevel.HIGH
    elif power_score >= 1:
        power_potential = TrainabilityLevel.MODERATE
    else:
        power_potential = TrainabilityLevel.LOW

    # Endurance potential
    if endurance_score >= 4:
        endurance_potential = TrainabilityLevel.VERY_HIGH
    elif endurance_score >= 2:
        endurance_potential = TrainabilityLevel.HIGH
    elif endurance_score >= 1:
        endurance_potential = TrainabilityLevel.MODERATE
    else:
        endurance_potential = TrainabilityLevel.LOW

    # VO2max trainability
    if vo2max_score >= 3:
        vo2max_trainability = TrainabilityLevel.VERY_HIGH
    elif vo2max_score >= 2:
        vo2max_trainability = TrainabilityLevel.HIGH
    elif vo2max_score >= 1:
        vo2max_trainability = TrainabilityLevel.MODERATE
    else:
        vo2max_trainability = TrainabilityLevel.LOW

    # Muscle growth
    if muscle_score >= 2:
        muscle_growth = TrainabilityLevel.VERY_HIGH
    elif muscle_score >= 1:
        muscle_growth = TrainabilityLevel.HIGH
    else:
        muscle_growth = TrainabilityLevel.MODERATE

    # Injury risk
    if injury_risk_score >= 3:
        tendon_risk = InjuryRisk.HIGH
    elif injury_risk_score >= 2:
        tendon_risk = InjuryRisk.ELEVATED
    elif injury_risk_score >= 1:
        tendon_risk = InjuryRisk.MODERATE
    else:
        tendon_risk = InjuryRisk.LOW

    # Recovery
    if recovery_score >= 1:
        recovery_speed = "Snabb"
    elif recovery_score <= -1:
        recovery_speed = "Långsam"
    else:
        recovery_speed = "Normal"

    # Overall type
    if fiber_type == FiberType.POWER:
        overall_type = "EXPLOSIV KRAFTTYP"
    elif fiber_type == FiberType.ENDURANCE:
        overall_type = "UTHÅLLIGHETSTYP"
    else:
        overall_type = "HYBRID/ALLROUNDER"

    # =========================================================================
    # Generate recommendations
    # =========================================================================

    ideal_sports = []
    training_recs = []
    injury_prev = []
    recovery_strats = []

    if fiber_type == FiberType.POWER:
        ideal_sports = [
            "Sprint (100-400m)",
            "Styrkelyft",
            "Olympisk tyngdlyftning",
            "Hopp och kast",
            "Kampsport",
            "Ishockey, fotboll (kortdistans)"
        ]
        training_recs = [
            "FOKUS: Explosiva rörelser och maximal kraft",
            "INTENSITET: Hög intensitet, låg volym",
            "VILA: Längre viloperioder mellan set (2-5 min)",
            "FREKVENS: 3-4 pass/vecka med god återhämtning",
            "UTHÅLLIGHET: Komplettera med måttlig konditionsträning"
        ]
    elif fiber_type == FiberType.ENDURANCE:
        ideal_sports = [
            "Långdistanslöpning",
            "Cykling",
            "Simning (längre distanser)",
            "Triathlon",
            "Längdskidor",
            "Rodd (distans)"
        ]
        training_recs = [
            "FOKUS: Aerob basträning och uthållighet",
            "INTENSITET: Låg-måttlig med inslag av intervaller",
            "VOLYM: Högre volym tolereras väl",
            "FREKVENS: 5-6 pass/vecka möjligt",
            "STYRKA: Komplettera med styrketräning för prestanda"
        ]
    else:
        ideal_sports = [
            "Melllandistanslöpning (800-3000m)",
            "Funktionell fitness/CrossFit",
            "Lagsporter (fotboll, handboll)",
            "Tennis, padel",
            "Simning",
            "Rodd"
        ]
        training_recs = [
            "FOKUS: Blandad träning - styrka + kondition",
            "INTENSITET: Variera mellan hög och låg",
            "VOLYM: Måttlig, undvik ensidighet",
            "FREKVENS: 4-5 pass/vecka",
            "PERIODISERING: Växla fokus mellan kraft och uthållighet"
        ]

    # Injury prevention based on risk
    if tendon_risk in [InjuryRisk.ELEVATED, InjuryRisk.HIGH]:
        injury_prev = [
            "KRITISKT: Längre uppvärmning (15+ min)",
            "Gradvis progression - öka belastning max 10%/vecka",
            "Excentrik träning för senstyrka",
            "Kollagen/C-vitamin före träning kan stödja senor",
            "Undvik snabba riktningsförändringar utan uppvärmning",
            "Stretching EFTER träning, inte före",
            "Vila vid minsta tecken på överbelastning"
        ]
    else:
        injury_prev = [
            "Grundläggande uppvärmning innan intensiv träning",
            "Progressiv överbelastning",
            "Lyssna på kroppen vid smärta"
        ]

    # Recovery strategies
    if recovery_speed == "Långsam":
        recovery_strats = [
            "MINST 48 timmar mellan tunga pass för samma muskelgrupp",
            "Aktiv återhämtning: promenader, lätt cykling",
            "Prioritera sömn: 8-9 timmar",
            "Anti-inflammatorisk kost: omega-3, kurkuma, ingefära",
            "Överväg kall/varm-behandling (kontrastbad)",
            "Begränsa HIIT till 2-3 ggr/vecka",
            "Stresshantering viktigt för återhämtning"
        ]
    elif recovery_speed == "Snabb":
        recovery_strats = [
            "Kan tolerera högre träningsfrekvens",
            "Kortare vila mellan pass möjligt",
            "HIIT 3-4 ggr/vecka möjligt",
            "Glöm inte basåterhämtning: sömn, kost"
        ]
    else:
        recovery_strats = [
            "48 timmar vila mellan tunga pass",
            "God sömn och kost för optimal återhämtning",
            "Lyssna på kroppen"
        ]

    # Add COMT-specific
    if comt in ['AA', 'A/A']:
        training_recs.append("OBS: Undvik överträning - du är känsligare för hög volym")
        recovery_strats.append("Extra viktigt med stresshantering utanför träning")

    return TrainingProfile(
        overall_type=overall_type,
        muscle_fiber_tendency=fiber_type,
        power_potential=power_potential,
        endurance_potential=endurance_potential,
        vo2max_trainability=vo2max_trainability,
        muscle_growth_potential=muscle_growth,
        tendon_injury_risk=tendon_risk,
        recovery_speed=recovery_speed,
        ideal_sports=ideal_sports,
        training_recommendations=training_recs,
        injury_prevention=injury_prev,
        recovery_strategies=recovery_strats,
        power_genes=power_genes,
        endurance_genes=endurance_genes,
        injury_genes=injury_genes,
        recovery_genes=recovery_genes
    )


def trainability_to_bar(level: TrainabilityLevel) -> str:
    """Convert trainability level to visual bar."""
    bars = {
        TrainabilityLevel.LOW: "[##----]",
        TrainabilityLevel.MODERATE: "[###---]",
        TrainabilityLevel.HIGH: "[#####-]",
        TrainabilityLevel.VERY_HIGH: "[######]"
    }
    return bars.get(level, "[???]")


def risk_to_bar(level: InjuryRisk) -> str:
    """Convert injury risk to visual bar."""
    bars = {
        InjuryRisk.LOW: "[#-----] Låg",
        InjuryRisk.MODERATE: "[##----] Måttlig",
        InjuryRisk.ELEVATED: "[####--] Förhöjd",
        InjuryRisk.HIGH: "[######] Hög"
    }
    return bars.get(level, "[???]")


def format_training_report(profile: TrainingProfile) -> str:
    """Format the training profile as a readable report."""

    lines = []
    lines.append("=" * 70)
    lines.append("TRÄNINGSPROFIL")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"ÖVERGRIPANDE TYP: {profile.overall_type}")
    lines.append(f"MUSKELFIBERTENDENS: {profile.muscle_fiber_tendency.value.upper()}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("GENETISK POTENTIAL")
    lines.append("-" * 70)
    lines.append(f"  Kraftpotential:        {trainability_to_bar(profile.power_potential)} {profile.power_potential.value}")
    lines.append(f"  Uthållighetspotential: {trainability_to_bar(profile.endurance_potential)} {profile.endurance_potential.value}")
    lines.append(f"  VO2max-träningsbarhet: {trainability_to_bar(profile.vo2max_trainability)} {profile.vo2max_trainability.value}")
    lines.append(f"  Muskeltillväxt:        {trainability_to_bar(profile.muscle_growth_potential)} {profile.muscle_growth_potential.value}")
    lines.append("")
    lines.append(f"  Senskaderisk:          {risk_to_bar(profile.tendon_injury_risk)}")
    lines.append(f"  Återhämtningshastighet: {profile.recovery_speed}")
    lines.append("")

    if profile.power_genes:
        lines.append("-" * 70)
        lines.append("KRAFT/POWER-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.power_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    if profile.endurance_genes:
        lines.append("-" * 70)
        lines.append("UTHÅLLIGHETS-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.endurance_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    if profile.injury_genes:
        lines.append("-" * 70)
        lines.append("SKADERISK-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.injury_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    if profile.recovery_genes:
        lines.append("-" * 70)
        lines.append("ÅTERHÄMTNINGS-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.recovery_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    lines.append("-" * 70)
    lines.append("IDEALA SPORTER")
    lines.append("-" * 70)
    for sport in profile.ideal_sports:
        lines.append(f"  - {sport}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("TRÄNINGSREKOMMENDATIONER")
    lines.append("-" * 70)
    for rec in profile.training_recommendations:
        lines.append(f"  - {rec}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("SKADEPREVENTION")
    lines.append("-" * 70)
    for rec in profile.injury_prevention:
        lines.append(f"  - {rec}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("ÅTERHÄMTNINGSSTRATEGIER")
    lines.append("-" * 70)
    for rec in profile.recovery_strategies:
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
        print("Usage: python gwl_training_profile.py <genome_file>")
        sys.exit(1)

    genome_file = sys.argv[1]
    print(f"Loading genome from {genome_file}...")
    genotypes = load_genome_snps(genome_file)

    print("Generating training profile...")
    profile = analyze_training_profile(genotypes)

    report = format_training_report(profile)
    print(report)
