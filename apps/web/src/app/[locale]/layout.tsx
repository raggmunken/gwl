import LocaleSwitcher from "@/components/locale-switcher";

export default function LocaleLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <header className="p-4 flex justify-end">
        <LocaleSwitcher />
      </header>
      {children}
    </>
  );
}
