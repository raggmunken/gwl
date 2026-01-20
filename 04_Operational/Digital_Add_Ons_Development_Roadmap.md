# DIGITAL ADD-ONS DEVELOPMENT ROADMAP

**Datum:** 2026-01-19
**För:** Engineering & Product Development
**Version:** 1.0

---

## 🎯 EXECUTIVE SUMMARY

**Goal:** Develop 4 digital add-ons (Sleep, Stress, Workout, Meal Planning) for launch Month 7-12 Year 1.

**Budget:** 250K SEK total development
- Sleep Optimization: 50K (Month 7-8)
- Stress Management: 50K (Month 7-8)
- Workout Plan: 100K (Month 10-11)
- Meal Planning: 50K (Month 10-11)

**Timeline:**
- **Month 7-9:** Sleep + Stress (parallel development)
- **Month 10-12:** Workout + Meal Planning (parallel development)
- **Month 13+:** Iterate based on feedback

**Revenue Target (Year 1, Month 7-12):**
- 304K SEK from add-ons (conservative)
- ROI: 304K revenue / 250K dev cost = **1.2× in Year 1 alone**
- Year 2 ROI: 1.5M revenue / 250K = **6× cumulative**

**Tech Stack:**
- Backend: Python (FastAPI or Flask)
- ML/AI: TensorFlow or PyTorch (for recommendations)
- Database: PostgreSQL (genetic + behavioral data)
- APIs: Oura, Whoop, Garmin, Apple Health
- Frontend: React (web), React Native (mobile)

---

## 📋 FREEMIUM ARCHITECTURE (FEATURE GATING)

### What is Freemium?

**Basic (FREE):**
- Core functionality to drive adoption (60-70% usage)
- Limited features, no premium content
- Goal: Hook users, show value

**Premium (PAID):**
- Advanced features, personalized content, integrations
- Supplements, tracking, coaching
- Goal: Convert 25-30% of basic users

### How Feature Gating Works

**Technical Implementation:**
- User table: `subscription_tier` (essential, premium, elite)
- Add-on table: `user_addons` (sleep_premium: true/false)
- API checks tier before serving content:
  ```python
  if user.has_addon('sleep_premium'):
      return full_sleep_report()
  else:
      return basic_sleep_tips()
  ```

**Upsell Prompts:**
- Basic users see: "Upgrade to Premium for sleep tracker integration (195 kr/mån)"
- Timing: After 7 days of basic usage (proven interest)
- A/B test: Prompt timing, messaging, discount offers

---

## 🛏️ SLEEP OPTIMIZATION (Month 7-8, 50K Budget)

### Genetic Basis

**SNPs Required:**
- **PER3 (rs57875989):** VNTR polymorphism (4/4, 4/5, 5/5)
  - 4/4 = Short sleeper (morning person, 6-7h sufficient)
  - 5/5 = Long sleeper (night owl, need 8-9h)
- **ADORA2A (rs5751876):** Adenosine receptor
  - T/T = High caffeine sensitivity (affects sleep even 6h before bed)
  - C/C = Low sensitivity (can drink coffee at 16:00)
- **CYP1A2 (rs762551):** Caffeine metabolism
  - A/A = Slow metabolizer (half-life 8h)
  - C/C = Fast metabolizer (half-life 3h)
- **COMT (rs4680):** Dopamine, stress → sleep quality
  - Val/Val = Fast dopamine clearance (poor sleep under stress)
  - Met/Met = Slow clearance (good sleep even stressed)

---

### Features

#### Basic (FREE)

**1. Sleep Window Calculator**
- Input: PER3 genotype
- Output: "Your optimal sleep: 22:30-06:30 (8h window)"
- Algorithm:
  ```python
  def calculate_sleep_window(per3_genotype):
      if per3_genotype == '4/4':  # Short sleeper
          return {'bedtime': '23:00', 'wake': '06:00', 'duration': 7}
      elif per3_genotype == '5/5':  # Long sleeper
          return {'bedtime': '22:00', 'wake': '07:00', 'duration': 9}
      else:  # 4/5 heterozygous
          return {'bedtime': '22:30', 'wake': '06:30', 'duration': 8}
  ```

