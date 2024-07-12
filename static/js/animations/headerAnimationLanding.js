const navbar = document.querySelector("#navBar");
const heightDisplay = window.innerHeight;
const widthDisplay = window.innerWidth;
const navbarDisplay = navbar.getBoundingClientRect().height;

window.addEventListener("scroll", () => {});

document.addEventListener("DOMContentLoaded", () => {
  const loading = document.querySelector(".loading");


  window.addEventListener("load", () => {
    setTimeout(() => {
      loading.style.display = "none";
    }, 1000);
  });
});
