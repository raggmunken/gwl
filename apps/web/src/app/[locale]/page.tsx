import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n";

export default async function LocaleHome({
  params,
}: {
  params: { locale: Locale };
}) {
  const t = await getTranslations({ locale: params.locale, namespace: "home" });
  return (
    <main className="p-8">
      <h1 className="text-2xl font-semibold">{t("welcome")}</h1>
      <p className="mt-2 text-muted-foreground">Genetic Wellness Labs</p>
    </main>
  );
}
