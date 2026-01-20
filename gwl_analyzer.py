"""
GWL DNA Analyzer
================
Huvudskript som analyserar 23andMe rådata och genererar komplett profil.

Användning:
    python gwl_analyzer.py din_dna_fil.txt

Genetic Wellness Labs - Nutrigenomics Platform
"""

import sys
import io
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

# Import unified database
from gwl_unified_database import (
    UNIFIED_DATABASE, UnifiedSNP, Category, RiskLevel, ActionPriority,
    get_snp, get_all_rsids, analyze_genotype,
    determine_apoe_genotype, determine_mthfr_status,
    get_database_stats
)

# Import extended SNPs (adds 15+ more SNPs to database)
try:
    import gwl_extended_snps
except ImportError:
    pass  # Extended SNPs not available

# =============================================================================
# DATA CLASSES FOR RESULTS
# =============================================================================

@dataclass
class AnalyzedSNP:
    """Resultat för en analyserad SNP"""
    rsid: str
    gene: str
    genotype: str
    risk_level: str
    effect: str
    description: str
    categories: List[str]
    nutrient_recommendations: List[Dict]
    lifestyle_recommendations: List[str]
    drug_interactions: List[Dict]
    priority: int  # 1-5, lägre = viktigare

@dataclass
class GeneInteraction:
    """En gen-gen interaktion som detekterats"""
    name: str
    genes: List[str]
    effect: str
    combined_recommendation: str

@dataclass
class HaplotypeResult:
    """Resultat för haplotypanalys"""
    gene: str
    haplotype: str
    risk_level: str
    description: str
    recommendations: List[str]

@dataclass
class AnalysisReport:
    """Komplett analysrapport"""
    name: str
    analysis_date: str
    total_snps_in_file: int
    snps_analyzed: int
    snps_with_variants: int

    # Resultat
    analyzed_snps: List[AnalyzedSNP]
    haplotypes: List[HaplotypeResult]
    gene_interactions: List[GeneInteraction]

    # Sammanfattning
    high_priority_findings: List[str]
    nutrient_protocol: List[Dict]
    lifestyle_protocol: List[str]
    drug_alerts: List[Dict]

    # Rådata
    raw_genotypes: Dict[str, str]

# =============================================================================
# 23ANDME FILE PARSER
# =============================================================================

def parse_23andme_file(filepath: str) -> Dict[str, str]:
    """
    Läs in 23andMe rådata-fil och returnera dict med rsid -> genotype.

    Args:
        filepath: Sökväg till 23andMe txt-fil

    Returns:
        Dict med rsid -> genotype (t.ex. {"rs1801133": "AG"})
    """
    genotypes = {}

    # Prova olika encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                for line in f:
                    # Skippa kommentarer och tomma rader
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    # 23andMe format: rsid\tchromosome\tposition\tgenotype
                    parts = line.split('\t')
                    if len(parts) >= 4:
                        rsid = parts[0].lower()
                        genotype = parts[3].upper()

                        # Filtrera bort ogiltiga
                        if rsid.startswith('rs') and genotype not in ['--', '-', '']:
                            genotypes[rsid] = genotype

            print(f"Laste in {len(genotypes)} SNPs fran {filepath}")
            return genotypes

        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading file with {encoding}: {e}")
            continue

    print(f"Kunde inte lasa filen {filepath}")
    return {}

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_snp_from_file(rsid: str, genotype: str) -> Optional[AnalyzedSNP]:
    """Analysera en SNP från filinläsning."""

    result = analyze_genotype(rsid, genotype)
    if not result:
        return None

    # Handle case where genotype is unknown (no risk_level returned)
    if 'risk_level' not in result:
        return None

    # Bestäm prioritet baserat på risk och kategori
    risk = result['risk_level']
    priority = 5  # Default låg

    if risk == RiskLevel.HIGH.value:
        priority = 1
    elif risk == RiskLevel.SIGNIFICANTLY_INCREASED.value:
        priority = 2
    elif risk == RiskLevel.MODERATELY_INCREASED.value:
        priority = 3
    elif risk == RiskLevel.SLIGHTLY_INCREASED.value:
        priority = 4

    # Höj prioritet för farmakogenomik
    if Category.PHARMACOGENOMICS.value in result['categories']:
        priority = min(priority, 2)

    return AnalyzedSNP(
        rsid=rsid,
        gene=result['gene'],
        genotype=genotype,
        risk_level=risk,
        effect=result['effect'],
        description=result['description'],
        categories=result['categories'],
        nutrient_recommendations=result['nutrient_recommendations'],
        lifestyle_recommendations=result['lifestyle_recommendations'],
        drug_interactions=result['drug_interactions'],
        priority=priority
    )

