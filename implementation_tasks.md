# Genetic Wellness Labs — Implementation Plan (Iterative, Low-Cost Stack)

Date: 19 Sep 2025
Sources: `pages_design/enterprise_web_and_service_plan.md`, `pages_design/public_site_page_blueprints.md`, `pages_design/portal_flows_and_wireframes.md`, `pages_design/stack_decision.md`

Guiding principles
- Use free/low‑cost services and reuse your existing Supabase project from `.env`.
- Ship incrementally with clear acceptance criteria per iteration.
- Each iteration lists at least 10 granular tasks, "why" notes, and done criteria.

---

## Iteration 1 — Foundations & Accounts (10 tasks)
Goal: Prepare all accounts, environments, and secrets to unblock build.

1) Create/confirm Vercel account and org
- Why: hosting + CI/CD on free tier.
- Done: org exists and you can add a project.

2) Confirm Supabase project (already present in `.env`)
- Why: DB + storage free tier.
- Done: You can log in and see the database; keep credentials safe.

3) Enable `pg_trgm` extension on Supabase
- Why: typo‑tolerant search v1 using Postgres.
- How: Supabase SQL editor → `create extension if not exists pg_trgm;`
- Done: Query succeeds.

4) Create Stripe account (test mode)
- Why: payments for kits/subscriptions.
- Done: Keys visible; webhooks enabled later.

5) Create Resend account + verify domain
- Why: transactional emails.
- Done: API key and verified sending domain.

6) Create Cookiebot account
- Why: GDPR cookie consent.
- Done: Domain configured and script ID obtained.

7) Create GA4 property + web stream
- Why: analytics on free tier.
- Done: Measurement ID available.

8) Create Cal.com account
- Why: consultations booking.
- Done: Embed link or API key created.

9) Create HubSpot free CRM
- Why: lead capture + basic support inbox.
- Done: Portal ID or private app token available.

10) Cloudflare DNS (optional, if managing DNS)
- Why: control DNS, future R2 if desired.
- Done: Domain in Cloudflare and ready to add Vercel records.

Acceptance: `.env.example` copied to `.env` with collected values.

---

## Iteration 2 — Repo & Scaffolding (10 tasks)
Goal: Create codebase skeleton with CI/CD and UI kit.

1) Initialize Git repo in `gwl/` and commit current docs
- Why: version control.

2) Create GitHub private repo and push
- Why: Vercel pulls from GitHub.

3) Scaffold Next.js 14 app `apps/web` with Tailwind + TypeScript + App Router
- Why: foundation for marketing + portal.

4) Add shadcn/ui and base components (button, input, card, dialog, toast)
- Why: consistent UI on free components.

5) Add ESLint/Prettier configs and scripts
- Why: code quality.

6) Add CI (GitHub Actions) for lint + typecheck + build
- Why: catch issues early.

7) Set up Vercel project and link to GitHub
- Why: deploy previews.

8) Configure environment variables in Vercel
- Why: keep secrets in platform.

9) Add Sentry SDK (free tier) with DSN
- Why: error monitoring.

10) Add base routes and health check `/api/health`
- Why: uptime monitor target.

Acceptance: PR builds succeed; Preview URL live.

---

## Iteration 3 — CMS & Content Model (10 tasks)
Goal: Headless CMS with localized, component-driven content.

1) Initialize Sanity project (`apps/studio/`) or `apps/web/sanity/`
2) Define document types: Page, Product (DNA stages), Package (Check‑ups), Article, FAQ, Testimonial, TeamMember
3) Define blocks/components: Hero, Steps, FeatureGrid, ComparisonTable, PricingTable, FAQAccordion, etc.
4) Add localization (SV/EN) fields and hreflang support
5) Implement Preview mode in Next.js with draft overlays
6) Author roles/workflow (Author → Editor → Approver)
7) Seed sample content for Home, DNA Category, Stage 1 PDP
8) Add webhooks to rebuild ISR on publish
9) Document content governance and naming conventions
10) CMS backup/export script

Acceptance: Pages render from Sanity content locally and on preview URL.

---

## Iteration 4 — Database & Search (10 tasks)
Goal: Data model and search v1 using Postgres.

1) Add Prisma to project; configure with Supabase connection
2) Implement schema per `enterprise_web_and_service_plan.md` (User, Product, Order, Kit, Result, Plan, etc.)
3) Generate and run initial migration
4) Add seed script for DNA products (Stage 1/2/3) and pricing
5) Implement Postgres FTS for Articles/FAQs with language config
6) Add `pg_trgm` indices for fuzzy matching
7) Build `GET /api/search` endpoint with filters
8) Add simple frontend search page and UI integration
9) Write unit tests for search ranking and typo tolerance
10) Document search limitations and upgrade path to Typesense

Acceptance: Search returns relevant results with typo tolerance.

---

## Iteration 5 — Auth, MFA & Privacy (10 tasks)
Goal: Secure login and privacy-first defaults.

1) Add NextAuth with email magic link via Resend
2) Add optional OIDC provider (Google/Microsoft) if desired later
3) Implement roles: Customer, Nutritionist, Support, Admin
4) Add TOTP MFA setup using `otplib` and recovery codes
5) Session management and device list with revoke
6) Rate limiting for auth endpoints; captcha on suspicious activity
7) Consent center (testing/results, marketing, research)
8) Data export (JSON/PDF) queue stub and download endpoint
9) Account deletion request with grace period
10) Audit log table and write paths for PII/PHI access

