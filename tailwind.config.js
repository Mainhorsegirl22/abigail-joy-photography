/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html"],
  theme: {
    extend: {
      colors: {
        espresso: '#2B251F',
        ivory:    '#F7F4EE',
        linen:    '#EDE8DF',
        taupe:    '#C9BFB0',
        sage:     '#A8AA9A',
        brass:    '#97784B',
      },
      fontFamily: {
        serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
        sans:  ['Montserrat', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      letterSpacing: {
        label: '0.18em',
        tightest: '-0.03em',
      },
      boxShadow: {
        'card':  '0 1px 2px rgba(43,37,31,0.06), 0 4px 12px rgba(43,37,31,0.07), 0 12px 32px rgba(43,37,31,0.06)',
        'float': '0 2px 4px rgba(43,37,31,0.08), 0 8px 24px rgba(43,37,31,0.10), 0 24px 56px rgba(43,37,31,0.10)',
        'btn':   '0 1px 2px rgba(43,37,31,0.25), 0 4px 14px rgba(151,120,75,0.35)',
      },
      transitionTimingFunction: {
        spring: 'cubic-bezier(0.34, 1.3, 0.5, 1)',
      },
    }
  },
  plugins: [],
}
