// document.addEventListener('DOMContentLoaded', function () {
//     // Espera a que se cargue el DOM antes de intentar seleccionar el elemento
//     var staff = document.querySelector('.staff')

//     if (staff) {
//         // Realiza operaciones solo si el elemento fue encontrado
//         const wrapperStaff = document.querySelector('.wrapperStaff')
//         const carouselStaff = document.querySelector('.carouselStaff')
//         const firstCardStaffWidth =
//             carouselStaff.querySelector('.cardStaff').offsetWidth
//         const arrowBtns = document.querySelectorAll('.wrapperStaff i')
//         const carouselStaffChildrens = [...carouselStaff.children]

//         let isDragging = false,
//             isAutoPlay = true,
//             startX,
//             startScrollLeft,
//             timeoutId

//         // Get the number of cardStaffs that can fit in the carouselStaff at once
//         let cardStaffPerView = Math.round(
//             carouselStaff.offsetWidth / firstCardStaffWidth
//         )

//         // Insert copies of the last few cardStaffs to the beginning of the carouselStaff for infinite scrolling
//         carouselStaffChildrens
//             .slice(-cardStaffPerView)
//             .reverse()
//             .forEach((cardStaff, index) => {
//                 const clonedCardStaff = cardStaff.cloneNode(true)
//                 clonedCardStaff.classList.add(
//                     'infinite-cardStaff',
//                     `infinite-cardStaff-${index}`
//                 )
//                 carouselStaff.insertAdjacentElement(
//                     'afterbegin',
//                     clonedCardStaff
//                 )
//             })

//         // Insert copies of the first few cardStaffs to the end of the carouselStaff for infinite scrolling
//         carouselStaffChildrens
//             .slice(0, cardStaffPerView)
//             .forEach((cardStaff, index) => {
//                 const clonedCardStaff = cardStaff.cloneNode(true)
//                 clonedCardStaff.classList.add(
//                     'infinite-cardStaff',
//                     `infinite-cardStaff-${index}`
//                 )
//                 carouselStaff.insertAdjacentElement(
//                     'beforeend',
//                     clonedCardStaff
//                 )
//             })

//         // Scroll the carouselStaff at appropriate postition to hide first few duplicate cardStaffs on Firefox
//         carouselStaff.classList.add('no-transition')
//         carouselStaff.scrollLeft = carouselStaff.offsetWidth
//         carouselStaff.classList.remove('no-transition')

//         // Add event listeners for the arrow buttons to scroll the carouselStaff left and right
//         arrowBtns.forEach((btn) => {
//             btn.addEventListener('click', () => {
//                 carouselStaff.scrollLeft +=
//                     btn.id == 'left'
//                         ? -firstCardStaffWidth
//                         : firstCardStaffWidth
//             })
//         })

//         const dragStart = (e) => {
//             isDragging = true
//             carouselStaff.classList.add('dragging')
//             // Records the initial cursor and scroll position of the carouselStaff
//             startX = e.pageX
//             startScrollLeft = carouselStaff.scrollLeft
//         }

//         const dragging = (e) => {
//             if (!isDragging) return // if isDragging is false return from here
//             // Updates the scroll position of the carouselStaff based on the cursor movement
//             carouselStaff.scrollLeft = startScrollLeft - (e.pageX - startX)
//         }

//         const dragStop = () => {
//             isDragging = false
//             carouselStaff.classList.remove('dragging')
//         }

//         const infiniteScroll = () => {
//             // If the carouselStaff is at the beginning, scroll to the end
//             if (carouselStaff.scrollLeft === 0) {
//                 carouselStaff.classList.add('no-transition')
//                 carouselStaff.scrollLeft =
//                     carouselStaff.scrollWidth - 2 * carouselStaff.offsetWidth
//                 carouselStaff.classList.remove('no-transition')
//             }
//             // If the carouselStaff is at the end, scroll to the beginning
//             else if (
//                 Math.ceil(carouselStaff.scrollLeft) ===
//                 carouselStaff.scrollWidth - carouselStaff.offsetWidth
//             ) {
//                 carouselStaff.classList.add('no-transition')
//                 carouselStaff.scrollLeft = carouselStaff.offsetWidth
//                 carouselStaff.classList.remove('no-transition')
//             }

//             // Clear existing timeout & start autoplay if mouse is not hovering over carouselStaff
//             clearTimeout(timeoutId)
//             if (!wrapperStaff.matches(':hover')) autoPlay()
//         }

//         const autoPlay = () => {
//             if (window.innerWidth < 800 || !isAutoPlay) return // Return if window is smaller than 800 or isAutoPlay is false
//             // Autoplay the carouselStaff after every 2500 ms
//             timeoutId = setTimeout(
//                 () => (carouselStaff.scrollLeft += firstCardStaffWidth),
//                 2200
//             )
//         }
//         autoPlay()

//         carouselStaff.addEventListener('mousedown', dragStart)
//         carouselStaff.addEventListener('mousemove', dragging)
//         document.addEventListener('mouseup', dragStop)
//         carouselStaff.addEventListener('scroll', infiniteScroll)
//         wrapperStaff.addEventListener('mouseenter', () =>
//             clearTimeout(timeoutId)
//         )
//         wrapperStaff.addEventListener('mouseleave', autoPlay)

