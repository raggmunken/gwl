# Final stack decision (free/low-cost, leveraging existing keys)

Date: 19 Sep 2025

We will prioritize free tiers and reuse your existing Supabase project from `.env` to reduce cost and complexity.

## Frontend & Hosting
- Next.js 14 (App Router, TypeScript), Tailwind, shadcn/ui — Free
- Vercel Pro (available) — use Pro features (Edge Network, analytics, concurrency); free-tier assumptions not required

## Content Management (CMS)
- Sanity (Free dev plan) for structured, localized content with preview
  - Rationale: Excellent authoring UX, roles, and component schemas; minimizes custom build time

## Database & Storage
- Supabase Postgres (Free tier) — reuse existing credentials in `.env`
  - Prisma ORM for type-safe DB access
  - Enable `pg_trgm` extension for Search v1 (typo-tolerant)
- Supabase Storage (Free tier) for assets/PDF reports initially
  - Optional: migrate to Cloudflare R2 later for cost/performance

## Auth & Security
- NextAuth (Free) with Email (Resend) and optional OIDC
- TOTP MFA via `otplib` (Free)

## Payments & Subscriptions
- Stripe (Free to start; per-transaction fees) + Stripe Tax + Klarna

## Email
- Resend (Free tier) for transactional email
- Mailchimp (Free tier) for marketing (optional initially)

## Consent & Analytics
- Cookiebot (Free for small site) for CMP/TCF compatibility
- GA4 (Free) + optional Umami self-host later

## CRM & Support
- HubSpot CRM (Free) for leads; shared inbox for support (Free)

## Calendaring
- Cal.com (Free) with embedded booking

## Monitoring & Logs
- Sentry (Free tier), UptimeRobot (Free), basic logs via Vercel + browser console

## Search
- Phase 1: Postgres FTS + `pg_trgm` (Free)
- Phase 2: Consider Typesense (OSS) or Algolia (Free dev tier)

Notes
- This decision supersedes `stack_free_choices.md` where they differ; both remain for reference.
- All selections align to the business plan and the design docs while minimizing cost and setup overhead.

## Locale & currency defaults
- Default language: `sv-SE` (Swedish). Secondary locale: `en-US`.
- Default currency: `SEK`. For English locale/routes, display prices in `EUR`.
- Implementation:
  - Next.js i18n routing with `next-intl` (or similar) to serve `/sv/...` and `/en/...`.
  - Maintain Stripe Price objects per currency (SEK and EUR) and select by active locale.
  - Format with `Intl.NumberFormat` based on locale and currency.
  - Hreflang tags and localized metadata as per `public_site_page_blueprints.md`.

## Vitamin subscription pricing (recurring, monthly)
- Basic: 400 SEK
- Medium: 500 SEK
- Full: 600 SEK
- Stripe setup:
  - Create Products: `Vitamin Subscription (Basic|Medium|Full)`.
  - Create recurring Prices in SEK (monthly) for each.
  - Create EUR Prices for each (amounts to be confirmed: mirror numbers or set explicit EUR pricing).

## Optional DB alternative
- Firebase (Firestore) can be used if we decide it better fits realtime or operational characteristics. Current choice: Supabase (Postgres) for strong relational needs (orders, kits, results, plans).
  - Switch path (high level): replace Prisma/Postgres models with Firestore collections; adjust API routes; migrate auth/session adapters; re-implement search (Algolia or Typesense).

## Documentation
- Next.js: https://nextjs.org/docs
- Vercel: https://vercel.com/docs
- Tailwind CSS: https://tailwindcss.com/docs
- shadcn/ui: https://ui.shadcn.com/docs
- Sanity CMS: https://www.sanity.io/docs
- Supabase: https://supabase.com/docs
- Prisma ORM: https://www.prisma.io/docs
- Auth.js (NextAuth): https://authjs.dev/reference/nextjs
- TOTP (MFA) example (Supabase guide): https://supabase.com/docs/guides/auth/auth-mfa/totp
- Stripe: https://stripe.com/docs
- Klarna via Stripe: https://stripe.com/docs/payments/klarna
- Resend (email): https://resend.com/docs/introduction
- Mailchimp (marketing): https://mailchimp.com/developer/
- Cookiebot: https://www.cookiebot.com/en/developer/
- GA4: https://developers.google.com/analytics/devguides/collection/ga4
- HubSpot CRM: https://knowledge.hubspot.com/crm
- Cal.com: https://cal.com/docs/developing/introduction
- Sentry: https://docs.sentry.io/
- Typesense: https://typesense.org/docs/
- Algolia: https://www.algolia.com/doc/
- Cloudflare R2: https://developers.cloudflare.com/r2/
- OpenTelemetry: https://opentelemetry.io/docs/
- UptimeRobot: https://uptimerobot.com/api/
- Firebase (optional): https://firebase.google.com/docs
