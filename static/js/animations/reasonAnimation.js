document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".reasons");
  const reasonAll = document.querySelectorAll(".reason");
  if (!container) {
    
    return;
  }

  const containerTop = container.getBoundingClientRect().top + window.scrollY;

  window.addEventListener("scroll", () => {
    const scrollPosition = window.scrollY;

    if (scrollPosition >= containerTop - 250) {
      reasonAll.forEach((reason, index  ) => {
        setTimeout(() => {
          reason.classList.add("animate");
        }, index * 500); // Ajusta el tiempo de retraso según lo necesites
      });
    }
  });
});


