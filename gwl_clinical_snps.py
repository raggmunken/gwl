#!/usr/bin/env python3
"""
GWL Clinical SNPs Master List
=============================
Comprehensive list of clinically significant SNPs for nutrigenomics.

This is a curated list of SNPs with known health/nutrition implications.
Source: SNPedia, PharmGKB, ClinVar, GWAS Catalog, published literature.

Genetic Wellness Labs - Nutrigenomics Platform
"""

# =============================================================================
# MASTER LIST OF CLINICALLY RELEVANT SNPs
# =============================================================================
# Format: rsid -> {gene, category, importance, notes}
# Importance: 1 = Critical, 2 = High, 3 = Moderate, 4 = Low

CLINICAL_SNPS = {
    # =========================================================================
    # PHARMACOGENOMICS - Drug metabolism (CRITICAL for safety)
    # =========================================================================

    # CYP2D6 - Codeine, antidepressants, tamoxifen, many others
    "rs3892097": {"gene": "CYP2D6", "category": "pharmacogenomics", "importance": 1, "notes": "*4 allele - no function"},
    "rs1065852": {"gene": "CYP2D6", "category": "pharmacogenomics", "importance": 1, "notes": "*10 allele - reduced"},
    "rs16947": {"gene": "CYP2D6", "category": "pharmacogenomics", "importance": 2, "notes": "*2 allele"},
    "rs1135840": {"gene": "CYP2D6", "category": "pharmacogenomics", "importance": 2, "notes": "Activity marker"},
    "rs28371725": {"gene": "CYP2D6", "category": "pharmacogenomics", "importance": 2, "notes": "*41 allele"},

    # CYP2C19 - Clopidogrel, PPIs, antidepressants
    "rs4244285": {"gene": "CYP2C19", "category": "pharmacogenomics", "importance": 1, "notes": "*2 allele - no function"},
    "rs4986893": {"gene": "CYP2C19", "category": "pharmacogenomics", "importance": 1, "notes": "*3 allele - no function"},
    "rs12248560": {"gene": "CYP2C19", "category": "pharmacogenomics", "importance": 1, "notes": "*17 allele - rapid"},
    "rs28399504": {"gene": "CYP2C19", "category": "pharmacogenomics", "importance": 2, "notes": "*4 allele"},

    # CYP2C9 - Warfarin, NSAIDs, sulfonylureas
    "rs1799853": {"gene": "CYP2C9", "category": "pharmacogenomics", "importance": 1, "notes": "*2 allele - reduced"},
    "rs1057910": {"gene": "CYP2C9", "category": "pharmacogenomics", "importance": 1, "notes": "*3 allele - reduced"},
    "rs7900194": {"gene": "CYP2C9", "category": "pharmacogenomics", "importance": 2, "notes": "*8 allele"},

    # CYP3A4/5 - Statins, immunosuppressants, many drugs
    "rs2740574": {"gene": "CYP3A4", "category": "pharmacogenomics", "importance": 2, "notes": "*1B allele"},
    "rs35599367": {"gene": "CYP3A4", "category": "pharmacogenomics", "importance": 2, "notes": "*22 allele - reduced"},
    "rs776746": {"gene": "CYP3A5", "category": "pharmacogenomics", "importance": 2, "notes": "*3 allele"},

    # CYP1A2 - Caffeine, theophylline, clozapine
    "rs762551": {"gene": "CYP1A2", "category": "caffeine", "importance": 2, "notes": "*1F allele - inducible"},
    "rs2069514": {"gene": "CYP1A2", "category": "caffeine", "importance": 3, "notes": "*1C allele"},

    # VKORC1 - Warfarin sensitivity
    "rs9923231": {"gene": "VKORC1", "category": "pharmacogenomics", "importance": 1, "notes": "Warfarin sensitivity"},
    "rs9934438": {"gene": "VKORC1", "category": "pharmacogenomics", "importance": 2, "notes": "Warfarin dose"},

    # SLCO1B1 - Statin myopathy risk
    "rs4149056": {"gene": "SLCO1B1", "category": "pharmacogenomics", "importance": 1, "notes": "*5 allele - statin risk"},
    "rs2306283": {"gene": "SLCO1B1", "category": "pharmacogenomics", "importance": 2, "notes": "*1B allele"},

    # DPYD - 5-FU toxicity (cancer treatment)
    "rs3918290": {"gene": "DPYD", "category": "pharmacogenomics", "importance": 1, "notes": "*2A - 5-FU toxicity"},
    "rs67376798": {"gene": "DPYD", "category": "pharmacogenomics", "importance": 1, "notes": "5-FU toxicity"},
    "rs55886062": {"gene": "DPYD", "category": "pharmacogenomics", "importance": 1, "notes": "*13 allele"},

    # TPMT - Thiopurine toxicity
    "rs1800462": {"gene": "TPMT", "category": "pharmacogenomics", "importance": 1, "notes": "*2 allele"},
    "rs1800460": {"gene": "TPMT", "category": "pharmacogenomics", "importance": 1, "notes": "*3B allele"},
    "rs1142345": {"gene": "TPMT", "category": "pharmacogenomics", "importance": 1, "notes": "*3C allele"},

    # UGT1A1 - Irinotecan toxicity
    "rs8175347": {"gene": "UGT1A1", "category": "pharmacogenomics", "importance": 2, "notes": "*28 allele"},

    # NAT2 - Isoniazid, sulfonamides
    "rs1801280": {"gene": "NAT2", "category": "pharmacogenomics", "importance": 2, "notes": "Slow acetylator"},
    "rs1799930": {"gene": "NAT2", "category": "pharmacogenomics", "importance": 2, "notes": "Slow acetylator"},
    "rs1799931": {"gene": "NAT2", "category": "pharmacogenomics", "importance": 2, "notes": "Slow acetylator"},
    "rs1041983": {"gene": "NAT2", "category": "pharmacogenomics", "importance": 3, "notes": "Acetylator status"},

    # =========================================================================
    # METHYLATION & B-VITAMINS
    # =========================================================================

    # MTHFR - Folate metabolism
    "rs1801133": {"gene": "MTHFR", "category": "methylation", "importance": 1, "notes": "C677T - major variant"},
    "rs1801131": {"gene": "MTHFR", "category": "methylation", "importance": 2, "notes": "A1298C - secondary"},

    # MTR - B12 dependent methionine synthase
    "rs1805087": {"gene": "MTR", "category": "methylation", "importance": 2, "notes": "A2756G"},

    # MTRR - MTR reductase
    "rs1801394": {"gene": "MTRR", "category": "methylation", "importance": 2, "notes": "A66G"},
    "rs10380": {"gene": "MTRR", "category": "methylation", "importance": 3, "notes": "Secondary variant"},

    # BHMT - Betaine-homocysteine methyltransferase
    "rs3733890": {"gene": "BHMT", "category": "methylation", "importance": 3, "notes": "R239Q"},
    "rs567754": {"gene": "BHMT", "category": "methylation", "importance": 3, "notes": "Secondary variant"},

    # CBS - Cystathionine beta-synthase
    "rs234706": {"gene": "CBS", "category": "methylation", "importance": 2, "notes": "C699T"},
    "rs2851391": {"gene": "CBS", "category": "methylation", "importance": 3, "notes": "Secondary"},

    # COMT - Catechol-O-methyltransferase
    "rs4680": {"gene": "COMT", "category": "stress", "importance": 1, "notes": "Val158Met - warrior/worrier"},
    "rs4633": {"gene": "COMT", "category": "stress", "importance": 3, "notes": "H62H"},
    "rs6269": {"gene": "COMT", "category": "stress", "importance": 3, "notes": "Haplotype marker"},

    # MAO-A - Monoamine oxidase A
    "rs6323": {"gene": "MAOA", "category": "stress", "importance": 2, "notes": "Activity variant"},

    # TCN2 - B12 transport
    "rs1801198": {"gene": "TCN2", "category": "methylation", "importance": 2, "notes": "C776G"},

    # FUT2 - B12 absorption
    "rs601338": {"gene": "FUT2", "category": "methylation", "importance": 2, "notes": "Non-secretor status"},
    "rs602662": {"gene": "FUT2", "category": "methylation", "importance": 3, "notes": "Secondary"},

    # =========================================================================
    # VITAMIN D
    # =========================================================================

    # VDR - Vitamin D receptor
    "rs2228570": {"gene": "VDR", "category": "vitamin_d", "importance": 2, "notes": "FokI - receptor function"},
    "rs1544410": {"gene": "VDR", "category": "vitamin_d", "importance": 2, "notes": "BsmI"},
    "rs731236": {"gene": "VDR", "category": "vitamin_d", "importance": 2, "notes": "TaqI"},
    "rs7975232": {"gene": "VDR", "category": "vitamin_d", "importance": 3, "notes": "ApaI"},

    # CYP2R1 - 25-hydroxylation
    "rs10741657": {"gene": "CYP2R1", "category": "vitamin_d", "importance": 2, "notes": "25-OH-D levels"},
    "rs12794714": {"gene": "CYP2R1", "category": "vitamin_d", "importance": 2, "notes": "25-OH-D levels"},

    # CYP27B1 - 1-alpha hydroxylation
    "rs10877012": {"gene": "CYP27B1", "category": "vitamin_d", "importance": 2, "notes": "1,25-OH-D production"},

    # GC - Vitamin D binding protein
    "rs2282679": {"gene": "GC", "category": "vitamin_d", "importance": 2, "notes": "D transport"},
    "rs4588": {"gene": "GC", "category": "vitamin_d", "importance": 2, "notes": "D binding"},
    "rs7041": {"gene": "GC", "category": "vitamin_d", "importance": 2, "notes": "D binding"},

    # =========================================================================
    # OMEGA-3 / FAT METABOLISM
    # =========================================================================

    # FADS1/2 - Fatty acid desaturase
    "rs174546": {"gene": "FADS1", "category": "omega3", "importance": 2, "notes": "LC-PUFA synthesis"},
    "rs174547": {"gene": "FADS1", "category": "omega3", "importance": 2, "notes": "LC-PUFA synthesis"},
    "rs174548": {"gene": "FADS1", "category": "omega3", "importance": 3, "notes": "LC-PUFA synthesis"},
    "rs174553": {"gene": "FADS1", "category": "omega3", "importance": 3, "notes": "LC-PUFA synthesis"},
    "rs174556": {"gene": "FADS1", "category": "omega3", "importance": 3, "notes": "LC-PUFA synthesis"},
    "rs1535": {"gene": "FADS2", "category": "omega3", "importance": 2, "notes": "LC-PUFA synthesis"},
    "rs174583": {"gene": "FADS2", "category": "omega3", "importance": 3, "notes": "LC-PUFA synthesis"},

    # ELOVL2 - Fatty acid elongation
    "rs953413": {"gene": "ELOVL2", "category": "omega3", "importance": 3, "notes": "DHA synthesis"},

    # PPARG - Fat storage
    "rs1801282": {"gene": "PPARG", "category": "metabolism", "importance": 2, "notes": "Pro12Ala"},

    # APOE - Lipid metabolism
    "rs429358": {"gene": "APOE", "category": "cardiovascular", "importance": 1, "notes": "APOE4 marker 1"},
    "rs7412": {"gene": "APOE", "category": "cardiovascular", "importance": 1, "notes": "APOE4 marker 2"},

    # CETP - HDL metabolism
    "rs708272": {"gene": "CETP", "category": "cardiovascular", "importance": 2, "notes": "TaqIB"},
    "rs5882": {"gene": "CETP", "category": "cardiovascular", "importance": 3, "notes": "I405V"},

    # LPL - Triglyceride metabolism
    "rs328": {"gene": "LPL", "category": "cardiovascular", "importance": 2, "notes": "S447X - protective"},
    "rs320": {"gene": "LPL", "category": "cardiovascular", "importance": 3, "notes": "HindIII"},

    # PCSK9 - LDL metabolism
    "rs11591147": {"gene": "PCSK9", "category": "cardiovascular", "importance": 2, "notes": "R46L - protective"},

    # =========================================================================
    # VITAMIN A / CAROTENOIDS
    # =========================================================================

    # BCMO1/BCO1 - Beta-carotene conversion
    "rs12934922": {"gene": "BCO1", "category": "vitamin_a", "importance": 2, "notes": "A379V - reduced conversion"},
    "rs7501331": {"gene": "BCO1", "category": "vitamin_a", "importance": 2, "notes": "R267S - reduced conversion"},
    "rs6564851": {"gene": "BCO1", "category": "vitamin_a", "importance": 3, "notes": "Promoter variant"},

    # =========================================================================
    # IRON METABOLISM
    # =========================================================================

    # HFE - Hemochromatosis
    "rs1800562": {"gene": "HFE", "category": "iron", "importance": 1, "notes": "C282Y - hemochromatosis"},
    "rs1799945": {"gene": "HFE", "category": "iron", "importance": 2, "notes": "H63D"},
    "rs1800730": {"gene": "HFE", "category": "iron", "importance": 3, "notes": "S65C"},

    # TF - Transferrin
    "rs3811647": {"gene": "TF", "category": "iron", "importance": 3, "notes": "Iron levels"},

    # TMPRSS6 - Iron regulation
    "rs855791": {"gene": "TMPRSS6", "category": "iron", "importance": 2, "notes": "Iron levels"},
    "rs4820268": {"gene": "TMPRSS6", "category": "iron", "importance": 3, "notes": "Iron levels"},

    # =========================================================================
    # DETOXIFICATION
    # =========================================================================

    # Phase I
    "rs1056836": {"gene": "CYP1B1", "category": "detox", "importance": 2, "notes": "L432V"},
    "rs1048943": {"gene": "CYP1A1", "category": "detox", "importance": 2, "notes": "I462V"},
    "rs4646903": {"gene": "CYP1A1", "category": "detox", "importance": 3, "notes": "MspI"},

    # Phase II - Glutathione
    "rs1695": {"gene": "GSTP1", "category": "detox", "importance": 2, "notes": "I105V"},
    "rs1138272": {"gene": "GSTP1", "category": "detox", "importance": 3, "notes": "A114V"},
    # GSTM1/T1 - Copy number variations, harder to detect

    # NQO1 - Quinone reductase
    "rs1800566": {"gene": "NQO1", "category": "detox", "importance": 2, "notes": "*2 allele - no function"},
    "rs10517": {"gene": "NQO1", "category": "detox", "importance": 3, "notes": "*3 allele"},

    # SOD2 - Superoxide dismutase
    "rs4880": {"gene": "SOD2", "category": "antioxidant", "importance": 2, "notes": "A16V - mitochondrial"},

    # CAT - Catalase
    "rs1001179": {"gene": "CAT", "category": "antioxidant", "importance": 3, "notes": "C-262T"},

    # GPX1 - Glutathione peroxidase
    "rs1050450": {"gene": "GPX1", "category": "antioxidant", "importance": 3, "notes": "Pro198Leu"},

    # PON1 - Paraoxonase
    "rs662": {"gene": "PON1", "category": "detox", "importance": 2, "notes": "Q192R"},
    "rs854560": {"gene": "PON1", "category": "detox", "importance": 3, "notes": "L55M"},

    # =========================================================================
    # INFLAMMATION
    # =========================================================================

    # IL-6
    "rs1800795": {"gene": "IL6", "category": "inflammation", "importance": 2, "notes": "G-174C"},
    "rs1800796": {"gene": "IL6", "category": "inflammation", "importance": 3, "notes": "G-572C"},

    # TNF-alpha
    "rs1800629": {"gene": "TNF", "category": "inflammation", "importance": 2, "notes": "G-308A"},
    "rs361525": {"gene": "TNF", "category": "inflammation", "importance": 3, "notes": "G-238A"},

    # IL-1 beta
    "rs16944": {"gene": "IL1B", "category": "inflammation", "importance": 2, "notes": "C-511T"},
    "rs1143634": {"gene": "IL1B", "category": "inflammation", "importance": 3, "notes": "C+3953T"},

    # CRP
    "rs1205": {"gene": "CRP", "category": "inflammation", "importance": 2, "notes": "CRP levels"},
    "rs3093077": {"gene": "CRP", "category": "inflammation", "importance": 3, "notes": "CRP levels"},

    # IL-10
    "rs1800896": {"gene": "IL10", "category": "inflammation", "importance": 3, "notes": "G-1082A"},

    # =========================================================================
    # BLOOD SUGAR / DIABETES
    # =========================================================================

    # TCF7L2 - Strongest diabetes gene
    "rs7903146": {"gene": "TCF7L2", "category": "diabetes", "importance": 1, "notes": "Strongest T2D risk"},
    "rs12255372": {"gene": "TCF7L2", "category": "diabetes", "importance": 2, "notes": "T2D risk"},

    # KCNJ11 - Insulin secretion
    "rs5219": {"gene": "KCNJ11", "category": "diabetes", "importance": 2, "notes": "E23K"},

    # PPARG
    "rs1801282": {"gene": "PPARG", "category": "diabetes", "importance": 2, "notes": "Pro12Ala"},

    # SLC30A8 - Zinc transporter
    "rs13266634": {"gene": "SLC30A8", "category": "diabetes", "importance": 2, "notes": "R325W"},

    # CDKN2A/B
    "rs10811661": {"gene": "CDKN2B", "category": "diabetes", "importance": 2, "notes": "T2D risk"},

    # IGF2BP2
    "rs4402960": {"gene": "IGF2BP2", "category": "diabetes", "importance": 3, "notes": "T2D risk"},

    # FTO - Obesity/diabetes
    "rs9939609": {"gene": "FTO", "category": "obesity", "importance": 1, "notes": "Strongest obesity gene"},
    "rs1558902": {"gene": "FTO", "category": "obesity", "importance": 2, "notes": "Obesity risk"},
    "rs1121980": {"gene": "FTO", "category": "obesity", "importance": 3, "notes": "Obesity risk"},

    # MC4R - Appetite
    "rs17782313": {"gene": "MC4R", "category": "obesity", "importance": 2, "notes": "Obesity risk"},

    # =========================================================================
    # FOOD INTOLERANCES
    # =========================================================================

    # LCT - Lactose
    "rs4988235": {"gene": "LCT", "category": "food", "importance": 1, "notes": "Lactase persistence"},
    "rs182549": {"gene": "LCT", "category": "food", "importance": 2, "notes": "Lactase persistence"},

    # HLA - Celiac
    "rs2187668": {"gene": "HLA-DQ2.5", "category": "food", "importance": 1, "notes": "Celiac risk - DQ2.5"},
    "rs7454108": {"gene": "HLA-DQ8", "category": "food", "importance": 2, "notes": "Celiac risk - DQ8"},

    # =========================================================================
    # SLEEP & CIRCADIAN
    # =========================================================================

    # CLOCK
    "rs1801260": {"gene": "CLOCK", "category": "sleep", "importance": 2, "notes": "3111T>C - evening type"},
    "rs3749474": {"gene": "CLOCK", "category": "sleep", "importance": 3, "notes": "Clock gene"},

    # PER2
    "rs2304672": {"gene": "PER2", "category": "sleep", "importance": 3, "notes": "Circadian rhythm"},

    # PER3
    "rs228697": {"gene": "PER3", "category": "sleep", "importance": 3, "notes": "Sleep need"},

    # ADA - Adenosine
    "rs73598374": {"gene": "ADA", "category": "sleep", "importance": 2, "notes": "Deep sleep"},

    # ADORA2A - Caffeine sensitivity sleep
    "rs5751876": {"gene": "ADORA2A", "category": "caffeine", "importance": 2, "notes": "Caffeine insomnia"},
    "rs2298383": {"gene": "ADORA2A", "category": "caffeine", "importance": 3, "notes": "Caffeine anxiety"},

    # =========================================================================
    # FITNESS & MUSCLE
    # =========================================================================

    # ACTN3 - Power vs endurance
    "rs1815739": {"gene": "ACTN3", "category": "fitness", "importance": 2, "notes": "R577X - sprint vs endurance"},

    # ACE - Endurance
    "rs4646994": {"gene": "ACE", "category": "fitness", "importance": 2, "notes": "I/D - endurance"},
    "rs4343": {"gene": "ACE", "category": "fitness", "importance": 3, "notes": "ACE activity"},

    # PPARGC1A - Mitochondrial biogenesis
    "rs8192678": {"gene": "PPARGC1A", "category": "fitness", "importance": 3, "notes": "Gly482Ser"},

    # ADRB2 - Beta-2 receptor
    "rs1042713": {"gene": "ADRB2", "category": "fitness", "importance": 2, "notes": "Arg16Gly"},
    "rs1042714": {"gene": "ADRB2", "category": "fitness", "importance": 3, "notes": "Gln27Glu"},

    # ADRB3 - Fat metabolism
    "rs4994": {"gene": "ADRB3", "category": "fitness", "importance": 2, "notes": "Trp64Arg"},

    # COL5A1 - Tendon injuries
    "rs12722": {"gene": "COL5A1", "category": "fitness", "importance": 3, "notes": "Injury risk"},

    # =========================================================================
    # LONGEVITY
    # =========================================================================

    "rs2802292": {"gene": "FOXO3", "category": "longevity", "importance": 2, "notes": "Longevity"},
    "rs2764264": {"gene": "FOXO3", "category": "longevity", "importance": 3, "notes": "Longevity"},

    # =========================================================================
    # MENTAL HEALTH & NEUROTRANSMITTERS
    # =========================================================================

    # BDNF - Brain plasticity
    "rs6265": {"gene": "BDNF", "category": "mental", "importance": 2, "notes": "Val66Met"},

    # SLC6A4 - Serotonin transporter
    "rs25531": {"gene": "SLC6A4", "category": "mental", "importance": 2, "notes": "5-HTTLPR"},

    # DRD2 - Dopamine receptor
    "rs1800497": {"gene": "DRD2", "category": "mental", "importance": 2, "notes": "Taq1A"},

    # HTR2A - Serotonin receptor
    "rs6311": {"gene": "HTR2A", "category": "mental", "importance": 3, "notes": "A-1438G"},
    "rs6313": {"gene": "HTR2A", "category": "mental", "importance": 3, "notes": "T102C"},

    # OXTR - Oxytocin receptor
    "rs53576": {"gene": "OXTR", "category": "mental", "importance": 3, "notes": "Social behavior"},

    # =========================================================================
    # CARDIOVASCULAR
    # =========================================================================

    # AGT - Blood pressure
    "rs699": {"gene": "AGT", "category": "cardiovascular", "importance": 2, "notes": "M235T"},
    "rs4762": {"gene": "AGT", "category": "cardiovascular", "importance": 3, "notes": "T174M"},

    # ACE
    "rs4343": {"gene": "ACE", "category": "cardiovascular", "importance": 2, "notes": "ACE levels"},

    # NOS3 - Nitric oxide
    "rs1799983": {"gene": "NOS3", "category": "cardiovascular", "importance": 2, "notes": "Glu298Asp"},
    "rs2070744": {"gene": "NOS3", "category": "cardiovascular", "importance": 3, "notes": "T-786C"},

    # F5 - Factor V Leiden (clotting)
    "rs6025": {"gene": "F5", "category": "cardiovascular", "importance": 1, "notes": "Factor V Leiden"},

    # F2 - Prothrombin
    "rs1799963": {"gene": "F2", "category": "cardiovascular", "importance": 1, "notes": "G20210A"},

    # MTHFR - homocysteine/CVD
    "rs1801133": {"gene": "MTHFR", "category": "cardiovascular", "importance": 1, "notes": "C677T - CVD risk"},

    # 9p21 - MI risk
    "rs10757278": {"gene": "CDKN2B-AS1", "category": "cardiovascular", "importance": 2, "notes": "MI risk"},
    "rs1333049": {"gene": "CDKN2B-AS1", "category": "cardiovascular", "importance": 2, "notes": "CAD risk"},
}


