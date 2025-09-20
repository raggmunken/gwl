import type { Metadata } from "next";
import type { Locale } from "@/i18n";
import LocaleSwitcher from "@/components/locale-switcher";

export const metadata: Metadata = {
  title: "Genetic Wellness Labs",
  description: "Personalized nutrition via DNA insights.",
};

export default function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { locale?: Locale };
}) {
  // Fallback to 'sv' if params are not yet available
  const _locale = (params as any)?.locale ?? "sv";
  return (
    <>
      <header className="p-4 flex justify-end">
        <LocaleSwitcher />
      </header>
      {children}
    </>
  );
}
