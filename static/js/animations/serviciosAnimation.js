// Archivo serviciosAnimation.js

window.addEventListener('load', function () {
    const servContainer = document.querySelector('.serv-container')
    const title = document.querySelector('.serv_h1')
    const text = document.querySelector('.serv_p')
    const servFreeContainer = document.querySelector('.serv-free-container')
    const recordaElement = document.querySelector('.recorda')

    servContainer.classList.add('show')

    // Retraso para la animación del título
    setTimeout(() => {
        title.classList.add('show')
    }, 500)

    // Retraso adicional para la animación del texto
    setTimeout(() => {
        text.classList.add('show')
    }, 1000)

    // Intersection Observer para las secciones de servicios
    const options = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1,
    }

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show')
                observer.unobserve(entry.target)
            }
        })
    }, options)

    const ladoIzqElements = document.querySelectorAll('.lado_izq')
    const ladoDerElements = document.querySelectorAll('.lado_der')

    ladoIzqElements.forEach((element) => {
        observer.observe(element)
    })

    ladoDerElements.forEach((element) => {
        observer.observe(element)
    })

    observer.observe(servFreeContainer)

    // Función para aplicar y remover la animación de énfasis
    function applyEmphasisAnimation() {
        recordaElement.classList.add('emphasis')
        setTimeout(() => {
            recordaElement.classList.remove('emphasis')
            setTimeout(applyEmphasisAnimation, 2000) // Espera 2 segundos antes de volver a aplicar la animación
        }, 1000) // Duración de la animación
    }

    // Iniciar la animación de énfasis
    setTimeout(applyEmphasisAnimation, 2000) // Ajusta el tiempo según sea necesario
})