def get_clinical_snps_in_genome(genome_snps: dict) -> dict:
    """
    Find which clinical SNPs are present in a genome file.

    Args:
        genome_snps: Dict of rsid -> genotype from genome file

    Returns:
        Dict of rsid -> {snp_info, genotype}
    """
    found = {}
    genome_lower = {k.lower(): v for k, v in genome_snps.items()}

    for rsid, info in CLINICAL_SNPS.items():
        rsid_lower = rsid.lower()
        if rsid_lower in genome_lower:
            found[rsid] = {
                **info,
                'rsid': rsid,
                'genotype': genome_lower[rsid_lower]
            }

    return found


def get_missing_clinical_snps(genome_snps: dict, database_rsids: set) -> list:
    """
    Find clinical SNPs that are in genome but not in database.

    Returns list sorted by importance.
    """
    found_in_genome = get_clinical_snps_in_genome(genome_snps)
    database_lower = {r.lower() for r in database_rsids}

    missing = []
    for rsid, info in found_in_genome.items():
        if rsid.lower() not in database_lower:
            missing.append(info)

    # Sort by importance (1 = most important)
    missing.sort(key=lambda x: x['importance'])

    return missing


def print_clinical_coverage_report(genome_snps: dict, database_rsids: set):
    """Print a report of clinical SNP coverage."""
    found = get_clinical_snps_in_genome(genome_snps)
    database_lower = {r.lower() for r in database_rsids}

    # Categorize
    in_database = []
    missing = []
    not_in_genome = []

    for rsid, info in CLINICAL_SNPS.items():
        rsid_lower = rsid.lower()
        if rsid_lower in found:
            if rsid_lower in database_lower:
                in_database.append((rsid, info, found[rsid_lower]['genotype']))
            else:
                missing.append((rsid, info, found[rsid_lower]['genotype']))
        else:
            not_in_genome.append((rsid, info))

    print(f"\n{'='*60}")
    print("CLINICAL SNP COVERAGE REPORT")
    print(f"{'='*60}")
    print(f"\nTotal clinical SNPs defined: {len(CLINICAL_SNPS)}")
    print(f"Found in genome file: {len(found)} ({100*len(found)/len(CLINICAL_SNPS):.1f}%)")
    print(f"Already in database: {len(in_database)}")
    print(f"Missing from database: {len(missing)}")
    print(f"Not in genome file: {len(not_in_genome)}")

    if missing:
        print(f"\n--- MISSING FROM DATABASE (by importance) ---")
        for rsid, info, genotype in sorted(missing, key=lambda x: x[1]['importance'])[:30]:
            print(f"  [{info['importance']}] {rsid}: {info['gene']} - {info['notes']} [Genotype: {genotype}]")

    return {
        'total_clinical': len(CLINICAL_SNPS),
        'in_genome': len(found),
        'in_database': len(in_database),
        'missing': len(missing),
        'not_in_genome': len(not_in_genome),
        'missing_snps': missing
    }


