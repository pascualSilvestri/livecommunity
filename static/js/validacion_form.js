import { modalError } from "./modal.js"

// Elementos del DOM
const formElements = {
    nombre: document.getElementById('id_nombre'),
    apellido: document.getElementById("id_apellido"),
    userTelegram: document.getElementById("id_userTelegram"),
    userDiscord: document.getElementById("id_userDiscord"),
    email: document.getElementById("id_email"),
    telefono: document.getElementById("id_telefono"),
    idCliente: document.getElementById('id_cliente'),
    nacionalidad: document.getElementById('id_nacionalidad'),
    wallet: document.getElementById('id_wallet'),
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
    idCliente: false,
    userDiscord: false,
    nacionalidad: false,
    wallet: false
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
};

// Mensajes de error
const errorMessages = {
    nombre: `No puede estar vacío, mínimo 2 letras, no se aceptan números.`,
    email: `El formato correcto es ejemplo@correo.com`,
    usuario: `Debe comenzar con un @ ejemplo @usuarioTelegram`,
    btnError: "Por favor complete los campos correctamente.",
    idCliente: 'Su cuenta no está verificada correctamente, por favor verifique el ID ingresado',
    telefono: 'Acepta solo números',
    noDeposito: 'Para terminar el proceso de registro debe fondear la cuenta de Skilling.',
    nacionalidad: 'Por favor seleccione una nacionalidad',
    wallet: 'Ingrese una dirección de wallet válida'
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
        if (element && (element.tagName === 'INPUT' || element.tagName === 'SELECT') && key !== 'idCliente') {
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
                    default:
                        regexKey = 'usuario';
                }
                validateField(e.target, e.target.value, regexKey);
            });
        }
    });
};

// Validación de ID de cliente
const validateClientId = async () => {
    if (!formElements.idCliente) return;

    formElements.idCliente.addEventListener('blur', async () => {
        const value = formElements.idCliente.value;
        if (value && regex.telefono.test(value)) {
            try {
                const { esValido, haDepositado } = await validarIdYDeposito();
                if (esValido && haDepositado) {
                    setValidState(formElements.idCliente, true);
                    if (formElements.mensajeVerificado) {
                        formElements.mensajeVerificado.style.display = 'block';
                        setTimeout(() => {
                            if (formElements.mensajeVerificado) {
                                formElements.mensajeVerificado.style.display = 'none';
                            }
                        }, 3000);
                    }
                    if (formElements.sectionValidacion) {
                        formElements.sectionValidacion.style.display = 'none';
                    }
                    errorState.idCliente = true;
                } else {
                    setValidState(formElements.idCliente, false);
                    modalError(esValido ? errorMessages.noDeposito : errorMessages.idCliente);
                    if (esValido && formElements.sectionValidacion) {
                        formElements.sectionValidacion.style.display = 'flex';
                    }
                    errorState.idCliente = false;
                }
            } catch (error) {
                console.error("Error en la validación:", error);
                modalError("Error al validar el ID. Por favor, inténtelo de nuevo.");
                setValidState(formElements.idCliente, false);
                errorState.idCliente = false;
            }
        } else {
            modalError(errorMessages.idCliente);
            setValidState(formElements.idCliente, false);
            errorState.idCliente = false;
        }
    });
};

// Obtener datos del cliente
const obtenerDatos = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/skilling/proxy/${formElements.idCliente.value}/`);
        if (!response.ok) throw new Error("Error en la respuesta del servidor");
        return await response.json();
    } catch (error) {
        console.error("Error al obtener datos:", error);
        return null;
    }
};

// Validar ID y depósito
const validarIdYDeposito = async () => {
    const datos = await obtenerDatos();
    if (!datos || !datos.registrations || datos.registrations.length === 0) {
        return { esValido: false, haDepositado: false };
    }
    const cliente = datos.registrations[0];
    return { esValido: true, haDepositado: cliente.First_Deposit > 170 };
};

// Validación del formulario
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
