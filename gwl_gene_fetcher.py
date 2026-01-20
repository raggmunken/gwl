#!/usr/bin/env python3
"""
GWL Gene Fetcher - Automatisk hämtning av gener från vetenskapliga databaser
=============================================================================

Detta skript hämtar genetisk information från:
1. NCBI dbSNP - SNP-information
2. PubMed - Vetenskapliga publikationer
3. ClinVar - Kliniska associationer

Användning:
    python gwl_gene_fetcher.py --search "vitamin D polymorphism"
    python gwl_gene_fetcher.py --rsid rs1801133
    python gwl_gene_fetcher.py --expand-database
"""

import requests
import json
import time
import re
import sys
import io
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import xml.etree.ElementTree as ET

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# NCBI API endpoints
NCBI_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
NCBI_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
NCBI_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
NCBI_ELINK = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"

# Rate limiting
REQUESTS_PER_SECOND = 3
last_request_time = 0

def rate_limit():
    """Respektera NCBI:s rate limits"""
    global last_request_time
    elapsed = time.time() - last_request_time
    if elapsed < 1/REQUESTS_PER_SECOND:
        time.sleep(1/REQUESTS_PER_SECOND - elapsed)
    last_request_time = time.time()

@dataclass
class FetchedReference:
    """En hämtad vetenskaplig referens"""
    pmid: str
    doi: str
    title: str
    journal: str
    year: int
    abstract: str
    keywords: List[str]

@dataclass
class FetchedSNP:
    """En hämtad SNP med all information"""
    rsid: str
    gene: str
    chromosome: str
    position: int
    alleles: List[str]
    minor_allele: str
    maf_european: float
    clinical_significance: str
    pubmed_ids: List[str]
    references: List[FetchedReference]

# =============================================================================
# NCBI API FUNKTIONER
# =============================================================================

def search_pubmed(query: str, max_results: int = 20) -> List[str]:
    """
    Söker i PubMed och returnerar PMIDs

    Args:
        query: Söksträngen (t.ex. "MTHFR C677T folate")
        max_results: Max antal resultat

    Returns:
        Lista med PMIDs
    """
    rate_limit()

    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance"
    }

    try:
        response = requests.get(NCBI_ESEARCH, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        return data.get("esearchresult", {}).get("idlist", [])
    except Exception as e:
        print(f"[!] PubMed sökning misslyckades: {e}")
        return []

def fetch_pubmed_articles(pmids: List[str]) -> List[FetchedReference]:
    """
    Hämtar fullständig artikelinformation från PubMed

    Args:
        pmids: Lista med PubMed IDs

    Returns:
        Lista med FetchedReference objekt
    """
    if not pmids:
        return []

    rate_limit()

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }

    try:
        response = requests.get(NCBI_EFETCH, params=params, timeout=30)
        response.raise_for_status()

        references = []
        root = ET.fromstring(response.content)

        for article in root.findall(".//PubmedArticle"):
            try:
                # PMID
                pmid_elem = article.find(".//PMID")
                pmid = pmid_elem.text if pmid_elem is not None else ""

                # Titel
                title_elem = article.find(".//ArticleTitle")
                title = title_elem.text if title_elem is not None else "Unknown title"

                # Journal
                journal_elem = article.find(".//Journal/Title")
                journal = journal_elem.text if journal_elem is not None else "Unknown journal"

                # År
                year_elem = article.find(".//PubDate/Year")
                if year_elem is None:
                    year_elem = article.find(".//PubDate/MedlineDate")
                year = int(year_elem.text[:4]) if year_elem is not None and year_elem.text else 2000

                # DOI
                doi = ""
                for article_id in article.findall(".//ArticleId"):
                    if article_id.get("IdType") == "doi":
                        doi = article_id.text or ""
                        break

                # Abstract
                abstract_parts = []
                for abstract_text in article.findall(".//AbstractText"):
                    if abstract_text.text:
                        abstract_parts.append(abstract_text.text)
                abstract = " ".join(abstract_parts)

                # Keywords
                keywords = []
                for keyword in article.findall(".//Keyword"):
                    if keyword.text:
                        keywords.append(keyword.text)

                references.append(FetchedReference(
                    pmid=pmid,
                    doi=doi,
                    title=title,
                    journal=journal,
                    year=year,
                    abstract=abstract,
                    keywords=keywords
                ))

            except Exception as e:
                print(f"[!] Kunde inte parsa artikel: {e}")
                continue

        return references

    except Exception as e:
        print(f"[!] PubMed fetch misslyckades: {e}")
        return []

