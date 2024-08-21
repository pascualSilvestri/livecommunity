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
        nombre: 'Agustín Gómez',
        descripcion: '',
        imagen: './static/img/testimonios/AgustinGomez.png',
        video: './static/video/testimonios/Agustín Gómez.mp4'
    },
    {
        id: 2,
        nombre: 'Franco Gómez ',
        descripcion:'',
        imagen: './static/img/testimonios/FrancoGomez.png',
        video: './static/video/testimonios/Franco Gómez.mp4'
    },
    {
        id: 3,
        nombre: 'Francisco Vallejo',
        descripcion: '',
        imagen: './static/img/testimonios/FranciscoVallejo.png',
        video: './static/video/testimonios/testimonio francisco EDIT.mp4'
    },
    {
        id: 4,
        nombre: 'Mabel Otalora',
        descripcion: '',
        imagen: './static/img/testimonios/MABELOTALORA.png',
        video: './static/video/testimonios/MABEL OTALORA EDIT.mp4'
    },
    {
        id: 5,
        nombre: 'Ricarod Molano',
        descripcion: '',
        imagen: './static/img/testimonios/RicardoMolano.png',
        video: './static/video/testimonios/RICARDO MOLANO EDIT.mp4'
    },
    {
        id: 6,
        nombre: 'Cecilia Gonzales',
        descripcion: '',
        imagen: './static/img/testimonios/cecilia.png',
        video: './static/video/testimonios/cecilia.mp4'
    },
    {
        id: 7,
        nombre: 'Javier nou',
        descripcion: '',
        imagen: './static/img/testimonios/anonimo.png',
        video: './static/video/testimonios/testimonioAnomimo1.mp4'
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
