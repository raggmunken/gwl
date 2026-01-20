#!/usr/bin/env python3
"""
GWL SNP Fetcher
===============
Fetches SNP data from public databases (SNPedia, dbSNP) and caches locally.

Features:
- Fetches SNP info from SNPedia API
- Caches results to avoid repeated API calls
- Prioritizes clinically relevant SNPs
- Converts to UnifiedSNP format for integration

Genetic Wellness Labs - Nutrigenomics Platform
"""

import json
import os
import re
import time
import urllib.request
import urllib.parse
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from pathlib import Path

# Cache configuration
CACHE_DIR = Path(__file__).parent / "snp_cache"
CACHE_FILE = CACHE_DIR / "snpedia_cache.json"
CACHE_EXPIRY_DAYS = 30  # Re-fetch after 30 days

# Rate limiting
API_DELAY_SECONDS = 0.5  # Be nice to SNPedia

# Known clinically relevant SNP categories for prioritization
CLINICAL_CATEGORIES = {
    "pharmacogenomics": [
        "CYP2D6", "CYP2C9", "CYP2C19", "CYP3A4", "CYP1A2", "CYP2B6",
        "SLCO1B1", "VKORC1", "DPYD", "TPMT", "UGT1A1", "NAT2"
    ],
    "nutrigenomics": [
        "MTHFR", "MTRR", "MTR", "BHMT", "CBS", "COMT", "VDR", "BCMO1",
        "FADS1", "FADS2", "FUT2", "TCN2", "SLC23A1", "NBPF3"
    ],
    "metabolism": [
        "FTO", "MC4R", "PPARG", "ADRB2", "ADRB3", "FABP2", "ADIPOQ",
        "LEP", "LEPR", "UCP1", "UCP2", "UCP3"
    ],
    "cardiovascular": [
        "APOE", "APOB", "APOA1", "PCSK9", "LDLR", "CETP", "LPL",
        "MTHFR", "ACE", "AGT", "NOS3", "F2", "F5"
    ],
    "inflammation": [
        "IL6", "IL1B", "IL10", "TNF", "CRP", "NFKB1", "PTGS2"
    ],
    "detoxification": [
        "GSTM1", "GSTT1", "GSTP1", "SOD2", "CAT", "GPX1", "NQO1",
        "CYP1B1", "CYP1A1", "NAT1", "NAT2", "PON1"
    ],
    "immune": [
        "HLA-DQ2", "HLA-DQ8", "HLA-B27", "IL23R", "NOD2", "ATG16L1"
    ],
    "bone_health": [
        "VDR", "COL1A1", "ESR1", "LRP5", "SOST"
    ],
    "sleep_circadian": [
        "CLOCK", "PER2", "PER3", "ARNTL", "ADA", "ADORA2A"
    ],
    "fitness": [
        "ACTN3", "ACE", "PPARGC1A", "AMPD1", "COL5A1", "VEGFA"
    ],
    "longevity": [
        "FOXO3", "APOE", "CETP", "IL6", "TERT", "SIRT1"
    ],
    "mental_health": [
        "COMT", "BDNF", "SLC6A4", "HTR2A", "DRD2", "DRD4", "MAOA"
    ]
}

# Flatten to get all genes of interest
ALL_CLINICAL_GENES = set()
for genes in CLINICAL_CATEGORIES.values():
    ALL_CLINICAL_GENES.update(genes)


@dataclass
class FetchedSNP:
    """Data fetched from SNPedia"""
    rsid: str
    gene: str
    chromosome: str
    position: int
    summary: str
    magnitude_data: Dict[str, dict]  # genotype -> {magnitude, summary}
    categories: List[str]
    references: List[str]
    fetch_date: str
    source: str = "SNPedia"