def search_snp_info(rsid: str) -> Optional[Dict]:
    """
    Hämtar SNP-information från NCBI dbSNP

    Args:
        rsid: SNP identifierare (t.ex. "rs1801133")

    Returns:
        Dict med SNP-information eller None
    """
    rate_limit()

    # Rensa rsid
    rsid = rsid.lower().replace("rs", "")

    params = {
        "db": "snp",
        "term": rsid,
        "retmode": "json"
    }

    try:
        # Först söka efter SNP
        response = requests.get(NCBI_ESEARCH, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        ids = data.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return None

        # Hämta summary
        rate_limit()
        summary_params = {
            "db": "snp",
            "id": ids[0],
            "retmode": "json"
        }

        summary_response = requests.get(NCBI_ESUMMARY, params=summary_params, timeout=30)
        summary_response.raise_for_status()
        summary_data = summary_response.json()

        result = summary_data.get("result", {})
        snp_data = result.get(ids[0], {})

        return {
            "rsid": f"rs{rsid}",
            "gene": snp_data.get("genes", [{}])[0].get("name", "Unknown") if snp_data.get("genes") else "Unknown",
            "chromosome": snp_data.get("chr", "Unknown"),
            "position": snp_data.get("chrpos", 0),
            "clinical_significance": snp_data.get("clinical_significance", "not provided"),
            "maf": snp_data.get("global_maf", 0),
            "alleles": snp_data.get("docsum", "").split("/") if "/" in snp_data.get("docsum", "") else []
        }

    except Exception as e:
        print(f"[!] SNP sökning misslyckades för rs{rsid}: {e}")
        return None

def search_snps_for_topic(topic: str, max_results: int = 50) -> List[str]:
    """
    Söker efter SNPs relaterade till ett ämne via PubMed-abstracts

    Args:
        topic: Sökterm (t.ex. "vitamin D metabolism")
        max_results: Max antal resultat

    Returns:
        Lista med rsids
    """
    rate_limit()

    # Metod 1: Sök direkt i dbSNP
    params = {
        "db": "snp",
        "term": f"{topic}[All Fields] AND homo sapiens[Organism]",
        "retmax": max_results,
        "retmode": "json"
    }

    rsids = []
    try:
        response = requests.get(NCBI_ESEARCH, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        ids = data.get("esearchresult", {}).get("idlist", [])
        rsids = [f"rs{id}" for id in ids]

    except Exception as e:
        print(f"[!] dbSNP sökning misslyckades: {e}")

    # Metod 2: Om inga resultat, sök i PubMed och extrahera rsids
    if not rsids:
        print(f"      Alternativ metod: söker i PubMed...")
        pmids = search_pubmed(f"{topic} polymorphism rs", 50)
        if pmids:
            refs = fetch_pubmed_articles(pmids[:20])
            for ref in refs:
                # Extrahera rsids från abstract
                found = re.findall(r'rs\d{4,12}', ref.abstract.lower())
                rsids.extend(found)
            rsids = list(set(rsids))[:max_results]

    return rsids

def get_snp_pubmed_links(rsid: str) -> List[str]:
    """
    Hämtar PubMed-artiklar länkade till en SNP

    Args:
        rsid: SNP identifierare

    Returns:
        Lista med PMIDs
    """
    rate_limit()

    rsid_num = rsid.lower().replace("rs", "")

    # Först hämta SNP UID
    params = {
        "db": "snp",
        "term": rsid_num,
        "retmode": "json"
    }

    try:
        response = requests.get(NCBI_ESEARCH, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        snp_ids = data.get("esearchresult", {}).get("idlist", [])
        if not snp_ids:
            return []

        # Hämta länkade PubMed-artiklar
        rate_limit()
        link_params = {
            "dbfrom": "snp",
            "db": "pubmed",
            "id": snp_ids[0],
            "retmode": "json"
        }

        link_response = requests.get(NCBI_ELINK, params=link_params, timeout=30)
        link_response.raise_for_status()
        link_data = link_response.json()

        pmids = []
        linksets = link_data.get("linksets", [])
        for linkset in linksets:
            for linksetdb in linkset.get("linksetdbs", []):
                if linksetdb.get("dbto") == "pubmed":
                    pmids.extend([str(id) for id in linksetdb.get("links", [])])

        return pmids[:20]  # Max 20 artiklar

    except Exception as e:
        print(f"[!] SNP-PubMed länkning misslyckades för {rsid}: {e}")
        return []

# =============================================================================
# WELLNESS-SPECIFIKA SÖKNINGAR
# =============================================================================

# Kända wellness SNPs - dessa är verifierade i forskningen
KNOWN_WELLNESS_SNPS = {
    "vitamin_d": [
        "rs2228570",   # VDR FokI
        "rs1544410",   # VDR BsmI
        "rs731236",    # VDR TaqI
        "rs10741657",  # CYP2R1
        "rs12785878",  # DHCR7
        "rs2282679",   # GC (vitamin D binding protein)
    ],
    "methylation": [
        "rs1801133",   # MTHFR C677T
        "rs1801131",   # MTHFR A1298C
        "rs1805087",   # MTR A2756G
        "rs1801394",   # MTRR A66G
        "rs602662",    # FUT2 secretor
    ],
    "omega3": [
        "rs174546",    # FADS1
        "rs174547",    # FADS1
        "rs1535",      # FADS2
        "rs174575",    # FADS2
    ],
    "stress_mood": [
        "rs4680",      # COMT Val158Met
        "rs6265",      # BDNF Val66Met
    ],
    "sleep": [
        "rs1801260",   # CLOCK
        "rs73598374",  # ADA
    ],
    "caffeine": [
        "rs762551",    # CYP1A2
        "rs4410790",   # AHR
    ],
    "alcohol": [
        "rs1229984",   # ADH1B
        "rs671",       # ALDH2
    ],
    "weight": [
        "rs9939609",   # FTO
        "rs17782313",  # MC4R
    ],
    "cardiovascular": [
        "rs429358",    # APOE e4
        "rs7412",      # APOE e2
        "rs1333049",   # 9p21
    ],
    "inflammation": [
        "rs1800795",   # IL6
        "rs1800629",   # TNF
    ],
    "exercise": [
        "rs1815739",   # ACTN3
        "rs8192678",   # PPARGC1A
    ],
    "detox": [
        "rs1695",      # GSTP1
        "rs1050450",   # GPX1
        "rs4880",      # SOD2
    ],
    "iron": [
        "rs1800562",   # HFE C282Y
        "rs1799945",   # HFE H63D
    ],
    "insulin": [
        "rs7903146",   # TCF7L2
    ],
    "lactose": [
        "rs4988235",   # LCT
    ],
    "gluten": [
        "rs2187668",   # HLA-DQ2.5
    ],
    "longevity": [
        "rs2802292",   # FOXO3
    ],
    "thyroid": [
        "rs965513",    # FOXE1
    ],
    "histamine": [
        "rs1049793",   # DAO
    ],
}

# Predefinerade kategorier för wellness-gener (för topic-baserad sökning)
WELLNESS_CATEGORIES = {
    "vitamin_d": [
        "VDR vitamin D receptor polymorphism",
        "CYP2R1 vitamin D metabolism",
        "CYP27B1 vitamin D activation",
        "GC vitamin D binding protein"
    ],
    "methylation": [
        "MTHFR folate metabolism",
        "MTR methionine synthase",
        "MTRR methionine synthase reductase",
        "BHMT betaine homocysteine"
    ],
    "omega3": [
        "FADS1 fatty acid desaturase",
        "FADS2 delta 6 desaturase",
        "ELOVL fatty acid elongation"
    ],
    "stress_mood": [
        "COMT catechol-O-methyltransferase",
        "BDNF brain derived neurotrophic factor",
        "SLC6A4 serotonin transporter",
        "MAOA monoamine oxidase"
    ],
    "sleep": [
        "CLOCK circadian rhythm",
        "PER2 period circadian",
        "ADA adenosine deaminase sleep"
    ],
    "caffeine": [
        "CYP1A2 caffeine metabolism",
        "ADORA2A adenosine receptor caffeine"
    ],
    "weight": [
        "FTO obesity gene",
        "MC4R melanocortin receptor appetite",
        "PPARG peroxisome metabolism"
    ],
    "inflammation": [
        "IL6 interleukin inflammation",
        "TNF tumor necrosis factor",
        "CRP C-reactive protein genetic"
    ],
    "cardiovascular": [
        "APOE apolipoprotein cholesterol",
        "9p21 coronary heart disease",
        "LPA lipoprotein cardiovascular"
    ],
    "detox": [
        "GSTP1 glutathione detoxification",
        "GPX1 glutathione peroxidase",
        "SOD2 superoxide dismutase"
    ],
    "exercise": [
        "ACTN3 muscle fiber type",
        "PPARGC1A endurance exercise",
        "ACE angiotensin exercise performance"
    ],
    "insulin": [
        "TCF7L2 diabetes risk",
        "SLC30A8 zinc transporter diabetes",
        "PPARG insulin sensitivity"
    ],
    "iron": [
        "HFE hemochromatosis iron",
        "TFR2 transferrin receptor iron"
    ],
    "lactose": [
        "LCT lactase persistence",
        "MCM6 lactose tolerance"
    ]
}

def fetch_known_snps_for_category(category: str) -> Dict[str, Dict]:
    """
    Hämtar information för kända SNPs i en kategori

    Args:
        category: Kategorinamn från KNOWN_WELLNESS_SNPS

    Returns:
        Dict med rsid -> geninfo
    """
    if category not in KNOWN_WELLNESS_SNPS:
        print(f"[!] Okänd kategori: {category}")
        print(f"    Tillgängliga: {', '.join(KNOWN_WELLNESS_SNPS.keys())}")
        return {}

    results = {}
    rsids = KNOWN_WELLNESS_SNPS[category]

    print(f"\n[*] Hämtar {len(rsids)} kända SNPs för kategori: {category}")

    for rsid in rsids:
        print(f"    Hämtar {rsid}...")
        snp_info = deep_fetch_snp(rsid)
        if snp_info:
            snp_info["category"] = category
            results[rsid] = snp_info
        time.sleep(0.5)

    return results

def fetch_all_known_snps() -> Dict[str, Dict]:
    """
    Hämtar information för ALLA kända wellness SNPs

    Returns:
        Dict med rsid -> geninfo
    """
    all_genes = {}

    for category in KNOWN_WELLNESS_SNPS:
        print(f"\n{'='*50}")
        print(f"KATEGORI: {category.upper()}")
        print(f"{'='*50}")
        genes = fetch_known_snps_for_category(category)
        all_genes.update(genes)
        print(f"[+] {category}: {len(genes)} gener hämtade")
        time.sleep(1)

    return all_genes

def fetch_wellness_genes_for_category(category: str, max_per_search: int = 10) -> Dict[str, Dict]:
    """
    Hämtar gener för en specifik wellness-kategori

    Args:
        category: Kategorinamn från WELLNESS_CATEGORIES
        max_per_search: Max SNPs per sökning

    Returns:
        Dict med rsid -> geninfo
    """
    if category not in WELLNESS_CATEGORIES:
        print(f"[!] Okänd kategori: {category}")
        return {}

    results = {}
    search_terms = WELLNESS_CATEGORIES[category]

    print(f"\n[*] Hämtar gener för kategori: {category}")

    for term in search_terms:
        print(f"    Söker: {term}")

        # Sök SNPs
        rsids = search_snps_for_topic(term, max_per_search)

        for rsid in rsids[:5]:  # Max 5 per sökterm
            if rsid in results:
                continue

            print(f"      Hämtar info för {rsid}...")

            # Hämta SNP-info
            snp_info = search_snp_info(rsid)
            if not snp_info:
                continue

            # Hämta relaterade PubMed-artiklar
            pmids = get_snp_pubmed_links(rsid)
            if pmids:
                references = fetch_pubmed_articles(pmids[:5])  # Max 5 artiklar
            else:
                # Alternativ: Sök direkt på rsid + gen
                search_query = f"{rsid} {snp_info.get('gene', '')}"
                pmids = search_pubmed(search_query, 5)
                references = fetch_pubmed_articles(pmids)

            snp_info["references"] = references
            snp_info["category"] = category
            results[rsid] = snp_info

            time.sleep(0.5)  # Extra rate limiting

    return results

def fetch_all_wellness_genes() -> Dict[str, Dict]:
    """
    Hämtar gener för alla wellness-kategorier

    Returns:
        Dict med rsid -> geninfo för alla kategorier
    """
    all_genes = {}

    for category in WELLNESS_CATEGORIES:
        genes = fetch_wellness_genes_for_category(category)
        all_genes.update(genes)
        print(f"[+] Kategori {category}: {len(genes)} gener hämtade")
        time.sleep(1)  # Paus mellan kategorier

    return all_genes

# =============================================================================
# DATABAS-GENERERING
# =============================================================================

def generate_database_entry(rsid: str, snp_info: Dict) -> str:
    """
    Genererar en Python-kodrad för gendatabasen

    Args:
        rsid: SNP identifierare
        snp_info: Dict med SNP-information

    Returns:
        Python-kod för GeneVariant
    """
    gene = snp_info.get("gene", "Unknown")
    chromosome = snp_info.get("chromosome", "?")
    clinical = snp_info.get("clinical_significance", "")
    category = snp_info.get("category", "other")
    references = snp_info.get("references", [])

    # Skapa referens-strängar
    ref_strings = []
    for ref in references[:3]:  # Max 3 referenser
        ref_str = f'''Reference(
            pmid="{ref.pmid}",
            doi="{ref.doi}",
            title="{ref.title[:100]}...",
            journal="{ref.journal}",
            year={ref.year},
            finding="Se abstrakt för detaljer"
        )'''
        ref_strings.append(ref_str)

    refs_code = ",\n            ".join(ref_strings) if ref_strings else "# Inga referenser hämtade"

    # Mappa kategori
    category_map = {
        "vitamin_d": "Category.VITAMIN_D",
        "methylation": "Category.VITAMIN_B",
        "omega3": "Category.OMEGA3",
        "stress_mood": "Category.STRESS",
        "sleep": "Category.SLEEP",
        "caffeine": "Category.CAFFEINE",
        "weight": "Category.WEIGHT",
        "inflammation": "Category.INFLAMMATION",
        "cardiovascular": "Category.CARDIOVASCULAR",
        "detox": "Category.DETOX",
        "exercise": "Category.EXERCISE_POWER",
        "insulin": "Category.INSULIN",
        "iron": "Category.IRON",
        "lactose": "Category.LACTOSE"
    }
    cat_code = category_map.get(category, "Category.OTHER")

    entry = f'''
    # ---- {gene} {rsid} ----
    # Autogenererad - behöver manuell granskning
    GeneVariant(
        rsid="{rsid}",
        gene="{gene}",
        name="{gene} variant",
        chromosome="{chromosome}",
        category={cat_code},
        evidence_level=EvidenceLevel.PRELIMINARY,  # GRANSKA
        risk_allele="?",  # FYLL I
        protective_allele="?",  # FYLL I
        frequency_eur=0.0,  # FYLL I
        description="Autogenererad. {clinical}",
        clinical_significance="{clinical}",
        recommendation="Behöver manuell granskning av litteraturen.",
        references=[
            {refs_code}
        ],
        genotype_effects={{
            # FYLL I GENOTYP-EFFEKTER
        }}
    ),'''

    return entry

def export_to_json(genes: Dict[str, Dict], filepath: str):
    """
    Exporterar hämtade gener till JSON för vidare bearbetning

    Args:
        genes: Dict med rsid -> geninfo
        filepath: Sökväg till output-fil
    """
    # Konvertera references till dict
    export_data = {}
    for rsid, info in genes.items():
        export_info = info.copy()
        if "references" in export_info:
            export_info["references"] = [asdict(ref) for ref in export_info["references"]]
        export_data[rsid] = export_info

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"[+] Exporterat {len(genes)} gener till {filepath}")

def generate_database_file(genes: Dict[str, Dict], filepath: str):
    """
    Genererar en Python-databasfil med alla gener

    Args:
        genes: Dict med rsid -> geninfo
        filepath: Sökväg till output-fil
    """
    header = '''#!/usr/bin/env python3
"""
GWL Autogenererad Gendatabas
=============================
Genererad av gwl_gene_fetcher.py

VIKTIGT: Denna fil behöver manuell granskning!
- Verifiera alla gener mot primärkällor
- Fyll i risk_allele och protective_allele
- Fyll i genotype_effects
- Justera evidensnivåer
"""

from gwl_gene_database import GeneVariant, Reference, Category, EvidenceLevel

# Autogenererade gener - BEHÖVER GRANSKNING
AUTO_GENERATED_GENES = [
'''

    entries = []
    for rsid, info in genes.items():
        entries.append(generate_database_entry(rsid, info))

    footer = '''
]

if __name__ == "__main__":
    print(f"Autogenererade gener: {len(AUTO_GENERATED_GENES)}")
'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write("\n".join(entries))
        f.write(footer)

    print(f"[+] Genererat databasfil: {filepath}")

# =============================================================================
# SPECIFIK SNP-SÖKNING MED DETALJERAD INFO
# =============================================================================

def deep_fetch_snp(rsid: str) -> Optional[Dict]:
    """
    Hämtar detaljerad information för en specifik SNP

    Args:
        rsid: SNP identifierare

    Returns:
        Dict med all tillgänglig information
    """
    print(f"\n[*] Djuphämtning för {rsid}...")

    # 1. Grundläggande SNP-info
    snp_info = search_snp_info(rsid)
    if not snp_info:
        print(f"[!] Kunde inte hitta {rsid}")
        return None

    print(f"    Gen: {snp_info.get('gene', 'Unknown')}")
    print(f"    Kromosom: {snp_info.get('chromosome', 'Unknown')}")

    # 2. Länkade PubMed-artiklar
    pmids = get_snp_pubmed_links(rsid)
    print(f"    Länkade artiklar: {len(pmids)}")

    if not pmids:
        # Alternativ sökning
        gene = snp_info.get("gene", "")
        if gene:
            search_query = f'"{rsid}" OR ("{gene}" AND polymorphism)'
            pmids = search_pubmed(search_query, 20)
            print(f"    Alternativ sökning: {len(pmids)} artiklar")

    # 3. Hämta artikeldetaljer
    references = fetch_pubmed_articles(pmids[:10])
    snp_info["references"] = references

    # 4. Analysera abstracts för att hitta nyckelinformation
    keywords_found = set()
    for ref in references:
        abstract_lower = ref.abstract.lower()

        # Leta efter vanliga mönster
        patterns = [
            r"risk allele[:\s]+([ACTG])",
            r"([ACTG])\s+allele.*(?:risk|associated)",
            r"minor allele[:\s]+([ACTG])",
            r"([ACTG])/([ACTG])\s+polymorphism"
        ]

        for pattern in patterns:
            matches = re.findall(pattern, abstract_lower)
            for match in matches:
                if isinstance(match, tuple):
                    keywords_found.update(match)
                else:
                    keywords_found.add(match)

        # Samla nyckelord
        for kw in ref.keywords:
            keywords_found.add(kw.lower())

    snp_info["extracted_alleles"] = list(keywords_found)

    print(f"    Extraherade nyckelord: {list(keywords_found)[:10]}")

    return snp_info

# =============================================================================
# MAIN / CLI
# =============================================================================

def print_usage():
    """Skriver ut användningsinstruktioner"""
    print("""
GWL Gene Fetcher - Automatisk hämtning av genetisk information
==============================================================

Användning:
    python gwl_gene_fetcher.py [kommando] [argument]

Kommandon:
    --rsid <rsid>           Hämta detaljerad info för en specifik SNP
                            Exempel: --rsid rs1801133

    --search <term>         Sök efter SNPs relaterade till ett ämne
                            Exempel: --search "vitamin D metabolism"

    --category <cat>        Hämta alla SNPs i en kategori
                            Kategorier: vitamin_d, methylation, omega3,
                            stress_mood, sleep, caffeine, weight,
                            inflammation, cardiovascular, detox,
                            exercise, insulin, iron, lactose

    --expand-database       Hämta SNPs för ALLA kategorier
                            (tar lång tid, ~30-60 min)

    --export <format>       Exportformat: json (default) eller python

    --output <filepath>     Output-fil (default: gwl_fetched_genes.json)

Exempel:
    python gwl_gene_fetcher.py --rsid rs1801133
    python gwl_gene_fetcher.py --category vitamin_d --output vitamin_d_genes.json
    python gwl_gene_fetcher.py --search "caffeine metabolism" --export python
    python gwl_gene_fetcher.py --expand-database

Notera:
    - NCBI rate limits: max 3 requests/sekund utan API-nyckel
    - För snabbare hämtning, skaffa NCBI API-nyckel
    - Autogenererade gener behöver ALLTID manuell granskning
""")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="GWL Gene Fetcher")
    parser.add_argument("--rsid", type=str, help="Hämta specifik SNP")
    parser.add_argument("--search", type=str, help="Sök SNPs efter term")
    parser.add_argument("--category", type=str, help="Hämta SNPs för kategori (topic-baserad)")
    parser.add_argument("--known", type=str, help="Hämta kända SNPs för kategori (snabbare)")
    parser.add_argument("--known-all", action="store_true", help="Hämta alla kända wellness SNPs")
    parser.add_argument("--expand-database", action="store_true", help="Hämta alla kategorier (topic-baserad)")
    parser.add_argument("--export", type=str, default="json", help="Exportformat: json eller python")
    parser.add_argument("--output", type=str, default="gwl_fetched_genes.json", help="Output-fil")
    parser.add_argument("--list-categories", action="store_true", help="Lista alla kategorier")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        print_usage()
        return

    # Lista kategorier
    if args.list_categories:
        print("\n[*] Tillgängliga kategorier (kända SNPs):")
        for cat, snps in KNOWN_WELLNESS_SNPS.items():
            print(f"    {cat}: {len(snps)} SNPs")
        return

    genes = {}

    # Hämta specifik SNP
    if args.rsid:
        snp_info = deep_fetch_snp(args.rsid)
        if snp_info:
            genes[args.rsid] = snp_info
            print(f"\n[+] Hämtade info för {args.rsid}")
            print(f"    Gen: {snp_info.get('gene')}")
            print(f"    Referenser: {len(snp_info.get('references', []))}")

    # Sök efter term
    elif args.search:
        print(f"\n[*] Söker SNPs för: {args.search}")
        rsids = search_snps_for_topic(args.search, 20)
        print(f"[+] Hittade {len(rsids)} SNPs")

        for rsid in rsids[:10]:
            snp_info = deep_fetch_snp(rsid)
            if snp_info:
                genes[rsid] = snp_info

    # Hämta kända SNPs för kategori (REKOMMENDERAT)
    elif args.known:
        genes = fetch_known_snps_for_category(args.known)

    # Hämta ALLA kända SNPs
    elif args.known_all:
        print("\n[*] Hämtar ALLA kända wellness SNPs...")
        total_snps = sum(len(snps) for snps in KNOWN_WELLNESS_SNPS.values())
        print(f"[*] Totalt {total_snps} SNPs att hämta...")
        genes = fetch_all_known_snps()

    # Hämta kategori (topic-baserad, mindre tillförlitlig)
    elif args.category:
        genes = fetch_wellness_genes_for_category(args.category)

    # Expandera databas
    elif args.expand_database:
        print("\n[*] Hämtar alla wellness-kategorier...")
        print("[!] Detta tar lång tid (30-60 minuter)")
        genes = fetch_all_wellness_genes()

    # Exportera
    if genes:
        if args.export == "json":
            export_to_json(genes, args.output)
        elif args.export == "python":
            output_py = args.output.replace(".json", ".py")
            generate_database_file(genes, output_py)

        print(f"\n[+] Totalt {len(genes)} gener hämtade")
        print(f"[!] Kom ihåg: Autogenererade data behöver MANUELL GRANSKNING")

if __name__ == "__main__":
    main()
