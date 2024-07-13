document.addEventListener("DOMContentLoaded", () => {
    const title = document.querySelector(".staff_h2");
    const text = document.querySelector(".staff p");
    const section = document.querySelector(".staff");
    const cardStaff = document.querySelectorAll(".cardStaff");
    const carousel = document.querySelector('.carouselStaff');
  
    if (!section) {
      console.error("No se encontró el contenedor con la clase .staff");
      return;
    }
  
    const sectionTop = section.getBoundingClientRect().top + window.scrollY;
  
    window.addEventListener('scroll', () => {
      const scrollPosition = window.scrollY;
  
      if (scrollPosition >= sectionTop - 250) {
        title.classList.add("animate");
        text.classList.add("animate");
        carousel.classList.add('animate');
      } else {
        title.classList.remove("animate");
        text.classList.remove("animate");
        carousel.classList.remove('animate');
      }
    });
  
    cardStaff.forEach((card) =>
      card.addEventListener("mouseenter", () => {
        card.querySelector('ul').classList.add('show');
      })
    );
  
    cardStaff.forEach((card) =>
      card.addEventListener("mouseleave", () => {
        card.querySelector('ul').classList.remove('show');
      })
    );
  });
  