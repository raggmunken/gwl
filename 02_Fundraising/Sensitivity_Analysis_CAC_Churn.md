# SENSITIVITY ANALYSIS: CAC & CHURN
## Financial Model Stress-Testing

**Datum:** 2026-01-18
**Version:** 1.0
**För:** Investerare & Strategisk Planering
**Typ:** Financial Risk Analysis

---

## EXECUTIVE SUMMARY

Denna analys testar vår finansiella modell under olika CAC (Customer Acquisition Cost) och churn-scenarios.

**Base Case Assumptions:**
- CAC: 1,713 SEK (blended)
- Monthly Churn: 7% (14.3 months LTV)
- CLV: 9,820 SEK
- Break-Even: 368 customers (Month 14-16)

**Key Finding:**
- **Model är robust** vid moderate stress (CAC 2,500 SEK, churn 10%)
- **Model breaks** vid severe stress (CAC > 3,500 SEK OR churn > 15%)
- **Pivot-trösklar identifierade** för varje failure mode

---

## 📊 CAC SENSITIVITY ANALYSIS

### Scenario 1: Base Case (CAC 1,713 SEK)

**Assumptions:**
- Google Ads: 2,400 SEK CAC (40% av mix)
- Facebook Ads: 2,100 SEK CAC (30% av mix)
- Organic: 200 SEK CAC (10% av mix)
- Affiliate: 1,545 SEK CAC (20% av mix)
- **Blended CAC:** 1,713 SEK

**Unit Economics:**
```
CLV: 9,820 SEK
CAC: 1,713 SEK
CLV/CAC: 5.7×
Payback Period: 3.2 months
```

**Break-Even:**
- Customers needed: 368
- Timeline: Month 14-16
- Revenue at break-even: 3.6M SEK

**Verdict:** ✅ Excellent unit economics

---

### Scenario 2: Moderate CAC (2,500 SEK)

**Assumption:** CAC 46% högre än base case

**Why This Happens:**
- Google/Facebook ads more expensive than expected
- Lower conversion rates (2% instead of 3%)
- Premium product = harder to sell

**Unit Economics:**
```
CLV: 9,820 SEK
CAC: 2,500 SEK
CLV/CAC: 3.9×
Payback Period: 4.7 months
```

**Break-Even:**
- Customers needed: 520
- Timeline: Month 18-20
- Revenue at break-even: 5.1M SEK

**Impact on Fundraising:**
- 5M seed INSUFFICIENT
- Need +2M bridge Month 15
- Total capital: 7M SEK

**Verdict:** ⚠️ Tighter but workable. Need bridge financing.

---

### Scenario 3: Pessimistic CAC (3,500 SEK)

**Assumption:** CAC 2× högre än base case

**Why This Happens:**
- High-ticket product in lågkonjunktur = very hard to sell
- Conversion rates < 1%
- Forced to use expensive channels

**Unit Economics:**
```
CLV: 9,820 SEK
CAC: 3,500 SEK
CLV/CAC: 2.8×
Payback Period: 6.6 months
```

**Break-Even:**
- Customers needed: 730
- Timeline: Month 24+
- Revenue at break-even: 7.2M SEK

**Impact on Fundraising:**
- 5M seed VERY INSUFFICIENT
- Need +5M Series A much sooner (Month 12-15)
- Total capital: 10M SEK
- Risk: Series A hard to raise without traction

**Verdict:** ⚠️ Model is stressed. Must consider pivot.

---

### Scenario 4: Disaster CAC (5,000 SEK)

**Assumption:** CAC 3× högre än base case

**Why This Happens:**
- Premium pricing totally wrong for market
- No product-market fit
- Burning money on ads with no returns

**Unit Economics:**
```
CLV: 9,820 SEK
CAC: 5,000 SEK
CLV/CAC: 2.0×
Payback Period: 9.4 months
```

**Break-Even:**
- Customers needed: 1,050
- Timeline: Month 36+
- Revenue at break-even: 10.3M SEK

**Impact on Fundraising:**
- Model BROKEN
- Would need 15M+ SEK to reach break-even
- Investors will not fund

**Verdict:** ❌ Must pivot immediately. Lower price or change model entirely.

---

## CAC SCENARIO COMPARISON TABLE

