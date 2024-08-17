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
const testimonios = [
    {
        id: 1,
        nombre: 'María Stefanie',
        descripcion: '',
        imagen: './static/img/staff/AylenHeredia.png',
        video: './static/video/video_hero.mp4'
    },
    {
        id: 2,
        nombre: 'Carlos Mendoza',
        descripcion: '"Live Community ha cambiado mi vida. Gracias a sus cursos, ahora entiendo mejor cómo funciona el mercado y puedo tomar decisiones más informadas. ¡Recomendado al 100%!"',
        imagen: './static/img/staff/AlexCamacho.png',
        video: './static/video/video_hero_testing.mp4'
    },
    {
        id: 3,
        nombre: 'Ana Fernández',
        descripcion: '"Los cursos de Live Community son simplemente geniales. El material es claro y el soporte es increíble. Estoy muy agradecida por todo lo que he aprendido."',
        imagen: './static/img/staff/DiegoCeron.png',
        video: './static/video/video_hero.mp4'
    },
    {
        id: 4,
        nombre: 'Jorge Pérez',
        descripcion: '"La experiencia con Live Community ha sido fenomenal. Los instructores son expertos en el tema y el contenido es muy accesible. He mejorado mis habilidades de trading enormemente."',
        imagen: './static/img/staff/JoseLinares.png',
        video: './static/video/video_hero_testing.mp4'
    },
    {
        id: 5,
        nombre: 'Manuel Turisons',
        descripcion: '"Los cursos de Live Community son simplemente geniales. El material es claro y el soporte es increíble. Estoy muy agradecida por todo lo que he aprendido."',
        imagen: './static/img/staff/MauroAlvarez.png',
        video: './static/video/video_hero_testing.mp4'
    },
];

document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.video_card_container');
    const videoElement = document.querySelector('.video_testimonios_video video');
    const nombreElement = document.querySelector('.video_testimonios_nombre');
    const descripcionElement = document.querySelector('.video_testimonios_descripcion');
    const prevButton = document.querySelector('.after_video');
    const nextButton = document.querySelector('.next_video');

    let scrollAmount = 0;
    let cardWidth = 0; // Se calculará después de generar las tarjetas

    // Generar dinámicamente las tarjetas de video
    function generarTarjetas() {
        testimonios.forEach(testimonio => {
            const card = document.createElement('div');
            card.classList.add('video_card');
            card.innerHTML = `
                <img src="${testimonio.imagen}" alt="${testimonio.nombre}">
                <div class="video_info">
                    <p>${testimonio.nombre}</p>
                </div>
            `;
            card.addEventListener('click', () => {
                actualizarTestimonio(testimonio.id);
            });
            container.appendChild(card, nextButton); // Inserta antes del botón de "next"
        });

        // Calcular el ancho de las tarjetas una vez que se hayan generado
        const cards = document.querySelectorAll('.video_card');
        cardWidth = cards[0].offsetWidth + 10; // Tamaño de cada tarjeta más margen
    }

    // Función para actualizar el testimonio seleccionado
    function actualizarTestimonio(id) {
        const testimonio = testimonios.find(t => t.id === id);
        if (testimonio) {
            videoElement.src = testimonio.video;
            nombreElement.textContent = testimonio.nombre;
            descripcionElement.textContent = testimonio.descripcion;
            videoElement.load(); // Recarga el video para asegurarse de que se cambie correctamente
            videoElement.pause(); // Pausa el video hasta que se presione el botón de play
            videoElement.controls = false; // Oculta los controles hasta que se haga clic para reproducir
        }
    }

    // Manejar la navegación del slider
    nextButton.addEventListener('click', () => {
        if (scrollAmount < (testimonios.length - 1) * cardWidth) {
            scrollAmount += cardWidth;
            container.scrollTo({
                left: scrollAmount,
                behavior: 'smooth'
            });
        }
    });

    prevButton.addEventListener('click', () => {
        if (scrollAmount > 0) {
            scrollAmount -= cardWidth;
            container.scrollTo({
                left: scrollAmount,
                behavior: 'smooth'
            });
        }
    });

    // Añadir botón de play en el centro del video
    videoElement.addEventListener('click', function() {
        if (videoElement.paused) {
            videoElement.play();
            videoElement.controls = true; // Muestra los controles cuando se reproduce
        } else {
            videoElement.pause();
        }
    });

    // Generar las tarjetas y actualizar el primer testimonio como el predeterminado
    generarTarjetas();
    actualizarTestimonio(1); // Mostrar el primer testimonio por defecto
});
