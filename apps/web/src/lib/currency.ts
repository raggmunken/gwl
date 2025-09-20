import type { Locale } from "@/i18n";

export type SupportedCurrency = "SEK" | "EUR";

export function getCurrencyForLocale(locale: Locale): SupportedCurrency {
  return locale === "en" ? "EUR" : "SEK";
}

export function formatPrice(amountMinor: number, currency: SupportedCurrency, locale: Locale) {
  const amount = amountMinor / 100; // Stripe-style minor units
  return new Intl.NumberFormat(locale === "en" ? "en-US" : "sv-SE", {
    style: "currency",
    currency
  }).format(amount);
}
