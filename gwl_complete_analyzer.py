#!/usr/bin/env python3
"""
Genetic Wellness Labs - Komplett DNA-analysverktyg
===================================================
Skapar en fullständig "instruktionsmanual" för din genetik baserad på
evidensbaserad forskning från PubMed.

Version: 2.0.0
"""

import os
import sys
import io
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from datetime import datetime
from collections import defaultdict

# Importera gendatabasen
from gwl_gene_database import (
    GENE_DATABASE, GeneVariant, Category, EvidenceLevel, RiskLevel,
    get_gene_dict, get_genes_by_category, Reference
)


@dataclass
class AnalysisResult:
    """Resultat för en enskild genetisk analys"""
    variant: GeneVariant
    genotype: str
    risk_level: RiskLevel
    interpretation: str


@dataclass
class GeneInteraction:
    """Interaktion mellan gener"""
    genes: List[str]  # rsids
    name: str
    condition: str  # Villkor för interaktion
    effect: str
    recommendation: str


@dataclass
class SupplementRecommendation:
    """Supplement-rekommendation"""
    name: str
    dosage: str
    timing: str
    reason: str
    priority: int  # 1-5
    evidence: EvidenceLevel
    genes_involved: List[str]
    contraindications: List[str] = field(default_factory=list)


@dataclass
class LifestyleRecommendation:
    """Livsstilsrekommendation"""
    category: str
    recommendation: str
    reason: str
    genes_involved: List[str]
    priority: int


# =============================================================================
# GEN-INTERAKTIONER - Viktiga kombinationer
# =============================================================================

GENE_INTERACTIONS = [
    GeneInteraction(
        genes=["rs1801133", "rs1801131"],  # MTHFR C677T + A1298C
        name="MTHFR Compound Heterozygot",
        condition="rs1801133=AG AND rs1801131=GT",
        effect="Kombinerad MTHFR-påverkan kan ge kliniskt signifikant reducerad metylering även om vardera variant är heterozygot.",
        recommendation="Överväg metylfolat + metyl-B12. Kontrollera homocystein."
    ),
    GeneInteraction(
        genes=["rs429358", "rs7412"],  # APOE ε4 + ε2
        name="APOE Haplotyp",
        condition="Kombinerar till ε2/ε2, ε2/ε3, ε3/ε3, ε3/ε4, ε4/ε4",
        effect="APOE-haplotyp är kritisk för hjärt-kärl och hjärnhälsa.",
        recommendation="ε4-bärare: Begränsa mättat fett, optimera omega-3. ε2-bärare: Generellt skyddande."
    ),
    GeneInteraction(
        genes=["rs174546", "rs1535"],  # FADS1 + FADS2
        name="FADS1/2 Dubbelrisk",
        condition="Riskalleler i båda",
        effect="Dubbel FADS-påverkan ger kraftigt reducerad omega-3-omvandling.",
        recommendation="Marin EPA/DHA absolut nödvändigt. Växtbaserad ALA otillräcklig."
    ),
    GeneInteraction(
        genes=["rs4680", "rs762551"],  # COMT + CYP1A2
        name="COMT + Koffein",
        condition="COMT AA (slow) AND CYP1A2 CC (slow)",
        effect="Långsam COMT + långsam koffein = förlängd katekolamineffekt av koffein. Kan ge ångest.",
        recommendation="Kraftigt begränsa koffein. Max 100 mg/dag. Undvik efter kl 12."
    ),
    GeneInteraction(
        genes=["rs1800562", "rs1799945"],  # HFE C282Y + H63D
        name="HFE Compound Heterozygot",
        condition="rs1800562=AG AND rs1799945=CG",
        effect="C282Y/H63D compound heterozygot kan ge mild hemokromatos.",
        recommendation="Monitorera ferritin årligen. Undvik järntillskott."
    ),
    GeneInteraction(
        genes=["rs7501331", "rs12934922"],  # BCMO1 varianter
        name="BCMO1 Dubbelrisk",
        condition="Riskalleler i båda",
        effect="Kombinerad BCMO1-påverkan ger mycket kraftigt reducerad betakarotenomvandling.",
        recommendation="Preformerad A-vitamin (retinol) nödvändigt. Betakaroten ineffektivt."
    ),
    GeneInteraction(
        genes=["rs2228570", "rs10741657"],  # VDR FokI + CYP2R1
        name="D-vitamin Dubbelrisk",
        condition="Riskalleler i båda",
        effect="Reducerad VDR-funktion + reducerad aktivering = kraftigt ökat D-vitaminbehov.",
        recommendation="Högdos D3 (4000-5000 IE/dag vinter). Kontrollera 25(OH)D nivåer."
    ),
]