| Scenario | CAC | CLV/CAC | Break-Even Customers | Break-Even Month | Additional Funding Needed | Verdict |
|----------|-----|---------|----------------------|------------------|---------------------------|---------|
| **Base Case** | 1,713 SEK | 5.7× | 368 | Month 14-16 | 0 (5M seed OK) | ✅ Excellent |
| **Moderate** | 2,500 SEK | 3.9× | 520 | Month 18-20 | +2M bridge Month 15 | ⚠️ Tight but OK |
| **Pessimistic** | 3,500 SEK | 2.8× | 730 | Month 24+ | +5M Series A sooner | ⚠️ Stressed |
| **Disaster** | 5,000 SEK | 2.0× | 1,050 | Month 36+ | +10M+ (unfundable) | ❌ Pivot required |

---

## 🚨 CAC PIVOT DECISION TREE

```
Pre-Seed Test (Month 1-3, 50K ads budget)
    |
    ├─ CAC < 2,000 SEK
    |   └─> ✅ Proceed to seed round with confidence
    |
    ├─ CAC 2,000-3,000 SEK
    |   └─> ⚠️ Proceed but revise financial model (need bridge)
    |
    └─ CAC > 3,000 SEK
        └─> ❌ STOP seed fundraising
            |
            ├─ Option A: Lower price to 2,995 SEK (DNA-only)
            ├─ Option B: Focus B2B (lower CAC)
            └─ Option C: Pivot to different model
```

---

## 📉 CHURN SENSITIVITY ANALYSIS

### Scenario 1: Base Case (7% Monthly Churn)

**Assumptions:**
- Monthly churn: 7%
- Average customer lifetime: 14.3 months
- Retention drivers: Personalization, dietist follow-up, blood tests

**CLV Calculation:**
```
DNA-test margin: 2,170 SEK
Subscription margin: 402 SEK/month × 14.3 months = 5,749 SEK
Upsells: 901 SEK
Total CLV: 9,820 SEK
```

**Break-Even:**
- Customers needed: 368
- Timeline: Month 14-16

**Verdict:** ✅ Model works

---

### Scenario 2: Moderate Churn (10% Monthly)

**Assumption:** 43% högre churn än base case

**Why This Happens:**
- Customers don't see results fast enough
- Generic supplement fatigue (even if personalized)
- Price sensitivity (cutting "nice-to-have" expenses)

**CLV Calculation:**
```
Average customer lifetime: 10 months
DNA-test margin: 2,170 SEK
Subscription margin: 402 SEK/month × 10 months = 4,020 SEK
Upsells: 950 SEK
Total CLV: 7,140 SEK
```

**Break-Even:**
- Customers needed: 520
- Timeline: Month 18-20
- Additional funding: +2M bridge Month 15

**Verdict:** ⚠️ Tight but workable. Need better retention tactics.

---

### Scenario 3: Pessimistic Churn (15% Monthly)

**Assumption:** 2× högre churn än base case

**Why This Happens:**
- Supplement prenumerationer typical behavior (3-4 months avg)
- No perceived value from personalization
- Economic downturn → cut subscriptions

**CLV Calculation:**
```
Average customer lifetime: 6.7 months
DNA-test margin: 2,170 SEK
Subscription margin: 402 SEK/month × 6.7 months = 2,693 SEK
Upsells: 157 SEK
Total CLV: 5,020 SEK
```

**Break-Even:**
- Customers needed: 780
- Timeline: Month 24+
- Additional funding: +5M Series A sooner

**Verdict:** ❌ Model broken. Must pivot to non-subscription.

---

### Scenario 4: Disaster Churn (20% Monthly)

**Assumption:** 3× högre churn än base case

**Why This Happens:**
- Complete product failure (no results)
- Customers cancel after Month 1-2
- Retention tactics don't work

**CLV Calculation:**
```
Average customer lifetime: 5 months
DNA-test margin: 2,170 SEK
Subscription margin: 402 SEK/month × 5 months = 2,010 SEK
Upsells: -280 SEK (refunds)
Total CLV: 3,900 SEK
```

**Break-Even:**
- Customers needed: 1,050
- Timeline: Month 36+
- Model unfundable

**Verdict:** ❌ Pivot immediately to DNA-only (no subscription).

