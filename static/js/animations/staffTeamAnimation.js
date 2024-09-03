document.addEventListener("DOMContentLoaded", () => {
  const title = document.querySelector(".staff_h2");
  const text = document.querySelector(".staff_p");
  const section = document.querySelector(".staff");
  const cardStaff = document.querySelectorAll(".cardStaff");
  const carousel = document.querySelector('.carouselStaff');

  if (!section) {
    
    return;
  }



  const sectionTop = section.getBoundingClientRect().top + window.scrollY;

  window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY;

    if (scrollPosition >= sectionTop - 250) {
      if (title) title.classList.add("animate");
      if (text) text.classList.add("animate");
      if (carousel) carousel.classList.add('animate');
    } else {
      if (title) title.classList.remove("animate");
      if (text) text.classList.remove("animate");
      if (carousel) carousel.classList.remove('animate');
    }
  });

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
  } else {
    console.error("No se encontraron elementos con la clase .cardStaff");
  }
});
