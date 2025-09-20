export default async function LocaleHome({
  params,
}: {
  params: Promise<{ locale: "sv" | "en" }>;
}) {
  const { locale } = await params;
  return (
    <main className="p-8">
      <h1 className="text-2xl font-semibold">Genetic Wellness Labs</h1>
      <p className="mt-2 text-muted-foreground">Locale: {locale}</p>
    </main>
  );
}
