#!/usr/bin/env python3
"""
GWL Transport Pathways & Nutrient Interactions
================================================

Hanterar:
1. Transportvägar som delas av flera näringsämnen (konkurrens)
2. Absorption antagonism (zinkvs koppar, kalcium vs magnesium)
3. Synergistiska kombinationer
4. Timing-rekommendationer
5. Gen-näringsämne-interaktioner
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum

class InteractionType(Enum):
    COMPETITION = "konkurrens"          # Tävlar om samma väg
    ANTAGONISM = "antagonism"           # Motverkar varandra
    SYNERGY = "synergi"                 # Förstärker varandra
    DEPENDENCY = "beroende"             # En kräver den andra
    DEPLETION = "utarmning"             # En förbrukar den andra

class TransportSystem(Enum):
    # Mineraltransport
    DMT1 = "DMT1 (Divalent Metal Transporter 1)"  # Fe, Mn, Co, Zn, Cu, Cd
    ZIP_FAMILY = "ZIP transportörer (zink)"
    CALCIUM_CHANNELS = "Kalciumkanaler (TRPV5/6)"
    SODIUM_DEPENDENT = "Natriumberoende transport"

    # Vitamintransport
    CUBILIN_AMNIONLESS = "Cubilin-Amnionless (B12)"
    RFC = "Reduced Folate Carrier (folat)"
    SVCT = "SVCT (C-vitamin)"
    SCARB1 = "SR-B1 (E-vitamin, karotenoider)"

    # Fettlösliga
    BILE_DEPENDENT = "Gallsaltsberoende (ADEK)"
    CHYLOMICRON = "Kylomikronvägen"

    # Aminosyror
    LAT = "LAT (Large Amino Acid Transporter)"
    B0AT = "B0AT (neutral aminosyra)"

@dataclass
class TransportCompetition:
    """Konkurrens om samma transportväg"""
    transport_system: TransportSystem
    competing_nutrients: List[str]
    winner_at_high_dose: str
    clinical_significance: str
    recommendation: str

@dataclass
class NutrientInteraction:
    """Interaktion mellan två näringsämnen"""
    nutrient_a: str
    nutrient_b: str
    interaction_type: InteractionType
    mechanism: str
    effect: str
    recommendation: str
    timing_advice: str
    references: List[str]

@dataclass
class GeneNutrientInteraction:
    """Hur en gen påverkar ett näringsämnes metabolism"""
    gene: str
    rsid: str
    nutrient: str
    mechanism: str
    effect_by_genotype: Dict[str, str]
    recommendation_by_genotype: Dict[str, str]

# =============================================================================
# TRANSPORTVÄGSKONKURRENS
# =============================================================================

TRANSPORT_COMPETITIONS: List[TransportCompetition] = [
    TransportCompetition(
        transport_system=TransportSystem.DMT1,
        competing_nutrients=["Järn (Fe2+)", "Zink", "Mangan", "Kobolt", "Koppar", "Kadmium"],
        winner_at_high_dose="Järn dominerar vid höga doser",
        clinical_significance="""
DMT1 är huvudtransportören för tvåvärda metaller i tarmen.
Vid högt järnintag minskar absorption av zink, mangan och koppar.
Detta är kliniskt relevant vid järntillskott.
        """,
        recommendation="""
- Ta inte järn och zink samtidigt
- Separera med minst 2-3 timmar
- Om båda behövs: järn på morgonen, zink på kvällen
- Vid järntillskott: övervaka zinkstatus
        """
    ),

    TransportCompetition(
        transport_system=TransportSystem.CALCIUM_CHANNELS,
        competing_nutrients=["Kalcium", "Magnesium", "Zink", "Järn"],
        winner_at_high_dose="Kalcium dominerar",
        clinical_significance="""
Högt kalciumintag (>500mg på en gång) minskar absorption av:
- Magnesium: 50% reduktion möjlig
- Zink: 30-50% reduktion
- Järn: signifikant reduktion (non-hem järn)
        """,
        recommendation="""