class SNPediaFetcher:
    """Fetches SNP data from SNPedia MediaWiki API"""

    BASE_URL = "https://bots.snpedia.com/api.php"

    def __init__(self):
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict[str, dict]:
        """Load cached SNP data"""
        CACHE_DIR.mkdir(exist_ok=True)
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_cache(self):
        """Save cache to disk"""
        CACHE_DIR.mkdir(exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _is_cache_valid(self, rsid: str) -> bool:
        """Check if cached data is still valid"""
        if rsid not in self.cache:
            return False

        cached = self.cache[rsid]
        if 'fetch_date' not in cached:
            return False

        try:
            fetch_date = datetime.fromisoformat(cached['fetch_date'])
            expiry = fetch_date + timedelta(days=CACHE_EXPIRY_DAYS)
            return datetime.now() < expiry
        except (ValueError, TypeError):
            return False

    def _fetch_page(self, title: str) -> Optional[str]:
        """Fetch a page from SNPedia"""
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'revisions',
            'rvprop': 'content',
            'format': 'json'
        }

        url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"

        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'GWL-Nutrigenomics/1.0 (research)'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                pages = data.get('query', {}).get('pages', {})
                for page_id, page_data in pages.items():
                    if page_id == '-1':
                        return None
                    revisions = page_data.get('revisions', [])
                    if revisions:
                        return revisions[0].get('*', '')
        except Exception as e:
            print(f"  Error fetching {title}: {e}")
            return None

        return None

    def _parse_snp_page(self, rsid: str, content: str) -> Optional[FetchedSNP]:
        """Parse SNPedia page content"""
        if not content:
            return None

        # Extract basic info
        gene = ""
        chromosome = ""
        position = 0
        summary = ""

        # Parse gene
        gene_match = re.search(r'\|\s*Gene\s*=\s*([^\|\n]+)', content, re.IGNORECASE)
        if gene_match:
            gene = gene_match.group(1).strip()

        # Parse chromosome
        chr_match = re.search(r'\|\s*Chromosome\s*=\s*(\d+|X|Y)', content, re.IGNORECASE)
        if chr_match:
            chromosome = chr_match.group(1)

        # Parse position
        pos_match = re.search(r'\|\s*Position\s*=\s*(\d+)', content, re.IGNORECASE)
        if pos_match:
            position = int(pos_match.group(1))

        # Parse summary (first paragraph after template)
        summary_match = re.search(r'\}\}\s*\n\s*([^\n\[{]+)', content)
        if summary_match:
            summary = summary_match.group(1).strip()

        # Extract categories from content
        categories = []
        for cat_name, genes in CLINICAL_CATEGORIES.items():
            if gene.upper() in [g.upper() for g in genes]:
                categories.append(cat_name)

        # Find PMID references
        pmids = re.findall(r'PMID\s*=?\s*(\d+)', content, re.IGNORECASE)

        return FetchedSNP(
            rsid=rsid,
            gene=gene,
            chromosome=chromosome,
            position=position,
            summary=summary,
            magnitude_data={},
            categories=categories,
            references=list(set(pmids)),
            fetch_date=datetime.now().isoformat()
        )

    def _fetch_genotype_info(self, rsid: str, genotype: str) -> Optional[dict]:
        """Fetch genotype-specific page from SNPedia"""
        # SNPedia uses format like Rs1234(A;A)
        page_title = f"{rsid}({genotype[0]};{genotype[1]})"
        content = self._fetch_page(page_title)

        if not content:
            # Try alternative format
            page_title = f"{rsid}({genotype[1]};{genotype[0]})"
            content = self._fetch_page(page_title)

        if not content:
            return None

        # Parse magnitude
        magnitude = 0
        mag_match = re.search(r'\|\s*magnitude\s*=\s*([\d.]+)', content, re.IGNORECASE)
        if mag_match:
            magnitude = float(mag_match.group(1))

        # Parse summary/repute
        summary = ""
        sum_match = re.search(r'\|\s*summary\s*=\s*([^\|\n]+)', content, re.IGNORECASE)
        if sum_match:
            summary = sum_match.group(1).strip()

        repute = "neutral"
        rep_match = re.search(r'\|\s*repute\s*=\s*(\w+)', content, re.IGNORECASE)
        if rep_match:
            repute = rep_match.group(1).lower()

        return {
            'magnitude': magnitude,
            'summary': summary,
            'repute': repute
        }

    def fetch_snp(self, rsid: str, fetch_genotypes: bool = True) -> Optional[FetchedSNP]:
        """
        Fetch SNP data from SNPedia.

        Args:
            rsid: The rsid to fetch (e.g., "rs1234567")
            fetch_genotypes: Also fetch genotype-specific pages

        Returns:
            FetchedSNP object or None if not found
        """
        rsid = rsid.lower()

        # Check cache first
        if self._is_cache_valid(rsid):
            cached = self.cache[rsid]
            return FetchedSNP(**cached)

        print(f"  Fetching {rsid} from SNPedia...")
        time.sleep(API_DELAY_SECONDS)

        # Fetch main SNP page
        content = self._fetch_page(rsid.capitalize())
        if not content:
            # Mark as not found in cache to avoid repeated lookups
            self.cache[rsid] = {'not_found': True, 'fetch_date': datetime.now().isoformat()}
            self._save_cache()
            return None

        snp = self._parse_snp_page(rsid, content)
        if not snp:
            return None

        # Fetch common genotype pages if requested
        if fetch_genotypes:
            common_genotypes = ['AA', 'AG', 'GG', 'AC', 'CC', 'AT', 'TT', 'CT', 'CG', 'GT']
            for gt in common_genotypes:
                time.sleep(API_DELAY_SECONDS / 2)  # Shorter delay for genotype pages
                gt_info = self._fetch_genotype_info(rsid, gt)
                if gt_info and gt_info.get('magnitude', 0) > 0:
                    snp.magnitude_data[gt] = gt_info

        # Cache the result
        self.cache[rsid] = asdict(snp)
        self._save_cache()

        return snp

    def get_cache_stats(self) -> dict:
        """Get statistics about the cache"""
        total = len(self.cache)
        not_found = sum(1 for v in self.cache.values() if v.get('not_found'))
        found = total - not_found

        genes = set()
        for v in self.cache.values():
            if 'gene' in v and v['gene']:
                genes.add(v['gene'])

        return {
            'total_cached': total,
            'found': found,
            'not_found': not_found,
            'unique_genes': len(genes)
        }


