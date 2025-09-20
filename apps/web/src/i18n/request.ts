import {getRequestConfig} from 'next-intl/server';

export default getRequestConfig(async ({requestLocale}) => {
  // Define the locales you support
  const locales = ['sv', 'en'] as const;
  const defaultLocale = 'sv' as const;

  // Resolve the active locale
  const locale = (await requestLocale) ?? defaultLocale;
  if (!locales.includes(locale as any)) {
    return {
      locale: defaultLocale,
      messages: (await import(`@/messages/${defaultLocale}.json`)).default,
    };
  }

  return {
    locale,
    messages: (await import(`@/messages/${locale}.json`)).default,
  };
});
