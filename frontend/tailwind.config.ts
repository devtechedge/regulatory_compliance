import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#07090d",
          900: "#0c1118",
          800: "#121821",
          700: "#1a2230",
          600: "#243044",
        },
        line: "#243044",
        mint: "#2dd4bf",
        warn: "#fbbf24",
        danger: "#f87171",
        ok: "#34d399",
      },
      fontFamily: {
        sans: ["var(--font-sans)", "ui-sans-serif", "system-ui"],
        mono: ["var(--font-mono)", "ui-monospace", "SFMono-Regular"],
      },
    },
  },
  plugins: [],
};

export default config;
