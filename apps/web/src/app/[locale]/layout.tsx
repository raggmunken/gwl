import type { Metadata } from "next";
import { NextIntlClientProvider } from "next-intl";
import { getMessages, type Locale } from "@/i18n";
import "../globals.css";

export const metadata: Metadata = {
  title: "Genetic Wellness Labs",
  description: "Personalized nutrition via DNA insights.",
};

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { locale: Locale };
}) {
  const { locale } = params;
  const messages = await getMessages(locale);

  // Note: Root html/body are defined in app/layout.tsx
  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      {children}
    </NextIntlClientProvider>
  );
}
