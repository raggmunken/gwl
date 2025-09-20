import { NextIntlClientProvider } from "next-intl";
import LocaleSwitcher from "@/components/locale-switcher";

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: "sv" | "en" }>;
}) {
  const { locale } = await params;
  const messages = (await import(`@/messages/${locale}.json`)).default;
  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      <header className="p-4 flex justify-end">
        <LocaleSwitcher />
      </header>
      {children}
    </NextIntlClientProvider>
  );
}
