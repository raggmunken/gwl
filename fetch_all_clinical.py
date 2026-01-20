#!/usr/bin/env python3
"""
Fetch all missing clinical SNPs and save permanently.
"""

import sys
sys.path.insert(0, '.')

from gwl_snp_fetcher import SNPediaFetcher, load_genome_snps
from gwl_snp_converter import convert_cached_snp, generate_python_code
from gwl_unified_database import get_all_rsids, UNIFIED_DATABASE
from gwl_clinical_snps import get_missing_clinical_snps, CLINICAL_SNPS

# Load extended SNPs
try:
    import gwl_extended_snps
except ImportError:
    pass

def main():
    genome_file = "GENOME/genome_Rasmus_Persson_v5_Full_20240920231531.txt"

    print("Loading genome file...")
    genome_snps = load_genome_snps(genome_file)

    print("Finding missing clinical SNPs...")
    db_rsids = set(get_all_rsids())
    missing = get_missing_clinical_snps(genome_snps, db_rsids)

    print(f"\nFound {len(missing)} missing clinical SNPs")
    print(f"Fetching from SNPedia...\n")

    fetcher = SNPediaFetcher()
    converted = []

    for i, snp_info in enumerate(missing):
        rsid = snp_info['rsid']
        genotype = snp_info['genotype']
        gene = snp_info['gene']

        print(f"[{i+1}/{len(missing)}] Fetching {rsid} ({gene})...", end=" ")

        # Fetch from SNPedia
        snp_data = fetcher.fetch_snp(rsid)

        if snp_data and snp_data.gene:
            # Convert
            from dataclasses import asdict
            cached = asdict(snp_data)
            unified = convert_cached_snp(rsid, cached, genotype)

            if unified:
                converted.append(unified)
                print(f"OK - {len(snp_data.magnitude_data)} genotypes")
            else:
                print("SKIP - conversion failed")
        else:
            print("NOT FOUND in SNPedia")

    print(f"\n\nConverted {len(converted)} SNPs successfully")

    if converted:
        # Generate Python file
        output_file = "gwl_clinical_auto.py"
        code = generate_python_code(converted)

        # Fix the module name
        code = code.replace(
            'def add_auto_fetched_snps():',
            'def add_clinical_auto_snps():'
        )
        code = code.replace(
            '_added = add_auto_fetched_snps()',
            '_added = add_clinical_auto_snps()'
        )
        code = code.replace(
            'print(f"Lade till {_added} auto-hämtade SNPs")',
            'print(f"Lade till {_added} kliniska auto-SNPs")'
        )

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)

        print(f"\nSaved to: {output_file}")
        print(f"To use: import gwl_clinical_auto")

if __name__ == '__main__':
    main()
