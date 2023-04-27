// Obtener el elemento <p>
const miParrafo = document.getElementById("mensaje");

// Esperar 3 segundos y luego ocultar el elemento <p>
setTimeout(()=> {

	if(miParrafo!=null){
		miParrafo.style.display = "none";
	}

}, 3000); // 3000 milisegundos = 3 segundos


let body = document.body; 
let element = document.getElementById("wsp"); 
//Update DOM on scroll 
document.addEventListener("scroll", function() {  
    let scrollAmt = window.pageYOffset || document.documentElement.scrollTop; 
	if(window.innerHeight/4 >= scrollAmt) 
		if(element != null){
			element.style.display = "none"; 
		}
	 	 
  	else{
		if (element != null){
			element.style.display = "block"; 
		}
		
	}	
		
}); 


