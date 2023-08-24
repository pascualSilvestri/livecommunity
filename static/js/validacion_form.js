
//Importamos la funcion send:handle de whatsappCOntroller.js
import { modalError } from "./modal.js"

//Referencias a objetos del DOM
const nombre = document.getElementById('id_nombre')
const apellido = document.getElementById("id_apellido")
const userTelegram = document.getElementById("id_userTelegram")
const email = document.getElementById("id_correo")
const telefono = document.getElementById("id_telefono")
const idAfiliado = document.getElementById("id_idAfiliado")
const contenedores = document.querySelectorAll('.inputbox')
const form = document.querySelector('.form-send')
const btn = document.querySelector('#btn-send')
const section_de_validacion = document.getElementById('nuevo_id_cliente')
const mensaje_verificado = document.querySelector('.mensaje-verificar-cliente')

const input_idCliente = document.querySelector('#id_cliente')
const input_validar = document.querySelector('#id_nuevo_cliente')

const input = document.querySelector('#id_nuevo_cliente')
const inputNombre = document.querySelector('#nombre_nuevo_cliente')

var miParrafo = document.getElementById("mensaje");

const idClientes = []

//verificadores de que los inputs estan correctamente ingresados
let errorN = false
let errorA = false
let errorE = false
let errorU = false
let errorT = false
let errorC = false

//Expreciones regulares para validar cada tipo de input
const redex = {
    'nombre': /^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$/,
    'correo': /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
    'usuario': /^@[a-zA-Z0-9_]+$/,
    'telefono': /^[0-9]*$/
};

//Mensaje de error para cada tipo de input 
const errorMensaje = {
    'nombre': `No puede estar vacio, min-2 letras no se aceptan numeros.`,
    'email': `El formato correcto es ejemplo@correo.com`,
    'usuario': `Debe comenzar con un @ ejemplo @usuarioTelegram`,
    'btnError': "Por favor complete los campo correctamente.",
    'idCliente': 'Su cuenta no esta verificada correctamente, por favor verifique el ID ingresado',
    'telefono': 'Acepta solo numeros',
    'noDeposito': 'Para terminar el proceso de registro debe fondear la cuenta de libertex.'
};


//ingreso un input y una expresion regular para saber si esta bien Parametros (input, string)
// const validarCampo = (nombre, redexNombre) => {
//     return redex[redexNombre].test(nombre.value)
// }

//Cambia el border del input para avisar que hay un error en los datos introducidos
function error(cont) {
    cont.classList.add("sin-validar");
    cont.classList.remove("valida");
}
//Cambia el color del borde para avisar que los datos introducidos son correctos
function valido(cont) {
    cont.classList.remove("sin-validar")
    cont.classList.add("valida");
}



//Verifica que no hay error en los datos ingresado
//return un Boolean

const enviarDatos = () => {
    if (errorN && errorA && errorE && errorT && errorU && errorC) {
        return true
    }
}

async function obtenerDatos() {
    try {

        //http://127.0.0.1:8000/api/verificar/
        //https://livecommunity.info/api/verificar/
        const response = await fetch('https://livecommunity.info/api/verificar/'); // cambiar a localhost para local 
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        const data = await response.json();
        data['data'].forEach(element => {
            idClientes.push(element);
        });
    } catch (error) {
        console.error(error);
    }
}

obtenerDatos()

const deposito = (array) => {

    const client = array.filter(c => c.client == input_idCliente.value)

    if(client.length>0){
        if (client[0].deposit == 1) {
            return true
        } else {
            return false
        }
    }
    
}





//Logica para validar los inputs 
//toma un valor input 

