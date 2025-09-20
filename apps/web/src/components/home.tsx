"use client";

import { useTranslations } from "next-intl";

export default function HomeContent() {
  const t = useTranslations("home");
  return (
    <main className="p-8">
      <h1 className="text-2xl font-semibold">{t("welcome")}</h1>
      <p className="mt-2 text-muted-foreground">Genetic Wellness Labs</p>
    </main>
  );
}
