# Genetic Wellness Labs — Quickstart (Free/Low‑Cost Stack)

This repo contains planning docs and samples to build the GWL website + portal using free/low‑cost services.

## Prerequisites
- Node.js 20+ (check: `node -v`)
- npm 10+ (check: `npm -v`) or pnpm
- Git + GitHub account
- Vercel account (Free) for hosting
- Accounts to create (Free tiers): Sanity, Supabase (already present), Stripe, Resend, Cookiebot, GA4, Cal.com, HubSpot, Sentry

## 1. Environment variables
- Copy `.env.example` to `.env` and fill values as you create accounts.
- Note: You already have a `.env` with Supabase and other keys; keep it secure and do not commit it.

## 2. Initialize repository
```powershell
# In the gwl folder
git init
git add .
git commit -m "chore: init docs, plans, samples, env"
```

Create a GitHub private repository and push:
```powershell
git branch -M main
git remote add origin https://github.com/<your-org>/gwl.git
git push -u origin main
```

## 3. Scaffold Next.js app (apps/web)
```powershell
npx create-next-app@latest apps/web --ts --tailwind --eslint --app --src-dir --import-alias "@/*"
```

Install shadcn/ui components:
```powershell
# Run inside apps/web
npx shadcn-ui@latest init -d
npx shadcn-ui@latest add button input card dialog toast
```

## 4. Database & Prisma (Supabase)
- In Supabase SQL editor, enable search extension:
```sql
create extension if not exists pg_trgm;
```
- Add Prisma and initialize:
```powershell
# Inside apps/web
npm i -E prisma @prisma/client
npx prisma init --datasource-provider postgresql
# Set DATABASE_URL in apps/web/.env, then run:
npx prisma migrate dev --name init
```

## 5. Auth & Email
- Install NextAuth + Resend + TOTP support:
```powershell
npm i -E next-auth resend otplib zod
```
- Configure email sign-in (Resend) and TOTP MFA (`otplib`).

## 6. CMS (Sanity)
- Create a Sanity project. Add schemas for Pages, Products, Packages, Articles, FAQs, Testimonials, TeamMember, and Blocks.
- Enable Preview mode in Next.js.

## 7. Payments (Stripe)
- Create test products (Stage 1/2/3, subscriptions) and prices.
- Add checkout creation API route and webhook handler.

## 8. Storage
- Use Supabase Storage buckets for assets and PDF reports initially.

## 9. Analytics & Consent
- Add GA4 Measurement ID.
- Add Cookiebot script and configure Consent Mode.

## 10. Deploy
- Link Vercel project:
```powershell
vercel link
vercel env add  # add env vars
```
- Push changes and confirm preview deploy works.

## References
- `pages_design/enterprise_web_and_service_plan.md`
- `pages_design/public_site_page_blueprints.md`
- `pages_design/portal_flows_and_wireframes.md`
- `implementation_tasks.md`
- Samples: `lab_samples/` and `analytics/event_taxonomy.json`