Acceptance: Auth works locally and on preview; MFA enforced optionally; consent records versioned.

---

## Iteration 6 — Payments & E‑commerce (10 tasks)
Goal: Buy kits and subscriptions with VAT and webhooks.

1) Model products in DB and Stripe (Stage 1/2/3, subscriptions)
2) Implement cart and checkout session creation
3) Handle Stripe webhooks (checkout success, subscription events)
4) VAT display (SE), price formatting, tax inclusive flag
5) Refunds create credit notes and email receipts
6) Invoice links available in portal via Stripe
7) Store orders and items; reconcile totals
8) Abandoned cart event + email stub
9) Admin price/discount management UI skeleton
10) E2E tests for checkout success/fail and webhooks

Acceptance: Test mode purchase flow completes; orders visible; invoices downloadable.

---

## Iteration 7 — Public Site A (10 tasks)
Goal: Core pages for discovery and conversion.

1) Home page (hero, proof, steps, product tiles, lead capture)
2) How It Works (stepper, security/privacy sidebar)
3) DNA Testing Category (comparison matrix)
4) Stage 1 PDP (benefits, add to cart, references, FAQs)
5) Stage 2 PDP
6) Stage 3 PDP
7) Personalized Plans page
8) Vitamin Subscriptions page
9) Pricing page
10) JSON‑LD (Organization, WebSite, Product, Service) on all above

Acceptance: Pages render from CMS content; Lighthouse ≥90 desktop/≥85 mobile.

---

## Iteration 8 — Public Site B (10 tasks)
Goal: Trust, education, and lead capture.

1) Check‑ups & Packages page (cards → detail)
2) Science & Evidence page
3) Resources: Guides listing + detail
4) FAQs (category listing + accordions)
5) Success Stories page
6) For Business (lead form, value props)
7) About (mission, team, values)
8) Contact (form, DPO contact)
9) Legal pages (Privacy, Terms, Cookies, DPA, Research Consent, Medical Disclaimer)
10) Site Search results page

Acceptance: All pages functional, SEO metadata complete, forms spam-protected.

---

## Iteration 9 — Portal Core (10 tasks)
Goal: Onboarding, kit registration, and status.

1) Dashboard with onboarding progress
2) Welcome + Consent review flow (granular)
3) Health profile (optional) form with validations
4) Register Kit with code entry + QR/barcode scanner
5) Kit status tracker UI (Received → In Analysis → Ready)
6) Email notifications on status changes (Resend)
7) Results placeholder page
8) Secure messages/documents shell
9) Billing & Subscriptions shell
10) Referrals shell with link and copy

Acceptance: New user can complete onboarding and register a kit.

---

## Iteration 10 — Results, Plan, Subscriptions & Launch Readiness (10 tasks)
Goal: Deliver insights, plan, and manage subscriptions; finalize QA.

1) Results viewer: parse `lab_samples/results_sample.json` into modular cards
2) PDF download (from Supabase Storage placeholder)
3) Glossary tooltips and links to Science page
4) Personalized Plan: weekly view, adherence tracking, "why this" explainers
5) Plan changelog and versioning
6) Subscriptions: manage tier/quantity; pause/cancel; invoices list
7) Orders history and shipping tracker placeholder
8) Analytics events instrumented per `analytics/event_taxonomy.json`
9) A11y audit (WCAG 2.2 AA) and fixes; Lighthouse budgets
10) Compliance: DPIA draft, Records of Processing, review legal pages

Acceptance: Portal usable E2E in preview; compliance checklist ready; go‑live plan approved.

---

## Proposed commands (Windows PowerShell) — to run when ready
Note: Do not include `cd` in commands; adjust the working directory in your IDE/terminal to `gwl/`.

1) Initialize Git and first commit
```
git init
git add .
git commit -m "chore: init docs, plans, samples, env"
```

2) Create GitHub repo and push (replace with your remote)
```
git branch -M main
git remote add origin https://github.com/<your-org>/gwl.git
git push -u origin main
```

3) Scaffold Next.js app (creates `apps/web`)
```
npx create-next-app@latest apps/web --ts --tailwind --eslint --app --src-dir --import-alias "@/*"
```

4) Add shadcn/ui in apps/web
```
cd apps/web
npx shadcn-ui@latest init -d
npx shadcn-ui@latest add button input card dialog toast
```

5) Add Prisma to web app and generate client
```
cd apps/web
npm i -E prisma @prisma/client
npx prisma init --datasource-provider postgresql
# Paste DATABASE_URL in apps/web/.env and run:
npx prisma migrate dev --name init
```

6) Add NextAuth and Resend
```
npm i -E next-auth resend otplib zod
```

7) Add Sentry
```
npm i -E @sentry/nextjs
npx @sentry/wizard -i nextjs
```

8) Link Vercel project and set env vars
```
vercel link
vercel env add # follow prompts
```

---

## Notes
- Keep secrets out of git. `.gitignore` excludes `.env`.
- Use the docs in `pages_design/` and samples in `lab_samples/` to build UI before integrations are live.
