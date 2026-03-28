import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "OnlyStudents | Company Portal",
  description:
    "Post jobs, share industry challenges, and discover AI-matched student talent on OnlyStudents — the platform connecting companies with top student candidates.",
  keywords: "student hiring, company portal, AI talent matching, job posting, industry challenges",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