def analyze_haplotypes(genotypes: Dict[str, str]) -> List[HaplotypeResult]:
    """Analysera haplotyper (APOE, MTHFR, etc.)"""
    results = []

    # APOE
    if 'rs429358' in genotypes and 'rs7412' in genotypes:
        apoe_result = determine_apoe_genotype(genotypes['rs429358'], genotypes['rs7412'])
        apoe_diplotype = apoe_result.get('diplotype', 'Unknown')

        risk = RiskLevel.NORMAL
        desc = apoe_result.get('description', '')
        recs = apoe_result.get('recommendations', [])

        if apoe_diplotype == "e4/e4":
            risk = RiskLevel.HIGH
            if not desc:
                desc = "Hogsta risk for Alzheimer (10-15x) och CVD"
            if not recs:
                recs = [
                    "KRITISKT: Minimera mattat fett (<7%)",
                    "Omega-3 hogdos: EPA 2g + DHA 1g dagligen",
                    "MCT-olja for hjarnenergi",
                    "Undvik alkohol",
                    "Statinbehandling rekommenderas",
                    "Kognitiv uppfoljning fran 50 ars alder"
                ]
        elif "e4" in apoe_diplotype:
            risk = RiskLevel.MODERATELY_INCREASED
            if not desc:
                desc = "Forhojd risk for Alzheimer (2-3x) och CVD"
            if not recs:
                recs = [
                    "Begransad mattat fett",
                    "Omega-3 2-3g/dag",
                    "Antioxidanter (E, C, kurkumin)",
                    "Regelbunden motion"
                ]
        elif apoe_diplotype == "e2/e2":
            risk = RiskLevel.SLIGHTLY_INCREASED
            if not desc:
                desc = "Skyddande mot Alzheimer men risk for hyperlipidemi"
            if not recs:
                recs = [
                    "Overvaka triglycerider",
                    "Omega-3 for TG-kontroll"
                ]
        else:
            if not desc:
                desc = f"Normal APOE ({apoe_diplotype})"
            if not recs:
                recs = ["Standardrekommendationer"]

        results.append(HaplotypeResult(
            gene="APOE",
            haplotype=apoe_diplotype,
            risk_level=risk.value,
            description=desc,
            recommendations=recs
        ))

    # MTHFR
    if 'rs1801133' in genotypes and 'rs1801131' in genotypes:
        mthfr = determine_mthfr_status(genotypes['rs1801133'], genotypes['rs1801131'])

        risk = RiskLevel.NORMAL
        recs = mthfr.get('recommendations', [])

        # Handle Swedish severity levels from unified database
        severity = mthfr.get('severity', 'NORMAL')
        if severity in ['ALLVARLIG', 'ALLVARLIG (Compound)']:
            risk = RiskLevel.SIGNIFICANTLY_INCREASED
            if not recs:
                recs = [
                    "ENDAST metylfolat (5-MTHF) - UNDVIK folsyra",
                    "Metylkobalamin (B12) 1000-5000 mcg/dag",
                    "Riboflavin (B2) 50-100 mg/dag",
                    "P5P (B6) 25-50 mg/dag",
                    "Betain (TMG) som alternativ metyldonator",
                    "UNDVIK lustgas vid operation",
                    "Arlig homocysteinkontroll"
                ]
        elif severity == 'MÅTTLIG':
            risk = RiskLevel.MODERATELY_INCREASED
            if not recs:
                recs = [
                    "Metylfolat rekommenderas",
                    "B-vitaminkomplex med aktiva former"
                ]
        elif severity == 'LÄTT':
            risk = RiskLevel.SLIGHTLY_INCREASED
            if not recs:
                recs = ["Metylfolat kan vara fordelaktigt"]
        else:
            if not recs:
                recs = ["Standardrekommendationer"]

        results.append(HaplotypeResult(
            gene="MTHFR",
            haplotype=mthfr.get('combined', 'Unknown'),
            risk_level=risk.value,
            description=mthfr.get('description', ''),
            recommendations=recs
        ))

    return results

