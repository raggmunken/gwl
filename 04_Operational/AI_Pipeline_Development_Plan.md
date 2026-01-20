# AI-PIPELINE UTVECKLINGSPLAN
## Egen AI för DNA → Nutrition Matching

**Datum:** 2026-01-19
**Version:** 1.0
**Owner:** CTO (hire Month 6-9) + Part-time ML Engineer
**Timeline:** Month 3-12 (MVP Month 6, Continuous improvement)

---

## EXECUTIVE SUMMARY

**Vision:** Bygga proprietär AI som automatiskt analyserar DNA-data och genererar personaliserade näringsrekommendationer baserat på:
1. Genotyp (VDR, MTHFR, BCMO1, etc.)
2. Vetenskaplig litteratur (PubMed, GWAS Catalog)
3. Customer outcomes (energy, focus, blood biomarkers)
4. Continuous learning (varje ny kund = träningsdata)

**Competitive Moat:**
- Konkurrenter kan inte kopiera utan data (1,000+ customers = unique dataset)
- AI förbättras automatiskt med varje ny kund
- Kan lansera nya rapporter utan labkostnad (reanalyzera befintlig DNA-data)

**Budget:**
- Core nutrition development: 200K (Year 1) - already allocated
- Add-on development (Sleep, Stress, Workout, Meal): 250K (Year 1)
- ML Engineer: 300K/år (part-time, Year 1-2)
- AWS compute: 50K/år (training + inference)
- **Total Year 1:** 800K (+250K for add-ons)

**ROI:**
- Dietist tid: 60 min → 10 min per kund = **6× efficiency**
- Scalability: 1 dietist can handle 400 customers (vs 160 without AI)
- Quality: Consistent recommendations (no human error)
- Innovation speed: Launch new features faster (workout, sleep, stress)

---

## 1. SYSTEM ARCHITECTURE

### 1.1 Data Flow

```
[Customer DNA Sample]
        ↓
[Lab: DNA Extraction + Genotyping]
        ↓
[VCF File: Raw Genotypes] → [S3 Encrypted Storage]
        ↓
[AI Pipeline: 5 Stages]
        ↓
[Personalized Health Report (Draft)]
        ↓
[Legitimerad Dietist: Review & Approve]
        ↓
[Customer: Final Report + Supplements]
        ↓
[Outcome Tracking: Energy, Focus, Blood Tests]
        ↓
[Feedback Loop: Re-train AI]
```

---

### 1.2 AI Pipeline (5 Stages)

**Stage 1: Genotype Import & QC**
- **Input:** VCF file from lab (650K SNPs from microarray)
- **Process:**
  - Parse VCF → Extract 100 wellness SNPs
  - Quality control (genotype call rate >98%)
  - Flag missing data, low-quality calls
  - Store in PostgreSQL (encrypted)
- **Output:** Clean genotype table (CustomerID, SNP, Genotype)
- **Tech:** Python + Biopython + PyVCF

**Stage 2: Genotype → Phenotype Mapping**
- **Input:** 100 genotypes
- **Process:**
  - Match genotype to known associations
  - Example: VDR Fok1 ff → "40% lower vitamin D absorption"
  - Lookup databases: dbSNP, ClinVar, PharmGKB, GWAS Catalog
  - Calculate polygenic risk scores (e.g., obesity risk from FTO + multiple SNPs)
- **Output:** Phenotype predictions (Vitamin D absorption: LOW, Folate metabolism: IMPAIRED, etc.)
- **Tech:** Python + Pandas + custom lookup tables

**Stage 3: Evidence-Based Recommendations**
- **Input:** Phenotype predictions
- **Process:**
  - Generate supplement recommendations
  - Example: VDR Fok1 ff + Low D-vitamin → "Recommend 4,000 IU vitamin D3 (vs 2,000 IU standard)"
  - Dose adjustments based on genotype
  - Interaction checks (e.g., high-dose B12 if MTHFR + high homocysteine)
  - Map to 10 standardized formulas
