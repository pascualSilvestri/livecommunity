const bandera = false
const idClientes = []
const input = document.querySelector('#id_nuevo_cliente')
const inputNombre = document.querySelector('#nombre_nuevo_cliente')
// const input_idCliente = document.querySelector('#id_cliente')
const section_A_Validar = document.querySelector('.validacion-2')
const mensaje_verificado = document.querySelector('.mensaje-verificar-cliente')
const mensaje_no_verificado = document.querySelector('.error-verificar-cliente')
const btn_validar = document.querySelector('.button-verificar-cliente')
const section_de_validacion = document.querySelector('.verificar-nuevo-cliente')

async function obtenerDatos() {
    try {
      
        //http://127.0.0.1:8000/api/verificar/
        //https://livecommunity.info/api/verificar/
      const response = await fetch('http://127.0.0.1:8000/api/skilling/verificar/'); // cambiar a localhost para local
      if (!response.ok) {
        throw new Error('Error en la respuesta del servidor');
      }
      const data = await response.json();
      console.log(data)
      data['data'].forEach(element => {
        idClientes.push(element);
      });
    } catch (error) {
      console.error(error);
    }
  }

  obtenerDatos()

 
//Verifica si esta el elemento en la base datos 
//retorna un boolean

const verificarNuevoCliente = ()=>{

  // const client = idClientes.filter(e=> e.full_name.toLowerCase() == inputNombre.value.toLowerCase() && e.fpa.toLowerCase()== input.value.toLowerCase())
  const client = idClientes.filter(e=> e.client==input.value)
  if(client.length > 0){
    return true
  }
}

// if(btn_validar != null){
//   btn_validar.addEventListener('click',(e) =>{
//     verificarNuevoCliente()
//   })
// }



if(btn_validar != null){
    //le asocio un evento tipo blur validar cuando desenfoca 
    btn_validar.addEventListener('click', e => {
        //una exprecion regular para validar que sean solo numeros y minimo 10 caracter
        // const redex = /^[0-9]{2,}$/
        //verifico con la funcion verificarNuevo si exite en base de datos
        //con la exprecion regular verifico que sea numero y mini 10 caracter
        if(verificarNuevoCliente()){
            //si cumple con los requerimientos se habilitas las siguientes secciones
            section_A_Validar.style.display = 'block'
            section_de_validacion.style.display = 'none'
            //Muestra mensaje de verificacion valida 3 egundos 

        }else{
            //si no cumple no se muestran las siguientes secciones
            section_A_Validar.style.display = 'none'
            mensaje_verificado.style.display= 'none'
            mensaje_no_verificado.style.display = 'block'
            // input_idCliente.value = ''
        }
        

    })
    
}