**2. Caffeine Cutoff Time**
- Input: CYP1A2 + ADORA2A
- Output: "No caffeine after 14:00 (slow metabolizer + high sensitivity)"
- Algorithm:
  ```python
  def caffeine_cutoff(cyp1a2, adora2a, target_bedtime):
      # CYP1A2: A/A = 8h half-life, C/C = 3h
      half_life = 8 if 'A' in cyp1a2 else 3

      # ADORA2A: T/T = extra 2h buffer needed
      buffer = 2 if 'T' in adora2a else 0

      # 3 half-lives to clear 87.5% of caffeine
      clearance_time = (3 * half_life) + buffer

      cutoff = target_bedtime - timedelta(hours=clearance_time)
      return cutoff  # e.g., 14:00
  ```

**3. Weekly Sleep Tips (Email)**
- Automated email series (7 tips over 7 weeks)
- Content: "Sleep hygiene 101", "Light exposure", "Temperature", etc.
- Personalized: Mention their genotype ("As a PER3 5/5 long sleeper...")

---

#### Premium (195 kr/mån)

**4. Sleep Supplements (Personalized Stack)**
- Input: PER3, COMT
- Output: Custom supplement dosages delivered monthly
- Supplements:
  - **Melatonin:** 1-3mg (PER3 5/5 = 3mg, 4/4 = 1mg)
  - **Magnesium glycinate:** 300-400mg (universal)
  - **L-theanine:** 100-200mg (COMT Val/Val = 200mg for stress)
- Cost (COGS): ~60 kr/mån (bulk pricing)
- Margin: 195 - 60 = 135 kr/mån (69%)

**5. Sleep Tracker Integration**
- APIs:
  - **Oura Ring:** Most accurate (gold standard for sleep stages)
  - **Whoop:** Recovery score, HRV
  - **Apple Watch:** Sleep Stages (watchOS 10+)
  - **Garmin:** Body Battery, sleep quality
- Data synced:
  - Total sleep time
  - Sleep stages (deep, REM, light)
  - Sleep efficiency (time asleep / time in bed)
  - HRV (heart rate variability during sleep)
- Tech:
  - Oura API: `GET /v2/usercollection/daily_sleep`
  - Whoop API: `GET /v1/recovery`
  - Apple Health: HealthKit integration (iOS app required)
  - Garmin: Garmin Health API (enterprise tier, $2,000/year)

**6. Monthly Sleep Report**
- Generated first week of each month
- Sections:
  - **Summary:** "You averaged 7.2h sleep (target: 8h for your PER3 genotype)"
  - **Deep Sleep:** "15% deep sleep (below optimal 20%, try magnesium increase)"
  - **Trends:** Chart showing sleep hours over 30 days
  - **Recommendations:** "Your HRV dropped Week 3 → stress spike, increase L-theanine"
- Format: PDF (email) + in-app dashboard

**7. Dietist Review (If Issues)**
- Trigger: Sleep <6h for 7+ consecutive days
- Action: Dietist gets notification → schedules 15 min call
- Goal: Identify non-genetic factors (stress, diet, screen time)

---

### Development Plan (Month 7-8)

**Month 7 Week 1-2: Algorithm Development (15K)**
- Implement sleep window calculator (PER3 logic)
- Implement caffeine cutoff calculator (CYP1A2 + ADORA2A)
- Unit tests (genetic edge cases: homozygous vs heterozygous)

**Month 7 Week 3-4: Email Automation (5K)**
- Write 7 email templates (sleep tips)
- Setup email service (SendGrid or Mailgun)
- Personalize with Jinja templates (insert genotype data)

**Month 8 Week 1-2: API Integrations (20K)**
- Oura Ring: Apply for developer access, implement OAuth
- Whoop: Similar OAuth flow
- Apple Health: HealthKit integration (requires iOS app work)
- Garmin: Enterprise API contract ($2K/year), implement

**Month 8 Week 3-4: Supplement Logic + Report Generator (10K)**
- Build supplement recommendation engine (PER3 → melatonin dose)
- Integrate with supplement supplier API (auto-add to monthly box)
- Build PDF report generator (Python: ReportLab or WeasyPrint)
- Dashboard charts (frontend: Chart.js or D3.js)

**Total: 50K** (15 + 5 + 20 + 10)

---

### Testing & QA (Month 9)

**Beta Test:**
- Recruit: 50 customers (email: "Try new Sleep Optimization, free for Month 1")
- Criteria: Own Oura/Whoop/Apple Watch (for tracker integration test)
- Feedback: Survey after 30 days
  - "Was sleep window accurate?" (Yes/No + comment)
  - "Did you upgrade to premium?" (If no, why not?)

**Metrics to Track:**
- Basic → Premium conversion: Target 25%
- Average sleep improvement: Target +30 min (self-reported)
- App crashes: <1% (sleep tracker syncs can be buggy)

---