---

## CHURN SCENARIO COMPARISON TABLE

| Scenario | Monthly Churn | Avg LTV (months) | CLV | Break-Even Customers | Break-Even Month | Verdict |
|----------|---------------|------------------|-----|----------------------|------------------|---------|
| **Optimistic** | 5% | 20 months | 13,560 SEK | 260 | Month 10-12 | ✅ Amazing |
| **Base Case** | 7% | 14.3 months | 9,820 SEK | 368 | Month 14-16 | ✅ Good |
| **Moderate** | 10% | 10 months | 7,140 SEK | 520 | Month 18-20 | ⚠️ OK but tight |
| **Pessimistic** | 15% | 6.7 months | 5,020 SEK | 780 | Month 24+ | ❌ Broken |
| **Disaster** | 20% | 5 months | 3,900 SEK | 1,050 | Month 36+ | ❌ Must pivot |

---

## 🚨 CHURN PIVOT DECISION TREE

```
Beta Study (Month 6-12, 81 customers)
    |
    ├─ Retention > 80% at Month 6
    |   └─> ✅ Model validated, continue subscription
    |
    ├─ Retention 60-80% at Month 6
    |   └─> ⚠️ Improve retention tactics (more dietist follow-up)
    |
    └─ Retention < 60% at Month 6
        └─> ❌ Pivot to non-subscription model
            |
            ├─ Option A: DNA-only (2,995 SEK one-time)
            ├─ Option B: 3-month supply (no recurring)
            └─ Option C: Annual plan (12-month prepay)
```

---

## 🔄 COMBINED CAC + CHURN STRESS TEST

### Scenario Matrix: What Happens When BOTH Go Wrong?

| Churn → <br> CAC ↓ | 7% (Base) | 10% (Moderate) | 15% (Pessimistic) |
|---------------------|-----------|----------------|-------------------|
| **1,713 SEK (Base)** | ✅ 368 customers<br>Month 14-16 | ⚠️ 520 customers<br>Month 18-20 | ❌ 780 customers<br>Month 24+ |
| **2,500 SEK (Moderate)** | ⚠️ 520 customers<br>Month 18-20 | ⚠️ 730 customers<br>Month 22-24 | ❌ 1,100 customers<br>Month 30+ |
| **3,500 SEK (Pessimistic)** | ⚠️ 730 customers<br>Month 24+ | ❌ 1,050 customers<br>Month 30+ | ❌ Model broken<br>Unfundable |

**Key Insight:**
- **Green Zone** (✅): Base case or ONE moderate stress → Model works
- **Yellow Zone** (⚠️): ONE moderate stress + ONE base OR two moderate → Tight but OK with bridge
- **Red Zone** (❌): BOTH moderate/pessimistic → Model broken, must pivot

---

## 💰 FUNDRAISING IMPLICATIONS

### Scenario A: Base Case (CAC 1,713 SEK, Churn 7%)

**Capital Needed:**
- Seed: 5M SEK
- Series A (Month 18): 10M SEK
- Total: 15M SEK

**Founder Equity at Exit (150M SEK):**
- Post-Seed: 82%
- Post-Series A: 69.7%
- Exit value: 104.5M SEK

---

### Scenario B: Moderate Stress (CAC 2,500 SEK, Churn 10%)

**Capital Needed:**
- Seed: 5M SEK
- Bridge (Month 15): +2M SEK @ 10% equity
- Series A (Month 20): 10M SEK @ 15% equity
- Total: 17M SEK

**Founder Equity at Exit (150M SEK):**
- Post-Seed: 82%
- Post-Bridge: 73.8%
- Post-Series A: 62.7%
- Exit value: 94M SEK

**Difference vs Base:** -10.5M SEK founder equity

---

### Scenario C: Severe Stress (CAC 3,500 SEK, Churn 15%)

**Capital Needed:**
- Seed: 5M SEK
- Bridge (Month 12): +3M SEK @ 15% equity
- Series A (Month 18): 12M SEK @ 18% equity
- Total: 20M SEK

**Founder Equity at Exit (150M SEK):**
- Post-Seed: 82%
- Post-Bridge: 69.7%
- Post-Series A: 57.2%
- Exit value: 85.8M SEK

