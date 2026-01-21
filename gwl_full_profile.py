#!/usr/bin/env python3
"""
GWL Full Profile Generator
===========================
Generates a comprehensive genetic profile combining all analysis modules.

Combines:
- Neurotransmitter Profile
- Stress Profile
- Training Profile
- Diet Profile
- Cognitive Profile

Genetic Wellness Labs - Nutrigenomics Platform
"""

import sys
import os
from datetime import datetime
from typing import Dict

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gwl_snp_fetcher import load_genome_snps
from gwl_neurotransmitter_profile import generate_neurotransmitter_profile, format_neurotransmitter_report
from gwl_stress_profile import analyze_stress_profile, format_stress_report
from gwl_training_profile import analyze_training_profile, format_training_report
from gwl_diet_profile import analyze_diet_profile, format_diet_report
from gwl_cognitive_profile import analyze_cognitive_profile, format_cognitive_report


def generate_executive_summary(genotypes: Dict[str, str]) -> str:
    """Generate a brief executive summary of all profiles."""

    # Generate all profiles
    neuro = generate_neurotransmitter_profile(genotypes)
    stress = analyze_stress_profile(genotypes)
    training = analyze_training_profile(genotypes)
    diet = analyze_diet_profile(genotypes)
    cognitive = analyze_cognitive_profile(genotypes)

    lines = []
    lines.append("=" * 70)
    lines.append("EXECUTIVE SUMMARY - GENETISK PROFIL")
    lines.append("=" * 70)
    lines.append("")

    lines.append("PERSONLIGHETSTYP:")
    lines.append(f"  {neuro.overall_type}")
    lines.append("")

    lines.append("VIKTIGA DRAG:")
    for trait in neuro.personality_traits[:4]:
        lines.append(f"  - {trait}")
    lines.append("")

    lines.append("STRESSHANTERING:")
    lines.append(f"  Typ: {stress.overall_type}")
    lines.append(f"  Akut stress: {stress.acute_stress_handling.name}")
    lines.append(f"  Återhämtning: {stress.recovery_speed}")
    lines.append("")

    lines.append("TRÄNING:")
    lines.append(f"  Typ: {training.overall_type}")
    lines.append(f"  Muskelfibertendens: {training.muscle_fiber_tendency.value}")
    lines.append(f"  Senskaderisk: {training.tendon_injury_risk.value}")
    lines.append("")

    lines.append("KOST:")
    lines.append(f"  Rekommenderad: {diet.overall_diet_type}")
    lines.append(f"  Kolhydrattolerans: {diet.carb_response.value}")
    lines.append(f"  Laktos: {'Tolerant' if diet.lactose_tolerance else 'INTOLERANT'}")
    lines.append("")

    lines.append("KOGNITION:")
    lines.append(f"  Typ: {cognitive.overall_type}")
    lines.append(f"  Inlärningsstil: {cognitive.learning_style}")
    lines.append(f"  Alzheimer-risk: {cognitive.cognitive_aging_risk}")
    lines.append("")

    lines.append("TOP 5 OPTIMERINGSSTRATEGIER:")
    strategies = []
    strategies.extend(neuro.optimization_strategies[:2])
    strategies.extend(stress.coping_recommendations[:1])
    strategies.extend(training.training_recommendations[:1])
    strategies.extend(diet.foods_to_emphasize[:1])

    for i, strategy in enumerate(strategies[:5], 1):
        lines.append(f"  {i}. {strategy}")
    lines.append("")

    lines.append("=" * 70)

    return "\n".join(lines)


def generate_full_profile(genome_file: str, output_dir: str = ".") -> Dict[str, str]:
    """
    Generate full genetic profile from genome file.

    Returns dict with paths to generated files.
    """

    print(f"Loading genome from {genome_file}...")
    genotypes = load_genome_snps(genome_file)
    print(f"Loaded {len(genotypes)} SNPs")

    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    base_name = os.path.splitext(os.path.basename(genome_file))[0]

    reports = {}

    # Generate executive summary
    print("Generating executive summary...")
    summary = generate_executive_summary(genotypes)
    reports['summary'] = summary

    # Generate neurotransmitter profile
    print("Generating neurotransmitter profile...")
    neuro_profile = generate_neurotransmitter_profile(genotypes)
    neuro_report = format_neurotransmitter_report(neuro_profile)
    reports['neurotransmitter'] = neuro_report

    # Generate stress profile
    print("Generating stress profile...")
    stress_profile = analyze_stress_profile(genotypes)
    stress_report = format_stress_report(stress_profile)
    reports['stress'] = stress_report

    # Generate training profile
    print("Generating training profile...")
    training_profile = analyze_training_profile(genotypes)
    training_report = format_training_report(training_profile)
    reports['training'] = training_report

    # Generate diet profile
    print("Generating diet profile...")
    diet_profile = analyze_diet_profile(genotypes)
    diet_report = format_diet_report(diet_profile)
    reports['diet'] = diet_report

    # Generate cognitive profile
    print("Generating cognitive profile...")
    cognitive_profile = analyze_cognitive_profile(genotypes)
    cognitive_report = format_cognitive_report(cognitive_profile)
    reports['cognitive'] = cognitive_report

    # Combine all reports
    full_report = []
    full_report.append("=" * 70)
    full_report.append("GWL FULLSTÄNDIG GENETISK PROFIL")
    full_report.append(f"Genererad: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    full_report.append("=" * 70)
    full_report.append("")
    full_report.append("")
    full_report.append(summary)
    full_report.append("")
    full_report.append("")
    full_report.append(neuro_report)
    full_report.append("")
    full_report.append("")
    full_report.append(stress_report)
    full_report.append("")
    full_report.append("")
    full_report.append(training_report)
    full_report.append("")
    full_report.append("")
    full_report.append(diet_report)
    full_report.append("")
    full_report.append("")
    full_report.append(cognitive_report)
    full_report.append("")
    full_report.append("=" * 70)
    full_report.append("SLUT PÅ RAPPORT")
    full_report.append("=" * 70)

    combined = "\n".join(full_report)

    # Save to file
    output_file = os.path.join(output_dir, f"GWL_FullProfil_{timestamp}.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined)

    print(f"\nRapport sparad till: {output_file}")

    return {
        'combined_report': combined,
        'output_file': output_file,
        'reports': reports
    }


def main():
    """Main entry point."""

    if len(sys.argv) < 2:
        print("Usage: python gwl_full_profile.py <genome_file> [--summary]")
        print("")
        print("Options:")
        print("  --summary    Only print executive summary")
        print("")
        print("Example:")
        print("  python gwl_full_profile.py genome.txt")
        sys.exit(1)

    genome_file = sys.argv[1]
    summary_only = "--summary" in sys.argv

    if not os.path.exists(genome_file):
        print(f"Error: File not found: {genome_file}")
        sys.exit(1)

    if summary_only:
        genotypes = load_genome_snps(genome_file)
        summary = generate_executive_summary(genotypes)
        print(summary)
    else:
        result = generate_full_profile(genome_file)
        print(result['combined_report'])


if __name__ == "__main__":
    main()
