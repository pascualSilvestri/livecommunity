document.addEventListener("DOMContentLoaded", () => {
  const title = document.querySelector(".tus_maestros h2");
  const text = document.querySelector(".tus_maestros p");
  const section = document.querySelector(".staff");
  const cardStaff = document.querySelectorAll(".cardStaff");
  const carousel = document.querySelector('.carousel');

  // Verificar que los elementos principales existan
  if (title && text && section && carousel) {
    const observerOptions = {
      root: null,
      rootMargin: "0px",
      threshold: 0.1,
    };

    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          title.classList.add("animate");
          text.classList.add("animate");
          carousel.classList.add('animate');
          observer.disconnect(); // Deja de observar una vez que la animación se ha activado
        } else {
          title.classList.remove("animate");
          text.classList.remove("animate");
          carousel.classList.remove('animate');
        }
      });
    }, observerOptions);

    observer.observe(section);
  } 

  // Verificar que existan las tarjetas de staff antes de agregar los eventos
  if (cardStaff.length > 0) {
    cardStaff.forEach((card) => 
      card.addEventListener("mouseenter", () => {
        const ul = card.querySelector('ul');
        if (ul) {
          ul.classList.add('show');
        } else {
          console.error("No se encontró el elemento <ul> dentro de .cardStaff");
        }
      })
    );

    cardStaff.forEach((card) => 
      card.addEventListener("mouseleave", () => {
        const ul = card.querySelector('ul');
        if (ul) {
          ul.classList.remove('show');
        }
      })
    );
  }
});