class ClinicalSNPPrioritizer:
    """Prioritizes SNPs based on clinical relevance"""

    # High-priority SNPs that should always be checked
    HIGH_PRIORITY_SNPS = {
        # Pharmacogenomics - critical for drug safety
        'rs1799853', 'rs1057910',  # CYP2C9
        'rs4244285', 'rs4986893', 'rs12248560',  # CYP2C19
        'rs3892097', 'rs1065852',  # CYP2D6
        'rs762551',  # CYP1A2
        'rs4149056',  # SLCO1B1
        'rs9923231',  # VKORC1

        # Nutrigenomics - methylation
        'rs1801133', 'rs1801131',  # MTHFR
        'rs1801394',  # MTRR
        'rs1805087',  # MTR
        'rs4680',  # COMT

        # Cardiovascular
        'rs429358', 'rs7412',  # APOE
        'rs1800629',  # TNF
        'rs1800795',  # IL6

        # Metabolism/Weight
        'rs9939609',  # FTO
        'rs7903146',  # TCF7L2
        'rs1801282',  # PPARG

        # Vitamin metabolism
        'rs10741657', 'rs12794714',  # CYP2R1
        'rs2228570', 'rs1544410',  # VDR
        'rs12934922', 'rs7501331',  # BCMO1
        'rs174546', 'rs174547',  # FADS1

        # Detox
        'rs1695',  # GSTP1
        'rs1056836',  # CYP1B1

        # Food intolerances
        'rs4988235',  # LCT (lactose)
        'rs2187668',  # HLA-DQ2.5 (celiac)

        # Fitness/Performance
        'rs1815739',  # ACTN3
        'rs4994',  # ADRB3
        'rs1042713',  # ADRB2

        # Iron
        'rs1800562', 'rs1799945',  # HFE

        # Sleep
        'rs73598374',  # ADA
        'rs1801260',  # CLOCK

        # Longevity
        'rs2802292',  # FOXO3
    }

    def __init__(self, genome_snps: Dict[str, str]):
        """
        Initialize with SNPs from genome file.

        Args:
            genome_snps: Dict of rsid -> genotype from genome file
        """
        self.genome_snps = genome_snps
        self.genome_rsids = set(genome_snps.keys())

    def get_priority_snps(self, existing_db_rsids: Set[str]) -> List[str]:
        """
        Get prioritized list of SNPs to fetch.

        Args:
            existing_db_rsids: rsids already in our database

        Returns:
            List of rsids to fetch, prioritized by clinical relevance
        """
        # SNPs in genome but not in database
        missing = self.genome_rsids - existing_db_rsids

        # Start with high-priority SNPs
        priority_1 = []
        priority_2 = []
        priority_3 = []

        for rsid in missing:
            rsid_lower = rsid.lower()

            if rsid_lower in self.HIGH_PRIORITY_SNPS or rsid in self.HIGH_PRIORITY_SNPS:
                priority_1.append(rsid)
            else:
                # Check if it's in a known gene
                # We'd need to look this up, so for now just add to lower priority
                priority_3.append(rsid)

        # Return prioritized list
        return priority_1 + priority_2 + priority_3[:500]  # Limit to 500 for now

    def filter_clinically_relevant(self, fetched_snps: List[FetchedSNP]) -> List[FetchedSNP]:
        """
        Filter fetched SNPs to only clinically relevant ones.

        Args:
            fetched_snps: List of fetched SNPs

        Returns:
            Filtered list with only clinically relevant SNPs
        """
        relevant = []

        for snp in fetched_snps:
            # Check if gene is in our clinical list
            if snp.gene and snp.gene.upper() in [g.upper() for g in ALL_CLINICAL_GENES]:
                relevant.append(snp)
                continue

            # Check if has high magnitude genotypes
            for gt, data in snp.magnitude_data.items():
                if data.get('magnitude', 0) >= 2:  # Magnitude >= 2 is significant
                    relevant.append(snp)
                    break

            # Check if has any categories
            if snp.categories:
                relevant.append(snp)

        return relevant


