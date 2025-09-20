# Stack choices (free or lowest-cost first)

Date: 19 Sep 2025

## Hosting & Frontend
- Vercel (Free): Fast, serverless, preview deployments, great DX. Alt: Netlify (Free).
- Framework: Next.js 14 + TypeScript + App Router (Free). UI: Tailwind + shadcn/ui (Free).

## CMS
- Sanity (Free dev plan): Structured content, roles, preview, localization. Alt: Strapi (Free OSS, but hosting adds ops cost).

## Database & ORM
- Neon Postgres (Free): Serverless Postgres with extensions. ORM: Prisma (Free).
- Search v1: Postgres full‑text + pg_trgm (Free, typo tolerance). Later: Typesense (OSS) if needed.

## Auth & Security
- NextAuth (Free) with Email/Passwordless + OIDC; TOTP MFA via `otplib` (Free).

## Payments & Tax
- Stripe (Free to start, fees per txn). Klarna via Stripe.

## File Storage
- Cloudflare R2 (Free tier): Asset/report storage. Alt: AWS S3 (Always free 5 GB).

## Email
- Transactional: Resend (Free tier). Alt: SendGrid (Free 100/day).
- Marketing: Mailchimp (Free tier for small lists). Alt: Buttondown (low-cost).

## Consent & Analytics
- Cookie CMP: Cookiebot (Free for small site). Alt: CookieYes (Free tier).
- Analytics: GA4 (Free). Optional: Umami self‑host later.

## CRM & Support
- HubSpot CRM (Free). Support: Email → HubSpot inbox to start (Free). Later: Zendesk (Paid).

## Calendaring
- Cal.com (Free plan) or Calendly (Free basic).

## Monitoring & Logs
- Sentry (Free), UptimeRobot (Free), OpenTelemetry (Free), Vercel Analytics (Free tier).

## Shipping (Phase 2+)
- Start manual labels. Scale with Shippo (no monthly fee, pay‑as‑you‑go API) when volume warrants.

## Infrastructure & CI/CD
- GitHub (Free private repos), GitHub Actions (Free tier). DNS + WAF: Cloudflare (Free).

## Documentation
- Next.js: https://nextjs.org/docs
- Vercel: https://vercel.com/docs
- Tailwind CSS: https://tailwindcss.com/docs
- shadcn/ui: https://ui.shadcn.com/docs
- Sanity CMS: https://www.sanity.io/docs
- Strapi (alt CMS): https://docs.strapi.io/
- Neon Postgres: https://neon.tech/docs
- Postgres FTS: https://www.postgresql.org/docs/current/textsearch-intro.html
- pg_trgm: https://www.postgresql.org/docs/current/pgtrgm.html
- Prisma ORM: https://www.prisma.io/docs
- NextAuth (Auth.js): https://authjs.dev/reference/nextjs
- otplib (TOTP MFA): https://github.com/yeojz/otplib#readme
- Stripe: https://stripe.com/docs
- Klarna via Stripe: https://stripe.com/docs/payments/klarna
- Cloudflare R2: https://developers.cloudflare.com/r2/
- AWS S3 (alt storage): https://docs.aws.amazon.com/s3/index.html
- Resend: https://resend.com/docs/introduction
- SendGrid (alt email): https://docs.sendgrid.com/
- Mailchimp (marketing): https://mailchimp.com/developer/
- Cookiebot (CMP): https://www.cookiebot.com/en/developer/
- CookieYes (alt CMP): https://www.cookieyes.com/documentation/
- GA4: https://developers.google.com/analytics/devguides/collection/ga4
- HubSpot CRM: https://knowledge.hubspot.com/crm
- Cal.com: https://cal.com/docs/developing/introduction
- Calendly (alt): https://developer.calendly.com/
- Sentry: https://docs.sentry.io/
- UptimeRobot API: https://uptimerobot.com/api/
- OpenTelemetry: https://opentelemetry.io/docs/
- Vercel Analytics: https://vercel.com/docs/analytics
- Shippo (shipping): https://docs.goshippo.com/
- GitHub Actions: https://docs.github.com/actions
- Cloudflare (DNS/WAF): https://developers.cloudflare.com/dns/
- Supabase (alt DB): https://supabase.com/docs
- Firebase (alt DB): https://firebase.google.com/docs
