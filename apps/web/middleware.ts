import createMiddleware from 'next-intl/middleware';

export default createMiddleware({
  locales: ['sv', 'en'],
  defaultLocale: 'sv'
});

export const config = {
  // Skip all paths that should not be internationalized
  matcher: ['/((?!_next|.*\..*).*)']
};
