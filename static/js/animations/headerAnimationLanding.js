const navbar = document.querySelector('#navBar');
const heightDisplay = window.innerHeight;
const widthDisplay = window.innerWidth;
let navbarDisplay;

if (navbar) {
    navbarDisplay = navbar.getBoundingClientRect().height;
} 

window.addEventListener('scroll', () => {
    // Aquí puedes agregar lógica adicional si es necesario
});

document.addEventListener('DOMContentLoaded', () => {
    const loading = document.querySelector('.loading');

    if (!loading) {
        
        return;
    }

    window.addEventListener('load', () => {
        setTimeout(() => {
            loading.style.display = 'none';

            // Animación del navbar, título y el botón
            const title = document.querySelector('.hero h1');
            const button = document.querySelector('.hero .btn');

            // Verificaciones antes de aplicar animaciones
            if (navbar) {
                // Navbar animación
                setTimeout(() => {
                    navbar.classList.add('animate');
                }, 500); // 500 ms de retardo para el navbar
            }

            if (title) {
                // Título animación
                setTimeout(() => {
                    title.classList.add('animate');
                }, 1000); // 1000 ms de retardo para el título
            } 

            if (button) {
                // Botón animación
                setTimeout(() => {
                    button.classList.add('animate');
                }, 1500); // 1500 ms de retardo para el botón
            } 
        }, 1000);
    });
});