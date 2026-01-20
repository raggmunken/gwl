# GWL Nutrigenomics Platform - Development Status

## Projekt: Genetic Wellness Labs DNA Analyzer
**Datum:** 2026-01-19
**Status:** ✅ KOMPLETT - Unified Database & Analyzer färdiga!

---

## 🎯 SNABBSTART

```bash
# Analysera din 23andMe-fil:
python gwl_analyzer.py din_23andme_fil.txt --name "Ditt Namn"

# Se databasstatistik:
python gwl_analyzer.py --stats
```

**Output:** Genererar komplett rapport i Markdown och JSON med:
- Alla dina genetiska varianter
- APOE och MTHFR haplotyper
- Näringsrekommendationer med doser
- Livsstilsrekommendationer
- Läkemedelsvarningar (farmakogenomik)

---

## Projektöversikt

Ett komplett nutrigenomik-verktyg som analyserar 23andMe DNA-rådata och genererar personaliserade kost-, supplement- och livsstilsrekommendationer baserat på genetisk profil.

### Huvudfunktioner:
- Analys av 23andMe raw data (.txt format)
- Gen-näringämne interaktioner
- Haplotyp- och diplotypbestämning (APOE, CYP2D6, CYP2C19, etc.)
- Pathway-analys (metylering, detox, inflammation, neurotransmittorer)
- Gen-gen interaktioner (epistasis)
- Farmakogenomik (CPIC guidelines)
- Populationsfrekvenser för alleler (gnomAD, CPIC)
- Vetenskapliga referenser (PubMed)

---

## Skapade Filer - KOMPLETT LISTA

### 1. `gwl_gene_database.py`
**Status:** ✅ Klar
**Beskrivning:** Evidensbaserad gendatabas med 46 gener

### 2. `gwl_gene_fetcher.py`
**Status:** ✅ Klar
**Beskrivning:** Hämtar gendata från NCBI/PubMed
- 37 fördefinierade wellness-SNPs i 19 kategorier
- PubMed-artikelhämtning

### 3. `gwl_nutrient_database.py`
**Status:** ✅ Klar
**Beskrivning:** Komplett näringsdatabas
- D-vitamin, Omega-3, Magnesium, A-vitamin, L-Theanin
- Dosinfo: RDI, optimal, UL, LD50
- Genetiska modifierare

### 4. `gwl_transport_pathways.py`
**Status:** ✅ Klar
**Beskrivning:** Transportvägskonkurrens
- 6 transportsystem (DMT1, ZIP, kalciumkanaler, etc.)
- 15 näringsinteraktioner
- 9 gen-näringsinteraktioner

### 5. `gwl_haplotypes.py`
**Status:** ✅ Klar
**Beskrivning:** Haplotyper och diplotyper
- **APOE** (e2/e3/e4) - 6 diplotyper
- **CYP2D6** (*1, *2, *4, *10, *17, *xN) - 5 diplotyper
- **CYP2C19** (*1, *2, *3, *17) - 5 diplotyper
- **CYP2C9** (*1, *2, *3) - 6 diplotyper
- **VKORC1** - 3 genotyper
- **MTHFR** (C677T + A1298C) - 5 kombinationer
- **HLA-B*57:01** - 3 status
- **SLCO1B1** - 3 genotyper
- **COMT** (Val158Met) - 3 genotyper

**Funktioner:**
- `determine_apoe_haplotype(rs429358, rs7412)`
- `determine_mthfr_status(rs1801133, rs1801131)`
- `determine_cyp2d6_activity_score(allele1, allele2)`
- `get_metabolizer_status_from_score(score)`

### 6. `gwl_pathways.py`
**Status:** ✅ Klar
**Beskrivning:** 9 biologiska pathways

| Pathway | Gener | Näringsämnen |
|---------|-------|--------------|
| Metyleringscykeln | 8 | 7 |
| Transsulfurering | 5 | 7 |
| Fas I Detox (CYP450) | 8 | 5 |
| Fas II Detox | 8 | 7 |
| Inflammation | 7 | 7 |
| Antioxidantförsvar | 6 | 10 |
| Neurotransmittorer | 10 | 10 |
| BH4-cykeln | 4 | 5 |
| Dygnsrytm | 8 | 7 |