- Dela upp kalciumintag (max 500mg per tillfälle)
- Ta magnesium separat från kalcium
- Optimal ratio Mg:Ca = 1:1 till 1:2
- Ta järn med C-vitamin, separat från kalcium
        """
    ),

    TransportCompetition(
        transport_system=TransportSystem.ZIP_FAMILY,
        competing_nutrients=["Zink", "Koppar", "Järn"],
        winner_at_high_dose="Zink dominerar, blockerar koppar",
        clinical_significance="""
Höga zinkdoser (>50mg/dag) kan orsaka kopparbrist.
Zink inducerar metallotionein som binder koppar i tarmceller.
Vid långvarig högdos-zink: risk för kopparbristanemi.
        """,
        recommendation="""
- Vid zink >25mg/dag: överväg koppartillskott (1-2mg)
- Optimal Zn:Cu ratio = 8:1 till 15:1
- Monitorera blodstatus vid långvarig zinkbehandling
        """
    ),

    TransportCompetition(
        transport_system=TransportSystem.SCARB1,
        competing_nutrients=["Vitamin E", "Betakaroten", "Lykopen", "Lutein", "Astaxantin"],
        winner_at_high_dose="Varierar - alla konkurrerar",
        clinical_significance="""
Alla fettlösliga antioxidanter och karotenoider delar SR-B1.
Höga doser av en karotenoid minskar absorption av andra.
T.ex. högt betakarotenintag minskar lykopenabsorption.
        """,
        recommendation="""
- Ta inte megadoser av enskilda karotenoider
- Kombinera olika karotenoider i måttliga doser
- Bäst: bred spektrum från varierad kost
        """
    ),

    TransportCompetition(
        transport_system=TransportSystem.LAT,
        competing_nutrients=["Fenylalanin", "Tyrosin", "Tryptofan", "Leucin", "Isoleucin", "Valin", "L-DOPA"],
        winner_at_high_dose="BCAA (leucin, isoleucin, valin) dominerar",
        clinical_significance="""
BCAA konkurrerar med tryptofan om transport över blod-hjärnbarriären.
Högt BCAA-intag (t.ex. efter träning) minskar tryptofanupptag i hjärnan.
Relevant för serotoninsyntes och humör.
        """,
        recommendation="""
- Om tryptofan/5-HTP för sömn/humör: ta separat från BCAA
- BCAA bäst direkt efter träning
- Tryptofan/5-HTP bäst på kvällen med kolhydrater
        """
    ),

    TransportCompetition(
        transport_system=TransportSystem.RFC,
        competing_nutrients=["Folat", "Metylfolat", "Metotrexat"],
        winner_at_high_dose="Metotrexat blockerar folat",
        clinical_significance="""
Metotrexat (MTX) använder samma transportör som folat.
Vid MTX-behandling blir folatupptag blockerat - avsiktligt vid cancer,
men ger biverkningar som kräver folinsyra-rescue.
        """,
        recommendation="""