class CompleteAnalyzer:
    """Komplett DNA-analysator med geninteraktioner"""

    def __init__(self, dna_file_path: str):
        self.dna_file_path = dna_file_path
        self.genotypes: Dict[str, str] = {}
        self.gene_db = get_gene_dict()
        self.results: List[AnalysisResult] = []
        self.interactions_found: List[Tuple[GeneInteraction, str]] = []

    def load_23andme_data(self) -> int:
        """Laddar 23andMe rådata"""
        print(f"Laddar DNA-data fran: {self.dna_file_path}")
        count = 0

        with open(self.dna_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue

                parts = line.strip().split('\t')
                if len(parts) >= 4:
                    rsid = parts[0]
                    genotype = parts[3]
                    if genotype != '--' and genotype != '':
                        self.genotypes[rsid] = genotype
                        count += 1

        print(f"Laddade {count:,} genetiska varianter")
        return count

    def normalize_genotype(self, genotype: str) -> str:
        """Normaliserar genotyp till sorterad ordning"""
        if len(genotype) == 2:
            return ''.join(sorted(genotype.upper()))
        return genotype.upper()

    def analyze_variant(self, variant: GeneVariant) -> Optional[AnalysisResult]:
        """Analyserar en specifik variant"""
        if variant.rsid not in self.genotypes:
            return None

        raw_genotype = self.genotypes[variant.rsid]
        normalized = self.normalize_genotype(raw_genotype)

        # Sök efter matchande effekt
        if normalized in variant.genotype_effects:
            risk_level, interpretation = variant.genotype_effects[normalized]
        else:
            # Prova omvänd ordning för heterozygota
            reversed_gt = raw_genotype[::-1] if len(raw_genotype) == 2 else raw_genotype
            normalized_rev = self.normalize_genotype(reversed_gt)
            if normalized_rev in variant.genotype_effects:
                risk_level, interpretation = variant.genotype_effects[normalized_rev]
            else:
                risk_level = RiskLevel.NORMAL
                interpretation = f"Genotyp {raw_genotype} - effekt ej definierad i databas"

        return AnalysisResult(
            variant=variant,
            genotype=raw_genotype,
            risk_level=risk_level,
            interpretation=interpretation
        )

    def run_analysis(self) -> List[AnalysisResult]:
        """Kör komplett analys"""
        print(f"\nAnalyserar {len(GENE_DATABASE)} wellness-gener...")

        for variant in GENE_DATABASE:
            result = self.analyze_variant(variant)
            if result:
                self.results.append(result)

        print(f"Hittade data for {len(self.results)} av {len(GENE_DATABASE)} varianter")

        # Analysera interaktioner
        self.analyze_interactions()

        return self.results

    def analyze_interactions(self):
        """Analyserar geninteraktioner"""
        results_by_rsid = {r.variant.rsid: r for r in self.results}

        for interaction in GENE_INTERACTIONS:
            # Kolla om vi har data för alla gener i interaktionen
            relevant_results = []
            for rsid in interaction.genes:
                if rsid in results_by_rsid:
                    relevant_results.append(results_by_rsid[rsid])

            if len(relevant_results) == len(interaction.genes):
                # Evaluera specifika interaktionsvillkor
                description = self._evaluate_interaction(interaction, relevant_results)
                if description:
                    self.interactions_found.append((interaction, description))

    def _evaluate_interaction(self, interaction: GeneInteraction, results: List[AnalysisResult]) -> Optional[str]:
        """Evaluerar om en interaktion är aktiv"""
        rsid_to_result = {r.variant.rsid: r for r in results}

        # MTHFR compound heterozygot
        if interaction.name == "MTHFR Compound Heterozygot":
            r1 = rsid_to_result.get("rs1801133")
            r2 = rsid_to_result.get("rs1801131")
            if r1 and r2:
                if r1.genotype in ["AG", "GA"] and r2.genotype in ["GT", "TG"]:
                    return f"MTHFR C677T: {r1.genotype}, A1298C: {r2.genotype} - Compound heterozygot påverkan"

        # APOE haplotyp
        if interaction.name == "APOE Haplotyp":
            r1 = rsid_to_result.get("rs429358")  # ε4
            r2 = rsid_to_result.get("rs7412")    # ε2
            if r1 and r2:
                haplotype = self._determine_apoe_haplotype(r1.genotype, r2.genotype)
                return f"APOE haplotyp: {haplotype}"

        # FADS1/2 dubbelrisk
        if interaction.name == "FADS1/2 Dubbelrisk":
            r1 = rsid_to_result.get("rs174546")
            r2 = rsid_to_result.get("rs1535")
            if r1 and r2:
                if r1.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED] and \
                   r2.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
                    return f"FADS1: {r1.genotype}, FADS2: {r2.genotype} - Dubbelrisk for omega-3 metabolism"

        # COMT + Koffein
        if interaction.name == "COMT + Koffein":
            r1 = rsid_to_result.get("rs4680")
            r2 = rsid_to_result.get("rs762551")
            if r1 and r2:
                if r1.genotype == "AA" and r2.genotype in ["CC", "AC"]:
                    return f"COMT slow ({r1.genotype}) + CYP1A2 slow ({r2.genotype}) - Var forsiktig med koffein"

        # HFE compound
        if interaction.name == "HFE Compound Heterozygot":
            r1 = rsid_to_result.get("rs1800562")
            r2 = rsid_to_result.get("rs1799945")
            if r1 and r2:
                if r1.genotype in ["AG", "GA"] and r2.genotype in ["CG", "GC"]:
                    return f"HFE C282Y/H63D compound heterozygot - Monitorera jarnnivaaer"

        # BCMO1 dubbelrisk
        if interaction.name == "BCMO1 Dubbelrisk":
            r1 = rsid_to_result.get("rs7501331")
            r2 = rsid_to_result.get("rs12934922")
            if r1 and r2:
                if r1.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED] and \
                   r2.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
                    return f"BCMO1 dubbelrisk - Mycket reducerad betakaroteomvandling"

        # D-vitamin dubbelrisk
        if interaction.name == "D-vitamin Dubbelrisk":
            r1 = rsid_to_result.get("rs2228570")
            r2 = rsid_to_result.get("rs10741657")
            if r1 and r2:
                if r1.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED] and \
                   r2.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
                    return f"VDR + CYP2R1 dubbelrisk - Okat D-vitaminbehov"

        return None

    def _determine_apoe_haplotype(self, rs429358: str, rs7412: str) -> str:
        """Bestämmer APOE-haplotyp från rs429358 och rs7412"""
        # rs429358: T=ε2/ε3, C=ε4
        # rs7412: C=ε3/ε4, T=ε2

        e4_count = rs429358.upper().count('C')
        e2_count = rs7412.upper().count('T')

        if e4_count == 2:
            return "e4/e4 (hog risk)"
        elif e4_count == 1:
            if e2_count >= 1:
                return "e2/e4"
            else:
                return "e3/e4 (moderat risk)"
        elif e2_count == 2:
            return "e2/e2 (skyddande)"
        elif e2_count == 1:
            return "e2/e3 (skyddande)"
        else:
            return "e3/e3 (normal)"

    def generate_supplement_recommendations(self) -> List[SupplementRecommendation]:
        """Genererar personliga supplement-rekommendationer"""
        recommendations = []
        results_by_rsid = {r.variant.rsid: r for r in self.results}

        # =====================================================================
        # D-VITAMIN
        # =====================================================================
        vdr_risk = 0
        vdr_genes = []
        for rsid in ["rs2228570", "rs1544410", "rs731236", "rs10741657", "rs12785878", "rs2282679"]:
            if rsid in results_by_rsid:
                r = results_by_rsid[rsid]
                if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED, RiskLevel.HIGH]:
                    vdr_risk += 1
                    vdr_genes.append(r.variant.gene)

        if vdr_risk >= 3:
            recommendations.append(SupplementRecommendation(
                name="D-vitamin D3 (kolecalciferol)",
                dosage="4000-5000 IE/dag (okt-apr), 2000 IE/dag (maj-sep)",
                timing="Med fetrik maltid for battre absorption",
                reason="Flera VDR/CYP2R1-varianter indikerar kraftigt okat D-vitaminbehov",
                priority=5,
                evidence=EvidenceLevel.STRONG,
                genes_involved=list(set(vdr_genes)),
                contraindications=["Hyperkalcemi", "Sarkoidos", "Njursten (forsiktighet)"]
            ))
        elif vdr_risk >= 1:
            recommendations.append(SupplementRecommendation(
                name="D-vitamin D3",
                dosage="2000-3000 IE/dag",
                timing="Med fetrik maltid",
                reason="VDR-varianter kan paverka D-vitaminrespons",
                priority=4,
                evidence=EvidenceLevel.STRONG,
                genes_involved=list(set(vdr_genes)) if vdr_genes else ["VDR"],
            ))
        else:
            recommendations.append(SupplementRecommendation(
                name="D-vitamin D3",
                dosage="1000-2000 IE/dag (vinter)",
                timing="Med maltid",
                reason="Standard underhallsdos for skandinaviskt klimat",
                priority=3,
                evidence=EvidenceLevel.STRONG,
                genes_involved=[],
            ))

        # =====================================================================
        # METYLERING & B-VITAMINER
        # =====================================================================
        mthfr_677 = results_by_rsid.get("rs1801133")
        mthfr_1298 = results_by_rsid.get("rs1801131")

        if mthfr_677 and mthfr_677.genotype == "AA":  # TT homozygot
            recommendations.append(SupplementRecommendation(
                name="Metylfolat (5-MTHF, L-metylfolat)",
                dosage="400-800 mcg/dag",
                timing="Med maltid, kan delas pa morgon och kvall",
                reason="MTHFR C677T TT-genotyp ger ~30% enzymaktivitet - kraver aktiverad folat",
                priority=5,
                evidence=EvidenceLevel.STRONG,
                genes_involved=["MTHFR"],
                contraindications=["Undvik hog dos folsyra (kan maskera B12-brist)"]
            ))
            recommendations.append(SupplementRecommendation(
                name="Metyl-B12 (metylkobalamin)",
                dosage="1000-2000 mcg/dag",
                timing="Sublingualt pa morgonen",
                reason="Synergistiskt med metylfolat for optimal metylering",
                priority=5,
                evidence=EvidenceLevel.STRONG,
                genes_involved=["MTHFR", "MTR", "MTRR"],
            ))
        elif mthfr_677 and mthfr_677.genotype in ["AG", "GA"]:  # CT heterozygot
            recommendations.append(SupplementRecommendation(
                name="Aktivt B-komplex med metylfolat",
                dosage="1 kapsel/dag innehallande 400 mcg metylfolat",
                timing="Med frukost",
                reason="MTHFR C677T heterozygot - metylfolat fordelaktigt",
                priority=4,
                evidence=EvidenceLevel.STRONG,
                genes_involved=["MTHFR"],
            ))

        # Compound heterozygot
        if mthfr_677 and mthfr_1298:
            if mthfr_677.genotype in ["AG", "GA"] and mthfr_1298.genotype in ["GT", "TG"]:
                # Redan rekommenderat B-komplex, oka prioritet
                for rec in recommendations:
                    if "metylfolat" in rec.name.lower():
                        rec.priority = 5
                        rec.reason += " Compound heterozygot forstarker paverkan."

        # B12 (FUT2)
        fut2 = results_by_rsid.get("rs602662")
        if fut2 and fut2.genotype == "AA":  # Non-secretor
            recommendations.append(SupplementRecommendation(
                name="B12 (metyl- eller adenosylkobalamin)",
                dosage="1000 mcg/dag sublingualt",
                timing="Pa morgonen, under tungan",
                reason="FUT2 non-secretor status kan ge reducerad B12-absorption via tarmen",
                priority=4,
                evidence=EvidenceLevel.STRONG,
                genes_involved=["FUT2"],
            ))

        # =====================================================================
        # OMEGA-3
        # =====================================================================
        fads1 = results_by_rsid.get("rs174546")
        fads2 = results_by_rsid.get("rs1535")

        fads_risk = 0
        if fads1 and fads1.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            fads_risk += 1
        if fads2 and fads2.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            fads_risk += 1

        if fads_risk >= 2:
            recommendations.append(SupplementRecommendation(
                name="Omega-3 (EPA+DHA fran fisk eller alg)",
                dosage="2000-3000 mg EPA+DHA/dag (minst 1000 mg EPA)",
                timing="Med maltid, kan delas pa 2-3 doser",
                reason="FADS1+FADS2 varianter ger kraftigt reducerad ALA→EPA/DHA-omvandling",
                priority=5,
                evidence=EvidenceLevel.STRONG,
                genes_involved=["FADS1", "FADS2"],
                contraindications=["Forsiktighet vid blodfortunnande medicin"]
            ))
        elif fads_risk >= 1:
            recommendations.append(SupplementRecommendation(
                name="Omega-3 (EPA+DHA)",
                dosage="1500-2000 mg EPA+DHA/dag",
                timing="Med maltid",
                reason="FADS-variant reducerar omega-3-omvandling fran vaxtbaserade kallor",
                priority=5,
                evidence=EvidenceLevel.STRONG,
                genes_involved=["FADS1"] if fads1 else ["FADS2"],
            ))
        else:
            recommendations.append(SupplementRecommendation(
                name="Omega-3 (EPA+DHA)",
                dosage="1000-1500 mg EPA+DHA/dag",
                timing="Med maltid",
                reason="Allman hjart- och hjarnhalsa",
                priority=3,
                evidence=EvidenceLevel.STRONG,
                genes_involved=[],
            ))

        # =====================================================================
        # VITAMIN A (BCMO1)
        # =====================================================================
        bcmo1_1 = results_by_rsid.get("rs7501331")
        bcmo1_2 = results_by_rsid.get("rs12934922")

        bcmo1_risk = 0
        if bcmo1_1 and bcmo1_1.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            bcmo1_risk += 1
        if bcmo1_2 and bcmo1_2.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            bcmo1_risk += 1

        if bcmo1_risk >= 1:
            recommendations.append(SupplementRecommendation(
                name="Retinol (preformerad A-vitamin)",
                dosage="2500-5000 IE/dag (max 10000 IE)",
                timing="Med fetrik maltid",
                reason="BCMO1-varianter reducerar betakaroten→retinol-omvandling med 32-69%",
                priority=4,
                evidence=EvidenceLevel.MODERATE,
                genes_involved=["BCMO1"],
                contraindications=["Undvik hoga doser vid graviditet", "Leversjukdom"]
            ))

        # =====================================================================
        # MAGNESIUM (COMT)
        # =====================================================================
        comt = results_by_rsid.get("rs4680")

        if comt and comt.genotype == "AA":  # Met/Met
            recommendations.append(SupplementRecommendation(
                name="Magnesium (glycinat eller treonat)",
                dosage="300-400 mg elementart Mg/dag",
                timing="Pa kvallen 1-2 timmar fore somn",
                reason="COMT Met/Met ('Worrier') behover extra stod for stresshantering. Mg stodjer COMT-funktion.",
                priority=5,
                evidence=EvidenceLevel.MODERATE,
                genes_involved=["COMT"],
            ))
            recommendations.append(SupplementRecommendation(
                name="L-teanin",
                dosage="200-400 mg/dag vid behov",
                timing="Vid stress eller pa kvallen",
                reason="Stodjer lugn fokus for stresskansliga COMT-varianter utan drovaktighet",
                priority=3,
                evidence=EvidenceLevel.MODERATE,
                genes_involved=["COMT"],
            ))
        else:
            recommendations.append(SupplementRecommendation(
                name="Magnesium (glycinat)",
                dosage="200-300 mg/dag",
                timing="Pa kvallen",
                reason="Grundlaggande for 300+ enzymer, de flesta har suboptimalt intag",
                priority=3,
                evidence=EvidenceLevel.MODERATE,
                genes_involved=[],
            ))

        # =====================================================================
        # SELEN (GPX1)
        # =====================================================================
        gpx1 = results_by_rsid.get("rs1050450")

        if gpx1 and gpx1.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            recommendations.append(SupplementRecommendation(
                name="Selen (selenometionin)",
                dosage="100-200 mcg/dag",
                timing="Med maltid",
                reason="GPX1 Leu-variant har reducerad antioxidantfunktion och ar mer beroende av selen",
                priority=4,
                evidence=EvidenceLevel.MODERATE,
                genes_involved=["GPX1"],
                contraindications=["Max 400 mcg/dag totalt (inklusive kost)"]
            ))

        # =====================================================================
        # JÄRN (HFE)
        # =====================================================================
        hfe_c282y = results_by_rsid.get("rs1800562")

        if hfe_c282y and hfe_c282y.genotype == "AA":  # Homozygot
            # ANTI-rekommendation
            recommendations.append(SupplementRecommendation(
                name="UNDVIK JARNTILLSKOTT",
                dosage="Inget jarntillskott",
                timing="N/A",
                reason="HFE C282Y homozygot = hemokromatos. Jarntillskott kontraindicerat.",
                priority=5,
                evidence=EvidenceLevel.STRONG,
                genes_involved=["HFE"],
                contraindications=["Jarntillskott", "C-vitamin i hoga doser (okar jarnabsorption)"]
            ))
        elif hfe_c282y and hfe_c282y.genotype in ["AG", "GA"]:
            recommendations.append(SupplementRecommendation(
                name="Jarn - Var forsiktig",
                dosage="Endast vid dokumenterad brist",
                timing="N/A",
                reason="HFE C282Y barare - undvik jarntillskott utan blodprov",
                priority=3,
                evidence=EvidenceLevel.STRONG,
                genes_involved=["HFE"],
            ))

        # =====================================================================
        # KOLIN
        # =====================================================================
        # Alla med MTHFR-varianter har okat kolinbehov
        if mthfr_677 and mthfr_677.risk_level in [RiskLevel.MODERATE, RiskLevel.HIGH]:
            recommendations.append(SupplementRecommendation(
                name="Kolin (alfa-GPC eller CDP-kolin)",
                dosage="300-600 mg/dag",
                timing="Med maltid, helst pa morgonen",
                reason="MTHFR-varianter okar beroendet av kolin for metylering",
                priority=3,
                evidence=EvidenceLevel.MODERATE,
                genes_involved=["MTHFR"],
            ))

        # Sortera efter prioritet
        recommendations.sort(key=lambda x: x.priority, reverse=True)

        return recommendations

    def generate_lifestyle_recommendations(self) -> List[LifestyleRecommendation]:
        """Genererar livsstilsrekommendationer"""
        recommendations = []
        results_by_rsid = {r.variant.rsid: r for r in self.results}

        # COMT
        comt = results_by_rsid.get("rs4680")
        if comt:
            if comt.genotype == "AA":  # Met/Met
                recommendations.append(LifestyleRecommendation(
                    category="Stresshantering",
                    recommendation="Daglig stresshantering kritisk: meditation (10-20 min), yoga, promenader i naturen, djupandning",
                    reason="COMT Met/Met ger langsam katekolaminnedbrytning - du ar mer stresskanslig men har battre fokus under lugna forhallanden",
                    genes_involved=["COMT"],
                    priority=5
                ))
                recommendations.append(LifestyleRecommendation(
                    category="Koffein",
                    recommendation="Begransa koffein till 100-200 mg/dag (1-2 koppar kaffe), endast pa morgonen fore kl 11",
                    reason="COMT Met/Met + langre katekolamineffekt = koffein kan orsaka angst och somnproblem",
                    genes_involved=["COMT"],
                    priority=5
                ))
            elif comt.genotype == "GG":  # Val/Val
                recommendations.append(LifestyleRecommendation(
                    category="Stimulans",
                    recommendation="Du kan behova mer stimulans for optimal funktion - utmanande uppgifter, tidspress kan vara positivt",
                    reason="COMT Val/Val ('Warrior') hanterar stress val men kan bli understimulerad",
                    genes_involved=["COMT"],
                    priority=3
                ))

        # CYP1A2 (koffein)
        cyp1a2 = results_by_rsid.get("rs762551")
        if cyp1a2:
            if cyp1a2.genotype == "CC":
                recommendations.append(LifestyleRecommendation(
                    category="Koffein",
                    recommendation="Langsam koffeinmetaboliserare: Max 1-2 koppar kaffe/dag, sista kopp fore kl 14",
                    reason="CYP1A2 CC = halveringstid 8+ timmar. Koffein paverkar somn och kan oka hjartrisk vid hog konsumtion.",
                    genes_involved=["CYP1A2"],
                    priority=4
                ))
            elif cyp1a2.genotype == "AA":
                recommendations.append(LifestyleRecommendation(
                    category="Koffein",
                    recommendation="Snabb koffeinmetaboliserare: Upp till 4 koppar kaffe/dag tolereras val",
                    reason="CYP1A2 AA = halveringstid 2-4 timmar. Koffein bryts ned snabbt.",
                    genes_involved=["CYP1A2"],
                    priority=2
                ))

        # ALDH2 (alkohol)
        aldh2 = results_by_rsid.get("rs671")
        if aldh2 and aldh2.risk_level in [RiskLevel.ELEVATED, RiskLevel.HIGH]:
            recommendations.append(LifestyleRecommendation(
                category="Alkohol",
                recommendation="KRAFTIGT begransa eller undvik alkohol helt",
                reason="ALDH2-variant ger defekt acetaldehydnedbrytning - okad toxicitet, flush, huvudvark, langvarig bakfylla",
                genes_involved=["ALDH2"],
                priority=5
            ))

        # CLOCK (somn)
        clock = results_by_rsid.get("rs1801260")
        if clock:
            if "C" in clock.genotype.upper():
                recommendations.append(LifestyleRecommendation(
                    category="Somn & dygnsrytm",
                    recommendation="Du ar troligen en kvallsmanniska. Om mojligt, anpassa schema. Anvand ljusterapi pa morgonen.",
                    reason="CLOCK-variant associerad med senare kronotyp",
                    genes_involved=["CLOCK"],
                    priority=3
                ))

        # BDNF
        bdnf = results_by_rsid.get("rs6265")
        if bdnf and bdnf.risk_level in [RiskLevel.MODERATE]:
            recommendations.append(LifestyleRecommendation(
                category="Traning",
                recommendation="Regelbunden aerob traning (30 min, 4-5 ggr/vecka) ar extra viktigt for dig",
                reason="BDNF Met-variant ger reducerad BDNF-sekretion. Traning okar BDNF-nivaer signifikant.",
                genes_involved=["BDNF"],
                priority=4
            ))

        # APOE
        apoe4 = results_by_rsid.get("rs429358")
        if apoe4 and apoe4.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            recommendations.append(LifestyleRecommendation(
                category="Hjarhalsa & kognition",
                recommendation="Prioritera hjarnhalsa: regelbunden traning, social aktivitet, mental stimulans, god somn",
                reason="APOE e4-barare har okad risk for Alzheimers - men livsstilsfaktorer kan kraftigt paverka risken",
                genes_involved=["APOE"],
                priority=5
            ))
            recommendations.append(LifestyleRecommendation(
                category="Alkohol",
                recommendation="Begransa alkohol - APOE e4-barare ar kansligare for alkoholens negativa hjarneffekter",
                reason="APOE e4 + alkohol = synergistisk negativ effekt pa kognition",
                genes_involved=["APOE"],
                priority=4
            ))

        # TCF7L2 (diabetes)
        tcf7l2 = results_by_rsid.get("rs7903146")
        if tcf7l2 and tcf7l2.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            recommendations.append(LifestyleRecommendation(
                category="Blodsockerkontroll",
                recommendation="Extra fokus pa blodsockerstabilitet: undvik snabba kolhydrater, prioritera fiber, protein forst vid maltid",
                reason="TCF7L2-variant ger okad typ 2-diabetesrisk genom reducerad insulinsekretion",
                genes_involved=["TCF7L2"],
                priority=4
            ))

        # Sortera efter prioritet
        recommendations.sort(key=lambda x: x.priority, reverse=True)

        return recommendations

    def generate_diet_recommendations(self) -> List[LifestyleRecommendation]:
        """Genererar kostråd"""
        recommendations = []
        results_by_rsid = {r.variant.rsid: r for r in self.results}

        # Laktos
        lct = results_by_rsid.get("rs4988235")
        if lct:
            if lct.genotype == "AA" or lct.risk_level == RiskLevel.HIGH:
                recommendations.append(LifestyleRecommendation(
                    category="Mejeri",
                    recommendation="Du ar laktosintolerant. Valj laktosfria produkter eller vaxtbaserade alternativ.",
                    reason="LCT-13910 C/C = laktasproduktion upphor i vuxen alder",
                    genes_involved=["MCM6/LCT"],
                    priority=5
                ))
            else:
                recommendations.append(LifestyleRecommendation(
                    category="Mejeri",
                    recommendation="Du ar laktospersistent och kan konsumera mjolkprodukter utan problem",
                    reason="LCT-13910 T-barare bevarar laktasproduktion",
                    genes_involved=["MCM6/LCT"],
                    priority=1
                ))

        # FTO (vikt)
        fto = results_by_rsid.get("rs9939609")
        if fto and fto.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            recommendations.append(LifestyleRecommendation(
                category="Mattnad & vikt",
                recommendation="Prioritera protein (25-30g/maltid) och fiber for battre mattnad. Var medveten om portionsstorlekar.",
                reason="FTO-variant associerad med okad hunger och reducerad mattnad",
                genes_involved=["FTO"],
                priority=4
            ))
            recommendations.append(LifestyleRecommendation(
                category="Mattider",
                recommendation="Overavag tidsbegransat atande (16:8 fasta) - kan vara extra fordelaktigt for din genotyp",
                reason="FTO-effekten motverkas delvis av periodisk fasta i studier",
                genes_involved=["FTO"],
                priority=3
            ))

        # APOE4 och fett
        apoe4 = results_by_rsid.get("rs429358")
        if apoe4 and apoe4.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            recommendations.append(LifestyleRecommendation(
                category="Fetter",
                recommendation="Begransa mattat fett (<20g/dag). Prioritera omattade fetter: olivolja, avokado, notter, fet fisk.",
                reason="APOE e4-barare har hogre LDL-respons pa mattat fett",
                genes_involved=["APOE"],
                priority=5
            ))
            recommendations.append(LifestyleRecommendation(
                category="Fisk",
                recommendation="At fet fisk minst 2-3 ganger/vecka (lax, makrill, sill, sardiner)",
                reason="Omega-3 fran fisk ar extra viktigt for APOE e4-barare for hjarhalsa",
                genes_involved=["APOE"],
                priority=4
            ))

        # BCMO1 (A-vitamin)
        bcmo1 = results_by_rsid.get("rs7501331")
        if bcmo1 and bcmo1.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            recommendations.append(LifestyleRecommendation(
                category="A-vitamin",
                recommendation="Inkludera animaliska A-vitaminkallor: lever (1-2 ggr/manad), agg, mejeriprodukter",
                reason="BCMO1-variant reducerar omvandling fran betakaroten - du behover preformerad retinol",
                genes_involved=["BCMO1"],
                priority=4
            ))

        # Inflammation
        il6 = results_by_rsid.get("rs1800795")
        tnf = results_by_rsid.get("rs1800629")

        inflammation_risk = 0
        if il6 and il6.risk_level in [RiskLevel.MODERATE]:
            inflammation_risk += 1
        if tnf and tnf.risk_level in [RiskLevel.MODERATE]:
            inflammation_risk += 1

        if inflammation_risk >= 1:
            recommendations.append(LifestyleRecommendation(
                category="Antiinflammatorisk kost",
                recommendation="Fokusera pa antiinflammatorisk kost: mycket gronsaker, bar, fet fisk, olivolja, gurkmeja/kurkumin",
                reason="Genetiska varianter ger hogre basal inflammation",
                genes_involved=["IL6", "TNF"],
                priority=4
            ))
            recommendations.append(LifestyleRecommendation(
                category="Undvik",
                recommendation="Minimera processad mat, socker, raffinerade kolhydrater, industriella vegetabiliska oljor",
                reason="Dessa okar inflammation, sarskilt vid genetisk predisposition",
                genes_involved=["IL6", "TNF"],
                priority=4
            ))

        # HLA-DQ2 (celiaki)
        hla = results_by_rsid.get("rs2187668")
        if hla and hla.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED]:
            recommendations.append(LifestyleRecommendation(
                category="Gluten",
                recommendation="Du har genetisk predisposition for celiaki. Vid GI-symptom - utred celiaki.",
                reason="HLA-DQ2-barare. OBS: Majoriteten utvecklar INTE celiaki.",
                genes_involved=["HLA-DQ2.5"],
                priority=3
            ))

        recommendations.sort(key=lambda x: x.priority, reverse=True)
        return recommendations

    def generate_exercise_recommendations(self) -> List[LifestyleRecommendation]:
        """Genererar träningsråd"""
        recommendations = []
        results_by_rsid = {r.variant.rsid: r for r in self.results}

        # ACTN3
        actn3 = results_by_rsid.get("rs1815739")
        if actn3:
            if actn3.genotype == "CC":  # R/R
                recommendations.append(LifestyleRecommendation(
                    category="Traningstyp",
                    recommendation="Du har genetisk fordel for explosiv styrka/sprint. Inkludera styrketraning och HIIT.",
                    reason="ACTN3 R/R = fungerande alfa-actinin-3 i snabba muskelfibrer",
                    genes_involved=["ACTN3"],
                    priority=4
                ))
            elif actn3.genotype == "TT":  # X/X
                recommendations.append(LifestyleRecommendation(
                    category="Traningstyp",
                    recommendation="Du har genetisk fordel for uthallighet. Fokusera pa langre pass, konditionstraning, langdistans.",
                    reason="ACTN3 X/X = ingen alfa-actinin-3, fordelaktigt for langsamma muskelfibrer",
                    genes_involved=["ACTN3"],
                    priority=4
                ))
            else:  # R/X
                recommendations.append(LifestyleRecommendation(
                    category="Traningstyp",
                    recommendation="Du har balanserad muskelfibersammansattning. Varierad traning passar dig bast.",
                    reason="ACTN3 R/X = allroundkapacitet",
                    genes_involved=["ACTN3"],
                    priority=3
                ))

        # PPARGC1A
        ppargc1a = results_by_rsid.get("rs8192678")
        if ppargc1a and ppargc1a.genotype == "AA":
            recommendations.append(LifestyleRecommendation(
                category="Uthallighet",
                recommendation="Du kan behova mer konsekvent traning for samma uthallighetsfobarttring. Var talmodig.",
                reason="PPARGC1A Ser/Ser-variant ger nagot lagre mitokondriell respons pa traning",
                genes_involved=["PPARGC1A"],
                priority=3
            ))

        # BDNF
        bdnf = results_by_rsid.get("rs6265")
        if bdnf and bdnf.risk_level in [RiskLevel.MODERATE]:
            recommendations.append(LifestyleRecommendation(
                category="Hjarhalsa genom traning",
                recommendation="Aerob traning (lopning, cykling, simning) ar sarskilt viktigt for dig for hjarnhalsa",
                reason="BDNF Met-variant = traning ar det mest effektiva sattet att oka BDNF-nivaer",
                genes_involved=["BDNF"],
                priority=5
            ))

        recommendations.sort(key=lambda x: x.priority, reverse=True)
        return recommendations