**Funktioner:**
- `get_pathway(pathway_id)`
- `find_gene_in_pathways(gene)`
- `find_nutrient_in_pathways(nutrient)`
- `assess_pathway_status(pathway_id, genetic_variants)`

### 7. `gwl_epistasis.py`
**Status:** ✅ Klar
**Beskrivning:** 12 gen-gen interaktioner

| Interaktion | Typ | Klinisk betydelse |
|-------------|-----|-------------------|
| MTHFR Compound | Synergistisk | Hög |
| MTHFR + MTR + MTRR | Synergistisk | Hög |
| COMT + MTHFR | Modifierande | Måttlig |
| GST Double Null | Synergistisk | Hög |
| CYP1B1 + COMT | Synergistisk | Hög |
| IL-6 + TNF-alfa | Synergistisk | Hög |
| FADS + IL-6 | Modifierande | Måttlig |
| APOE + CETP | Modifierande | Måttlig |
| COMT + MAO-A | Kompensatorisk | Måttlig |
| BDNF + COMT | Modifierande | Måttlig |
| CYP2D6 + CYP3A4 | Synergistisk | Hög |
| VDR + CYP2R1 | Modifierande | Måttlig |

**Funktioner:**
- `analyze_epistasis(genotypes)`
- `get_interactions_by_gene(gene)`
- `get_critical_interactions()`

### 8. `gwl_pharmacogenomics.py`
**Status:** ✅ Klar
**Beskrivning:** 14 läkemedel-gen-par (CPIC)

| Läkemedel | Gen | Evidens | Kategori |
|-----------|-----|---------|----------|
| Kodein | CYP2D6 | 1A | Smärta |
| Tramadol | CYP2D6 | 1A | Smärta |
| Clopidogrel | CYP2C19 | 1A | Kardio |
| Warfarin | CYP2C9/VKORC1 | 1A | Kardio |
| Simvastatin | SLCO1B1 | 1A | Kardio |
| Metoprolol | CYP2D6 | 2A | Kardio |
| Escitalopram | CYP2C19 | 1A | Psykiatri |
| Sertralin | CYP2C19 | 2A | Psykiatri |
| Amitriptylin | CYP2D6/CYP2C19 | 1A | Psykiatri |
| Tamoxifen | CYP2D6 | 1A | Onkologi |
| 5-Fluorouracil | DPYD | 1A | Onkologi |
| Abacavir | HLA-B*57:01 | 1A | Antiinfektiv |
| Omeprazol | CYP2C19 | 2A | GI |
| Tacrolimus | CYP3A5 | 1A | Immunsuppressiv |

**Funktioner:**
- `calculate_cyp2d6_activity_score(allele1, allele2)`
- `activity_score_to_phenotype(score)`
- `get_drugs_by_gene(gene)`
- `get_critical_warnings(phenotype)`
- `generate_pgx_report(genotypes)`

### 9. `gwl_population_frequencies.py`
**Status:** ✅ Klar
**Beskrivning:** Allelfrekvenser för 22 SNPs

**Populationer:**
- EUR (European)
- EAS (East Asian)
- AFR (African)
- SAS (South Asian)
- AMR (Latino/American)
- ASJ (Ashkenazi Jewish)
- FIN (Finnish)
- NFE (Non-Finnish European)

**Intressanta exempel:**
- VKORC1 rs9923231: A-allel 90% i EAS, 10% i AFR
- CYP2D6*4 rs3892097: 22% i EUR, <1% i EAS
- CYP2D6*10 rs1065852: 45% i EAS, 2% i EUR
- IL-6 rs1800795: C-allel 42% i EUR, 0% i EAS
- FADS1 rs174546: T-allel 33% i EUR, 2% i AFR

**Funktioner:**
- `get_snp_frequency(rsid)`
- `get_allele_frequency(rsid, population)`
- `compare_populations(rsid)`
- `get_population_specific_recommendations(genotypes, population)`

### 10. `gwl_master_fetcher.py`
**Status:** ✅ Klar
**Beskrivning:** Komplett hämtningsskript

