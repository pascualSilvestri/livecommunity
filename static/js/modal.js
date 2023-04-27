
//Referncias a los objetos en el DOM
const modal = document.querySelector(".modal-telegram");
const btn_salir = document.querySelector('.btn-salir');
const btn_video = document.querySelector('.link-video-telegram');
const p = document.querySelector('.text-video-telegram')

//Mostrar modal
if(p != null){
    p.addEventListener('click',e=>{
        console.log('apreteboton de video')
        modal.style.display = "flex"
    })
}

//Oculatar modual
if(btn_salir != null){
    btn_salir.addEventListener('click',e=>{
        modal.style.display = "none"
    })
}