## 🧘 STRESS MANAGEMENT (Month 7-8, 50K Budget)

### Genetic Basis

**SNPs Required:**
- **COMT (rs4680):** Val158Met polymorphism
  - Val/Val = Fast dopamine clearance (low stress resilience, rumination)
  - Met/Met = Slow clearance (high resilience, calm under pressure)
  - Val/Met = Moderate
- **BDNF (rs6265):** Val66Met polymorphism
  - Val/Val = High BDNF (good brain plasticity, fast stress recovery)
  - Met carriers = Lower BDNF (slower recovery, more prone to anxiety)
- **5-HTTLPR (SLC6A4):** Serotonin transporter
  - s/s = Low serotonin transport (higher anxiety risk)
  - l/l = High transport (more emotionally stable)
- **MAOA (uVNTR):** MAO-A enzyme (stress reactivity)
  - Low activity = Heightened emotional response
  - High activity = Calmer disposition

---

### Features

#### Basic (FREE)

**1. Stress Resilience Assessment**
- Input: COMT + BDNF genotypes
- Output: "Your stress type: Moderate Resilience (COMT Val/Met + BDNF Val/Val)"
- Description: "You recover quickly from acute stress (high BDNF) but can ruminate on long-term stressors (COMT Val). Best strategies: Daily meditation + adaptogens."

**2. 5× Guided Meditations (Intro Library)**
- Content:
  - 5 min: "Quick Breathing Exercise"
  - 10 min: "Body Scan for Stress Relief"
  - 10 min: "Loving-Kindness Meditation"
  - 15 min: "Mindful Walking"
  - 15 min: "Sleep Meditation"
- Format: Audio files (MP3) + transcripts
- Source: License from Calm/Headspace B2B ($5K/year) OR create in-house (hire voice actor $2K)

**3. Monthly Stress Tips (Email)**
- Same as sleep tips: 7-email series
- Topics: "HRV tracking", "Adaptogens 101", "Breathwork techniques"

---

#### Premium (195 kr/mån)

**4. Full Meditation Library (50+ Sessions)**
- Categories:
  - Sleep (10 sessions, 10-30 min)
  - Focus (10 sessions, for work)
  - Anxiety (15 sessions, for panic attacks)
  - Breathwork (10 sessions, box breathing, 4-7-8)
  - Movement (5 sessions, yoga nidra)
- Cost: License from Calm B2B (~$10K/year for unlimited users) OR create (voice actor $10K)

**5. Stress Supplements (Personalized)**
- Input: COMT, BDNF, 5-HTTLPR
- Output:
  - **COMT Val/Val (low resilience):**
    - Ashwagandha 300mg (2× daily) - adaptogen
    - Rhodiola rosea 200mg (morning) - reduces cortisol
    - L-tyrosine 500mg (morning) - dopamine precursor
  - **BDNF Met carrier (slow recovery):**
    - Omega-3 high DHA (2g/day) - brain plasticity
    - Magnesium L-threonate (144mg elemental) - crosses blood-brain barrier
  - **5-HTTLPR s/s (low serotonin):**
    - 5-HTP 100mg (evening) - serotonin precursor
    - L-tryptophan 500mg (alternative to 5-HTP)
- Cost (COGS): ~80 kr/mån
- Margin: 195 - 80 = 115 kr/mån (59%)

**6. HRV Tracking Integration**
- APIs: Same as sleep (Oura, Whoop, Apple Watch, Garmin)
- Data: HRV (heart rate variability) - proxy for stress/recovery
  - High HRV = Good recovery, low stress
  - Low HRV = Poor recovery, high stress, over-training
- Dashboard: HRV trend over 30 days (line chart)
- Alerts: "Your HRV dropped 20% this week → increase stress management"

**7. Monthly Stress Coaching Call (15 min)**
- Staffing: Hire 1× stress coach (part-time, 15K/mån Year 2)
- Ratio: 1 coach per 100 customers (can handle ~400 calls/month @ 15 min each)
- Booking: Calendly integration (customer books via app)
- Topics: HRV interpretation, supplement adjustments, meditation troubleshooting

---

### Development Plan (Month 7-8)

**Month 7 Week 1-2: Stress Assessment (10K)**
- Build algorithm (COMT + BDNF + 5-HTTLPR → stress type)
- Write descriptions (4 genotype combinations, 200 words each)
- Unit tests

**Month 7 Week 3-4: Meditation Library (15K)**
- Option A: License from Calm B2B ($10K/year) ← **RECOMMENDED**
- Option B: Create in-house (hire voice actor $2K, script writing $3K, production $5K)
- Setup audio hosting (S3 + CloudFront for CDN, $50/mån)

