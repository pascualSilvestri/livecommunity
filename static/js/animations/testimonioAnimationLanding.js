document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slide');

    // Clonar las slides para efecto infinito
    slides.forEach((slide) => {
        const clone = slide.cloneNode(true);
        slider.appendChild(clone);
    });

    slides.forEach((slide) => {
        slide.addEventListener('mouseenter', () => {
            slider.style.animationPlayState = 'paused';
            slide.style.transform = 'scale(1.5)';
            slide.style.transition = 'transform 0.5s ease';
            slide.style.backgroundColor = '#031542';
            slide.style.zIndex = '10';
        });

        slide.addEventListener('mouseleave', () => {
            slider.style.animationPlayState = 'running';
            slide.style.transform = 'scale(1)';
            slide.style.backgroundColor = '#06102bb9';
            slide.style.zIndex = '0';
        });
    });
});



//////////////////////////////Testimonio secction--------------------------------