def analyze_gene_interactions(genotypes: Dict[str, str], analyzed_snps: List[AnalyzedSNP]) -> List[GeneInteraction]:
    """Hitta och analysera gen-gen interaktioner."""
    interactions = []

    # COMT + MTHFR
    if 'rs4680' in genotypes and 'rs1801133' in genotypes:
        comt = genotypes['rs4680']
        mthfr = genotypes['rs1801133']

        if comt == 'AA' and mthfr == 'AA':  # Met/Met + 677TT
            interactions.append(GeneInteraction(
                name="COMT Met/Met + MTHFR 677TT",
                genes=["COMT", "MTHFR"],
                effect="Hog dopamin men lag SAMe - risk for overmetyleringskanslighet",
                combined_recommendation="FORSIKTIGT med metylfolat - borja MYCKET lagt (50-100 mcg). "
                                        "Undvik SAMe-tillskott. Magnesium viktigt."
            ))
        elif comt == 'GG' and mthfr == 'AA':  # Val/Val + 677TT
            interactions.append(GeneInteraction(
                name="COMT Val/Val + MTHFR 677TT",
                genes=["COMT", "MTHFR"],
                effect="Lag dopamin + lag SAMe - risk for depression",
                combined_recommendation="Metylfolat tolereras battre. SAMe-tillskott kan vara fordelaktigt. "
                                        "Tyrosin for dopaminstod."
            ))

    # IL-6 + TNF-alfa
    if 'rs1800795' in genotypes and 'rs1800629' in genotypes:
        il6 = genotypes.get('rs1800795', '')
        tnf = genotypes.get('rs1800629', '')

        if 'C' in il6 and 'A' in tnf:
            interactions.append(GeneInteraction(
                name="IL-6 + TNF-alfa Pro-inflammatorisk",
                genes=["IL6", "TNF"],
                effect="Bada gener okar inflammation - kronisk laggradig inflammation trolig",
                combined_recommendation="STRIKT anti-inflammatorisk protokoll: Omega-3 hogdos (EPA 2-3g), "
                                        "kurkumin, vitamin D, eliminera socker och omega-6."
            ))

    # FADS + IL-6
    if 'rs174546' in genotypes and 'rs1800795' in genotypes:
        fads = genotypes['rs174546']
        il6 = genotypes['rs1800795']

        if fads == 'CC' and 'C' in il6:
            interactions.append(GeneInteraction(
                name="Hog FADS + Hog IL-6",
                genes=["FADS1", "IL6"],
                effect="Hog AA-produktion + hog inflammation = pro-inflammatorisk",
                combined_recommendation="KRAFTIGT minska omega-6 intag. Hogdos EPA/DHA obligatoriskt."
            ))
        elif fads == 'TT' and 'C' in il6:
            interactions.append(GeneInteraction(
                name="Lag FADS + Hog IL-6",
                genes=["FADS1", "IL6"],
                effect="Kan inte konvertera ALA men har hog inflammation",
                combined_recommendation="MASTE fa preformerad EPA/DHA - ALA fungerar INTE. "
                                        "Algojla eller fiskolja obligatoriskt."
            ))

    # CYP1B1 + COMT (östrogen)
    if 'rs1056836' in genotypes and 'rs4680' in genotypes:
        cyp1b1 = genotypes.get('rs1056836', '')
        comt = genotypes['rs4680']

        if 'G' in cyp1b1 and comt == 'AA':
            interactions.append(GeneInteraction(
                name="CYP1B1 hog + COMT Met/Met",
                genes=["CYP1B1", "COMT"],
                effect="Hog 4-OH-ostrogen + langsam metylering = okad cancerrisk",
                combined_recommendation="DIM/I3C for att skifta till 2-OH-vag. Korsblommiga gronsaker dagligen. "
                                        "Forsigtighet vid HRT."
            ))

    return interactions

