#!/usr/bin/env python3
"""
GWL Diet Profile Generator
===========================
Analyzes genetic variants to recommend optimal dietary strategies.

Determines:
- Optimal macronutrient ratios (carbs/fat/protein)
- Carbohydrate sensitivity
- Fat metabolism efficiency
- Satiety genetics
- Food intolerances
- Taste preferences
- Fasting response

Key genes:
- FTO: Obesity/satiety
- TCF7L2: Carbohydrate response
- PPARG: Fat metabolism
- FADS1/2: Omega-3 conversion
- LCT: Lactose tolerance
- TAS2R38: Bitter taste

Genetic Wellness Labs - Nutrigenomics Platform
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum


class MacroResponse(Enum):
    POOR = "poor"
    MODERATE = "moderate"
    GOOD = "good"
    EXCELLENT = "excellent"


class Sensitivity(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class DietProfile:
    """Complete diet genetics profile."""
    overall_diet_type: str

    carb_response: MacroResponse
    fat_response: MacroResponse
    protein_response: MacroResponse
    satiety_efficiency: Sensitivity
    carb_sensitivity: Sensitivity

    recommended_macro_ratio: Dict[str, int]  # carbs, fat, protein percentages

    lactose_tolerance: bool
    gluten_risk: str
    caffeine_metabolism: str
    alcohol_metabolism: str

    taste_profile: List[str]
    foods_to_emphasize: List[str]
    foods_to_limit: List[str]
    fasting_suitability: str

    macro_genes: List[Tuple[str, str, str]]
    satiety_genes: List[Tuple[str, str, str]]
    intolerance_genes: List[Tuple[str, str, str]]
    taste_genes: List[Tuple[str, str, str]]

    meal_timing_recommendations: List[str]
    supplement_recommendations: List[str]


def analyze_diet_profile(genotypes: Dict[str, str]) -> DietProfile:
    """
    Analyze diet-related genetics.

    Key genes analyzed:
    - FTO (rs9939609, rs1421085): Satiety/obesity
    - TCF7L2 (rs7903146): Carb response
    - PPARG (rs1801282): Fat metabolism
    - FADS1/2: Omega-3 conversion
    - APOA5 (rs662799): Fat tolerance
    - ADIPOQ (rs266729): Insulin sensitivity
    - LCT (rs4988235): Lactose
    - HLA-DQ: Celiac
    - CYP1A2 (rs762551): Caffeine
    - ALDH2 (rs671): Alcohol
    - TAS2R38: Bitter taste
    - MC4R: Appetite
    - LEP/LEPR: Satiety
    """

    macro_genes = []
    satiety_genes = []
    intolerance_genes = []
    taste_genes = []

    carb_score = 0  # Higher = better carb tolerance
    fat_score = 0  # Higher = better fat metabolism
    satiety_score = 0  # Higher = better satiety
    protein_score = 0

    # =========================================================================
    # FTO - Fat mass and obesity associated gene
    # =========================================================================
    fto = genotypes.get('rs9939609', '').upper()
    if fto:
        if fto in ['AA', 'A/A']:
            satiety_score -= 2
            satiety_genes.append(("FTO", fto, "A/A - Reducerad mättnadskänsla"))
            satiety_genes.append(("", "", "Tenderar att äta mer och oftare hungrig"))
            satiety_genes.append(("", "", "Bättre respons på proteinrika måltider"))
        elif fto in ['AT', 'TA', 'A/T', 'T/A']:
            satiety_score -= 1
            satiety_genes.append(("FTO", fto, "A/T - Något reducerad mättnadskänsla"))
        else:  # TT
            satiety_genes.append(("FTO", fto, "T/T - Normal mättnadskänsla"))

    fto_2 = genotypes.get('rs1421085', '').upper()
    if fto_2:
        if fto_2 in ['CC', 'C/C']:
            carb_score -= 1
            macro_genes.append(("FTO", fto_2, "C/C - Ökad känslighet för kolhydrater"))
        else:
            macro_genes.append(("FTO", fto_2, "T-bärare - Normal kolhydratrespons"))

    # =========================================================================
    # TCF7L2 - Carbohydrate/diabetes gene
    # =========================================================================
    tcf7l2 = genotypes.get('rs7903146', '').upper()
    if tcf7l2:
        if tcf7l2 in ['TT', 'T/T']:
            carb_score -= 2
            macro_genes.append(("TCF7L2", tcf7l2, "T/T - Reducerad kolhydrattolerans"))
            macro_genes.append(("", "", "Starkaste diabetes-riskgenen"))
            macro_genes.append(("", "", "Bättre med lågkolhydratkost"))
        elif tcf7l2 in ['CT', 'TC', 'C/T', 'T/C']:
            carb_score -= 1
            macro_genes.append(("TCF7L2", tcf7l2, "C/T - Något reducerad kolhydrattolerans"))
        else:  # CC
            macro_genes.append(("TCF7L2", tcf7l2, "C/C - Normal kolhydratmetabolism"))

    # =========================================================================
    # PPARG - Fat storage/metabolism
    # =========================================================================
    pparg = genotypes.get('rs1801282', '').upper()
    if pparg:
        if pparg in ['CG', 'GC', 'C/G', 'G/C', 'GG', 'G/G']:  # Pro12Ala
            fat_score += 1
            macro_genes.append(("PPARG", pparg, "Ala-bärare - Bättre insulinkänslighet"))
            macro_genes.append(("", "", "Lägre risk för typ 2-diabetes"))
        else:  # CC (Pro/Pro)
            macro_genes.append(("PPARG", pparg, "Pro/Pro - Normal fettlagring"))

    # =========================================================================
    # APOA5 - Triglyceride response to fat
    # =========================================================================
    apoa5 = genotypes.get('rs662799', '').upper()
    if apoa5:
        if apoa5 in ['GG', 'G/G', 'CC', 'C/C']:
            macro_genes.append(("APOA5", apoa5, "Normal triglyceridsvar på fett"))
        else:  # AG or AC
            fat_score -= 1
            macro_genes.append(("APOA5", apoa5, "Riskalall - Förhöjda triglycerider vid hög fettintag"))
            macro_genes.append(("", "", "Begränsa mättat fett"))

    # =========================================================================
    # ADIPOQ - Adiponectin/insulin sensitivity
    # =========================================================================
    adipoq = genotypes.get('rs266729', '').upper()
    if adipoq:
        if adipoq in ['GG', 'G/G']:
            macro_genes.append(("ADIPOQ", adipoq, "G/G - Lägre adiponektin"))
            macro_genes.append(("", "", "Ökad risk för insulinresistens"))
            carb_score -= 1
        elif adipoq in ['CC', 'C/C']:
            macro_genes.append(("ADIPOQ", adipoq, "C/C - Normal adiponektin"))

    # =========================================================================
    # FADS1/2 - Omega-3 conversion
    # =========================================================================
    fads1 = genotypes.get('rs174546', '').upper()
    if fads1:
        if fads1 in ['TT', 'T/T']:
            macro_genes.append(("FADS1", fads1, "T/T - Sämre omvandling av ALA→EPA/DHA"))
            macro_genes.append(("", "", "KRITISKT: Behöver omega-3 från fisk, inte växtbaserat"))
        elif fads1 in ['CC', 'C/C']:
            macro_genes.append(("FADS1", fads1, "C/C - Effektiv omega-3 konvertering"))
        else:
            macro_genes.append(("FADS1", fads1, "C/T - Måttlig omega-3 konvertering"))

    # =========================================================================
    # MC4R - Appetite regulation
    # =========================================================================
    mc4r = genotypes.get('rs17782313', '').upper()
    if mc4r:
        if mc4r in ['CC', 'C/C']:
            satiety_score -= 1
            satiety_genes.append(("MC4R", mc4r, "C/C - Ökad aptit och minskad mättnad"))
        else:
            satiety_genes.append(("MC4R", mc4r, "T-bärare - Normal aptitreglering"))

    # =========================================================================
    # LEP/LEPR - Leptin signaling
    # =========================================================================
    lepr = genotypes.get('rs1137101', '').upper()
    if lepr:
        if lepr in ['GG', 'G/G']:
            satiety_score -= 1
            satiety_genes.append(("LEPR", lepr, "G/G - Reducerad leptinkänslighet"))
        else:
            satiety_genes.append(("LEPR", lepr, "A-bärare - Normal leptinkänslighet"))

    # =========================================================================
    # LCT - Lactose tolerance
    # =========================================================================
    lct = genotypes.get('rs4988235', '').upper()
    lactose_tolerant = True
    if lct:
        if lct in ['GG', 'G/G', 'CC', 'C/C']:
            lactose_tolerant = False
            intolerance_genes.append(("LCT", lct, "Laktosintolerant - saknar laktaspersistens"))
        elif lct in ['AA', 'A/A', 'TT', 'T/T']:
            intolerance_genes.append(("LCT", lct, "Laktostolerant - har laktaspersistens"))
        else:
            intolerance_genes.append(("LCT", lct, "Bärare - troligen tolerant"))

    # =========================================================================
    # HLA-DQ - Celiac risk
    # =========================================================================
    celiac_risk = "Låg"
    hla_dq2 = genotypes.get('rs2187668', '').upper()
    if hla_dq2:
        if hla_dq2 in ['AA', 'A/A', 'TT', 'T/T']:
            celiac_risk = "Förhöjd (HLA-DQ2.5)"
            intolerance_genes.append(("HLA-DQ2.5", hla_dq2, "Ökad celiaki-risk"))
        elif hla_dq2 in ['AG', 'GA', 'A/G', 'G/A', 'CT', 'TC', 'C/T', 'T/C']:
            celiac_risk = "Något förhöjd"
            intolerance_genes.append(("HLA-DQ2.5", hla_dq2, "Bärare - viss celiaki-risk"))

    # =========================================================================
    # CYP1A2 - Caffeine metabolism
    # =========================================================================
    cyp1a2 = genotypes.get('rs762551', '').upper()
    caffeine_meta = "Normal"
    if cyp1a2:
        if cyp1a2 in ['AA', 'A/A']:
            caffeine_meta = "Snabb (kan dricka mer)"
            intolerance_genes.append(("CYP1A2", cyp1a2, "A/A - Snabb koffeinmetabolism"))
        else:  # AC or CC
            caffeine_meta = "Långsam (begränsa kaffe)"
            intolerance_genes.append(("CYP1A2", cyp1a2, "C-bärare - Långsam koffeinmetabolism"))
            intolerance_genes.append(("", "", "Ökad kardiovaskulär risk vid >2 koppar/dag"))

    # =========================================================================
    # ALDH2 - Alcohol metabolism
    # =========================================================================
    aldh2 = genotypes.get('rs671', '').upper()
    alcohol_meta = "Normal"
    if aldh2:
        if aldh2 in ['AA', 'A/A', 'GA', 'AG', 'G/A', 'A/G']:
            alcohol_meta = "Nedsatt (flush reaction)"
            intolerance_genes.append(("ALDH2", aldh2, "Nedsatt alkoholmetabolism"))
            intolerance_genes.append(("", "", "Acetaldehyd ackumuleras - ökad cancerrisk"))
        else:
            intolerance_genes.append(("ALDH2", aldh2, "G/G - Normal alkoholmetabolism"))

    # =========================================================================
    # TAS2R38 - Bitter taste (affects vegetable intake)
    # =========================================================================
    tas2r38 = genotypes.get('rs713598', '').upper()
    if tas2r38:
        if tas2r38 in ['GG', 'G/G', 'CC', 'C/C']:
            taste_genes.append(("TAS2R38", tas2r38, "Supertaster - mycket känslig för bitterhet"))
            taste_genes.append(("", "", "Kan ogillar korsblommiga grönsaker"))
        elif tas2r38 in ['CG', 'GC', 'C/G', 'G/C']:
            taste_genes.append(("TAS2R38", tas2r38, "Medium taster"))
        else:
            taste_genes.append(("TAS2R38", tas2r38, "Non-taster - okänslig för bitterhet"))

    # =========================================================================
    # CD36 - Fat taste
    # =========================================================================
    cd36 = genotypes.get('rs1761667', '').upper()
    if cd36:
        if cd36 in ['AA', 'A/A']:
            taste_genes.append(("CD36", cd36, "A/A - Reducerad fettsmak-perception"))
            taste_genes.append(("", "", "Tenderar att äta mer fett för mättnad"))
        elif cd36 in ['GG', 'G/G']:
            taste_genes.append(("CD36", cd36, "G/G - Känslig för fettsmak"))

    # =========================================================================
    # OR6A2 - Cilantro taste
    # =========================================================================
    or6a2 = genotypes.get('rs72921001', '').upper()
    if or6a2:
        if or6a2 in ['CC', 'C/C']:
            taste_genes.append(("OR6A2", or6a2, "C/C - Koriander smakar normalt"))
        else:
            taste_genes.append(("OR6A2", or6a2, "A-bärare - Koriander kan smaka tvål"))

    # =========================================================================
    # Calculate recommendations
    # =========================================================================

    # Determine carb response
    if carb_score <= -2:
        carb_response = MacroResponse.POOR
    elif carb_score <= -1:
        carb_response = MacroResponse.MODERATE
    else:
        carb_response = MacroResponse.GOOD

    # Determine fat response
    if fat_score >= 1:
        fat_response = MacroResponse.EXCELLENT
    elif fat_score >= 0:
        fat_response = MacroResponse.GOOD
    else:
        fat_response = MacroResponse.MODERATE

    # Satiety efficiency
    if satiety_score <= -2:
        satiety_eff = Sensitivity.VERY_HIGH  # Very high = needs more attention
    elif satiety_score <= -1:
        satiety_eff = Sensitivity.HIGH
    else:
        satiety_eff = Sensitivity.NORMAL

    # Carb sensitivity
    if carb_score <= -2:
        carb_sens = Sensitivity.VERY_HIGH
    elif carb_score <= -1:
        carb_sens = Sensitivity.HIGH
    else:
        carb_sens = Sensitivity.NORMAL

    # Determine macro ratios
    if carb_response == MacroResponse.POOR:
        macro_ratio = {"carbs": 25, "fat": 45, "protein": 30}
        diet_type = "LÅGKOLHYDRAT / KETO-VÄNLIG"
    elif carb_response == MacroResponse.MODERATE:
        macro_ratio = {"carbs": 35, "fat": 35, "protein": 30}
        diet_type = "MÅTTLIG KOLHYDRAT / MEDITERRAN"
    else:
        macro_ratio = {"carbs": 45, "fat": 30, "protein": 25}
        diet_type = "BALANSERAD / FLEXIBEL"

    # Adjust for satiety issues
    if satiety_eff in [Sensitivity.HIGH, Sensitivity.VERY_HIGH]:
        macro_ratio["protein"] = min(35, macro_ratio["protein"] + 5)
        macro_ratio["carbs"] = max(20, macro_ratio["carbs"] - 5)

    # Fasting suitability
    if carb_response == MacroResponse.POOR and fat_response in [MacroResponse.GOOD, MacroResponse.EXCELLENT]:
        fasting = "Utmärkt - bra fettförbränning och låg kolhydratkänslighet"
    elif satiety_eff == Sensitivity.VERY_HIGH:
        fasting = "Utmanande - satiety-problem kan göra fasta svår"
    else:
        fasting = "Lämplig - prova 16:8 intermittent fasting"

    # Foods to emphasize
    emphasize = []
    limit = []

    if carb_response == MacroResponse.POOR:
        emphasize.extend([
            "Feta fiskar (lax, makrill, sardiner)",
            "Ägg och äggulor",
            "Olivolja, avokado, nötter",
            "Gröna bladgrönsaker",
            "Bär (lågt GI)"
        ])
        limit.extend([
            "Bröd, pasta, ris",
            "Potatis och rotfrukter",
            "Socker och godis",
            "Fruktjuice och läsk"
        ])
    else:
        emphasize.extend([
            "Fullkorn (havre, quinoa, bulgur)",
            "Baljväxter (linser, bönor)",
            "Frukt och grönsaker",
            "Magert protein"
        ])

    # FADS1-based recommendations
    fads = genotypes.get('rs174546', '').upper()
    if fads in ['TT', 'T/T']:
        emphasize.append("KRITISKT: Fet fisk 3-4 ggr/vecka (inte linfrö!)")
        emphasize.append("Algolja-tillskott om vegetarian")

    # Lactose
    if not lactose_tolerant:
        limit.append("Mjölk och glass (laktosfri OK)")

    # Caffeine
    if "Långsam" in caffeine_meta:
        limit.append("Kaffe (max 1-2 koppar, ej efter lunch)")

    # Taste-based
    if any("Supertaster" in g[2] for g in taste_genes):
        emphasize.append("Tilaga korsblommiga grönsaker (ångkokning minskar bitterhet)")

    # Satiety-based meal timing
    meal_timing = []
    if satiety_eff in [Sensitivity.HIGH, Sensitivity.VERY_HIGH]:
        meal_timing = [
            "Ät proteinrik frukost för bättre mättnad hela dagen",
            "Undvik snabba kolhydrater på tom mage",
            "Ät grönsaker först på tallriken",
            "Vänta 20 min innan andra portionen",
            "Överväg 4-5 mindre måltider istället för 3 stora"
        ]
    else:
        meal_timing = [
            "3 huvudmåltider fungerar bra",
            "Flexibel med måltidsfrekvens"
        ]

    # Supplements
    supplements = []
    if fads in ['TT', 'T/T']:
        supplements.append("Omega-3 (EPA/DHA) - minst 1g/dag från fisk/alger")

    if carb_response == MacroResponse.POOR:
        supplements.append("Krom - kan stödja blodsockerreglering")
        supplements.append("Berberine - naturligt blodsockerstöd")
        supplements.append("Magnesium - viktigt vid lågkolhydratkost")

    if not lactose_tolerant:
        supplements.append("Kalcium + D-vitamin om du undviker mejeriprodukter")

    if not supplements:
        supplements.append("Inga specifika kosttillskott krävs baserat på genetik")

    return DietProfile(
        overall_diet_type=diet_type,
        carb_response=carb_response,
        fat_response=fat_response,
        protein_response=MacroResponse.GOOD,
        satiety_efficiency=satiety_eff,
        carb_sensitivity=carb_sens,
        recommended_macro_ratio=macro_ratio,
        lactose_tolerance=lactose_tolerant,
        gluten_risk=celiac_risk,
        caffeine_metabolism=caffeine_meta,
        alcohol_metabolism=alcohol_meta,
        taste_profile=[g[2] for g in taste_genes if g[0]],
        foods_to_emphasize=emphasize,
        foods_to_limit=limit,
        fasting_suitability=fasting,
        macro_genes=macro_genes,
        satiety_genes=satiety_genes,
        intolerance_genes=intolerance_genes,
        taste_genes=taste_genes,
        meal_timing_recommendations=meal_timing,
        supplement_recommendations=supplements
    )


def format_diet_report(profile: DietProfile) -> str:
    """Format the diet profile as a readable report."""

    lines = []
    lines.append("=" * 70)
    lines.append("KOSTPROFIL")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"REKOMMENDERAD KOSTTYP: {profile.overall_diet_type}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("OPTIMAL MAKROFÖRDELNING")
    lines.append("-" * 70)
    carbs = profile.recommended_macro_ratio["carbs"]
    fat = profile.recommended_macro_ratio["fat"]
    protein = profile.recommended_macro_ratio["protein"]
    lines.append(f"  Kolhydrater: {carbs}%  {'#' * (carbs // 5)}")
    lines.append(f"  Fett:        {fat}%  {'#' * (fat // 5)}")
    lines.append(f"  Protein:     {protein}%  {'#' * (protein // 5)}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("MAKRONÄRINGSRESPONS")
    lines.append("-" * 70)
    lines.append(f"  Kolhydratrespons:   {profile.carb_response.value}")
    lines.append(f"  Fettrespons:        {profile.fat_response.value}")
    lines.append(f"  Mättnadskänsla:     {profile.satiety_efficiency.value}")
    lines.append(f"  Kolhydratkänslighet: {profile.carb_sensitivity.value}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("TOLERANSER")
    lines.append("-" * 70)
    lines.append(f"  Laktos:    {'Tolerant' if profile.lactose_tolerance else 'INTOLERANT'}")
    lines.append(f"  Gluten:    Celiaki-risk: {profile.gluten_risk}")
    lines.append(f"  Koffein:   {profile.caffeine_metabolism}")
    lines.append(f"  Alkohol:   {profile.alcohol_metabolism}")
    lines.append(f"  Fasta:     {profile.fasting_suitability}")
    lines.append("")

    if profile.macro_genes:
        lines.append("-" * 70)
        lines.append("MAKRONÄRINGS-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.macro_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    if profile.satiety_genes:
        lines.append("-" * 70)
        lines.append("MÄTTNADS-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.satiety_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    if profile.intolerance_genes:
        lines.append("-" * 70)
        lines.append("INTOLERANS-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.intolerance_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    if profile.taste_genes:
        lines.append("-" * 70)
        lines.append("SMAK-GENER")
        lines.append("-" * 70)
        for gene, genotype, effect in profile.taste_genes:
            if gene:
                lines.append(f"  {gene} ({genotype}): {effect}")
            else:
                lines.append(f"    -> {effect}")
        lines.append("")

    lines.append("-" * 70)
    lines.append("LIVSMEDEL ATT PRIORITERA")
    lines.append("-" * 70)
    for food in profile.foods_to_emphasize:
        lines.append(f"  + {food}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("LIVSMEDEL ATT BEGRÄNSA")
    lines.append("-" * 70)
    for food in profile.foods_to_limit:
        lines.append(f"  - {food}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("MÅLTIDSREKOMMENDATIONER")
    lines.append("-" * 70)
    for rec in profile.meal_timing_recommendations:
        lines.append(f"  - {rec}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("KOSTTILLSKOTT")
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
        print("Usage: python gwl_diet_profile.py <genome_file>")
        sys.exit(1)

    genome_file = sys.argv[1]
    print(f"Loading genome from {genome_file}...")
    genotypes = load_genome_snps(genome_file)

    print("Generating diet profile...")
    profile = analyze_diet_profile(genotypes)

    report = format_diet_report(profile)
    print(report)
