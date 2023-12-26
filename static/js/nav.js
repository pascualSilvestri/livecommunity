document.addEventListener('DOMContentLoaded', function () {
    // Obtiene el valor de la variable desde localStorage
    var selectedLinkId = localStorage.getItem('selectedLinkId')

    // Establece la clase 'selected' en el elemento correspondiente
    if (selectedLinkId) {
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
            // Cambia la clase
            changeClass(this)

            // Guarda el ID del enlace seleccionado en localStorage
            var clickedElementId = this.parentElement.id
            localStorage.setItem('selectedLinkId', clickedElementId)

            console.log('Toqué este enlace: ' + this)
        })
    })
})

function changeClass(clickedElement) {
    var navigationLinks = document.querySelectorAll('nav a')
    console.log(clickedElement)
    navigationLinks.forEach(function (link) {
        link.parentElement.classList.remove('selected')
    })
    clickedElement.parentElement.classList.add('selected')
}
