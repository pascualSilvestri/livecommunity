const navbar = document.querySelector('#navBar');
const heightDisplay = window.innerHeight;
const widthDisplay = window.innerWidth;
const navbarDisplay = navbar.getBoundingClientRect().height;

window.addEventListener('scroll', () => {

});

document.addEventListener('DOMContentLoaded', () => {
    const loading = document.createElement('div');
    loading.classList.add('loading');
    loading.textContent = 'Loading...';
    document.body.appendChild(loading);


    window.addEventListener('load', () => {
        setTimeout(() => {
            loading.remove();
        }, 1000);
    });
});
