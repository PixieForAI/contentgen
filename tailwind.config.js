/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './templates/**/*.html',
      './apps/**/templates/**/*.html',
      './apps/**/*.py',
      './theme/static/src/**/*.js',
  ],
  theme: {
    extend: {
      // You can add your custom theme settings here.
      // For example, custom colors, fonts, etc.
      colors: {
        'primary': '#3498db',
        'secondary': '#2ecc71',
      }
    },
  },
  plugins: [],
}