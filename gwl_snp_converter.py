#!/usr/bin/env python3
"""
GWL SNP Converter
=================
Converts fetched SNPs from SNPedia cache to UnifiedSNP format.

This script:
1. Reads the SNPedia cache
2. Enriches data with user's genotype from genome file
3. Converts to UnifiedSNP format
4. Generates Python code or adds directly to database

Genetic Wellness Labs - Nutrigenomics Platform
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Import our modules
from gwl_unified_database import (
    UnifiedSNP, Category, RiskLevel, UNIFIED_DATABASE
)

CACHE_FILE = Path(__file__).parent / "snp_cache" / "snpedia_cache.json"

# Map SNPedia categories to our Category enum
CATEGORY_MAP = {
    'pharmacogenomics': Category.PHARMACOGENOMICS,
    'nutrigenomics': Category.METHYLATION,
    'metabolism': Category.BLOOD_SUGAR,
    'cardiovascular': Category.CARDIOVASCULAR,
    'inflammation': Category.INFLAMMATION,
    'detoxification': Category.DETOX_PHASE2,
    'immune': Category.IMMUNE,
    'bone_health': Category.BONE_HEALTH,
    'sleep_circadian': Category.SLEEP,
    'fitness': Category.MUSCLE,
    'longevity': Category.ANTIOXIDANT,
    'mental_health': Category.STRESS_MOOD
}

# Gene to category mapping for common genes
GENE_CATEGORY_MAP = {
    # Pharmacogenomics
    'CYP2D6': Category.PHARMACOGENOMICS, 'CYP2C9': Category.PHARMACOGENOMICS,
    'CYP2C19': Category.PHARMACOGENOMICS, 'CYP3A4': Category.PHARMACOGENOMICS,
    'CYP1A2': Category.CAFFEINE, 'SLCO1B1': Category.PHARMACOGENOMICS,
    'VKORC1': Category.PHARMACOGENOMICS, 'NAT2': Category.PHARMACOGENOMICS,

    # Methylation/B-vitamins
    'MTHFR': Category.METHYLATION, 'MTR': Category.METHYLATION,
    'MTRR': Category.METHYLATION, 'BHMT': Category.METHYLATION,
    'CBS': Category.METHYLATION, 'COMT': Category.STRESS_MOOD,

    # Vitamins
    'VDR': Category.VITAMIN_D, 'CYP2R1': Category.VITAMIN_D,
    'GC': Category.VITAMIN_D, 'BCMO1': Category.ANTIOXIDANT,
    'BCO1': Category.ANTIOXIDANT, 'FUT2': Category.METHYLATION,

    # Omega/Fat metabolism
    'FADS1': Category.OMEGA3, 'FADS2': Category.OMEGA3,
    'APOE': Category.CARDIOVASCULAR, 'PPARG': Category.BLOOD_SUGAR,

    # Weight/Metabolism
    'FTO': Category.OBESITY, 'MC4R': Category.OBESITY,
    'ADRB2': Category.MUSCLE, 'ADRB3': Category.OBESITY,

    # Blood sugar
    'TCF7L2': Category.BLOOD_SUGAR, 'KCNJ11': Category.BLOOD_SUGAR,

    # Iron
    'HFE': Category.IRON, 'TF': Category.IRON,

    # Inflammation
    'IL6': Category.INFLAMMATION, 'TNF': Category.INFLAMMATION,
    'IL1B': Category.INFLAMMATION, 'CRP': Category.INFLAMMATION,

    # Detox
    'GSTP1': Category.DETOX_PHASE2, 'GSTM1': Category.DETOX_PHASE2,
    'CYP1B1': Category.DETOX_PHASE1, 'NQO1': Category.DETOX_PHASE2,
    'SOD2': Category.ANTIOXIDANT,

    # Sleep
    'CLOCK': Category.CIRCADIAN, 'ADA': Category.SLEEP,
    'ADORA2A': Category.CAFFEINE, 'PER2': Category.CIRCADIAN,

    # Fitness
    'ACTN3': Category.MUSCLE, 'ACE': Category.MUSCLE,

    # Immune/Food
    'LCT': Category.IMMUNE, 'MCM6': Category.IMMUNE,
    'HLA-DQ2': Category.IMMUNE, 'HLA-DQ8': Category.IMMUNE,

    # Longevity
    'FOXO3': Category.ANTIOXIDANT, 'SIRT1': Category.ANTIOXIDANT,
}


def load_cache() -> Dict[str, dict]:
    """Load the SNPedia cache"""
    if not CACHE_FILE.exists():
        return {}

    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def magnitude_to_risk(magnitude: float, repute: str) -> RiskLevel:
    """Convert SNPedia magnitude to our RiskLevel"""
    if repute == 'good':
        return RiskLevel.PROTECTIVE
    elif magnitude >= 4:
        return RiskLevel.HIGH
    elif magnitude >= 3:
        return RiskLevel.SIGNIFICANTLY_INCREASED
    elif magnitude >= 2:
        return RiskLevel.MODERATELY_INCREASED
    elif magnitude >= 1:
        return RiskLevel.SLIGHTLY_INCREASED
    else:
        return RiskLevel.NORMAL


def get_category_for_gene(gene: str, snp_categories: List[str]) -> Category:
    """Determine the best category for a gene"""
    # First check our gene map
    gene_upper = gene.upper()
    if gene_upper in GENE_CATEGORY_MAP:
        return GENE_CATEGORY_MAP[gene_upper]

    # Check SNPedia categories
    for cat in snp_categories:
        if cat in CATEGORY_MAP:
            return CATEGORY_MAP[cat]

    # Default
    return Category.INFLAMMATION


def generate_recommendations(gene: str, genotype_data: dict, repute: str) -> Tuple[List[dict], List[str]]:
    """
    Generate nutrient and lifestyle recommendations based on gene and genotype.

    Returns:
        Tuple of (nutrient_recommendations, lifestyle_recommendations)
    """
    nutrients = []
    lifestyle = []

    gene_upper = gene.upper()
    summary = genotype_data.get('summary', '').lower()
    magnitude = genotype_data.get('magnitude', 0)

    # Gene-specific recommendations
    if gene_upper == 'MTHFR':
        if magnitude >= 2:
            nutrients.append({"nutrient": "Metylfolat (5-MTHF)", "dose": "400-800 mcg/dag", "reason": "Kringgår MTHFR-defekt"})
            nutrients.append({"nutrient": "Metylkobalamin (B12)", "dose": "1000 mcg/dag", "reason": "Stödjer metylering"})
            lifestyle.append("Undvik syntetisk folsyra")

    elif gene_upper == 'VDR':
        nutrients.append({"nutrient": "D-vitamin", "dose": "2000-4000 IE/dag", "reason": "VDR-variant kan kräva högre nivåer"})
        lifestyle.append("Testa D-vitamin-nivåer regelbundet")

    elif gene_upper in ['CYP2R1', 'GC']:
        nutrients.append({"nutrient": "D-vitamin", "dose": "3000-5000 IE/dag", "reason": "Kompensera för sämre D-vitamin-metabolism"})

    elif gene_upper in ['BCO1', 'BCMO1']:
        if magnitude >= 1.5:
            nutrients.append({"nutrient": "A-vitamin (retinol)", "dose": "5000 IE/dag", "reason": "Sämre konvertering från betakaroten"})
            lifestyle.append("Förlita dig inte på morötter för A-vitamin - ät lever eller ta tillskott")

    elif gene_upper in ['FADS1', 'FADS2']:
        nutrients.append({"nutrient": "Omega-3 (EPA/DHA)", "dose": "2-3 g/dag", "reason": "Sämre konvertering från ALA"})
        lifestyle.append("Prioritera fet fisk eller algolja framför vegetabiliska omega-3-källor")

    elif gene_upper == 'FTO':
        if magnitude >= 1.5:
            nutrients.append({"nutrient": "Protein", "dose": "1.6-2.0 g/kg/dag", "reason": "Ökar mättnad"})
            lifestyle.append("Proteinrik frukost rekommenderas starkt")
            lifestyle.append("Undvik snacking - håll regelbundna måltider")

    elif gene_upper in ['CYP2C9', 'CYP2C19', 'CYP2D6']:
        lifestyle.append("Informera läkare om denna variant vid läkemedelsförskrivning")

    elif gene_upper == 'SLCO1B1':
        lifestyle.append("Ökad risk för statinbiverkningar - diskutera med läkare")

    elif gene_upper == 'HFE':
        lifestyle.append("Monitorera järnnivåer regelbundet")
        lifestyle.append("Undvik järntillskott om inte ordinerat")

    elif gene_upper in ['LCT', 'MCM6']:
        if 'intoleran' in summary or magnitude >= 2:
            nutrients.append({"nutrient": "Kalcium", "dose": "1000 mg/dag", "reason": "Kompensera för minskade mejeriprodukter"})
            lifestyle.append("Laktosfria alternativ rekommenderas")

    # Add generic lifestyle recommendation if bad repute
    if repute == 'bad' and magnitude >= 2 and not lifestyle:
        lifestyle.append("Denna variant kan påverka din hälsa - konsultera specialist vid behov")

    return nutrients, lifestyle


def convert_cached_snp(rsid: str, cached_data: dict, user_genotype: Optional[str] = None) -> Optional[UnifiedSNP]:
    """
    Convert a cached SNP to UnifiedSNP format.

    Args:
        rsid: The rsid
        cached_data: Data from the cache
        user_genotype: Optional user's genotype for this SNP

    Returns:
        UnifiedSNP or None if conversion fails
    """
    if cached_data.get('not_found'):
        return None

    gene = cached_data.get('gene', '')
    if not gene:
        return None

    chromosome = cached_data.get('chromosome', '')
    position = cached_data.get('position', 0)
    categories = cached_data.get('categories', [])
    magnitude_data = cached_data.get('magnitude_data', {})
    references = cached_data.get('references', [])
    summary = cached_data.get('summary', '')

    # Determine category
    category = get_category_for_gene(gene, categories)

    # Build genotype effects
    genotype_effects = {}
    nutrient_recommendations = {}
    lifestyle_recommendations = {}

    for gt, data in magnitude_data.items():
        mag = data.get('magnitude', 0)
        repute = data.get('repute', 'neutral')
        gt_summary = data.get('summary', '')

        risk = magnitude_to_risk(mag, repute)

        genotype_effects[gt] = {
            'risk': risk,
            'effect': gt_summary or f"Magnitude {mag}",
            'description': gt_summary
        }

        # Generate recommendations for significant genotypes
        if mag >= 1.5:
            nutrients, lifestyle = generate_recommendations(gene, data, repute)
            if nutrients:
                nutrient_recommendations[gt] = nutrients
            if lifestyle:
                lifestyle_recommendations[gt] = lifestyle

    # If no genotype data, create minimal entry
    if not genotype_effects:
        genotype_effects = {
            'normal': {
                'risk': RiskLevel.NORMAL,
                'effect': summary or 'No data',
                'description': summary
            }
        }

    # Determine ref/alt alleles from genotypes
    all_alleles = set()
    for gt in magnitude_data.keys():
        all_alleles.update(list(gt))

    ref_allele = 'G' if 'G' in all_alleles else (list(all_alleles)[0] if all_alleles else 'N')
    alt_allele = [a for a in all_alleles if a != ref_allele][0] if len(all_alleles) > 1 else 'N'

    # Create UnifiedSNP
    try:
        snp = UnifiedSNP(
            rsid=rsid,
            gene=gene,
            chromosome=str(chromosome),
            position=int(position) if position else 0,
            ref_allele=ref_allele,
            alt_allele=alt_allele,
            categories=[category],
            genotype_effects=genotype_effects,
            nutrient_recommendations=nutrient_recommendations,
            lifestyle_recommendations=lifestyle_recommendations,
            drug_interactions={},
            pathways=[],
            interacts_with=[],
            haplotype_gene=None,
            haplotype_role=None,
            frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},  # Unknown
            pmids=references[:10],  # Limit to 10
            clinical_significance=summary[:200] if summary else f"Auto-fetched from SNPedia",
            evidence_level="SNPedia"
        )
        return snp
    except Exception as e:
        print(f"  Error converting {rsid}: {e}")
        return None


def generate_python_code(snps: List[UnifiedSNP]) -> str:
    """Generate Python code for adding SNPs to database"""

    lines = [
        '"""',
        'GWL Auto-Fetched SNPs',
        '=====================',
        f'Auto-generated from SNPedia cache on {datetime.now().strftime("%Y-%m-%d")}',
        '',
        'These SNPs were automatically fetched and converted.',
        'Review and adjust recommendations as needed.',
        '"""',
        '',
        'from gwl_unified_database import UnifiedSNP, Category, RiskLevel, UNIFIED_DATABASE',
        '',
        'AUTO_FETCHED_SNPS = {',
    ]

    for snp in snps:
        lines.append(f'    "{snp.rsid}": UnifiedSNP(')
        lines.append(f'        rsid="{snp.rsid}",')
        lines.append(f'        gene="{snp.gene}",')
        lines.append(f'        chromosome="{snp.chromosome}",')
        lines.append(f'        position={snp.position},')
        lines.append(f'        ref_allele="{snp.ref_allele}",')
        lines.append(f'        alt_allele="{snp.alt_allele}",')
        lines.append(f'        categories=[Category.{snp.categories[0].name}],')

        # Genotype effects
        lines.append('        genotype_effects={')
        for gt, effect in snp.genotype_effects.items():
            risk_name = effect['risk'].name if hasattr(effect['risk'], 'name') else effect['risk']
            desc = effect.get('description', '').replace('"', '\\"')[:100]
            lines.append(f'            "{gt}": {{"risk": RiskLevel.{risk_name}, "effect": "{desc}", "description": "{desc}"}},')
        lines.append('        },')

        # Nutrient recommendations
        lines.append('        nutrient_recommendations={')
        for gt, recs in snp.nutrient_recommendations.items():
            recs_str = str(recs).replace("'", '"')
            lines.append(f'            "{gt}": {recs_str},')
        lines.append('        },')

        # Lifestyle recommendations
        lines.append('        lifestyle_recommendations={')
        for gt, recs in snp.lifestyle_recommendations.items():
            recs_str = str(recs)
            lines.append(f'            "{gt}": {recs_str},')
        lines.append('        },')

        lines.append('        drug_interactions={},')
        lines.append('        pathways=[],')
        lines.append('        interacts_with=[],')
        lines.append('        haplotype_gene=None,')
        lines.append('        haplotype_role=None,')
        lines.append('        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},')
        lines.append(f'        pmids={snp.pmids[:5]},')
        lines.append(f'        clinical_significance="{snp.clinical_significance[:100]}",')
        lines.append(f'        evidence_level="SNPedia"')
        lines.append('    ),')
        lines.append('')

    lines.append('}')
    lines.append('')
    lines.append('def add_auto_fetched_snps():')
    lines.append('    """Add auto-fetched SNPs to database"""')
    lines.append('    for rsid, snp in AUTO_FETCHED_SNPS.items():')
    lines.append('        if rsid not in UNIFIED_DATABASE:')
    lines.append('            UNIFIED_DATABASE[rsid] = snp')
    lines.append('    return len(AUTO_FETCHED_SNPS)')
    lines.append('')
    lines.append('# Auto-add on import')
    lines.append('_added = add_auto_fetched_snps()')
    lines.append('print(f"Lade till {_added} auto-hämtade SNPs")')

    return '\n'.join(lines)


