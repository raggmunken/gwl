export default function LocaleHome({
  params,
}: {
  params: { locale: "sv" | "en" };
}) {
  return (
    <main className="p-8">
      <h1 className="text-2xl font-semibold">Genetic Wellness Labs</h1>
      <p className="mt-2 text-muted-foreground">Locale: {params.locale}</p>
    </main>
  );
}