if __name__ == '__main__':
    import argparse
    from gwl_snp_fetcher import load_genome_snps
    from gwl_unified_database import get_all_rsids

    # Load extended SNPs
    try:
        import gwl_extended_snps
    except ImportError:
        pass

    parser = argparse.ArgumentParser(description='Clinical SNP coverage analysis')
    parser.add_argument('genome_file', nargs='?', help='Genome file to analyze')
    parser.add_argument('--list', action='store_true', help='List all clinical SNPs')

    args = parser.parse_args()

    if args.list:
        print("\nAll Clinical SNPs by Category:\n")
        by_category = {}
        for rsid, info in CLINICAL_SNPS.items():
            cat = info['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append((rsid, info))

        for cat in sorted(by_category.keys()):
            print(f"\n{cat.upper()} ({len(by_category[cat])} SNPs):")
            for rsid, info in sorted(by_category[cat], key=lambda x: x[1]['importance']):
                print(f"  [{info['importance']}] {rsid}: {info['gene']} - {info['notes']}")

    elif args.genome_file:
        genome_snps = load_genome_snps(args.genome_file)
        db_rsids = set(get_all_rsids())
        print_clinical_coverage_report(genome_snps, db_rsids)

    else:
        parser.print_help()
        print(f"\nTotal clinical SNPs defined: {len(CLINICAL_SNPS)}")