def load_genome_snps(filepath: str) -> Dict[str, str]:
    """Load SNPs from 23andMe format genome file"""
    snps = {}

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split('\t')
            if len(parts) >= 4:
                rsid = parts[0].lower()
                if rsid.startswith('rs'):
                    genotype = parts[3]
                    if genotype and genotype != '--':
                        snps[rsid] = genotype

    return snps


def convert_to_unified_format(snp: FetchedSNP, genotype: str) -> Optional[dict]:
    """
    Convert FetchedSNP to format compatible with UnifiedSNP.

    This creates a dict that can be used to construct a UnifiedSNP.
    """
    if not snp.gene:
        return None

    # Determine category
    from gwl_unified_database import Category

    category = Category.INFLAMMATION  # Default
    if snp.categories:
        cat_map = {
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
        for cat in snp.categories:
            if cat in cat_map:
                category = cat_map[cat]
                break

    # Build genotype effects from magnitude data
    from gwl_unified_database import RiskLevel

    genotype_effects = {}
    for gt, data in snp.magnitude_data.items():
        mag = data.get('magnitude', 0)
        repute = data.get('repute', 'neutral')
        summary = data.get('summary', '')

        # Convert magnitude to risk level
        if repute == 'good':
            risk = RiskLevel.PROTECTIVE
        elif mag >= 4:
            risk = RiskLevel.HIGH
        elif mag >= 3:
            risk = RiskLevel.SIGNIFICANTLY_INCREASED
        elif mag >= 2:
            risk = RiskLevel.MODERATELY_INCREASED
        elif mag >= 1:
            risk = RiskLevel.SLIGHTLY_INCREASED
        else:
            risk = RiskLevel.NORMAL

        genotype_effects[gt] = {
            'risk': risk,
            'effect': summary or f"Magnitude {mag}",
            'description': summary
        }

    return {
        'rsid': snp.rsid,
        'gene': snp.gene,
        'chromosome': snp.chromosome,
        'position': snp.position,
        'categories': [category],
        'genotype_effects': genotype_effects,
        'summary': snp.summary,
        'pmids': snp.references,
        'source': 'SNPedia (auto-fetched)'
    }


def main():
    """Main function for CLI usage"""
    import argparse

    parser = argparse.ArgumentParser(description='Fetch SNP data from SNPedia')
    parser.add_argument('genome_file', nargs='?', help='Path to genome file (23andMe format)')
    parser.add_argument('--rsid', help='Fetch specific rsid')
    parser.add_argument('--stats', action='store_true', help='Show cache statistics')
    parser.add_argument('--limit', type=int, default=50, help='Max SNPs to fetch (default: 50)')
    parser.add_argument('--priority-only', action='store_true', help='Only fetch high-priority SNPs')

    args = parser.parse_args()

    fetcher = SNPediaFetcher()

    if args.stats:
        stats = fetcher.get_cache_stats()
        print("\n=== SNP Cache Statistics ===")
        print(f"Total cached: {stats['total_cached']}")
        print(f"Found: {stats['found']}")
        print(f"Not found: {stats['not_found']}")
        print(f"Unique genes: {stats['unique_genes']}")
        return

    if args.rsid:
        # Fetch single SNP
        snp = fetcher.fetch_snp(args.rsid)
        if snp:
            print(f"\n=== {snp.rsid.upper()} ===")
            print(f"Gene: {snp.gene}")
            print(f"Chromosome: {snp.chromosome}")
            print(f"Position: {snp.position}")
            print(f"Summary: {snp.summary}")
            print(f"Categories: {', '.join(snp.categories) or 'None'}")
            print(f"References: {', '.join(snp.references) or 'None'}")
            print(f"\nGenotype data:")
            for gt, data in snp.magnitude_data.items():
                print(f"  {gt}: magnitude={data.get('magnitude', 0)}, "
                      f"repute={data.get('repute', 'unknown')}, "
                      f"summary={data.get('summary', 'N/A')}")
        else:
            print(f"SNP {args.rsid} not found in SNPedia")
        return

    if not args.genome_file:
        parser.print_help()
        return

    # Load genome file
    print(f"\nLoading genome file: {args.genome_file}")
    genome_snps = load_genome_snps(args.genome_file)
    print(f"Found {len(genome_snps)} SNPs in genome file")

    # Get existing database rsids
    from gwl_unified_database import get_all_rsids
    try:
        import gwl_extended_snps
    except ImportError:
        pass

    existing_rsids = set(get_all_rsids())
    print(f"Current database has {len(existing_rsids)} SNPs")

    # Prioritize SNPs to fetch
    prioritizer = ClinicalSNPPrioritizer(genome_snps)

    if args.priority_only:
        to_fetch = [rs for rs in prioritizer.HIGH_PRIORITY_SNPS
                    if rs.lower() in genome_snps and rs.lower() not in existing_rsids]
    else:
        to_fetch = prioritizer.get_priority_snps(existing_rsids)

    print(f"\nSNPs to fetch: {len(to_fetch)} (limit: {args.limit})")

    # Fetch SNPs
    fetched = []
    errors = 0

    for i, rsid in enumerate(to_fetch[:args.limit]):
        try:
            snp = fetcher.fetch_snp(rsid)
            if snp and snp.gene:
                fetched.append(snp)
                genotype = genome_snps.get(rsid.lower(), 'N/A')
                print(f"  [{i+1}/{min(len(to_fetch), args.limit)}] {rsid}: "
                      f"{snp.gene} - {len(snp.magnitude_data)} genotypes, "
                      f"your genotype: {genotype}")
        except Exception as e:
            errors += 1
            print(f"  Error fetching {rsid}: {e}")

        if (i + 1) % 10 == 0:
            fetcher._save_cache()  # Save periodically

    # Final save
    fetcher._save_cache()

    # Filter to clinically relevant
    relevant = prioritizer.filter_clinically_relevant(fetched)

    print(f"\n=== Summary ===")
    print(f"Fetched: {len(fetched)} SNPs")
    print(f"Clinically relevant: {len(relevant)} SNPs")
    print(f"Errors: {errors}")
    print(f"Cache size: {fetcher.get_cache_stats()['total_cached']}")

    # Show found SNPs
    if relevant:
        print(f"\n=== Clinically Relevant SNPs Found ===")
        for snp in relevant[:20]:
            genotype = genome_snps.get(snp.rsid.lower(), 'N/A')
            gt_info = snp.magnitude_data.get(genotype, {})
            mag = gt_info.get('magnitude', 0)
            print(f"  {snp.rsid}: {snp.gene} [{genotype}] - "
                  f"mag={mag}, categories={snp.categories}")


if __name__ == '__main__':
    main()
