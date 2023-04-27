
//Importamos la funcion send:handle de whatsappCOntroller.js


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
var miParrafo = document.getElementById("mensaje");


//verificadores de que los inputs estan correctamente ingresados
let errorN = false
let errorA = false
let errorE = false
let errorU = false
let errorT = false

//Expreciones regulares para validar cada tipo de input
const redex = {
    'nombre': /^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$/,
    'correo': /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
    'usuario': /^@[a-zA-Z0-9_]+$/,
    'telefono': /^[0-9]*$/
};

//Mensaje de error para cada tipo de input 
const errorMensaje = {
    'nombre': `No puede estar vacio, min-2 letras.`,
    'apellido': `No puede estar vacio, min-2 letras.`,
    'email': `El formato correcto es ejemplo@correo.com`,
    'usuario': `Debe comenzar con un @`,
    'btnError': "Por favor complete los campo correctamente."
};


//ingreso un input y una expresion regular para saber si esta bien Parametros (input, string)
const validarCampo = (nombre, redexNombre) => {
    return redex[redexNombre].test(nombre.value)
}

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
    if (errorN && errorA && errorE && errorT && errorU) {
        return true 
    }
}





//Logica para validar los inputs 
//toma un valor input 

function validar(input) {
    //verificamos que no es null
    if (input != null) {
        //asociamos un event del tipo keyup para verificar cada ves que se suelta una tecla
        input.addEventListener("keyup", e => {
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



//validamos que los datos esten correcto
//i lo estan se envia en form
//si no lo estan, prevenimos que no se envien


// verificamos que no es null el form
if(form != null){
    //asociamos un evento tipo submit al form
    form.addEventListener('submit', e => {
        // verificamos que los datos estan ingresado correctamtente
        if (enviarDatos()) {
            //mostramos al usuario un modal para confirmar que ingreso los datos correctos
            const confirmar = confirm("Confirma que los datos estan ingresados correctamente")
            if (confirmar) {
                //enviamos el formulario
                form.submit()
            }else{
                //prevenimos el envio de datos si el usuario cancela el modal
                e.preventDefault();
            }

        }else{
            //prevenimos el envio de datos si los datos no estan correctametne ingresados
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



