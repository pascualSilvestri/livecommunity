
//Referncias a los objetos en el DOM
const modal = document.querySelector(".modal-telegram");
const btn_salir = document.querySelector('.btn-salir');
const btn_video = document.querySelector('.link-video-telegram');

//Mostrar modal
if(btn_video!=null){
    btn_video.addEventListener('click',e=>{
        modal.style.display = "flex"
    })
}

//Oculatar modual
if(btn_salir != null){
    btn_salir.addEventListener('click',e=>{
        modal.style.display = "none"
    })
}