"""
GWL Master Fetcher
==================
Komplett skript för att hämta all genetisk data från NCBI/PubMed.
Kör detta manuellt för att uppdatera databaserna med senaste forskning.

Genetic Wellness Labs - Nutrigenomics Platform

Användning:
    python gwl_master_fetcher.py --all              # Hämta allt
    python gwl_master_fetcher.py --genes            # Bara gener
    python gwl_master_fetcher.py --snps rs1801133   # Specifik SNP
    python gwl_master_fetcher.py --category methylation  # Kategori
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import json
import time
import re
import argparse
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Set
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote
from urllib.error import HTTPError, URLError

# =============================================================================
# CONFIGURATION
# =============================================================================

NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
RATE_LIMIT_DELAY = 0.35  # Sekunder mellan requests (NCBI limit: 3/s utan API-nyckel)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# COMPLETE SNP DATABASE - Alla SNPs att hämta
# =============================================================================

WELLNESS_SNPS = {
    # Metylering - Komplett one-carbon metabolism pathway
    "methylation": {
        "description": "Metyleringscykeln och folatmetabolism",
        "snps": [
            # MTHFR - central i folat→metylfolat konvertering
            "rs1801133",  # MTHFR C677T - 70% reducerad aktivitet vid TT
            "rs1801131",  # MTHFR A1298C - interagerar med C677T
            # MTR/MTRR - B12-beroende remetylering av homocystein
            "rs1805087",  # MTR A2756G - metioninsyntetas
            "rs1801394",  # MTRR A66G - metioninsyntetas reduktas
            "rs162036",   # MTRR - ytterligare variant, interagerar med rs1801394
            "rs10380",    # MTRR - påverkar B12-respons
            # BHMT - alternativ remetylering via betain
            "rs3733890",  # BHMT - betain-homocystein metyltransferas
            "rs567754",   # BHMT - påverkar betainbehov
            # CBS - transsulfureringsvägen
            "rs234706",   # CBS C699T - homocystein→cystein
            "rs2851391",  # CBS - ytterligare variant
            # SHMT - serin-glycin interkonvertering
            "rs1979277",  # SHMT1 - cytosolisk, folatcykel
            # FOLR/SLC - folattransport
            "rs1051266",  # SLC19A1 (RFC1) - folattransportör
            "rs602662",   # FUT2 - B12-absorption
            # DHFR - dihydrofolatreduktas
            "rs70991108", # DHFR 19bp del - folatmetabolism
            # TCN2 - B12-transport
            "rs1801198",  # TCN2 - transkobalamin, B12-leverans till celler
        ]
    },

    # D-vitamin - Syntes, aktivering, transport och receptorfunktion
    "vitamin_d": {
        "description": "D-vitaminmetabolism och receptorfunktion",
        "snps": [
            # VDR - vitamin D-receptor (alla interagerar)
            "rs2228570",  # VDR FokI - påverkar receptoraktivitet
            "rs1544410",  # VDR BsmI - mRNA-stabilitet
            "rs731236",   # VDR TaqI - kopplad till BsmI
            "rs7975232",  # VDR ApaI - haplotyp med BsmI/TaqI
            "rs11568820", # VDR Cdx2 - tarmabsorption av kalcium
            # CYP2R1 - lever 25-hydroxylas (D→25-OH-D)
            "rs10741657", # CYP2R1 - huvudenzym för 25-hydroxylering
            "rs12794714", # CYP2R1 - ytterligare variant
            # CYP27B1 - njur 1-alfa-hydroxylas (25-OH-D→1,25-OH-D)
            "rs10877012", # CYP27B1 - aktivering till aktiv form
            # CYP24A1 - nedbrytning av vitamin D
            "rs6013897",  # CYP24A1 - katabolism, påverkar halveringstid
            # DHCR7 - 7-dehydrokolesterol (hudsyntes)
            "rs12785878", # DHCR7 - prekursor för D3-syntes i hud
            # GC (DBP) - vitamin D-bindande protein (transport)
            "rs2282679",  # GC - huvudtransportör i blod
            "rs4588",     # GC - Thr436Lys, påverkar bindningsaffinitet
            "rs7041",     # GC - Asp432Glu, haplotyp med rs4588
        ]
    },

    # Omega-3 - Fettsyrasyntes och metabolism
    "omega3": {
        "description": "Fettsyrametabolism och desaturaser",
        "snps": [
            # FADS1 - delta-5-desaturas (DGLA→AA, EPA→DHA)
            "rs174546",   # FADS1 - stark effekt på omega-3/6 konvertering
            "rs174547",   # FADS1 - kopplad till rs174546
            "rs174548",   # FADS1 - haplotyp
            "rs174550",   # FADS1 - påverkar AA-nivåer
            # FADS2 - delta-6-desaturas (LA→GLA, ALA→SDA)
            "rs1535",     # FADS2 - rate-limiting steg
            "rs174575",   # FADS2 - påverkar EPA/DHA-syntes
            "rs174583",   # FADS2 - ytterligare variant
            "rs968567",   # FADS2 promotor - reglerar expression
            # ELOVL2 - elongering av fettsyror
            "rs953413",   # ELOVL2 - EPA→DPA→DHA elongering
            "rs3734398",  # ELOVL2 - påverkar DHA-nivåer
            # ELOVL5 - elongering
            "rs209512",   # ELOVL5 - GLA→DGLA elongering
            # PPARA - reglerar fettsyrametabolism
            "rs1800206",  # PPARA Leu162Val - fettsyraoxidation
        ]
    },

    # Stress & humör - Neurotransmittorsystem
    "stress_mood": {
        "description": "Neurotransmittorer och stressrespons",
        "snps": [
            # COMT - dopamin/noradrenalin nedbrytning (katekolaminer)
            "rs4680",     # COMT Val158Met - "warrior vs worrier"
            "rs4633",     # COMT - haplotyp med Val158Met
            "rs4818",     # COMT - påverkar enzymaktivitet
            # BDNF - neuroplasticitet och stressresiliens
            "rs6265",     # BDNF Val66Met - sekretion och plasticitet
            "rs7124442",  # BDNF - påverkar expression
            # MAO-A - serotonin/dopamin/noradrenalin nedbrytning
            "rs6323",     # MAO-A - enzymaktivitet
            "rs1137070",  # MAO-A - ytterligare variant
            # MAO-B - dopamin-specifik
            "rs1799836",  # MAO-B - dopaminmetabolism
            # Dopaminsystemet
            "rs1800497",  # DRD2/ANKK1 Taq1A - dopaminreceptor densitet
            "rs1799732",  # DRD2 -141C - receptorexpression
            "rs1800955",  # DRD4 -521C/T - novelty seeking
            "rs747302",   # DRD1 - belöningssystem
            # Serotoninsystemet
            "rs4570625",  # TPH2 - serotoninsyntes i hjärnan
            "rs25531",    # SLC6A4 (5-HTTLPR) - serotonintransportör
            "rs6295",     # HTR1A - serotonin 1A-receptor
            "rs6313",     # HTR2A - serotonin 2A-receptor
            # Oxytocin - social bonding
            "rs53576",    # OXTR - oxytocinreceptor
            "rs2254298",  # OXTR - social kognition
            # HPA-axel (stressrespons)
            "rs41423247", # NR3C1 - glukokortikoidreceptor
            "rs5522",     # NR3C2 - mineralokortikoidreceptor
            # GABA-system
            "rs211014",   # GABRA2 - ångest och stressrespons
        ]
    },

    # Koffein - Metabolism och känslighet
    "caffeine": {
        "description": "Koffeinmetabolism",
        "snps": [
            # CYP1A2 - huvudenzym för koffeinmetabolism
            "rs762551",   # CYP1A2 *1F - snabb/långsam metaboliserare
            "rs2069514",  # CYP1A2 *1C - reducerad aktivitet
            # AHR - reglerar CYP1A2-expression
            "rs4410790",  # AHR - påverkar CYP1A2-induktion
            "rs6968865",  # AHR - kopplad till koffeinkonsumtion
            # ADORA2A - adenosinreceptor (koffeinets mål)
            "rs5751876",  # ADORA2A - koffeinkänslighet, sömnpåverkan
            "rs2298383",  # ADORA2A - ångestrespons på koffein
        ]
    },

    # Sömn - Cirkadisk klocka och sömnreglering
    "sleep": {
        "description": "Dygnsrytm och sömn",
        "snps": [
            # CLOCK - central klockgen
            "rs1801260",  # CLOCK 3111T/C - kvällsmänniska
            "rs3749474",  # CLOCK - sömnlängd
            # PER-gener - periodgener
            "rs2304672",  # PER2 - fas-förskjutning
            "rs934945",   # PER2 - morgon/kvällspreferens
            "rs57875989", # PER3 VNTR - sömnbehov
            "rs228697",   # PER3 - sömnhomeostas
            # CRY-gener - kryptokromer
            "rs2287161",  # CRY1 - försenad sömnfas
            "rs8192440",  # CRY2 - depression och sömn
            # Melatoninsystemet
            "rs10830963", # MTNR1B - melatoninreceptor 1B
            "rs4753426",  # MTNR1B - melatoninkänslighet
            "rs12506228", # ASMT - melatoninsyntes
            # Adenosinsystemet (sömnhomeostas)
            "rs5751876",  # ADORA2A - sömnbehov efter vakenhet
            # NPAS2 - CLOCK-paralog i hjärnan
            "rs2305160",  # NPAS2 - cirkadisk reglering
        ]
    },

    # Järn - Absorption, transport och lagring
    "iron": {
        "description": "Järnmetabolism och hemokromatos",
        "snps": [
            # HFE - järnabsorptionsreglering
            "rs1800562",  # HFE C282Y - hemokromatos huvudmutation
            "rs1799945",  # HFE H63D - mildare variant, interagerar med C282Y
            "rs1800730",  # HFE S65C - tredje HFE-variant
            # TMPRSS6 - hepcidinreglering
            "rs855791",   # TMPRSS6 - påverkar järnstatus
            "rs4820268",  # TMPRSS6 - ytterligare variant
            # TF - transferrin (järntransport)
            "rs3811647",  # TF - transferrinnivåer
            "rs1799852",  # TF - järnbindning
            # TFR2 - transferrinreceptor 2
            "rs7385804",  # TFR2 - järnsensing
            # HAMP - hepcidin (masterregulator)
            "rs10421768", # HAMP - järnhomeostas
            # SLC11A2 (DMT1) - järnabsorption i tarm
            "rs224589",   # SLC11A2 - järnupptag
        ]
    },

    # Antioxidant - Försvarssystem mot oxidativ stress
    "antioxidant": {
        "description": "Antioxidantförsvar och oxidativ stress",
        "snps": [
            # SOD - superoxiddismutas (första försvarslinjen)
            "rs4880",     # SOD2 Ala16Val - mitokondriell, kritisk
            "rs2070424",  # SOD1 - cytosolisk
            "rs2536512",  # SOD3 - extracellulär
            # CAT - katalas (H2O2→H2O)
            "rs1001179",  # CAT -262C/T - promotor
            "rs769217",   # CAT - enzymaktivitet
            # GPX - glutationperoxidas
            "rs1050450",  # GPX1 Pro198Leu - selenoenzym
            "rs713041",   # GPX4 - lipidperoxidation
            # NRF2 (NFE2L2) - master antioxidant regulator
            "rs6721961",  # NRF2 -617C/A - aktiverar ARE-gener
            "rs35652124", # NRF2 - ytterligare promotorvariant
            # NQO1 - kinonreduktas
            "rs1800566",  # NQO1 Pro187Ser - CoQ10-aktivering
            # Glutationsystemet
            "rs1695",     # GSTP1 - glutationtransferas (även detox)
            "rs17883901", # GCLC - glutationsyntes
            "rs3170633",  # GCLM - glutationsyntes
            # Tioredoxinsystemet
            "rs1139793",  # TXNRD1 - tioredoxinreduktas
        ]
    },

    # Inflammation - Cytokiner och inflammationsreglering
    "inflammation": {
        "description": "Inflammationsreglering och cytokiner",
        "snps": [
            # IL-6 pathway
            "rs1800795",  # IL-6 -174G>C - proinflammatorisk
            "rs1800796",  # IL-6 -572G>C - promotor
            "rs2228145",  # IL6R - receptorvariant (sIL-6R)
            # TNF-alfa pathway
            "rs1800629",  # TNF-a -308G>A - stark effekt
            "rs361525",   # TNF-a -238G>A - promotor
            "rs1799964",  # TNF-a -1031T>C - haplotyp
            # IL-1 pathway
            "rs16944",    # IL-1B -511C>T - promotor
            "rs1143634",  # IL-1B +3954C>T - exon 5
            "rs1143627",  # IL-1B -31T>C - TATA-box
            "rs315952",   # IL-1RN - receptorantagonist
            # IL-10 (antiinflammatorisk)
            "rs1800896",  # IL-10 -1082G>A - balanserar inflammation
            "rs1800871",  # IL-10 -819C>T - haplotyp
            # CRP - inflammationsmarkör
            "rs1205",     # CRP - basnivåer
            "rs3093077",  # CRP - ytterligare variant
            # COX-2/prostaglandiner
            "rs20417",    # PTGS2 (COX-2) - prostaglandinsyntes
            "rs689466",   # PTGS2 - promotor
            # NF-kB pathway
            "rs28362491", # NFKB1 - master inflammationsregulator
            # NLRP3 inflammasom
            "rs35829419", # NLRP3 - inflammasomaktivering
        ]
    },

    # Detox fas I
    "detox_phase1": {
        "description": "Cytokrom P450 enzymer (fas I)",
        "snps": [
            "rs1048943",  # CYP1A1
            "rs762551",   # CYP1A2
            "rs1056836",  # CYP1B1
            "rs3892097",  # CYP2D6 *4
            "rs16947",    # CYP2D6 *2
            "rs1065852",  # CYP2D6 *10
            "rs28371706", # CYP2D6 *17
            "rs4244285",  # CYP2C19 *2
            "rs12248560", # CYP2C19 *17
            "rs1799853",  # CYP2C9 *2
            "rs1057910",  # CYP2C9 *3
            "rs2740574",  # CYP3A4
            "rs35599367", # CYP3A4 *22
            "rs776746",   # CYP3A5 *3
            "rs2031920",  # CYP2E1
        ]
    },

    # Detox fas II
    "detox_phase2": {
        "description": "Konjugeringsreaktioner (fas II)",
        "snps": [
            "rs1695",     # GSTP1
            "rs1138272",  # GSTP1
            "rs8175347",  # UGT1A1 *28
            "rs9282861",  # SULT1A1
            "rs1801280",  # NAT2
            "rs1799930",  # NAT2
            "rs662",      # PON1
            "rs854560",   # PON1
        ]
    },

    # Benhälsa
    "bone_health": {
        "description": "Benhälsa och kalciummetabolism",
        "snps": [
            "rs9340799",  # ESR1
            "rs2234693",  # ESR1
            "rs4988235",  # LCT (laktos)
        ]
    },

    # Blodtryck - RAAS och sympatiska nervsystemet
    "blood_pressure": {
        "description": "Blodtrycksreglering",
        "snps": [
            # RAAS-systemet (renin-angiotensin-aldosteron)
            "rs4340",     # ACE I/D - angiotensinkonverterande enzym
            "rs4343",     # ACE - kopplad till I/D
            "rs699",      # AGT M235T - angiotensinogen
            "rs5186",     # AGTR1 A1166C - angiotensin II-receptor
            "rs5182",     # AGTR1 - ytterligare variant
            "rs4961",     # ADD1 Gly460Trp - saltkänslighet
            # Sympatiska nervsystemet
            "rs1801253",  # ADRB1 Arg389Gly - beta-1 receptor
            "rs1801252",  # ADRB1 Ser49Gly - haplotyp
            "rs1042713",  # ADRB2 Arg16Gly - beta-2 receptor
            "rs1042714",  # ADRB2 Gln27Glu - haplotyp
            # Kväveoxid (vasodilatation)
            "rs1799983",  # NOS3 Glu298Asp - endotelial NO-syntas
            "rs2070744",  # NOS3 -786T>C - promotor
            # Natriuretiska peptider
            "rs5068",     # NPPA - ANP, natriures
            "rs198389",   # NPPB - BNP
            # CYP11B2 - aldosteronsyntes
            "rs1799998",  # CYP11B2 -344C>T - aldosteron
        ]
    },

    # Vikt/metabolism - Aptit, energibalans och fettlagring
    "obesity": {
        "description": "Viktreglering och metabolism",
        "snps": [
            # FTO - fat mass and obesity associated
            "rs9939609",  # FTO - starkaste obesitasgenen
            "rs1558902",  # FTO - oberoende signal
            "rs1121980",  # FTO - haplotyp
            # MC4R - melanokortinreceptor (mättnad)
            "rs17782313", # MC4R - aptitreglering
            "rs571312",   # MC4R - ytterligare variant
            # Leptin/leptinreceptor
            "rs7799039",  # LEP -2548G>A - leptinproduktion
            "rs1137101",  # LEPR Gln223Arg - leptinresistens
            # PPARG - fettcellsdifferentiering
            "rs1801282",  # PPARG Pro12Ala - insulinkänslighet
            # Adrenerga receptorer (termogenes)
            "rs1042713",  # ADRB2 Arg16Gly - lipolys
            "rs4994",     # ADRB3 Trp64Arg - brun fettaktivering
            # ADIPOQ - adiponektin
            "rs2241766",  # ADIPOQ - insulinkänslighet
            "rs1501299",  # ADIPOQ - fettvävsfunktion
            # TMEM18 - tidig obesitas
            "rs6548238",  # TMEM18 - BMI-association
            # BDNF - energibalans i hjärnan
            "rs6265",     # BDNF Val66Met - även aptitreglering
        ]
    },

    # Histamin - Nedbrytning och intolerans
    "histamine": {
        "description": "Histaminnedbrytning",
        "snps": [
            # HNMT - histamin-N-metyltransferas (intracellulär)
            "rs1049793",  # HNMT Thr105Ile - reducerad aktivitet
            "rs1049742",  # HNMT - ytterligare variant
            "rs11558538", # HNMT - enzymstabilitet
            # AOC1 (DAO) - diaminoxidas (extracellulär, tarm)
            "rs10156191", # AOC1 - huvudvariant för histaminintolerans
            "rs1049742",  # AOC1 - kopplad variant
            "rs2052129",  # AOC1 - promotor
            "rs2268999",  # AOC1 - enzymaktivitet
            # HDC - histidindekarboxylas (histaminsyntes)
            "rs2073440",  # HDC - histaminproduktion
            # HRH1-4 - histaminreceptorer
            "rs901865",   # HRH1 - receptor 1
            "rs2067474",  # HRH4 - immunreglering
        ]
    },

    # Blodsocker - Insulinsekretion och glukosmetabolism
    "blood_sugar": {
        "description": "Glukosmetabolism och insulinkänslighet",
        "snps": [
            # TCF7L2 - starkaste T2D-genen
            "rs7903146",  # TCF7L2 - betacellsfunktion
            "rs12255372", # TCF7L2 - kopplad variant
            # KCNJ11/ABCC8 - ATP-känslig K-kanal (insulinsekretion)
            "rs5219",     # KCNJ11 Glu23Lys - insulinfrisättning
            "rs5215",     # KCNJ11 - haplotyp
            "rs757110",   # ABCC8 - sulfonylurearespons
            # SLC30A8 - zinktransportör i betaceller
            "rs13266634", # SLC30A8 - insulinlagring
            # PPARG - insulinkänslighet
            "rs1801282",  # PPARG Pro12Ala - TZD-respons
            # IRS1 - insulinreceptorsubstrat
            "rs2943641",  # IRS1 - insulinsignalering
            # GCKR - glukokinas regulator
            "rs780094",   # GCKR - fasteglukosnivåer
            "rs1260326",  # GCKR Pro446Leu - kopplad
            # MTNR1B - melatonin och insulinsekretion
            "rs10830963", # MTNR1B - nattlig glukos
            # G6PC2 - glukos-6-fosfatas
            "rs560887",   # G6PC2 - fasteglukosnivåer
            # ADCY5 - cAMP-signalering
            "rs11708067", # ADCY5 - insulinsekretion
        ]
    },

    # Sköldkörtel - Hormonsyntes, aktivering och signalering
    "thyroid": {
        "description": "Sköldkörtelfunktion",
        "snps": [
            # Dejodinas - T4→T3 konvertering
            "rs225014",   # DIO2 Thr92Ala - lokal T3-aktivering
            "rs12885300", # DIO2 - ytterligare variant
            "rs2235544",  # DIO1 - perifer konvertering
            "rs11206244", # DIO1 - T3-nivåer
            # TSHR - TSH-receptor
            "rs1991517",  # TSHR - receptorfunktion
            "rs179247",   # TSHR - Graves sjukdom
            # TPO - tyreoperoxidas (hormonsyntes)
            "rs2071403",  # TPO - antikroppsrisk
            # TG - tyreoglobulin
            "rs2076740",  # TG - hormonproduktion
            # FOXE1 - sköldkörtelutveckling
            "rs965513",   # FOXE1 - sköldkörtelcancer/funktion
            # PDE8B - cAMP-nedbrytning
            "rs4704397",  # PDE8B - TSH-nivåer
            # SLC16A2 - T3-transport in i celler
            "rs17606253", # SLC16A2 - hormonupptag
        ]
    },

    # Muskler - Fibertyp, styrka och uthållighet
    "muscle": {
        "description": "Muskelfunktion och prestation",
        "snps": [
            # ACTN3 - alfa-aktinin-3 (snabba muskelfibrer)
            "rs1815739",  # ACTN3 R577X - sprint vs uthållighet
            # ACE - angiotensinkonverterande enzym
            "rs4340",     # ACE I/D - uthållighet (I) vs styrka (D)
            # PPARGC1A - mitokondriell biogenes
            "rs8192678",  # PPARGC1A Gly482Ser - uthållighetskapacitet
            # VEGFA - angiogenes
            "rs2010963",  # VEGFA - kapillärtäthet
            # CNTF - ciliary neurotrophic factor
            "rs1800169",  # CNTF - muskelmassa
            # MSTN - myostatin (muskeltillväxthämmare)
            "rs1805086",  # MSTN - muskelmassa
            # IGF1 - insulinlik tillväxtfaktor
            "rs35767",    # IGF1 - muskeltillväxt
            # COL5A1 - kollagen (senor/ligament)
            "rs12722",    # COL5A1 - skaderisk
            # AMPD1 - adenosinmonofosfatdeaminas
            "rs17602729", # AMPD1 - muskeluthållighet
            # NRF1 - mitokondriefunktion
            "rs6949152",  # NRF1 - aerob kapacitet
        ]
    },

    # Immunsystem - Immunförsvar och autoimmunitet
    "immune": {
        "description": "Immunfunktion",
        "snps": [
            # Interferonsystemet
            "rs12979860", # IFNL3 (IL28B) - virusförsvar
            "rs8099917",  # IFNL3 - hepatit C-respons
            # HLA-systemet (vävnadstyp)
            "rs2395029",  # HLA-B*57:01 tag - läkemedelsreaktion
            # Toll-like receptorer (medfött immunförsvar)
            "rs4986790",  # TLR4 Asp299Gly - bakterierespons
            "rs4986791",  # TLR4 Thr399Ile - haplotyp
            "rs5743708",  # TLR2 - gram-positiva bakterier
            # Vitamin D och immunitet
            "rs2228570",  # VDR FokI - antimikrobiella peptider
            # Komplementsystemet
            "rs2230199",  # C3 - komplementaktivering
            # MBL2 - mannos-bindande lektin
            "rs1800450",  # MBL2 - opsonisering
            "rs5030737",  # MBL2 - strukturell variant
            # CTLA4 - T-cellsreglering
            "rs3087243",  # CTLA4 - autoimmunitet
            # IL-17 pathway
            "rs2275913",  # IL17A - Th17-respons
            # PTPN22 - T-cellsaktivering
            "rs2476601",  # PTPN22 - autoimmunrisk
        ]
    },

    # Hud - Pigmentering, solkänslighet och åldrande
    "skin": {
        "description": "Hudhälsa och solkänslighet",
        "snps": [
            # MC1R - melanokortinreceptor (rödhårighet/fräknar)
            "rs1805007",  # MC1R R151C - stark rödhårsvariant
            "rs1805008",  # MC1R R160W - rödhårighet
            "rs1805009",  # MC1R D294H - rödhårighet
            "rs2228479",  # MC1R V92M - mildare variant
            # TYR - tyrosinas (melaninsyntes)
            "rs1126809",  # TYR Arg402Gln - pigmentering
            "rs1042602",  # TYR Ser192Tyr - hudton
            # OCA2/HERC2 - ögon/hudfärg
            "rs12913832", # HERC2 - blå/bruna ögon
            "rs1800407",  # OCA2 - pigmentering
            # SLC45A2 - melanosomtransport
            "rs16891982", # SLC45A2 - ljus hudton
            # IRF4 - fräknar och solkänslighet
            "rs12203592", # IRF4 - fräknar, melanom
            # ASIP - agouti signaling protein
            "rs4911414",  # ASIP - pigmentfördelning
            # MMP1 - kollagennedbrytning (åldrande)
            "rs1799750",  # MMP1 - rynkbildning
            # Antioxidantförsvar i hud
            "rs4880",     # SOD2 - UV-skydd
        ]
    },

    # Kardiovaskulär - Lipider, koagulation och kärlhälsa
    "cardiovascular": {
        "description": "Hjärt-kärlhälsa och lipidmetabolism",
        "snps": [
            # APOE - lipoproteinmetabolism
            "rs429358",   # APOE e4 - LDL, Alzheimer
            "rs7412",     # APOE e2 - lipidprofil
            # LDL-metabolism
            "rs688",      # LDLR - LDL-receptorfunktion
            "rs5925",     # LDLR - kolesterolupptag
            "rs505151",   # PCSK9 - LDL-receptornedbrytning
            # HDL-metabolism
            "rs708272",   # CETP TaqIB - HDL-nivåer
            "rs1800588",  # LIPC -514C>T - HDL
            "rs1800775",  # CETP -629C>A - HDL
            # Triglycerider
            "rs662799",   # APOA5 -1131T>C - triglycerider
            "rs328",      # LPL Ser447Stop - lipasaktivitet
            "rs1260326",  # GCKR - triglycerider
            # Lp(a) - oberoende riskfaktor
            "rs10455872", # LPA - Lp(a)-nivåer
            "rs3798220",  # LPA - hög Lp(a)
            # Koagulation
            "rs6025",     # F5 Leiden - trombosrisk
            "rs1799963",  # F2 G20210A - protrombinmutation
            "rs1801133",  # MTHFR - homocystein (kärlskada)
            # Warfarin/antikoagulation
            "rs9923231",  # VKORC1 - warfarindos
            "rs4149056",  # SLCO1B1 - statinbiverkningar
            # Endotelfunktion
            "rs1799983",  # NOS3 - kväveoxidproduktion
            # Homocystein
            "rs1801133",  # MTHFR C677T - homocysteinnivåer
        ]
    },

    # Farmakogenomik - extrar
    "pharmacogenomics": {
        "description": "Läkemedelsmetabolism",
        "snps": [
            "rs2395029",  # HLA-B*57:01 tag
            "rs3918290",  # DPYD *2A
            "rs55886062", # DPYD
            "rs67376798", # DPYD
            "rs12777823", # CYP2C8
        ]
    },

    # BH4-cykel - Tetrahydrobiopterin (kofaktor för neurotransmittorer)
    "bh4_cycle": {
        "description": "Tetrahydrobiopterin-cykel",
        "snps": [
            # GCH1 - GTP-cyklohydrolas (rate-limiting)
            "rs998259",   # GCH1 - BH4-syntes
            "rs841",      # GCH1 - smärtkänslighet
            "rs3783641",  # GCH1 - dopaminsyntes
            # SPR - sepiapterinreduktas
            "rs11248056", # SPR - BH4-syntes
            # QDPR - dihydropteridinreduktas (BH4-recycling)
            "rs2237030",  # QDPR - BH4-regenerering
            # PTS - 6-pyruvoyltetrahydropterinsyntetas
            "rs2859380",  # PTS - BH4-biosyntes
            # PCBD1 - pterin-4a-karbinolamindehydratas
            "rs61753730", # PCBD1 - BH4-recycling
            # DHFR - dihydrofolatreduktas (koppling till folat)
            "rs70991108", # DHFR - interagerar med BH4-cykel
            # NOS3 - kväveoxidsyntas (BH4-beroende)
            "rs1799983",  # NOS3 - BH4 som kofaktor
        ]
    },

    # =========================================================================
    # NYA KATEGORIER - Nutrigenomics, Longevity, Vitaminer, Mineraler
    # =========================================================================

    # Vitamin A / Betakaroten - BCMO1 konvertering
    "vitamin_a": {
        "description": "Vitamin A och betakaroten-metabolism",
        "snps": [
            # BCMO1 - betakaroten→retinol konvertering (central!)
            "rs7501331",  # BCMO1 - 32% reducerad konvertering vid T-allel
            "rs12934922", # BCMO1 - 69% reducerad konvertering vid AT/TT
            "rs11645428", # BCMO1 - ytterligare variant
            # BCO2 - asymmetrisk klyvning av karotenoider
            "rs2250417",  # BCO2 - karotenoidmetabolism
            # RBP4 - retinolbindande protein (transport)
            "rs3758539",  # RBP4 - vitamin A-transport
            # TTR - transtyretin (retinoltransport)
            "rs1800458",  # TTR - retinolbindning
            # LRAT - lecitin-retinol acyltransferas (lagring)
            "rs2071304",  # LRAT - vitamin A-lagring i lever
        ]
    },

    # Vitamin E - Tokoferol metabolism
    "vitamin_e": {
        "description": "Vitamin E-metabolism och antioxidantfunktion",
        "snps": [
            # TTPA - alfa-tokoferol transferprotein
            "rs6994076",  # TTPA - vitamin E-transport
            # CYP4F2 - vitamin E-katabolism
            "rs2108622",  # CYP4F2 - påverkar vitamin E-nivåer
            # APOA5 - lipidmetabolism (vitamin E är fettlösligt)
            "rs662799",   # APOA5 - påverkar vitamin E-absorption
            # SR-B1 (SCARB1) - vitamin E-upptag
            "rs5888",     # SCARB1 - HDL och vitamin E-transport
            # APOE - påverkar vitamin E-behov
            "rs429358",   # APOE e4 - högre vitamin E-behov
        ]
    },

    # Vitamin C - Askorbinsyra metabolism
    "vitamin_c": {
        "description": "Vitamin C-metabolism och transport",
        "snps": [
            # SLC23A1 - vitamin C-transportör (SVCT1)
            "rs33972313", # SLC23A1 - tarmabsorption
            "rs6596473",  # SLC23A1 - plasmanivåer
            # SLC23A2 - vitamin C-transportör (SVCT2)
            "rs1776948",  # SLC23A2 - vävnadsupptag
            "rs6053005",  # SLC23A2 - vitamin C-nivåer
            # GSTT1/GSTM1 - oxidativ stress (vitamin C-behov)
            "rs366631",   # GSTT1 - null genotyp ökar C-behov
            # HP - haptoglobin (vitamin C-interaktion)
            "rs2000999",  # HP - påverkar vitamin C-effekt
        ]
    },

    # Vitamin B1 (Tiamin)
    "vitamin_b1": {
        "description": "Tiamin-metabolism och transport",
        "snps": [
            # SLC19A2 - tiamintransportör (THTR1)
            "rs6656822",  # SLC19A2 - tiaminupptag
            # SLC19A3 - tiamintransportör (THTR2)
            "rs13007017", # SLC19A3 - hjärntransport
            # TPK1 - tiaminpyrofosfokinas
            "rs10513762", # TPK1 - tiamin→TPP aktivering
            # SLC25A19 - mitokondriell tiamintransport
            "rs2236225",  # SLC25A19 - mitokondriefunktion
        ]
    },

    # Vitamin B2 (Riboflavin) - Viktig för MTHFR!
    "vitamin_b2": {
        "description": "Riboflavin-metabolism (MTHFR-kofaktor)",
        "snps": [
            # SLC52A1 - riboflavintransportör (RFT1)
            "rs3746804",  # SLC52A1 - riboflavinupptag
            # SLC52A2 - riboflavintransportör (RFT2)
            "rs1060503",  # SLC52A2 - plasmanivåer
            # SLC52A3 - riboflavintransportör (RFT3)
            "rs2280546",  # SLC52A3 - tarmabsorption
            # MTHFR - riboflavin är kofaktor!
            "rs1801133",  # MTHFR C677T - riboflavin förbättrar funktion vid TT
            # FMO3 - flavinberoende enzym
            "rs2266782",  # FMO3 - riboflavinberoende
        ]
    },

    # Vitamin B6 (Pyridoxin/P5P)
    "vitamin_b6": {
        "description": "Vitamin B6-metabolism och aktivering",
        "snps": [
            # ALPL - alkaliskt fosfatas (P5P-aktivering)
            "rs4654748",  # ALPL - B6-aktivering till P5P
            "rs1256335",  # ALPL - plasmanivåer
            # NBPF3 - B6-metabolism
            "rs4654749",  # NBPF3 - B6-status
            # PDXK - pyridoxalkinas
            "rs2839185",  # PDXK - B6-fosforylering
            # AOX1 - aldehydoxidas (B6-katabolism)
            "rs55754655", # AOX1 - B6-nedbrytning
        ]
    },

    # Cholin och Fosfatidylkolin
    "choline": {
        "description": "Kolin-metabolism och fosfatidylkolin",
        "snps": [
            # PEMT - fosfatidyletanolamin N-metyltransferas
            "rs12325817", # PEMT - endogen kolinsyntes (kvinnor!)
            "rs7946",     # PEMT - kolinbehov
            "rs4646343",  # PEMT - leversteatos-risk
            # CHDH - kolindehydrogenas
            "rs9001",     # CHDH - kolinoxidation
            "rs12676",    # CHDH - betainproduktion
            # SLC44A1 - kolintransportör
            "rs7873937",  # SLC44A1 - kolinupptag
            # BHMT - betain-homocystein metyltransferas
            "rs3733890",  # BHMT - kolin→betain→metionin
            # MTHFD1 - folatcykel (kolininteraktion)
            "rs2236225",  # MTHFD1 - ökar kolinbehov
        ]
    },

    # Glutathion - Master antioxidant
    "glutathione": {
        "description": "Glutationsyntes och -metabolism",
        "snps": [
            # GCLC - glutamat-cystein ligas (rate-limiting)
            "rs17883901", # GCLC - glutationsyntes
            "rs12524494", # GCLC - promotorvariant
            # GCLM - glutamat-cystein ligas modifier
            "rs3170633",  # GCLM - glutationproduktion
            "rs41303970", # GCLM - oxidativ stress-respons
            # GSS - glutationsyntas
            "rs3761144",  # GSS - slutsteg i syntes
            # GSR - glutationreduktas (recycling)
            "rs2551715",  # GSR - GSSG→GSH regenerering
            # GPX1 - glutationperoxidas 1
            "rs1050450",  # GPX1 Pro198Leu - selenoenzym
            # GPX4 - fosfolipid-hydroperoxidas
            "rs713041",   # GPX4 - membranantioxidant
            # GSTP1 - glutation S-transferas Pi
            "rs1695",     # GSTP1 Ile105Val - detox
            "rs1138272",  # GSTP1 Ala114Val
            # GSTM1 - glutation S-transferas Mu (deletion)
            "rs366631",   # GSTM1 null - detoxkapacitet
            # GSTT1 - glutation S-transferas Theta (deletion)
            "rs17856199", # GSTT1 - detoxkapacitet
        ]
    },

    # Kollagen och bindväv
    "collagen": {
        "description": "Kollagensyntes och bindvävshälsa",
        "snps": [
            # COL1A1 - kollagen typ I alfa 1
            "rs1800012",  # COL1A1 Sp1 - benmineraldensitet, skaderisk
            "rs2249492",  # COL1A1 - osteoporosrisk
            # COL5A1 - kollagen typ V alfa 1
            "rs12722",    # COL5A1 - senor/ligament, skaderisk
            "rs3196378",  # COL5A1 - Akilles-skaderisk
            # COL1A2 - kollagen typ I alfa 2
            "rs42524",    # COL1A2 - benhälsa
            # COL2A1 - kollagen typ II (brosk)
            "rs2276454",  # COL2A1 - artros
            # COL3A1 - kollagen typ III (hud, kärl)
            "rs1800255",  # COL3A1 - kärlväggsstyrka
            # MMP1 - matrixmetalloproteas 1 (kollagennedbrytning)
            "rs1799750",  # MMP1 - rynkbildning, hudåldrande
            # MMP3 - matrixmetalloproteas 3
            "rs3025058",  # MMP3 - diskdegeneration
            # TIMP1 - MMP-inhibitor
            "rs4898",     # TIMP1 - balanserar kollagennedbrytning
        ]
    },

    # Tarmhälsa och mikrobiom
    "gut_health": {
        "description": "Tarmhälsa, permeabilitet och mikrobiom",
        "snps": [
            # FUT2 - sekretorstatus (tarmflora!)
            "rs601338",   # FUT2 - non-secretor, B12-absorption, mikrobiom
            "rs602662",   # FUT2 - kopplad variant
            # LCT - laktas (laktosintolerans)
            "rs4988235",  # LCT - laktospersistens
            "rs182549",   # LCT - europeisk variant
            # MCM6 - reglerar LCT
            "rs4988235",  # MCM6/LCT - laktosintolerans
            # HLA-DQ2/DQ8 - celiaki
            "rs2187668",  # HLA-DQ2.5 - celiaki-risk
            "rs7454108",  # HLA-DQ8 - celiaki-risk
            # NOD2 - Crohns sjukdom, tarmimmunitet
            "rs2066844",  # NOD2 R702W - IBD-risk
            "rs2066845",  # NOD2 G908R - IBD-risk
            "rs2066847",  # NOD2 1007fs - IBD-risk
            # ATG16L1 - autofagi (tarmbarriär)
            "rs2241880",  # ATG16L1 - Crohns, tarmpermeabilitet
            # IL23R - tarmimmunitet
            "rs11209026", # IL23R - IBD-skydd
            # MUC2 - mucinproduktion (tarmbarriär)
            "rs11825977", # MUC2 - slemhinneintegritet
        ]
    },

    # Longevity och åldrande
    "longevity": {
        "description": "Longevity-gener och hälsosamt åldrande",
        "snps": [
            # FOXO3 - forkhead box O3 (starkaste longevity-genen)
            "rs2802292",  # FOXO3 - 100-åringar, insulinsignalering
            "rs2764264",  # FOXO3 - ytterligare variant
            # APOE - apolipoprotein E
            "rs429358",   # APOE e4 - Alzheimer, hjärt-kärl
            "rs7412",     # APOE e2 - skyddande
            # TERT - telomeras (telomerlängd)
            "rs2736100",  # TERT - telomerlängd
            "rs2853669",  # TERT - telomerasaktivitet
            # TERC - telomeras RNA-komponent
            "rs12696304", # TERC - telomerlängd
            # SIRT1 - sirtuin 1 (kalorierestriktion)
            "rs7895833",  # SIRT1 - metabolisk hälsa
            "rs3758391",  # SIRT1 - longevity
            # SIRT3 - mitokondriell sirtuin
            "rs11555236", # SIRT3 - mitokondriefunktion
            # KLOTHO - anti-aging hormon
            "rs9536314",  # KLOTHO KL-VS - kognitiv funktion
            "rs9527025",  # KLOTHO - njurfunktion
            # CETP - kolesterylester transferprotein
            "rs5882",     # CETP - HDL, longevity
            # IGF1R - insulinlik tillväxtfaktor receptor
            "rs2229765",  # IGF1R - longevity pathway
            # MTOR-pathway
            "rs1130214",  # AKT1 - mTOR-signalering
        ]
    },

    # Alkohol och acetaldehyd-metabolism
    "alcohol_metabolism": {
        "description": "Alkohol- och acetaldehydmetabolism",
        "snps": [
            # ADH1B - alkoholdehydrogenas 1B
            "rs1229984",  # ADH1B His48Arg - snabb alkoholmetabolism
            "rs2066702",  # ADH1B - afrikansk variant
            # ADH1C - alkoholdehydrogenas 1C
            "rs698",      # ADH1C Ile350Val - metabolismhastighet
            # ALDH2 - aldehyddehydrogenas 2
            "rs671",      # ALDH2 Glu504Lys - "Asian flush", acetaldehydansamling
            # CYP2E1 - cytokrom P450 2E1
            "rs2031920",  # CYP2E1 - alkoholinducerbar
            "rs6413432",  # CYP2E1 - leverskaderisk
            # GSTM1 - glutationtransferas (acetaldehyddetox)
            "rs366631",   # GSTM1 null - ökad känslighet
        ]
    },

    # Kognitiv funktion och hjärnhälsa
    "cognitive": {
        "description": "Kognitiv funktion, minne och neuroprotektion",
        "snps": [
            # APOE - Alzheimer-risk
            "rs429358",   # APOE e4 - Alzheimer, behöver mer DHA
            "rs7412",     # APOE e2 - skyddande
            # BDNF - brain-derived neurotrophic factor
            "rs6265",     # BDNF Val66Met - neuroplasticitet
            "rs7124442",  # BDNF - expression
            # KIBRA (WWC1) - episodiskt minne
            "rs17070145", # KIBRA - minneskapacitet
            # COMT - dopaminmetabolism
            "rs4680",     # COMT Val158Met - arbetsminne
            # DRD2 - dopaminreceptor
            "rs1800497",  # DRD2/ANKK1 - inlärning, belöning
            # CHRNA4 - nikotinreceptor (uppmärksamhet)
            "rs1044396",  # CHRNA4 - uppmärksamhet
            # NCAN - neurocan (synaptisk plasticitet)
            "rs1064395",  # NCAN - bipolär, kognition
            # CLU - clusterin (Alzheimer-skydd)
            "rs11136000", # CLU - Alzheimer-risk
            # PICALM - fosfatidylinositolbindning
            "rs3851179",  # PICALM - Alzheimer-risk
            # CR1 - komplementreceptor 1
            "rs6656401",  # CR1 - Alzheimer-risk
            # TOMM40 - mitokondriell import
            "rs2075650",  # TOMM40 - kognitiv nedgång
        ]
    },

    # Ögonhälsa och syn
    "eye_health": {
        "description": "Ögonhälsa, makuladegeneration och syn",
        "snps": [
            # CFH - komplementfaktor H (AMD)
            "rs1061170",  # CFH Y402H - AMD-risk
            "rs800292",   # CFH - AMD
            # ARMS2/HTRA1 - AMD
            "rs10490924", # ARMS2 - AMD-risk
            "rs11200638", # HTRA1 - AMD
            # C3 - komplement C3
            "rs2230199",  # C3 - AMD-risk
            # CFB - komplementfaktor B
            "rs641153",   # CFB - AMD-skydd
            # BCMO1 - betakaroten→retinol (näthinnan)
            "rs7501331",  # BCMO1 - makulapigment
            # SCARB1 - lutein/zeaxantinupptag
            "rs5888",     # SCARB1 - makulapigmenttäthet
            # GSTP1 - oxidativ stress i ögat
            "rs1695",     # GSTP1 - kataraktrisk
        ]
    },

    # Magnesium-metabolism
    "magnesium": {
        "description": "Magnesiumhomeostas och transport",
        "snps": [
            # TRPM6 - magnesiumkanal (tarm/njure)
            "rs2274924",  # TRPM6 - magnesiumabsorption
            "rs3750425",  # TRPM6 - hypomagnesemi-risk
            # TRPM7 - magnesiumkanal
            "rs8042919",  # TRPM7 - intracellulär Mg
            # CNNM2 - magnesiumtransportör
            "rs7914558",  # CNNM2 - serummagnesium
            # MUC1 - magnesiumreglering
            "rs4072037",  # MUC1 - magnesiumstatus
            # SHROOM3 - njurmagnesiumhantering
            "rs17216707", # SHROOM3 - magnesiumutsöndring
            # ATP2B1 - kalcium/magnesium-ATPas
            "rs2681472",  # ATP2B1 - blodtryck, Mg-beroende
        ]
    },

    # Zink-metabolism
    "zinc": {
        "description": "Zinkmetabolism och homeostas",
        "snps": [
            # SLC30A8 - zinktransportör (betaceller)
            "rs13266634", # SLC30A8 - T2D, insulinsekretion
            # SLC39A4 (ZIP4) - zinkabsorption
            "rs1871534",  # SLC39A4 - zinkupptag
            # SLC39A8 (ZIP8) - zinktransport
            "rs13107325", # SLC39A8 - zink, mangan, kadmium
            # MT1A/MT2A - metallotionein (zinklagring)
            "rs8052394",  # MT1A - zinkbuffring
            "rs10636",    # MT2A - zinkstatus
            # CA1 - karbanhydras (zinkenzym)
            "rs1532423",  # CA1 - zinkberoende enzym
        ]
    },

    # Koppar-metabolism
    "copper": {
        "description": "Kopparmetabolism och homeostas",
        "snps": [
            # ATP7A - koppartransport (Menkes)
            "rs2227291",  # ATP7A - kopparabsorption
            # ATP7B - kopparutsöndring (Wilsons)
            "rs732774",   # ATP7B - kopparexkretion
            "rs1801243",  # ATP7B - kopparstatus
            # CP - ceruloplasmin (koppartransport)
            "rs701753",   # CP - serumkoppar
            # SOD1 - superoxiddismutas (kopparenzym)
            "rs2070424",  # SOD1 - koppar/zink-SOD
            # ATOX1 - koppar-chaperon
            "rs73598374", # ATOX1 - intracellulär koppar
        ]
    },

    # Mangan-metabolism
    "manganese": {
        "description": "Manganmetabolism och transport",
        "snps": [
            # SLC39A8 - mangan/zinktransportör
            "rs13107325", # SLC39A8 - manganupptag
            # SLC30A10 - manganexportör
            "rs1776029",  # SLC30A10 - manganhomeostas
            # SOD2 - mangan-superoxiddismutas
            "rs4880",     # SOD2 Ala16Val - manganenzym
            # PARK2 - parkin (manganrelaterad neurodegeneration)
            "rs9356058",  # PARK2 - mangantoxicitet
        ]
    },

    # Jod och sköldkörtel (utökning)
    "iodine": {
        "description": "Jodmetabolism och sköldkörtelfunktion",
        "snps": [
            # SLC5A5 (NIS) - natriumjodsymportör
            "rs7250346",  # SLC5A5 - jodupptag i sköldkörtel
            # TPO - tyreoperoxidas
            "rs2071403",  # TPO - jodorganifiering
            # TG - tyreoglobulin
            "rs2076740",  # TG - jodlagring
            # DIO1 - dejodinas 1
            "rs2235544",  # DIO1 - T4→T3
            # DIO2 - dejodinas 2
            "rs225014",   # DIO2 Thr92Ala - lokal T3
            # TSHR - TSH-receptor
            "rs1991517",  # TSHR - TSH-känslighet
            # FOXE1 - sköldkörtelutveckling
            "rs965513",   # FOXE1 - sköldkörtelfunktion
        ]
    },

    # Kreatinmetabolism
    "creatine": {
        "description": "Kreatinsyntes och transport",
        "snps": [
            # GAMT - guanidinoacetat N-metyltransferas
            "rs17851582", # GAMT - kreatinsyntes
            # GATM (AGAT) - arginin-glycin amidinotransferas
            "rs1049503",  # GATM - kreatinsyntes steg 1
            # SLC6A8 - kreatintransportör
            "rs5934442",  # SLC6A8 - kreatinupptag i muskel
            # CKM - kreatinkinas (muskel)
            "rs8111989",  # CKM - ATP-regenerering
        ]
    },

    # Karnitin-metabolism
    "carnitine": {
        "description": "Karnitinsyntes och fettsyratransport",
        "snps": [
            # SLC22A5 (OCTN2) - karnitintransportör
            "rs2631367",  # SLC22A5 - karnitinupptag
            "rs274558",   # SLC22A5 - primär karnitinbrist
            # CPT1A - karnitinpalmitoyltransferas 1A
            "rs80356779", # CPT1A - fettsyratransport till mitokondrier
            # CPT2 - karnitinpalmitoyltransferas 2
            "rs1799821",  # CPT2 - mitokondriell fettsyraoxidation
            # BBOX1 - gamma-butyrobetainhydroxylas
            "rs12356193", # BBOX1 - karnitinsyntes
            # TMLHE - trimetyllysindioxygenase
            "rs17147454", # TMLHE - karnitinbiosyntes
        ]
    },

    # Taurin-metabolism
    "taurine": {
        "description": "Taurinsyntes och transport",
        "snps": [
            # CSAD - cysteinsufinat dekarboxylas
            "rs7571842",  # CSAD - taurinsyntes
            # CDO1 - cysteindioxygenase
            "rs34623097", # CDO1 - cystein→taurin
            # SLC6A6 - taurintransportör
            "rs2013162",  # SLC6A6 - taurinupptag
            # CBS - cystationin beta-syntas (cysteinkälla)
            "rs234706",   # CBS - taurinprekursor
        ]
    },

    # Urea-cykel och ammoniakmetabolism
    "urea_cycle": {
        "description": "Ureacykel och kvävebalans",
        "snps": [
            # CPS1 - karbamoylfosfatsyntas 1
            "rs1047891",  # CPS1 - ureacykelkapacitet
            "rs7422339",  # CPS1 - ammoniakhantering
            # OTC - ornitintranskarbamylas
            "rs5963409",  # OTC - ureacykel
            # ASS1 - argininosuccinatsyntas
            "rs2297518",  # ASS1 - citrullin→arginin
            # ARG1 - arginas 1
            "rs2781666",  # ARG1 - arginin→urea
            # NOS1 - neuronal kväveoxidsyntas
            "rs2682826",  # NOS1 - NO-produktion
        ]
    },

    # Purin/Urat-metabolism (gikt)
    "uric_acid": {
        "description": "Urinsyrametabolism och gikt",
        "snps": [
            # SLC2A9 (GLUT9) - urattransportör
            "rs734553",   # SLC2A9 - urinsyranivåer
            "rs12498742", # SLC2A9 - giktrisk
            # ABCG2 - urattransportör
            "rs2231142",  # ABCG2 Q141K - giktrisk
            # SLC22A12 (URAT1) - urattransportör
            "rs505802",   # SLC22A12 - uratreabsorption
            # SLC17A1 - urattransportör
            "rs1165196",  # SLC17A1 - urinsyra
            # XDH - xantinoxidas (urinsyraproduktion)
            "rs206860",   # XDH - purin→urinsyra
        ]
    },

    # Oxalatmetabolism (njursten)
    "oxalate": {
        "description": "Oxalatmetabolism och njurstensrisk",
        "snps": [
            # AGXT - alanin-glyoxylataminotransferas
            "rs34116584", # AGXT - primär hyperoxaluri
            # GRHPR - glyoxylatreduktas
            "rs11545034", # GRHPR - oxalatmetabolism
            # SLC26A6 - oxalattransportör
            "rs2310996",  # SLC26A6 - tarmoxalatsekretion
            # CLDN14 - claudin 14 (njursten)
            "rs219780",   # CLDN14 - kalciumnjursten
            # VDR - vitamin D-receptor (kalciumoxalatsten)
            "rs2228570",  # VDR FokI - njurstensrisk
        ]
    },

    # Saltbalans och elektrolyter
    "electrolytes": {
        "description": "Elektrolytbalans och salthantering",
        "snps": [
            # ADD1 - adducin (saltkänslighet)
            "rs4961",     # ADD1 Gly460Trp - saltkänsligt blodtryck
            # WNK1 - kinas (elektrolytbalans)
            "rs765250",   # WNK1 - blodtryck
            # SCNN1A - natriumkanal (ENaC)
            "rs2228576",  # SCNN1A - natriumreabsorption
            # KCNJ1 (ROMK) - kaliumkanal
            "rs2186832",  # KCNJ1 - kaliumutsöndring
            # SLC12A3 - natriumkloridkotransportör
            "rs11643718", # SLC12A3 - Gitelmans syndrom
            # CLCNKB - kloridkanal
            "rs12140311", # CLCNKB - elektrolytbalans
        ]
    },

    # Aptit och mättnad
    "appetite": {
        "description": "Aptitreglering och mättnadssignaler",
        "snps": [
            # FTO - fat mass and obesity
            "rs9939609",  # FTO - aptit, mättnad
            # MC4R - melanokortinreceptor
            "rs17782313", # MC4R - mättnadssignal
            # LEP - leptin
            "rs7799039",  # LEP - leptinproduktion
            # LEPR - leptinreceptor
            "rs1137101",  # LEPR - leptinkänslighet
            # GHRL - ghrelin (hungersignal)
            "rs696217",   # GHRL - ghrelinnivåer
            # GHSR - ghrelinreceptor
            "rs2232165",  # GHSR - hungerrespons
            # NPY - neuropeptid Y (aptitstimulerande)
            "rs16147",    # NPY - aptit, stress-ätande
            # AGRP - agouti-related protein
            "rs5030980",  # AGRP - aptitstimulerande
            # POMC - proopiomelanocortin
            "rs1042571",  # POMC - mättnad
            # CARTPT - CART prepropeptid
            "rs2239670",  # CARTPT - aptithämning
        ]
    },

    # Smakuppfattning
    "taste": {
        "description": "Smakuppfattning och matpreferenser",
        "snps": [
            # TAS2R38 - bittersmak (PTC/PROP)
            "rs713598",   # TAS2R38 - bitterkänslighet
            "rs1726866",  # TAS2R38 - grönsaksaversion
            "rs10246939", # TAS2R38 - haplotyp
            # TAS1R2 - sötsmak
            "rs35874116", # TAS1R2 - sötsugning
            # TAS1R3 - sötsmak
            "rs307355",   # TAS1R3 - sötsmaksreceptor
            # OR6A2 - koriandersmak (tvål/soppa)
            "rs72921001", # OR6A2 - korianderaversion
            # CD36 - fettsmak
            "rs1761667",  # CD36 - fettkänslighet
            # TRPV1 - capsaicinreceptor (chili)
            "rs8065080",  # TRPV1 - chilikänslighet
        ]
    },

    # Matintoleranser (utöver laktos)
    "food_intolerance": {
        "description": "Matintoleranser och överkänslighet",
        "snps": [
            # LCT - laktos
            "rs4988235",  # LCT - laktosintolerans
            # HLA-DQ2/DQ8 - gluten/celiaki
            "rs2187668",  # HLA-DQ2.5 - celiaki
            "rs7454108",  # HLA-DQ8 - celiaki
            # FUT2 - fruktosmalabsorption
            "rs601338",   # FUT2 - tarmfunktion
            # ALDOB - fruktosintolerans
            "rs1800546",  # ALDOB - hereditär fruktosintolerans
            # SI - sukras-isomaltas (sackarosintolerans)
            "rs9290264",  # SI - sackarosintolerans
            # G6PD - favism (bönor)
            "rs1050828",  # G6PD - favism-risk
            # NAT2 - koffein/histamin
            "rs1801280",  # NAT2 - histaminnedbrytning
        ]
    },

    # Fasta och metabolisk flexibilitet
    "fasting": {
        "description": "Fasteförmåga och metabolisk flexibilitet",
        "snps": [
            # PPARGC1A - PGC-1alfa (mitokondrier, fasta)
            "rs8192678",  # PPARGC1A - metabolisk flexibilitet
            # SIRT1 - sirtuin (fasteadaptation)
            "rs7895833",  # SIRT1 - kalorierestriktion
            # FOXO3 - forkhead (fastefördelar)
            "rs2802292",  # FOXO3 - fastebenefits
            # PPARA - fettsyraoxidation
            "rs1800206",  # PPARA - fettförbränning vid fasta
            # CPT1A - fettsyratransport
            "rs80356779", # CPT1A - ketogenes
            # HMGCR - HMG-CoA reduktas
            "rs3846662",  # HMGCR - kolesterolsyntes vid fasta
            # ADIPOQ - adiponektin
            "rs2241766",  # ADIPOQ - insulinkänslighet
        ]
    },

    # Circadian/Kronobiologi (utökning av sleep)
    "circadian": {
        "description": "Dygnsrytm och kronobiologi",
        "snps": [
            # CLOCK - central klockgen
            "rs1801260",  # CLOCK 3111T/C
            "rs3749474",  # CLOCK - sömnlängd
            # PER1 - period 1
            "rs2735611",  # PER1 - morgon/kväll
            # PER2 - period 2
            "rs2304672",  # PER2 - fasförskjutning
            "rs934945",   # PER2 - kronotyp
            # PER3 - period 3
            "rs57875989", # PER3 VNTR
            "rs228697",   # PER3 - sömnbehov
            # CRY1 - kryptokrom 1
            "rs2287161",  # CRY1 - försenad sömnfas
            # CRY2 - kryptokrom 2
            "rs8192440",  # CRY2 - depression
            # ARNTL (BMAL1) - central klockgen
            "rs2278749",  # ARNTL - metabolisk rytm
            # NR1D1 (REV-ERB) - klockrepressor
            "rs2314339",  # NR1D1 - metabolisk rytm
            # NPAS2 - CLOCK-paralog
            "rs2305160",  # NPAS2 - cirkadisk
            # RORA - RAR-relaterad orphan receptor
            "rs12912233", # RORA - sömn, autism
        ]
    },

    # Smärtkänslighet
    "pain_sensitivity": {
        "description": "Smärtkänslighet och analgetisk respons",
        "snps": [
            # COMT - katekolaminmetabolism
            "rs4680",     # COMT Val158Met - smärtkänslighet
            # OPRM1 - opioidreceptor mu
            "rs1799971",  # OPRM1 A118G - opioidrespons
            # SCN9A - natriumkanal (smärtsignalering)
            "rs6746030",  # SCN9A - smärtkänslighet
            # GCH1 - BH4-syntes (smärtmodulering)
            "rs841",      # GCH1 - kronisk smärta
            # TRPV1 - capsaicinreceptor
            "rs8065080",  # TRPV1 - värmesmärta
            # ABCB1 - P-glykoprotein (opioidtransport)
            "rs1045642",  # ABCB1 - morfinrespons
            # FAAH - endocannabinoidnedbrytning
            "rs324420",   # FAAH - smärtmodulering
        ]
    },

    # Fertilitet (kvinnor)
    "fertility_female": {
        "description": "Kvinnlig fertilitet och reproduktion",
        "snps": [
            # FSHR - FSH-receptor
            "rs6166",     # FSHR - ovariell respons
            "rs6165",     # FSHR - IVF-respons
            # ESR1 - östrogenreceptor alfa
            "rs2234693",  # ESR1 PvuII - fertilitet
            "rs9340799",  # ESR1 XbaI - fertilitet
            # AMH - anti-Müllerskt hormon
            "rs10407022", # AMH - ovariell reserv
            # AMHR2 - AMH-receptor
            "rs2002555",  # AMHR2 - ovariell funktion
            # LHB - luteiniserande hormon
            "rs1800447",  # LHB - ovulation
            # MTHFR - folat (neural tube defects)
            "rs1801133",  # MTHFR - graviditetsutfall
            # COMT - östrogennedbrytning
            "rs4680",     # COMT - östrogenmetabolism
        ]
    },

    # Fertilitet (män)
    "fertility_male": {
        "description": "Manlig fertilitet och spermiefunktion",
        "snps": [
            # FSHR - FSH-receptor
            "rs6166",     # FSHR - spermatogenes
            # AR - androgenreceptor (CAG-repeat)
            "rs5919411",  # AR - testosteronkänslighet
            # SHBG - könshormonbindande globulin
            "rs6259",     # SHBG - fritt testosteron
            "rs1799941",  # SHBG - testosteronnivåer
            # CYP19A1 - aromatas
            "rs2414096",  # CYP19A1 - östrogen/testosteron-ratio
            # MTHFR - DNA-metylering i spermier
            "rs1801133",  # MTHFR - spermiekvalitet
            # GSTP1 - oxidativ stress i testiklar
            "rs1695",     # GSTP1 - spermieskydd
            # NOS3 - kväveoxid (erektil funktion)
            "rs1799983",  # NOS3 - blodflöde
        ]
    },

    # Hormonbalans
    "hormones": {
        "description": "Hormonproduktion och metabolism",
        "snps": [
            # CYP17A1 - steroidsyntes
            "rs743572",   # CYP17A1 - DHEA, testosteron
            # CYP19A1 - aromatas (testosteron→östrogen)
            "rs2414096",  # CYP19A1 - östrogenproduktion
            "rs10046",    # CYP19A1 - bröstcancerrisk
            # HSD17B1 - östradiolsyntes
            "rs605059",   # HSD17B1 - östrogennivåer
            # SRD5A2 - 5-alfa-reduktas (testosteron→DHT)
            "rs523349",   # SRD5A2 - DHT-produktion
            # SHBG - hormonbindning
            "rs6259",     # SHBG - fritt hormon
            # ESR1 - östrogenreceptor
            "rs2234693",  # ESR1 - östrogenkänslighet
            # ESR2 - östrogenreceptor beta
            "rs4986938",  # ESR2 - östrogensignalering
            # PGR - progesteronreceptor
            "rs1042838",  # PGR - progesteronrespons
            # AR - androgenreceptor
            "rs5919411",  # AR - androgenkänslighet
        ]
    },

    # Benmetabolism (utökning av bone_health)
    "bone_metabolism": {
        "description": "Benmetabolism och osteoporosrisk",
        "snps": [
            # VDR - vitamin D-receptor
            "rs2228570",  # VDR FokI - kalciumabsorption
            "rs1544410",  # VDR BsmI - benmineraldensitet
            # ESR1 - östrogenreceptor
            "rs2234693",  # ESR1 - benmassa
            "rs9340799",  # ESR1 - osteoporosrisk
            # COL1A1 - kollagen typ I
            "rs1800012",  # COL1A1 - frakturrisk
            # LRP5 - Wnt-signalering (benbildning)
            "rs3736228",  # LRP5 - benmassa
            "rs4988321",  # LRP5 - osteoporosrisk
            # SOST - sklerostin (benhämmare)
            "rs1513670",  # SOST - benmassa
            # RANKL (TNFSF11) - osteoklastaktivering
            "rs9594759",  # RANKL - bennedbrytning
            # OPG (TNFRSF11B) - osteoklasthämmare
            "rs2073618",  # OPG - benskydd
            # RUNX2 - osteoblastdifferentiering
            "rs1321075",  # RUNX2 - benbildning
            # SP7 (Osterix) - benbildning
            "rs2016266",  # SP7 - benmassa
        ]
    },

    # =========================================================================
    # YTTERLIGARE HÄLSOKATEGORIER - Komplett "Instruktionsbok"
    # =========================================================================

    # Allergi och atopi
    "allergy": {
        "description": "Allergi, atopi och överkänslighet",
        "snps": [
            # IL4 - interleukin 4 (Th2-respons)
            "rs2243250",  # IL4 -589C>T - IgE-produktion
            # IL4R - IL4-receptor
            "rs1805010",  # IL4R Ile50Val - atopi
            "rs1801275",  # IL4R Gln576Arg - astma
            # IL13 - interleukin 13
            "rs20541",    # IL13 Arg130Gln - astma, eksem
            "rs1800925",  # IL13 -1112C>T - IgE
            # FCER1A - IgE-receptor
            "rs2251746",  # FCER1A - IgE-nivåer
            # HLA-DRB1 - vävnadstyp (allergi)
            "rs6457617",  # HLA-DRB1 - pollenallergi
            # FLG - filaggrin (hudbarriär, eksem)
            "rs61816761", # FLG R501X - atopisk dermatit
            "rs558269137",# FLG 2282del4 - eksem
            # TSLP - thymic stromal lymphopoietin
            "rs1837253",  # TSLP - astma, allergi
            # IL33 - alarmin
            "rs1342326",  # IL33 - astma
            # STAT6 - signaltransduktion
            "rs324011",   # STAT6 - IgE, atopi
        ]
    },

    # Autoimmunitet
    "autoimmune": {
        "description": "Autoimmuna sjukdomar och immunreglering",
        "snps": [
            # HLA-DRB1 - vävnadstyp
            "rs6457617",  # HLA-DRB1 - RA, MS, T1D
            # PTPN22 - T-cellsaktivering
            "rs2476601",  # PTPN22 R620W - RA, T1D, lupus
            # CTLA4 - T-cellshämmare
            "rs3087243",  # CTLA4 - autoimmunitet
            "rs231775",   # CTLA4 +49A>G - Graves, T1D
            # IL2RA - IL2-receptor (Treg)
            "rs2104286",  # IL2RA - MS, T1D
            # STAT4 - signaltransduktion
            "rs7574865",  # STAT4 - lupus, RA
            # IRF5 - interferonreglering
            "rs2004640",  # IRF5 - lupus
            # TNFAIP3 (A20) - NF-kB-hämmare
            "rs2230926",  # TNFAIP3 - RA, lupus
            # IL23R - Th17-respons
            "rs11209026", # IL23R - IBD, psoriasis
            # TYK2 - JAK-signalering
            "rs34536443", # TYK2 - MS, psoriasis, IBD
            # BANK1 - B-cellsaktivering
            "rs10516487", # BANK1 - lupus
        ]
    },

    # Cancer-prevention och DNA-reparation
    "cancer_prevention": {
        "description": "DNA-reparation och cancerpreventiva gener",
        "snps": [
            # TP53 - tumörsuppressor
            "rs1042522",  # TP53 Arg72Pro - cancerrespons
            # BRCA-relaterade (ej BRCA1/2 själva - de är för komplexa)
            "rs16942",    # BRCA1-region - bröstcancer
            # CHEK2 - cellcykelkontroll
            "rs17879961", # CHEK2 I157T - bröstcancer
            # ATM - DNA-reparation
            "rs1801516",  # ATM D1853N - strålkänslighet
            # XRCC1 - basexcisionsreparation
            "rs25487",    # XRCC1 Arg399Gln - DNA-reparation
            "rs1799782",  # XRCC1 Arg194Trp
            # OGG1 - oxidativ DNA-skada
            "rs1052133",  # OGG1 Ser326Cys - oxidativ reparation
            # ERCC2 (XPD) - nukleotidexcisionsreparation
            "rs13181",    # ERCC2 Lys751Gln - DNA-reparation
            "rs1799793",  # ERCC2 Asp312Asn
            # MTHFR - DNA-metylering
            "rs1801133",  # MTHFR - folat, DNA-syntes
            # NAT2 - karcinogenmetabolism
            "rs1801280",  # NAT2 - acetylerarstatus
            # GSTP1 - karcinogendetox
            "rs1695",     # GSTP1 - detoxkapacitet
            # NQO1 - kinondetox
            "rs1800566",  # NQO1 - bensenmetabolism
            # EPHX1 - epoxidhydrolas
            "rs1051740",  # EPHX1 - PAH-metabolism
        ]
    },

    # Mitokondriefunktion och energi
    "mitochondria": {
        "description": "Mitokondriefunktion och cellulär energi",
        "snps": [
            # PPARGC1A (PGC-1α) - mitokondriell biogenes
            "rs8192678",  # PPARGC1A Gly482Ser - mitokondrier
            # TFAM - mitokondriell transkription
            "rs1937",     # TFAM - mtDNA-kopietal
            # NRF1 - mitokondriell biogenes
            "rs6949152",  # NRF1 - mitokondriefunktion
            # SIRT3 - mitokondriell sirtuin
            "rs11555236", # SIRT3 - mitokondriell metabolism
            # UCP2 - uncoupling protein 2
            "rs659366",   # UCP2 - energieffektivitet
            "rs660339",   # UCP2 Ala55Val
            # UCP3 - uncoupling protein 3
            "rs1800849",  # UCP3 - termogenes
            # SOD2 - mitokondriell antioxidant
            "rs4880",     # SOD2 Ala16Val - ROS-skydd
            # POLG - mtDNA-polymeras
            "rs2307441",  # POLG - mtDNA-replikation
            # MT-ND - NADH-dehydrogenas (mtDNA)
            "rs28357980", # MT-ND1 - komplex I
            # COQ2 - CoQ10-syntes
            "rs4693075",  # COQ2 - CoQ10-produktion
        ]
    },

    # Epigenetik och metylering (utökning)
    "epigenetics": {
        "description": "Epigenetisk reglering och DNA-metylering",
        "snps": [
            # DNMT1 - DNA-metyltransferas 1
            "rs2228611",  # DNMT1 - metyleringsunderhåll
            # DNMT3A - de novo metylering
            "rs1550117",  # DNMT3A - epigenetisk programmering
            # DNMT3B - de novo metylering
            "rs2424913",  # DNMT3B - metylering
            # TET2 - demetylering
            "rs2454206",  # TET2 - epigenetisk reglering
            # MTHFR - metyldonator
            "rs1801133",  # MTHFR C677T - SAM-produktion
            "rs1801131",  # MTHFR A1298C
            # MAT1A - metioninadenosyltransferas
            "rs2993763",  # MAT1A - SAM-syntes
            # AHCY - S-adenosylhomocysteinhydrolas
            "rs819147",   # AHCY - metyleringscykel
            # HDAC - histondeacetylas
            "rs1741981",  # HDAC9 - histonmodifiering
            # SIRT1 - histondeacetylering
            "rs7895833",  # SIRT1 - epigenetisk reglering
        ]
    },

    # Hudåldrande och hudtyp
    "skin_aging": {
        "description": "Hudåldrande, kollagen och UV-skydd",
        "snps": [
            # MMP1 - kollagenas
            "rs1799750",  # MMP1 - rynkbildning
            # MMP3 - stromelysin
            "rs3025058",  # MMP3 - hudelasticitet
            # COL1A1 - kollagen typ I
            "rs1800012",  # COL1A1 - hudtjocklek
            # ELN - elastin
            "rs2289360",  # ELN - hudelasticitet
            # SOD2 - antioxidant
            "rs4880",     # SOD2 - UV-skydd
            # CAT - katalas
            "rs1001179",  # CAT - oxidativ stress
            # GPX1 - glutationperoxidas
            "rs1050450",  # GPX1 - antioxidant
            # MC1R - pigmentering
            "rs1805007",  # MC1R - solkänslighet
            "rs1805008",  # MC1R - rödhårighet
            # STXBP5L - hudåldrande
            "rs322458",   # STXBP5L - perceived age
            # AGER - advanced glycation
            "rs2070600",  # AGER - AGE-receptor
        ]
    },

    # Hårhälsa
    "hair_health": {
        "description": "Hårtillväxt, hårförlust och pigmentering",
        "snps": [
            # AR - androgenreceptor (manligt håravfall)
            "rs6152",     # AR - androgen alopeci
            # EDA2R - ektodysplasinreceptor
            "rs1385699",  # EDA2R - manligt håravfall
            # HDAC9 - histondeacetylas
            "rs2240419",  # HDAC9 - håravfall
            # WNT10A - Wnt-signalering
            "rs121908120",# WNT10A - hårfollikel
            # IRF4 - hårfärg
            "rs12203592", # IRF4 - hårpigmentering
            # MC1R - hårfärg
            "rs1805007",  # MC1R - rödhårighet
            "rs1805008",  # MC1R - hårfärg
            # TYR - tyrosinas
            "rs1042602",  # TYR - pigmentering
            # SLC45A2 - pigmentering
            "rs16891982", # SLC45A2 - hårfärg
            # KITLG - melanocytutveckling
            "rs12821256", # KITLG - blond hårfärg
        ]
    },

    # Njurfunktion
    "kidney": {
        "description": "Njurfunktion och njursjukdom",
        "snps": [
            # UMOD - uromodulin
            "rs12917707", # UMOD - kronisk njursjukdom
            "rs4293393",  # UMOD - eGFR
            # SHROOM3 - njurutveckling
            "rs17319721", # SHROOM3 - eGFR
            # APOL1 - apolipoprotein L1
            "rs73885319", # APOL1 G1 - njursjukdom (afrikansk)
            # CST3 - cystatin C
            "rs911119",   # CST3 - njurfunktionsmarkör
            # SLC7A9 - aminosyratransport
            "rs2236225",  # SLC7A9 - cystinuri
            # KLOTHO - anti-aging, njure
            "rs9536314",  # KLOTHO - njurfunktion
            # ACE - njurblodflöde
            "rs4340",     # ACE I/D - njursjukdom
            # AGT - angiotensinogen
            "rs699",      # AGT - njurblodtryck
        ]
    },

    # Leverfunktion
    "liver": {
        "description": "Leverfunktion och levermetabolism",
        "snps": [
            # PNPLA3 - fettlever (NAFLD)
            "rs738409",   # PNPLA3 I148M - NAFLD, NASH
            # TM6SF2 - leverfett
            "rs58542926", # TM6SF2 - NAFLD
            # MBOAT7 - fosfolipidmetabolism
            "rs641738",   # MBOAT7 - leverfett
            # HFE - järnöverlagring
            "rs1800562",  # HFE C282Y - hemokromatos
            "rs1799945",  # HFE H63D
            # UGT1A1 - bilirubin (Gilberts)
            "rs8175347",  # UGT1A1 - Gilberts syndrom
            # SERPINA1 - alfa-1-antitrypsin
            "rs28929474", # SERPINA1 Z-allel - leversjukdom
            # ABCB4 - gallsyratransport
            "rs31653",    # ABCB4 - gallsten
            # CYP2E1 - leverskada
            "rs2031920",  # CYP2E1 - alkoholinducerad
        ]
    },

    # Lungfunktion
    "lung": {
        "description": "Lungfunktion och andningsvägar",
        "snps": [
            # SERPINA1 - alfa-1-antitrypsin
            "rs28929474", # SERPINA1 Z - emfysem
            "rs17580",    # SERPINA1 S - lungsjukdom
            # HHIP - hedgehog-signalering
            "rs13118928", # HHIP - KOL
            # FAM13A - lungfunktion
            "rs7671167",  # FAM13A - KOL
            # CHRNA3/5 - nikotinreceptor
            "rs1051730",  # CHRNA3 - nikotinberoende, lungcancer
            # GSTM1 - detox
            "rs366631",   # GSTM1 null - lungcancerrisk
            # GSTP1 - detox
            "rs1695",     # GSTP1 - lungfunktion
            # MMP12 - elastinnedbrytning
            "rs2276109",  # MMP12 - KOL
            # TGFB1 - fibros
            "rs1800469",  # TGFB1 - lungfibros
        ]
    },

    # Blodkoagulation
    "coagulation": {
        "description": "Blodkoagulation och trombosrisk",
        "snps": [
            # F5 - faktor V Leiden
            "rs6025",     # F5 Leiden - trombosrisk
            # F2 - protrombin
            "rs1799963",  # F2 G20210A - trombos
            # MTHFR - homocystein
            "rs1801133",  # MTHFR - homocystein, trombos
            # SERPINC1 - antitrombin
            "rs2227589",  # SERPINC1 - antitrombinnivåer
            # PROC - protein C
            "rs1799809",  # PROC - protein C-brist
            # PROS1 - protein S
            "rs121918472",# PROS1 - protein S-brist
            # PAI-1 (SERPINE1) - fibrinolys
            "rs1799889",  # PAI-1 4G/5G - trombosrisk
            # GP1BA - trombocytfunktion
            "rs2243093",  # GP1BA - blödningsrisk
            # ITGB3 - trombocytaggregation
            "rs5918",     # ITGB3 PlA1/A2 - trombocyter
            # VKORC1 - vitamin K-cykel
            "rs9923231",  # VKORC1 - warfarindos
        ]
    },

    # Blodbildning och anemi
    "hematology": {
        "description": "Blodbildning och anemirisk",
        "snps": [
            # HBB - hemoglobin beta (sicklecell, talassemi)
            "rs334",      # HBB - sicklecell
            "rs33930165", # HBB - beta-talassemi
            # HBA - hemoglobin alfa
            "rs41469351", # HBA - alfa-talassemi
            # G6PD - glukos-6-fosfatdehydrogenas
            "rs1050828",  # G6PD - hemolytisk anemi
            # TMPRSS6 - järnreglering
            "rs855791",   # TMPRSS6 - järnbristanemi
            # HFE - järnöverlagring
            "rs1800562",  # HFE C282Y - hemokromatos
            # EPO - erytropoietin
            "rs1617640",  # EPO - erytropoietinnivåer
            # EPOR - EPO-receptor
            "rs121918116",# EPOR - polycytemi
            # VHL - von Hippel-Lindau
            "rs779805",   # VHL - erytrocytos
        ]
    },

    # Immunsystemets styrka
    "immune_strength": {
        "description": "Immunförsvarets effektivitet",
        "snps": [
            # TLR4 - bakterieigenkänning
            "rs4986790",  # TLR4 Asp299Gly - infektionskänslighet
            "rs4986791",  # TLR4 Thr399Ile
            # TLR2 - gram-positiva bakterier
            "rs5743708",  # TLR2 - infektionsrisk
            # MBL2 - mannos-bindande lektin
            "rs1800450",  # MBL2 - opsonisering
            "rs5030737",  # MBL2 - immunförsvar
            # DEFB1 - defensin
            "rs1800972",  # DEFB1 - antimikrobiellt försvar
            # IL10 - antiinflammatorisk
            "rs1800896",  # IL10 - immunbalans
            # IFNG - interferon gamma
            "rs2430561",  # IFNG - Th1-respons
            # IL12B - interleukin 12
            "rs3212227",  # IL12B - cellmedierad immunitet
            # CD14 - LPS-receptor
            "rs2569190",  # CD14 - bakterierespons
            # FCGR2A - IgG-receptor
            "rs1801274",  # FCGR2A - fagocytos
        ]
    },

    # Infektionskänslighet
    "infection_susceptibility": {
        "description": "Känslighet för specifika infektioner",
        "snps": [
            # CCR5 - HIV-resistens
            "rs333",      # CCR5-delta32 - HIV-resistens
            # IFNL3 (IL28B) - hepatit C
            "rs12979860", # IFNL3 - HCV-respons
            "rs8099917",  # IFNL3 - HCV-behandling
            # HLA-B*57:01 - HIV-progression
            "rs2395029",  # HLA-B*57:01 tag - HIV
            # FUT2 - norovirus
            "rs601338",   # FUT2 - norovirusresistens
            # TIRAP - malaria
            "rs8177374",  # TIRAP - malariaresistens
            # HBB - malaria (sicklecell-skydd)
            "rs334",      # HBB - malariaresistens
            # DARC (Duffy) - malaria
            "rs2814778",  # DARC - P. vivax-resistens
            # ACE2 - SARS-CoV-2
            "rs2285666",  # ACE2 - COVID-19-känslighet
            # TMPRSS2 - SARS-CoV-2
            "rs12329760", # TMPRSS2 - COVID-19
        ]
    },

    # Läkemedelsmetabolism (utökning av pharmacogenomics)
    "drug_metabolism": {
        "description": "Läkemedelsmetabolism och dosering",
        "snps": [
            # CYP2D6 - kodein, tramadol, antidepressiva
            "rs3892097",  # CYP2D6 *4 - poor metabolizer
            "rs16947",    # CYP2D6 *2
            "rs1065852",  # CYP2D6 *10
            # CYP2C19 - PPI, klopidogrel, antidepressiva
            "rs4244285",  # CYP2C19 *2 - poor metabolizer
            "rs12248560", # CYP2C19 *17 - ultra-rapid
            # CYP2C9 - warfarin, NSAID
            "rs1799853",  # CYP2C9 *2
            "rs1057910",  # CYP2C9 *3
            # CYP3A4/5 - statiner, immunsuppressiva
            "rs35599367", # CYP3A4 *22
            "rs776746",   # CYP3A5 *3
            # SLCO1B1 - statinbiverkningar
            "rs4149056",  # SLCO1B1 - myopati
            # VKORC1 - warfarin
            "rs9923231",  # VKORC1 - warfarindos
            # DPYD - 5-fluorouracil
            "rs3918290",  # DPYD *2A - toxicitet
            # TPMT - azatioprin
            "rs1800460",  # TPMT *3B
            "rs1142345",  # TPMT *3C
            # UGT1A1 - irinotecan
            "rs8175347",  # UGT1A1 *28
            # ABCB1 - P-glykoprotein
            "rs1045642",  # ABCB1 - läkemedelstransport
        ]
    },

    # Beroende och missbruk
    "addiction": {
        "description": "Beroendebenägenhet och belöningssystem",
        "snps": [
            # DRD2 - dopaminreceptor
            "rs1800497",  # DRD2/ANKK1 Taq1A - beroende
            # DRD4 - dopaminreceptor
            "rs1800955",  # DRD4 - novelty seeking
            # OPRM1 - opioidreceptor
            "rs1799971",  # OPRM1 A118G - opioidberoende
            # CHRNA5 - nikotinreceptor
            "rs16969968", # CHRNA5 - nikotinberoende
            # CHRNA3 - nikotinreceptor
            "rs1051730",  # CHRNA3 - rökbeteende
            # ADH1B - alkohol
            "rs1229984",  # ADH1B - alkoholberoende
            # ALDH2 - alkohol
            "rs671",      # ALDH2 - alkoholintolerans
            # GABRA2 - GABA-receptor
            "rs279858",   # GABRA2 - alkoholberoende
            # SLC6A4 - serotonintransportör
            "rs25531",    # SLC6A4 - beroende, depression
            # COMT - dopaminmetabolism
            "rs4680",     # COMT - belöningskänslighet
            # FAAH - endocannabinoider
            "rs324420",   # FAAH - cannabisberoende
        ]
    },

    # Mental hälsa (utökning)
    "mental_health": {
        "description": "Psykisk hälsa och psykiatrisk risk",
        "snps": [
            # SLC6A4 - serotonintransportör
            "rs25531",    # SLC6A4 5-HTTLPR - depression
            # BDNF - neuroplasticitet
            "rs6265",     # BDNF Val66Met - depression
            # COMT - dopamin
            "rs4680",     # COMT - ångest, psykos
            # FKBP5 - stressrespons
            "rs1360780",  # FKBP5 - PTSD, depression
            # NR3C1 - glukokortikoidreceptor
            "rs41423247", # NR3C1 - stressrespons
            # CACNA1C - kalciumkanal
            "rs1006737",  # CACNA1C - bipolär, schizofreni
            # ANK3 - ankyrin 3
            "rs10994336", # ANK3 - bipolär
            # DISC1 - disrupted in schizophrenia
            "rs821616",   # DISC1 - schizofreni
            # ZNF804A - schizofreni
            "rs1344706",  # ZNF804A - psykosrisk
            # NCAN - neurocan
            "rs1064395",  # NCAN - bipolär
            # OXTR - oxytocin
            "rs53576",    # OXTR - social ångest
        ]
    },

    # Träningsrespons och återhämtning
    "exercise_response": {
        "description": "Träningsrespons, återhämtning och skaderisk",
        "snps": [
            # ACTN3 - muskelfibertyp
            "rs1815739",  # ACTN3 R577X - power vs endurance
            # ACE - uthållighet
            "rs4340",     # ACE I/D - uthållighet
            # PPARGC1A - mitokondrier
            "rs8192678",  # PPARGC1A - VO2max-respons
            # VEGFA - angiogenes
            "rs2010963",  # VEGFA - kapillärtäthet
            # IL6 - inflammationsrespons
            "rs1800795",  # IL6 - träningsinflammation
            # TNF - återhämtning
            "rs1800629",  # TNF - muskelskada
            # COL1A1 - skaderisk
            "rs1800012",  # COL1A1 - senskada
            # COL5A1 - ligament
            "rs12722",    # COL5A1 - Akilles-skada
            # MMP3 - vävnadsreparation
            "rs3025058",  # MMP3 - skaderisk
            # CKM - kreatinkinas
            "rs8111989",  # CKM - muskelskademarkörer
            # AMPD1 - muskeluthållighet
            "rs17602729", # AMPD1 - muskelkramp
            # NOS3 - blodflöde
            "rs1799983",  # NOS3 - träningsblodflöde
        ]
    },

    # Hydratisering och vätskebalans
    "hydration": {
        "description": "Vätskebalans och elektrolyter",
        "snps": [
            # AQP1 - aquaporin 1
            "rs1049305",  # AQP1 - vätskereglering
            # AVP - vasopressin
            "rs3761548",  # AVP - vätskebalans
            # AVPR2 - vasopressinreceptor
            "rs5765649",  # AVPR2 - njurkoncentration
            # ADD1 - saltkänslighet
            "rs4961",     # ADD1 - natriumbalans
            # ACE - vätskebalans
            "rs4340",     # ACE - blodtryck, vätska
            # AGT - angiotensinogen
            "rs699",      # AGT - vätskeretention
            # SCNN1A - natriumkanal
            "rs2228576",  # SCNN1A - natriumreabsorption
        ]
    },

    # Värme/kyla-tolerans
    "thermoregulation": {
        "description": "Temperaturreglering och tolerans",
        "snps": [
            # UCP1 - brun fett
            "rs1800592",  # UCP1 - termogenes
            # UCP2 - energieffektivitet
            "rs659366",   # UCP2 - värmeproduktion
            # UCP3 - muskelvärmning
            "rs1800849",  # UCP3 - termogenes
            # TRPM8 - köldreceptor
            "rs11562975", # TRPM8 - köldkänslighet
            # TRPV1 - värmereceptor
            "rs8065080",  # TRPV1 - värmekänslighet
            # ADRB3 - brun fettaktivering
            "rs4994",     # ADRB3 Trp64Arg - termogenes
            # PRDM16 - brun fett
            "rs2651899",  # PRDM16 - brun fettbildning
        ]
    },

    # Höjdanpassning
    "altitude": {
        "description": "Höjdanpassning och syreeffektivitet",
        "snps": [
            # EPAS1 - HIF-2α
            "rs1868092",  # EPAS1 - höjdanpassning
            # EGLN1 (PHD2) - HIF-reglering
            "rs480902",   # EGLN1 - syresensing
            # HBB - hemoglobin
            "rs334",      # HBB - syrebindning
            # EPO - erytropoietin
            "rs1617640",  # EPO - erytropoietinproduktion
            # VEGFA - angiogenes
            "rs2010963",  # VEGFA - kärlbildning
            # NOS3 - kväveoxid
            "rs1799983",  # NOS3 - vasodilatation
            # ACE - syreeffektivitet
            "rs4340",     # ACE - höjdprestation
        ]
    },

    # Ätbeteende och matpsykologi
    "eating_behavior": {
        "description": "Ätbeteende, mättnad och matpsykologi",
        "snps": [
            # FTO - aptit
            "rs9939609",  # FTO - överätande
            # MC4R - mättnad
            "rs17782313", # MC4R - mättnadssignal
            # DRD2 - belöning
            "rs1800497",  # DRD2 - matbelöning
            # OPRM1 - hedoniskt ätande
            "rs1799971",  # OPRM1 - matnjutning
            # ANKK1 - dopamin
            "rs1800497",  # ANKK1 - belöningskänslighet
            # SLC6A4 - serotonin
            "rs25531",    # SLC6A4 - emotionellt ätande
            # BDNF - aptitreglering
            "rs6265",     # BDNF - viktreglering
            # LEP - leptin
            "rs7799039",  # LEP - mättnad
            # LEPR - leptinreceptor
            "rs1137101",  # LEPR - leptinresistens
            # NPY - stressätande
            "rs16147",    # NPY - stress-ätande
        ]
    },

    # Dygnsvariation i metabolism
    "chronotype": {
        "description": "Kronotyp och metabolisk dygnsrytm",
        "snps": [
            # PER2 - morgon/kväll
            "rs2304672",  # PER2 - kronotyp
            # CLOCK - dygnsrytm
            "rs1801260",  # CLOCK - kvällsmänniska
            # CRY1 - sömnfas
            "rs2287161",  # CRY1 - försenad fas
            # MTNR1B - melatonin
            "rs10830963", # MTNR1B - glukosrytm
            # ARNTL - metabolisk rytm
            "rs2278749",  # ARNTL - metabolisk timing
            # NR1D1 - metabolisk klocka
            "rs2314339",  # NR1D1 - lipidmetabolism
            # NPAS2 - hjärnklocka
            "rs2305160",  # NPAS2 - cirkadisk
            # PER3 - sömnbehov
            "rs57875989", # PER3 - sömnlängd
        ]
    },

    # Graviditet och fosterutveckling
    "pregnancy": {
        "description": "Graviditet, fosterutveckling och komplikationer",
        "snps": [
            # MTHFR - neuralrörsdefekter
            "rs1801133",  # MTHFR C677T - folat
            "rs1801131",  # MTHFR A1298C
            # F5 - trombosrisk
            "rs6025",     # F5 Leiden - graviditetstrombos
            # F2 - protrombin
            "rs1799963",  # F2 - missfall
            # ACE - preeklampsi
            "rs4340",     # ACE - preeklampsi
            # AGT - graviditetshypertoni
            "rs699",      # AGT - preeklampsi
            # VEGFA - placentautveckling
            "rs2010963",  # VEGFA - preeklampsi
            # ESR1 - östrogenreceptor
            "rs2234693",  # ESR1 - graviditetsutfall
            # FSHR - fertilitet
            "rs6166",     # FSHR - ovariell respons
            # LHB - ovulation
            "rs1800447",  # LHB - graviditet
        ]
    },

    # Åldrande och senescence
    "aging": {
        "description": "Biologiskt åldrande och senescence",
        "snps": [
            # TERT - telomerlängd
            "rs2736100",  # TERT - telomeras
            # TERC - telomeras RNA
            "rs12696304", # TERC - telomerlängd
            # FOXO3 - longevity
            "rs2802292",  # FOXO3 - hälsosamt åldrande
            # APOE - åldrande
            "rs429358",   # APOE e4 - åldrande
            # KLOTHO - anti-aging
            "rs9536314",  # KLOTHO - åldrande
            # SIRT1 - cellulär åldrande
            "rs7895833",  # SIRT1 - longevity
            # SIRT3 - mitokondriellt åldrande
            "rs11555236", # SIRT3 - åldrande
            # TP53 - cellcykel
            "rs1042522",  # TP53 - åldrande
            # CDKN2A (p16) - senescence
            "rs3731239",  # CDKN2A - cellåldrande
            # LMNA - progeria-relaterad
            "rs4641",     # LMNA - kärlåldrande
        ]
    },

    # Detox fas III (transport)
    "detox_phase3": {
        "description": "Fas III detox - transportörer",
        "snps": [
            # ABCB1 (P-glykoprotein) - efflux
            "rs1045642",  # ABCB1 C3435T - läkemedelstransport
            "rs2032582",  # ABCB1 G2677T/A
            "rs1128503",  # ABCB1 C1236T
            # ABCC2 (MRP2) - biliär utsöndring
            "rs717620",   # ABCC2 - gallexkretion
            # ABCG2 (BCRP) - efflux
            "rs2231142",  # ABCG2 - urattransport
            # SLC22A1 (OCT1) - hepatiskt upptag
            "rs628031",   # SLC22A1 - metforminrespons
            # SLCO1B1 - hepatiskt upptag
            "rs4149056",  # SLCO1B1 - statintransport
            # SLC22A2 (OCT2) - njurutsöndring
            "rs316019",   # SLC22A2 - njurtransport
        ]
    },

    # Xenobiotika och miljögifter
    "xenobiotics": {
        "description": "Metabolism av miljögifter och xenobiotika",
        "snps": [
            # PON1 - paraoxonas (pesticider)
            "rs662",      # PON1 Q192R - pesticiddetox
            "rs854560",   # PON1 L55M
            # EPHX1 - epoxidhydrolas (PAH)
            "rs1051740",  # EPHX1 - PAH-metabolism
            "rs2234922",  # EPHX1 - xenobiotika
            # NAT1 - N-acetyltransferas 1
            "rs4986782",  # NAT1 - aromatiska aminer
            # NAT2 - N-acetyltransferas 2
            "rs1801280",  # NAT2 - acetylerarstatus
            "rs1799930",  # NAT2 - karcinogenmetabolism
            # AHR - arylkolvätereceptor (dioxin)
            "rs2066853",  # AHR - dioxinkänslighet
            # NQO1 - kinondetox
            "rs1800566",  # NQO1 - bensenmetabolism
            # GSTM1 - glutationtransferas
            "rs366631",   # GSTM1 null - detoxkapacitet
            # GSTT1 - glutationtransferas
            "rs17856199", # GSTT1 null - detox
        ]
    },

    # =========================================================================
    # SUPPLEMENT LIBRARY - Specifika SNPs från Vitamin_Mineral_Supplementation_Library
    # =========================================================================

    # CoQ10 / Ubiquinol metabolism
    "coq10": {
        "description": "Coenzym Q10-syntes och metabolism",
        "snps": [
            # COQ2-COQ9 - CoQ10-syntes
            "rs4693075",  # COQ2 - CoQ10-produktion
            "rs6535454",  # COQ2 - CoQ10-brist
            "rs2074388",  # COQ3 - CoQ10-syntes
            "rs2228309",  # COQ4 - mitokondriefunktion
            "rs1129069",  # COQ5 - CoQ10-biosyntes
            "rs2295112",  # COQ6 - CoQ10-syntes
            "rs2074389",  # COQ7 - CoQ10-syntes
            "rs10420252", # COQ8A - CoQ10-syntes
            "rs1045642",  # ABCB1 - CoQ10-transport
            # NQO1 - kinonreduktas (CoQ10-recycling)
            "rs1800566",  # NQO1 - CoQ10-regenerering
            # APOE - CoQ10-behov
            "rs429358",   # APOE e4 - högre CoQ10-behov
        ]
    },

    # Vitamin B3 / NAD+ metabolism (NR/NMN)
    "nad_metabolism": {
        "description": "NAD+-metabolism och sirtuinaktivering",
        "snps": [
            # NAMPT - nikotinamid fosforibosyltransferas (rate-limiting)
            "rs61330082", # NAMPT - NAD+-syntes
            "rs9770242",  # NAMPT - NAD+-nivåer
            # NMNAT1/2/3 - nikotinamid mononukleotid adenylyltransferas
            "rs11539044", # NMNAT1 - NAD+-syntes
            # SIRT1 - sirtuin 1 (NAD+-beroende)
            "rs7895833",  # SIRT1 - NAD+-användning
            "rs3758391",  # SIRT1 - longevity
            # SIRT3 - mitokondriell sirtuin
            "rs11555236", # SIRT3 - mitokondriell NAD+
            # PARP1 - poly(ADP-ribos)polymeras (NAD+-konsument)
            "rs1136410",  # PARP1 - DNA-reparation, NAD+-förbrukning
            # CD38 - NAD+-konsument
            "rs1800561",  # CD38 - NAD+-nedbrytning
        ]
    },

    # Tyrosin och katekolaminsyntes
    "tyrosine": {
        "description": "Tyrosinmetabolism och katekolaminsyntes",
        "snps": [
            # TH - tyrosinhydroxylas (rate-limiting för dopamin)
            "rs6356",     # TH - dopaminsyntes
            "rs10770141", # TH - katekolaminproduktion
            # DDC - DOPA-dekarboxylas
            "rs3837091",  # DDC - dopamin/serotonin-syntes
            # DBH - dopamin beta-hydroxylas (dopamin→noradrenalin)
            "rs1611115",  # DBH - noradrenalinsyntes
            "rs77905",    # DBH - DBH-aktivitet
            # COMT - katekolamin O-metyltransferas
            "rs4680",     # COMT Val158Met - dopaminnedbrytning
            # MAO-A - monoaminoxidas A
            "rs6323",     # MAO-A - katekolaminnedbrytning
            # PAH - fenylalaninhydroxylas (fenylalanin→tyrosin)
            "rs1042503",  # PAH - tyrosinproduktion
        ]
    },

    # Tryptofan och serotoninsyntes
    "tryptophan": {
        "description": "Tryptofanmetabolism och serotoninsyntes",
        "snps": [
            # TPH1 - tryptofanhydroxylas 1 (perifer)
            "rs1800532",  # TPH1 - serotoninsyntes
            # TPH2 - tryptofanhydroxylas 2 (hjärna)
            "rs4570625",  # TPH2 - hjärnserotonin
            "rs1386494",  # TPH2 - depression
            # DDC - aromatisk aminosyradekarboxylas
            "rs3837091",  # DDC - 5-HTP→serotonin
            # SLC6A4 - serotonintransportör
            "rs25531",    # SLC6A4 5-HTTLPR - serotoninåterupptag
            # HTR2A - serotoninreceptor 2A
            "rs6311",     # HTR2A - serotoninrespons
            # IDO1/TDO2 - tryptofan→kynurenin (konkurrerar med serotonin)
            "rs3824259",  # IDO1 - kynureninvägen
            "rs3755910",  # TDO2 - tryptofannedbrytning
            # AANAT - serotonin→melatonin
            "rs3760138",  # AANAT - melatoninsyntes
        ]
    },

    # Glutamin och tarmhälsa
    "glutamine": {
        "description": "Glutaminmetabolism och tarmbarriär",
        "snps": [
            # GLS - glutaminas (glutamin→glutamat)
            "rs2657879",  # GLS - glutaminmetabolism
            "rs12185688", # GLS - tarmhälsa
            # GLS2 - leverglutaminas
            "rs2638315",  # GLS2 - levermetabolism
            # GLUL - glutaminsyntas
            "rs10911021", # GLUL - glutaminsyntes
            # SLC1A5 - glutamintransportör (ASCT2)
            "rs3027956",  # SLC1A5 - glutaminupptag
            # SLC38A1 - glutamintransportör (SNAT1)
            "rs1049434",  # SLC38A1 - glutamintransport
        ]
    },

    # Glycin och kollagensyntes
    "glycine": {
        "description": "Glycinmetabolism och kollagensyntes",
        "snps": [
            # GLDC - glycindekarboxylas
            "rs2297441",  # GLDC - glycinmetabolism
            # SHMT1/2 - serinhydroximetyltransferas
            "rs1979277",  # SHMT1 - glycin/serinbalans
            "rs12952106", # SHMT2 - mitokondriell glycin
            # SLC6A9 - glycintransportör (GLYT1)
            "rs2486001",  # SLC6A9 - glycinåterupptag
            # ALAS1 - aminolevulinatsyntetas (glycin→hem)
            "rs352162",   # ALAS1 - hemsyntes
            # PRODH - prolindehydrogenas (prolin→glycin)
            "rs2904552",  # PRODH - prolinmetabolism
        ]
    },

    # Arginin och kväveoxid
    "arginine": {
        "description": "Argininmetabolism och NO-produktion",
        "snps": [
            # NOS3 - endotelial kväveoxidsyntas
            "rs1799983",  # NOS3 Glu298Asp - NO-produktion
            "rs2070744",  # NOS3 - promotorvariant
            # NOS1 - neuronal NO-syntas
            "rs2682826",  # NOS1 - neuronal NO
            # ARG1 - arginas 1 (arginin→ornitin)
            "rs2781666",  # ARG1 - argininkonkurrens
            # ASS1 - argininosuccinatsyntas
            "rs2297518",  # ASS1 - argininsyntes
            # ASL - argininosuccinatlyas
            "rs1133775",  # ASL - argininproduktion
            # SLC7A1 - arginin/lysintransportör (CAT1)
            "rs41318021", # SLC7A1 - argininupptag
            # DDAH1 - dimetylarginin dimetylaminohydrolas
            "rs233112",   # DDAH1 - ADMA-nedbrytning (NO-hämmare)
        ]
    },

    # Beta-alanin och karnosin
    "beta_alanine": {
        "description": "Beta-alanin och karnosinmetabolism",
        "snps": [
            # CARNS1 - karnosinsyntetas
            "rs2887884",  # CARNS1 - karnosinproduktion
            # CNDP1 - karnosindipeptidas (karnosinnedbrytning)
            "rs2346061",  # CNDP1 - karnosinnivåer
            # SLC6A6 - taurin/beta-alanintransportör
            "rs2013162",  # SLC6A6 - beta-alaninupptag
            # HDC - histidindekarboxylas (histidin→histamin)
            "rs2073440",  # HDC - histaminproduktion
        ]
    },

    # Citrullin och ureacykel
    "citrulline": {
        "description": "Citrullinmetabolism och NO-prekursor",
        "snps": [
            # ASS1 - citrullin→argininosuccinat
            "rs2297518",  # ASS1 - citrullinkonvertering
            # ASL - argininosuccinat→arginin
            "rs1133775",  # ASL - argininproduktion
            # CPS1 - karbamoylfosfatsyntas
            "rs1047891",  # CPS1 - ureacykelkapacitet
            # OTC - ornitintranskarbamylas
            "rs5963409",  # OTC - citrullinsyntes
            # NOS3 - citrullin som NO-biprodukt
            "rs1799983",  # NOS3 - NO/citrullin
        ]
    },

    # Adaptogens respons (Ashwagandha, Rhodiola)
    "adaptogen_response": {
        "description": "Adaptogenrespons och stresshantering",
        "snps": [
            # COMT - stressrespons
            "rs4680",     # COMT Val158Met - adaptogenbehov
            # NR3C1 - glukokortikoidreceptor
            "rs41423247", # NR3C1 - kortisolkänslighet
            "rs6190",     # NR3C1 - stressrespons
            # FKBP5 - kortisolreglering
            "rs1360780",  # FKBP5 - HPA-axel
            "rs9296158",  # FKBP5 - stressåterhämtning
            # CRHR1 - CRH-receptor
            "rs110402",   # CRHR1 - stressrespons
            # ADRB2 - beta-2-adrenerg receptor
            "rs1042713",  # ADRB2 - stressrespons
            # TPO - sköldkörtel (ashwagandha påverkar)
            "rs2071403",  # TPO - sköldkörtelfunktion
            # DIO2 - T4→T3 (ashwagandha påverkar)
            "rs225014",   # DIO2 - sköldkörtelkonvertering
        ]
    },

    # Curcumin/Turmeric metabolism
    "curcumin": {
        "description": "Curcuminmetabolism och antiinflammatorisk respons",
        "snps": [
            # UGT1A1 - glukuronidkonjugering (curcumin-metabolism)
            "rs8175347",  # UGT1A1 *28 - Gilberts, curcumin-metabolism
            # IL1B - interleukin 1 beta
            "rs16944",    # IL1B - inflammationsrespons
            "rs1143634",  # IL1B - curcuminrespons
            # IL6 - interleukin 6
            "rs1800795",  # IL6 - inflammationsrespons
            # TNF - tumörnekrosfaktor
            "rs1800629",  # TNF - antiinflammatorisk respons
            # CYP3A4 - curcuminmetabolism
            "rs35599367", # CYP3A4 *22 - curcuminnedbrytning
            # NF-kB-relaterade
            "rs28362491", # NFKB1 - inflammationsreglering
        ]
    },

    # Berberine metabolism
    "berberine": {
        "description": "Berberinmetabolism och glukosreglering",
        "snps": [
            # CYP3A4 - berberinmetabolism
            "rs35599367", # CYP3A4 *22 - berberinnedbrytning
            # CYP2D6 - berberinmetabolism
            "rs3892097",  # CYP2D6 *4 - berberinmetabolism
            # ABCB1 - P-glykoprotein (berberintransport)
            "rs1045642",  # ABCB1 - berberinabsorption
            # TCF7L2 - diabetesriskgen
            "rs7903146",  # TCF7L2 - berberinrespons
            # PPARG - insulinkänslighet
            "rs1801282",  # PPARG Pro12Ala - berberinrespons
            # AMPK-relaterade
            "rs2796498",  # PRKAA2 - AMPK-aktivering
            # APOE - lipidrespons
            "rs429358",   # APOE - berberinlipideffekt
        ]
    },

    # Melatonin metabolism
    "melatonin": {
        "description": "Melatoninsyntes och -metabolism",
        "snps": [
            # AANAT - arylalkylamin N-acetyltransferas (serotonin→melatonin)
            "rs3760138",  # AANAT - melatoninsyntes
            "rs28936679", # AANAT - melatoninproduktion
            # ASMT - acetylserotonin O-metyltransferas (slutsteg)
            "rs4446909",  # ASMT - melatoninsyntes
            "rs5989681",  # ASMT - melatoninnivåer
            # MTNR1A - melatoninreceptor 1A
            "rs2119882",  # MTNR1A - melatoninkänslighet
            # MTNR1B - melatoninreceptor 1B
            "rs10830963", # MTNR1B - glukosmetabolism, diabetes
            "rs1387153",  # MTNR1B - melatoninrespons
            # CYP1A2 - melatoninmetabolism
            "rs762551",   # CYP1A2 - melatoninnedbrytning
            # PER2 - cirkadisk rytm
            "rs2304672",  # PER2 - melatonintiming
        ]
    },

    # Probiotika respons
    "probiotic_response": {
        "description": "Probiotikrespons och mikrobiominteraktion",
        "snps": [
            # FUT2 - sekretorstatus (mikrobiomsammansättning)
            "rs601338",   # FUT2 - non-secretor, mikrobiom
            # LCT - laktas (laktobacillusrespons)
            "rs4988235",  # LCT - laktosintolerans
            # NOD2 - bakterieigenkänning
            "rs2066844",  # NOD2 - tarmimmunitet
            "rs2066845",  # NOD2 - mikrobiombalans
            # TLR4 - bakterieigenkänning
            "rs4986790",  # TLR4 - probiotikrespons
            # IL10 - antiinflammatorisk
            "rs1800896",  # IL10 - tarmimmunbalans
            # MUC2 - mucinproduktion
            "rs11825977", # MUC2 - slemhinnebarriär
            # DEFB1 - defensin
            "rs1800972",  # DEFB1 - antimikrobiellt försvar
        ]
    },

    # Omega-6 / GLA metabolism
    "omega6": {
        "description": "Omega-6 och GLA-metabolism",
        "snps": [
            # FADS1 - delta-5-desaturas
            "rs174546",   # FADS1 - AA-syntes
            "rs174547",   # FADS1 - omega-6-konvertering
            # FADS2 - delta-6-desaturas
            "rs174575",   # FADS2 - GLA-syntes
            "rs1535",     # FADS2 - omega-6-metabolism
            # ELOVL2 - fettsyraförlängning
            "rs953413",   # ELOVL2 - omega-6-förlängning
            # ALOX5 - 5-lipoxygenas (AA→leukotriener)
            "rs2115819",  # ALOX5 - inflammatorisk respons
            # PTGS2 (COX-2) - prostaglandinsyntes
            "rs20417",    # PTGS2 - inflammationsrespons
        ]
    },

    # Inositol metabolism
    "inositol": {
        "description": "Inositolmetabolism och insulinsignalering",
        "snps": [
            # ISYNA1 - inositolsyntas
            "rs2305160",  # ISYNA1 - inositolproduktion
            # IMPA1 - inositolmonofosfatas
            "rs669838",   # IMPA1 - inositolrecycling
            # IMPA2 - inositolmonofosfatas 2
            "rs3786282",  # IMPA2 - inositolmetabolism
            # PIK3R1 - fosfoinositid 3-kinas
            "rs3730089",  # PIK3R1 - insulinsignalering
            # INSR - insulinreceptor
            "rs2059806",  # INSR - insulinkänslighet
            # IRS1 - insulinreceptorsubstrat
            "rs1801278",  # IRS1 - insulinsignalering
        ]
    },

    # PQQ och mitokondriell biogenes
    "pqq": {
        "description": "PQQ och mitokondriell biogenes",
        "snps": [
            # PPARGC1A - PGC-1alfa (mitokondriell biogenes)
            "rs8192678",  # PPARGC1A - mitokondrier
            # NRF1 - nukleär respiratorisk faktor
            "rs6949152",  # NRF1 - mitokondriell biogenes
            # TFAM - mitokondriell transkriptionsfaktor
            "rs1937",     # TFAM - mtDNA-kopietal
            # SIRT1 - sirtuin (PQQ aktiverar)
            "rs7895833",  # SIRT1 - mitokondriefunktion
            # SIRT3 - mitokondriell sirtuin
            "rs11555236", # SIRT3 - mitokondriell metabolism
        ]
    },

    # Resveratrol respons
    "resveratrol": {
        "description": "Resveratrolmetabolism och sirtuinaktivering",
        "snps": [
            # SIRT1 - resveratrolmål
            "rs7895833",  # SIRT1 - resveratrolrespons
            "rs3758391",  # SIRT1 - longevity
            # CYP1A1 - resveratrolmetabolism
            "rs1048943",  # CYP1A1 - resveratrolnedbrytning
            # CYP1B1 - resveratrolmetabolism
            "rs1056836",  # CYP1B1 - resveratrolmetabolism
            # SULT1A1 - sulfatkonjugering
            "rs9282861",  # SULT1A1 - resveratrolkonjugering
            # UGT1A1 - glukuronidkonjugering
            "rs8175347",  # UGT1A1 - resveratrolmetabolism
            # NQO1 - kinonreduktas
            "rs1800566",  # NQO1 - antioxidantrespons
        ]
    },

    # Quercetin metabolism
    "quercetin": {
        "description": "Quercetinmetabolism och antiinflammatorisk effekt",
        "snps": [
            # COMT - quercetinmetylering
            "rs4680",     # COMT - quercetinmetabolism
            # SULT1A1 - quercetinsulfatering
            "rs9282861",  # SULT1A1 - quercetinkonjugering
            # UGT1A1 - quercetinglukuronidkonjugering
            "rs8175347",  # UGT1A1 - quercetinmetabolism
            # CYP1A2 - quercetinmetabolism
            "rs762551",   # CYP1A2 - quercetinnedbrytning
            # NF-kB-relaterade
            "rs28362491", # NFKB1 - antiinflammatorisk respons
            # ABCB1 - quercetintransport
            "rs1045642",  # ABCB1 - quercetinabsorption
        ]
    },

    # Alpha-lipoic acid (ALA) metabolism
    "alpha_lipoic_acid": {
        "description": "Alfa-liponsyra metabolism och antioxidant",
        "snps": [
            # LIPT1 - lipoattransferas
            "rs11539044", # LIPT1 - lipoatmetabolism
            # LIAS - lipoatsyntetas
            "rs2278008",  # LIAS - ALA-syntes
            # SLC25A1 - mitokondriell transport
            "rs1127678",  # SLC25A1 - ALA-transport
            # NQO1 - kinonreduktas (ALA-recycling)
            "rs1800566",  # NQO1 - ALA-regenerering
            # GSR - glutationreduktas (ALA regenererar glutation)
            "rs2551715",  # GSR - glutationrecycling
            # PPARG - insulinkänslighet (ALA-effekt)
            "rs1801282",  # PPARG - ALA-respons
        ]
    },

    # Phosphatidylserine och fosfolipider
    "phospholipids": {
        "description": "Fosfolipidmetabolism och hjärnhälsa",
        "snps": [
            # PEMT - fosfatidyletanolamin→fosfatidylkolin
            "rs12325817", # PEMT - fosfolipidsyntes
            "rs7946",     # PEMT - kolinbehov
            # PCYT1A - CDP-kolinsyntes
            "rs7639752",  # PCYT1A - fosfolipidproduktion
            # LPCAT3 - fosfolipidremodellering
            "rs2064074",  # LPCAT3 - membransammansättning
            # PLA2G6 - fosfolipas A2
            "rs132985",   # PLA2G6 - fosfolipidnedbrytning
            # APOE - fosfolipidtransport
            "rs429358",   # APOE - hjärnfosfolipider
        ]
    },

    # Digestive enzymes och magsyra
    "digestive_enzymes": {
        "description": "Matsmältningsenzymer och magsyraproduktion",
        "snps": [
            # AMY1 - amylas (kolhydratsmältning)
            "rs4244372",  # AMY1 - amylasaktivitet
            # LCT - laktas
            "rs4988235",  # LCT - laktossmältning
            # SI - sukras-isomaltas
            "rs9290264",  # SI - sackarossmältning
            # PRSS1 - trypsinogen
            "rs10273639", # PRSS1 - proteinsmältning
            # LIPF - gastrisk lipas
            "rs814628",   # LIPF - fettsmältning
            # ATP4A - protonpump (magsyra)
            "rs2733743",  # ATP4A - magsyraproduktion
            # GIF - intrinsic factor (B12-absorption)
            "rs558660",   # GIF - B12-absorption
        ]
    },

    # MSM / Svavel metabolism
    "sulfur_metabolism": {
        "description": "Svavelmetabolism och MSM",
        "snps": [
            # CBS - cystationin beta-syntas
            "rs234706",   # CBS - svavelmetabolism
            "rs1801181",  # CBS - homocystein→cystein
            # CTH - cystationas (cystein→taurin)
            "rs1021737",  # CTH - svavelaminosyror
            # SUOX - sulfitoxidas
            "rs705702",   # SUOX - sulfitdetox
            # PAPSS2 - PAPS-syntas (sulfatering)
            "rs10993994", # PAPSS2 - sulfateringskapacitet
            # SULT1A1 - sulfotransferas
            "rs9282861",  # SULT1A1 - sulfatering
        ]
    },

    # Hyaluronic acid och ledvätska
    "hyaluronic_acid": {
        "description": "Hyaluronsyrasyntes och ledhälsa",
        "snps": [
            # HAS1/2/3 - hyaluronsyrasyntetas
            "rs4455882",  # HAS2 - hyaluronsyraproduktion
            "rs2232945",  # HAS3 - hyaluronsyrasyntes
            # HYAL1/2 - hyaluronidas (nedbrytning)
            "rs2070980",  # HYAL1 - hyaluronsyranedbrytning
            # CD44 - hyaluronsyrareceptor
            "rs353639",   # CD44 - hyaluronsyrabindning
            # ACAN - aggrekan (broskproteoglykan)
            "rs1516797",  # ACAN - broskstruktur
        ]
    },

    # Glucosamine och kondroitin
    "glucosamine": {
        "description": "Glukosamin och kondroitinmetabolism",
        "snps": [
            # GFPT1 - glutamin-fruktos-6-fosfat transaminase
            "rs10507248", # GFPT1 - glukosaminsyntes
            # GNPDA1 - glukosamin-6-fosfat deaminase
            "rs2839698",  # GNPDA1 - glukosaminmetabolism
            # CHST11 - kondroitinsulfotransferas
            "rs2280153",  # CHST11 - kondroitinsulfatering
            # CSGALNACT1 - kondroitinsulfatsyntes
            "rs11607062", # CSGALNACT1 - kondroitinproduktion
            # ACAN - aggrekan
            "rs1516797",  # ACAN - broskstruktur
            # COL2A1 - kollagen typ II (brosk)
            "rs2276454",  # COL2A1 - broskkollagen
        ]
    }
}

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class PubMedReference:
    pmid: str
    title: str
    authors: str
    journal: str
    year: str
    doi: str
    abstract: str

@dataclass
class SNPData:
    rsid: str
    gene: str
    chromosome: str
    position: int
    ref_allele: str
    alt_allele: str
    function: str
    clinical_significance: str
    maf_global: float
    references: List[PubMedReference]
    fetch_date: str

@dataclass
class CategoryData:
    category: str
    description: str
    snps: List[SNPData]
    total_references: int
    fetch_date: str

# =============================================================================
# NCBI API FUNCTIONS
# =============================================================================

def make_request(url: str, max_retries: int = 3) -> Optional[str]:
    """Gör en HTTP-request med retry-logik."""
    for attempt in range(max_retries):
        try:
            req = Request(url)
            req.add_header('User-Agent', 'GWL-Fetcher/1.0 (Genetic Wellness Labs)')
            with urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')
        except HTTPError as e:
            print(f"  HTTP Error {e.code}: {e.reason}")
            if e.code == 429:  # Rate limit
                time.sleep(5)
            elif attempt < max_retries - 1:
                time.sleep(2)
        except URLError as e:
            print(f"  URL Error: {e.reason}")
            if attempt < max_retries - 1:
                time.sleep(2)
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)

    return None

def search_pubmed(query: str, max_results: int = 10) -> List[str]:
    """Sök i PubMed och returnera PMIDs."""
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': max_results,
        'retmode': 'json',
        'sort': 'relevance'
    }

    url = f"{NCBI_BASE_URL}/esearch.fcgi?{urlencode(params)}"
    time.sleep(RATE_LIMIT_DELAY)

    response = make_request(url)
    if response:
        try:
            data = json.loads(response)
            return data.get('esearchresult', {}).get('idlist', [])
        except json.JSONDecodeError:
            pass

    return []

def fetch_pubmed_details(pmids: List[str]) -> List[PubMedReference]:
    """Hämta detaljer för PubMed-artiklar."""
    if not pmids:
        return []

    references = []

    # Hämta i batchar om 10
    for i in range(0, len(pmids), 10):
        batch = pmids[i:i+10]
        params = {
            'db': 'pubmed',
            'id': ','.join(batch),
            'retmode': 'xml'
        }

        url = f"{NCBI_BASE_URL}/efetch.fcgi?{urlencode(params)}"
        time.sleep(RATE_LIMIT_DELAY)

        response = make_request(url)
        if response:
            # Enkel XML-parsing
            for pmid in batch:
                ref = parse_pubmed_xml(response, pmid)
                if ref:
                    references.append(ref)

    return references

def parse_pubmed_xml(xml: str, pmid: str) -> Optional[PubMedReference]:
    """Extrahera information från PubMed XML."""
    try:
        # Hitta artikel för denna PMID
        article_start = xml.find(f'<PMID Version="1">{pmid}</PMID>')
        if article_start == -1:
            return None

        article_end = xml.find('</PubmedArticle>', article_start)
        if article_end == -1:
            return None

        article = xml[article_start:article_end]

        # Extrahera fält
        title = extract_xml_value(article, 'ArticleTitle')
        journal = extract_xml_value(article, 'Title')  # Journal title
        year = extract_xml_value(article, 'Year')
        abstract = extract_xml_value(article, 'AbstractText')

        # DOI
        doi_match = re.search(r'<ArticleId IdType="doi">([^<]+)</ArticleId>', article)
        doi = doi_match.group(1) if doi_match else ""

        # Författare (förenklas till första författare)
        author_match = re.search(r'<LastName>([^<]+)</LastName>', article)
        authors = f"{author_match.group(1)} et al." if author_match else ""

        return PubMedReference(
            pmid=pmid,
            title=title[:500] if title else "",
            authors=authors,
            journal=journal[:100] if journal else "",
            year=year,
            doi=doi,
            abstract=abstract[:1000] if abstract else ""
        )

    except Exception as e:
        print(f"  Error parsing PMID {pmid}: {e}")
        return None

def extract_xml_value(xml: str, tag: str) -> str:
    """Extrahera värde mellan XML-taggar."""
    pattern = f'<{tag}[^>]*>([^<]*)</{tag}>'
    match = re.search(pattern, xml)
    return match.group(1) if match else ""

def fetch_snp_info(rsid: str) -> Optional[dict]:
    """Hämta SNP-information från dbSNP."""
    params = {
        'db': 'snp',
        'term': rsid,
        'retmode': 'json'
    }

    url = f"{NCBI_BASE_URL}/esearch.fcgi?{urlencode(params)}"
    time.sleep(RATE_LIMIT_DELAY)

    response = make_request(url)
    if not response:
        return None

    try:
        data = json.loads(response)
        id_list = data.get('esearchresult', {}).get('idlist', [])

        if id_list:
            # Hämta summary
            summary_url = f"{NCBI_BASE_URL}/esummary.fcgi?db=snp&id={id_list[0]}&retmode=json"
            time.sleep(RATE_LIMIT_DELAY)

            summary_response = make_request(summary_url)
            if summary_response:
                summary_data = json.loads(summary_response)
                return summary_data.get('result', {}).get(id_list[0], {})
    except:
        pass

    return None

# =============================================================================
# FETCH FUNCTIONS
# =============================================================================

def fetch_snp_data(rsid: str, category: str = "") -> Optional[SNPData]:
    """Hämta komplett data för en SNP."""
    print(f"  Hämtar {rsid}...", flush=True)

    # Hämta SNP-info från dbSNP
    snp_info = fetch_snp_info(rsid)

    gene = ""
    chromosome = ""
    position = 0
    ref_allele = ""
    alt_allele = ""
    function = ""
    clinical_sig = ""
    maf = 0.0

    if snp_info:
        gene = snp_info.get('genes', [{}])[0].get('name', '') if snp_info.get('genes') else ''
        chromosome = snp_info.get('chr', '')
        chrpos = snp_info.get('chrpos', '') or ''
        if ':' in str(chrpos):
            position = int(str(chrpos).split(':')[1])
        else:
            position = int(chrpos) if chrpos else 0

        # Alleler
        alleles = snp_info.get('docsum', '').split('>')
        if len(alleles) > 1:
            ref_allele = alleles[0][-1] if alleles[0] else ''
            alt_allele = alleles[1][0] if len(alleles[1]) > 0 else ''

        # Funktion
        fxn = snp_info.get('fxn_class', '')
        function = fxn if fxn else "unknown"

        # MAF
        maf = float(snp_info.get('global_maf', {}).get('freq', 0) or 0)

    # Sök efter relaterade PubMed-artiklar
    search_terms = [
        f"{rsid} polymorphism",
        f"{rsid} nutrigenomics" if category else f"{rsid} genetics",
        f"{rsid} supplementation" if "vitamin" in category.lower() else f"{rsid} health"
    ]

    all_pmids = set()
    for term in search_terms[:2]:  # Begränsa antal sökningar
        pmids = search_pubmed(term, 5)
        all_pmids.update(pmids)

    references = fetch_pubmed_details(list(all_pmids)[:10])

    # Generera klinisk signifikans från första referensen
    if references:
        clinical_sig = references[0].title[:200]
    else:
        clinical_sig = f"Genetisk variant i {gene}" if gene else "Genetisk variant"

    return SNPData(
        rsid=rsid,
        gene=gene,
        chromosome=chromosome,
        position=position,
        ref_allele=ref_allele,
        alt_allele=alt_allele,
        function=function,
        clinical_significance=clinical_sig,
        maf_global=maf,
        references=references,
        fetch_date=datetime.now().isoformat()
    )

def fetch_category(category_name: str) -> Optional[CategoryData]:
    """Hämta all data för en kategori."""
    if category_name not in WELLNESS_SNPS:
        print(f"Okänd kategori: {category_name}")
        return None

    cat_info = WELLNESS_SNPS[category_name]
    print(f"\n{'='*60}")
    print(f"Hämtar kategori: {category_name.upper()}")
    print(f"Beskrivning: {cat_info['description']}")
    print(f"Antal SNPs: {len(cat_info['snps'])}")
    print(f"{'='*60}")

    snps_data = []
    for i, rsid in enumerate(cat_info['snps'], 1):
        snp_data = fetch_snp_data(rsid, category_name)
        if snp_data:
            snps_data.append(snp_data)
            print(f"    ✓ {rsid} klar ({i}/{len(cat_info['snps'])})", flush=True)
        else:
            print(f"    ✗ {rsid} misslyckades ({i}/{len(cat_info['snps'])})", flush=True)

    total_refs = sum(len(s.references) for s in snps_data)

    return CategoryData(
        category=category_name,
        description=cat_info['description'],
        snps=snps_data,
        total_references=total_refs,
        fetch_date=datetime.now().isoformat()
    )

def fetch_all_categories() -> Dict[str, CategoryData]:
    """Hämta data för alla kategorier."""
    all_data = {}

    for category_name in WELLNESS_SNPS.keys():
        cat_data = fetch_category(category_name)
        if cat_data:
            all_data[category_name] = cat_data

    return all_data

# =============================================================================
# EXPORT FUNCTIONS
# =============================================================================

def export_to_json(data: Dict, filename: str):
    """Exportera data till JSON-fil."""
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Konvertera dataclasses till dicts
    def convert(obj):
        if hasattr(obj, '__dataclass_fields__'):
            return asdict(obj)
        elif isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(i) for i in obj]
        return obj

    export_data = convert(data)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"\nExporterat till: {filepath}")

def export_to_python_module(data: Dict[str, CategoryData], filename: str):
    """Exportera data som Python-modul."""
    filepath = os.path.join(OUTPUT_DIR, filename)

    lines = [
        '"""',
        'GWL Auto-Generated Gene Data',
        f'Generated: {datetime.now().isoformat()}',
        '',
        'This file was automatically generated by gwl_master_fetcher.py',
        'Do not edit manually - rerun the fetcher to update.',
        '"""',
        '',
        'FETCHED_GENE_DATA = {'
    ]

    for cat_name, cat_data in data.items():
        lines.append(f'    "{cat_name}": {{')
        lines.append(f'        "description": "{cat_data.description}",')
        lines.append(f'        "fetch_date": "{cat_data.fetch_date}",')
        lines.append(f'        "snps": {{')

        for snp in cat_data.snps:
            lines.append(f'            "{snp.rsid}": {{')
            lines.append(f'                "gene": "{snp.gene}",')
            lines.append(f'                "chromosome": "{snp.chromosome}",')
            lines.append(f'                "position": {snp.position},')
            lines.append(f'                "ref_allele": "{snp.ref_allele}",')
            lines.append(f'                "alt_allele": "{snp.alt_allele}",')
            lines.append(f'                "function": "{snp.function}",')
            lines.append(f'                "maf_global": {snp.maf_global},')

            # Referenser
            lines.append(f'                "references": [')
            for ref in snp.references[:3]:  # Max 3 referenser per SNP
                title_escaped = ref.title.replace('"', '\\"').replace('\n', ' ')
                lines.append(f'                    {{"pmid": "{ref.pmid}", "title": "{title_escaped[:100]}..."}},')
            lines.append(f'                ],')
            lines.append(f'            }},')

        lines.append(f'        }}')
        lines.append(f'    }},')

    lines.append('}')
    lines.append('')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Exporterat Python-modul till: {filepath}")

