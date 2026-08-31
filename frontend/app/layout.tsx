import type { Metadata } from "next";
import { IBM_Plex_Mono, IBM_Plex_Sans } from "next/font/google";
import "./globals.css";
import { Chrome } from "@/components/Chrome";

const sans = IBM_Plex_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-sans",
});

const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "RegTrace-AI — HITL Web3 compliance copilot",
  description:
    "Human-in-the-Loop regulatory copilot for VASP licensing. Source-traced MiCA / VARA framework mapping with hallucination mitigation.",
  icons: {
    icon: [{ url: "/favicon.svg", type: "image/svg+xml" }],
  },
};

const THEME_BOOT = `(function(){try{var k="regulatory_compliance-theme";var t=localStorage.getItem(k);if(t!=="light"&&t!=="dark")t="dark";var r=document.documentElement;r.setAttribute("data-theme",t);r.style.colorScheme=t;if(t==="dark")r.classList.add("dark");else r.classList.remove("dark");}catch(e){document.documentElement.setAttribute("data-theme","dark");}})();`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${sans.variable} ${mono.variable}`} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: THEME_BOOT }} />
      </head>
      <body className="font-sans antialiased bg-ink-950 text-slate-100">
        <Chrome />
        <main className="mx-auto max-w-[1440px] px-5 pb-16 pt-4">{children}</main>
      </body>
    </html>
  );
}
