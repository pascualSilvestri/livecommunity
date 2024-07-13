document.addEventListener('DOMContentLoaded', () => {
    const title = document.querySelector('.tus_maestros h2')
    const text = document.querySelector('.tus_maestros p')
    const section = document.querySelector('.staff')

    // Verificar que los elementos existan
    if (title && text && section) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1,
        }

        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    title.classList.add('animate')
                    text.classList.add('animate')
                    observer.disconnect() // Deja de observar una vez que la animación se ha activado
                }
            })
        }, observerOptions)

        observer.observe(section)
    } else {
        console.error(
            'No se encontraron los elementos necesarios para las animaciones.'
        )
    }
})
