import { NextIntlClientProvider } from "next-intl";
import LocaleSwitcher from "@/components/locale-switcher";

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { locale: "sv" | "en" };
}) {
  const messages = (await import(`@/messages/${params.locale}.json`)).default;
  return (
    <NextIntlClientProvider locale={params.locale} messages={messages}>
      <header className="p-4 flex justify-end">
        <LocaleSwitcher />
      </header>
      {children}
    </NextIntlClientProvider>
  );
}