**Difference vs Base:** -18.7M SEK founder equity

**Verdict:** ❌ At this point, pivot is better than raising more capital with heavy dilution.

---

## 🎯 EARLY WARNING INDICATORS

### CAC Warning Signs (Month 1-3 Pre-Seed Test)

**Green Flags (Proceed):**
- ✅ CAC < 2,000 SEK after 50K spend
- ✅ Conversion rate > 3% (landing page → signup)
- ✅ Cost-per-click < 15 SEK

**Yellow Flags (Revise Model):**
- ⚠️ CAC 2,000-3,000 SEK
- ⚠️ Conversion rate 2-3%
- ⚠️ Cost-per-click 15-25 SEK

**Red Flags (Stop or Pivot):**
- ❌ CAC > 3,000 SEK
- ❌ Conversion rate < 2%
- ❌ Cost-per-click > 25 SEK

---

### Churn Warning Signs (Month 6-12 Beta Study)

**Green Flags (Continue Subscription):**
- ✅ >80% retention at Month 3
- ✅ >70% retention at Month 6
- ✅ Customer NPS > 40

**Yellow Flags (Improve Retention):**
- ⚠️ 60-80% retention at Month 3
- ⚠️ 50-70% retention at Month 6
- ⚠️ Customer NPS 20-40

**Red Flags (Pivot to Non-Subscription):**
- ❌ <60% retention at Month 3
- ❌ <50% retention at Month 6
- ❌ Customer NPS < 20

---

## 📈 MITIGATION STRATEGIES

### If CAC Is Higher Than Expected:

**1. Lower Price Point**
- Launch DNA-Only tier (2,995 SEK)
- Lower CAC tolerance: Break-even at CAC < 1,670 SEK
- Sacrifice margin for volume

**2. B2B-First Strategy**
- Corporate wellness (8,500 SEK/employee)
- Lower CAC (500-800 SEK sales cycle)
- Bulk revenue stability

**3. Improve Conversion Rate**
- A/B test landing pages
- Add social proof (testimonials, case studies)
- Klarna payment plan (reduce perceived cost)

**4. Optimize Channel Mix**
- Shift from paid ads to content marketing (lower CAC)
- Build affiliate network (performance-based)
- PR & media coverage (free CAC)

---

### If Churn Is Higher Than Expected:

**1. Strengthen Retention Drivers**
- More frequent dietist check-ins (monthly vs quarterly)
- Gamification (track progress, achievements)
- Community building (private Facebook group)

**2. Outcome Tracking**
- Blood tests at Month 3 and 6 (show proof it works)
- Visual dashboards (energy, focus tracking)
- Before/after photos/data

**3. Churn Prevention Tactics**
- Pause option (instead of cancel)
- Discounts for long-term commitment (6-month prepay)
- Win-back campaigns (special offers for churned customers)

**4. Pivot to Non-Subscription**
- DNA-only (2,995 SEK one-time)
- 3-month supply (5,995 SEK, no recurring)
- Annual plan (9,980 SEK, 12-month prepay)

---

## ✅ CONCLUSION: MODEL ROBUSTNESS

**Our Financial Model:**
- **Robust** under moderate stress (CAC 2,500 SEK OR churn 10%)
- **Stressed** under severe single stress (CAC 3,500 SEK OR churn 15%)
- **Broken** under combined stress (CAC 3,500 SEK AND churn 15%)

**Key Takeaways:**
1. **We have room for error** → Model doesn't break with ONE moderate stress
2. **But not much** → If BOTH CAC and churn are worse, we must pivot quickly
3. **Early warning system** → Pre-seed test (Month 3) and beta study (Month 6-12) give us data to decide
4. **Pivot options ready** → DNA-only, B2B-first, non-subscription models all viable

**For Investors:**
- This is NOT a "hope for the best" model
- We have concrete thresholds and pivot plans
- Capital allocation prioritizes validation (test CAC, measure retention)
- If stress signals appear, we pivot BEFORE running out of money

---

**Dokumentversion:** 1.0
**Skapad:** 2026-01-18
**För:** Investerare, strategisk planering, risk analysis
**Relaterade dokument:** Due_Diligence_Response.md, Kostnadanalys.md, Affarsplan.md
