document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.about-us')
    const about_us_img_1 = document.querySelector('.about_us_img_1')
    const about_us_img_2 = document.querySelector('.about_us_img_2')
    const titleAbout = document.querySelector('.about_us_h2')
    const textContainer = document.querySelector('.about_us_p')

    if (!container) {
        console.error('No se encontró el contenedor con la clase .about-us')
        return
    }

    const containerTop = container.getBoundingClientRect().top + window.scrollY

    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY

        console.log('Posición de scroll:', scrollPosition)
        console.log('Posición superior del contenedor:', containerTop)

        if (scrollPosition >= containerTop - 250) {
            about_us_img_1.classList.add('animate')
            setTimeout(() => {
                about_us_img_2.classList.add('animate')
            }, 500) // Ajusta el tiempo de retraso según lo necesites
            setTimeout(() => {
                titleAbout.classList.add('animate')
            }, 500) // Ajusta el tiempo de retraso según lo necesites
            setTimeout(() => {
                textContainer.classList.add('animate')
            }, 500) // Ajusta el tiempo de retraso según lo necesites
        } else {
            about_us_img_1.classList.remove('animate')
            about_us_img_2.classList.remove('animate')
            titleAbout.classList.remove('animate')
            textContainer.classList.remove('animate')
        }

        // Efecto parallax para las imágenes
        if (about_us_img_1.classList.contains('animate')) {
            about_us_img_1.style.transform = `translateY(${
                scrollPosition * 0.2
            }px)`
        }
        if (about_us_img_2.classList.contains('animate')) {
            about_us_img_2.style.transform = `translateY(${
                scrollPosition * 0.1
            }px)`
        }
    })
})