**Kategorier (20 st, 100+ SNPs):**
- methylation, vitamin_d, omega3, stress_mood, caffeine
- sleep, iron, antioxidant, inflammation, detox_phase1
- detox_phase2, bone_health, blood_pressure, obesity
- histamine, blood_sugar, thyroid, muscle, immune
- skin, cardiovascular, pharmacogenomics, bh4_cycle

**Användning:**
```bash
python gwl_master_fetcher.py --list              # Lista kategorier
python gwl_master_fetcher.py --category methylation  # Hämta kategori
python gwl_master_fetcher.py --snp rs1801133    # Hämta specifik SNP
python gwl_master_fetcher.py --all              # Hämta ALLT
```

---

## Ursprungliga Filer

### `gwl_dna_analyzer.py`
Original DNA-analysator

### `gwl_complete_analyzer.py`
Komplett analysator (behöver integreras med nya moduler)

### `gwl_fetched_genes.json`
Tidigare hämtade gener

---

## Tekniska Detaljer

### Windows Encoding Fix
Alla filer använder:
```python
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

### Datastrukturer
- `@dataclass` för alla datamodeller
- `Enum` för kategorier, typer, fenotyper
- `Dict[str, ...]` för databaser
- Typade funktioner med `Optional`, `List`, `Tuple`, `Set`

### SNP Format
- rsid: rs-nummer (t.ex. rs1801133)
- Genotyp: Två alleler (t.ex. AA, AG, GG)
- 23andMe raw data-format hanteras

---

## Nästa Steg

1. ✅ ~~Skapa alla moduler~~
2. **Integrera alla moduler i `gwl_complete_analyzer.py`**
3. Testa med riktig 23andMe-data
4. Generera komplett GWL-profil med alla analyser

---

## Användningsexempel

### Analysera MTHFR-status:
```python
from gwl_haplotypes import determine_mthfr_status
status = determine_mthfr_status("GA", "TG")
# -> {'c677t': 'CT', 'a1298c': 'AC', 'phenotype': 'MTHFR CT/AC',
#     'severity': 'Compound heterozygot - reducerad aktivitet (~40-50%)'}
```

### Hitta gen-gen interaktioner:
```python
from gwl_epistasis import analyze_epistasis
results = analyze_epistasis({"rs1801133": "AA", "rs4680": "AA"})
```

### Kontrollera läkemedelsinteraktioner:
```python
from gwl_pharmacogenomics import get_drugs_by_gene, get_critical_warnings
warnings = get_critical_warnings(MetabolizerPhenotype.POOR)
```

### Populationsspecifika rekommendationer:
```python
from gwl_population_frequencies import get_population_specific_recommendations, Population
recs = get_population_specific_recommendations(genotypes, Population.EUR)
```

---

## Filstruktur

```
D:\CLAUDE_CODE\
├── gwl_gene_database.py          # Gendatabas (46 gener)
├── gwl_gene_fetcher.py           # NCBI/PubMed hämtare
├── gwl_nutrient_database.py      # Näringsdatabas
├── gwl_transport_pathways.py     # Transport & interaktioner
├── gwl_haplotypes.py             # Haplotyper (9 gener)
├── gwl_pathways.py               # Biologiska pathways (9 st)
├── gwl_epistasis.py              # Gen-gen interaktioner (12 st)
├── gwl_pharmacogenomics.py       # CPIC läkemedel (14 st)
├── gwl_population_frequencies.py # Allelfrekvenser (22 SNPs)
├── gwl_master_fetcher.py         # Master hämtare (100+ SNPs)
├── gwl_dna_analyzer.py           # Original analysator
├── gwl_complete_analyzer.py      # Komplett analysator
├── gwl_fetched_genes.json        # Hämtad data
└── GWL_DEVELOPMENT_STATUS.md     # Denna fil
```

---

## Referenser

Alla moduler innehåller PubMed-referenser (PMID) för evidensbasering.

**Huvudsakliga guidelines:**
- CPIC (Clinical Pharmacogenetics Implementation Consortium)
- DPWG (Dutch Pharmacogenetics Working Group)
- PharmGKB
- gnomAD (Genome Aggregation Database)
- 1000 Genomes Project
