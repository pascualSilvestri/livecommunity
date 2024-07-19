document.addEventListener('DOMContentLoaded', (event) => {
    const serviceContainer = document.querySelector('.service_container');
    const services = document.querySelectorAll('.service');
    const numServices = services.length;

    // Clonar los primeros 4 elementos y agregarlos al final del contenedor
    for (let i = 0; i < numServices; i++) {
        const clone = services[i].cloneNode(true);
        serviceContainer.appendChild(clone);
    }
});
