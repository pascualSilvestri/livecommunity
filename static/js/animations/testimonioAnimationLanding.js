const slider = document.querySelector('.slider')
const slides = document.querySelectorAll('.slide')

// Clonar las slides para efecto infinito
slides.forEach((slide) => {
    const clone = slide.cloneNode(true)
    slider.appendChild(clone)
})
