# Localization & Currency Plan (sv-SE default, en with EUR)

Date: 20 Sep 2025

## Goals
- Default site language Swedish (`sv-SE`), with English (`en-US`) as secondary.
- Default currency SEK; for English routes, display EUR.
- Path-based locales: `/sv/...` and `/en/...` with hreflang and localized metadata.
- Currency-aware pricing and checkout using Stripe Prices per currency.

## Approach

1) Routing & i18n
- Use `next-intl` or Next.js 14 i18n patterns with App Router.
- Localized routes:
  - `/sv/*` (default) and `/en/*`.
  - Root (`/`) redirects to `/sv/` (detect existing preference via cookie).
- Hreflang:
  - Inject `<link rel="alternate" hreflang="sv" href="/sv/..." />` and equivalent for `en`.
- Metadata:
  - Localize `<title>`, `<meta>` description, Open Graph, JSON‑LD.

2) Currency mapping by locale
- Mapping:
  - `sv-SE` → `SEK`
  - `en-US` → `EUR`
- Persist the user’s selection (cookie `locale`, `currency`).
- Display formatting with `Intl.NumberFormat(locale, { style: 'currency', currency })`.

3) Stripe prices per currency
- For each sellable item, create Stripe Prices in SEK and EUR.
- Use `lookup_key` (e.g., `vitamin_basic_monthly_sek`, `vitamin_basic_monthly_eur`).
- At checkout, pick the price ID that matches current currency.
- Store price IDs in environment variables or DB table for easy lookup.

4) Server-side data flow (App Router)
- Server Components fetch CMS content and product/price mappings.
- Inject localized metadata and JSON‑LD.
- All price display is pulled server-side using mapped Price IDs (avoids client-only currency logic).

5) Fallback behavior (until EUR is live)
- If EUR prices are not yet configured, display SEK with a small note “EUR pricing coming soon” and prevent currency switch from enabling checkout.

## Implementation Steps
- Add dependency: `next-intl`.
- Create `i18n.ts` with locales, defaultLocale, and dictionary loader.
- Wrap root layout with `NextIntlClientProvider`.
- Create `LocaleSwitcher` component and persist selection to cookie.
- Implement currency mapping utility `getCurrencyForLocale(locale)`.
- Add `formatPrice(amountMinor, currency, locale)` utility.
- Create a `prices` registry (env or DB) mapping products → { SEK: priceId, EUR: priceId }.
- Update PDPs and Pricing page to fetch prices based on locale.
- Update checkout session creation to use the mapped Price ID for current locale.

## Acceptance Criteria
- Visiting `/sv/` shows SEK pricing; `/en/` shows EUR.
- Switching locale updates prices and metadata instantly (SSR/ISR friendly).
- Checkout uses the correct Stripe Price based on locale.
- Hreflang, canonical, and JSON‑LD localized per page.
- Lighthouse SEO/Perf unaffected; no layout shift on price render.

## References
- Next.js: https://nextjs.org/docs
- next-intl: https://next-intl-docs.vercel.app/
- Stripe Prices: https://stripe.com/docs/billing/prices-guide
- Intl: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat
