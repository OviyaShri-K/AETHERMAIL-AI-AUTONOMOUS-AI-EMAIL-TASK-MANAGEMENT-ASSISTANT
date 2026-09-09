import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        navy: {
          900: "#0B132B",
          800: "#1C2541",
          700: "#3A506B",
        },
        cyan: {
          500: "#00F0FF",
          400: "#5BC0BE",
        },
      },
    },
  },
  plugins: [],
};
export default config;