function validar(input) {
    //verificamos que no es null
    if (input != null) {
        //asociamos un event del tipo keyup para verificar cada ves que se suelta una tecla
        input.addEventListener("blur", e => {
            console.log(e.target.id)
            //verificamos el input que estamos presionado o enfocando
            if (e.target.id == "id_nombre") {
                //verificamos que el input no este vacio y cumpla con la validacion de la exprecion regular
                if (input.value != "" && redex["nombre"].test(input.value)) {
                    //si es valido le colocamos un border color verde
                    valido(input)
                    //errorN la cambiamos a true para avisar de que el dato ingresado es correcto
                    errorN = true
                    //si no 
                } else {
                    //verificamos que el input este vacio
                    modalError(errorMensaje.nombre)
                    if (input.value == "") {
                        //errorN la igualamos a false para avisar de que hay un error
                        errorN = false
                    }
                    // verificamos de que errorN es true y el input esta vacio le cambiamos a false y le colocamos border color rojo
                    if (!errorN) {
                        error(input)
                        errorN = false
                    }
                }

            }
            // misma logica que arriba para otro input 
            if (e.target.id == "id_apellido") {

                if (input.value != "" && redex["nombre"].test(input.value)) {
                    valido(input)
                    errorA = true
                    if (input.value == "") {
                        errorA = false
                    }

                } else {
                    modalError(errorMensaje.nombre)
                    if (input.value == "") {
                        errorA = false
                    }
                    if (!errorA) {
                        error(input)
                        errorA = false

                    }
                }

            }

            if (e.target.id == "id_correo") {

                if (input.value != "" && redex["correo"].test(input.value)) {
                    valido(input)
                    errorE = true
                    if (input.value == "") {
                        errorE = false
                    }

                } else {
                    modalError(errorMensaje.email)
                    if (input.value == "") {
                        errorE = false
                    }
                    if (!errorE) {
                        error(input)
                        errorE = false

                    }
                }
            }

            if (e.target.id == "id_telefono") {

                if (input.value != "" && redex["telefono"].test(input.value)) {
                    valido(input)
                    errorT = true
                } else {
                    modalError(errorMensaje.telefono)
                    if (input.value == "" || !redex["telefono"].test(input.value)) {
                        errorT = false
                    }
                    if (!errorT) {
                        error(input)
                        errorT = false

                    }
                }

            }

            if (e.target.id == "id_userTelegram") {

                if (input.value != "" && redex["usuario"].test(input.value)) {
                    valido(input)
                    errorU = true
                    if (input.value == "") {
                        errorU = false
                    }

                } else {
                    modalError(errorMensaje.usuario)
                    if (input.value == "") {
                        errorU = false
                    }
                    if (!errorU) {
                        error(input)
                        errorU = false

                    }

                }

            }
        })
    }
}

function validarId() {
    if (input_idCliente.value == input_validar.value) {
        return true;
    }
    return false;
}

if (input_idCliente != null){
    input_idCliente.addEventListener('blur', e => {

        if (input_idCliente.value != "" && redex["telefono"].test(input_idCliente.value) && validarId() && deposito(idClientes)) {
            valido(input_idCliente)
    
            mensaje_verificado.style.display = 'block'
            setTimeout(() => {
    
                if (mensaje_verificado != null) {
                    mensaje_verificado.style.display = 'none'
                }
    
            }, 3000);
            section_de_validacion.style.display = 'none'
            errorC = true
            if (input_idCliente.value == "") {
                errorC = false
            }
        } else if (!deposito(idClientes)) {
            modalError(errorMensaje.noDeposito)
            if (input_idCliente.value == "" || !validar()) {
                errorC = false
            }
            if (!errorC) {
                error(input_idCliente)
                errorC = false
    
            }
        } else {
            modalError(errorMensaje.idCliente)
            section_de_validacion.style.display = 'flex'
            section_de_validacion.scrollIntoView()
            window.scrollTo({
                top: 1200,
                behavior: "smooth"
            });
            if (input_idCliente.value == "" || !validar()) {
                errorC = false
            }
            if (!errorC) {
                error(input_idCliente)
                errorC = false
    
            }
    
        }
    })
} 


//validamos que los datos esten correcto
//i lo estan se envia en form
//si no lo estan, prevenimos que no se envien


// verificamos que no es null el form
if (form != null) {
    //asociamos un evento tipo submit al form
    form.addEventListener('submit', e => {
        // verificamos que los datos estan ingresado correctamtente
        if (enviarDatos()) {
            //mostramos al usuario un modal para confirmar que ingreso los datos correctos
            const confirmar = confirm("Confirma que los datos estan ingresados correctamente")
            if (!confirmar) {
                //prevenimos el envio de datos si el usuario cancela el modal
                e.preventDefault();
            }

        } else {
            //prevenimos el envio de datos si los datos no estan correctametne ingresados
            modalError(errorMensaje.btnError)
            e.preventDefault();
        }
       
    })
}



// btn.addEventListener('click', e => {

//     if (enviarDatos()) {
//         const confirmar = confirm("Confirma que los datos estan ingresados correctamente")
//         if (confirmar) {
//             form.submit()
//             send_handle()
//         }

//     }
// })




//Validamos cada input
validar(nombre)
validar(apellido)
validar(email)
validar(telefono)
validar(userTelegram)