**Month 8 Week 1-2: Supplement Logic (5K)**
- Build recommendation engine (genotype → supplement stack)
- Integrate with supplier API (add to monthly box)
- COGS negotiation (bulk pricing for adaptogens)

**Month 8 Week 3-4: HRV Integration (15K)**
- Same as sleep tracker APIs (Oura, Whoop, Garmin, Apple)
- HRV data parsing (different APIs return different formats)
- Dashboard charts (HRV trend line, color-coded: green/yellow/red)
- Alert logic (if HRV drops >15% week-over-week → notification)

**Month 9: Coaching Platform (5K)**
- Calendly integration for booking
- Hire stress coach (advertise on LinkedIn, target: psychology grad students, 15K/mån part-time)
- Coach onboarding: 2-day training on genetic stress types

**Total: 50K** (10 + 15 + 5 + 15 + 5)

---

### Testing & QA (Month 9)

**Beta Test:**
- Recruit: 50 customers
- Focus: HRV integration accuracy (most complex part)
- Feedback:
  - "Did HRV data sync correctly?" (Yes/No)
  - "Was stress assessment accurate?" (1-5 scale)
  - "Would you pay 195 kr/mån for premium?" (Yes/No + reason)

---

## 💪 WORKOUT PLAN (Month 10-11, 100K Budget)

### Genetic Basis

**SNPs Required:**
- **ACTN3 (rs1815739):** R577X polymorphism
  - R/R = Power/sprinter (fast-twitch muscle fibers)
  - X/X = Endurance (slow-twitch fibers)
  - R/X = Mixed (versatile athlete)
- **ACE (rs4340 or rs1799752):** I/D polymorphism
  - D/D = Endurance (better oxygen utilization, V02 max)
  - I/I = Strength (muscle building, power)
  - I/D = Mixed
- **PPARGC1A (rs8192678):** PGC-1α (mitochondrial biogenesis)
  - G/G = High endurance potential (more mitochondria)
  - S/S = Lower endurance (but fine for strength)
- **COL1A1 (rs1800012):** Collagen production
  - T/T = Higher injury risk (weaker connective tissue)
  - G/G = Normal (lower injury risk)
- **ADRB2 (rs1042713):** Beta-2 adrenergic receptor (fat oxidation)
  - Arg/Arg = Better fat burning during cardio
  - Gly/Gly = Carb-dependent (need more carbs for energy)

---

### Features

#### Basic (FREE)

**1. Genetic Workout Type Recommendation**
- Input: ACTN3 + ACE
- Output: "Your optimal training: Strength-focused (ACTN3 R/R + ACE I/I)"
- Description:
  - **Strength:** Heavy compound lifts, 3-6 reps, 3-5 min rest, 3-4× per week
  - **Endurance:** Running, cycling, swimming, HIIT, 5-6× per week
  - **Hybrid:** Mix of both (CrossFit-style, 4× per week)

**2. 1× Static Workout Plan (3-day/week)**
- Based on genetic type (Strength, Endurance, or Hybrid)
- Example (Strength, 3-day split):
  - **Day 1 (Upper Push):** Bench press 4×6, Overhead press 3×8, Dips 3×10
  - **Day 2 (Lower):** Squat 4×6, Deadlift 3×5, Lunges 3×10
  - **Day 3 (Upper Pull):** Pull-ups 4×8, Rows 3×10, Face pulls 3×15
- Format: PDF or in-app list

**3. Exercise Video Library (20 Core Movements)**
- Content:
  - Squat, Deadlift, Bench press, Overhead press, Pull-up
  - Row, Lunge, Plank, Push-up, Dip
  - Hip thrust, RDL, Lat pulldown, Leg press, Calf raise
  - Face pull, Bicep curl, Tricep extension, Lateral raise, Leg curl
- Format: 1-2 min videos (form cues, common mistakes)
- Source: Film in-house ($3K: rent gym, hire PT model, videographer) OR license from ExRx.net

---

#### Premium (195 kr/mån)

