document.addEventListener('DOMContentLoaded', function () {
    // Obtiene el valor de la variable desde localStorage
    var selectedLinkId = localStorage.getItem('selectedLinkId')
    const brokerBtn = document.getElementById('broker')
    const sub_menu = document.querySelector('.sub_menu')
    const loginLink = document.getElementById('log_in') // Obtiene el botón de Log In

    // Establece la clase 'selected' en el elemento correspondiente
    if (selectedLinkId && selectedLinkId !== 'log_in') {
        // Verifica si el ID no es 'log_in'
        var selectedLink = document.getElementById(selectedLinkId)
        if (selectedLink) {
            selectedLink.classList.add('selected')
        }
    }

    var navigationLinks = document.querySelectorAll('nav li a')

    navigationLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault()

            // Obtiene la URL del enlace y navega manualmente
            var targetUrl = this.getAttribute('href')
            window.location.href = targetUrl

            // Si es el enlace de "Log In", no hacer nada en cuanto a las clases
            if (this.parentElement.id !== 'log_in') {
                // Cambia la clase si no es "Log In"
                changeClass(this)

                // Guarda el ID del enlace seleccionado en localStorage
                var clickedElementId = this.parentElement.id
                localStorage.setItem('selectedLinkId', clickedElementId)
            }

            console.log('Toqué este enlace: ' + this)
        })
    })

    brokerBtn.addEventListener('click', function (event) {
        toggleMenuBroker(sub_menu, 'block')
    })

    sub_menu.addEventListener('mouseleave', function (event) {
        toggleMenuBroker(sub_menu, 'none')
    })
})

function toggleMenuBroker(btn, display) {
    btn.style.display = display
}

function changeClass(clickedElement) {
    var navigationLinks = document.querySelectorAll('nav a')
    console.log(clickedElement)
    navigationLinks.forEach(function (link) {
        link.parentElement.classList.remove('selected')
    })
    clickedElement.parentElement.classList.add('selected')
}
