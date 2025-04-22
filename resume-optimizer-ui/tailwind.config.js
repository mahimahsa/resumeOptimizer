// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: [],
//   theme: {
//     extend: {},
//   },
//   plugins: [],
// }
// /** @type {import('tailwindcss').Config} */
// export default {
//   content: [
//     "./app/**/*.{js,ts,jsx,tsx,mdx}",
//   "./components/**/*.{js,ts,jsx,tsx,mdx}",
//   "./store/**/*.{js,ts,jsx,tsx,mdx}"
//   ],
//   theme: {
//     extend: {},
//   },
//   plugins: [],
// };
export default {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  // // Disable purge during development to test
  // safelist: ['bg-red-500', 'text-center', 'text-4xl'],
};