def compile_nutrient_protocol(analyzed_snps: List[AnalyzedSNP], haplotypes: List[HaplotypeResult]) -> List[Dict]:
    """Sammanställ ett prioriterat näringsprotokoll."""
    all_recs = {}

    # Samla från SNPs
    for snp in analyzed_snps:
        for rec in snp.nutrient_recommendations:
            nutrient = rec.get('nutrient', '')
            if nutrient not in all_recs:
                all_recs[nutrient] = {
                    "nutrient": nutrient,
                    "dose": rec.get('dose', ''),
                    "reasons": [],
                    "priority": rec.get('priority', 'normal'),
                    "genes": []
                }
            all_recs[nutrient]["reasons"].append(rec.get('reason', ''))
            all_recs[nutrient]["genes"].append(snp.gene)

            # Uppgradera prioritet om critical/high
            if rec.get('priority') == 'critical':
                all_recs[nutrient]["priority"] = 'critical'
            elif rec.get('priority') == 'high' and all_recs[nutrient]["priority"] != 'critical':
                all_recs[nutrient]["priority"] = 'high'

    # Samla från haplotyper
    for hap in haplotypes:
        for rec in hap.recommendations:
            # Enkel parsing
            if ':' in rec:
                parts = rec.split(':')
                nutrient = parts[0].strip()
                dose = parts[1].strip() if len(parts) > 1 else ''
            else:
                nutrient = rec
                dose = ''

            if nutrient not in all_recs and not nutrient.startswith('UNDVIK'):
                all_recs[nutrient] = {
                    "nutrient": nutrient,
                    "dose": dose,
                    "reasons": [f"Baserat pa {hap.gene} {hap.haplotype}"],
                    "priority": "high" if hap.risk_level in [RiskLevel.HIGH.value, RiskLevel.SIGNIFICANTLY_INCREASED.value] else "normal",
                    "genes": [hap.gene]
                }

    # Sortera efter prioritet
    priority_order = {'critical': 0, 'high': 1, 'normal': 2}
    sorted_recs = sorted(
        all_recs.values(),
        key=lambda x: priority_order.get(x['priority'], 2)
    )

    return sorted_recs

