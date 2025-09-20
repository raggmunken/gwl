# Stripe Catalog Plan — SEK default, EUR for English

Date: 20 Sep 2025

Goal
- Configure Stripe Products/Prices for all sellable items with SEK as default currency, and create EUR prices for English locale.
- Subscriptions (vitamins) are recurring monthly.
- DNA kits and Check‑ups are one‑time payments.

Currencies & Locales
- sv-SE → SEK (default)
- en-US → EUR

Vitamin Subscriptions (recurring monthly)
- Basic: 400 SEK/month
- Medium: 500 SEK/month
- Full: 600 SEK/month

DNA Kits (one‑time)
- Stage 1: 1200 SEK
- Stage 2: 2000 SEK
- Stage 3: 2400 SEK

Check‑up Packages (one‑time)
- Health: 1300 SEK
- Longevity: 2200 SEK
- Cardiovascular: 1800 SEK
- Cognitive: 1600 SEK

Lookup Key Convention
- Use lowercase, kebab-case with currency suffix.
- Examples:
  - `vitamin-basic-monthly-sek`, `vitamin-basic-monthly-eur`
  - `dna-stage-1-sek`, `dna-stage-1-eur`
  - `checkup-health-sek`, `checkup-health-eur`

Steps (Dashboard UI)
1) Create Products
   - Vitamins (three separate products): "Vitamin Subscription — Basic", "— Medium", "— Full".
   - DNA Kits: "DNA Testing — Stage 1/2/3".
   - Check‑ups: "Check‑up — Health", "— Longevity", "— Cardiovascular", "— Cognitive".
   - Product type: Standard; tax behavior: inclusive (SE) if applicable.
   - Add descriptions and images.

2) Create Prices per Product
   - Vitamins: Recurring → Monthly; currency SEK; amount as defined; set `lookup_key` as above.
   - DNA/Check‑ups: One‑time; currency SEK; amount as defined; set `lookup_key`.
   - Create EUR prices for each product (same cadence for subs) with `lookup_key` ending in `-eur`.
     - If EUR price amounts aren’t yet finalized, create placeholder prices and set them to Inactive for now.

3) Taxes
   - Enable Stripe Tax. Set default tax registration country to SE.
   - For EUR buyers (English locale), ensure VAT rules are correct (OSS/IOSS if applicable). You can still charge in EUR even if registered in SE.

4) Webhooks (Test mode first)
   - Add endpoint URL (e.g., `https://<preview-deploy>/api/stripe/webhook`).
   - Subscribe to: `checkout.session.completed`, `invoice.payment_succeeded`, `invoice.payment_failed`, `customer.subscription.*`.
   - Copy `STRIPE_WEBHOOK_SECRET` to `.env`.

5) Server Integration (outline)
   - A catalog map in DB or config linking product slugs → Stripe Price IDs per currency.
   - Checkout session creation picks the Price ID based on current locale → currency mapping.
   - Webhook handler upserts `Order` / `Subscription` and reconciles totals.

Command-line (Stripe CLI)
- Optional: use Stripe CLI to create prices:
```bash
# Example: Vitamin Basic SEK monthly (400 SEK)
stripe prices create \
  --currency=sek \
  --unit-amount=40000 \
  --recurring="interval=month" \
  --product="{{PRODUCT_ID_VITAMIN_BASIC}}" \
  --lookup-key=vitamin-basic-monthly-sek

# Example: Vitamin Basic EUR monthly placeholder (inactive)
stripe prices create \
  --currency=eur \
  --unit-amount=XXXX \
  --recurring="interval=month" \
  --product="{{PRODUCT_ID_VITAMIN_BASIC}}" \
  --active=false \
  --lookup-key=vitamin-basic-monthly-eur
```

Acceptance Criteria
- All items have SEK and EUR Prices (EUR may be inactive pending amounts).
- Lookup keys unique, stable, and referenced by backend.
- Webhooks deliver and are verified with secret.

Open Decision
- Confirm EUR amounts (fixed list vs. conversion from SEK). Until confirmed, keep EUR prices inactive and display notice on English pages per `l10n_currency_plan.md`.

References
- Stripe: https://stripe.com/docs
- Prices guide: https://stripe.com/docs/billing/prices-guide
- Stripe Tax: https://stripe.com/docs/tax
- Klarna: https://stripe.com/docs/payments/klarna
