import type { Locale } from "@/i18n";

export default async function LocaleHome({ params }: { params: { locale: Locale } }) {
  return (
    <main className="p-8">
      <h1 className="text-2xl font-semibold">GWL</h1>
      <p className="mt-2">Locale: {params.locale}</p>
    </main>
  );
}
