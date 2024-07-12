const navbar = document.querySelector('#navBar')
const heightDisplay = window.innerHeight
const widthDisplay = window.innerWidth
const navbarDisplay = navbar.getBoundingClientRect().height

window.addEventListener('scroll', () => {})

document.addEventListener('DOMContentLoaded', () => {
    const loading = document.querySelector('.loading')

    window.addEventListener('load', () => {
        setTimeout(() => {
            loading.style.display = 'none'

            // Animación del navbar, título y el botón
            const title = document.querySelector('.hero h1')
            const button = document.querySelector('.hero .btn')

            // Navbar animación
            setTimeout(() => {
                navbar.classList.add('animate')
            }, 500) // 500 ms de retardo para el navbar

            // Título animación
            setTimeout(() => {
                title.classList.add('animate')
            }, 1000) // 1000 ms de retardo para el título

            // Botón animación
            setTimeout(() => {
                button.classList.add('animate')
            }, 1500) // 1500 ms de retardo para el botón
        }, 1000)
    })
})
