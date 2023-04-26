const bandera = false
const idClientes = []
const input = document.querySelector('#id_nuevo_cliente')
const section_A_Validar = document.querySelector('.validacion-2')
const datos = fetch('verificarNuevoCliente/')
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error en la respuesta del servidor');
        }
    })
    .then(data => {
        data['data'].forEach(element => {
            idClientes.push(element)
        });
    })
    .catch(error => {
        // Maneja errores
        console.error(error);
    });

console.log(idClientes)

//Verifica si esta el elemento en la base datos 
//retorna un boolean
const verificarNuevoCliente = (input,array)=>{
    for(const element of array){
        if(input.value==element){
            return true
        }
    }
}


//compruebo que el input no sea null
if(input != null){
    //le asocio un evento tipo blur validar cuando desenfoca 
    input.addEventListener('blur', e => {
        //una exprecion regular para validar que sean solo numeros y minimo 10 caracter
        const redex = /^[0-9]{10,}$/
        //verifico con la funcion verificarNuevo si exite en base de datos
        //con la exprecion regular verifico que sea numero y mini 10 caracter
        if(!verificarNuevoCliente(input,idClientes)&&redex.test(input.value)){
            //si cumple con los requerimientos se habilitas las siguientes secciones
            section_A_Validar.style.display = 'block'
        }else{
            //si no cumple no se muestran las siguientes secciones
            section_A_Validar.style.display = 'none'
        }
        

    })
    
}


