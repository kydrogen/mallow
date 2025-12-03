export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        earth: {
          50: '#faf8f3',
          100: '#f5f1e8',
          200: '#ede5d9',
          300: '#e0d4c4',
          400: '#d4c5b1',
          500: '#cfbdae',
          600: '#bba694',
          700: '#9d8d78',
          800: '#7a7560',
          900: '#5a5247',
        }
      },
      fontFamily: {
        serif: ['Georgia', 'serif'],
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
