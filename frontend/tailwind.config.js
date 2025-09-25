import { heroui } from "@heroui/theme"

export default {
  content: [
    "./src/**/*.{js,jsx}",
    "./node_modules/@heroui/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  darkMode: "class",
  plugins: [heroui()],
}
