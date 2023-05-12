const modal_cliente = document.querySelector(".modal-id-cliente");
const link = document.querySelector(".link-video-telegram");
const salir = document.querySelector(".salir-cliente");


//Crear modal error
function abrirModal(mensaje){
    const body = document.body
    const modal = document.createElement('div')
    modal.classList.add('modaleError')
    const msj = document.createElement('p')
    msj.innerHTML=mensaje;
    modal.appendChild(msj)
    body.appendChild(modal)
    
} 
//cerrar modal error
function cerrarModal(){
    const modal = document.querySelector('.modaleError')
    if(modal != null){
        modal.style.display = 'none'
        modal.remove();
    }
    
}


//modal error
export function modalError(mensaje){
    abrirModal(mensaje)
    setTimeout(cerrarModal,3000)
}

if(link != null){
    link.addEventListener('click',e=>{
        modal_cliente.style.display = "flex"
    })
}

//Oculatar modual
if(salir!= null){
    salir.addEventListener('click',e=>{
        modal_cliente.style.display = "none"
    })
}





/*modal telegram*/
//Referncias a los objetos en el DOM
const modal = document.querySelector(".modal-telegram");
const btn_salir = document.querySelector('.btn-salir');
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