document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".broker_inicio_container");

  if (!container) {
    console.error("No se encontró el contenedor con la clase .about-us");
    return;
  }

  const containerTop = container.getBoundingClientRect().top + window.scrollY;

  window.addEventListener("scroll", () => {
    const scrollPosition = window.scrollY;

    if (scrollPosition >= containerTop - 500) {
      container.classList.add("animate");
    } 
  });
});