def generate_summary_report(data: Dict[str, CategoryData]) -> str:
    """Generera sammanfattningsrapport."""
    lines = [
        "=" * 70,
        "GWL MASTER FETCHER - SAMMANFATTNING",
        f"Körd: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 70,
        ""
    ]

    total_snps = 0
    total_refs = 0

    for cat_name, cat_data in data.items():
        lines.append(f"\n{cat_name.upper()}")
        lines.append(f"  Beskrivning: {cat_data.description}")
        lines.append(f"  Antal SNPs: {len(cat_data.snps)}")
        lines.append(f"  Referenser: {cat_data.total_references}")

        total_snps += len(cat_data.snps)
        total_refs += cat_data.total_references

        for snp in cat_data.snps:
            gene_info = f" ({snp.gene})" if snp.gene else ""
            refs_info = f", {len(snp.references)} refs" if snp.references else ""
            lines.append(f"    - {snp.rsid}{gene_info}{refs_info}")

    lines.append("")
    lines.append("=" * 70)
    lines.append(f"TOTALT: {total_snps} SNPs, {total_refs} referenser")
    lines.append("=" * 70)

    return '\n'.join(lines)

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='GWL Master Fetcher - Hämta genetisk data')

    parser.add_argument('--all', action='store_true', help='Hämta alla kategorier')
    parser.add_argument('--category', '-c', type=str, help='Hämta specifik kategori')
    parser.add_argument('--snp', '-s', type=str, help='Hämta specifik SNP (rsid)')
    parser.add_argument('--list', '-l', action='store_true', help='Lista alla kategorier')
    parser.add_argument('--output', '-o', type=str, default='gwl_fetched_data', help='Output-filnamn (utan extension)')
    parser.add_argument('--format', '-f', type=str, choices=['json', 'python', 'both'], default='both', help='Output-format')

    args = parser.parse_args()

    print("=" * 70)
    print("GWL MASTER FETCHER")
    print("Genetic Wellness Labs - Nutrigenomics Data Fetcher")
    print("=" * 70)

    if args.list:
        print("\nTillgängliga kategorier:")
        for cat_name, cat_info in WELLNESS_SNPS.items():
            print(f"  {cat_name}: {cat_info['description']} ({len(cat_info['snps'])} SNPs)")

        total_snps = sum(len(c['snps']) for c in WELLNESS_SNPS.values())
        print(f"\nTotalt: {len(WELLNESS_SNPS)} kategorier, {total_snps} SNPs")
        return

    if args.snp:
        print(f"\nHämtar data för SNP: {args.snp}")
        snp_data = fetch_snp_data(args.snp)
        if snp_data:
            print(f"\nResultat:")
            print(f"  Gen: {snp_data.gene}")
            print(f"  Kromosom: {snp_data.chromosome}")
            print(f"  Position: {snp_data.position}")
            print(f"  Ref/Alt: {snp_data.ref_allele}/{snp_data.alt_allele}")
            print(f"  MAF: {snp_data.maf_global}")
            print(f"  Referenser: {len(snp_data.references)}")

            if args.format in ['json', 'both']:
                export_to_json({'snp': snp_data}, f"{args.output}_{args.snp}.json")
        return

    if args.category:
        if args.category not in WELLNESS_SNPS:
            print(f"Okänd kategori: {args.category}")
            print("Använd --list för att se tillgängliga kategorier")
            return

        cat_data = fetch_category(args.category)
        if cat_data:
            data = {args.category: cat_data}
            report = generate_summary_report(data)
            print(report)

            if args.format in ['json', 'both']:
                export_to_json(data, f"{args.output}_{args.category}.json")
            if args.format in ['python', 'both']:
                export_to_python_module(data, f"{args.output}_{args.category}.py")
        return

    if args.all:
        print("\nHämtar ALLA kategorier...")
        print(f"Detta kan ta {len(WELLNESS_SNPS) * 2}-{len(WELLNESS_SNPS) * 5} minuter.")

        all_data = fetch_all_categories()

        report = generate_summary_report(all_data)
        print(report)

        if args.format in ['json', 'both']:
            export_to_json(all_data, f"{args.output}_complete.json")
        if args.format in ['python', 'both']:
            export_to_python_module(all_data, f"{args.output}_complete.py")

        # Spara rapport
        report_path = os.path.join(OUTPUT_DIR, f"{args.output}_report.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nRapport sparad: {report_path}")

        return

    # Default: visa hjälp
    parser.print_help()
    print("\nExempel:")
    print("  python gwl_master_fetcher.py --list")
    print("  python gwl_master_fetcher.py --category methylation")
    print("  python gwl_master_fetcher.py --snp rs1801133")
    print("  python gwl_master_fetcher.py --all")

if __name__ == "__main__":
    main()
