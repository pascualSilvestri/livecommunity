document.addEventListener('DOMContentLoaded', function () {
    // Animación del logo
    setTimeout(function () {
        const logo = document.querySelector('.broker-logo')
        logo.classList.add('animate')
    }, 1000)

    // Animación del texto al hacer scroll
    const aboutUsText = document.querySelector('.broker_about_us_text p')
    const observerText = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    aboutUsText.classList.add('visible')
                    observerText.unobserve(entry.target)
                    typeText(aboutUsText)
                }
            })
        },
        { threshold: 0.1 }
    )

    observerText.observe(aboutUsText)

    function typeText(element) {
        const text = element.textContent // Use textContent to preserve line breaks
        element.textContent = ''
        element.classList.add('typing')

        let i = 0
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i)
                i++
                setTimeout(type, 40)
            }
        }

        type()
    }

    // Función para manejar las animaciones de las tarjetas al hacer scroll
    function handleCardAnimations(entries, observer) {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible')
                observer.unobserve(entry.target)
            }
        })
    }

    // Crear un IntersectionObserver para las tarjetas
    const observerCards = new IntersectionObserver(handleCardAnimations, {
        threshold: 0.1,
    })

    // Seleccionar los elementos y añadir clases específicas
    const cardBig1 = document.querySelectorAll('.broker_info_card_big')[0]
    const cardBig2 = document.querySelectorAll('.broker_info_card_big')[1]
    const cardSmall1 = document.querySelectorAll('.broker_info_card_small')[0]
    const cardSmall2 = document.querySelectorAll('.broker_info_card_small')[1]

    cardBig1.classList.add('appear-from-top')
    cardBig2.classList.add('appear-from-bottom')
    cardSmall1.classList.add('appear-from-left')
    cardSmall2.classList.add('appear-from-right')

    // Observar los elementos
    observerCards.observe(cardBig1)
    observerCards.observe(cardBig2)
    observerCards.observe(cardSmall1)
    observerCards.observe(cardSmall2)
})