**4. Personalized Workout Programs (3/4/5-day Splits)**
- Input: ACTN3, ACE, COL1A1 (injury risk), training goal (strength vs hypertrophy vs fat loss)
- Output: Custom program with progressive overload
- Example (Strength, 4-day):
  - **Day 1 (Lower Power):** Squat 5×5 @ 85%, Deadlift 3×3 @ 90%
  - **Day 2 (Upper Power):** Bench 5×5 @ 85%, OHP 4×6 @ 80%
  - **Day 3 (Rest/Cardio):** 20 min LISS (if ADRB2 Arg/Arg for fat burn)
  - **Day 4 (Lower Hypertrophy):** Squat 4×10 @ 70%, RDL 3×12, Leg curl 3×15
  - **Day 5 (Upper Hypertrophy):** Bench 4×10, Rows 4×10, Accessories
- Progressive Overload: Each week, increase weight 2.5% or add 1 rep

**5. Full Exercise Video Library (200+ Exercises)**
- Same 20 core + 180 variations/accessories
- Source: License from FitBot or Trainerize ($5K/year) OR film ($15K one-time)

**6. Progress Tracking**
- Features:
  - Log sets/reps/weight per exercise
  - Auto-calculate 1RM (one-rep max) using Epley formula
  - Track volume over time (sets × reps × weight)
  - Deload week recommendations (every 4-6 weeks based on volume)
- Tech: Database schema
  ```sql
  CREATE TABLE workout_logs (
      user_id INT,
      date DATE,
      exercise VARCHAR(50),
      sets INT,
      reps INT,
      weight DECIMAL,
      rpe INT  -- Rate of Perceived Exertion (1-10)
  );
  ```
- Dashboard: Charts (volume trend, 1RM progression)

**7. Monthly Program Updates**
- Auto-generate new program every 4 weeks (avoid plateaus)
- Logic:
  - If volume increased >10% → deload week (reduce volume 40%)
  - If 1RM stalled for 3 weeks → switch exercise variation (e.g., squat → front squat)
  - If COL1A1 T/T (high injury risk) → add mobility work (hip flexor stretch, thoracic rotation)

**8. Injury Prevention Tips (Personalized to COL1A1)**
- COL1A1 T/T (high risk):
  - Warm-up: 10 min (foam rolling, dynamic stretching)
  - Avoid: Explosive movements until 6 months training (no box jumps, Olympic lifts)
  - Add: Collagen supplement (10g/day, helps tendon health)
- COL1A1 G/G (low risk):
  - Standard warm-up (5 min)
  - Can do explosive work (power cleans, plyometrics)

---

### Development Plan (Month 10-11)

**Month 10 Week 1-2: Workout Generator Algorithm (40K)**
- This is the most complex part (why 100K budget vs 50K for sleep)
- ML model training:
  - Input: ACTN3, ACE, COL1A1, PPARGC1A, ADRB2, training_goal, days_per_week
  - Output: Exercise selection, sets, reps, weight %
  - Training data: Scrape 500+ workout programs from T-Nation, StrongerByScience, etc.
  - Model: Random Forest or Neural Network (TensorFlow)
- Progressive overload logic (auto-increase weight)
- Deload logic (detect volume spikes)

**Month 10 Week 3-4: Exercise Database (15K)**
- Option A: License from FitBot ($5K/year, includes videos) ← **RECOMMENDED**
- Option B: Build in-house (film 200 videos $15K)
- Database schema:
  ```sql
  CREATE TABLE exercises (
      id INT PRIMARY KEY,
      name VARCHAR(100),
      category VARCHAR(50),  -- compound, isolation, cardio
      muscle_group VARCHAR(50),  -- chest, back, legs, etc.
      video_url VARCHAR(200),
      difficulty VARCHAR(20)  -- beginner, intermediate, advanced
  );
  ```

**Month 11 Week 1-2: Progress Tracking Backend (20K)**
- Build API endpoints:
  - `POST /workout/log` (log sets/reps/weight)
  - `GET /workout/history?exercise=squat` (retrieve past logs)
  - `GET /workout/stats` (1RM, volume trend)
- Database: PostgreSQL (workout_logs table)
- Calculations: 1RM formula, volume calculation