def compile_drug_alerts(analyzed_snps: List[AnalyzedSNP]) -> List[Dict]:
    """Sammanställ läkemedelsvarningar."""
    alerts = []

    for snp in analyzed_snps:
        for interaction in snp.drug_interactions:
            alerts.append({
                "drug": interaction.get('drug', ''),
                "gene": snp.gene,
                "genotype": snp.genotype,
                "action": interaction.get('action', ''),
                "note": interaction.get('note', ''),
                "rsid": snp.rsid
            })

    # Sortera: UNDVIK först
    alerts.sort(key=lambda x: 0 if 'UNDVIK' in x['action'].upper() else 1)

    return alerts

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_dna(filepath: str, name: str = "Anonym") -> AnalysisReport:
    """
    Huvudfunktion - analysera DNA-fil och generera rapport.

    Args:
        filepath: Sökväg till 23andMe-fil
        name: Namn för rapporten

    Returns:
        AnalysisReport med alla resultat
    """
    print(f"\n{'='*60}")
    print(f"GWL DNA ANALYZER")
    print(f"{'='*60}")
    print(f"Analyserar: {filepath}")
    print(f"Namn: {name}")
    print(f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Läs in fil
    genotypes = parse_23andme_file(filepath)
    if not genotypes:
        raise ValueError("Kunde inte läsa DNA-filen")

    # Hitta matchande SNPs
    db_rsids = set(get_all_rsids())
    file_rsids = set(genotypes.keys())
    matching_rsids = db_rsids.intersection(file_rsids)

    print(f"\nSNPs i fil: {len(genotypes)}")
    print(f"SNPs i databas: {len(db_rsids)}")
    print(f"Matchande SNPs: {len(matching_rsids)}")

    # Analysera varje SNP
    analyzed_snps = []
    for rsid in matching_rsids:
        result = analyze_snp_from_file(rsid, genotypes[rsid])
        if result:
            analyzed_snps.append(result)

    # Sortera efter prioritet
    analyzed_snps.sort(key=lambda x: x.priority)

    # Räkna varianter
    variants_count = sum(1 for s in analyzed_snps
                        if s.risk_level not in [RiskLevel.NORMAL.value, RiskLevel.PROTECTIVE.value])

    print(f"Analyserade SNPs: {len(analyzed_snps)}")
    print(f"SNPs med varianter: {variants_count}")

    # Haplotyper
    print("\nAnalyserar haplotyper...")
    haplotypes = analyze_haplotypes(genotypes)
    for hap in haplotypes:
        print(f"  {hap.gene}: {hap.haplotype}")

    # Gen-interaktioner
    print("\nAnalyserar gen-interaktioner...")
    interactions = analyze_gene_interactions(genotypes, analyzed_snps)
    for inter in interactions:
        print(f"  {inter.name}")

    # Sammanställ protokoll
    print("\nSammanstaller protokoll...")
    nutrient_protocol = compile_nutrient_protocol(analyzed_snps, haplotypes)
    drug_alerts = compile_drug_alerts(analyzed_snps)

    # High priority findings
    high_priority = []
    for snp in analyzed_snps:
        if snp.priority <= 2:
            high_priority.append(f"{snp.gene} {snp.rsid}: {snp.effect}")

    for hap in haplotypes:
        if hap.risk_level in [RiskLevel.HIGH.value, RiskLevel.SIGNIFICANTLY_INCREASED.value]:
            high_priority.append(f"{hap.gene} {hap.haplotype}: {hap.description}")

    # Lifestyle recommendations
    all_lifestyle = []
    for snp in analyzed_snps:
        all_lifestyle.extend(snp.lifestyle_recommendations)
    for hap in haplotypes:
        all_lifestyle.extend(hap.recommendations)
    # Ta bort dubbletter
    lifestyle_protocol = list(dict.fromkeys(all_lifestyle))

    # Skapa rapport
    report = AnalysisReport(
        name=name,
        analysis_date=datetime.now().isoformat(),
        total_snps_in_file=len(genotypes),
        snps_analyzed=len(analyzed_snps),
        snps_with_variants=variants_count,
        analyzed_snps=analyzed_snps,
        haplotypes=haplotypes,
        gene_interactions=interactions,
        high_priority_findings=high_priority,
        nutrient_protocol=nutrient_protocol,
        lifestyle_protocol=lifestyle_protocol,
        drug_alerts=drug_alerts,
        raw_genotypes={k: v for k, v in genotypes.items() if k in matching_rsids}
    )

    print(f"\nAnalys klar!")
    return report

# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_markdown_report(report: AnalysisReport) -> str:
    """Generera en Markdown-rapport."""
    lines = [
        f"# GWL Genetisk Profil: {report.name}",
        f"**Analyserad:** {report.analysis_date[:10]}",
        "",
        "---",
        "",
        "## Sammanfattning",
        "",
        f"- **SNPs i fil:** {report.total_snps_in_file}",
        f"- **Analyserade SNPs:** {report.snps_analyzed}",
        f"- **SNPs med varianter:** {report.snps_with_variants}",
        "",
    ]

    # High priority
    if report.high_priority_findings:
        lines.append("## Viktigaste fynden")
        lines.append("")
        for finding in report.high_priority_findings:
            lines.append(f"- {finding}")
        lines.append("")

    # Haplotypes
    if report.haplotypes:
        lines.append("## Haplotyper")
        lines.append("")
        for hap in report.haplotypes:
            lines.append(f"### {hap.gene}: {hap.haplotype}")
            lines.append(f"**Risk:** {hap.risk_level}")
            lines.append(f"**Beskrivning:** {hap.description}")
            lines.append("")
            if hap.recommendations:
                lines.append("**Rekommendationer:**")
                for rec in hap.recommendations:
                    lines.append(f"- {rec}")
            lines.append("")

    # Gene interactions
    if report.gene_interactions:
        lines.append("## Gen-Gen Interaktioner")
        lines.append("")
        for inter in report.gene_interactions:
            lines.append(f"### {inter.name}")
            lines.append(f"**Gener:** {', '.join(inter.genes)}")
            lines.append(f"**Effekt:** {inter.effect}")
            lines.append(f"**Rekommendation:** {inter.combined_recommendation}")
            lines.append("")

    # Drug alerts
    if report.drug_alerts:
        lines.append("## Lakemedelsvarningar")
        lines.append("")
        lines.append("| Lakemedel | Gen | Genotyp | Atgard | Notering |")
        lines.append("|-----------|-----|---------|--------|----------|")
        for alert in report.drug_alerts:
            lines.append(f"| {alert['drug']} | {alert['gene']} | {alert['genotype']} | {alert['action']} | {alert['note']} |")
        lines.append("")

    # Nutrient protocol
    if report.nutrient_protocol:
        lines.append("## Naringsprotokoll")
        lines.append("")

        # Critical
        critical = [n for n in report.nutrient_protocol if n['priority'] == 'critical']
        if critical:
            lines.append("### Kritiska (Obligatoriska)")
            for n in critical:
                genes = ', '.join(set(n['genes']))
                lines.append(f"- **{n['nutrient']}** - {n['dose']}")
                lines.append(f"  - Gener: {genes}")
                lines.append(f"  - Anledning: {'; '.join(set(n['reasons']))}")
            lines.append("")

        # High priority
        high = [n for n in report.nutrient_protocol if n['priority'] == 'high']
        if high:
            lines.append("### Hog Prioritet")
            for n in high:
                genes = ', '.join(set(n['genes']))
                lines.append(f"- **{n['nutrient']}** - {n['dose']}")
                lines.append(f"  - Gener: {genes}")
            lines.append("")

        # Normal
        normal = [n for n in report.nutrient_protocol if n['priority'] == 'normal']
        if normal:
            lines.append("### Rekommenderade")
            for n in normal[:15]:  # Begränsa
                lines.append(f"- {n['nutrient']} - {n['dose']}")
            lines.append("")

    # Lifestyle
    if report.lifestyle_protocol:
        lines.append("## Livsstilsrekommendationer")
        lines.append("")
        for rec in report.lifestyle_protocol[:20]:  # Begränsa
            lines.append(f"- {rec}")
        lines.append("")

    # Detailed SNP table
    lines.append("## Detaljerad SNP-Analys")
    lines.append("")
    lines.append("| Gen | rsid | Genotyp | Risk | Effekt |")
    lines.append("|-----|------|---------|------|--------|")
    for snp in report.analyzed_snps[:30]:  # Begränsa
        lines.append(f"| {snp.gene} | {snp.rsid} | {snp.genotype} | {snp.risk_level} | {snp.effect[:50]}... |")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("*Genererad av Genetic Wellness Labs - Nutrigenomics Platform*")
    lines.append("")
    lines.append("**Disclaimer:** Denna rapport ar endast for informationsandamal och ersatter inte medicinsk radgivning.")

    return '\n'.join(lines)

def save_report(report: AnalysisReport, output_dir: str = "."):
    """Spara rapport i olika format."""

    base_name = f"GWL_Profil_{report.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"

    # Markdown
    md_path = os.path.join(output_dir, f"{base_name}.md")
    md_content = generate_markdown_report(report)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Sparade Markdown: {md_path}")

    # JSON
    json_path = os.path.join(output_dir, f"{base_name}.json")

    def convert(obj):
        if hasattr(obj, '__dataclass_fields__'):
            return asdict(obj)
        elif isinstance(obj, list):
            return [convert(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        return obj

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(convert(report), f, indent=2, ensure_ascii=False)
    print(f"Sparade JSON: {json_path}")

    return md_path, json_path

# =============================================================================
# MAIN
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description='GWL DNA Analyzer')
    parser.add_argument('file', nargs='?', help='23andMe raw data file')
    parser.add_argument('--name', '-n', default='Anonym', help='Name for the report')
    parser.add_argument('--output', '-o', default='.', help='Output directory')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')

    args = parser.parse_args()

    if args.stats:
        stats = get_database_stats()
        print("\nGWL Database Statistics:")
        print(f"  Total SNPs: {stats['total_snps']}")
        print(f"  Unique Genes: {stats['genes']}")
        print(f"  Total Pathways: {stats['pathways']}")
        print(f"  With Drug Interactions: {stats['with_drug_interactions']}")
        print(f"  With Haplotype Info: {stats['with_haplotype_info']}")
        print("\n  SNPs per Category:")
        for cat, count in sorted(stats['categories'].items(), key=lambda x: -x[1]):
            print(f"    {cat}: {count}")
        return

    if not args.file:
        parser.print_help()
        print("\nExample:")
        print("  python gwl_analyzer.py my_23andme_data.txt --name 'John Doe'")
        return

    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        return

    # Run analysis
    report = analyze_dna(args.file, args.name)

    # Save reports
    save_report(report, args.output)

    # Print summary
    print("\n" + "=" * 60)
    print("SAMMANFATTNING")
    print("=" * 60)

    if report.high_priority_findings:
        print("\nVIKTIGASTE FYNDEN:")
        for finding in report.high_priority_findings[:5]:
            print(f"  ! {finding}")

    if report.drug_alerts:
        print(f"\nLAKEMEDELSVARNINGAR: {len(report.drug_alerts)}")
        for alert in report.drug_alerts[:3]:
            print(f"  ! {alert['drug']}: {alert['action']}")

    print(f"\nRapport sparad!")

if __name__ == "__main__":
    # Fix Windows encoding for special characters
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    main()
