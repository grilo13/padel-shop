/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.{html,js}"],
    theme: {
        extend: {
            screens: {
                sm: '576px',
                md: '768px',
                lg: '992px',
                xl: '1200px'
            },
            container: {
                center: true,
                padding: '1rem'
            },
            fontFamily: {
                poppins: "'Poppins', sans-serif",
                roboto: "'Roboto', sans-serif"
            },
            colors: {
                'primary': '#7FA9CD'
            }
        },
    },
    plugins: [],
}
