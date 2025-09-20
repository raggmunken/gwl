# Account setup checklist (free/low-cost)

Fill this to collect keys for .env. Keep secrets in your password manager.

1) Vercel (hosting)
- Create org + project. Add GitHub repo later. No keys needed yet.

2) Sanity (CMS)
- Create Sanity project + dataset (prod). Enable preview. Collect:
  - SANITY_PROJECT_ID
  - SANITY_DATASET
  - SANITY_API_TOKEN (Editor)

3) Neon (Postgres)
- Create project + database. Enable extensions `pg_trgm`.
  - DATABASE_URL (e.g., postgres://...)

4) Stripe (payments)
- Activate account. Enable Tax if needed. Collect:
  - STRIPE_PUBLISHABLE_KEY
  - STRIPE_SECRET_KEY
  - STRIPE_WEBHOOK_SECRET (after webhook creation)

5) Cloudflare R2 (storage)
- Create account + R2 bucket. Collect:
  - CLOUDFLARE_ACCOUNT_ID
  - R2_ACCESS_KEY_ID
  - R2_SECRET_ACCESS_KEY
  - R2_BUCKET_NAME
  - R2_PUBLIC_BASE_URL (via public bucket/route)

6) Resend (transactional email)
- Create API key + verify sending domain.
  - RESEND_API_KEY
  - EMAIL_FROM (e.g., no-reply@yourdomain)

7) Mailchimp (marketing email)
- Create audience + API key.
  - MAILCHIMP_API_KEY
  - MAILCHIMP_AUDIENCE_ID

8) Cookiebot (cookie consent)
- Create domain, configure categories. Collect:
  - COOKIEBOT_ID

9) GA4 (analytics)
- Create property + web data stream.
  - NEXT_PUBLIC_GA4_ID (Measurement ID)

10) HubSpot (CRM)
- Create portal. For embeds use portal/site IDs or Private App token if calling API.
  - HUBSPOT_PORTAL_ID (or HUBSPOT_PRIVATE_APP_TOKEN)

11) Cal.com / Calendly (calendaring)
- Create account, set availability.
  - CALCOM_API_KEY or embed link

12) Sentry (monitoring)
- Create project → Next.js. Collect:
  - SENTRY_DSN

13) Cloudflare (DNS)
- Point domain to Cloudflare. Later: add Vercel records.
