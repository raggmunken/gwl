"""
GWL Auto-Fetched SNPs
=====================
Auto-generated from SNPedia cache on 2026-01-21

These SNPs were automatically fetched and converted.
Review and adjust recommendations as needed.
"""

from gwl_unified_database import UnifiedSNP, Category, RiskLevel, UNIFIED_DATABASE

AUTO_FETCHED_SNPS = {
    "rs4986893": UnifiedSNP(
        rsid="rs4986893",
        gene="CYP2C19",
        chromosome="10",
        position=94780653,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "poor metabolizer of several commonly prescribed drugs", "description": "poor metabolizer of several commonly prescribed drugs"},
            "AG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "carrier of a CYP2C19*3 allele, a \"slow metabolizer\" allele", "description": "carrier of a CYP2C19*3 allele, a \"slow metabolizer\" allele"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Informera läkare om denna variant vid läkemedelsförskrivning'],
            "AG": ['Informera läkare om denna variant vid läkemedelsförskrivning'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18547414', '23130019', '18974781', '22265638', '23661171'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1057910": UnifiedSNP(
        rsid="rs1057910",
        gene="CYP2C9",
        chromosome="10",
        position=94981296,
        ref_allele="A",
        alt_allele="C",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "normal; no effect on warfarin metabolism", "description": "normal; no effect on warfarin metabolism"},
            "AC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "CYP2C9*3 carrier; average 40% reduction in warfarin metabolism", "description": "CYP2C9*3 carrier; average 40% reduction in warfarin metabolism"},
            "CC": {"risk": RiskLevel.HIGH, "effect": "CYP2C9*3 homozygote; average 80% reduction in warfarin metabolism; reduced metabolism of number of o", "description": "CYP2C9*3 homozygote; average 80% reduction in warfarin metabolism; reduced metabolism of number of o"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AC": ['Informera läkare om denna variant vid läkemedelsförskrivning'],
            "CC": ['Informera läkare om denna variant vid läkemedelsförskrivning'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18992263', '20808793', '20842355', '22321278', '23133420'],
        clinical_significance="SNP",
        evidence_level="SNPedia"
    ),

    "rs3918290": UnifiedSNP(
        rsid="rs3918290",
        gene="DPYD",
        chromosome="1",
        position=97450058,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "AA": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "5-fluorouracil toxicity, dihydropyrimidine dehydrogenase deficiency", "description": "5-fluorouracil toxicity, dihydropyrimidine dehydrogenase deficiency"},
            "AG": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "some 5-fluorouracil toxicity, dihydropyrimidine dehydrogenase deficiency carrier", "description": "some 5-fluorouracil toxicity, dihydropyrimidine dehydrogenase deficiency carrier"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['17697348', '18547414', '29372689', '26216193', '23835662'],
        clinical_significance="Note that the terms used in the literature for this gene can be confusing, since the gene is in reve",
        evidence_level="SNPedia"
    ),

    "rs67376798": UnifiedSNP(
        rsid="rs67376798",
        gene="DPYD",
        chromosome="1",
        position=97082391,
        ref_allele="A",
        alt_allele="T",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "AA": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "5-fluorouracil toxicity", "description": "5-fluorouracil toxicity"},
            "AT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "carrier of a null DPYD allele", "description": "carrier of a null DPYD allele"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "AT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=[],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs55886062": UnifiedSNP(
        rsid="rs55886062",
        gene="DPYD",
        chromosome="1",
        position=97515787,
        ref_allele="A",
        alt_allele="C",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "AC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "carrier of a null DPYD allele", "description": "carrier of a null DPYD allele"},
            "CC": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "5-fluorouracil toxicity", "description": "5-fluorouracil toxicity"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=[],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1800462": UnifiedSNP(
        rsid="rs1800462",
        gene="TPMT",
        chromosome="6",
        position=18143724,
        ref_allele="G",
        alt_allele="C",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "CC": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "incapable of detoxifying certain drugs", "description": "incapable of detoxifying certain drugs"},
            "CG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "detoxifying ability of certain drugs may be diminished", "description": "detoxifying ability of certain drugs may be diminished"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18547414', '23133420', '22385887', '18685564'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1800460": UnifiedSNP(
        rsid="rs1800460",
        gene="TPMT",
        chromosome="6",
        position=18138997,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "AA": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "incapable of detoxifying byproducts of certain drugs", "description": "incapable of detoxifying byproducts of certain drugs"},
            "AG": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "(TPMT*3B) impaired drug metabolism", "description": "(TPMT*3B) impaired drug metabolism"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18547414', '18662289', '23133420', '22385887', '18685564'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1142345": UnifiedSNP(
        rsid="rs1142345",
        gene="TPMT",
        chromosome="6",
        position=18130687,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "AG": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "TPMT*3C . impaired drug metabolism", "description": "TPMT*3C . impaired drug metabolism"},
            "GG": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "possibly incapable of detoxifying certain drugs", "description": "possibly incapable of detoxifying certain drugs"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18547414', '23133420', '18685564', '18662289'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs17782313": UnifiedSNP(
        rsid="rs17782313",
        gene="MC4R",
        chromosome="18",
        position=60183864,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.OBESITY],
        genotype_effects={
            "CC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "adults likely to be 0.44 BMI units higher", "description": "adults likely to be 0.44 BMI units higher"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "adults likely to be 0.22 BMI units higher", "description": "adults likely to be 0.22 BMI units higher"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20881960', '29466028', '22310352', '20017980', '21147891'],
        clinical_significance="Note that",
        evidence_level="SNPedia"
    ),

    "rs6025": UnifiedSNP(
        rsid="rs6025",
        gene="F5",
        chromosome="1",
        position=169549811,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.CARDIOVASCULAR],
        genotype_effects={
            "AA": {"risk": RiskLevel.HIGH, "effect": "11.4x higher risk of thrombosis", "description": "11.4x higher risk of thrombosis"},
            "AG": {"risk": RiskLevel.HIGH, "effect": "3.5-4.4x risk of thrombosis", "description": "3.5-4.4x risk of thrombosis"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['32110755', '23018527', '33448877', '21291465', '23150947'],
        clinical_significance="In a 2013 meta-analysis of 31 databases, the analysis of Factor V",
        evidence_level="SNPedia"
    ),

    "rs2395029": UnifiedSNP(
        rsid="rs2395029",
        gene="HCP5",
        chromosome="6",
        position=31464003,
        ref_allele="G",
        alt_allele="T",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.HIGH, "effect": "HLA-B*5701 homozygote likely if Caucasian or Hispanic; high risk for hypersensitivity to various dru", "description": "HLA-B*5701 homozygote likely if Caucasian or Hispanic; high risk for hypersensitivity to various dru"},
            "GT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "HLA-B*5701 carrier most likely (if Caucasian or Hispanic)", "description": "HLA-B*5701 carrier most likely (if Caucasian or Hispanic)"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19935381', '19679225', '19276793', '20041166', '18982067'],
        clinical_significance="* see also:",
        evidence_level="SNPedia"
    ),

    "rs3909184": UnifiedSNP(
        rsid="rs3909184",
        gene="FLOT1",
        chromosome="6",
        position=30731607,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['33356553', '26083016'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs9263726": UnifiedSNP(
        rsid="rs9263726",
        gene="PSORS1C1",
        chromosome="6",
        position=31138722,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "In Japanese populations, associated with HLA-B*5801 allele and allopurinol side effects", "description": "In Japanese populations, associated with HLA-B*5801 allele and allopurinol side effects"},
            "AG": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "In Japanese populations, associated with HLA-B*5801 allele and allopurinol side effects", "description": "In Japanese populations, associated with HLA-B*5801 allele and allopurinol side effects"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['33356553', '21912425'],
        clinical_significance="The minor allele of this SNP,",
        evidence_level="SNPedia"
    ),

    "rs671": UnifiedSNP(
        rsid="rs671",
        gene="ALDH2",
        chromosome="12",
        position=111803962,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.HIGH, "effect": "Asian Flusher; increased risk of esophageal cancer; East Asian ancestry; Disulfiram not effective fo", "description": "Asian Flusher; increased risk of esophageal cancer; East Asian ancestry; Disulfiram not effective fo"},
            "AG": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "Asian Flush; worse hangovers; increased risk of esophageal cancer; East Asian ancestry; Disulfiram p", "description": "Asian Flush; worse hangovers; increased risk of esophageal cancer; East Asian ancestry; Disulfiram p"},
            "GG": {"risk": RiskLevel.PROTECTIVE, "effect": "Alcohol Flush: Normal, doesn't flush. Normal hangovers. Normal risk of Alcoholism. Normal risk of Es", "description": "Alcohol Flush: Normal, doesn't flush. Normal hangovers. Normal risk of Alcoholism. Normal risk of Es"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19041386', '23364009', '21900886', '21372407', '19698717'],
        clinical_significance="The",
        evidence_level="SNPedia"
    ),

    "rs28399504": UnifiedSNP(
        rsid="rs28399504",
        gene="CYP2C19",
        chromosome="10",
        position=94762706,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "AG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "carrier of a CYP2C19*4 allele, considered a \"slow metabolizer\" variant", "description": "carrier of a CYP2C19*4 allele, considered a \"slow metabolizer\" variant"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "poor metabolizer", "description": "poor metabolizer"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AG": ['Informera läkare om denna variant vid läkemedelsförskrivning'],
            "GG": ['Informera läkare om denna variant vid läkemedelsförskrivning'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18547414', '21247447', '23130019'],
        clinical_significance="The risk allele is",
        evidence_level="SNPedia"
    ),

    "rs7900194": UnifiedSNP(
        rsid="rs7900194",
        gene="CYP2C9",
        chromosome="10",
        position=94942309,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19663669'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2740574": UnifiedSNP(
        rsid="rs2740574",
        gene="CYP3A",
        chromosome="7",
        position=99784473,
        ref_allele="G",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "2.5x increased risk for prostate or ovarian cancer; CYP3A4*1B homozygote", "description": "2.5x increased risk for prostate or ovarian cancer; CYP3A4*1B homozygote"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23175176', '22466345', '19076156', '25217544', '20459744'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs35599367": UnifiedSNP(
        rsid="rs35599367",
        gene="CYP3A4",
        chromosome="7",
        position=99768693,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20386561', '26488616', '21946898', '23574377', '21903774'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs776746": UnifiedSNP(
        rsid="rs776746",
        gene="CYP3A5",
        chromosome="7",
        position=99672916,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "carrier of 1 nonfunctional CYP3A5 allele; drug metabolism affects", "description": "carrier of 1 nonfunctional CYP3A5 allele; drug metabolism affects"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "CYP3A5*3 homozygote;  CYP3A5 non-expressor", "description": "CYP3A5*3 homozygote;  CYP3A5 non-expressor"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['32256016', '24297552', '23501331', '33564260', '22108237'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs9934438": UnifiedSNP(
        rsid="rs9934438",
        gene="VKORC1",
        chromosome="16",
        position=31093557,
        ref_allele="A",
        alt_allele="N",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "coumadin resistance", "description": "coumadin resistance"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23124848', '19172700', '20585445', '24602049', '21179439'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2306283": UnifiedSNP(
        rsid="rs2306283",
        gene="SLCO1B1",
        chromosome="12",
        position=21176804,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23471819', '33501733', '22562052', '23133420', '25926430'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1801280": UnifiedSNP(
        rsid="rs1801280",
        gene="NAT2",
        chromosome="8",
        position=18400344,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23175176', '16847422', '26445549', '18298806', '22200898'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1799930": UnifiedSNP(
        rsid="rs1799930",
        gene="NAT2",
        chromosome="8",
        position=18400593,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Somewhat increased risk of hearing loss", "description": "Somewhat increased risk of hearing loss"},
            "AG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Possibly slightly increased risk of hearing loss", "description": "Possibly slightly increased risk of hearing loss"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23175176', '16847422', '26409796', '19390575', '19766908'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1799931": UnifiedSNP(
        rsid="rs1799931",
        gene="NAT2",
        chromosome="8",
        position=18400860,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23175176', '23072573', '16847422', '26409796', '19766908'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs234706": UnifiedSNP(
        rsid="rs234706",
        gene="CBS",
        chromosome="21",
        position=43065240,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.METHYLATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "0.50 reduced risk of cleft lip / palate, 0.51 reduced risk of non-Hodgkin lymphoma. Increased respon", "description": "0.50 reduced risk of cleft lip / palate, 0.51 reduced risk of non-Hodgkin lymphoma. Increased respon"},
            "AG": {"risk": RiskLevel.PROTECTIVE, "effect": "0.94 reduced risk of cleft lip / palate", "description": "0.94 reduced risk of cleft lip / palate"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['17697348', '23882023', '17119116', '20565774', '18708408'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs601338": UnifiedSNP(
        rsid="rs601338",
        gene="FUT2",
        chromosome="19",
        position=48703417,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.METHYLATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "resistance to Norovirus infection", "description": "resistance to Norovirus infection"},
            "AG": {"risk": RiskLevel.NORMAL, "effect": "susceptible to Norovirus infections", "description": "susceptible to Norovirus infections"},
            "GG": {"risk": RiskLevel.NORMAL, "effect": "susceptible to Norovirus infections", "description": "susceptible to Norovirus infections"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['30376117', '23075394', '28824326', '24816252', '22521342'],
        clinical_significance="It also appears to affect the composition of the microbiome",
        evidence_level="SNPedia"
    ),

    "rs1544410": UnifiedSNP(
        rsid="rs1544410",
        gene="VDR",
        chromosome="12",
        position=47846052,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.VITAMIN_D],
        genotype_effects={
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Increased risk of low bone mineral density disorders", "description": "Increased risk of low bone mineral density disorders"},
            "GG": {"risk": RiskLevel.PROTECTIVE, "effect": "Decreased risk of low bone mineral density disorders", "description": "Decreased risk of low bone mineral density disorders"},
        },
        nutrient_recommendations={
            "AA": [{"nutrient": "D-vitamin", "dose": "2000-4000 IE/dag", "reason": "VDR-variant kan kräva högre nivåer"}],
            "GG": [{"nutrient": "D-vitamin", "dose": "2000-4000 IE/dag", "reason": "VDR-variant kan kräva högre nivåer"}],
        },
        lifestyle_recommendations={
            "AA": ['Testa D-vitamin-nivåer regelbundet'],
            "GG": ['Testa D-vitamin-nivåer regelbundet'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['29409002', '20041166', '22681928', '18361940', '19734102'],
        clinical_significance="rs1544410 increases susceptibility to Shorter stature for carriers of the A allele",
        evidence_level="SNPedia"
    ),

    "rs731236": UnifiedSNP(
        rsid="rs731236",
        gene="VDR",
        chromosome="12",
        position=47844974,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.VITAMIN_D],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['31654764', '19454612', '20716226', '23979900', '21814771'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs10877012": UnifiedSNP(
        rsid="rs10877012",
        gene="CYP27B1",
        chromosome="12",
        position=57768302,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18593774', '17606874', '22690899', '23923033', '21358824'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs7041": UnifiedSNP(
        rsid="rs7041",
        gene="GC",
        chromosome="4",
        position=71752617,
        ref_allele="T",
        alt_allele="N",
        categories=[Category.VITAMIN_D],
        genotype_effects={
            "TT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "ex-smokers at 2x higher risk for COPD; supplement with Vitamin D?", "description": "ex-smokers at 2x higher risk for COPD; supplement with Vitamin D?"},
        },
        nutrient_recommendations={
            "TT": [{"nutrient": "D-vitamin", "dose": "3000-5000 IE/dag", "reason": "Kompensera för sämre D-vitamin-metabolism"}],
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22328951', '22144504', '23734748', '26383826', '28284354'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs174547": UnifiedSNP(
        rsid="rs174547",
        gene="FADS1",
        chromosome="11",
        position=61803311,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.OMEGA3],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['32397743', '20037589', '21829377', '24823311', '23808484'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1535": UnifiedSNP(
        rsid="rs1535",
        gene="FADS2",
        chromosome="11",
        position=61830500,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.OMEGA3],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "==Publications==", "description": "==Publications=="},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['27311901', '22194195', '31991592', '21347282', '22743310'],
        clinical_significance="==Publications==",
        evidence_level="SNPedia"
    ),

    "rs708272": UnifiedSNP(
        rsid="rs708272",
        gene="CETP",
        chromosome="16",
        position=56962376,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.CARDIOVASCULAR],
        genotype_effects={
            "CC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Small reduction in coronary heart disease risk from alcohol consumption", "description": "Small reduction in coronary heart disease risk from alcohol consumption"},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "B2B2 genotype; some reduction in heart disease risk from moderate alcohol consumption", "description": "B2B2 genotype; some reduction in heart disease risk from moderate alcohol consumption"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Small reduction in heart disease risk from drinking alcohol", "description": "Small reduction in heart disease risk from drinking alcohol"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22011848', '17157861', '31739638', '18275964', '22073289'],
        clinical_significance="A similarly confusing picture emerges from a study of two populations of 10,000+ individuals each. T",
        evidence_level="SNPedia"
    ),

    "rs328": UnifiedSNP(
        rsid="rs328",
        gene="LPL",
        chromosome="8",
        position=19962213,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.CARDIOVASCULAR],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19197348', '24386095', '17157861', '18275964', '17291198'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs11591147": UnifiedSNP(
        rsid="rs11591147",
        gene="PCSK9",
        chromosome="1",
        position=55039974,
        ref_allele="G",
        alt_allele="T",
        categories=[Category.CARDIOVASCULAR],
        genotype_effects={
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "2-3 fold lower risk of heart disease", "description": "2-3 fold lower risk of heart disease"},
            "GT": {"risk": RiskLevel.PROTECTIVE, "effect": "2-3 fold lower risk of heart disease", "description": "2-3 fold lower risk of heart disease"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20031607', '23300213', '29748315', '21285406', '19773416'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs7501331": UnifiedSNP(
        rsid="rs7501331",
        gene="BCO1",
        chromosome="16",
        position=81280891,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.ANTIOXIDANT],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Reduced conversion of beta-carotene to retinol", "description": "Reduced conversion of beta-carotene to retinol"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Reduced conversion of beta-carotene to retinol", "description": "Reduced conversion of beta-carotene to retinol"},
        },
        nutrient_recommendations={
            "TT": [{"nutrient": "A-vitamin (retinol)", "dose": "5000 IE/dag", "reason": "Sämre konvertering från betakaroten"}],
            "CT": [{"nutrient": "A-vitamin (retinol)", "dose": "5000 IE/dag", "reason": "Sämre konvertering från betakaroten"}],
        },
        lifestyle_recommendations={
            "TT": ['Förlita dig inte på morötter för A-vitamin - ät lever eller ta tillskott'],
            "CT": ['Förlita dig inte på morötter för A-vitamin - ät lever eller ta tillskott'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22113863', '29428584', '21091228', '19557453', '19844255'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1799945": UnifiedSNP(
        rsid="rs1799945",
        gene="LOC108783645",
        chromosome="6",
        position=26090951,
        ref_allele="G",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.HIGH, "effect": "Two copies of H63D, likely affected by mild form of hemochromatosis", "description": "Two copies of H63D, likely affected by mild form of hemochromatosis"},
            "CG": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "One copy of H63D, carrier of hemochromatosis, likely unaffected unless also C282Y carrier.", "description": "One copy of H63D, carrier of hemochromatosis, likely unaffected unless also C282Y carrier."},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19165391', '18603647', '19401444', '24663082', '18194558'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs855791": UnifiedSNP(
        rsid="rs855791",
        gene="TMPRSS6",
        chromosome="22",
        position=37066896,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19820699', '23263863', '21149283', '23222517', '20927387'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs662": UnifiedSNP(
        rsid="rs662",
        gene="PON1",
        chromosome="7",
        position=95308134,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.DETOX_PHASE2],
        genotype_effects={
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "~2x higher risk of of coronary heart disease reported in some studies, but lower risk seen in other ", "description": "~2x higher risk of of coronary heart disease reported in some studies, but lower risk seen in other "},
            "GG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Mixed; conflicting results reported related to stroke and CAD", "description": "Mixed; conflicting results reported related to stroke and CAD"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22615820', '20856122', '31647334', '21223581', '20031584'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs16944": UnifiedSNP(
        rsid="rs16944",
        gene="IL1B",
        chromosome="2",
        position=112837290,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Increased risk (~3x) for osteoarthritis", "description": "Increased risk (~3x) for osteoarthritis"},
            "AG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Minorly increased risk of mental illness and osteoarthritis", "description": "Minorly increased risk of mental illness and osteoarthritis"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Slightly increased (~2x or less) risk for certain mental disorders", "description": "Slightly increased (~2x or less) risk for certain mental disorders"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['25735143', '25222025', '28268030', '20347268', '26813132'],
        clinical_significance="The rs16944 A allele increases susceptibility to",
        evidence_level="SNPedia"
    ),

    "rs1205": UnifiedSNP(
        rsid="rs1205",
        gene="CRP",
        chromosome="1",
        position=159712443,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20538124', '24894103', '19101671', '23940726', '26550110'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1800896": UnifiedSNP(
        rsid="rs1800896",
        gene="IL10",
        chromosome="1",
        position=206773552,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.8x increased prostate cancer risk", "description": "1.8x increased prostate cancer risk"},
            "AG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.6x increased prostate cancer risk", "description": "1.6x increased prostate cancer risk"},
            "GG": {"risk": RiskLevel.PROTECTIVE, "effect": "Normal prostate cancer risk", "description": "Normal prostate cancer risk"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20299965', '28268030', '16672419', '22144535', '16672072'],
        clinical_significance="This SNP is upstream of the",
        evidence_level="SNPedia"
    ),

    "rs12255372": UnifiedSNP(
        rsid="rs12255372",
        gene="TCF7L2",
        chromosome="10",
        position=113049143,
        ref_allele="G",
        alt_allele="T",
        categories=[Category.BLOOD_SUGAR],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "slight increases (~1.5x) in risk for type-2 diabetes and possibly breast cancer and aggressive prost", "description": "slight increases (~1.5x) in risk for type-2 diabetes and possibly breast cancer and aggressive prost"},
            "GT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.3x increased type-2 diabetes risk", "description": "1.3x increased type-2 diabetes risk"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20648057', '17972059', '19924244', '17259383', '22441719'],
        clinical_significance="'''* Breast Cancer Risk Overview:''' some papers report a small increase in risk, around 1.1 to 1.2x",
        evidence_level="SNPedia"
    ),

    "rs13266634": UnifiedSNP(
        rsid="rs13266634",
        gene="SLC30A8",
        chromosome="8",
        position=117172544,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "increased risk for type-2 diabetes", "description": "increased risk for type-2 diabetes"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "increased risk for type-2 diabetes", "description": "increased risk for type-2 diabetes"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19324937', '20424228', '23334806', '18694974', '18210030'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs10811661": UnifiedSNP(
        rsid="rs10811661",
        gene="CDKN2A/B",
        chromosome="9",
        position=22134095,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.2x increased risk for type-2 diabetes", "description": "1.2x increased risk for type-2 diabetes"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.2x increased risk for type-2 diabetes", "description": "1.2x increased risk for type-2 diabetes"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19324937', '20424228', '20386740', '18694974', '19460916'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1558902": UnifiedSNP(
        rsid="rs1558902",
        gene="FTO",
        chromosome="16",
        position=53769662,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.OBESITY],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20703240', '22504289', '24084939', '21544081', '29548861'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs182549": UnifiedSNP(
        rsid="rs182549",
        gene="MCM6",
        chromosome="2",
        position=135859184,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.IMMUNE],
        genotype_effects={
            "CC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "possibly lactose intolerant", "description": "possibly lactose intolerant"},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "Can digest milk.", "description": "Can digest milk."},
            "CT": {"risk": RiskLevel.PROTECTIVE, "effect": "Can digest milk.", "description": "Can digest milk."},
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Kalcium", "dose": "1000 mg/dag", "reason": "Kompensera för minskade mejeriprodukter"}],
        },
        lifestyle_recommendations={
            "CC": ['Laktosfria alternativ rekommenderas'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['11788828', '15114531', '22572735', '23029545', '17159977'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs5751876": UnifiedSNP(
        rsid="rs5751876",
        gene="SPECC1L-ADORA2A",
        chromosome="22",
        position=24441333,
        ref_allele="T",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "significantly higher anxiety levels after moderate caffeine consumption", "description": "significantly higher anxiety levels after moderate caffeine consumption"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19902562', '22012471', '22940476', '21658325', '22745815'],
        clinical_significance="However",
        evidence_level="SNPedia"
    ),

    "rs4343": UnifiedSNP(
        rsid="rs4343",
        gene="ACE",
        chromosome="17",
        position=63488670,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.MUSCLE],
        genotype_effects={
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "ACE I/I genotype", "description": "ACE I/I genotype"},
            "AG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "ACE I/D genotype", "description": "ACE I/D genotype"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "ACE D/D genotype", "description": "ACE D/D genotype"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20639399', '20682755', '28271690', '26823847', '21258267'],
        clinical_significance="See",
        evidence_level="SNPedia"
    ),

    "rs8192678": UnifiedSNP(
        rsid="rs8192678",
        gene="PPARGC1A",
        chromosome="4",
        position=23814039,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.MUSCLE],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18996470', '23269818', '25923461', '24317794', '22038464'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1042714": UnifiedSNP(
        rsid="rs1042714",
        gene="ADRB2",
        chromosome="5",
        position=148826910,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.MUSCLE],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "A study of 334 families with at least one child with", "description": "A study of 334 families with at least one child with"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18279468', '21291465', '22363809', '23229733', '24322328'],
        clinical_significance="A study of 334 families with at least one child with",
        evidence_level="SNPedia"
    ),

    "rs2764264": UnifiedSNP(
        rsid="rs2764264",
        gene="FOXO3",
        chromosome="6",
        position=108613258,
        ref_allele="C",
        alt_allele="N",
        categories=[Category.ANTIOXIDANT],
        genotype_effects={
            "CC": {"risk": RiskLevel.PROTECTIVE, "effect": "greater odds of living to 95", "description": "greater odds of living to 95"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['31009445', '24350933', '18765803', '19196970'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1800497": UnifiedSNP(
        rsid="rs1800497",
        gene="ANKK1",
        chromosome="11",
        position=113400106,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.PROTECTIVE, "effect": "Normal (A2/A2)", "description": "Normal (A2/A2)"},
            "TT": {"risk": RiskLevel.HIGH, "effect": "A1/A1: Bad at avoidance of errors. 0.25x lower OCD; 0.56x lower Tardive Diskinesia; higher ADHD; 1.4", "description": "A1/A1: Bad at avoidance of errors. 0.25x lower OCD; 0.56x lower Tardive Diskinesia; higher ADHD; 1.4"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "A1/A2: Bad at avoidance of errors. 0.5x lower OCD risk, 0.87x lower Tardive Diskinesia risk, higher ", "description": "A1/A2: Bad at avoidance of errors. 0.5x lower OCD risk, 0.87x lower Tardive Diskinesia risk, higher "},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19512960', '19321766', '19470168', '17135598', '17483451'],
        clinical_significance="A wide variety of reports have been published over more than ten years either linking",
        evidence_level="SNPedia"
    ),

    "rs6277": UnifiedSNP(
        rsid="rs6277",
        gene="DRD2",
        chromosome="11",
        position=113412737,
        ref_allele="T",
        alt_allele="N",
        categories=[Category.STRESS_MOOD],
        genotype_effects={
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "normal schizophrenia risk, learns NoGo faster", "description": "normal schizophrenia risk, learns NoGo faster"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19373123', '26445370', '21172166', '19158809', '21861710'],
        clinical_significance="Note that",
        evidence_level="SNPedia"
    ),

    "rs27072": UnifiedSNP(
        rsid="rs27072",
        gene="SLC6A3",
        chromosome="5",
        position=1394407,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "2x risk of severe alcohol withdrawal. Possible increased odds of ADHD.", "description": "2x risk of severe alcohol withdrawal. Possible increased odds of ADHD."},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "Lower risk of alcohol withdrawal seizures, and probably lower odds of ADHD.", "description": "Lower risk of alcohol withdrawal seizures, and probably lower odds of ADHD."},
            "CT": {"risk": RiskLevel.PROTECTIVE, "effect": "Lower risk of alcohol withdrawal seizures, and perhaps lower odds of ADHD.", "description": "Lower risk of alcohol withdrawal seizures, and perhaps lower odds of ADHD."},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23647133', '25683821', '23340505', '24780147'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1611115": UnifiedSNP(
        rsid="rs1611115",
        gene="DBH",
        chromosome="9",
        position=133635393,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "This study concludes that", "description": "This study concludes that"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20621148', '23384717', '18180394', '18330705', '33204361'],
        clinical_significance="This study concludes that",
        evidence_level="SNPedia"
    ),

    "rs3785143": UnifiedSNP(
        rsid="rs3785143",
        gene="SLC6A2",
        chromosome="16",
        position=55661194,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "may be associated with ADHD", "description": "may be associated with ADHD"},
            "CT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "may be associated with ADHD", "description": "may be associated with ADHD"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23266789', '25229170', '18937309', '22297068'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs4570625": UnifiedSNP(
        rsid="rs4570625",
        gene="TPH2",
        chromosome="12",
        position=71938143,
        ref_allele="G",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "maybe: higher scores on anxiety-related personality traits; greater placebo response", "description": "maybe: higher scores on anxiety-related personality traits; greater placebo response"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['26013962', '21396719', '22698518', '22655589', '23628433'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1799971": UnifiedSNP(
        rsid="rs1799971",
        gene="OPRM1",
        chromosome="6",
        position=154039662,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "stronger cravings for alcohol. if alcoholic, naltrexone treatment 2x more successful", "description": "stronger cravings for alcohol. if alcoholic, naltrexone treatment 2x more successful"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "more pain", "description": "more pain"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21277709', '25715171', '22046326', '26233486', '26832728'],
        clinical_significance="However, subsequent research results are mixed, and there are other studies both agreeing or disagre",
        evidence_level="SNPedia"
    ),

    "rs699": UnifiedSNP(
        rsid="rs699",
        gene="AGT",
        chromosome="1",
        position=230710048,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.CARDIOVASCULAR],
        genotype_effects={
            "CC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "increased risk of hypertension", "description": "increased risk of hypertension"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "increased risk of hypertension", "description": "increased risk of hypertension"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18279468', '28271690', '18069999', '23354977', '18698212'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs10757278": UnifiedSNP(
        rsid="rs10757278",
        gene="CDKN2A,CDKN2B",
        chromosome="9",
        position=22124478,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "0.78x reduced risk for Coronary Heart Disease. 0.77x reduced risk for Brain Aneurysm and Abdominal A", "description": "0.78x reduced risk for Coronary Heart Disease. 0.77x reduced risk for Brain Aneurysm and Abdominal A"},
            "AG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.3x risk for Heart Attack. Normal risk for Abdominal Aortic Aneurysm and Brain Aneurysm.", "description": "1.3x risk for Heart Attack. Normal risk for Abdominal Aortic Aneurysm and Brain Aneurysm."},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.6x risk for Heart Attack; 1.3x risk for Abdominal Aortic Aneurysm and Brain Aneurysm.", "description": "1.6x risk for Heart Attack; 1.3x risk for Abdominal Aortic Aneurysm and Brain Aneurysm."},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19359634', '20386740', '19503741', '24087953', '21511257'],
        clinical_significance="For early onset MI, the odds are slightly higher; homozygote",
        evidence_level="SNPedia"
    ),

    "rs1333049": UnifiedSNP(
        rsid="rs1333049",
        gene="CDKN2A,CDKN2B",
        chromosome="9",
        position=22125504,
        ref_allele="G",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.HIGH, "effect": "1.9x increased risk for coronary artery disease", "description": "1.9x increased risk for coronary artery disease"},
            "CG": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "1.5x increased risk for CAD", "description": "1.5x increased risk for CAD"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20386740', '17634449', '24087953', '25232560', '22436605'],
        clinical_significance="This SNP has also been reported to have the highest association of any SNP studied in a subsequent e",
        evidence_level="SNPedia"
    ),

    "rs1805086": UnifiedSNP(
        rsid="rs1805086",
        gene="MSTN",
        chromosome="2",
        position=190060351,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23354683', '21283721', '19237423'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1061235": UnifiedSNP(
        rsid="rs1061235",
        gene="HLA-A",
        chromosome="6",
        position=29945521,
        ref_allele="A",
        alt_allele="T",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "Normal carbamazepine sensitivity; common in clinvar", "description": "Normal carbamazepine sensitivity; common in clinvar"},
            "AT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "26% risk of bad reaction to anti-epileptic carbamazepine", "description": "26% risk of bad reaction to anti-epileptic carbamazepine"},
            "TT": {"risk": RiskLevel.HIGH, "effect": "26% risk of bad reaction to anti-epileptic carbamazepine", "description": "26% risk of bad reaction to anti-epileptic carbamazepine"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['26083016', '21428769'],
        clinical_significance="The HLA-A*3101 allele, found in about 2 - 5% of Northern Europeans, is significantly associated with",
        evidence_level="SNPedia"
    ),

    "rs1800925": UnifiedSNP(
        rsid="rs1800925",
        gene="TH2LCRR",
        chromosome="5",
        position=132657117,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "This SNP is in the promoter region of the IL-13 gene", "description": "This SNP is in the promoter region of the IL-13 gene"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18186920', '18625055', '18075513', '20015396', '19796199'],
        clinical_significance="This SNP is in the promoter region of the IL-13 gene",
        evidence_level="SNPedia"
    ),

    "rs7216389": UnifiedSNP(
        rsid="rs7216389",
        gene="GSDMB",
        chromosome="17",
        position=39913696,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.PROTECTIVE, "effect": "0.69x lower risk of Childhood Asthma.", "description": "0.69x lower risk of Childhood Asthma."},
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.5x increased risk for Childhood Asthma.", "description": "1.5x increased risk for Childhood Asthma."},
            "CT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Normal risk for Childhood Asthma.", "description": "Normal risk for Childhood Asthma."},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18439551', '23028483', '19714205', '20503266', '19732864'],
        clinical_significance="A large study of Scottish",
        evidence_level="SNPedia"
    ),

    "rs2395182": UnifiedSNP(
        rsid="rs2395182",
        gene="HLA-DRA",
        chromosome="6",
        position=32445540,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20018075', '15770496'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs5400": UnifiedSNP(
        rsid="rs5400",
        gene="SLC2A2",
        chromosome="3",
        position=171014511,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "normal sugar consumption", "description": "normal sugar consumption"},
            "TT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "significantly higher sugar consumption", "description": "significantly higher sugar consumption"},
            "CT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "significantly higher sugar consumption?", "description": "significantly higher sugar consumption?"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18678618', '21283750', '20066028', '31728565', '26112465'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1421085": UnifiedSNP(
        rsid="rs1421085",
        gene="FTO",
        chromosome="16",
        position=53767042,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.OBESITY],
        genotype_effects={
            "CC": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "~1.7x increased obesity risk", "description": "~1.7x increased obesity risk"},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "normal obesity risk", "description": "normal obesity risk"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "~1.3x increased obesity risk", "description": "~1.3x increased obesity risk"},
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Protein", "dose": "1.6-2.0 g/kg/dag", "reason": "Ökar mättnad"}],
            "CT": [{"nutrient": "Protein", "dose": "1.6-2.0 g/kg/dag", "reason": "Ökar mättnad"}],
        },
        lifestyle_recommendations={
            "CC": ['Proteinrik frukost rekommenderas starkt', 'Undvik snacking - håll regelbundna måltider'],
            "CT": ['Proteinrik frukost rekommenderas starkt', 'Undvik snacking - håll regelbundna måltider'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22590636', '23342142', '22189543', '21283731', '22187296'],
        clinical_significance="However, in one study of 583 extremely obese women with several",
        evidence_level="SNPedia"
    ),

    "rs4506565": UnifiedSNP(
        rsid="rs4506565",
        gene="TCF7L2",
        chromosome="10",
        position=112996282,
        ref_allele="A",
        alt_allele="T",
        categories=[Category.BLOOD_SUGAR],
        genotype_effects={
            "AT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "1.4x increased risk for type-2 diabetes", "description": "1.4x increased risk for type-2 diabetes"},
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.9x increased risk for type-2 diabetes", "description": "1.9x increased risk for type-2 diabetes"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23142382', '19053027', '24128935', '23188737', '19913122'],
        clinical_significance="Note: this is one of two SNPs within the",
        evidence_level="SNPedia"
    ),

    "rs1260326": UnifiedSNP(
        rsid="rs1260326",
        gene="GCKR",
        chromosome="2",
        position=27508073,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "slightly higher risk for gout", "description": "slightly higher risk for gout"},
            "CT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "slightly higher risk for gout", "description": "slightly higher risk for gout"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23022100', '21943158', '27882376', '20657596', '23903356'],
        clinical_significance="The T allele of",
        evidence_level="SNPedia"
    ),

    "rs713598": UnifiedSNP(
        rsid="rs713598",
        gene="TAS2R38",
        chromosome="7",
        position=141973545,
        ref_allele="G",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Possibly unable to taste bitter in some foods.", "description": "Possibly unable to taste bitter in some foods."},
            "CC": {"risk": RiskLevel.PROTECTIVE, "effect": "Can taste bitter.", "description": "Can taste bitter."},
            "CG": {"risk": RiskLevel.PROTECTIVE, "effect": "Can taste bitter.", "description": "Can taste bitter."},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['31137020', '24083639', '25257701', '23133589', '20675712'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs7799039": UnifiedSNP(
        rsid="rs7799039",
        gene="LOC105375494",
        chromosome="7",
        position=128238730,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20140086', '19942621', '20201642', '23284729', '19035456'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1137101": UnifiedSNP(
        rsid="rs1137101",
        gene="LEPR",
        chromosome="1",
        position=65592830,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.BLOOD_SUGAR],
        genotype_effects={
            "AG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Slight increase in obesity and T2DM risk", "description": "Slight increase in obesity and T2DM risk"},
            "GG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Slight increase in obesity and T2DM risk", "description": "Slight increase in obesity and T2DM risk"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19818126', '23284729', '22983835', '20517895', '20149225'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1229984": UnifiedSNP(
        rsid="rs1229984",
        gene="ADH1B",
        chromosome="4",
        position=99318162,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "0.56x decreased risk of oral/throat cancers", "description": "0.56x decreased risk of oral/throat cancers"},
            "AG": {"risk": RiskLevel.PROTECTIVE, "effect": "0.56x decreased risk of oral/throat cancers", "description": "0.56x decreased risk of oral/throat cancers"},
            "GG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "normal oral/throat cancer risk; more frequent alcohol consumption", "description": "normal oral/throat cancer risk; more frequent alcohol consumption"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['30371560', '21372407', '19698717', '24553426', '23895337'],
        clinical_significance="A study of over 3800 cases of upper aerodigestive",
        evidence_level="SNPedia"
    ),

    "rs4961": UnifiedSNP(
        rsid="rs4961",
        gene="ADD1",
        chromosome="4",
        position=2904980,
        ref_allele="G",
        alt_allele="T",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.8x increased risk for high blood pressure", "description": "1.8x increased risk for high blood pressure"},
            "GT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.8x increased risk for high blood pressure", "description": "1.8x increased risk for high blood pressure"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['29550988', '19960031', '19838659', '21291465', '20145305'],
        clinical_significance="Subsequent studies have tended to confirm this association, and to extend it to risk for",
        evidence_level="SNPedia"
    ),

    "rs10936599": UnifiedSNP(
        rsid="rs10936599",
        gene="MYNN",
        chromosome="3",
        position=169774313,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.PROTECTIVE, "effect": "longer telomeres, longer life?", "description": "longer telomeres, longer life?"},
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "shorter telomeres, shorter life?", "description": "shorter telomeres, shorter life?"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21708826', '32577134', '21833088', '24292274', '30325019'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2736100": UnifiedSNP(
        rsid="rs2736100",
        gene="TERT",
        chromosome="5",
        position=1286401,
        ref_allele="G",
        alt_allele="T",
        categories=[Category.ANTIOXIDANT],
        genotype_effects={
            "GG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "1.6x higher risk for glioma development", "description": "1.6x higher risk for glioma development"},
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "higher risk of Interstitial lung disease, and testicular cancer, 2.1x risk of pulmonary fibrosis", "description": "higher risk of Interstitial lung disease, and testicular cancer, 2.1x risk of pulmonary fibrosis"},
            "GT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "1.3x higher risk for glioma development, 2.1x risk of pulmonary fibrosis", "description": "1.3x higher risk for glioma development, 2.1x risk of pulmonary fibrosis"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['28300824', '22886559', '21350045', '22711262', '27162544'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs3758391": UnifiedSNP(
        rsid="rs3758391",
        gene="SIRT1",
        chromosome="10",
        position=67883584,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.ANTIOXIDANT],
        genotype_effects={
            "CC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Normal (worse) aging.", "description": "Normal (worse) aging."},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "Increased longevity. Less mental decline with age.", "description": "Increased longevity. Less mental decline with age."},
            "CT": {"risk": RiskLevel.PROTECTIVE, "effect": "Less mental decline with age.", "description": "Less mental decline with age."},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20503258', '32849821', '20633545', '27089876', '32967053'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1042522": UnifiedSNP(
        rsid="rs1042522",
        gene="TP53",
        chromosome="17",
        position=7676154,
        ref_allele="G",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Common variant. Slightly shorter lifespan.", "description": "Common variant. Slightly shorter lifespan."},
            "CC": {"risk": RiskLevel.PROTECTIVE, "effect": "Live 3 years longer. Chemotherapy is more effective.", "description": "Live 3 years longer. Chemotherapy is more effective."},
            "CG": {"risk": RiskLevel.PROTECTIVE, "effect": "Slightly increased lifespan?", "description": "Slightly increased lifespan?"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['16465622', '19707196', '20587610', '27436625', '18715757'],
        clinical_significance="For details of all 25 SNPs in this group, along with the two methods used to calculate overall risk ",
        evidence_level="SNPedia"
    ),

    "rs10490924": UnifiedSNP(
        rsid="rs10490924",
        gene="LOC105378525",
        chromosome="10",
        position=122454932,
        ref_allele="G",
        alt_allele="T",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "8.2x risk for age related macular degeneration", "description": "8.2x risk for age related macular degeneration"},
            "GT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "2.7x risk for age related macular degeneration", "description": "2.7x risk for age related macular degeneration"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22552255', '23644223', '24067115', '22699975', '19268887'],
        clinical_significance="Disease risk in combination with the",
        evidence_level="SNPedia"
    ),

    "rs1061170": UnifiedSNP(
        rsid="rs1061170",
        gene="CFH",
        chromosome="1",
        position=196690107,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "5.9x risk for AMD; higher mortality among nonagenarians", "description": "5.9x risk for AMD; higher mortality among nonagenarians"},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "lower risk for AMD, generally longer live than (C) allele carriers", "description": "lower risk for AMD, generally longer live than (C) allele carriers"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "2.5x risk for AMD; higher mortality among nonagenarians", "description": "2.5x risk for AMD; higher mortality among nonagenarians"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21665990', '22253316', '21871809', '17940599', '23662819'],
        clinical_significance="A haplotype of",
        evidence_level="SNPedia"
    ),

    "rs1805007": UnifiedSNP(
        rsid="rs1805007",
        gene="MC1R",
        chromosome="16",
        position=89919709,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "increased response to anesthetics; 13-20x higher likelihood of red hair; increased risk of melanoma", "description": "increased response to anesthetics; 13-20x higher likelihood of red hair; increased risk of melanoma"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Carrier of a red hair associated variant; higher risk of melanoma", "description": "Carrier of a red hair associated variant; higher risk of melanoma"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['12663858', '23393597', '23548203', '20670983', '17952075'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1805008": UnifiedSNP(
        rsid="rs1805008",
        gene="MC1R",
        chromosome="16",
        position=89919736,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "~7-10x higher likelihood of red hair; higher risk of melanoma", "description": "~7-10x higher likelihood of red hair; higher risk of melanoma"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Red hair carrier, higher risk of melanoma", "description": "Red hair carrier, higher risk of melanoma"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23393597', '20670983', '20042077', '18392143', '17999355'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs11209026": UnifiedSNP(
        rsid="rs11209026",
        gene="IL23R",
        chromosome="1",
        position=67240275,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.IMMUNE],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "0.26x lower risk for certain autoimmune diseases.", "description": "0.26x lower risk for certain autoimmune diseases."},
            "AG": {"risk": RiskLevel.PROTECTIVE, "effect": "0.26x lower risk for certain autoimmune diseases.", "description": "0.26x lower risk for certain autoimmune diseases."},
            "GG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Normal, but higher risk for certain autoimmune diseases.", "description": "Normal, but higher risk for certain autoimmune diseases."},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['17684544', '29967744', '20953190', '25680555', '21896776'],
        clinical_significance="A relatively rare allele at SNP",
        evidence_level="SNPedia"
    ),

    "rs2066844": UnifiedSNP(
        rsid="rs2066844",
        gene="NOD2",
        chromosome="16",
        position=50712015,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.IMMUNE],
        genotype_effects={
            "TT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "Significance unclear; possibly higher risk for Crohn's disease", "description": "Significance unclear; possibly higher risk for Crohn's disease"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Significance is unclear, but possibly, ~2x higher risk for Crohn's disease", "description": "Significance is unclear, but possibly, ~2x higher risk for Crohn's disease"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23651603', '17684544', '20066736', '20959815', '20082483'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs5743293": UnifiedSNP(
        rsid="rs5743293",
        gene="NOD2",
        chromosome="16",
        position=50729870,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.IMMUNE],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19570052', '28506689', '18715515', '20412372', '22563200'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs738409": UnifiedSNP(
        rsid="rs738409",
        gene="PNPLA3",
        chromosome="22",
        position=43928847,
        ref_allele="G",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.PROTECTIVE, "effect": "most common genotype; slightly less damage from alcohol", "description": "most common genotype; slightly less damage from alcohol"},
            "CC": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "higher odds of alcoholic liver disease, increased liver fat", "description": "higher odds of alcoholic liver disease, increased liver fat"},
            "CG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "increased liver fat, odds of alcoholic liver disease", "description": "increased liver fat, odds of alcoholic liver disease"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['26745088', '20373368', '21334404', '23269818', '22704398'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs58542926": UnifiedSNP(
        rsid="rs58542926",
        gene="TM6SF2",
        chromosome="19",
        position=19268740,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Complex; slightly lower risk of heart attacks, yet slightly higher risk for diabetes and NAFLD", "description": "Complex; slightly lower risk of heart attacks, yet slightly higher risk for diabetes and NAFLD"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['26331730', '33476381', '30564000', '31826071', '26847197'],
        clinical_significance="Known more commonly as the TM6SF2 E167K variant, but also as c.499C>T or p.Glu167Lys,",
        evidence_level="SNPedia"
    ),

    "rs1041983": UnifiedSNP(
        rsid="rs1041983",
        gene="NAT2",
        chromosome="8",
        position=18400285,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.PHARMACOGENOMICS],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18680467', '18547414', '22414877', '22092036', '22336957'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs567754": UnifiedSNP(
        rsid="rs567754",
        gene="BHMT",
        chromosome="5",
        position=79120593,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.METHYLATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18457970', '19493349', '19048631'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2851391": UnifiedSNP(
        rsid="rs2851391",
        gene="CBS",
        chromosome="21",
        position=43067294,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.METHYLATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19493349', '23824729', '23251661', '24816252', '17035141'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs4633": UnifiedSNP(
        rsid="rs4633",
        gene="COMT",
        chromosome="22",
        position=19962712,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.STRESS_MOOD],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "higher risk for endometrial cancer", "description": "higher risk for endometrial cancer"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "higher risk for endometrial cancer", "description": "higher risk for endometrial cancer"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22939719', '16380905', '18389087', '29330410', '18574484'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs6269": UnifiedSNP(
        rsid="rs6269",
        gene="COMT",
        chromosome="22",
        position=19962429,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.STRESS_MOOD],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['29330410', '18574484', '21462137', '27228319', '19193196'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs602662": UnifiedSNP(
        rsid="rs602662",
        gene="FUT2",
        chromosome="19",
        position=48703728,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.METHYLATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "Higher vitamin B12 levels", "description": "Higher vitamin B12 levels"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Lower vitamin B12 levels", "description": "Lower vitamin B12 levels"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23201895', '21115529', '20570966', '28824326', '18776911'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs7975232": UnifiedSNP(
        rsid="rs7975232",
        gene="VDR",
        chromosome="12",
        position=47845054,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.VITAMIN_D],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['31654764', '22522591', '23979900', '23065592', '22681928'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs174548": UnifiedSNP(
        rsid="rs174548",
        gene="FADS1",
        chromosome="11",
        position=61803876,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.OMEGA3],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "FADS1 codes for an enzyme involved in fatty acid unsaturation and the", "description": "FADS1 codes for an enzyme involved in fatty acid unsaturation and the"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20864672', '25646338', '24816252', '22960237', '19043545'],
        clinical_significance="FADS1 codes for an enzyme involved in fatty acid unsaturation and the",
        evidence_level="SNPedia"
    ),

    "rs174556": UnifiedSNP(
        rsid="rs174556",
        gene="FADS1",
        chromosome="11",
        position=61813163,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.OMEGA3],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['24816252', '32682282'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs174583": UnifiedSNP(
        rsid="rs174583",
        gene="FADS2",
        chromosome="11",
        position=61842278,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.OMEGA3],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18936223', '20395685', '22960237', '20565855', '20339536'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs953413": UnifiedSNP(
        rsid="rs953413",
        gene="ELOVL2",
        chromosome="6",
        position=11012626,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['32502762'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs5882": UnifiedSNP(
        rsid="rs5882",
        gene="CETP",
        chromosome="16",
        position=56982180,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.CARDIOVASCULAR],
        genotype_effects={
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Faster aging. Increased risk for Dementia. Less good cholesterol.", "description": "Faster aging. Increased risk for Dementia. Less good cholesterol."},
            "AG": {"risk": RiskLevel.PROTECTIVE, "effect": "Lower risk of dementia and Alzheimer's disease. Higher good cholesterol.", "description": "Lower risk of dementia and Alzheimer's disease. Higher good cholesterol."},
            "GG": {"risk": RiskLevel.PROTECTIVE, "effect": "Longer lifespan, 0.28x lower risk of dementia, 0.31x lower risk of Alzheimer's.", "description": "Longer lifespan, 0.28x lower risk of dementia, 0.31x lower risk of Alzheimer's."},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['26244602', '29942448', '18549840', '12802015', '24468472'],
        clinical_significance="New research also indicates that G homozygotes have an average of 70% less risk of dementia and",
        evidence_level="SNPedia"
    ),

    "rs320": UnifiedSNP(
        rsid="rs320",
        gene="LPL",
        chromosome="8",
        position=19961566,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.CARDIOVASCULAR],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20429872', '25156894', '17721767', '19041386', '18922999'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs3811647": UnifiedSNP(
        rsid="rs3811647",
        gene="TF",
        chromosome="3",
        position=133765185,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.IRON],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21208937', '19673882', '23903878', '21785125', '23092954'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs4820268": UnifiedSNP(
        rsid="rs4820268",
        gene="TMPRSS6",
        chromosome="22",
        position=37073551,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20927387', '19880490', '21208937', '19673882', '28151393'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1138272": UnifiedSNP(
        rsid="rs1138272",
        gene="GSTP1",
        chromosome="11",
        position=67586108,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.DETOX_PHASE2],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18854777', '21741876', '23175176', '18776599', '17194543'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1800796": UnifiedSNP(
        rsid="rs1800796",
        gene="LOC541472",
        chromosome="7",
        position=22726627,
        ref_allele="C",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "slightly increased risk for abdominal aortic aneurysm reported", "description": "slightly increased risk for abdominal aortic aneurysm reported"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19267250', '25735143', '18276608', '28268030', '26813132'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs361525": UnifiedSNP(
        rsid="rs361525",
        gene="TNF",
        chromosome="6",
        position=31575324,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "** However, a 2009 European study of 30,000 breast cancer cases, compared to 30,000 controls, found ", "description": "** However, a 2009 European study of 30,000 breast cancer cases, compared to 30,000 controls, found "},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21790707', '24003507', '27195243', '26170653', '24252077'],
        clinical_significance="** However, a 2009 European study of 30,000 breast cancer cases, compared to 30,000 controls, found ",
        evidence_level="SNPedia"
    ),

    "rs1143634": UnifiedSNP(
        rsid="rs1143634",
        gene="IL1B",
        chromosome="2",
        position=112832813,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "rs1143634 increases susceptibility to", "description": "rs1143634 increases susceptibility to"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19911060', '28268030', '20347268', '22925444', '29023524'],
        clinical_significance="rs1143634 increases susceptibility to",
        evidence_level="SNPedia"
    ),

    "rs4402960": UnifiedSNP(
        rsid="rs4402960",
        gene="IGF2BP2",
        chromosome="3",
        position=185793899,
        ref_allele="G",
        alt_allele="T",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.2x increased risk for type-2 diabetes, 1.5x risk for gestational diabetes", "description": "1.2x increased risk for type-2 diabetes, 1.5x risk for gestational diabetes"},
            "GT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.2x increased risk for type-2 diabetes, ~1x risk for gestational diabetes", "description": "1.2x increased risk for type-2 diabetes, ~1x risk for gestational diabetes"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19324937', '22096510', '20424228', '18694974', '19460916'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1121980": UnifiedSNP(
        rsid="rs1121980",
        gene="FTO",
        chromosome="16",
        position=53775335,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.OBESITY],
        genotype_effects={
            "TT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "Moderate increase (2.76x) in risk for obesity", "description": "Moderate increase (2.76x) in risk for obesity"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Slight increase (1.67x) in risk for obesity", "description": "Slight increase (1.67x) in risk for obesity"},
        },
        nutrient_recommendations={
            "TT": [{"nutrient": "Protein", "dose": "1.6-2.0 g/kg/dag", "reason": "Ökar mättnad"}],
            "CT": [{"nutrient": "Protein", "dose": "1.6-2.0 g/kg/dag", "reason": "Ökar mättnad"}],
        },
        lifestyle_recommendations={
            "TT": ['Proteinrik frukost rekommenderas starkt', 'Undvik snacking - håll regelbundna måltider'],
            "CT": ['Proteinrik frukost rekommenderas starkt', 'Undvik snacking - håll regelbundna måltider'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21115529', '30099472', '26935496', '18487448', '18599522'],
        clinical_significance="Note that although",
        evidence_level="SNPedia"
    ),

    "rs3749474": UnifiedSNP(
        rsid="rs3749474",
        gene="CLOCK",
        chromosome="4",
        position=55434518,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.CIRCADIAN],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21172166', '21773969', '19888304', '26181468', '23822714'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs228697": UnifiedSNP(
        rsid="rs228697",
        gene="PER3",
        chromosome="1",
        position=7827519,
        ref_allele="G",
        alt_allele="C",
        categories=[Category.SLEEP],
        genotype_effects={
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Somewhat more likely to prefer staying up late", "description": "Somewhat more likely to prefer staying up late"},
            "CG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Somewhat more likely to prefer staying up late", "description": "Somewhat more likely to prefer staying up late"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['25201053'],
        clinical_significance="Based on a study of 182 DSPT individuals, 67 free-running type (FRT) individuals, and 925 controls, ",
        evidence_level="SNPedia"
    ),

    "rs2298383": UnifiedSNP(
        rsid="rs2298383",
        gene="SPECC1L-ADORA2A",
        chromosome="22",
        position=24429543,
        ref_allele="C",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "increased anxiety in response to caffeine", "description": "increased anxiety in response to caffeine"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22336631', '31817803', '26589317', '20334879', '32615857'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs12722": UnifiedSNP(
        rsid="rs12722",
        gene="LOC101448202",
        chromosome="9",
        position=134842570,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['29632650', '29799806', '19956930', '24755981', '24085259'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2283265": UnifiedSNP(
        rsid="rs2283265",
        gene="DRD2",
        chromosome="11",
        position=113414814,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.STRESS_MOOD],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18332877', '22579533', '19772578', '24495967', '19321766'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2734849": UnifiedSNP(
        rsid="rs2734849",
        gene="ANKK1",
        chromosome="11",
        position=113399438,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['31867628', '18354387'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs6311": UnifiedSNP(
        rsid="rs6311",
        gene="HTR2A",
        chromosome="13",
        position=46897343,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.STRESS_MOOD],
        genotype_effects={
            "CC": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "3.6x increased risk of sexual dysfunction when taking SSRI Antidepressants.", "description": "3.6x increased risk of sexual dysfunction when taking SSRI Antidepressants."},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "Normal (lower) risk of sexual dysfunction when taking SSRI Antidepressants.", "description": "Normal (lower) risk of sexual dysfunction when taking SSRI Antidepressants."},
            "CT": {"risk": RiskLevel.PROTECTIVE, "effect": "Normal risk of sexual dysfunction when taking SSRI Antidepressants.", "description": "Normal risk of sexual dysfunction when taking SSRI Antidepressants."},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21162693', '21172166', '19545856', '29120849', '19911060'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs6313": UnifiedSNP(
        rsid="rs6313",
        gene="HTR2A",
        chromosome="13",
        position=46895805,
        ref_allele="T",
        alt_allele="N",
        categories=[Category.STRESS_MOOD],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "depression, panic, stress response", "description": "depression, panic, stress response"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21089121', '17964050', '20431430', '19545856', '21162693'],
        clinical_significance="Note: the orientation of",
        evidence_level="SNPedia"
    ),

    "rs53576": UnifiedSNP(
        rsid="rs53576",
        gene="OXTR",
        chromosome="3",
        position=8762685,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Lack of empathy?", "description": "Lack of empathy?"},
            "AG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Lack of empathy?", "description": "Lack of empathy?"},
            "GG": {"risk": RiskLevel.PROTECTIVE, "effect": "Optimistic and empathetic; handle stress well", "description": "Optimistic and empathetic; handle stress well"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22809402', '26389606', '23470776', '23708061', '22939719'],
        clinical_significance="rs53576 is a silent G to A change in the oxytocin receptor (OXTR) gene. Studies have demonstrated th",
        evidence_level="SNPedia"
    ),

    "rs4762": UnifiedSNP(
        rsid="rs4762",
        gene="AGT",
        chromosome="1",
        position=230710231,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.CARDIOVASCULAR],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "Note that", "description": "Note that"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23251296', '23716723', '25020710', '28271690', '28361007'],
        clinical_significance="Note that",
        evidence_level="SNPedia"
    ),

    "rs2070744": UnifiedSNP(
        rsid="rs2070744",
        gene="NOS3",
        chromosome="7",
        position=150992991,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.CARDIOVASCULAR],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "increased prostate cancer risk", "description": "increased prostate cancer risk"},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "cardiovascular differences", "description": "cardiovascular differences"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18279468', '28474840', '19701646', '20204503', '18776599'],
        clinical_significance="* Progression (but not occurence) of",
        evidence_level="SNPedia"
    ),

    "rs1800169": UnifiedSNP(
        rsid="rs1800169",
        gene="ZFP91-CNTF",
        chromosome="11",
        position=58624028,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20368905', '16696750', '19833146'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1800012": UnifiedSNP(
        rsid="rs1800012",
        gene="COL1A1",
        chromosome="17",
        position=50200388,
        ref_allele="T",
        alt_allele="N",
        categories=[Category.BONE_HEALTH],
        genotype_effects={
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "Complex; possibly lower risk of ACL ruptures, yet higher risk for bone loss and disc disease", "description": "Complex; possibly lower risk of ACL ruptures, yet higher risk for bone loss and disc disease"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22174012', '22190259', '17903296', '22066665', '20015871'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs679620": UnifiedSNP(
        rsid="rs679620",
        gene="MMP3",
        chromosome="11",
        position=102842889,
        ref_allele="G",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "higher risk for Achilles tendinopathy?", "description": "higher risk for Achilles tendinopathy?"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['32607795', '20622166', '22671570', '22776467', '19064570'],
        clinical_significance="A study of 1418 African-American women and men from the Genetic Epidemiology Network of Arteriopathy",
        evidence_level="SNPedia"
    ),

    "rs7181866": UnifiedSNP(
        rsid="rs7181866",
        gene="GABPB1",
        chromosome="15",
        position=50318595,
        ref_allele="G",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23486860', '22749526', '30904536'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1572312": UnifiedSNP(
        rsid="rs1572312",
        gene="NFIA-AS2",
        chromosome="1",
        position=60952057,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['26231489'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs7832552": UnifiedSNP(
        rsid="rs7832552",
        gene="TRHR",
        chromosome="8",
        position=109103447,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['28294290', '23543262', '19268274'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2854464": UnifiedSNP(
        rsid="rs2854464",
        gene="ACVR1B",
        chromosome="12",
        position=51995107,
        ref_allele="A",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "higher muscle strength", "description": "higher muscle strength"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21063444', '22330029'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs4253778": UnifiedSNP(
        rsid="rs4253778",
        gene="PPARA",
        chromosome="22",
        position=46234737,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22968028', '19653005', '25294067', '26671228', '24784145'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs20541": UnifiedSNP(
        rsid="rs20541",
        gene="IL13",
        chromosome="5",
        position=132660272,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['16759385', '19956102', '23663310', '22023794', '15726497'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs1295686": UnifiedSNP(
        rsid="rs1295686",
        gene="IL13",
        chromosome="5",
        position=132660151,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19956102', '15726497', '21050946', '32678078', '18676870'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2305480": UnifiedSNP(
        rsid="rs2305480",
        gene="GSDMB",
        chromosome="17",
        position=39905943,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "if 4 years old or younger, ~3x increased asthma risk if exposed to smoke", "description": "if 4 years old or younger, ~3x increased asthma risk if exposed to smoke"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "3.5x increase in risk of asthma for Han Chinese", "description": "3.5x increase in risk of asthma for Han Chinese"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20860503', '24241537', '19458352', '27163155', '22469062'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2052129": UnifiedSNP(
        rsid="rs2052129",
        gene="AOC1",
        chromosome="7",
        position=150851884,
        ref_allele="A",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "related to Histamine intolerance", "description": "related to Histamine intolerance"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=[],
        clinical_significance="No association between the promoter SNP",
        evidence_level="SNPedia"
    ),

    "rs780094": UnifiedSNP(
        rsid="rs780094",
        gene="GCKR",
        chromosome="2",
        position=27518370,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['28683826', '23307301', '19096518', '25283508', '18179892'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs17602729": UnifiedSNP(
        rsid="rs17602729",
        gene="AMPD1",
        chromosome="1",
        position=114693436,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.MUSCLE],
        genotype_effects={
            "AA": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "AMPD1 deficiency homozygous (orientation reversed)", "description": "AMPD1 deficiency homozygous (orientation reversed)"},
            "AG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "AMPD1 deficiency heterozygous (orientation reversed)", "description": "AMPD1 deficiency heterozygous (orientation reversed)"},
            "AC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "unexpected genotype", "description": "unexpected genotype"},
            "AT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "Really unexpected!", "description": "Really unexpected!"},
            "TT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "AMPD1 deficiency homozygous", "description": "AMPD1 deficiency homozygous"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "AMPD1 deficiency heterozygous", "description": "AMPD1 deficiency heterozygous"},
            "CG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "unexpected genotype", "description": "unexpected genotype"},
            "GT": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "unexpected genotype", "description": "unexpected genotype"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AA": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['25682119', '26529652', '18974781', '26554440', '18852891'],
        clinical_significance="In fact, heterozygotes for",
        evidence_level="SNPedia"
    ),

    "rs1726866": UnifiedSNP(
        rsid="rs1726866",
        gene="TAS2R38",
        chromosome="7",
        position=141972905,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.PROTECTIVE, "effect": "can taste bitter", "description": "can taste bitter"},
            "TT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "possible unable to taste bitter", "description": "possible unable to taste bitter"},
            "CT": {"risk": RiskLevel.NORMAL, "effect": "can taste bitter", "description": "can taste bitter"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19092995', '18248681', '18834969', '23133589', '19779476'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs10246939": UnifiedSNP(
        rsid="rs10246939",
        gene="TAS2R38",
        chromosome="7",
        position=141972804,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "CC": {"risk": RiskLevel.NORMAL, "effect": "can taste bitter", "description": "can taste bitter"},
            "TT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "possibly unable to taste bitterness", "description": "possibly unable to taste bitterness"},
            "CT": {"risk": RiskLevel.NORMAL, "effect": "can taste bitter", "description": "can taste bitter"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['18248681', '18834969', '23133589', '23966204', '19779476'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs5186": UnifiedSNP(
        rsid="rs5186",
        gene="AGTR1",
        chromosome="3",
        position=148742201,
        ref_allele="A",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "~1.4x increased risk of hypertension", "description": "~1.4x increased risk of hypertension"},
            "CC": {"risk": RiskLevel.SIGNIFICANTLY_INCREASED, "effect": "7.3x increased risk of hypertension", "description": "7.3x increased risk of hypertension"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CC": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['19587357', '19330904', '17588946', '17211857', '18279468'],
        clinical_significance="Pregnant women who are",
        evidence_level="SNPedia"
    ),

    "rs1935949": UnifiedSNP(
        rsid="rs1935949",
        gene="FOXO3",
        chromosome="6",
        position=108678084,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.ANTIOXIDANT],
        genotype_effects={
            "CC": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Reference", "description": "Reference"},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "1.46 OR for reaching \"exceptional longevity\"", "description": "1.46 OR for reaching \"exceptional longevity\""},
            "CT": {"risk": RiskLevel.PROTECTIVE, "effect": "1.27X likelihood of \"exceptional longevity\"", "description": "1.27X likelihood of \"exceptional longevity\""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=[],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs7726159": UnifiedSNP(
        rsid="rs7726159",
        gene="TERT",
        chromosome="5",
        position=1282204,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.ANTIOXIDANT],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['25027329', '20628624', '26294352', '22267287'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs25487": UnifiedSNP(
        rsid="rs25487",
        gene="XRCC1",
        chromosome="19",
        position=43551574,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "0.7x lower risk for skin cancer", "description": "0.7x lower risk for skin cancer"},
            "AG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "2x higher risk for skin cancer; possibly other cancers", "description": "2x higher risk for skin cancer; possibly other cancers"},
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "2x higher risk for skin cancer; possibly other cancers", "description": "2x higher risk for skin cancer; possibly other cancers"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "AG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['30616520', '24172093', '25563194', '24500421', '24084248'],
        clinical_significance="In a study of ~300 Koreans,",
        evidence_level="SNPedia"
    ),

    "rs13181": UnifiedSNP(
        rsid="rs13181",
        gene="ERCC2",
        chromosome="19",
        position=45351661,
        ref_allele="G",
        alt_allele="T",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": ">1.12x increased risk for cutaneous melanoma; possible increase in ovarian cancer risk", "description": ">1.12x increased risk for cutaneous melanoma; possible increase in ovarian cancer risk"},
            "TT": {"risk": RiskLevel.PROTECTIVE, "effect": "Normal risk for cutaneous melanoma", "description": "Normal risk for cutaneous melanoma"},
            "GT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "1.12x increased risk for cutaneous melanoma", "description": "1.12x increased risk for cutaneous melanoma"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['25789018', '23680703', '21826087', '19902366', '21426550'],
        clinical_significance="A preliminary (as yet unreplicated) study of 430 patients with",
        evidence_level="SNPedia"
    ),

    "rs9594759": UnifiedSNP(
        rsid="rs9594759",
        gene="LOC105370177",
        chromosome="13",
        position=42458457,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['22370887', '29528523', '19079262', '23072920'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs3736228": UnifiedSNP(
        rsid="rs3736228",
        gene="LRP5",
        chromosome="11",
        position=68433827,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.BONE_HEALTH],
        genotype_effects={
            "TT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "increased risk for osteoporosis", "description": "increased risk for osteoporosis"},
            "CT": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "increased risk for osteoporosis", "description": "increased risk for osteoporosis"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['25232223', '20960157', '17903296', '23242660', '16723389'],
        clinical_significance="Note that",
        evidence_level="SNPedia"
    ),

    "rs4988300": UnifiedSNP(
        rsid="rs4988300",
        gene="LRP5",
        chromosome="11",
        position=68321363,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.BONE_HEALTH],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['25762437', '18455228', '17903296', '16723389', '17002564'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2230199": UnifiedSNP(
        rsid="rs2230199",
        gene="C3",
        chromosome="19",
        position=6718376,
        ref_allele="G",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "GG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "2.5x+ risk of ARMD", "description": "2.5x+ risk of ARMD"},
            "CG": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "1.6x+ risk of ARMD", "description": "1.6x+ risk of ARMD"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "GG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "CG": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['23337555', '23919682', '27116510', '22361228', '15726497'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs12203592": UnifiedSNP(
        rsid="rs12203592",
        gene="IRF4",
        chromosome="6",
        position=396321,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Primarily in Europeans; more likely presence of freckles, brown hair and high sensitivity of skin to", "description": "Primarily in Europeans; more likely presence of freckles, brown hair and high sensitivity of skin to"},
            "CT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "Primarily in Europeans; likely presence of freckles, brown hair and high sensitivity of skin to sun ", "description": "Primarily in Europeans; likely presence of freckles, brown hair and high sensitivity of skin to sun "},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20463881', '20585627', '22512251', '20602913', '29054604'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs4911414": UnifiedSNP(
        rsid="rs4911414",
        gene="ASIP",
        chromosome="20",
        position=34141638,
        ref_allele="G",
        alt_allele="T",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "TT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "2-4x higher risk of sun sensitivity if part of risk haplotype", "description": "2-4x higher risk of sun sensitivity if part of risk haplotype"},
            "GT": {"risk": RiskLevel.MODERATELY_INCREASED, "effect": "2-4x higher risk of sun sensitivity if part of risk haplotype", "description": "2-4x higher risk of sun sensitivity if part of risk haplotype"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
            "TT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
            "GT": ['Denna variant kan påverka din hälsa - konsultera specialist vid behov'],
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['21221757', '19384953', '22628150', '23548203'],
        clinical_significance="Based on a study by the same authors of 4,000+",
        evidence_level="SNPedia"
    ),

    "rs3087243": UnifiedSNP(
        rsid="rs3087243",
        gene="CTLA4",
        chromosome="2",
        position=203874196,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "AA": {"risk": RiskLevel.PROTECTIVE, "effect": "Normal risk for auto-immune diseases", "description": "Normal risk for auto-immune diseases"},
            "AG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "increased risk for auto-immune diseases", "description": "increased risk for auto-immune diseases"},
            "GG": {"risk": RiskLevel.SLIGHTLY_INCREASED, "effect": "Increased risk for autoimmune diseases", "description": "Increased risk for autoimmune diseases"},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['27888068', '18776148', '22891215', '29979892', '24270470'],
        clinical_significance="In a study of 395 Spanish patients with",
        evidence_level="SNPedia"
    ),

    "rs4293393": UnifiedSNP(
        rsid="rs4293393",
        gene="UMOD",
        chromosome="16",
        position=20353266,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20686651', '19959715', '20222955'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

    "rs2467853": UnifiedSNP(
        rsid="rs2467853",
        gene="SPATA5L1",
        chromosome="15",
        position=45406595,
        ref_allele="N",
        alt_allele="N",
        categories=[Category.INFLAMMATION],
        genotype_effects={
            "normal": {"risk": RiskLevel.NORMAL, "effect": "", "description": ""},
        },
        nutrient_recommendations={
        },
        lifestyle_recommendations={
        },
        drug_interactions={},
        pathways=[],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.0, "EAS": 0.0, "AFR": 0.0},
        pmids=['20686651', '19430482', '20222955'],
        clinical_significance="Auto-fetched from SNPedia",
        evidence_level="SNPedia"
    ),

}

def add_clinical_auto_snps():
    """Add auto-fetched SNPs to database"""
    for rsid, snp in AUTO_FETCHED_SNPS.items():
        if rsid not in UNIFIED_DATABASE:
            UNIFIED_DATABASE[rsid] = snp
    return len(AUTO_FETCHED_SNPS)

# Auto-add on import
_added = add_clinical_auto_snps()
print(f"Lade till {_added} kliniska auto-SNPs")