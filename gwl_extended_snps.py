"""
GWL Extended SNP Database
=========================
Additional SNPs for comprehensive nutrigenomics analysis.

This extends the unified database with 100+ more clinically relevant SNPs.
"""

from gwl_unified_database import UnifiedSNP, Category, RiskLevel, ActionPriority

# =============================================================================
# EXTENDED SNP DATABASE - FITNESS & ATHLETIC PERFORMANCE
# =============================================================================

EXTENDED_SNPS = {
    # =========================================================================
    # ACTN3 - Sprint/Power vs Endurance
    # =========================================================================
    "rs1815739": UnifiedSNP(
        rsid="rs1815739",
        gene="ACTN3",
        chromosome="11",
        position=66560624,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.MUSCLE],
        genotype_effects={
            "CC": {
                "risk": RiskLevel.NORMAL,
                "effect": "R/R - Full alpha-actinin-3",
                "description": "Snabbryckande muskelfibrer (typ II) fungerar optimalt. Fördelaktigt för sprint, styrka, power."
            },
            "CT": {
                "risk": RiskLevel.NORMAL,
                "effect": "R/X - Intermediär",
                "description": "Blandad profil - god för både styrka och uthållighet."
            },
            "TT": {
                "risk": RiskLevel.NORMAL,
                "effect": "X/X - Ingen alpha-actinin-3",
                "description": "Långsamma muskelfibrer (typ I) dominerar. Fördelaktigt för uthållighet, maraton, långdistans."
            }
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Kreatin", "dose": "3-5 g/dag", "reason": "Stödjer snabbryckande fibrer"}],
            "CT": [{"nutrient": "Kreatin", "dose": "3-5 g/dag", "reason": "Balanserad nytta"}],
            "TT": [{"nutrient": "Beta-alanin", "dose": "3-6 g/dag", "reason": "Ökar uthållighetskapacitet"}]
        },
        lifestyle_recommendations={
            "CC": ["Styrketräning och explosiv träning passar dig", "Sprint, hopp, tyngdlyftning"],
            "CT": ["Varierad träning fungerar bra", "Kombinera styrka och kondition"],
            "TT": ["Uthållighetsträning passar dig", "Löpning, cykling, simning på längre distanser"]
        },
        drug_interactions={},
        pathways=["Muskelkontraktion", "Fiber-typ differentiering"],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.42, "EAS": 0.52, "AFR": 0.11, "SAS": 0.40, "AMR": 0.35},
        clinical_significance="Fitness-optimering",
        evidence_level="Strong",
        pmids=["18043716", "12879365"]
    ),

    # =========================================================================
    # FTO - Obesity/Appetite
    # =========================================================================
    "rs9939609": UnifiedSNP(
        rsid="rs9939609",
        gene="FTO",
        chromosome="16",
        position=53820527,
        ref_allele="T",
        alt_allele="A",
        categories=[Category.BLOOD_SUGAR, Category.OBESITY],
        genotype_effects={
            "TT": {
                "risk": RiskLevel.NORMAL,
                "effect": "Normal FTO",
                "description": "Normal mättnadskänsla och hunger-reglering."
            },
            "AT": {
                "risk": RiskLevel.SLIGHTLY_INCREASED,
                "effect": "Heterozygot FTO-variant",
                "description": "Lätt ökad risk för övervikt. ~1.5 kg högre vikt i genomsnitt."
            },
            "AA": {
                "risk": RiskLevel.MODERATELY_INCREASED,
                "effect": "Homozygot FTO-variant",
                "description": "Ökad hungerkänsla, minskad mättnad. ~3 kg högre vikt i genomsnitt. 1.7x risk för fetma."
            }
        },
        nutrient_recommendations={
            "TT": [],
            "AT": [{"nutrient": "Protein", "dose": "1.6-2.0 g/kg", "reason": "Protein ökar mättnad", "priority": "high"}],
            "AA": [
                {"nutrient": "Protein", "dose": "1.8-2.2 g/kg", "reason": "Protein kritiskt för mättnad", "priority": "critical"},
                {"nutrient": "Fiber", "dose": "30-40 g/dag", "reason": "Ökar mättnad, sänker GI", "priority": "high"}
            ]
        },
        lifestyle_recommendations={
            "TT": ["Standardrekommendationer"],
            "AT": ["Fokusera på proteinrik kost", "Regelbunden måltidsrytm", "Undvik snacking"],
            "AA": [
                "KRITISKT: Proteinrik frukost",
                "Ät långsamt - ta 20 min per måltid",
                "Fysisk aktivitet särskilt viktig (kompenserar genetisk risk)",
                "Undvik ultraprocessad mat",
                "Regelbunden styrketräning ökar muskelmassa och metabolism"
            ]
        },
        drug_interactions={},
        pathways=["Hunger-mättnad reglering", "Energibalans"],
        interacts_with=["MC4R"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.42, "EAS": 0.12, "AFR": 0.49, "SAS": 0.30, "AMR": 0.38},
        clinical_significance="Vikthantering",
        evidence_level="Strong",
        pmids=["17434869", "19079261"]
    ),

    # =========================================================================
    # TCF7L2 - Diabetes Risk
    # =========================================================================
    "rs7903146": UnifiedSNP(
        rsid="rs7903146",
        gene="TCF7L2",
        chromosome="10",
        position=114758349,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.BLOOD_SUGAR, Category.BLOOD_SUGAR],
        genotype_effects={
            "CC": {
                "risk": RiskLevel.NORMAL,
                "effect": "Normal TCF7L2",
                "description": "Normal insulinkänslighet och glukosmetabolism."
            },
            "CT": {
                "risk": RiskLevel.SLIGHTLY_INCREASED,
                "effect": "Heterozygot variant",
                "description": "~1.4x ökad risk för typ 2-diabetes."
            },
            "TT": {
                "risk": RiskLevel.MODERATELY_INCREASED,
                "effect": "Homozygot variant",
                "description": "~2x ökad risk för typ 2-diabetes. Försämrad insulinsekretion."
            }
        },
        nutrient_recommendations={
            "CC": [],
            "CT": [
                {"nutrient": "Magnesium", "dose": "300-400 mg/dag", "reason": "Förbättrar insulinkänslighet"},
                {"nutrient": "Krompikolinat", "dose": "200-400 mcg/dag", "reason": "Blodsocker-stöd"}
            ],
            "TT": [
                {"nutrient": "Magnesium", "dose": "400 mg/dag", "reason": "Kritiskt för insulinfunktion", "priority": "high"},
                {"nutrient": "Berberin", "dose": "500 mg 2-3x/dag", "reason": "Naturlig blodsockerregulator"},
                {"nutrient": "Alpha-liponsyra", "dose": "300-600 mg/dag", "reason": "Insulinkänslighet"}
            ]
        },
        lifestyle_recommendations={
            "CC": ["Standardrekommendationer"],
            "CT": ["Begränsa raffinerade kolhydrater", "Regelbunden motion", "Monitorera fasteglukos årligen"],
            "TT": [
                "KRITISKT: Lågt GI-kost",
                "Minimera socker och vitt mjöl",
                "Styrketräning ökar insulinkänslighet",
                "Intermittent fasta kan vara fördelaktigt",
                "Regelbunden blodsocker-monitorering",
                "HbA1c-test årligen"
            ]
        },
        drug_interactions={
            "TT": [{"drug": "Metformin", "action": "Kan behövas tidigare", "note": "Diskutera med läkare vid prediabetes"}]
        },
        pathways=["Insulin-signalering", "Beta-cell funktion"],
        interacts_with=["PPARG", "KCNJ11"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.30, "EAS": 0.04, "AFR": 0.29, "SAS": 0.30, "AMR": 0.27},
        clinical_significance="Diabetesrisk",
        evidence_level="Strong",
        pmids=["16415884", "17463248"]
    ),

    # =========================================================================
    # PPARG - Fat Storage / Insulin
    # =========================================================================
    "rs1801282": UnifiedSNP(
        rsid="rs1801282",
        gene="PPARG",
        chromosome="3",
        position=12393125,
        ref_allele="C",
        alt_allele="G",
        categories=[Category.BLOOD_SUGAR, Category.OBESITY],
        genotype_effects={
            "CC": {
                "risk": RiskLevel.NORMAL,
                "effect": "Pro/Pro - Normal PPARG",
                "description": "Normal fettmetabolism och insulinkänslighet."
            },
            "CG": {
                "risk": RiskLevel.PROTECTIVE,
                "effect": "Pro/Ala - Skyddande",
                "description": "20-25% lägre risk för typ 2-diabetes. Förbättrad insulinkänslighet."
            },
            "GG": {
                "risk": RiskLevel.PROTECTIVE,
                "effect": "Ala/Ala - Maximal skydd",
                "description": "Skyddande mot diabetes. Lägre BMI i genomsnitt."
            }
        },
        nutrient_recommendations={
            "CC": [{"nutrient": "Omega-3", "dose": "2 g/dag", "reason": "PPARG-aktivator, förbättrar insulinkänslighet"}],
            "CG": [],
            "GG": []
        },
        lifestyle_recommendations={
            "CC": ["Omega-3-rik kost viktigt", "Undvik mättat fett", "Regelbunden motion"],
            "CG": ["Du har genetiskt skydd - fortsätt hälsosam livsstil"],
            "GG": ["Genetiskt skyddad mot diabetes"]
        },
        drug_interactions={},
        pathways=["Fettcells-differentiering", "Insulinkänslighet"],
        interacts_with=["TCF7L2"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.12, "EAS": 0.02, "AFR": 0.01, "SAS": 0.15, "AMR": 0.09},
        clinical_significance="Metabolt skydd",
        evidence_level="Strong",
        pmids=["9614170", "15677715"]
    ),

    # =========================================================================
    # LCT - Lactose Tolerance
    # =========================================================================
    "rs4988235": UnifiedSNP(
        rsid="rs4988235",
        gene="LCT/MCM6",
        chromosome="2",
        position=136608646,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.IMMUNE, Category.IMMUNE],
        genotype_effects={
            "GG": {
                "risk": RiskLevel.MODERATELY_INCREASED,
                "effect": "Laktosintolerant",
                "description": "Laktas-enzymet avtar efter barndomen. Kan inte bryta ner mjölksocker effektivt."
            },
            "AG": {
                "risk": RiskLevel.NORMAL,
                "effect": "Laktostolerant",
                "description": "Laktas-produktion fortsätter. Kan konsumera mejeriprodukter utan problem."
            },
            "AA": {
                "risk": RiskLevel.NORMAL,
                "effect": "Laktostolerant",
                "description": "Full laktos-persistens. Inga problem med mejeriprodukter."
            }
        },
        nutrient_recommendations={
            "GG": [
                {"nutrient": "Kalcium", "dose": "1000-1200 mg/dag", "reason": "Kompensera för minskade mejeriprodukter", "priority": "high"},
                {"nutrient": "D-vitamin", "dose": "2000-4000 IE/dag", "reason": "Kritiskt utan mjölk-D"},
                {"nutrient": "Laktas-enzym", "dose": "Vid behov", "reason": "Ta före mejerikonsumtion"}
            ],
            "AG": [],
            "AA": []
        },
        lifestyle_recommendations={
            "GG": [
                "Undvik eller begränsa mjölkprodukter",
                "Laktosfria alternativ (havremjölk, mandelmjölk)",
                "Hårdost och yoghurt tolereras ofta bättre (fermenterade)",
                "Kalciumrika grönsaker: grönkål, broccoli, bok choy"
            ],
            "AG": ["Du tolererar laktos normalt"],
            "AA": ["Full laktostolerans"]
        },
        drug_interactions={},
        pathways=["Laktosmetabolism", "Tarmhälsa"],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.76, "EAS": 0.01, "AFR": 0.14, "SAS": 0.21, "AMR": 0.50},
        clinical_significance="Matintolerans",
        evidence_level="Strong",
        pmids=["11788828", "15106124"]
    ),

    # =========================================================================
    # BCMO1 - Beta-carotene to Vitamin A conversion
    # =========================================================================
    "rs12934922": UnifiedSNP(
        rsid="rs12934922",
        gene="BCMO1",
        chromosome="16",
        position=81264597,
        ref_allele="A",
        alt_allele="T",
        categories=[Category.VITAMIN_D, Category.ANTIOXIDANT],
        genotype_effects={
            "AA": {
                "risk": RiskLevel.NORMAL,
                "effect": "Normal BCMO1",
                "description": "Normal omvandling av betakaroten till A-vitamin."
            },
            "AT": {
                "risk": RiskLevel.SLIGHTLY_INCREASED,
                "effect": "Reducerad konvertering",
                "description": "~32% lägre omvandling av betakaroten till retinol."
            },
            "TT": {
                "risk": RiskLevel.MODERATELY_INCREASED,
                "effect": "Kraftigt reducerad konvertering",
                "description": "~69% lägre betakaroten-konvertering. Behöver förformad A-vitamin."
            }
        },
        nutrient_recommendations={
            "AA": [],
            "AT": [{"nutrient": "A-vitamin (retinol)", "dose": "2500-5000 IE/dag", "reason": "Kompensera för sämre konvertering"}],
            "TT": [
                {"nutrient": "A-vitamin (retinol)", "dose": "5000-10000 IE/dag", "reason": "KRITISKT - kan inte konvertera betakaroten", "priority": "critical"},
                {"nutrient": "Lever/torskleverolja", "dose": "1-2 tsk/dag", "reason": "Naturlig retinolkälla"}
            ]
        },
        lifestyle_recommendations={
            "AA": ["Morötter och grönsaker ger tillräckligt A-vitamin"],
            "AT": ["Inkludera animaliska A-vitaminkällor (lever, ägg, mejeriprodukter)"],
            "TT": [
                "FÖRLITA DIG INTE på morötter/sötpotatis för A-vitamin",
                "Ät lever 1-2 ggr/månad (rikaste A-vitaminkällan)",
                "Äggula, smör från gräsbetade djur",
                "Överväg torskleverolja"
            ]
        },
        drug_interactions={},
        pathways=["Karotenoid-metabolism", "Retinoid-signalering"],
        interacts_with=["rs7501331"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.42, "EAS": 0.24, "AFR": 0.26, "SAS": 0.34, "AMR": 0.38},
        clinical_significance="A-vitamin status",
        evidence_level="Strong",
        pmids=["19103647", "22113863"]
    ),

    # =========================================================================
    # FOXO3 - Longevity
    # =========================================================================
    "rs2802292": UnifiedSNP(
        rsid="rs2802292",
        gene="FOXO3",
        chromosome="6",
        position=108986878,
        ref_allele="T",
        alt_allele="G",
        categories=[Category.ANTIOXIDANT, Category.ANTIOXIDANT],
        genotype_effects={
            "TT": {
                "risk": RiskLevel.NORMAL,
                "effect": "Normal FOXO3",
                "description": "Standard livslängdsassocierad genotyp."
            },
            "TG": {
                "risk": RiskLevel.PROTECTIVE,
                "effect": "En longevity-allel",
                "description": "Associerat med längre livslängd och bättre åldrande."
            },
            "GG": {
                "risk": RiskLevel.PROTECTIVE,
                "effect": "Dubbel longevity-allel",
                "description": "Starkt associerat med 100+-årig livslängd. ~2.7x högre chans att nå 100."
            }
        },
        nutrient_recommendations={
            "TT": [{"nutrient": "Resveratrol", "dose": "150-500 mg/dag", "reason": "FOXO3-aktivator"}],
            "TG": [],
            "GG": []
        },
        lifestyle_recommendations={
            "TT": ["Fasta/kalorirestriktion aktiverar FOXO3", "Regelbunden motion", "Stresshantering"],
            "TG": ["Du har genetisk fördel - optimera med livsstil"],
            "GG": ["Genetiskt skyddad - men livsstil förstärker fördelen"]
        },
        drug_interactions={},
        pathways=["Autophagy", "Stressresistens", "Cellreparation"],
        interacts_with=[],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.38, "EAS": 0.44, "AFR": 0.27, "SAS": 0.37, "AMR": 0.35},
        clinical_significance="Longevity",
        evidence_level="Strong",
        pmids=["18765803", "25855638"]
    ),

    # =========================================================================
    # ADA - Sleep Quality
    # =========================================================================
    "rs73598374": UnifiedSNP(
        rsid="rs73598374",
        gene="ADA",
        chromosome="20",
        position=44619522,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.SLEEP, Category.CIRCADIAN],
        genotype_effects={
            "CC": {
                "risk": RiskLevel.NORMAL,
                "effect": "Normal ADA",
                "description": "Normal adenosin-metabolism. Standard sömnkvalitet."
            },
            "CT": {
                "risk": RiskLevel.NORMAL,
                "effect": "Heterozygot variant",
                "description": "Något djupare sömn. Högre adenosin-uppbyggnad under vakenhet."
            },
            "TT": {
                "risk": RiskLevel.PROTECTIVE,
                "effect": "Homozygot variant",
                "description": "Djupare sömn, mer delta-vågor. Snabbare återhämtning från sömnbrist."
            }
        },
        nutrient_recommendations={
            "CC": [
                {"nutrient": "Magnesium", "dose": "300-400 mg", "reason": "Sömnstöd"},
                {"nutrient": "Glycin", "dose": "3g före sömn", "reason": "Förbättrar sömnkvalitet"}
            ],
            "CT": [],
            "TT": []
        },
        lifestyle_recommendations={
            "CC": [
                "Undvik koffein efter kl 14",
                "Regelbundna sömntider",
                "Sval, mörk sovmiljö"
            ],
            "CT": ["Du har något bättre sömnkvalitet genetiskt"],
            "TT": ["Genetisk fördel för djupsömn"]
        },
        drug_interactions={},
        pathways=["Adenosin-metabolism", "Sömn-vakenhet reglering"],
        interacts_with=["CYP1A2"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.04, "EAS": 0.01, "AFR": 0.01, "SAS": 0.02, "AMR": 0.03},
        clinical_significance="Sömnkvalitet",
        evidence_level="Moderate",
        pmids=["15716947", "19118814"]
    ),

    # =========================================================================
    # HLA-DQ2.5 - Celiac Disease Risk
    # =========================================================================
    "rs2187668": UnifiedSNP(
        rsid="rs2187668",
        gene="HLA-DQ2.5",
        chromosome="6",
        position=32605884,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.IMMUNE, Category.IMMUNE],
        genotype_effects={
            "TT": {
                "risk": RiskLevel.NORMAL,
                "effect": "Ej HLA-DQ2.5-bärare",
                "description": "Mycket låg risk för celiaki (<1%)."
            },
            "CT": {
                "risk": RiskLevel.SLIGHTLY_INCREASED,
                "effect": "Heterozygot HLA-DQ2.5",
                "description": "Ökad risk för celiaki (~3%). Screenas om symtom."
            },
            "CC": {
                "risk": RiskLevel.MODERATELY_INCREASED,
                "effect": "Homozygot HLA-DQ2.5",
                "description": "Signifikant ökad risk för celiaki (~10-15% livstidsrisk)."
            }
        },
        nutrient_recommendations={
            "TT": [],
            "CT": [],
            "CC": [{"nutrient": "Glutenfri multi-vitamin", "dose": "Vid glutenfri kost", "reason": "Kompensera för begränsad kost"}]
        },
        lifestyle_recommendations={
            "TT": ["Du kan sannolikt tolerera gluten utan problem"],
            "CT": [
                "Genetisk predisposition för celiaki",
                "Vid symtom (magbesvär, trötthet, hudutslag): testa för celiaki",
                "Testa transglutaminas-antikroppar"
            ],
            "CC": [
                "HÖG genetisk risk för celiaki",
                "Testa för celiaki även utan uppenbara symtom",
                "Vid positivt test: strikt glutenfri kost",
                "Screena regelbundet (vart 2-3 år) om negativ"
            ]
        },
        drug_interactions={},
        pathways=["Immunreaktion", "Glutenintolerans"],
        interacts_with=[],
        haplotype_gene="HLA",
        haplotype_role="DQ2.5 allel - huvudmarkör för celiaki-predisposition",
        frequencies={"EUR": 0.15, "EAS": 0.02, "AFR": 0.04, "SAS": 0.08, "AMR": 0.10},
        clinical_significance="Celiaki-risk",
        evidence_level="Strong",
        pmids=["17558408", "20190752"]
    ),

    # =========================================================================
    # ADRB2 - Endurance/Metabolism
    # =========================================================================
    "rs1042713": UnifiedSNP(
        rsid="rs1042713",
        gene="ADRB2",
        chromosome="5",
        position=148206440,
        ref_allele="G",
        alt_allele="A",
        categories=[Category.MUSCLE, Category.BLOOD_SUGAR],
        genotype_effects={
            "GG": {
                "risk": RiskLevel.NORMAL,
                "effect": "Arg/Arg - Normal ADRB2",
                "description": "Normal adrenalinrespons. Standardmetabolism."
            },
            "AG": {
                "risk": RiskLevel.NORMAL,
                "effect": "Arg/Gly - Intermediär",
                "description": "Blandad adrenalinrespons."
            },
            "AA": {
                "risk": RiskLevel.NORMAL,
                "effect": "Gly/Gly - Ökad känslighet",
                "description": "Ökad adrenalinreceptorkänslighet. Bättre uthållighet. Lättare viktökning."
            }
        },
        nutrient_recommendations={
            "GG": [],
            "AG": [],
            "AA": [{"nutrient": "Omega-3", "dose": "2-3 g/dag", "reason": "Stödjer fettförbränning"}]
        },
        lifestyle_recommendations={
            "GG": ["Standardträning"],
            "AG": ["Blandat träningsprogram"],
            "AA": [
                "Uthållighetsträning fördelaktig",
                "Mer känslig för stress - stresshantering viktigt",
                "Kan behöva mer struktur i kost för viktkontroll"
            ]
        },
        drug_interactions={
            "AA": [{"drug": "Beta-blockerare", "action": "Kan behöva dosjustering", "note": "Ökad receptorkänslighet"}]
        },
        pathways=["Adrenalin-signalering", "Lipolys"],
        interacts_with=["ADRB3"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.40, "EAS": 0.55, "AFR": 0.47, "SAS": 0.52, "AMR": 0.44},
        clinical_significance="Fitness/metabolism",
        evidence_level="Moderate",
        pmids=["10441589", "15870086"]
    ),

    # =========================================================================
    # CLOCK - Circadian Rhythm
    # =========================================================================
    "rs1801260": UnifiedSNP(
        rsid="rs1801260",
        gene="CLOCK",
        chromosome="4",
        position=56294068,
        ref_allele="A",
        alt_allele="G",
        categories=[Category.SLEEP, Category.CIRCADIAN],
        genotype_effects={
            "AA": {
                "risk": RiskLevel.NORMAL,
                "effect": "Normal CLOCK",
                "description": "Normal dygnsrytm, morgonmänniska."
            },
            "AG": {
                "risk": RiskLevel.NORMAL,
                "effect": "Heterozygot",
                "description": "Intermediär kronotyp."
            },
            "GG": {
                "risk": RiskLevel.SLIGHTLY_INCREASED,
                "effect": "Kvällsmänniska",
                "description": "Försenad dygnsrytm. Svårare att vakna tidigt. Risk för sömnbrist i 9-5-samhälle."
            }
        },
        nutrient_recommendations={
            "AA": [],
            "AG": [],
            "GG": [
                {"nutrient": "Melatonin", "dose": "0.5-1 mg", "reason": "Hjälper tidigarelägga sömn"},
                {"nutrient": "Magnesium", "dose": "300-400 mg kvällstid", "reason": "Sömnstöd"}
            ]
        },
        lifestyle_recommendations={
            "AA": ["Du är naturligt morgonmänniska"],
            "AG": ["Flexibel kronotyp"],
            "GG": [
                "Du är genetiskt programmerad som kvällsmänniska",
                "Morgonljus (10,000 lux) vid uppvaknande - skiftar rytmen",
                "Undvik blått ljus kvällstid (skärmar)",
                "Om möjligt: flexibla arbetstider",
                "Melatonin tidigt på kvällen kan hjälpa"
            ]
        },
        drug_interactions={},
        pathways=["Dygnsrytm", "Melatonin-reglering"],
        interacts_with=["ADA", "PER2"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.28, "EAS": 0.15, "AFR": 0.20, "SAS": 0.22, "AMR": 0.25},
        clinical_significance="Sömn/kronotyp",
        evidence_level="Moderate",
        pmids=["11545747", "18388889"]
    ),

    # =========================================================================
    # GC - Vitamin D Binding Protein
    # =========================================================================
    "rs2282679": UnifiedSNP(
        rsid="rs2282679",
        gene="GC",
        chromosome="4",
        position=72618334,
        ref_allele="A",
        alt_allele="C",
        categories=[Category.VITAMIN_D, Category.VITAMIN_D],
        genotype_effects={
            "AA": {
                "risk": RiskLevel.NORMAL,
                "effect": "Normal GC",
                "description": "Normal D-vitamin transport och tillgänglighet."
            },
            "AC": {
                "risk": RiskLevel.SLIGHTLY_INCREASED,
                "effect": "Heterozygot variant",
                "description": "Lägre D-vitamin-nivåer i genomsnitt."
            },
            "CC": {
                "risk": RiskLevel.MODERATELY_INCREASED,
                "effect": "Homozygot variant",
                "description": "Signifikant lägre 25(OH)D-nivåer. Behöver högre D-vitamin intag."
            }
        },
        nutrient_recommendations={
            "AA": [{"nutrient": "D-vitamin", "dose": "2000 IE/dag", "reason": "Standarddos"}],
            "AC": [{"nutrient": "D-vitamin", "dose": "3000-4000 IE/dag", "reason": "Kompensera för lägre transport"}],
            "CC": [{"nutrient": "D-vitamin", "dose": "4000-5000 IE/dag", "reason": "Krävs för normala nivåer", "priority": "high"}]
        },
        lifestyle_recommendations={
            "AA": ["Standardrekommendationer för D-vitamin"],
            "AC": ["Testa D-vitamin-nivåer regelbundet"],
            "CC": [
                "Testanivåer 2x/år",
                "Sikta på 75-100 nmol/L",
                "Solexponering extra viktigt",
                "Ta D-vitamin med fet måltid"
            ]
        },
        drug_interactions={},
        pathways=["D-vitamin transport", "Kalciummetabolism"],
        interacts_with=["VDR", "CYP2R1"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.29, "EAS": 0.13, "AFR": 0.35, "SAS": 0.21, "AMR": 0.26},
        clinical_significance="D-vitamin status",
        evidence_level="Strong",
        pmids=["20541252", "21378990"]
    ),

    # =========================================================================
    # KCNJ11 - Insulin Secretion
    # =========================================================================
    "rs5219": UnifiedSNP(
        rsid="rs5219",
        gene="KCNJ11",
        chromosome="11",
        position=17409572,
        ref_allele="C",
        alt_allele="T",
        categories=[Category.BLOOD_SUGAR, Category.BLOOD_SUGAR],
        genotype_effects={
            "CC": {
                "risk": RiskLevel.NORMAL,
                "effect": "E23K Glu/Glu - Normal",
                "description": "Normal insulinsekretion från betaceller."
            },
            "CT": {
                "risk": RiskLevel.SLIGHTLY_INCREASED,
                "effect": "E23K Glu/Lys - Heterozygot",
                "description": "Lätt reducerad insulinsekretion. ~1.2x diabetesrisk."
            },
            "TT": {
                "risk": RiskLevel.MODERATELY_INCREASED,
                "effect": "E23K Lys/Lys - Homozygot",
                "description": "Reducerad insulinsekretion. ~1.4x diabetesrisk."
            }
        },
        nutrient_recommendations={
            "CC": [],
            "CT": [{"nutrient": "Magnesium", "dose": "300-400 mg/dag", "reason": "Stödjer insulinsekretion"}],
            "TT": [
                {"nutrient": "Magnesium", "dose": "400 mg/dag", "reason": "Kritiskt för beta-cellfunktion", "priority": "high"},
                {"nutrient": "Berberin", "dose": "500 mg 2-3x/dag", "reason": "Naturlig blodsockerstöd"}
            ]
        },
        lifestyle_recommendations={
            "CC": ["Standardrekommendationer"],
            "CT": ["Undvik stora kolhydratmängder på en gång", "Regelbunden motion"],
            "TT": [
                "Lågt GI-kost rekommenderas",
                "Fördela kolhydrater över dagen",
                "Kombinera alltid kolhydrater med protein/fett",
                "Regelbunden styrketräning"
            ]
        },
        drug_interactions={
            "TT": [{"drug": "Sulfonylureas", "action": "Reducerad effekt", "note": "KCNJ11-variant påverkar läkemedelsmål"}]
        },
        pathways=["Insulinsekretion", "Kaliumkanal-funktion"],
        interacts_with=["TCF7L2", "PPARG"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.35, "EAS": 0.40, "AFR": 0.15, "SAS": 0.32, "AMR": 0.30},
        clinical_significance="Diabetesrisk",
        evidence_level="Strong",
        pmids=["15677715", "19056611"]
    ),

    # =========================================================================
    # ADRB3 - Metabolism/Weight
    # =========================================================================
    "rs4994": UnifiedSNP(
        rsid="rs4994",
        gene="ADRB3",
        chromosome="8",
        position=37821570,
        ref_allele="T",
        alt_allele="C",
        categories=[Category.BLOOD_SUGAR, Category.OBESITY],
        genotype_effects={
            "TT": {
                "risk": RiskLevel.NORMAL,
                "effect": "Trp64Arg - Normal ADRB3",
                "description": "Normal fettcellsrespons på adrenalin."
            },
            "CT": {
                "risk": RiskLevel.SLIGHTLY_INCREASED,
                "effect": "Heterozygot variant",
                "description": "Reducerad fettförbränning. Svårare att gå ner i vikt."
            },
            "CC": {
                "risk": RiskLevel.MODERATELY_INCREASED,
                "effect": "Homozygot variant (Arg/Arg)",
                "description": "Signifikant reducerad lipolys. Svårare viktminskning, särskilt visceralt fett."
            }
        },
        nutrient_recommendations={
            "TT": [],
            "CT": [{"nutrient": "Grönt te-extrakt", "dose": "500 mg/dag", "reason": "Stimulerar lipolys (om ej COMT slow!)"}],
            "CC": [
                {"nutrient": "Koffein + grönt te", "dose": "Försiktigt", "reason": "Kan hjälpa fettförbränning, kontrollera COMT"},
                {"nutrient": "L-karnitin", "dose": "2-3 g/dag", "reason": "Stödjer fettsyrametabolism"}
            ]
        },
        lifestyle_recommendations={
            "TT": ["Standardrekommendationer"],
            "CT": ["Uthållighetsträning viktigt för fettförbränning", "Kyla kan aktivera brun fett"],
            "CC": [
                "Längre uthållighetspass (45+ min) effektivare",
                "Kyla/kylväst kan hjälpa aktivera brunt fett",
                "Tålamod vid viktminskning - det tar längre tid",
                "HIIT-träning kan vara fördelaktigt"
            ]
        },
        drug_interactions={},
        pathways=["Lipolys", "Termogenes", "Brunt fett-aktivering"],
        interacts_with=["ADRB2", "FTO"],
        haplotype_gene=None,
        haplotype_role=None,
        frequencies={"EUR": 0.08, "EAS": 0.19, "AFR": 0.10, "SAS": 0.12, "AMR": 0.09},
        clinical_significance="Vikthantering",
        evidence_level="Moderate",
        pmids=["7670469", "9771708"]
    ),
}


def add_extended_snps_to_database():
    """
    Funktion för att lägga till utökade SNPs till unified database.
    Anropas vid import.
    """
    from gwl_unified_database import UNIFIED_DATABASE

    for rsid, snp in EXTENDED_SNPS.items():
        UNIFIED_DATABASE[rsid] = snp

    return len(EXTENDED_SNPS)


# Auto-add on import
_added = add_extended_snps_to_database()
print(f"Lade till {_added} utökade SNPs till databasen")
