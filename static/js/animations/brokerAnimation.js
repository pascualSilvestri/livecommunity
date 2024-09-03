document.addEventListener('DOMContentLoaded', function () {
    // Animación del logo
    setTimeout(function () {
        const logo = document.querySelector('.broker-logo');
        if (logo) {
            logo.classList.add('animate');
        } else {
            console.error('No se encontró el elemento con la clase .broker-logo');
        }
    }, 1000);

    // Animación del texto al hacer scroll
    const aboutUsText = document.querySelector('.broker_about_us_text p');
    if (aboutUsText) {
        const observerText = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        aboutUsText.classList.add('visible');
                        observerText.unobserve(entry.target);
                        typeText(aboutUsText);
                    }
                });
            },
            { threshold: 0.1 }
        );

        observerText.observe(aboutUsText);

        function typeText(element) {
            const text = element.textContent; // Use textContent to preserve line breaks
            element.textContent = '';
            element.classList.add('typing');

            let i = 0;
            function type() {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(type, 40);
                } else {
                    // Remover la clase typing después de que el texto se haya escrito completamente
                    element.classList.remove('typing');
                }
            }

            type();
        }
    } else {
        console.error('No se encontró el elemento con la clase .broker_about_us_text p');
    }

    // Función para manejar las animaciones de las tarjetas al hacer scroll
    function handleCardAnimations(entries, observer) {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }

    // Crear un IntersectionObserver para las tarjetas
    const observerCards = new IntersectionObserver(handleCardAnimations, {
        threshold: 0.1,
    });

    // Seleccionar los elementos y añadir clases específicas
    const cardBig1 = document.querySelectorAll('.broker_info_card_big')[0];
    const cardBig2 = document.querySelectorAll('.broker_info_card_big')[1];
    const cardSmall1 = document.querySelectorAll('.broker_info_card_small')[0];
    const cardSmall2 = document.querySelectorAll('.broker_info_card_small')[1];

    if (cardBig1) {
        cardBig1.classList.add('appear-from-top');
        observerCards.observe(cardBig1);
    } 

    if (cardBig2) {
        cardBig2.classList.add('appear-from-bottom');
        observerCards.observe(cardBig2);
    } 

    if (cardSmall1) {
        cardSmall1.classList.add('appear-from-left');
        observerCards.observe(cardSmall1);
    } 

    if (cardSmall2) {
        cardSmall2.classList.add('appear-from-right');
        observerCards.observe(cardSmall2);
    } 
});