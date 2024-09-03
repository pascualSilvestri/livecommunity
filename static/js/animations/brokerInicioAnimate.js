document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".broker_inicio_container");

  if (!container) {
    
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