- **Output:** Supplement formula (Formula #3: High D-vitamin, Methylfolate, B12, Omega-3)
- **Tech:** Rule-based engine + ML (for complex interactions)

**Stage 4: Report Generation**
- **Input:** Recommendations + Genotypes
- **Process:**
  - Generate PDF report (LaTeX or Jinja2 templates)
  - Visualizations (gene cards, risk scores)
  - Explanations in plain Swedish
  - Disclaimers ("Not medical advice, consult doctor")
- **Output:** Draft PDF report (25-30 pages)
- **Tech:** Python + ReportLab / LaTeX + Jinja2

**Stage 5: Dietist Review & Approval**
- **Input:** Draft report
- **Process:**
  - Legitimerad dietist reviews AI recommendations
  - Checks for errors, edge cases
  - Can override recommendations (manual adjustments)
  - Approves final report
- **Output:** Final approved report
- **Tech:** Web UI (React) for dietist review interface
- **Time:** 10-15 min per customer (vs 60 min manual)

---

### 1.3 Continuous Learning Loop

**Feedback Data:**
1. **Subjective Outcomes (Self-Reported)**
   - Energy levels (1-10 scale, weekly)
   - Focus & mental clarity (1-10 scale, weekly)
   - Sleep quality (1-10 scale, weekly)
   - Collected via app/email

2. **Objective Outcomes (Blood Tests)**
   - D-vitamin levels (before/after 3 months)
   - Folat (before/after)
   - Homocysteine (before/after)
   - CRP (inflammation marker)
   - Collected via Werlabs integration

3. **Retention Data**
   - Did customer stay subscribed? (churn = bad outcomes?)
   - Did customer upgrade tier? (good outcomes)

**Re-Training:**
- **Frequency:** Quarterly (every 3 months)
- **Process:**
  - Collect all outcome data (n=650 customers Year 1)
  - Re-train ML models (XGBoost, Random Forest)
  - Validate: Do new models predict outcomes better?
  - Deploy: A/B test new model vs old model (50/50 split)
  - Roll out: If new model performs better, replace old
- **Tech:** MLflow (experiment tracking) + AWS SageMaker (training)

**Example Insights:**
- "Customers with MTHFR C677T TT + methylfolate saw 35% improvement in homocysteine (vs 20% with folic acid)"
- "VDR Fok1 ff customers need 5,000 IU vitamin D (not 4,000 IU) for optimal levels"
- "APOE4 carriers respond better to higher EPA/DHA doses (2,000 mg vs 1,000 mg)"

---

## 2. TECHNOLOGY STACK

### 2.1 Core Technologies

**Backend:**
- **Language:** Python 3.11+
- **Framework:** FastAPI (REST API for pipeline)
- **Database:** PostgreSQL (encrypted, AWS RDS)
- **Queue:** Celery + Redis (async task processing)
- **Storage:** AWS S3 (VCF files, reports, encrypted)

**ML/AI:**
- **Libraries:**
  - Scikit-learn (classification, regression)
  - XGBoost / LightGBM (gradient boosting for polygenic risk scores)
  - TensorFlow / PyTorch (deep learning if needed)
  - Pandas + NumPy (data manipulation)
- **Training:** AWS SageMaker (managed training)
- **Serving:** AWS Lambda (serverless inference) or EC2 (if high volume)
- **Experiment Tracking:** MLflow

**Bioinformatics:**
- **Biopython:** VCF parsing
- **PLINK:** Genotype analysis (if needed)
- **ANNOVAR:** Variant annotation (if needed)
- **dbSNP, ClinVar APIs:** Lookup genetic variants

**Frontend (Dietist Review UI):**
- **Framework:** React + TypeScript
- **UI Library:** Material-UI or Ant Design
- **Charts:** Recharts or D3.js (visualize genotypes, risk scores)
- **Auth:** AWS Cognito or Auth0

**DevOps:**
- **CI/CD:** GitHub Actions
- **Infrastructure:** Terraform (AWS)
- **Monitoring:** AWS CloudWatch + Sentry (error tracking)
- **Logging:** AWS CloudWatch Logs

---

### 2.2 Data Security (GDPR Article 9)

**Genetic Data = Special Category Data**

**Storage:**
- **Encryption at rest:** AES-256 (AWS S3, RDS)
- **Encryption in transit:** TLS 1.3 (all API calls)
- **Access control:** IAM roles (principle of least privilege)
- **Audit logs:** AWS CloudTrail (every data access logged)

**Data Retention:**
- **VCF files:** Retained indefinitely (customer owns data)
- **Reports:** Retained indefinitely
- **Customer can delete:** GDPR "right to be forgotten" (automated process)
- **Lab deletes:** DNA sample destroyed after 90 days (contractual requirement)

**Anonymization (for ML training):**
- **CustomerID → Anonymous hash** (SHA-256)
- No PII in training data (only: genotype + outcomes)
- Can't reverse-engineer identity from training data

**Compliance:**
- **ISO 27001 certified** infrastructure
- **GDPR Article 9 compliant** data handling
- **DPO (Data Protection Officer)** oversight

---

## 3. DEVELOPMENT ROADMAP

### Month 3-4: MVP Pipeline (Rule-Based)

**Goal:** Automate 80% of dietist work (Stage 1-4)

**Deliverables:**
- [ ] Stage 1: VCF import + QC (Python script)
- [ ] Stage 2: Genotype → Phenotype lookup (SQLite database of 100 SNPs)
- [ ] Stage 3: Rule-based recommendations (if/else logic for 100 SNPs)
- [ ] Stage 4: PDF report generation (LaTeX templates)
- [ ] Stage 5: Dietist review UI (React app, read-only for MVP)

**Team:**
- Part-time bioinformatiker: 25K/mån × 2 = 50K
- Freelance React developer (UI): 50K (2 weeks)
- **Total:** 100K

**Output:** Dietist can review AI-generated reports in 10-15 min (vs 60 min manual)

---

### Month 5-6: Beta Testing (81 Customers)

**Goal:** Validate pipeline accuracy with real customers

**Process:**
1. Process 81 beta customers through pipeline
2. Dietist reviews all 81 reports (flag errors)
3. Measure accuracy: % of recommendations dietist approves without changes
4. **Target: 90%+ approval rate**

**Feedback Loop:**
- Collect errors, edge cases
- Update rules (e.g., "If VDR Fok1 ff + low baseline D-vitamin, recommend 5,000 IU not 4,000")
- Reprocess 81 customers (v2)
- **Iterate until 95%+ accuracy**

**Budget:** 0 (part of beta program)

---

### Month 7-9: ML Enhancement (Polygenic Risk Scores)

**Goal:** Replace simple rules with ML models for complex traits

**Examples:**
- **Obesity risk:** FTO + 20 other SNPs → Polygenic risk score
- **Inflammation risk:** TNF-α + IL-6 + CRP + 15 others → Inflammation score
- **Longevity:** FOXO3 + APOE + 10 others → Healthy aging score

**Process:**
1. Collect outcome data (beta customers + early customers: n=200)
2. Train XGBoost models (genotype → outcome)
3. Validate: Does model predict outcomes better than rules?
4. Deploy: A/B test ML vs rules (50/50 split)
5. Roll out: If ML performs better (>10% improvement), replace rules

**Team:**
- ML Engineer (part-time): 30K/mån × 3 = 90K
- AWS SageMaker compute: 10K

**Total:** 100K

---

### Month 10-12: Continuous Learning (Feedback Loop)

**Goal:** Re-train models with real customer outcome data

**Data Collected (by Month 10):**
- 300-400 customers
- Subjective outcomes: Energy, focus, sleep (weekly surveys)
- Objective outcomes: Blood tests (n=100-150 at Month 10)

**Re-Training:**
1. Export anonymized data (genotype + outcomes)
2. Re-train models (XGBoost, Random Forest)
3. Validate: Cross-validation (80/20 split)
4. A/B test: New model vs old model (50/50 customers)
5. Roll out: If new model better, deploy

**Team:**
- ML Engineer: 30K/mån × 3 = 90K
- AWS compute: 10K

**Total:** 100K

---

### Month 7-9: Sleep + Stress Add-Ons (LAUNCH)

**Goal:** Launch first two digital add-ons with freemium model

**Sleep Optimization:**
- **Input Genetics:**
  - PER3 (VNTR polymorphism): Circadian rhythm (morning vs evening person)
  - ADORA2A (rs5751876): Caffeine sensitivity, sleep quality
  - COMT (Val158Met): Sleep quality under stress
  - CYP1A2 (rs762551): Caffeine metabolism speed
- **Output (Basic - FREE):**
  - Sleep window calculation: "Your optimal bedtime: 22:30-06:30 based on PER3"
  - Caffeine cutoff time: "No caffeine after 14:00 based on CYP1A2 slow metabolizer"
  - Weekly sleep tips (email)
- **Output (Premium - 195 kr/mån):**
  - Personalized sleep supplement stack: Melatonin dose, Magnesium glycinate, L-theanine
  - Sleep tracker integration (Oura, Whoop, Apple Watch via HealthKit)
  - Monthly sleep report + recommendations
  - HRV-based sleep quality scoring
- **Development:**
  - Add 5 new SNPs to pipeline (PER3, ADORA2A, COMT, CYP1A2, CLOCK)
  - Build sleep window algorithm (circadian chronotype calculation)
  - Caffeine metabolism model (CYP1A2 → cutoff time)
  - Sleep supplement recommendation engine (dose by genotype)
  - API integration: Oura, Whoop, Apple HealthKit
- **Team:**
  - ML Engineer (contract): 50K (sleep algorithm + HealthKit integration)
  - iOS developer (contract): 60K (HealthKit integration, 2 months)
- **Total:** 110K

**Stress Management:**
- **Input Genetics:**
  - COMT (Val158Met - rs4680): Dopamine metabolism (stress resilience)
  - BDNF (Val66Met - rs6265): Brain plasticity, stress response
  - 5-HTTLPR (serotonin transporter): Anxiety risk
  - MAOA (VNTR): Stress reactivity
  - FKBP5 (rs1360780): HPA axis stress response
- **Output (Basic - FREE):**
  - Stress resilience assessment: "High COMT = warrior (handles acute stress), Low COMT = worrier (sensitive to chronic stress)"
  - 5× guided meditations (10 min each)
  - Monthly stress tips (email)
- **Output (Premium - 195 kr/mån):**
  - Full meditation library (50+ sessions, 10-30 min)
  - Personalized stress supplement stack: Adaptogens (Ashwagandha, Rhodiola), Magnesium, B-vitamins
  - HRV tracking integration (stress measurement via wearables)
  - Monthly stress coaching call (15 min) with wellness coach
- **Development:**
  - Add 5 new SNPs to pipeline (COMT, BDNF, 5-HTTLPR, MAOA, FKBP5)
  - Stress resilience scoring algorithm (genotype → phenotype)
  - Stress supplement recommendation engine (High COMT → meditation, Low COMT → adaptogens)
  - HRV integration (Oura, Whoop, Apple Watch)
  - Meditation library (license from Headspace API or build library)
- **Team:**
  - ML Engineer (contract): 40K (stress algorithm + HRV integration)
  - Meditation library: 10K (license or content creation)
- **Total:** 50K

**Combined Sleep + Stress Development:** 160K (Month 7-9)

**Revenue Target (Month 7-12, 6 months):**
- Sleep Premium: 163 customers × 195 kr × 6 mån = 190,635 SEK
- Stress Premium: 143 customers × 195 kr × 6 mån = 167,310 SEK
- **Total:** 357,945 SEK

---

### Month 10-12: Workout + Meal Planning Add-Ons (LAUNCH)

**Goal:** Launch next two digital add-ons with freemium model

**Workout Plan:**
- **Input Genetics:**
  - ACTN3 (R577X - rs1815739): "Sprinter gene" - power vs endurance
  - ACE (I/D - rs4340): Endurance capacity, recovery
  - PPARGC1A (Gly482Ser - rs8192678): VO2 max potential
  - ADRB2 (Gln27Glu - rs1042714): Fat burning during exercise
  - COL1A1 (rs1800012): Injury risk (collagen production, soft tissue)
  - IL6 (rs1800795): Inflammation response to exercise
- **Output (Basic - FREE):**
  - Genetic workout type: "Your DNA: 70% Power / 30% Endurance → Strength training prioritized"
  - 1× workout plan (3-day/week, basic split)
  - Exercise video library (20 core exercises)
- **Output (Premium - 195 kr/mån):**
  - Personalized 3/4/5-day workout programs (auto-generated based on DNA + fitness level)
  - Full video library (200+ exercises with form tutorials)
  - Progress tracking (app: weight, reps, PRs)
  - Monthly program updates (progressive overload)
  - Injury prevention tips (based on COL1A1): "High injury risk → prioritize mobility, collagen supplementation"
- **Development:**
  - Add 10 new SNPs to pipeline (ACTN3, ACE, PPARGC1A, ADRB2, COL1A1, IL6, NOS3, UCP2, UCP3, AMPD1)
  - Workout type algorithm: Genotype → Power/Endurance/Hybrid classification
  - AI workout program generator: 3/4/5-day splits (strength, hypertrophy, endurance)
  - Exercise video library integration (license from Gymondo or build)
  - Progress tracking module (PostgreSQL + React frontend)
- **Team:**
  - ML Engineer (contract): 80K (workout algorithm + program generator, 2 months)
  - Freelance exercise physiologist: 20K (workout science, program templates)
  - Video library: 15K (license or content creation)
- **Total:** 115K

**Meal Planning:**
- **Input Genetics:**
  - MTHFR (C677T, A1298C): Folate metabolism → high-folate meal recommendations
  - LCT (rs4988235): Lactose intolerance → dairy-free recipes
  - FUT2 (rs601338): Vitamin B12 absorption → B12-rich meals
  - VDR (Fok1, Bsm1): Vitamin D absorption → D-rich meals (salmon, eggs)
  - FTO (rs9939609): Obesity risk → portion control, macro guidance
- **Output (Basic - FREE):**
  - 3× DNA-matched recipes/week (e.g., "High-folate spinach salmon bowl for MTHFR C677T")
  - Basic grocery list
- **Output (Premium - 195 kr/mån):**
  - 7× weekly meal plans (breakfast, lunch, dinner)
  - Auto-generated grocery lists (categorized by store section)
  - Recipe video tutorials (10-15 min cooking videos)
  - Nutrition macro tracking (protein, carbs, fats aligned with DNA)
  - Integration with dietist nutrition plan (seamless alignment)
- **Development:**
  - Recipe database: 200+ DNA-matched recipes (nutritionist-created)
  - Meal plan generator: AI selects 7 meals based on DNA + preferences (vegetarian, allergies)
  - Grocery list generator: Aggregates ingredients from weekly plan
  - Macro tracking: Calculates daily macros, compares to DNA-based targets
- **Team:**
  - Backend developer (contract): 40K (meal plan generator, 1 month)
  - Nutritionist (recipe creation): 30K (200 recipes × 150 SEK each)
- **Total:** 70K

**Combined Workout + Meal Development:** 185K (Month 10-12)

**Revenue Target (Month 10-12, 3 months):**
- Workout Premium: 195 customers × 195 kr × 3 mån = 114,075 SEK
- Meal Premium: 130 customers × 195 kr × 3 mån = 76,050 SEK
- **Total:** 190,125 SEK

---

### Month 10-12: PT Coaching Level 2 (LAUNCH via Partnership)

**Goal:** Launch hybrid PT coaching via partner (Pactster/MyAcademy)

**Input to PT:**
- Customer DNA report (workout type, injury risk, recovery capacity)
- Current fitness level (self-assessment)
- Goals (strength, weight loss, endurance, general fitness)

**Service:**
- Bi-weekly check-ins (15 min video call)
- Form corrections (customer submits video, PT reviews)
- Progression adjustments
- Injury prevention coaching (based on COL1A1)

**Development:**
- PT partner integration: API to share DNA data (with customer consent)
- Booking system: Calendly-style integration
- Video call infrastructure: Zoom API integration

**Team:**
- Backend developer (contract): 30K (PT booking + DNA data sharing API)
- PT partner onboarding: 0 SEK (partner responsibility)

**Total:** 30K

**Revenue Target (Month 10-12, 3 months):**
- PT Level 2: 65 customers × 148 kr (our 30% cut) × 3 mån = 28,860 SEK

---

### Year 1 Add-On Development Summary

| Add-On | Development Cost | Launch Month | Revenue (Year 1) |
|--------|------------------|--------------|------------------|
| Sleep Optimization | 110K | Month 7 | 190,635 SEK |
| Stress Management | 50K | Month 7 | 167,310 SEK |
| Workout Plan | 115K | Month 10 | 114,075 SEK |
| Meal Planning | 70K | Month 10 | 76,050 SEK |
| PT Coaching Level 2 | 30K | Month 10 | 28,860 SEK |
| **TOTAL** | **375K** | - | **576,930 SEK** |

**Revised Total AI Budget Year 1:** 650K (core) + 375K (add-ons) = **1,025K**

**ROI (Year 1):**
- Investment: 375K (add-on development)
- Revenue: 576,930 SEK (Year 1, partial year)
- **ROI: 1.54× (54% return Year 1)**

**ROI (Year 2, full year):**
- Revenue: 2,240,000 SEK (conservative projection from market analysis)
- Ongoing COGS: 90K (digital infrastructure, support)
- Net profit: 2,150,000 SEK
- **ROI: 5.7× (Year 2)**

---

### Year 2: Advanced Features

**Cognitive Performance / Nootropics (Q1):**
- **Input Genetics:**
  - APOE4 (rs429358, rs7412): Alzheimer's risk → neuroprotection focus
  - BDNF (Val66Met): Learning & memory
  - COMT (Val158Met): Working memory
  - CYP1A2 (rs762551): Caffeine response (focus vs jitters)
- **Output:**
  - Nootropic supplement stack: Omega-3 (high EPA for APOE4), Phosphatidylserine, Lion's Mane, Bacopa, L-theanine + caffeine
  - Monthly cognitive assessment (reaction time, memory tests)
  - Focus optimization guide
- **Development:** 60K
- **Revenue opportunity:** +295 kr/mån add-on (295 kr × 78 customers × 9 mån = 207K Year 2)

**Wearables Data Integration (Q1):**
- **Integrations:**
  - Oura Ring API
  - Whoop API
  - Garmin Connect API
  - Apple HealthKit (already done Month 7-9 for Sleep)
  - Google Fit (Android)
- **Output:**
  - Auto-sync: Sleep, HRV, steps, workouts, heart rate
  - AI analyzes trends → adjusts recommendations
  - Monthly insights report: "Your HRV declined 15% → increase magnesium 400→600mg, reduce stress"
- **Development:** 80K (API integrations × 5 platforms)
- **Revenue opportunity:** +95 kr/mån (95 kr × 228 customers × 9 mån = 195K Year 2)

**Community & Group Coaching (Q2):**
- **Platform:** Discord or Circle (white-label community)
- **Features:**
  - Private member community (peer support)
  - Weekly group coaching calls (30 min, max 10 people, dietist-led)
  - Accountability groups (4-6 people, shared goals)
  - Monthly challenges (step challenges, sleep challenges)
  - Early access to new features
- **Development:** 40K (Circle integration + group call infrastructure)
- **Revenue opportunity:** +495 kr/mån (495 kr × 52 customers × 6 mån = 154K Year 2)

---

## 4. KEY PERSONNEL

### 4.1 Part-Time Bioinformatician (Month 2-12)

**Role:**
- Build Stage 1-4 of pipeline
- Maintain genetic variant database (100 SNPs)
- Update recommendations as new research published
- QA: Review edge cases

**Requirements:**
- PhD or Master's in bioinformatics, genetics, or computational biology
- Python proficiency (Biopython, Pandas)
- Experience with VCF files, GWAS data
- Knowledge of nutrigenomics literature

**Time Commitment:** 20-30% (1-1.5 days/week)

**Compensation:** 15-20K/mån

**Where to Find:**
- PhD students at KI, Uppsala, Lund (seeking part-time income)
- PostDocs looking for side projects
- LinkedIn: "Bioinformatician Sweden"

---

### 4.2 ML Engineer (Month 7+, Part-Time)

**Role:**
- Build ML models (Stage 3 enhancement)
- Implement continuous learning loop
- A/B testing infrastructure
- Model monitoring (detect drift)

**Requirements:**
- Experience with scikit-learn, XGBoost
- AWS SageMaker or similar (MLflow, Kubeflow)
- Understanding of healthcare ML (GDPR, bias, fairness)
- Python + SQL

**Time Commitment:** 30% (1.5 days/week)

**Compensation:** 25-30K/mån

**Where to Find:**
- Freelance ML engineers on Upwork, Toptal
- LinkedIn: "Machine Learning Engineer Stockholm"
- Master's students in ML/AI (KTH, Chalmers)

---

### 4.3 CTO (Month 6-9, Full-Time)

**Role (AI-related):**
- Owns AI roadmap (workout, sleep, stress features)
- Hires ML team (Year 2)
- Ensures scalability (1,000 → 10,000 customers)
- Security & compliance (ISO 27001, GDPR)

**Requirements:**
- Backend experience (Python, FastAPI, PostgreSQL)
- Cloud (AWS, infrastructure as code)
- Healthcare-tech background (preferred)
- Security mindset (ISO 27001 experience)

**Compensation:** 500K/år (Year 1, with 5M seed) + 1-2% equity

**See:** CTO_Recruitment_Plan.md for full details

---

## 5. COST BREAKDOWN (Year 1)

### Core Nutrition AI Costs

**One-Time Costs:**

| Item | Cost | Notes |
|------|------|-------|
| Pipeline development (Stage 1-4) | 100K | Bioinformatician 2 mån |
| Dietist review UI (React) | 50K | Freelance developer |
| ML model development (Stage 3) | 100K | ML Engineer 3 mån |
| Testing & QA (81 beta) | 0 | Included in beta program |
| **Total One-Time (Core)** | **250K** | |

**Recurring Costs (Annual):**

| Item | Cost | Notes |
|------|------|-------|
| Bioinformatician (part-time) | 180K | 15K/mån × 12 |
| ML Engineer (part-time, Month 7-12) | 150K | 25K/mån × 6 |
| AWS compute (training + inference) | 50K | SageMaker + Lambda |
| AWS storage (VCF files, reports) | 10K | S3 (encrypted) |
| MLflow / monitoring tools | 10K | Experiment tracking |
| **Total Recurring Year 1 (Core)** | **400K** | |

**Core Nutrition Total Year 1: 650K**

---

### Add-On Development Costs (Year 1)

**Sleep + Stress (Month 7-9):**

| Item | Cost | Notes |
|------|------|-------|
| ML Engineer (contract) | 90K | Sleep 50K + Stress 40K |
| iOS Developer (HealthKit) | 60K | 2 months contract |
| Meditation library | 10K | License or content creation |
| **Subtotal** | **160K** | |

**Workout + Meal + PT (Month 10-12):**

| Item | Cost | Notes |
|------|------|-------|
| ML Engineer (contract) | 80K | Workout algorithm 2 months |
| Exercise physiologist | 20K | Workout science consulting |
| Exercise video library | 15K | License or content creation |
| Backend developer | 40K | Meal plan generator 1 month |
| Nutritionist (recipes) | 30K | 200 DNA-matched recipes |
| PT partner integration | 30K | API + booking system |
| **Subtotal** | **215K** | |

**Total Add-On Development Year 1: 375K**

---

### Combined AI Budget Year 1: 1,025K

| Category | Cost |
|----------|------|
| Core Nutrition (one-time + recurring) | 650K |
| Add-On Development (Sleep, Stress, Workout, Meal, PT) | 375K |
| **TOTAL YEAR 1** | **1,025K** |

**Already Allocated:**
- AI-Dietist development: 200K (MVP)
- Bioinformatics: 240K (already budgeted in Kostnadanalys V2)
- **Core remaining needed:** 210K

**Add-On Budget:**
- **New allocation needed:** 375K (from 5M seed round buffer)

**Source:** 5M seed round includes buffer (672K) → reallocate 585K total to AI (210K core + 375K add-ons)

---

### Year 2 AI Budget (Add-Ons Continued)

| Add-On | Development Cost | Notes |
|--------|------------------|-------|
| Cognitive Performance | 60K | Q1 launch |
| Wearables Integration | 80K | Q1 launch (Oura, Whoop, Garmin) |
| Community & Group Coaching | 40K | Q2 launch (Circle/Discord) |
| **Total Year 2** | **180K** | |

**Year 2 Recurring:**
- ML Engineer (full-time): 600K/år
- Bioinformatician (part-time): 180K/år
- AWS compute: 100K/år (2× customers, 2× features)
- **Total Recurring Year 2:** 880K

**Year 2 Total AI Budget:** 180K (development) + 880K (recurring) = **1,060K**

---

## 6. ROI ANALYSIS

### 6.1 Dietist Efficiency

**Without AI:**
- Time per customer: 60 min (analyze DNA + create plan)
- Dietist capacity: 8h/day ÷ 1h = 8 customers/day
- Monthly capacity: 8 × 20 = **160 customers/month**
- Cost per customer: 38K dietist salary ÷ 160 = **238 SEK**

**With AI:**
- Time per customer: 10 min (review AI draft)
- Dietist capacity: 8h/day ÷ 0.17h = 48 customers/day
- Monthly capacity: 48 × 20 = **960 customers/month** (6× improvement)
- Cost per customer: 38K ÷ 960 = **40 SEK** (-83% cost reduction)

**Savings at 650 customers:**
- Without AI: 238 × 650 = 154,700 SEK/år
- With AI: 40 × 650 = 26,000 SEK/år
- **Savings: 128,700 SEK/år**

**ROI:**
- Investment: 650K (Year 1)
- Savings: 128,700 SEK/år (ongoing)
- **Payback: 5 years**

**But:** This ignores scalability. At 2,000 customers:
- Without AI: Need 2,000 ÷ 160 = **12.5 dietists** (12.5 × 456K = **5.7M SEK/år**)
- With AI: Need 2,000 ÷ 960 = **2.1 dietists** (2.1 × 456K = **957K SEK/år**)
- **Savings: 4.7M SEK/år at scale**

---

### 6.2 Innovation Speed

**New Feature: Workout Recommendations**

**Without AI (Manual):**
- Dietist must learn workout science (2 months training)
- Manually create workout plans (60 min per customer)
- Hard to scale
- **Time to launch: 6 months**

**With AI (Automated):**
- Add 10 new SNPs (ACTN3, ACE, etc.) to pipeline
- Train model on literature (3 weeks)
- Generate workout recommendations (automated)
- Dietist reviews (10 min per customer)
- **Time to launch: 2 months**

**Competitive advantage:**
- Launch 3 months faster than competitors
- First-mover in "DNA-powered workout plans"

---

### 6.3 Data Moat (Continuous Improvement)

**Scenario:**
- Year 1: 650 customers
- Year 2: 2,000 customers
- Year 3: 5,000 customers

**Data Accumulation:**
- Year 1: 650 genotypes + 200 blood tests + 8,000 subjective surveys
- Year 2: 2,000 genotypes + 800 blood tests + 24,000 surveys
- Year 3: 5,000 genotypes + 2,500 blood tests + 60,000 surveys

**AI Improvement:**
- Year 1: Baseline accuracy (90%)
- Year 2: Improved accuracy (93%) - more training data
- Year 3: Advanced accuracy (96%) - large dataset + rare variants

**Competitor Challenge:**
- Competitor enters Year 3 → starts with 0 data
- Must collect 5,000 customers (3-5 years) to match our accuracy
- **Data moat = 3-5 year head start**

---

## 7. RISKS & MITIGATION

### Risk 1: AI Errors (Incorrect Recommendations)

**Example:** AI recommends high-dose vitamin E, but customer has blood clotting disorder (not in DNA)

**Impact:** Health harm, liability, reputation damage

**Mitigation:**
- **Dietist ALWAYS reviews** (human in the loop)
- **Disclaimers:** "Not medical advice, consult doctor before starting supplements"
- **Ansvarsförsäkring:** 35K/år (product liability insurance)
- **Feedback loop:** Track adverse events, update AI rules

**Probability:** Low (dietist catches 99% of errors)

---

### Risk 2: Bioinformatics Quality Issues

**Example:** VCF parsing bug causes wrong genotype (CC reported as TT)

**Impact:** Incorrect recommendations, customer harm

**Mitigation:**
- **Extensive testing:** 100 test samples before launch
- **Validation:** Compare AI output to manual analysis (10% spot-check)
- **Lab QC:** Genotyping call rate >98% (lab responsibility)
- **Version control:** Git (every code change tracked)

**Probability:** Low (testing + QC catches bugs)

---

### Risk 3: ML Model Bias

**Example:** Model trained on Swedish population doesn't generalize to immigrants (different genetic ancestry)

**Impact:** Inaccurate recommendations for minorities

**Mitigation:**
- **Diverse training data:** Collect ancestry information (self-reported)
- **Stratified training:** Train separate models for different ancestries (European, Asian, African, etc.)
- **Transparency:** Disclose "Model trained on European ancestry, may be less accurate for others"
- **Continuous improvement:** Add diverse customers → retrain models

**Probability:** Medium (initial model will be European-focused, improve over time)

---

### Risk 4: Competitor Copies AI

**Example:** Werlabs reverse-engineers our recommendations, builds similar AI

**Impact:** Lost competitive advantage

**Mitigation:**
- **Data moat:** Competitor needs 1,000+ customers (3-5 years) to match accuracy
- **Continuous improvement:** Our AI gets better every quarter (moving target)
- **Patent defense:** File patents on key algorithms (if novel)
- **Speed:** Launch new features faster (workout, sleep, stress) before they catch up

**Probability:** Medium-High (eventually competitors will build AI, but we have 3-5 year lead)

---

## 8. SUCCESS METRICS (KPIs)

### Year 1 Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Dietist Review Time** | <15 min/customer | Time tracking (manual) |
| **AI Approval Rate** | >90% (dietist accepts AI recommendations without changes) | Dietist feedback (flag changes) |
| **Customer Satisfaction** | >4.5/5 stars (report quality) | Post-report survey |
| **Adverse Events** | 0 serious adverse events (SAE) | Incident reporting |
| **Model Accuracy (Blood Tests)** | Predict 70%+ of customers who improve D-vitamin | Blood test outcomes (n=200) |
| **Time to Launch New Feature** | <3 months (workout recommendations) | Project timeline tracking |

---

## 9. FUTURE VISION (Year 3-5)

### 9.1 Holistisk Hälsoplattform

**Core (Year 1-2):**
- DNA + Nutrition + Supplements

**Expansion (Year 3-5):**
- 🍽️ **Meal Plans:** DNA-matched recipes, grocery lists
- 🏃 **Workout Plans:** Strength vs endurance, recovery recommendations
- 😴 **Sleep Optimization:** Circadian rhythm, sleep window, supplements (melatonin, magnesium)
- 🧘 **Stress Management:** Meditation, breathwork, adaptogens
- 🧠 **Cognitive Enhancement:** Nootropics, brain health (APOE4 carriers)
- 💊 **Pharmacogenomics:** Drug metabolism (CYP2D6, CYP2C19) for medication optimization

**Revenue Model:**
- Core nutrition: 865-1,195 kr/mån (current)
- Add-ons: 195-295 kr/mån each (workout, sleep, stress)
- **Total potential:** 1,500-2,000 kr/mån (all features)

---

### 9.2 Data Licensing (B2B2C)

**Opportunity:** Sell anonymized insights to:
- Supplement companies (product development)
- Research institutions (nutrigenomics studies)
- Pharma companies (drug development)

**Example:**
- "Swedish population data: 5,000 genotypes + 10,000 blood tests + 100,000 surveys"
- **Value:** 5-10M SEK (one-time or subscription)

**Privacy:**
- 100% anonymized (no PII)
- GDPR-compliant (research exemption)
- Customer consent required

---

### 9.3 White-Label Platform

**Opportunity:** License AI platform to:
- Other healthtech companies (dietist practices, gyms, healthcare providers)
- International expansion (Norwegian, Danish, Finnish markets)

**Revenue Model:**
- Setup fee: 500K SEK
- SaaS license: 50K/mån
- Per-customer fee: 100 SEK/customer

**Example:**
- License to Norrsken Health (Norwegian healthtech)
- They rebrand, we provide infrastructure + AI
- Split revenue: 70/30 (they get 70%, we get 30%)

---

## 10. CONCLUSION & NEXT STEPS

### Why AI is Critical

1. **Scalability:** 1 dietist handles 960 customers/mån (vs 160 manual) = **6× efficiency**
2. **Quality:** Consistent recommendations (no human error)
3. **Speed:** Launch new features 3× faster (workout, sleep, stress)
4. **Data Moat:** Competitor needs 3-5 years to match our accuracy
5. **Revenue:** Enable add-on features (workout, sleep, stress) = +500-1,000 kr/mån potential

### Investment

**Year 1:** 650K
- Pipeline development: 250K (one-time)
- Bioinformatician: 180K (recurring)
- ML Engineer: 150K (recurring, Month 7-12)
- AWS compute: 50K (recurring)

**ROI:**
- Payback: 5 years (dietist efficiency alone)
- **But:** Scalability benefit = 4.7M SEK/år savings at 2,000 customers
- **Real payback: 2-3 months at scale**

### Immediate Action Items

**Month 1-2:**
- [ ] Hire part-time bioinformatiker (post job ad)
- [ ] Setup AWS infrastructure (S3, RDS, Lambda)
- [ ] Define 100 SNPs for MVP (prioritize Tier 1 + Tier 2)

**Month 3-4:**
- [ ] Build Stage 1-4 of pipeline (VCF import → PDF report)
- [ ] Build dietist review UI (React app)
- [ ] Test with 10 dummy samples

**Month 5-6:**
- [ ] Beta test with 81 customers
- [ ] Iterate based on dietist feedback
- [ ] Achieve 90%+ approval rate

**Month 7-12:**
- [ ] Hire ML Engineer (part-time)
- [ ] Build ML models (polygenic risk scores)
- [ ] Implement continuous learning loop
- [ ] Launch workout recommendations (beta, Elite tier)

---

**Dokumentversion:** 1.0
**Skapad:** 2026-01-19
**Owner:** CTO (to-be-hired) + Part-time Bioinformatician
**Next Review:** Month 6 (after beta test results)
**Status:** READY FOR IMPLEMENTATION

---

## KÄLLOR & REFERENSER

**AI/ML Technologies:**
- Scikit-learn: https://scikit-learn.org/
- XGBoost: https://xgboost.readthedocs.io/
- AWS SageMaker: https://aws.amazon.com/sagemaker/
- MLflow: https://mlflow.org/

**Bioinformatics:**
- Biopython: https://biopython.org/
- PyVCF: https://pyvcf.readthedocs.io/
- dbSNP: https://www.ncbi.nlm.nih.gov/snp/
- ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/
- GWAS Catalog: https://www.ebi.ac.uk/gwas/

**Nutrigenomics Research:**
- PubMed: https://pubmed.ncbi.nlm.nih.gov/
- Nutrigenomics reviews: See Kallor_Master_Referenslista.md

**GDPR & Security:**
- GDPR Article 9: EU Regulation 2016/679
- ISO 27001: ISO/IEC 27001:2013
- AWS Security Best Practices: https://aws.amazon.com/security/

**Fullständig referenslista:** Se `Kallor_Master_Referenslista.md`
