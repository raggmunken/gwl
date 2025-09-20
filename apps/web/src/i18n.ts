export const locales = ["sv", "en"] as const;
export type Locale = typeof locales[number];

export async function getMessages(locale: Locale) {
  switch (locale) {
    case "en":
      return (await import("./messages/en.json")).default;
    case "sv":
    default:
      return (await import("./messages/sv.json")).default;
  }
}