def generate_complete_report(analyzer: CompleteAnalyzer, name: str, output_path: str):
    """Genererar komplett instruktionsmanual-rapport"""

    results_by_category = defaultdict(list)
    for result in analyzer.results:
        results_by_category[result.variant.category].append(result)

    supplements = analyzer.generate_supplement_recommendations()
    lifestyle = analyzer.generate_lifestyle_recommendations()
    diet = analyzer.generate_diet_recommendations()
    exercise = analyzer.generate_exercise_recommendations()

    # Räkna risknivåer
    risk_counts = defaultdict(int)
    for r in analyzer.results:
        risk_counts[r.risk_level] += 1

    lines = []

    # ==========================================================================
    # HEADER
    # ==========================================================================
    lines.append("# GENETIC WELLNESS LABS")
    lines.append("# Personlig Genetisk Instruktionsmanual")
    lines.append("")
    lines.append(f"**Namn:** {name}")
    lines.append(f"**Genererad:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Analyserade gener:** {len(analyzer.results)} av {len(GENE_DATABASE)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ==========================================================================
    # EXECUTIVE SUMMARY
    # ==========================================================================
    lines.append("## SAMMANFATTNING")
    lines.append("")
    lines.append("### Genetisk oversikt")
    lines.append("")
    lines.append(f"| Status | Antal | Andel |")
    lines.append(f"|--------|-------|-------|")
    total = sum(risk_counts.values())
    for level in [RiskLevel.OPTIMAL, RiskLevel.NORMAL, RiskLevel.MODERATE, RiskLevel.ELEVATED, RiskLevel.HIGH]:
        count = risk_counts[level]
        pct = (count / total * 100) if total > 0 else 0
        emoji = {"optimal": "🟢", "normal": "🟢", "moderat": "🟡", "förhöjd": "🟠", "hög": "🔴"}[level.value]
        lines.append(f"| {emoji} {level.value.capitalize()} | {count} | {pct:.0f}% |")
    lines.append("")

    # Viktiga fynd
    important_findings = [r for r in analyzer.results
                        if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED, RiskLevel.HIGH]]

    if important_findings:
        lines.append("### Viktiga genetiska fynd")
        lines.append("")
        for r in sorted(important_findings, key=lambda x: x.risk_level.value, reverse=True)[:10]:
            emoji = {"moderat": "🟡", "förhöjd": "🟠", "hög": "🔴"}[r.risk_level.value]
            lines.append(f"- {emoji} **{r.variant.gene}** ({r.variant.name}): {r.interpretation}")
        lines.append("")

    # Gen-interaktioner
    if analyzer.interactions_found:
        lines.append("### Identifierade gen-interaktioner")
        lines.append("")
        for interaction, description in analyzer.interactions_found:
            lines.append(f"- **{interaction.name}**: {description}")
            lines.append(f"  - *Effekt:* {interaction.effect}")
            lines.append(f"  - *Rekommendation:* {interaction.recommendation}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ==========================================================================
    # SUPPLEMENT-REKOMMENDATIONER
    # ==========================================================================
    lines.append("## SUPPLEMENT-PROTOKOLL")
    lines.append("")
    lines.append("Rekommendationer baserade pa din genetik, sorterade efter prioritet.")
    lines.append("")

    # Topprioritet
    high_priority = [s for s in supplements if s.priority >= 4]
    if high_priority:
        lines.append("### Hog prioritet (rekommenderas starkt)")
        lines.append("")
        for s in high_priority:
            stars = "⭐" * s.priority
            lines.append(f"#### {s.name} {stars}")
            lines.append(f"- **Dos:** {s.dosage}")
            lines.append(f"- **Timing:** {s.timing}")
            lines.append(f"- **Anledning:** {s.reason}")
            lines.append(f"- **Evidens:** {s.evidence.value}")
            if s.genes_involved:
                lines.append(f"- **Gener:** {', '.join(s.genes_involved)}")
            if s.contraindications:
                lines.append(f"- **Kontraindikationer:** {', '.join(s.contraindications)}")
            lines.append("")

    # Medel prioritet
    med_priority = [s for s in supplements if s.priority == 3]
    if med_priority:
        lines.append("### Medel prioritet (overavag)")
        lines.append("")
        for s in med_priority:
            lines.append(f"#### {s.name}")
            lines.append(f"- **Dos:** {s.dosage}")
            lines.append(f"- **Timing:** {s.timing}")
            lines.append(f"- **Anledning:** {s.reason}")
            if s.genes_involved:
                lines.append(f"- **Gener:** {', '.join(s.genes_involved)}")
            lines.append("")

    lines.append("---")
    lines.append("")

    # ==========================================================================
    # LIVSSTILSREKOMMENDATIONER
    # ==========================================================================
    lines.append("## LIVSSTILSREKOMMENDATIONER")
    lines.append("")

    for rec in lifestyle:
        priority_indicator = "⚠️ " if rec.priority >= 4 else ""
        lines.append(f"### {priority_indicator}{rec.category}")
        lines.append(f"**{rec.recommendation}**")
        lines.append(f"- *Anledning:* {rec.reason}")
        lines.append(f"- *Gener:* {', '.join(rec.genes_involved)}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ==========================================================================
    # KOSTRAD
    # ==========================================================================
    lines.append("## KOSTRAD")
    lines.append("")

    for rec in diet:
        priority_indicator = "⚠️ " if rec.priority >= 4 else ""
        lines.append(f"### {priority_indicator}{rec.category}")
        lines.append(f"**{rec.recommendation}**")
        lines.append(f"- *Anledning:* {rec.reason}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ==========================================================================
    # TRÄNINGSRÅD
    # ==========================================================================
    lines.append("## TRANINGSRAD")
    lines.append("")

    for rec in exercise:
        lines.append(f"### {rec.category}")
        lines.append(f"**{rec.recommendation}**")
        lines.append(f"- *Anledning:* {rec.reason}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ==========================================================================
    # DETALJERAD GENETISK ANALYS
    # ==========================================================================
    lines.append("## DETALJERAD GENETISK ANALYS")
    lines.append("")

    # Ordna kategorier logiskt
    category_order = [
        # Näring först
        Category.VITAMIN_D, Category.VITAMIN_B, Category.VITAMIN_A,
        Category.OMEGA3, Category.IRON, Category.CHOLINE,
        # Metabolism
        Category.CAFFEINE, Category.ALCOHOL, Category.LACTOSE, Category.GLUTEN,
        Category.HISTAMINE, Category.INSULIN,
        # Mental/stress
        Category.STRESS, Category.MOOD, Category.SLEEP,
        # Kropp
        Category.WEIGHT, Category.SATIETY, Category.CARDIOVASCULAR,
        Category.INFLAMMATION, Category.DETOX, Category.ANTIOXIDANT,
        # Träning
        Category.EXERCISE_POWER, Category.EXERCISE_ENDURANCE,
        # Övrigt
        Category.THYROID, Category.LONGEVITY,
    ]

    for category in category_order:
        if category not in results_by_category:
            continue

        cat_results = results_by_category[category]
        if not cat_results:
            continue

        # Beräkna övergripande status
        risk_scores = {RiskLevel.OPTIMAL: 0, RiskLevel.NORMAL: 1, RiskLevel.MODERATE: 2,
                      RiskLevel.ELEVATED: 3, RiskLevel.HIGH: 4}
        avg_score = sum(risk_scores[r.risk_level] for r in cat_results) / len(cat_results)

        if avg_score < 0.5:
            overall_status = "🟢 Optimal"
        elif avg_score < 1.5:
            overall_status = "🟢 Normal"
        elif avg_score < 2.5:
            overall_status = "🟡 Moderat"
        elif avg_score < 3.5:
            overall_status = "🟠 Forhojd"
        else:
            overall_status = "🔴 Hog"

        lines.append(f"### {category.value}")
        lines.append(f"**Overgripande status:** {overall_status}")
        lines.append("")

        lines.append("| Gen | Variant | Genotyp | Evidens | Status | Tolkning |")
        lines.append("|-----|---------|---------|---------|--------|----------|")

        for r in cat_results:
            emoji = {"optimal": "🟢", "normal": "🟢", "moderat": "🟡",
                    "förhöjd": "🟠", "hög": "🔴"}[r.risk_level.value]
            evidence = r.variant.evidence_level.value[:3].upper()
            lines.append(f"| {r.variant.gene} | {r.variant.name} | **{r.genotype}** | {evidence} | {emoji} | {r.interpretation[:60]}{'...' if len(r.interpretation) > 60 else ''} |")

        lines.append("")

        # Lägg till rekommendationer för kategorin
        findings = [r for r in cat_results if r.risk_level in [RiskLevel.MODERATE, RiskLevel.ELEVATED, RiskLevel.HIGH]]
        if findings:
            lines.append("**Rekommendationer for denna kategori:**")
            for r in findings:
                lines.append(f"- {r.variant.recommendation}")
            lines.append("")

        lines.append("")

    lines.append("---")
    lines.append("")

    # ==========================================================================
    # VETENSKAPLIGA REFERENSER
    # ==========================================================================
    lines.append("## VETENSKAPLIGA KALLOR")
    lines.append("")
    lines.append("Alla rekommendationer baseras pa peer-reviewed forskning. Nyckelreferenser:")
    lines.append("")

    # Samla unika referenser
    seen_pmids = set()
    for r in analyzer.results:
        for ref in r.variant.references:
            if ref.pmid not in seen_pmids:
                seen_pmids.add(ref.pmid)
                lines.append(f"- {ref.title} ({ref.journal}, {ref.year}) - [DOI](https://doi.org/{ref.doi})")

    lines.append("")
    lines.append("---")
    lines.append("")

    # ==========================================================================
    # DISCLAIMER
    # ==========================================================================
    lines.append("## VIKTIG INFORMATION")
    lines.append("")
    lines.append("### Begransningar")
    lines.append("")
    lines.append("1. **Genetik ar endast en del av bilden** - Livsstil, miljo, epigenetik och andra faktorer paverkar ocksa din halsa")
    lines.append("2. **Detta ar inte medicinsk diagnostik** - Konsultera alltid lakare for medicinska beslut")
    lines.append("3. **Individuell variation** - Effekten av genetiska varianter kan variera mellan individer")
    lines.append("4. **Forskningen utvecklas** - Nya studier kan andra var forstaelse")
    lines.append("")
    lines.append("### Evidensnivaer")
    lines.append("")
    lines.append("- **STARK**: Meta-analyser, stora GWAS-studier, FDA-godkand farmakogenomik")
    lines.append("- **MEDEL**: Randomiserade kontrollerade studier, prospektiva kohorter, replikerade fynd")
    lines.append("- **PRELIMINAR**: Observationsstudier, sma studier, behover ytterligare validering")
    lines.append("")
    lines.append("### Rekommendation")
    lines.append("")
    lines.append("Diskutera alltid supplementering med legitimerad dietist eller lakare, ")
    lines.append("sarskilt om du tar mediciner eller har kroniska sjukdomar.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Rapport genererad av Genetic Wellness Labs AI Pipeline v2.0*")
    lines.append(f"*{datetime.now().strftime('%Y-%m-%d')}*")

    # Skriv till fil
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\nRapport sparad till: {output_path}")


def main():
    """Huvudfunktion"""
    # Fix Windows encoding
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 70)
    print("GENETIC WELLNESS LABS - KOMPLETT DNA-ANALYS")
    print("Skapar din personliga genetiska instruktionsmanual")
    print("=" * 70)
    print()

    # Hitta DNA-fil
    dna_file = None
    genome_dir = os.path.join(os.path.dirname(__file__), "GENOME")

    if os.path.exists(genome_dir):
        for f in os.listdir(genome_dir):
            if f.endswith('.txt') and 'genome' in f.lower():
                dna_file = os.path.join(genome_dir, f)
                break

    if not dna_file:
        print("Kunde inte hitta DNA-fil i GENOME-mappen!")
        sys.exit(1)

    # Extrahera namn
    filename = os.path.basename(dna_file)
    name_parts = filename.replace('genome_', '').replace('_Full_', ' ').split('_v')[0]
    name = name_parts.replace('_', ' ').strip()

    print(f"Analyserar DNA for: {name}")
    print()

    # Kör analys
    analyzer = CompleteAnalyzer(dna_file)
    analyzer.load_23andme_data()
    analyzer.run_analysis()

    # Generera rapport
    output_path = os.path.join(os.path.dirname(__file__), f"GWL_Instruktionsmanual_{name.replace(' ', '_')}.md")
    generate_complete_report(analyzer, name, output_path)

    # Visa sammanfattning
    print()
    print("=" * 70)
    print("ANALYS KLAR")
    print("=" * 70)
    print()

    # Topp-rekommendationer
    supplements = analyzer.generate_supplement_recommendations()
    print("TOPP 5 SUPPLEMENT-REKOMMENDATIONER:")
    for i, s in enumerate(supplements[:5], 1):
        print(f"  {i}. {s.name}: {s.dosage}")

    print()
    print(f"Fullstandig instruktionsmanual sparad till:")
    print(f"  {output_path}")
    print()


if __name__ == "__main__":
    main()
