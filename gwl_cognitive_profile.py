#!/usr/bin/env python3
"""
GWL Cognitive Profile Generator
================================
Analyzes genetic variants related to cognitive function.

Explains:
- Memory capacity and type
- Learning style
- Attention and focus
- Processing speed
- Cognitive aging risk
- Neuroplasticity

Key genes:
- KIBRA: Episodic memory
- BDNF: Neuroplasticity
- APOE: Cognitive aging
- COMT: Working memory vs flexibility
- CHRNA4: Attention
- TOMM40: Cognitive aging

Genetic Wellness Labs - Nutrigenomics Platform
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum


class CognitiveLevel(Enum):
    LOW = "low"
    BELOW_AVERAGE = "below_average"
    AVERAGE = "average"
    ABOVE_AVERAGE = "above_average"
    HIGH = "high"


@dataclass
class CognitiveProfile:
    """Complete cognitive genetics profile."""
    overall_type: str

    episodic_memory: CognitiveLevel
    working_memory: CognitiveLevel
    cognitive_flexibility: CognitiveLevel
    attention_focus: CognitiveLevel
    processing_speed: CognitiveLevel
    neuroplasticity: CognitiveLevel
    cognitive_aging_risk: str

    learning_style: str
    optimal_study_strategies: List[str]
    cognitive_strengths: List[str]
    cognitive_challenges: List[str]

    neuroprotection_strategies: List[str]
    lifestyle_recommendations: List[str]
    supplement_recommendations: List[str]

    memory_genes: List[Tuple[str, str, str]]
    attention_genes: List[Tuple[str, str, str]]
    aging_genes: List[Tuple[str, str, str]]


def analyze_cognitive_profile(genotypes: Dict[str, str]) -> CognitiveProfile:
    """
    Analyze cognitive-related genetics.

    Key genes:
    - KIBRA (rs17070145): Episodic memory
    - BDNF (rs6265): Neuroplasticity
    - APOE (rs429358, rs7412): Cognitive aging
    - COMT (rs4680): Working memory vs flexibility tradeoff
    - CHRNA4 (rs1044396): Attention
    - TOMM40 (rs2075650): Cognitive aging
    - DRD2: Reward-based learning
    - SNAP25: Synaptic function
    """

    memory_genes = []
    attention_genes = []
    aging_genes = []

    episodic_score = 0
    working_mem_score = 0
    flexibility_score = 0
    attention_score = 0
    plasticity_score = 0
    aging_risk_score = 0

    strengths = []
    challenges = []

    # =========================================================================
    # KIBRA - Episodic Memory (rs17070145)
    # =========================================================================
    kibra = genotypes.get('rs17070145', '').upper()
    if kibra:
        if kibra in ['TT', 'T/T']:
            episodic_score += 2
            memory_genes.append(("KIBRA", kibra, "T/T - Förbättrat episodiskt minne"))
            memory_genes.append(("", "", "Bättre på att minnas händelser och upplevelser"))
            strengths.append("Starkt episodiskt minne - minns händelser väl")
        elif kibra in ['CT', 'TC', 'C/T', 'T/C']:
            episodic_score += 1
            memory_genes.append(("KIBRA", kibra, "C/T - Normalt-bra episodiskt minne"))
        else:  # CC
            memory_genes.append(("KIBRA", kibra, "C/C - Normalt episodiskt minne"))
            challenges.append("Episodiskt minne kan behöva extra stöd")

    # =========================================================================
    # BDNF - Brain-Derived Neurotrophic Factor (rs6265)
    # =========================================================================
    bdnf = genotypes.get('rs6265', '').upper()
    if bdnf:
        # G = Val, A = Met (or C = Val, T = Met depending on strand)
        if bdnf in ['GG', 'G/G', 'CC', 'C/C']:  # Val/Val
            plasticity_score += 2
            memory_genes.append(("BDNF", bdnf, "Val/Val - Normal BDNF-frisättning"))
            memory_genes.append(("", "", "Bra neuroplasticitet och inlärningsförmåga"))
            strengths.append("God neuroplasticitet - hjärnan anpassar sig väl")
        elif bdnf in ['AG', 'GA', 'A/G', 'G/A', 'CT', 'TC', 'C/T', 'T/C']:  # Val/Met
            plasticity_score += 1
            memory_genes.append(("BDNF", bdnf, "Val/Met - Något reducerad BDNF"))
            memory_genes.append(("", "", "Motion extra viktigt för BDNF-produktion"))
            challenges.append("Behöver träning för optimal BDNF-produktion")
        else:  # Met/Met
            plasticity_score -= 1
            memory_genes.append(("BDNF", bdnf, "Met/Met - Reducerad BDNF-frisättning"))
            memory_genes.append(("", "", "Ökad känslighet för stress på minnet"))
            challenges.append("Reducerad neuroplasticitet - kräver mer repetition")
            challenges.append("Stresskänslig inlärning")

    # =========================================================================
    # COMT - Working Memory vs Cognitive Flexibility (rs4680)
    # =========================================================================
    comt = genotypes.get('rs4680', '').upper()
    if comt:
        if comt in ['AA', 'A/A']:  # Met/Met
            working_mem_score += 2
            flexibility_score -= 1
            attention_genes.append(("COMT", comt, "Met/Met - Hög prefrontal dopamin"))
            attention_genes.append(("", "", "Bättre arbetsminne i lugna miljöer"))
            attention_genes.append(("", "", "Kan vara stel i tänkandet under stress"))
            strengths.append("Utmärkt arbetsminne i lugna situationer")
            strengths.append("Bra på detaljarbete och noggrannhet")
            challenges.append("Kognitiv flexibilitet minskar under stress")
        elif comt in ['GG', 'G/G']:  # Val/Val
            working_mem_score -= 1
            flexibility_score += 2
            attention_genes.append(("COMT", comt, "Val/Val - Låg prefrontal dopamin"))
            attention_genes.append(("", "", "Bättre kognitiv flexibilitet"))
            attention_genes.append(("", "", "Kan ha svårare med uthållig koncentration"))
            strengths.append("Hög kognitiv flexibilitet - bra på multitasking")
            strengths.append("Presterar väl under press")
            challenges.append("Kan ha svårt med långvarig fokusering")
        else:  # AG/GA - heterozygot
            attention_genes.append(("COMT", comt, "Val/Met - Balanserad dopaminnivå"))
            strengths.append("Balanserad kognitiv profil")

    # =========================================================================
    # CHRNA4 - Nicotinic Receptor / Attention (rs1044396)
    # =========================================================================
    chrna4 = genotypes.get('rs1044396', '').upper()
    if chrna4:
        if chrna4 in ['TT', 'T/T']:
            attention_score += 1
            attention_genes.append(("CHRNA4", chrna4, "T/T - Bättre selektiv uppmärksamhet"))
            strengths.append("Bra selektiv uppmärksamhet")
        elif chrna4 in ['CC', 'C/C']:
            attention_genes.append(("CHRNA4", chrna4, "C/C - Normal uppmärksamhet"))
        else:
            attention_genes.append(("CHRNA4", chrna4, "C/T - Normal-bra uppmärksamhet"))

    # =========================================================================
    # APOE - Cognitive Aging (rs429358, rs7412)
    # =========================================================================
    apoe_1 = genotypes.get('rs429358', '').upper()
    apoe_2 = genotypes.get('rs7412', '').upper()

    # Determine APOE genotype
    apoe_genotype = "e3/e3"  # default
    e4_count = 0
    e2_count = 0

    if apoe_1 and apoe_2:
        # rs429358: T=e3/e2, C=e4
        # rs7412: C=e3/e4, T=e2
        if 'C' in apoe_1.replace('/', ''):
            e4_count += apoe_1.replace('/', '').count('C')
        if 'T' in apoe_2.replace('/', ''):
            e2_count += apoe_2.replace('/', '').count('T')

        if e4_count >= 2:
            apoe_genotype = "e4/e4"
            aging_risk_score += 3
        elif e4_count == 1:
            apoe_genotype = "e3/e4"
            aging_risk_score += 1
        elif e2_count >= 1:
            apoe_genotype = "e2/e3"
            aging_risk_score -= 1

    if aging_risk_score >= 2:
        aging_genes.append(("APOE", apoe_genotype, "e4-bärare - Ökad Alzheimer-risk"))
        aging_genes.append(("", "", "Extra viktigt med livsstilsåtgärder"))
        challenges.append("Förhöjd risk för kognitivt åldrande")
    elif aging_risk_score <= -1:
        aging_genes.append(("APOE", apoe_genotype, "e2-bärare - Skyddande mot Alzheimer"))
        strengths.append("Genetiskt skydd mot kognitivt åldrande")
    else:
        aging_genes.append(("APOE", apoe_genotype, "Normal Alzheimer-risk"))

    # =========================================================================
    # TOMM40 - Cognitive Aging (rs2075650)
    # =========================================================================
    tomm40 = genotypes.get('rs2075650', '').upper()
    if tomm40:
        if tomm40 in ['GG', 'G/G']:
            aging_risk_score += 1
            aging_genes.append(("TOMM40", tomm40, "G/G - Associerad med snabbare kognitivt åldrande"))
        else:
            aging_genes.append(("TOMM40", tomm40, "A-bärare - Normal"))

    # =========================================================================
    # DRD2 - Reward-based Learning (rs1800497)
    # =========================================================================
    drd2 = genotypes.get('rs1800497', '').upper()
    if drd2:
        if drd2 in ['AA', 'A/A', 'TT', 'T/T']:  # A1/A1
            attention_genes.append(("DRD2", drd2, "A1/A1 - Lär sig bättre från belöning än straff"))
            strengths.append("Motiveras av positiv förstärkning")
            challenges.append("Kan ha svårt att lära från negativ feedback")
        else:
            attention_genes.append(("DRD2", drd2, "A2-bärare - Balanserad feedback-inlärning"))

    # =========================================================================
    # SNAP25 - Synaptic Function (rs3785143)
    # =========================================================================
    snap25 = genotypes.get('rs3785143', '').upper()
    if snap25:
        memory_genes.append(("SNAP25", snap25, "Synaptisk vesikelgen"))
        if snap25 in ['GG', 'G/G']:
            memory_genes.append(("", "", "G/G - Optimal synaptisk funktion"))

    # =========================================================================
    # Calculate levels
    # =========================================================================

    def score_to_level(score):
        if score >= 2:
            return CognitiveLevel.HIGH
        elif score >= 1:
            return CognitiveLevel.ABOVE_AVERAGE
        elif score <= -2:
            return CognitiveLevel.LOW
        elif score <= -1:
            return CognitiveLevel.BELOW_AVERAGE
        return CognitiveLevel.AVERAGE

    episodic_memory = score_to_level(episodic_score)
    working_memory = score_to_level(working_mem_score)
    cognitive_flex = score_to_level(flexibility_score)
    attention = score_to_level(attention_score)
    neuroplasticity = score_to_level(plasticity_score)

    # Cognitive aging risk
    if aging_risk_score >= 3:
        aging_risk = "Hög - aktiva åtgärder kritiska"
    elif aging_risk_score >= 1:
        aging_risk = "Något förhöjd - livsstilsåtgärder rekommenderas"
    elif aging_risk_score <= -1:
        aging_risk = "Låg - genetiskt skyddad"
    else:
        aging_risk = "Normal"

    # Overall type
    if working_memory == CognitiveLevel.HIGH and cognitive_flex in [CognitiveLevel.LOW, CognitiveLevel.BELOW_AVERAGE]:
        overall_type = "ANALYTIKER / DETALJFOKUSERAD"
        learning_style = "Strukturerad, steg-för-steg, detaljrik"
    elif cognitive_flex == CognitiveLevel.HIGH:
        overall_type = "FLEXIBEL / KREATIV TÄNKARE"
        learning_style = "Utforskande, konceptuell, 'big picture'"
    elif episodic_memory == CognitiveLevel.HIGH:
        overall_type = "BERÄTTANDE / NARRATIV TÄNKARE"
        learning_style = "Genom historier, exempel och upplevelser"
    else:
        overall_type = "BALANSERAD KOGNITIV PROFIL"
        learning_style = "Flexibel - anpassar sig till olika metoder"

    # =========================================================================
    # Generate recommendations
    # =========================================================================

    study_strategies = []
    neuroprotection = []
    lifestyle = []
    supplements = []

    # Based on COMT
    if comt in ['AA', 'A/A']:
        study_strategies.append("Studera i lugna, tysta miljöer")
        study_strategies.append("Ta pauser för att undvika mental överbelastning")
        study_strategies.append("Använd detaljerade anteckningar och struktur")
        study_strategies.append("Undvik multitasking under inlärning")
    elif comt in ['GG', 'G/G']:
        study_strategies.append("Kan hantera lite bakgrundsljud")
        study_strategies.append("Variera studiematerial för att hålla intresset")
        study_strategies.append("Deadline-press kan faktiskt hjälpa fokus")
        study_strategies.append("Korta, intensiva studiepass")

    # Based on BDNF
    if plasticity_score <= 0:
        study_strategies.append("Mer repetition behövs för långtidsminne")
        study_strategies.append("Spaced repetition är extra viktigt")
        lifestyle.append("KRITISKT: Regelbunden motion ökar BDNF")

    # Based on memory
    if episodic_score >= 1:
        study_strategies.append("Använd personliga kopplingar och berättelser")
        study_strategies.append("'Memory palace'-tekniken passar dig")
    else:
        study_strategies.append("Använd aktiva inlärningsmetoder (inte bara läsning)")
        study_strategies.append("Skapa visuella hjälpmedel och diagram")

    # Based on DRD2
    if drd2 in ['AA', 'A/A', 'TT', 'T/T']:
        study_strategies.append("Belöna dig själv efter studiepass")
        study_strategies.append("Gamification fungerar bra för dig")

    # Neuroprotection based on aging risk
    if aging_risk_score >= 1:
        neuroprotection = [
            "KRITISKT: Regelbunden aerob träning (30 min, 5 ggr/vecka)",
            "Mediterran kost - visat skydda kognitiv funktion",
            "Sociala aktiviteter - starkt skyddande",
            "Kognitiv stimulering - lär nya saker kontinuerligt",
            "Optimal sömn - 7-8 timmar",
            "Stresshantering - kronisk stress skadar hippocampus",
            "Överväg regelbunden kognitiv screening"
        ]
        supplements = [
            "Omega-3 DHA (minst 1g/dag) - kritiskt för hjärnhälsa",
            "Vitamin D - brist kopplad till demens",
            "B12 och folat - viktigt för metylering",
            "Överväg Lion's Mane (NGF-stimulerande)"
        ]
    else:
        neuroprotection = [
            "Regelbunden motion",
            "Sociala aktiviteter",
            "Kontinuerligt lärande",
            "God sömn"
        ]
        supplements = ["Omega-3 för allmän hjärnhälsa"]

    # General lifestyle
    lifestyle.extend([
        "Prioritera sömn - minneskonslolidering sker under sömn",
        "Regelbunden motion ökar BDNF och hjärnhälsa",
        "Minska stress - kortisol skadar hippocampus",
        "Sociala kontakter skyddar kognition"
    ])

    # Remove duplicates
    lifestyle = list(dict.fromkeys(lifestyle))
    study_strategies = list(dict.fromkeys(study_strategies))

    return CognitiveProfile(
        overall_type=overall_type,
        episodic_memory=episodic_memory,
        working_memory=working_memory,
        cognitive_flexibility=cognitive_flex,
        attention_focus=attention,
        processing_speed=CognitiveLevel.AVERAGE,
        neuroplasticity=neuroplasticity,
        cognitive_aging_risk=aging_risk,
        learning_style=learning_style,
        optimal_study_strategies=study_strategies,
        cognitive_strengths=strengths,
        cognitive_challenges=challenges,
        neuroprotection_strategies=neuroprotection,
        lifestyle_recommendations=lifestyle,
        supplement_recommendations=supplements,
        memory_genes=memory_genes,
        attention_genes=attention_genes,
        aging_genes=aging_genes
    )


def level_to_bar(level: CognitiveLevel) -> str:
    """Convert cognitive level to visual bar."""
    bars = {
        CognitiveLevel.LOW: "[#-----]",
        CognitiveLevel.BELOW_AVERAGE: "[##----]",
        CognitiveLevel.AVERAGE: "[###---]",
        CognitiveLevel.ABOVE_AVERAGE: "[####--]",
        CognitiveLevel.HIGH: "[#####-]"
    }
    return bars.get(level, "[???]")


def format_cognitive_report(profile: CognitiveProfile) -> str:
    """Format the cognitive profile as a readable report."""

    lines = []
    lines.append("=" * 70)
    lines.append("KOGNITIV PROFIL")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"ÖVERGRIPANDE TYP: {profile.overall_type}")
    lines.append(f"INLÄRNINGSSTIL: {profile.learning_style}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("KOGNITIVA FÖRMÅGOR")
    lines.append("-" * 70)
    lines.append(f"  Episodiskt minne:      {level_to_bar(profile.episodic_memory)} {profile.episodic_memory.value}")
    lines.append(f"  Arbetsminne:           {level_to_bar(profile.working_memory)} {profile.working_memory.value}")
    lines.append(f"  Kognitiv flexibilitet: {level_to_bar(profile.cognitive_flexibility)} {profile.cognitive_flexibility.value}")
    lines.append(f"  Uppmärksamhet/fokus:   {level_to_bar(profile.attention_focus)} {profile.attention_focus.value}")
    lines.append(f"  Neuroplasticitet:      {level_to_bar(profile.neuroplasticity)} {profile.neuroplasticity.value}")
    lines.append("")
    lines.append(f"  Kognitivt åldrande-risk: {profile.cognitive_aging_risk}")
    lines.append("")

    if profile.cognitive_strengths:
        lines.append("-" * 70)
        lines.append("KOGNITIVA STYRKOR")
        lines.append("-" * 70)
        for strength in profile.cognitive_strengths:
            lines.append(f"  + {strength}")
        lines.append("")

    if profile.cognitive_challenges:
        lines.append("-" * 70)
        lines.append("UTMANINGAR")
        lines.append("-" * 70)
        for challenge in profile.cognitive_challenges:
            lines.append(f"  - {challenge}")
        lines.append("")

    if profile.memory_genes:
        lines.append("-" * 70)
        lines.append("MINNES-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.memory_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    if profile.attention_genes:
        lines.append("-" * 70)
        lines.append("UPPMÄRKSAMHETS-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.attention_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    if profile.aging_genes:
        lines.append("-" * 70)
        lines.append("KOGNITIVT ÅLDRANDE-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.aging_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    lines.append("-" * 70)
    lines.append("OPTIMALA STUDIESTRATEGIER")
    lines.append("-" * 70)
    for strategy in profile.optimal_study_strategies:
        lines.append(f"  - {strategy}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("NEUROPROTEKTIVA ÅTGÄRDER")
    lines.append("-" * 70)
    for strategy in profile.neuroprotection_strategies:
        lines.append(f"  - {strategy}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("LIVSSTILSREKOMMENDATIONER")
    lines.append("-" * 70)
    for rec in profile.lifestyle_recommendations:
        lines.append(f"  - {rec}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("KOSTTILLSKOTT FÖR KOGNITION")
    lines.append("-" * 70)
    for supp in profile.supplement_recommendations:
        lines.append(f"  - {supp}")
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
        print("Usage: python gwl_cognitive_profile.py <genome_file>")
        sys.exit(1)

    genome_file = sys.argv[1]
    print(f"Loading genome from {genome_file}...")
    genotypes = load_genome_snps(genome_file)

    print("Generating cognitive profile...")
    profile = analyze_cognitive_profile(genotypes)

    report = format_cognitive_report(profile)
    print(report)
