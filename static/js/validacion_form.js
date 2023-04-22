const nombre = document.getElementById('id_nombre')
const apellido = document.getElementById("id_apellido")
const userTelegram = document.getElementById("id_userTelegram")
const email = document.getElementById("id_correo")
const telefono = document.getElementById("id_telefono")
const idAfiliado = document.getElementById("id_idAfiliado")

const contenedores = document.querySelectorAll('.inputbox')

const form = document.querySelector('.form-send')

const btn = document.querySelector('#btn-send')

import { send_handle } from './app.js'


let errorN = false
let errorA = false
let errorE = false
let errorU = false
let errorT = false

form.addEventListener('click', e => {
    e.preventDefault();
})

const redex = {
    'nombre': /^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$/,
    'correo': /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
    'usuario': /^@[a-zA-Z0-9_]+$/,
    'telefono': /^[0-9]*$/
};

const errorMensaje = {
    'nombre': `No puede estar vacio ni contener numeros, min-3 letras.`,
    'apellido': `No puede estar vacio ni contener numeros, min-3 letras.`,
    'email': `El formato correcto es ejemplo@correo.com`,
    'usuario': `No puede estar vacio debe contener min 2 letra`,
    'btnError': "Por favor complete los campo correctamente."
};


//ingreso un input y una expresion regular para saber si esta bien Parametros (input, string)
const validarCampo = (nombre, redexNombre) => {
    return redex[redexNombre].test(nombre.value)
}


function error(cont) {
    cont.classList.add("sin-validar");
    cont.classList.remove("valida");
}

function valido(cont) {
    cont.classList.remove("sin-validar")
    cont.classList.add("valida");
}

const enviarDatos = () => {
    if (errorN && errorA && errorE && errorT && errorU) {
        return true
    }
}

function validar(input) {
    if (input != null) {
        input.addEventListener("keyup", e => {
            if (e.target.id == "id_nombre") {
                if (input.value != "" && redex["nombre"].test(input.value)) {
                    valido(input)
                    errorN = true
                } else {
                    if (input.value == "") {
                        errorN = false
                    }
                    if (!errorN) {
                        error(input)
                        errorN = false
                    }
                }

            }

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


btn.addEventListener('click', e => {
    
    if(enviarDatos()){
        const confirmar = confirm("Confirma que los datos estan ingresados correctamente")
        if(confirmar){
            form.submit()
            send_handle()
        }
       
    }
})

















validar(nombre)
validar(apellido)
validar(email)
validar(telefono)
validar(userTelegram)