- Vid MTX-behandling: följ läkarens folsyra/folinsyraprotokoll
- MTHFR-bärare på lågdos MTX (RA): diskutera metylfolat med läkare
        """
    ),
]

# =============================================================================
# NÄRINGSÄMNESINTERAKTIONER
# =============================================================================

NUTRIENT_INTERACTIONS: List[NutrientInteraction] = [

    # --- SYNERGIER ---
    NutrientInteraction(
        nutrient_a="Vitamin D",
        nutrient_b="Vitamin K2",
        interaction_type=InteractionType.SYNERGY,
        mechanism="D-vitamin ökar kalciumabsorption, K2 aktiverar osteocalcin och MGP som dirigerar kalcium till ben och bort från artärer",
        effect="Bättre benhälsa, mindre artärförkalkning, säkrare högdos D-vitamin",
        recommendation="Ta alltid K2 (100-200mcg MK-7) med D-vitamin >2000 IE/dag",
        timing_advice="Kan tas tillsammans med fetrik måltid",
        references=["Masterjohn C. Vitamin D toxicity redefined. Med Hypotheses. 2007"]
    ),

    NutrientInteraction(
        nutrient_a="Vitamin D",
        nutrient_b="Magnesium",
        interaction_type=InteractionType.DEPENDENCY,
        mechanism="Magnesium krävs för: 1) D-vitaminaktivering i lever och njure, 2) Transport av D-vitamin i blodet, 3) PTH-reglering",
        effect="Utan tillräckligt Mg kan D-vitamin inte aktiveras effektivt",
        recommendation="Säkerställ Mg-status (300-400mg/dag) innan/under D-vitaminsupplementering",
        timing_advice="Mg på kvällen, D-vitamin med måltid",
        references=["Uwitonze AM. Role of Magnesium in Vitamin D Activation. J Am Osteopath Assoc. 2018"]
    ),

    NutrientInteraction(
        nutrient_a="Vitamin C",
        nutrient_b="Järn (non-hem)",
        interaction_type=InteractionType.SYNERGY,
        mechanism="C-vitamin reducerar Fe3+ till Fe2+ (DMT1 transporterar endast Fe2+), plus bildar lösligt komplex",
        effect="2-6x ökad järnabsorption från växtbaserade källor",
        recommendation="Ta 50-100mg C-vitamin med järnrik måltid eller järntillskott",
        timing_advice="Samtidigt för maximal effekt",
        references=["Hallberg L. Iron absorption from typical meals. Am J Clin Nutr. 1979"]
    ),

    NutrientInteraction(
        nutrient_a="Omega-3",
        nutrient_b="Vitamin E",
        interaction_type=InteractionType.SYNERGY,
        mechanism="E-vitamin skyddar omega-3 från lipidperoxidation (oxidation)",
        effect="Bevarar omega-3-integritet, minskar oxidativ stress från omega-3-intag",
        recommendation="Kvalitetsfiskolja innehåller ofta E-vitamin. Annars: 15-30 IE E-vitamin per 1000mg omega-3",
        timing_advice="Tillsammans",
        references=["Meydani M. Vitamin E requirement in relation to omega-3 intake. Nutr Rev. 1992"]
    ),

    NutrientInteraction(
        nutrient_a="B12",
        nutrient_b="Folat",
        interaction_type=InteractionType.DEPENDENCY,
        mechanism="B12 behövs för att 'fånga' folat inuti cellen (metylfolat trap). Utan B12 fastnar folat som metylTHF",
        effect="B12-brist kan maskeras av folattillskott (anemin förbättras men neurologisk skada fortsätter)",
        recommendation="Kontrollera alltid B12-status innan folattillskott. Supplementera båda om osäkert.",
        timing_advice="Kan tas tillsammans",
        references=["Smith AD. Folate-vitamin B12 interactions. Adv Nutr. 2016"]
    ),

    NutrientInteraction(
        nutrient_a="Zink",
        nutrient_b="Vitamin A",
        interaction_type=InteractionType.DEPENDENCY,
        mechanism="Zink krävs för: 1) Syntes av retinolbindande protein (RBP), 2) Omvandling av retinol till retinal (syn)",
        effect="Zinkbrist ger funktionell A-vitaminbrist även vid normala A-vitaminnivåer",
        recommendation="Säkerställ zinkstatus vid A-vitaminbrist som inte svarar på tillskott",
        timing_advice="Separat (zink kvällen, A-vitamin med fettrik måltid)",
        references=["Christian P. Interactions between zinc and vitamin A. Am J Clin Nutr. 1998"]
    ),

    NutrientInteraction(
        nutrient_a="L-teanin",
        nutrient_b="Koffein",
        interaction_type=InteractionType.SYNERGY,
        mechanism="L-teanin ökar alfavågor och dämpar koffeins stimulerande effekter på jitter/ångest. Koffein ökar alertness.",
        effect="'Flow-state': fokuserad vakenhet utan nervositet. Bättre än endera ensamt.",
        recommendation="100-200mg L-teanin + 50-100mg koffein. Ratio 1:1 till 2:1.",
        timing_advice="Tillsammans på morgonen/förmiddagen",
        references=["Owen GN. L-theanine and caffeine combination. Nutr Neurosci. 2008"]
    ),

    # --- ANTAGONISM ---
    NutrientInteraction(
        nutrient_a="Kalcium",
        nutrient_b="Järn",
        interaction_type=InteractionType.ANTAGONISM,
        mechanism="Kalcium hämmar både hem- och non-hemjärnabsorption via okänd mekanism (inte bara DMT1)",
        effect="300mg kalcium minskar järnabsorption med 50-60%",
        recommendation="Ta järn och kalcium vid olika måltider. Minst 2 timmars separation.",
        timing_advice="Kalcium: middag/kväll. Järn: morgon på fastande eller med C-vitamin.",
        references=["Hallberg L. Calcium and iron absorption. Am J Clin Nutr. 1991"]
    ),

    NutrientInteraction(
        nutrient_a="Zink",
        nutrient_b="Koppar",
        interaction_type=InteractionType.ANTAGONISM,
        mechanism="Höga zinkdoser inducerar metallotionein i tarmceller som binder koppar och förhindrar absorption",
        effect=">50mg zink/dag kan orsaka kopparbrist (anemi, neutropeni)",
        recommendation="Vid zink >25mg/dag långvarigt: överväg 1-2mg koppar. Ratio Zn:Cu = 10:1",
        timing_advice="Om båda supplementeras: ta separat (minst 2h)",
        references=["Prasad AS. Zinc-induced copper deficiency. Ann Intern Med. 1978"]
    ),

    NutrientInteraction(
        nutrient_a="Kalcium",
        nutrient_b="Magnesium",
        interaction_type=InteractionType.COMPETITION,
        mechanism="Delar delvis absorptionsvägar. Högt Ca:Mg ratio (>2:1) minskar Mg-absorption och ökar Mg-utsöndring.",
        effect="Högt kalciumintag utan magnesium kan förvärra Mg-brist",
        recommendation="Håll Ca:Mg ratio 1:1 till 2:1. Många behöver mer Mg, inte Ca.",
        timing_advice="Ta separat - Ca med mat, Mg på kvällen",
        references=["Rosanoff A. Suboptimal magnesium status in the United States. Nutr Rev. 2012"]
    ),

    NutrientInteraction(
        nutrient_a="Vitamin A (hög dos)",
        nutrient_b="Vitamin D",
        interaction_type=InteractionType.ANTAGONISM,
        mechanism="Retinsyra och kalcitriol konkurrerar om RXR-receptorn för gentranskription",
        effect="Höga doser retinol (>10,000 IE/dag) kan motverka D-vitamins effekter på skelett",
        recommendation="Undvik megadoser A-vitamin (>10,000 IE) om D-vitamin är prioriterat",
        timing_advice="Måttliga doser av båda kan tas samma dag",
        references=["Johansson S. Vitamin A antagonizes vitamin D action. Eur J Nutr. 2002"]
    ),

    # --- DEPLETION ---
    NutrientInteraction(
        nutrient_a="Alkohol",
        nutrient_b="B-vitaminer (B1, B6, B12, folat)",
        interaction_type=InteractionType.DEPLETION,
        mechanism="Alkohol: 1) Minskar absorption, 2) Ökar urinförlust, 3) Stör aktivering, 4) Skadar lever (lagring)",
        effect="Kronisk alkoholkonsumtion leder till B-vitaminbrist, särskilt B1 (Wernicke-Korsakoff)",
        recommendation="Vid regelbunden alkohol: B-komplextillskott. Tiamin (B1) särskilt viktigt.",
        timing_advice="B-vitaminer på morgonen, inte vid alkoholintag",
        references=["Martin PR. The role of thiamine deficiency in alcoholic brain disease. Alcohol Res Health. 2003"]
    ),

    NutrientInteraction(
        nutrient_a="PPI (omeprazol etc)",
        nutrient_b="Magnesium, B12, Kalcium, Järn",
        interaction_type=InteractionType.DEPLETION,
        mechanism="PPI minskar magsyra som behövs för: Mg-absorption, B12-frigörelse från mat, Ca-lösning, Fe-reduktion",
        effect="Långvarig PPI ökar risk för Mg-brist, B12-brist, frakturer (Ca), anemi (Fe)",
        recommendation="Vid >1 års PPI: kontrollera Mg, B12. Överväg tillskott. Kalciumcitrat absorberas bättre utan syra.",
        timing_advice="Tillskott minst 2h före/efter PPI",
        references=["Heidelbaugh JJ. Proton pump inhibitors and risk of nutrient deficiencies. Ther Adv Drug Saf. 2013"]
    ),

    NutrientInteraction(
        nutrient_a="Metformin",
        nutrient_b="Vitamin B12",
        interaction_type=InteractionType.DEPLETION,
        mechanism="Metformin stör kalciumberoende B12-IF-komplex-absorption i ileum",
        effect="10-30% av metforminanvändare utvecklar B12-brist över tid",
        recommendation="Vid metformin: kontrollera B12 årligen. Supplementera vid brist eller gränsvärden.",
        timing_advice="B12 sublingualt (undviker absorptionsproblem) eller separat från metformin",
        references=["Aroda VR. Long-term metformin use and vitamin B12 deficiency. J Clin Endocrinol Metab. 2016"]
    ),

    NutrientInteraction(
        nutrient_a="Koffein",
        nutrient_b="Kalcium, Järn, Magnesium",
        interaction_type=InteractionType.DEPLETION,
        mechanism="Koffein: 1) Ökar kalciumutsöndring i urin, 2) Tanninerna i kaffe/te binder järn, 3) Ökar Mg-förlust",
        effect="Högt koffeintag (>400mg) kan bidra till mineral depletion",
        recommendation="Begränsa kaffe/te till mellan måltider. Vänta 1h efter måltid innan kaffe.",
        timing_advice="Kaffe: 9-11 och 13-17 (bäst för kortisol). Inte med måltider.",
        references=["Massey LK. Caffeine and bone loss. J Am Coll Nutr. 2001"]
    ),
]

# =============================================================================
# GEN-NÄRINGSÄMNE-INTERAKTIONER
# =============================================================================

GENE_NUTRIENT_INTERACTIONS: List[GeneNutrientInteraction] = [

    GeneNutrientInteraction(
        gene="MTHFR",
        rsid="rs1801133",
        nutrient="Folat",
        mechanism="MTHFR omvandlar folat till aktiv metylfolat (5-MTHF). C677T-mutationen reducerar enzymaktivitet.",
        effect_by_genotype={
            "GG (CC)": "100% enzymaktivitet. Normal folatmetabolism.",
            "AG (CT)": "~65% enzymaktivitet. Kan använda vanlig folat men metylfolat fördelaktigt.",
            "AA (TT)": "~30% enzymaktivitet. Signifikant nedsatt. Kräver metylfolat.",
        },
        recommendation_by_genotype={
            "GG (CC)": "Folsyra eller metylfolat fungerar. 400-800 mcg/dag.",
            "AG (CT)": "Metylfolat fördelaktigt. 400-800 mcg/dag.",
            "AA (TT)": "ENDAST metylfolat (5-MTHF). Undvik folsyra (kan ackumuleras). 800-1000 mcg/dag. Kontrollera homocystein.",
        }
    ),

    GeneNutrientInteraction(
        gene="FADS1",
        rsid="rs174546",
        nutrient="Omega-3 (ALA, EPA, DHA)",
        mechanism="FADS1 kodar delta-5-desaturas som omvandlar DGLA→AA och EPA→DHA. T-allelen ger reducerad aktivitet.",
        effect_by_genotype={
            "CC": "Effektiv ALA→EPA→DHA-omvandling (~15% konvertering).",
            "CT": "Reducerad omvandling (~8-10% konvertering).",
            "TT": "Kraftigt reducerad omvandling (~3-5% konvertering).",
        },
        recommendation_by_genotype={
            "CC": "Växtbaserad omega-3 (ALA) kan delvis räcka. Ändå rekommenderas marin omega-3.",
            "CT": "Marin omega-3 (fisk/alg) nödvändigt. 1000-2000 mg EPA+DHA/dag.",
            "TT": "ALA (linfrö) nästan värdelöst. MÅSTE ha EPA/DHA direkt. 1500-3000 mg/dag.",
        }
    ),

    GeneNutrientInteraction(
        gene="BCMO1",
        rsid="rs7501331",
        nutrient="Vitamin A (betakaroten vs retinol)",
        mechanism="BCMO1 klyver betakaroten till retinal. T-allelen ger 32-69% reducerad aktivitet.",
        effect_by_genotype={
            "CC": "Effektiv betakaroten→retinol-omvandling.",
            "CT": "32% reducerad omvandling.",
            "TT": "69% reducerad omvandling.",
        },
        recommendation_by_genotype={
            "CC": "Betakaroten från morötter etc räcker för A-vitaminbehov.",
            "CT": "Inkludera animaliska A-vitaminkällor (lever, ägg, mejeriprodukter).",
            "TT": "Betakaroten räcker INTE. MÅSTE ha preformerad retinol. Retinol 2500-5000 IE/dag eller lever 1-2ggr/månad.",
        }
    ),

    GeneNutrientInteraction(
        gene="VDR",
        rsid="rs2228570",
        nutrient="Vitamin D",
        mechanism="VDR FokI påverkar D-vitaminreceptorns längd och aktivitet. T-allelen (f) ger längre, mindre aktiv receptor.",
        effect_by_genotype={
            "CC": "Kort, aktiv VDR. Normal D-vitaminrespons.",
            "CT": "Intermediär respons.",
            "TT": "Lång, mindre aktiv VDR. Sämre cellulär respons.",
        },
        recommendation_by_genotype={
            "CC": "Standard D-vitamindosering (1000-2000 IE/dag).",
            "CT": "Standard till lätt förhöjd (1000-3000 IE/dag).",
            "TT": "Kan behöva 25-50% högre dos för samma serumnivåer. Sikta på 75-100 nmol/L. 2000-4000 IE/dag.",
        }
    ),

    GeneNutrientInteraction(
        gene="COMT",
        rsid="rs4680",
        nutrient="Magnesium, L-teanin, Koffein",
        mechanism="COMT bryter ned dopamin/noradrenalin. Met/Met (AA) = långsam, Val/Val (GG) = snabb.",
        effect_by_genotype={
            "GG (Val/Val)": "Snabb COMT. Katekolaminer bryts ned snabbt. Stresstolerant men kan behöva stimulans.",
            "AG (Val/Met)": "Balanserad COMT. Flexibel.",
            "AA (Met/Met)": "Långsam COMT. Höga dopaminnivåer. Bra fokus men stresskänslig.",
        },
        recommendation_by_genotype={
            "GG (Val/Val)": "Tolererar koffein väl. Kan behöva mer stimulans för optimal funktion.",
            "AG (Val/Met)": "Måttligt koffeinintag (200-300 mg). Standard Mg (300-400 mg).",
            "AA (Met/Met)": "BEGRÄNSA koffein (max 100-200 mg). ÖKAT Mg-behov (400-600 mg). L-teanin (200-400 mg) mycket fördelaktigt för stresshantering.",
        }
    ),

    GeneNutrientInteraction(
        gene="CYP1A2",
        rsid="rs762551",
        nutrient="Koffein",
        mechanism="CYP1A2 metaboliserar ~95% av koffein. AA = snabb (2-4h halveringstid), AC/CC = långsam (6-8h+).",
        effect_by_genotype={
            "AA": "Snabb metaboliserare. Koffein bryts ned på 2-4 timmar.",
            "AC": "Intermediär. Halveringstid ~6 timmar.",
            "CC": "Långsam metaboliserare. Halveringstid 8+ timmar.",
        },
        recommendation_by_genotype={
            "AA": "Upp till 400 mg koffein/dag tolereras. Kan dricka kaffe till sen eftermiddag.",
            "AC": "Max 200-300 mg/dag. Undvik koffein efter kl 14.",
            "CC": "Max 100-200 mg/dag. Undvik efter kl 12. Ökad CVD-risk vid >3 koppar/dag.",
        }
    ),

    GeneNutrientInteraction(
        gene="FUT2",
        rsid="rs602662",
        nutrient="Vitamin B12",
        mechanism="FUT2 bestämmer secretor-status som påverkar tarmflora och B12-absorption.",
        effect_by_genotype={
            "GG": "Secretor. Normal tarmflora och B12-absorption.",
            "AG": "Secretor. Normal absorption.",
            "AA": "Non-secretor. Annorlunda tarmflora. ~15% lägre B12-nivåer.",
        },
        recommendation_by_genotype={
            "GG": "Standard B12-källor räcker.",
            "AG": "Standard B12-källor räcker.",
            "AA": "Fokusera extra på B12. Sublingualt metylkobalamin kan vara fördelaktigt (kringgår absorptionsproblem). 500-1000 mcg/dag vid risk.",
        }
    ),

    GeneNutrientInteraction(
        gene="HFE",
        rsid="rs1800562",
        nutrient="Järn",
        mechanism="HFE C282Y orsakar hereditär hemokromatos. Homozygota absorberar för mycket järn.",
        effect_by_genotype={
            "GG": "Normal järnmetabolism.",
            "AG": "Heterozygot bärare. Lätt ökad absorption. Sällan kliniskt signifikant.",
            "AA": "Hemokromatos. 80-90% utvecklar järnöverskott.",
        },
        recommendation_by_genotype={
            "GG": "Standard järnrekommendationer.",
            "AG": "Kontrollera ferritin vart 2-5 år. Undvik järntillskott om inte bristbekräftad.",
            "AA": "UNDVIK järntillskott och berikade livsmedel. Regelbunden ferritin/transferrin-kontroll. Blodgivning kan vara terapeutiskt.",
        }
    ),

    GeneNutrientInteraction(
        gene="TCF7L2",
        rsid="rs7903146",
        nutrient="Kolhydrater, Fiber, Krom, Magnesium",
        mechanism="TCF7L2 påverkar insulinsekretion. T-allelen ger reducerad β-cellsfunktion.",
        effect_by_genotype={
            "CC": "Normal insulinsekretion.",
            "CT": "~1.4x ökad T2D-risk.",
            "TT": "~1.8x ökad T2D-risk.",
        },
        recommendation_by_genotype={
            "CC": "Standardrekommendationer för kolhydrater.",
            "CT": "Begränsa raffinerade kolhydrater. Fokus på fiber (30g+/dag). Överväg krom (200mcg) och extra Mg.",
            "TT": "STRIKT blodsockerkontroll. Lågglykemisk kost. Protein först vid måltid. Krom, Mg, Berberin kan stödja. Regelbunden HbA1c-kontroll.",
        }
    ),
]

# =============================================================================
# HJÄLPFUNKTIONER
# =============================================================================

def get_interactions_for_nutrient(nutrient_name: str) -> List[NutrientInteraction]:
    """Hämta alla interaktioner för ett näringsämne"""
    return [
        i for i in NUTRIENT_INTERACTIONS
        if nutrient_name.lower() in i.nutrient_a.lower() or nutrient_name.lower() in i.nutrient_b.lower()
    ]

def get_transport_competition_for_nutrient(nutrient_name: str) -> List[TransportCompetition]:
    """Hämta transportvägskonkurrens för ett näringsämne"""
    return [
        tc for tc in TRANSPORT_COMPETITIONS
        if any(nutrient_name.lower() in n.lower() for n in tc.competing_nutrients)
    ]

def get_gene_interactions_for_genotypes(genotype_dict: Dict[str, str]) -> List[Tuple[GeneNutrientInteraction, str, str]]:
    """
    Givet en dict med rsid -> genotyp, returnera relevanta gen-näringsinteraktioner

    Returns:
        List av (interaction, genotyp, rekommendation)
    """
    results = []
    for gni in GENE_NUTRIENT_INTERACTIONS:
        if gni.rsid in genotype_dict:
            gt = genotype_dict[gni.rsid]
            # Hitta matchande nyckel
            for key in gni.effect_by_genotype:
                if gt in key or key in gt:
                    effect = gni.effect_by_genotype[key]
                    rec = gni.recommendation_by_genotype[key]
                    results.append((gni, effect, rec))
                    break
    return results

def generate_timing_schedule(supplements: List[str]) -> Dict[str, List[str]]:
    """
    Generera optimalt doseringsschema baserat på interaktioner

    Args:
        supplements: Lista med supplementnamn

    Returns:
        Dict med tidpunkt -> supplements
    """
    schedule = {
        "Morgon (fastande)": [],
        "Morgon (med frukost)": [],
        "Lunch": [],
        "Eftermiddag": [],
        "Middag": [],
        "Kväll (före sömn)": []
    }

    # Enkel logik - kan utökas
    for supp in supplements:
        supp_lower = supp.lower()

        if "järn" in supp_lower or "iron" in supp_lower:
            schedule["Morgon (fastande)"].append(f"{supp} + C-vitamin")
        elif "magnesium" in supp_lower:
            schedule["Kväll (före sömn)"].append(supp)
        elif "d-vitamin" in supp_lower or "vitamin d" in supp_lower:
            schedule["Morgon (med frukost)"].append(supp)
        elif "omega" in supp_lower:
            schedule["Morgon (med frukost)"].append(supp)
            schedule["Middag"].append(f"{supp} (dela dos)")
        elif "zink" in supp_lower:
            schedule["Kväll (före sömn)"].append(supp)
        elif "kalcium" in supp_lower:
            schedule["Lunch"].append(supp)
            schedule["Middag"].append(f"{supp} (dela dos)")
        elif "b-vitamin" in supp_lower or "b12" in supp_lower or "b-complex" in supp_lower:
            schedule["Morgon (med frukost)"].append(supp)
        elif "teanin" in supp_lower:
            schedule["Morgon (med frukost)"].append(f"{supp} (med kaffe)")
            schedule["Kväll (före sömn)"].append(f"{supp} (för sömn)")
        else:
            schedule["Morgon (med frukost)"].append(supp)

    # Ta bort tomma tider
    return {k: v for k, v in schedule.items() if v}


if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("GWL Transport Pathways & Interactions")
    print("=" * 50)
    print(f"\nTransportvags-konkurrenser: {len(TRANSPORT_COMPETITIONS)}")
    print(f"Narings-interaktioner: {len(NUTRIENT_INTERACTIONS)}")
    print(f"Gen-narings-interaktioner: {len(GENE_NUTRIENT_INTERACTIONS)}")

    print("\n\nExempel - interaktioner for Magnesium:")
    for inter in get_interactions_for_nutrient("magnesium"):
        print(f"  {inter.nutrient_a} + {inter.nutrient_b}: {inter.interaction_type.value}")
        print(f"    -> {inter.recommendation}")