//         // Tu lógica de slider para el personal aquí
//     }
// })document.addEventListener('DOMContentLoaded', function () {
//     // Espera a que se cargue el DOM antes de intentar seleccionar el elemento
//     var staff = document.querySelector('.staff')

//     if (staff) {
//         // Realiza operaciones solo si el elemento fue encontrado
//         const wrapperStaff = document.querySelector('.wrapperStaff')
//         const carouselStaff = document.querySelector('.carouselStaff')
//         const firstCardStaffWidth =
//             carouselStaff.querySelector('.cardStaff').offsetWidth
//         const arrowBtns = document.querySelectorAll('.wrapperStaff i')
//         const carouselStaffChildrens = [...carouselStaff.children]

//         let isDragging = false,
//             isAutoPlay = true,
//             startX,
//             startScrollLeft,
//             timeoutId

//         // Get the number of cardStaffs that can fit in the carouselStaff at once
//         let cardStaffPerView = Math.round(
//             carouselStaff.offsetWidth / firstCardStaffWidth
//         )

//         // Insert copies of the last few cardStaffs to the beginning of the carouselStaff for infinite scrolling
//         carouselStaffChildrens
//             .slice(-cardStaffPerView)
//             .reverse()
//             .forEach((cardStaff, index) => {
//                 const clonedCardStaff = cardStaff.cloneNode(true)
//                 clonedCardStaff.classList.add(
//                     'infinite-cardStaff',
//                     `infinite-cardStaff-${index}`
//                 )
//                 carouselStaff.insertAdjacentElement(
//                     'afterbegin',
//                     clonedCardStaff
//                 )
//             })

//         // Insert copies of the first few cardStaffs to the end of the carouselStaff for infinite scrolling
//         carouselStaffChildrens
//             .slice(0, cardStaffPerView)
//             .forEach((cardStaff, index) => {
//                 const clonedCardStaff = cardStaff.cloneNode(true)
//                 clonedCardStaff.classList.add(
//                     'infinite-cardStaff',
//                     `infinite-cardStaff-${index}`
//                 )
//                 carouselStaff.insertAdjacentElement(
//                     'beforeend',
//                     clonedCardStaff
//                 )
//             })

//         // Scroll the carouselStaff at appropriate postition to hide first few duplicate cardStaffs on Firefox
//         carouselStaff.classList.add('no-transition')
//         carouselStaff.scrollLeft = carouselStaff.offsetWidth
//         carouselStaff.classList.remove('no-transition')

//         // Add event listeners for the arrow buttons to scroll the carouselStaff left and right
//         arrowBtns.forEach((btn) => {
//             btn.addEventListener('click', () => {
//                 carouselStaff.scrollLeft +=
//                     btn.id == 'left'
//                         ? -firstCardStaffWidth
//                         : firstCardStaffWidth
//             })
//         })

//         const dragStart = (e) => {
//             isDragging = true
//             carouselStaff.classList.add('dragging')
//             // Records the initial cursor and scroll position of the carouselStaff
//             startX = e.pageX
//             startScrollLeft = carouselStaff.scrollLeft
//         }

//         const dragging = (e) => {
//             if (!isDragging) return // if isDragging is false return from here
//             // Updates the scroll position of the carouselStaff based on the cursor movement
//             carouselStaff.scrollLeft = startScrollLeft - (e.pageX - startX)
//         }

//         const dragStop = () => {
//             isDragging = false
//             carouselStaff.classList.remove('dragging')
//         }

//         const infiniteScroll = () => {
//             // If the carouselStaff is at the beginning, scroll to the end
//             if (carouselStaff.scrollLeft === 0) {
//                 carouselStaff.classList.add('no-transition')
//                 carouselStaff.scrollLeft =
//                     carouselStaff.scrollWidth - 2 * carouselStaff.offsetWidth
//                 carouselStaff.classList.remove('no-transition')
//             }
//             // If the carouselStaff is at the end, scroll to the beginning
//             else if (
//                 Math.ceil(carouselStaff.scrollLeft) ===
//                 carouselStaff.scrollWidth - carouselStaff.offsetWidth
//             ) {
//                 carouselStaff.classList.add('no-transition')
//                 carouselStaff.scrollLeft = carouselStaff.offsetWidth
//                 carouselStaff.classList.remove('no-transition')
//             }

//             // Clear existing timeout & start autoplay if mouse is not hovering over carouselStaff
//             clearTimeout(timeoutId)
//             if (!wrapperStaff.matches(':hover')) autoPlay()
//         }

//         const autoPlay = () => {
//             if (window.innerWidth < 800 || !isAutoPlay) return // Return if window is smaller than 800 or isAutoPlay is false
//             // Autoplay the carouselStaff after every 2500 ms
//             timeoutId = setTimeout(
//                 () => (carouselStaff.scrollLeft += firstCardStaffWidth),
//                 2200
//             )
//         }
//         autoPlay()

//         carouselStaff.addEventListener('mousedown', dragStart)
//         carouselStaff.addEventListener('mousemove', dragging)
//         document.addEventListener('mouseup', dragStop)
//         carouselStaff.addEventListener('scroll', infiniteScroll)
//         wrapperStaff.addEventListener('mouseenter', () =>
//             clearTimeout(timeoutId)
//         )
//         wrapperStaff.addEventListener('mouseleave', autoPlay)

//         // Tu lógica de slider para el personal aquí
//     }
// })

