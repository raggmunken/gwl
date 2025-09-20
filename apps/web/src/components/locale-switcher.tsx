"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

function switchLocalePath(pathname: string, target: "sv" | "en") {
  if (!pathname || pathname === "/") return `/${target}`;
  const parts = pathname.split("/");
  // Ensure first segment after root is locale
  if (parts.length > 1) {
    parts[1] = target;
    return parts.join("/") || `/${target}`;
  }
  return `/${target}`;
}

export default function LocaleSwitcher() {
  const pathname = usePathname();
  const toSv = switchLocalePath(pathname, "sv");
  const toEn = switchLocalePath(pathname, "en");
  return (
    <div className="flex gap-2 text-sm">
      <Link href={toSv} className="underline">SV</Link>
      <span>/</span>
      <Link href={toEn} className="underline">EN</Link>
    </div>
  );
}