**Month 11 Week 3-4: Frontend + Dashboard (25K)**
- React/React Native components:
  - Workout plan view (today's exercises)
  - Log workout (input sets/reps/weight)
  - Progress charts (Chart.js: volume over time, 1RM trend)
- Mobile considerations: Offline mode (log at gym without WiFi, sync later)

**Total: 100K** (40 + 15 + 20 + 25)

---

### Testing & QA (Month 12)

**Beta Test:**
- Recruit: 50 customers (mix of beginners and experienced lifters)
- Duration: 4 weeks (1 training block)
- Feedback:
  - "Was the program appropriate for your level?" (Yes/No)
  - "Did you see progress?" (Yes/No, how much)
  - "Was progress tracking easy to use?" (1-5 scale)

**Bug Testing:**
- Offline mode (does data sync correctly when back online?)
- Edge cases (what if user logs 0 reps? Negative weight?)
- Performance (does dashboard load quickly with 1000+ logged workouts?)

---

## 🍽️ MEAL PLANNING (Month 10-11, 50K Budget)

### DNA-Matching Logic

**Not SNP-specific, but uses existing DNA insights:**
- MTHFR+ → High-folate recipes (dark leafy greens, lentils, liver)
- APOE4+ → Low saturated fat (avoid butter, red meat, focus on fish)
- Lactose intolerant (LCT) → Dairy-free recipes
- Gluten sensitivity (HLA-DQ2/DQ8) → Gluten-free recipes

---

### Features

#### Basic (FREE)

**1. 3× DNA-Matched Recipes per Week (Dinners Only)**
- Content: 3 dinner recipes (Monday, Wednesday, Friday)
- Example (MTHFR+):
  - Monday: "Lentil & Spinach Curry (high folate)"
  - Wednesday: "Salmon with Broccoli & Quinoa (omega-3, B-vitamins)"
  - Friday: "Chicken Stir-Fry with Bok Choy (folate, lean protein)"
- Format: Email (text recipe) or in-app

**2. Basic Grocery List**
- Manual: List of ingredients for 3 recipes (not organized)
- Example: "Lentils, spinach, coconut milk, salmon, broccoli, quinoa, chicken, bok choy, soy sauce"

---

#### Premium (195 kr/mån)

**3. 7× Weekly Meal Plans (All Meals)**
- Content: Breakfast, lunch, dinner, 2 snacks × 7 days = 35 meals
- Customizable:
  - Dietary preferences (vegetarian, vegan, keto, paleo)
  - Calories (1,500 / 2,000 / 2,500 / 3,000)
  - Macros (high protein for muscle gain, low carb for fat loss)
- DNA-matched:
  - MTHFR+ → every day includes ≥1 high-folate food
  - APOE4+ → <7% saturated fat (vs standard 10%)
  - FADS1 (omega-3 conversion) → if poor converter, more fish (EPA/DHA direct)

**4. Auto-Generated Grocery Lists**
- Organized by store section:
  - Produce: Spinach (200g), broccoli (300g), ...
  - Protein: Chicken breast (1kg), salmon (500g), ...
  - Pantry: Quinoa (500g), lentils (500g), ...
- Integration (Future Phase 2):
  - Mat.se API (one-click order)
  - ICA, Coop APIs (if available)

**5. Recipe Video Tutorials**
- Content: 50 core recipes, 5-10 min cooking videos
- Example: "How to Cook Perfect Salmon (5 min)"
- Source: Film in-house (rent kitchen, hire chef, $10K) OR license from Tasty/Buzzfeed B2B

**6. Nutrition Macro Tracking**
- Features:
  - Auto-log meals from meal plan (macros pre-calculated)
  - Manual log (if eating off-plan)
  - Daily summary: "Today: 150g protein, 200g carbs, 60g fat (target: 160/180/65)"
- Integration with dietist:
  - If macros consistently off-target → dietist gets alert → schedule call

---

### Development Plan (Month 10-11)

**Month 10 Week 1-2: Recipe Database (15K)**
- Source recipes:
  - Option A: License from Yummly or Edamam API ($5K/year, 500K recipes)
  - Option B: Create in-house (hire nutritionist to write 100 recipes, $10K)
- Tag recipes:
  - `high_folate`, `low_sat_fat`, `gluten_free`, `dairy_free`, `vegan`, etc.
- Store in database:
  ```sql
  CREATE TABLE recipes (
      id INT PRIMARY KEY,
      name VARCHAR(200),
      ingredients JSONB,  -- [{"item": "spinach", "amount": "200g"}]
      macros JSONB,  -- {"protein": 30, "carbs": 45, "fat": 10}
      tags VARCHAR[],  -- ["high_folate", "vegetarian"]
      instructions TEXT
  );
  ```

**Month 10 Week 3-4: Meal Plan Generator (20K)**
- Algorithm:
  - Input: DNA tags (e.g., MTHFR+, APOE4+), calories, dietary preference
  - Output: 7-day meal plan (35 meals)
  - Logic:
    - Filter recipes by tags (if APOE4+, exclude high sat-fat)
    - Optimize for macro targets (linear programming: minimize deviation)
    - Ensure variety (no repeat recipes within 7 days)
- Tech: Python (PuLP library for optimization) or simpler rule-based (if/else)

**Month 11 Week 1-2: Grocery List Generator (5K)**
- Aggregate ingredients across 7 days
- Group by category (produce, protein, pantry)
- Quantity summation (if spinach in 3 recipes, total 600g)

**Month 11 Week 3-4: Macro Tracking Frontend (10K)**
- UI: Daily log (breakfast, lunch, dinner, snacks)
- Charts: Macro breakdown (protein/carbs/fat pie chart)
- Integration: Pre-fill from meal plan (one-tap logging)

**Total: 50K** (15 + 20 + 5 + 10)

---

### Testing & QA (Month 12)

**Beta Test:**
- Recruit: 30 customers (Premium/Elite only, need dietist baseline)
- Duration: 2 weeks (easier to test than 4-week workout program)
- Feedback:
  - "Did you enjoy the recipes?" (Yes/No, which ones?)
  - "Was grocery list accurate?" (Any missing/wrong items?)
  - "Would you pay 195 kr/mån?" (Yes/No + reason)

---

## 🔗 API INTEGRATIONS (WEARABLES)

### Oura Ring

**Documentation:** https://cloud.ouraring.com/docs/
**Cost:** Free (developer tier, up to 100 users), then $100/month (up to 5,000 users)

**OAuth Flow:**
1. User clicks "Connect Oura" in app
2. Redirect to Oura login → user authorizes
3. Receive access token → store in database
4. Periodic sync: `GET /v2/usercollection/daily_sleep` every morning

**Data Retrieved:**
- Sleep scores, duration, efficiency
- Sleep stages (deep, REM, light, awake)
- HRV (average during sleep)
- Resting heart rate

**Error Handling:**
- Token expired → refresh token (OAuth 2.0 flow)
- User revokes access → disable sync, notify user

---

### Whoop

**Documentation:** https://developer.whoop.com/
**Cost:** Free (apply for developer access)

**OAuth Flow:** Similar to Oura

**Data Retrieved:**
- Recovery score (0-100%)
- Sleep performance
- Strain (daily exertion)
- HRV

---

### Apple Health (HealthKit)

**Documentation:** https://developer.apple.com/documentation/healthkit
**Cost:** Free (requires iOS app)

**Integration:**
- NOT via web API (must use native iOS HealthKit framework)
- Requires: React Native iOS app (not just web)
- User authorizes in iOS Settings → app can read sleep, HRV, workouts

**Data Retrieved:**
- Sleep stages (watchOS 10+)
- HRV samples
- Workouts (duration, calories, heart rate)
- Steps, active energy

**Limitation:** Only works for iOS users (60% of Swedish market)

---

### Garmin

**Documentation:** https://developer.garmin.com/health-api/overview/
**Cost:** $2,000/year (enterprise tier)

**OAuth Flow:** Similar to Oura/Whoop

**Data Retrieved:**
- Body Battery (proprietary recovery metric)
- Sleep score
- Stress levels
- VO2 max estimate

**Why Garmin:**
- Popular among serious athletes (triathletes, runners)
- More accurate GPS/workout tracking than Oura/Whoop

---

### Integration Timeline

**Month 8 (During Sleep/Stress Dev):**
- Apply for Oura developer access (1 week approval)
- Apply for Whoop developer access (1 week approval)
- Sign Garmin Health API contract ($2K/year)

**Month 9:**
- Implement OAuth flows (2 weeks)
- Test data syncing (1 week)
- Error handling (token refresh, user revocation)

**Month 10:**
- Apple HealthKit (requires iOS app dev, 3-4 weeks)
- Alternatively: Phase 2 (launch web first, iOS app later)

---

## 💰 BUDGET BREAKDOWN

### Development Costs (One-Time, Year 1)

| Add-On | Development | APIs/Licenses | Total |
|--------|-------------|---------------|-------|
| Sleep Optimization | 40K (algorithms, reports) | 10K (Oura, Whoop, Garmin APIs) | **50K** |
| Stress Management | 35K (algorithms, HRV integration) | 15K (Calm B2B meditation library) | **50K** |
| Workout Plan | 75K (ML model, progress tracking) | 25K (FitBot video library, hosting) | **100K** |
| Meal Planning | 40K (meal plan generator, macros) | 10K (Yummly API, recipe licenses) | **50K** |
| **TOTAL** | **190K** | **60K** | **250K** |

---

### Recurring Costs (Annual, Year 1)

| Item | Cost/Year |
|------|-----------|
| Oura API | 1,200 (100/mån after free tier) |
| Whoop API | 0 (free developer tier) |
| Garmin Health API | 2,000 |
| Apple HealthKit | 0 (free, but requires iOS app dev) |
| Calm B2B (meditation) | 10,000 |
| FitBot (exercise videos) | 5,000 |
| Yummly API (recipes) | 5,000 |
| Hosting (AWS S3, CloudFront) | 1,200 (100/mån) |
| **TOTAL** | **24,400 SEK/year** (~2K/mån) |

**Margin Impact:**
- Add-on revenue Year 1: 304K
- Recurring costs: 24K
- **Net after recurring: 280K** (92% margin)

---

### Staffing (Year 2)

| Role | Time | Salary | When |
|------|------|--------|------|
| ML Engineer (Contract) | 3 months | 50K/mån | Month 10-12 (Workout AI) |
| iOS Developer (Contract) | 2 months | 60K/mån | Month 10-11 (HealthKit) |
| Stress Coach (Part-Time) | 20h/week | 15K/mån | Month 13+ (Year 2) |
| **Year 1 Total** | | **270K** | |

**Note:** ML Engineer & iOS dev are one-time (Year 1 only). Stress coach ongoing (Year 2+).

---

## 📊 ROI ANALYSIS

### Year 1

**Investment:**
- Development: 250K
- Staffing (ML, iOS): 270K
- **Total: 520K**

**Revenue:**
- Add-ons (Month 7-12): 304K
- **ROI Year 1:** 304K / 520K = **58%** (will be profitable in Year 2)

---

### Year 2

**Investment:**
- Recurring costs: 24K (APIs, hosting)
- Stress coach: 15K × 12 = 180K
- Iteration (bug fixes, new features): 50K
- **Total: 254K**

**Revenue:**
- Add-ons (B2C): 1,500K (1,200 customers × ~40% adoption × 195 kr avg × 12 mån)
- **ROI Year 2:** 1,500K / 254K = **5.9×**

---

### Cumulative (Year 1-2)

**Total Investment:** 520K + 254K = 774K
**Total Revenue:** 304K + 1,500K = 1,804K
**ROI:** 1,804K / 774K = **2.3×** (233% return)

---

## ✅ NEXT STEPS (IMMEDIATE ACTIONS)

### Month 1-2 (Pre-Development)

- [ ] **Hire ML Engineer:** Post on LinkedIn, target PhD students (50K/mån, 3-month contract)
- [ ] **Hire iOS Developer:** For HealthKit integration (60K/mån, 2-month contract)
- [ ] **Apply for APIs:**
  - Oura developer access (1 week)
  - Whoop developer access (1 week)
  - Garmin Health API contract (sign $2K/year)
- [ ] **License Content:**
  - Calm B2B meditation library ($10K/year)
  - FitBot exercise video library ($5K/year)
  - Yummly recipe API ($5K/year)

---

### Month 7-8 (Sleep + Stress Development)

- [ ] **Week 1-4:** Sleep window algorithm, caffeine cutoff, email automation
- [ ] **Week 5-8:** Stress assessment, meditation integration, supplement logic
- [ ] **Week 5-8 (Parallel):** API integrations (Oura, Whoop, Garmin, Apple)
- [ ] **Week 9:** Beta test (50 customers each for Sleep and Stress)

---

### Month 9 (Beta Testing & Iteration)

- [ ] **Week 1-2:** Collect feedback (surveys after 30 days)
- [ ] **Week 3-4:** Fix bugs (top 5 issues from beta)
- [ ] **Week 4:** Public launch prep (email campaign, in-app notifications)

---

### Month 10-11 (Workout + Meal Planning Development)

- [ ] **Week 1-4:** Workout AI model training, exercise database setup
- [ ] **Week 5-8:** Meal plan generator, recipe database, grocery lists
- [ ] **Week 5-8 (Parallel):** Progress tracking backend, macro tracking frontend
- [ ] **Week 9:** Beta test (50 customers Workout, 30 customers Meal Planning)

---

### Month 12 (Launch + Monitor)

- [ ] **Week 1:** Public launch (email all 650 customers)
- [ ] **Week 2-4:** Monitor metrics:
  - Adoption: Target 35% use ≥1 premium add-on
  - Ratings: Target 4.5+ stars
  - Conversion: Target 25-30% basic → premium
- [ ] **Month 12 End:** Revenue check (target 300K from add-ons Year 1)

---

**Dokumentversion:** 1.0
**Skapad:** 2026-01-19
**Författare:** Claude Sonnet 4.5 + Rasmus Persson
**För:** Engineering & Product Development
