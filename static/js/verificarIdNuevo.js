const bandera = false
const idClientes = []
const input = document.querySelector('#id_nuevo_cliente')
const input_idCliente = document.querySelector('#id_cliente')
const section_A_Validar = document.querySelector('.validacion-2')
const mensaje_verificado = document.querySelector('.mensaje-verificar-cliente')
const mensaje_no_verificado = document.querySelector('.error-verificar-cliente')
const btn_validar = document.querySelector('.button-verificar-cliente')
const section_de_validacion = document.querySelector('.verificar-nuevo-cliente')
//obtener datos de la api de django
const datos = fetch('verificarNuevoCliente/')
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error en la respuesta del servidor'+ response.statusText);
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
if(btn_validar != null){
    //le asocio un evento tipo blur validar cuando desenfoca 
    btn_validar.addEventListener('click', e => {
        //una exprecion regular para validar que sean solo numeros y minimo 10 caracter
        const redex = /^[0-9]{10,}$/
        //verifico con la funcion verificarNuevo si exite en base de datos
        //con la exprecion regular verifico que sea numero y mini 10 caracter
        if(!verificarNuevoCliente(input,idClientes)&&redex.test(input.value)){
            //si cumple con los requerimientos se habilitas las siguientes secciones
            section_A_Validar.style.display = 'block'
            mensaje_verificado.style.display= 'block'
            input_idCliente.value = input.value
            section_de_validacion.style.display = 'none'
            //Muestra mensaje de verificacion valida 3 segundos
            setTimeout(()=> {

                if(mensaje_verificado!=null){
                    mensaje_verificado.style.display = 'none'
                }
            
            }, 3000); 

        }else{
            //si no cumple no se muestran las siguientes secciones
            section_A_Validar.style.display = 'none'
            mensaje_verificado.style.display= 'none'
            mensaje_no_verificado.style.display = 'block'
            input_idCliente.value = ''
        }
        

    })
    
}


