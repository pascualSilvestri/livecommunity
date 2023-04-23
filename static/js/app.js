

let body = document.body; 
let element = document.getElementById("wsp"); 
//Update DOM on scroll 
document.addEventListener("scroll", function() {  
    let scrollAmt = window.pageYOffset || document.documentElement.scrollTop; 
	if(window.innerHeight/4 >= scrollAmt) 
	 	element.style.display = "none";  
  	else	 
		element.style.display = "block"; 
}); 
const divs = document.getElementsByClassName('.mensaje');

let i=0;
let interval = setInterval( () => {
	divs[i++].style.display = 'none';
	if(i==divs.length)
		clearInterval(interval);
}, 2500 );

function send_handle(){
	const nombre = document.getElementById('id_nombre').value.trim()
	const apellido = document.getElementById("id_apellido").value.trim()
	const userTelegram = document.getElementById("id_userTelegram").value.trim()
	const email = document.getElementById("id_correo").value.trim()
	const telefono = document.getElementById("id_telefono").value.trim()
	const idAfiliado = document.getElementById("id_idAfiliado").value.trim()
	
  let win = window.open(`https://wa.me/541138658887?text=Mi%20nombre%20es%20${nombre}%20${apellido}%0AMi%20usuario%20de%20Telegram%20es%20${userTelegram}%0AMi%20email%20es%20${email}%0AMi%20telefono%20es%20${telefono}%0AMi%20IdAfiliado%20es%20${idAfiliado}%0A%0A%0A%20**POR FAVOR ADJUNTAR FOTO DE COMPROBANTE DE FONDEO DE LIBERTEX**`, '_blank');
  win;
}

export { send_handle };