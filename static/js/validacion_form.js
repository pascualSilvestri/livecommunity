import { modalError } from "./modal.js"

// Elementos del DOM
const formElements = {
    nombre: document.getElementById('id_nombre'),
    apellido: document.getElementById("id_apellido"),
    userTelegram: document.getElementById("id_userTelegram"),
    userDiscord: document.getElementById("id_userDiscord"),
    email: document.getElementById("id_email"),
    telefono: document.getElementById("id_telefono"),
    nacionalidad: document.getElementById('id_nacionalidad'),
    wallet: document.getElementById('id_wallet'),
    documento: document.getElementById('documento'),
    form: document.querySelector('.form-send'),
    mensajeVerificado: document.querySelector('.mensaje-verificar-cliente'),
    sectionValidacion: document.getElementById('nuevo_id_cliente')
};

// Estado de errores
const errorState = {
    nombre: false,
    apellido: false,
    email: false,
    userTelegram: false,
    telefono: false,
    userDiscord: false,
    nacionalidad: false,
    wallet: false,
    documento: false
};

// Expresiones regulares
const regex = {
    nombre: /^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$/,
    email: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
    usuario: /^@[a-zA-Z0-9_]+$/,
    telefono: /^[0-9]*$/,
    // wallet: /^0x[a-fA-F0-9]{40}$/ // Ejemplo para direcciones Ethereum. Ajusta según tus necesidades.
    wallet: /[a-fA-F0-9]/,
    nacionalidad: /[a-zA-Z]/,
    documento: /^[0-9]{7,10}$/, // Asumiendo que el documento tiene entre 7 y 10 dígitos
};

// Mensajes de error
const errorMessages = {
    nombre: `No puede estar vacío, mínimo 2 letras, no se aceptan números.`,
    email: `El formato correcto es ejemplo@correo.com`,
    usuario: `Debe comenzar con un @ ejemplo @usuarioTelegram`,
    btnError: "Por favor complete los campos correctamente.",
    telefono: 'Acepta solo números',
    noDeposito: 'Para terminar el proceso de registro debe fondear la cuenta de Skilling.',
    nacionalidad: 'Por favor seleccione una nacionalidad',
    wallet: 'Ingrese una dirección de wallet válida',
    documento: 'El documento debe contener entre 7 y 10 dígitos numéricos.'
};

// Funciones auxiliares
const setValidState = (element, isValid) => {
    element.classList.toggle("sin-validar", !isValid);
    element.classList.toggle("valida", isValid);
};

const validateField = (field, value, regexKey) => {
    let isValid;
    if (regexKey === 'nacionalidad') {
        isValid = value !== "";
    } else {
        isValid = value !== "" && (regexKey ? regex[regexKey].test(value) : true);
    }
    setValidState(field, isValid);
    const fieldName = field.id.replace('id_', '');
    errorState[fieldName] = isValid;
    console.log(`Campo ${fieldName}: ${isValid ? 'válido' : 'inválido'}`);
    if (!isValid) modalError(errorMessages[regexKey] || errorMessages[fieldName] || errorMessages.nombre);
};

// Validación de campos
const setupFieldValidation = () => {
    Object.entries(formElements).forEach(([key, element]) => {
        if (element && (element.tagName === 'INPUT' || element.tagName === 'SELECT')) {
            element.addEventListener("blur", (e) => {
                let regexKey;
                switch(key) {
                    case 'nombre':
                    case 'apellido':
                        regexKey = 'nombre';
                        break;
                    case 'email':
                        regexKey = 'email';
                        break;
                    case 'telefono':
                        regexKey = 'telefono';
                        break;
                    case 'nacionalidad':
                        regexKey = 'nacionalidad';
                        break;
                    case 'wallet':
                        regexKey = 'wallet';
                        break;
                    case 'documento':
                        regexKey = 'documento';
                        break;
                    default:
                        regexKey = 'usuario';
                }
                validateField(e.target, e.target.value, regexKey);
            });
        }
    });
};

// Validación de ID de cliente



const setupFormValidation = () => {
    if (!formElements.form) return;
    formElements.form.addEventListener('submit', (e) => {
        console.log("Estado de errores antes de enviar:", errorState);
        if (Object.values(errorState).every(Boolean)) {
            if (!confirm("Confirma que los datos están ingresados correctamente")) {
                e.preventDefault();
            }
        } else {
            console.log("Campos con error:", Object.entries(errorState).filter(([key, value]) => !value));
            modalError(errorMessages.btnError);
            e.preventDefault();
        }
    });
};

// Inicialización
const init = () => {
    setupFieldValidation();
    validateClientId();
    setupFormValidation();
};

init();