def add_to_database_directly(snps: List[UnifiedSNP]) -> int:
    """Add SNPs directly to the runtime database"""
    added = 0
    for snp in snps:
        if snp.rsid not in UNIFIED_DATABASE:
            UNIFIED_DATABASE[snp.rsid] = snp
            added += 1
    return added


def main():
    """CLI for converting cached SNPs"""
    import argparse

    parser = argparse.ArgumentParser(description='Convert SNPedia cache to UnifiedSNP format')
    parser.add_argument('--generate', metavar='FILE', help='Generate Python file with converted SNPs')
    parser.add_argument('--add-runtime', action='store_true', help='Add to runtime database')
    parser.add_argument('--list', action='store_true', help='List convertible SNPs in cache')
    parser.add_argument('--genome', metavar='FILE', help='Genome file for genotype lookup')

    args = parser.parse_args()

    # Load cache
    cache = load_cache()
    if not cache:
        print("No cached SNPs found. Run gwl_snp_fetcher.py first.")
        return

    print(f"Found {len(cache)} entries in cache")

    # Load genome if provided
    genome_snps = {}
    if args.genome:
        from gwl_snp_fetcher import load_genome_snps
        genome_snps = load_genome_snps(args.genome)
        print(f"Loaded {len(genome_snps)} SNPs from genome file")

    # Convert SNPs
    converted = []
    skipped_not_found = 0
    skipped_no_gene = 0
    skipped_already_exists = 0

    # Load existing database
    try:
        import gwl_extended_snps
    except ImportError:
        pass

    existing_rsids = set(UNIFIED_DATABASE.keys())

    for rsid, data in cache.items():
        if data.get('not_found'):
            skipped_not_found += 1
            continue

        if rsid in existing_rsids:
            skipped_already_exists += 1
            continue

        user_genotype = genome_snps.get(rsid.lower())
        snp = convert_cached_snp(rsid, data, user_genotype)

        if snp:
            converted.append(snp)
        else:
            skipped_no_gene += 1

    print(f"\nConversion results:")
    print(f"  Converted: {len(converted)}")
    print(f"  Skipped (not found in SNPedia): {skipped_not_found}")
    print(f"  Skipped (no gene info): {skipped_no_gene}")
    print(f"  Skipped (already in database): {skipped_already_exists}")

    if args.list:
        print("\nConvertible SNPs:")
        for snp in converted:
            print(f"  {snp.rsid}: {snp.gene} - {snp.categories[0].value}")

    if args.generate:
        code = generate_python_code(converted)
        with open(args.generate, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"\nGenerated: {args.generate}")

    if args.add_runtime:
        added = add_to_database_directly(converted)
        print(f"\nAdded {added} SNPs to runtime database")
        print(f"Total SNPs in database: {len(UNIFIED_DATABASE)}")


if __name__ == '__main__':
    main()
