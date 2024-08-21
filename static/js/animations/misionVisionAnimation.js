document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.mision_vision_container')
    const mision_vision_container = document.querySelector('.mision_vision_container')
    const stats_container = document.querySelector('.stats_container')
    const titleAbout = document.querySelector('.about_us_h2')
    const textContainer = document.querySelector('.about_us_p')

    if (!container) {
        console.error('No se encontró el contenedor con la clase .about-us')
        return
    }

    const containerTop = container.getBoundingClientRect().top + window.scrollY

    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY


        if (scrollPosition >= containerTop - 300) {
            mision_vision_container.classList.add('animate')
            setTimeout(() => {
                stats_container.classList.add('animate')
            }, 500) // Ajusta el tiempo de retraso según lo necesites
            setTimeout(() => {
                titleAbout.classList.add('animate')
            }, 500) // Ajusta el tiempo de retraso según lo necesites
            setTimeout(() => {
                textContainer.classList.add('animate')
            }, 500) // Ajusta el tiempo de retraso según lo necesites
        } else {
            mision_vision_container.classList.remove('animate')
            stats_container.classList.remove('animate')
            titleAbout.classList.remove('animate')
            textContainer.classList.remove('animate')
        }

        // Efecto parallax para las imágenes
        if (mision_vision_container.classList.contains('animate')) {
            mision_vision_container.style.transform = `translateY(${
                scrollPosition * 0.1
            }px)`
        }
        if (stats_container.classList.contains('animate')) {
            stats_container.style.transform = `translateY(${
                scrollPosition * 0.1
            }px)`
        }
    })
})
