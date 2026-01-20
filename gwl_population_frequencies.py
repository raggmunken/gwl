"""
GWL Population Allele Frequencies Database
==========================================
Allelfrekvenser för kliniskt viktiga SNPs per population.
Data från gnomAD, 1000 Genomes, och CPIC.

Genetic Wellness Labs - Nutrigenomics Platform
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

# =============================================================================
# ENUMS
# =============================================================================

class Population(Enum):
    """Populationer enligt gnomAD/1000 Genomes klassificering"""
    EUR = "European (Europeisk)"
    EAS = "East Asian (Ostasiatisk)"
    AFR = "African/African American (Afrikansk)"
    SAS = "South Asian (Sydasiatisk)"
    AMR = "Latino/Admixed American (Latinamerikansk)"
    ASJ = "Ashkenazi Jewish (Ashkenazi-judisk)"
    FIN = "Finnish (Finsk)"
    NFE = "Non-Finnish European (Icke-finsk europeisk)"
    MID = "Middle Eastern"
    GLOBAL = "Global (alla populationer)"

class DataSource(Enum):
    GNOMAD = "gnomAD v4"
    THOUSAND_GENOMES = "1000 Genomes Phase 3"
    CPIC = "CPIC/PharmGKB"
    TOPMED = "TOPMed"
    HGVD = "Human Genetic Variation Database (Japan)"
    LITERATURE = "Publicerad litteratur"

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class AlleleFrequency:
    """Allelfrekvens för en specifik population"""
    population: Population
    ref_allele_freq: float
    alt_allele_freq: float
    sample_size: int
    source: DataSource

@dataclass
class SNPFrequencyData:
    """Komplett frekvendata för en SNP"""
    rsid: str
    gene: str
    ref_allele: str
    alt_allele: str
    chromosome: str
    position: int
    clinical_significance: str
    frequencies: Dict[Population, AlleleFrequency]
    notes: str

# =============================================================================
# METHYLATION GENE FREQUENCIES
# =============================================================================

MTHFR_C677T = SNPFrequencyData(
    rsid="rs1801133",
    gene="MTHFR",
    ref_allele="G",  # = C på aminosyranivå
    alt_allele="A",  # = T på aminosyranivå (677T)
    chromosome="1",
    position=11856378,
    clinical_significance="MTHFR C677T - Termolabilt enzym, påverkar folatmetabolism",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.64, 0.36, 64603, DataSource.GNOMAD),
        Population.NFE: AlleleFrequency(Population.NFE, 0.63, 0.37, 56885, DataSource.GNOMAD),
        Population.FIN: AlleleFrequency(Population.FIN, 0.77, 0.23, 10824, DataSource.GNOMAD),
        Population.EAS: AlleleFrequency(Population.EAS, 0.72, 0.28, 9977, DataSource.GNOMAD),
        Population.AFR: AlleleFrequency(Population.AFR, 0.90, 0.10, 12487, DataSource.GNOMAD),
        Population.SAS: AlleleFrequency(Population.SAS, 0.85, 0.15, 15308, DataSource.GNOMAD),
        Population.AMR: AlleleFrequency(Population.AMR, 0.55, 0.45, 7647, DataSource.GNOMAD),  # Högst!
        Population.ASJ: AlleleFrequency(Population.ASJ, 0.67, 0.33, 5076, DataSource.GNOMAD),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.70, 0.30, 151796, DataSource.GNOMAD)
    },
    notes="T-allelen (677T) är vanligast i Latinamerika (~45%) och lägst i Afrika (~10%). "
          "Homozygot TT ger ~30% enzymaktivitet."
)

MTHFR_A1298C = SNPFrequencyData(
    rsid="rs1801131",
    gene="MTHFR",
    ref_allele="T",  # = A på aminosyranivå
    alt_allele="G",  # = C på aminosyranivå (1298C)
    chromosome="1",
    position=11854476,
    clinical_significance="MTHFR A1298C - Reducerad aktivitet, påverkar BH4-regenerering",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.68, 0.32, 64603, DataSource.GNOMAD),
        Population.NFE: AlleleFrequency(Population.NFE, 0.67, 0.33, 56885, DataSource.GNOMAD),
        Population.FIN: AlleleFrequency(Population.FIN, 0.73, 0.27, 10824, DataSource.GNOMAD),
        Population.EAS: AlleleFrequency(Population.EAS, 0.78, 0.22, 9977, DataSource.GNOMAD),
        Population.AFR: AlleleFrequency(Population.AFR, 0.75, 0.25, 12487, DataSource.GNOMAD),
        Population.SAS: AlleleFrequency(Population.SAS, 0.70, 0.30, 15308, DataSource.GNOMAD),
        Population.AMR: AlleleFrequency(Population.AMR, 0.72, 0.28, 7647, DataSource.GNOMAD),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.71, 0.29, 151796, DataSource.GNOMAD)
    },
    notes="Jämnare fördelning mellan populationer jämfört med C677T."
)

COMT_VAL158MET = SNPFrequencyData(
    rsid="rs4680",
    gene="COMT",
    ref_allele="G",  # = Val
    alt_allele="A",  # = Met
    chromosome="22",
    position=19963748,
    clinical_significance="COMT Val158Met - Låg COMT (Met) = högre dopamin, ångestkänslighet",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.52, 0.48, 64603, DataSource.GNOMAD),
        Population.NFE: AlleleFrequency(Population.NFE, 0.52, 0.48, 56885, DataSource.GNOMAD),
        Population.FIN: AlleleFrequency(Population.FIN, 0.53, 0.47, 10824, DataSource.GNOMAD),
        Population.EAS: AlleleFrequency(Population.EAS, 0.72, 0.28, 9977, DataSource.GNOMAD),  # Mer Val
        Population.AFR: AlleleFrequency(Population.AFR, 0.69, 0.31, 12487, DataSource.GNOMAD),
        Population.SAS: AlleleFrequency(Population.SAS, 0.58, 0.42, 15308, DataSource.GNOMAD),
        Population.AMR: AlleleFrequency(Population.AMR, 0.58, 0.42, 7647, DataSource.GNOMAD),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.58, 0.42, 151796, DataSource.GNOMAD)
    },
    notes="Met-allelen är vanligare i Europa (~48%) än i Ostasien (~28%). "
          "Warrior (Val/Val) vs Worrier (Met/Met) fenotyp."
)

# =============================================================================
# VITAMIN D GENE FREQUENCIES
# =============================================================================

VDR_FOKI = SNPFrequencyData(
    rsid="rs2228570",
    gene="VDR",
    ref_allele="G",  # = f (lång receptor)
    alt_allele="A",  # = F (kort, mer aktiv receptor)
    chromosome="12",
    position=47879112,
    clinical_significance="VDR FokI - Påverkar D-vitaminreceptorfunktion",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.62, 0.38, 64603, DataSource.GNOMAD),
        Population.EAS: AlleleFrequency(Population.EAS, 0.56, 0.44, 9977, DataSource.GNOMAD),
        Population.AFR: AlleleFrequency(Population.AFR, 0.50, 0.50, 12487, DataSource.GNOMAD),
        Population.SAS: AlleleFrequency(Population.SAS, 0.58, 0.42, 15308, DataSource.GNOMAD),
        Population.AMR: AlleleFrequency(Population.AMR, 0.55, 0.45, 7647, DataSource.GNOMAD),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.58, 0.42, 151796, DataSource.GNOMAD)
    },
    notes="F-allelen (kort receptor, mer aktiv) är jämnt fördelad."
)

CYP2R1 = SNPFrequencyData(
    rsid="rs10741657",
    gene="CYP2R1",
    ref_allele="G",
    alt_allele="A",
    chromosome="11",
    position=14914878,
    clinical_significance="CYP2R1 - Påverkar 25-hydroxylering av D-vitamin",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.62, 0.38, 64603, DataSource.GNOMAD),
        Population.EAS: AlleleFrequency(Population.EAS, 0.70, 0.30, 9977, DataSource.GNOMAD),
        Population.AFR: AlleleFrequency(Population.AFR, 0.35, 0.65, 12487, DataSource.GNOMAD),  # Annorlunda!
        Population.SAS: AlleleFrequency(Population.SAS, 0.55, 0.45, 15308, DataSource.GNOMAD),
        Population.AMR: AlleleFrequency(Population.AMR, 0.50, 0.50, 7647, DataSource.GNOMAD),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.55, 0.45, 151796, DataSource.GNOMAD)
    },
    notes="A-allelen (reducerad hydroxylering) är vanligare i Afrika (~65%)."
)

# =============================================================================
# CYP PHARMACOGENES
# =============================================================================

CYP2D6_4 = SNPFrequencyData(
    rsid="rs3892097",
    gene="CYP2D6",
    ref_allele="C",
    alt_allele="T",  # *4 allel
    chromosome="22",
    position=42128945,
    clinical_significance="CYP2D6*4 - Null-allel, ingen enzymaktivitet",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.78, 0.22, 64603, DataSource.CPIC),
        Population.NFE: AlleleFrequency(Population.NFE, 0.77, 0.23, 56885, DataSource.CPIC),
        Population.FIN: AlleleFrequency(Population.FIN, 0.78, 0.22, 10824, DataSource.CPIC),
        Population.EAS: AlleleFrequency(Population.EAS, 0.99, 0.01, 9977, DataSource.CPIC),  # Sällsynt!
        Population.AFR: AlleleFrequency(Population.AFR, 0.98, 0.02, 12487, DataSource.CPIC),
        Population.SAS: AlleleFrequency(Population.SAS, 0.92, 0.08, 15308, DataSource.CPIC),
        Population.AMR: AlleleFrequency(Population.AMR, 0.88, 0.12, 7647, DataSource.CPIC),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.85, 0.15, 151796, DataSource.CPIC)
    },
    notes="*4 allelen är nästan uteslutande europeisk (~22%). Mycket sällsynt i Ostasien (<1%)."
)

CYP2D6_10 = SNPFrequencyData(
    rsid="rs1065852",
    gene="CYP2D6",
    ref_allele="C",
    alt_allele="T",  # *10 allel
    chromosome="22",
    position=42129770,
    clinical_significance="CYP2D6*10 - Reducerad aktivitet, instabilt enzym",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.98, 0.02, 64603, DataSource.CPIC),
        Population.EAS: AlleleFrequency(Population.EAS, 0.55, 0.45, 9977, DataSource.CPIC),  # Mycket vanlig!
        Population.AFR: AlleleFrequency(Population.AFR, 0.95, 0.05, 12487, DataSource.CPIC),
        Population.SAS: AlleleFrequency(Population.SAS, 0.92, 0.08, 15308, DataSource.CPIC),
        Population.AMR: AlleleFrequency(Population.AMR, 0.95, 0.05, 7647, DataSource.CPIC),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.85, 0.15, 151796, DataSource.CPIC)
    },
    notes="*10 är den vanligaste reducerande allelen i Ostasien (~45%). "
          "Förklarar varför lägre doser ofta behövs i asiatiska populationer."
)

CYP2C19_2 = SNPFrequencyData(
    rsid="rs4244285",
    gene="CYP2C19",
    ref_allele="G",
    alt_allele="A",  # *2 allel
    chromosome="10",
    position=94781859,
    clinical_significance="CYP2C19*2 - Null-allel, ingen enzymaktivitet",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.85, 0.15, 64603, DataSource.CPIC),
        Population.NFE: AlleleFrequency(Population.NFE, 0.85, 0.15, 56885, DataSource.CPIC),
        Population.EAS: AlleleFrequency(Population.EAS, 0.70, 0.30, 9977, DataSource.CPIC),  # Dubbelt så vanlig!
        Population.AFR: AlleleFrequency(Population.AFR, 0.83, 0.17, 12487, DataSource.CPIC),
        Population.SAS: AlleleFrequency(Population.SAS, 0.68, 0.32, 15308, DataSource.CPIC),
        Population.AMR: AlleleFrequency(Population.AMR, 0.88, 0.12, 7647, DataSource.CPIC),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.80, 0.20, 151796, DataSource.CPIC)
    },
    notes="*2 är dubbelt så vanlig i Ostasien (~30%) jämfört med Europa (~15%). "
          "Kritiskt för clopidogrel - FDA Black Box Warning."
)

CYP2C19_17 = SNPFrequencyData(
    rsid="rs12248560",
    gene="CYP2C19",
    ref_allele="C",
    alt_allele="T",  # *17 allel
    chromosome="10",
    position=94761900,
    clinical_significance="CYP2C19*17 - Ökad aktivitet, snabb metabolism",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.79, 0.21, 64603, DataSource.CPIC),
        Population.NFE: AlleleFrequency(Population.NFE, 0.79, 0.21, 56885, DataSource.CPIC),
        Population.EAS: AlleleFrequency(Population.EAS, 0.98, 0.02, 9977, DataSource.CPIC),  # Sällsynt
        Population.AFR: AlleleFrequency(Population.AFR, 0.82, 0.18, 12487, DataSource.CPIC),
        Population.SAS: AlleleFrequency(Population.SAS, 0.88, 0.12, 15308, DataSource.CPIC),
        Population.AMR: AlleleFrequency(Population.AMR, 0.85, 0.15, 7647, DataSource.CPIC),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.85, 0.15, 151796, DataSource.CPIC)
    },
    notes="*17 (snabb) är vanligare i Europa (~21%) och sällsynt i Ostasien (~2%). "
          "Risk för behandlingssvikt med PPI."
)

CYP2C9_2 = SNPFrequencyData(
    rsid="rs1799853",
    gene="CYP2C9",
    ref_allele="C",
    alt_allele="T",  # *2 allel
    chromosome="10",
    position=94942290,
    clinical_significance="CYP2C9*2 - Reducerad aktivitet (~70%)",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.87, 0.13, 64603, DataSource.CPIC),
        Population.NFE: AlleleFrequency(Population.NFE, 0.87, 0.13, 56885, DataSource.CPIC),
        Population.EAS: AlleleFrequency(Population.EAS, 0.99, 0.01, 9977, DataSource.CPIC),  # Sällsynt
        Population.AFR: AlleleFrequency(Population.AFR, 0.97, 0.03, 12487, DataSource.CPIC),
        Population.SAS: AlleleFrequency(Population.SAS, 0.90, 0.10, 15308, DataSource.CPIC),
        Population.AMR: AlleleFrequency(Population.AMR, 0.92, 0.08, 7647, DataSource.CPIC),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.90, 0.10, 151796, DataSource.CPIC)
    },
    notes="*2 och *3 är nästan uteslutande europeiska. Kritiskt för warfarindosering."
)

CYP2C9_3 = SNPFrequencyData(
    rsid="rs1057910",
    gene="CYP2C9",
    ref_allele="A",
    alt_allele="C",  # *3 allel
    chromosome="10",
    position=94981296,
    clinical_significance="CYP2C9*3 - Kraftigt reducerad aktivitet (~20%)",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.93, 0.07, 64603, DataSource.CPIC),
        Population.NFE: AlleleFrequency(Population.NFE, 0.93, 0.07, 56885, DataSource.CPIC),
        Population.EAS: AlleleFrequency(Population.EAS, 0.97, 0.03, 9977, DataSource.CPIC),
        Population.AFR: AlleleFrequency(Population.AFR, 0.98, 0.02, 12487, DataSource.CPIC),
        Population.SAS: AlleleFrequency(Population.SAS, 0.95, 0.05, 15308, DataSource.CPIC),
        Population.AMR: AlleleFrequency(Population.AMR, 0.95, 0.05, 7647, DataSource.CPIC),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.95, 0.05, 151796, DataSource.CPIC)
    },
    notes="*3 ger kraftigare reduktion än *2. Warfarindos kan behöva reduceras 70-80% vid *3/*3."
)

# =============================================================================
# CARDIOVASCULAR FREQUENCIES
# =============================================================================

APOE_RS429358 = SNPFrequencyData(
    rsid="rs429358",
    gene="APOE",
    ref_allele="T",  # e2/e3
    alt_allele="C",  # e4
    chromosome="19",
    position=44908684,
    clinical_significance="APOE - Skiljer e4 från e2/e3",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.85, 0.15, 64603, DataSource.GNOMAD),
        Population.NFE: AlleleFrequency(Population.NFE, 0.85, 0.15, 56885, DataSource.GNOMAD),
        Population.FIN: AlleleFrequency(Population.FIN, 0.80, 0.20, 10824, DataSource.GNOMAD),
        Population.EAS: AlleleFrequency(Population.EAS, 0.91, 0.09, 9977, DataSource.GNOMAD),
        Population.AFR: AlleleFrequency(Population.AFR, 0.73, 0.27, 12487, DataSource.GNOMAD),  # Högst e4!
        Population.SAS: AlleleFrequency(Population.SAS, 0.89, 0.11, 15308, DataSource.GNOMAD),
        Population.AMR: AlleleFrequency(Population.AMR, 0.86, 0.14, 7647, DataSource.GNOMAD),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.85, 0.15, 151796, DataSource.GNOMAD)
    },
    notes="e4 allelen (C) är vanligast i Afrika (~27%) och lägst i Ostasien (~9%). "
          "Alzheimer och CVD-risk."
)

APOE_RS7412 = SNPFrequencyData(
    rsid="rs7412",
    gene="APOE",
    ref_allele="C",  # e3/e4
    alt_allele="T",  # e2
    chromosome="19",
    position=44908822,
    clinical_significance="APOE - Skiljer e2 från e3/e4",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.92, 0.08, 64603, DataSource.GNOMAD),
        Population.NFE: AlleleFrequency(Population.NFE, 0.92, 0.08, 56885, DataSource.GNOMAD),
        Population.FIN: AlleleFrequency(Population.FIN, 0.93, 0.07, 10824, DataSource.GNOMAD),
        Population.EAS: AlleleFrequency(Population.EAS, 0.90, 0.10, 9977, DataSource.GNOMAD),
        Population.AFR: AlleleFrequency(Population.AFR, 0.96, 0.04, 12487, DataSource.GNOMAD),
        Population.SAS: AlleleFrequency(Population.SAS, 0.95, 0.05, 15308, DataSource.GNOMAD),
        Population.AMR: AlleleFrequency(Population.AMR, 0.94, 0.06, 7647, DataSource.GNOMAD),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.93, 0.07, 151796, DataSource.GNOMAD)
    },
    notes="e2 allelen (T) är relativt jämnt fördelad (~5-10%). Skyddande mot Alzheimer."
)

VKORC1 = SNPFrequencyData(
    rsid="rs9923231",
    gene="VKORC1",
    ref_allele="G",  # Högre warfarindos
    alt_allele="A",  # Lägre warfarindos
    chromosome="16",
    position=31096368,
    clinical_significance="VKORC1 -1639G>A - Påverkar warfarinkänslighet",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.42, 0.58, 64603, DataSource.CPIC),  # A vanligare!
        Population.NFE: AlleleFrequency(Population.NFE, 0.42, 0.58, 56885, DataSource.CPIC),
        Population.EAS: AlleleFrequency(Population.EAS, 0.10, 0.90, 9977, DataSource.CPIC),   # Mycket A!
        Population.AFR: AlleleFrequency(Population.AFR, 0.90, 0.10, 12487, DataSource.CPIC),  # Mest G
        Population.SAS: AlleleFrequency(Population.SAS, 0.25, 0.75, 15308, DataSource.CPIC),
        Population.AMR: AlleleFrequency(Population.AMR, 0.45, 0.55, 7647, DataSource.CPIC),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.45, 0.55, 151796, DataSource.CPIC)
    },
    notes="Dramatisk skillnad: A-allelen (lägre dos) ~90% i Ostasien, ~10% i Afrika. "
          "Förklarar varför asiater behöver lägre warfarindoser."
)

SLCO1B1 = SNPFrequencyData(
    rsid="rs4149056",
    gene="SLCO1B1",
    ref_allele="T",  # Normal funktion
    alt_allele="C",  # Reducerad funktion (*5)
    chromosome="12",
    position=21178615,
    clinical_significance="SLCO1B1 *5 - Reducerad statintransport, myopatirisk",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.85, 0.15, 64603, DataSource.CPIC),
        Population.NFE: AlleleFrequency(Population.NFE, 0.85, 0.15, 56885, DataSource.CPIC),
        Population.EAS: AlleleFrequency(Population.EAS, 0.85, 0.15, 9977, DataSource.CPIC),
        Population.AFR: AlleleFrequency(Population.AFR, 0.98, 0.02, 12487, DataSource.CPIC),  # Sällsynt
        Population.SAS: AlleleFrequency(Population.SAS, 0.90, 0.10, 15308, DataSource.CPIC),
        Population.AMR: AlleleFrequency(Population.AMR, 0.90, 0.10, 7647, DataSource.CPIC),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.88, 0.12, 151796, DataSource.CPIC)
    },
    notes="*5 allelen är sällsynt i Afrika (~2%). 16x ökad myopatirisk vid CC."
)

# =============================================================================
# INFLAMMATION FREQUENCIES
# =============================================================================

IL6_174 = SNPFrequencyData(
    rsid="rs1800795",
    gene="IL6",
    ref_allele="G",  # Lägre IL-6
    alt_allele="C",  # Högre IL-6
    chromosome="7",
    position=22727026,
    clinical_significance="IL-6 -174G>C - Påverkar IL-6-produktion",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.58, 0.42, 64603, DataSource.GNOMAD),
        Population.NFE: AlleleFrequency(Population.NFE, 0.58, 0.42, 56885, DataSource.GNOMAD),
        Population.EAS: AlleleFrequency(Population.EAS, 1.00, 0.00, 9977, DataSource.GNOMAD),  # G fixerad!
        Population.AFR: AlleleFrequency(Population.AFR, 0.97, 0.03, 12487, DataSource.GNOMAD),
        Population.SAS: AlleleFrequency(Population.SAS, 0.88, 0.12, 15308, DataSource.GNOMAD),
        Population.AMR: AlleleFrequency(Population.AMR, 0.70, 0.30, 7647, DataSource.GNOMAD),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.75, 0.25, 151796, DataSource.GNOMAD)
    },
    notes="C-allelen (högre IL-6) nästan uteslutande europeisk (~42%). "
          "Nästan helt frånvarande i Ostasien."
)

TNF_308 = SNPFrequencyData(
    rsid="rs1800629",
    gene="TNF",
    ref_allele="G",  # Normal
    alt_allele="A",  # Högre TNF-alfa
    chromosome="6",
    position=31543031,
    clinical_significance="TNF-alfa -308G>A - Högre TNF-produktion vid A",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.84, 0.16, 64603, DataSource.GNOMAD),
        Population.NFE: AlleleFrequency(Population.NFE, 0.84, 0.16, 56885, DataSource.GNOMAD),
        Population.EAS: AlleleFrequency(Population.EAS, 0.97, 0.03, 9977, DataSource.GNOMAD),
        Population.AFR: AlleleFrequency(Population.AFR, 0.85, 0.15, 12487, DataSource.GNOMAD),
        Population.SAS: AlleleFrequency(Population.SAS, 0.92, 0.08, 15308, DataSource.GNOMAD),
        Population.AMR: AlleleFrequency(Population.AMR, 0.88, 0.12, 7647, DataSource.GNOMAD),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.88, 0.12, 151796, DataSource.GNOMAD)
    },
    notes="A-allelen vanligare i Europa (~16%) än Ostasien (~3%)."
)

# =============================================================================
# OMEGA-3 METABOLISM
# =============================================================================

FADS1 = SNPFrequencyData(
    rsid="rs174546",
    gene="FADS1",
    ref_allele="C",  # Högre desaturasaktivitet
    alt_allele="T",  # Lägre aktivitet
    chromosome="11",
    position=61569830,
    clinical_significance="FADS1 - Påverkar omega-6/3 konvertering",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.67, 0.33, 64603, DataSource.GNOMAD),
        Population.NFE: AlleleFrequency(Population.NFE, 0.67, 0.33, 56885, DataSource.GNOMAD),
        Population.EAS: AlleleFrequency(Population.EAS, 0.64, 0.36, 9977, DataSource.GNOMAD),
        Population.AFR: AlleleFrequency(Population.AFR, 0.98, 0.02, 12487, DataSource.GNOMAD),  # Nästan fixerad C!
        Population.SAS: AlleleFrequency(Population.SAS, 0.72, 0.28, 15308, DataSource.GNOMAD),
        Population.AMR: AlleleFrequency(Population.AMR, 0.80, 0.20, 7647, DataSource.GNOMAD),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.75, 0.25, 151796, DataSource.GNOMAD)
    },
    notes="T-allelen (lägre konvertering) är sällsynt i Afrika (~2%) men vanlig i Europa (~33%). "
          "Afrikaner konverterar ALA->EPA effektivare, europeéer behöver preformerad EPA/DHA."
)

# =============================================================================
# DETOX GENES
# =============================================================================

GSTT1_NULL = SNPFrequencyData(
    rsid="GSTT1_del",
    gene="GSTT1",
    ref_allele="present",
    alt_allele="null (deletion)",
    chromosome="22",
    position=0,  # CNV
    clinical_significance="GSTT1 null - Ingen GSTT1-aktivitet",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.80, 0.20, 10000, DataSource.LITERATURE),
        Population.EAS: AlleleFrequency(Population.EAS, 0.50, 0.50, 10000, DataSource.LITERATURE),  # Mycket vanlig!
        Population.AFR: AlleleFrequency(Population.AFR, 0.75, 0.25, 10000, DataSource.LITERATURE),
        Population.SAS: AlleleFrequency(Population.SAS, 0.70, 0.30, 10000, DataSource.LITERATURE),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.70, 0.30, 50000, DataSource.LITERATURE)
    },
    notes="GSTT1 null (deletion) är mycket vanlig i Ostasien (~50%). CNV-analys krävs."
)

GSTM1_NULL = SNPFrequencyData(
    rsid="GSTM1_del",
    gene="GSTM1",
    ref_allele="present",
    alt_allele="null (deletion)",
    chromosome="1",
    position=0,  # CNV
    clinical_significance="GSTM1 null - Ingen GSTM1-aktivitet",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.50, 0.50, 10000, DataSource.LITERATURE),
        Population.EAS: AlleleFrequency(Population.EAS, 0.45, 0.55, 10000, DataSource.LITERATURE),
        Population.AFR: AlleleFrequency(Population.AFR, 0.70, 0.30, 10000, DataSource.LITERATURE),
        Population.SAS: AlleleFrequency(Population.SAS, 0.55, 0.45, 10000, DataSource.LITERATURE),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.55, 0.45, 50000, DataSource.LITERATURE)
    },
    notes="GSTM1 null (deletion) är vanlig i alla populationer (~40-55%). CNV-analys krävs."
)

# =============================================================================
# HLA FREQUENCIES
# =============================================================================

HLA_B5701 = SNPFrequencyData(
    rsid="rs2395029",
    gene="HLA-B*57:01",
    ref_allele="G",
    alt_allele="T",  # HLA-B*57:01 tag
    chromosome="6",
    position=31381296,
    clinical_significance="HLA-B*57:01 - Abacaviröverkänslighet",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.94, 0.06, 64603, DataSource.CPIC),  # ~6% bärare
        Population.NFE: AlleleFrequency(Population.NFE, 0.94, 0.06, 56885, DataSource.CPIC),
        Population.EAS: AlleleFrequency(Population.EAS, 0.99, 0.01, 9977, DataSource.CPIC),   # Sällsynt
        Population.AFR: AlleleFrequency(Population.AFR, 0.99, 0.01, 12487, DataSource.CPIC),  # Sällsynt
        Population.SAS: AlleleFrequency(Population.SAS, 0.97, 0.03, 15308, DataSource.CPIC),
        Population.AMR: AlleleFrequency(Population.AMR, 0.97, 0.03, 7647, DataSource.CPIC),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.96, 0.04, 151796, DataSource.CPIC)
    },
    notes="HLA-B*57:01 är vanligast hos kaukasier (~6%). Obligatoriskt test före abacavir."
)

# =============================================================================
# DPYD FOR FLUOROPYRIMIDINES
# =============================================================================

DPYD_2A = SNPFrequencyData(
    rsid="rs3918290",
    gene="DPYD",
    ref_allele="G",
    alt_allele="A",  # *2A allel
    chromosome="1",
    position=97915614,
    clinical_significance="DPYD*2A - Komplett DPD-brist, 5-FU toxicitet",
    frequencies={
        Population.EUR: AlleleFrequency(Population.EUR, 0.99, 0.01, 64603, DataSource.CPIC),
        Population.NFE: AlleleFrequency(Population.NFE, 0.99, 0.01, 56885, DataSource.CPIC),
        Population.EAS: AlleleFrequency(Population.EAS, 1.00, 0.00, 9977, DataSource.CPIC),   # Frånvarande
        Population.AFR: AlleleFrequency(Population.AFR, 0.998, 0.002, 12487, DataSource.CPIC),
        Population.GLOBAL: AlleleFrequency(Population.GLOBAL, 0.99, 0.01, 151796, DataSource.CPIC)
    },
    notes="*2A är sällsynt (~1% i Europa) men livshotande vid 5-FU. EMA kräver DPYD-test."
)

# =============================================================================
# COMPLETE FREQUENCY DATABASE
# =============================================================================

FREQUENCY_DATABASE: Dict[str, SNPFrequencyData] = {
    # Methylation
    "rs1801133": MTHFR_C677T,
    "rs1801131": MTHFR_A1298C,
    "rs4680": COMT_VAL158MET,

    # Vitamin D
    "rs2228570": VDR_FOKI,
    "rs10741657": CYP2R1,

    # CYP Pharmacogenes
    "rs3892097": CYP2D6_4,
    "rs1065852": CYP2D6_10,
    "rs4244285": CYP2C19_2,
    "rs12248560": CYP2C19_17,
    "rs1799853": CYP2C9_2,
    "rs1057910": CYP2C9_3,

    # Cardiovascular
    "rs429358": APOE_RS429358,
    "rs7412": APOE_RS7412,
    "rs9923231": VKORC1,
    "rs4149056": SLCO1B1,

    # Inflammation
    "rs1800795": IL6_174,
    "rs1800629": TNF_308,

    # Omega-3
    "rs174546": FADS1,

    # Detox (CNV)
    "GSTT1_del": GSTT1_NULL,
    "GSTM1_del": GSTM1_NULL,

    # HLA
    "rs2395029": HLA_B5701,

    # DPYD
    "rs3918290": DPYD_2A
}

# =============================================================================
# LOOKUP FUNCTIONS
# =============================================================================

def get_snp_frequency(rsid: str) -> Optional[SNPFrequencyData]:
    """Hämta frekvensdata för en specifik SNP."""
    return FREQUENCY_DATABASE.get(rsid)

def get_allele_frequency(rsid: str, population: Population) -> Optional[AlleleFrequency]:
    """Hämta allelfrekvens för en SNP i en specifik population."""
    snp = FREQUENCY_DATABASE.get(rsid)
    if snp:
        return snp.frequencies.get(population)
    return None

def compare_populations(rsid: str) -> Optional[Dict[str, float]]:
    """Jämför allelfrekvenser mellan alla populationer för en SNP."""
    snp = FREQUENCY_DATABASE.get(rsid)
    if not snp:
        return None

    result = {}
    for pop, freq in snp.frequencies.items():
        result[pop.value] = freq.alt_allele_freq
    return result

def get_snps_by_gene(gene: str) -> List[SNPFrequencyData]:
    """Hitta alla SNPs för en specifik gen."""
    return [snp for snp in FREQUENCY_DATABASE.values()
            if snp.gene.upper() == gene.upper()]

def get_population_specific_recommendations(genotypes: Dict[str, str], population: Population) -> List[Dict]:
    """
    Ge populationsspecifika rekommendationer baserat på genotyper.

    Args:
        genotypes: Dict med rsid -> genotyp
        population: Patientens population

    Returns:
        Lista med rekommendationer baserat på genotyp och populationsfrekvens
    """
    recommendations = []

    for rsid, genotype in genotypes.items():
        snp = FREQUENCY_DATABASE.get(rsid)
        if not snp:
            continue

        pop_freq = snp.frequencies.get(population)
        global_freq = snp.frequencies.get(Population.GLOBAL)

        if pop_freq and global_freq:
            # Räkna ut hur ovanlig genotypen är i populationen
            alt_count = genotype.count(snp.alt_allele)

            if alt_count == 2:  # Homozygot alt
                expected_freq = pop_freq.alt_allele_freq ** 2
            elif alt_count == 1:  # Heterozygot
                expected_freq = 2 * pop_freq.ref_allele_freq * pop_freq.alt_allele_freq
            else:  # Homozygot ref
                expected_freq = pop_freq.ref_allele_freq ** 2

            # Jämför med global frekvens
            global_expected = global_freq.alt_allele_freq ** alt_count if alt_count > 0 else global_freq.ref_allele_freq

            recommendations.append({
                "rsid": rsid,
                "gene": snp.gene,
                "genotype": genotype,
                "population_frequency": f"{expected_freq*100:.1f}%",
                "global_frequency": f"{global_expected*100:.1f}%",
                "rarer_in_population": expected_freq < global_expected * 0.5,
                "clinical_significance": snp.clinical_significance,
                "notes": snp.notes
            })

    return recommendations

def get_all_frequency_snps() -> List[str]:
    """Returnera alla SNPs med frekvensdata."""
    return list(FREQUENCY_DATABASE.keys())

def calculate_population_risk_score(genotypes: Dict[str, str], population: Population) -> Dict:
    """
    Beräkna en relativ riskscore baserat på populationsspecifika frekvenser.

    Args:
        genotypes: Dict med rsid -> genotyp
        population: Population

    Returns:
        Dict med riskscore och detaljer
    """
    scores = []
    details = []

    for rsid, genotype in genotypes.items():
        snp = FREQUENCY_DATABASE.get(rsid)
        if not snp:
            continue

        freq = snp.frequencies.get(population)
        if not freq:
            continue

        alt_count = genotype.count(snp.alt_allele)

        # Enkel viktning: ovanligare varianter ger högre poäng
        if alt_count == 2:
            rarity_score = (1 - freq.alt_allele_freq ** 2) * 2
        elif alt_count == 1:
            rarity_score = (1 - 2 * freq.ref_allele_freq * freq.alt_allele_freq)
        else:
            rarity_score = 0

        scores.append(rarity_score)
        details.append({
            "rsid": rsid,
            "gene": snp.gene,
            "genotype": genotype,
            "rarity_score": rarity_score
        })

    return {
        "total_score": sum(scores),
        "average_score": sum(scores) / len(scores) if scores else 0,
        "variants_analyzed": len(scores),
        "details": sorted(details, key=lambda x: x["rarity_score"], reverse=True)
    }

# =============================================================================
# MAIN / TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GWL POPULATION ALLELE FREQUENCIES DATABASE")
    print("=" * 70)

    print(f"\nAntal SNPs med frekvensdata: {len(FREQUENCY_DATABASE)}")

    print("\n" + "-" * 70)
    print("Populationsspecifika skillnader - Intressanta exempel:")
    print("-" * 70)

    interesting_snps = ["rs1801133", "rs3892097", "rs1065852", "rs4244285", "rs9923231", "rs1800795", "rs174546"]

    for rsid in interesting_snps:
        snp = FREQUENCY_DATABASE.get(rsid)
        if snp:
            print(f"\n{rsid} ({snp.gene}):")
            freqs = compare_populations(rsid)
            if freqs:
                sorted_freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
                for pop, freq in sorted_freqs[:3]:
                    print(f"  {pop}: {freq*100:.1f}%")

    print("\n" + "-" * 70)
    print("VKORC1 rs9923231 - Dramatisk populationsskillnad:")
    print("-" * 70)

    vkorc1 = FREQUENCY_DATABASE.get("rs9923231")
    if vkorc1:
        print(vkorc1.notes)
        for pop, freq in vkorc1.frequencies.items():
            if pop != Population.GLOBAL:
                print(f"  {pop.value}: A-allel {freq.alt_allele_freq*100:.0f}%")

    print("\n" + "-" * 70)
    print("TEST: Populationsspecifika rekommendationer")
    print("-" * 70)

    test_genotypes = {
        "rs1801133": "AA",  # MTHFR 677TT
        "rs4680": "AA",      # COMT Met/Met
        "rs3892097": "TT",   # CYP2D6 *4/*4
        "rs9923231": "AA"    # VKORC1 AA
    }

    print("\nFör en europeisk patient med dessa genotyper:")
    recommendations = get_population_specific_recommendations(test_genotypes, Population.EUR)
    for rec in recommendations:
        print(f"\n{rec['rsid']} ({rec['gene']}): {rec['genotype']}")
        print(f"  Population freq: {rec['population_frequency']}")
        print(f"  Global freq: {rec['global_frequency']}")

    print("\n" + "-" * 70)
    print("Alla SNPs i databasen:")
    print("-" * 70)
    for rsid in get_all_frequency_snps():
        snp = FREQUENCY_DATABASE[rsid]
        print(f"{rsid}: {snp.gene} - {snp.clinical_significance[:50]}...")

    print("\n" + "=" * 70)
    print("Databas laddad!")
    print("=" * 70)
