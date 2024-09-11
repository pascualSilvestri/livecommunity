const bandera = false;
const idClientes = [];
const input = document.querySelector('#id_nuevo_cliente');
const section_A_Validar = document.querySelector('.validacion-2');
const mensaje_verificado = document.querySelector('.mensaje-verificar-cliente');
const mensaje_no_verificado = document.querySelector('.error-verificar-cliente');
const mensaje_verificando = document.querySelector('.mensaje-verificando-cliente'); // Nuevo mensaje de estado
const btn_validar = document.querySelector('.button-verificar-cliente');
const section_de_validacion = document.querySelector('.verificar-nuevo-cliente');

// Función para obtener datos del servidor
async function obtenerDatos() {
  try {
    const response = await fetch('https://livecommunity.info/api/verificar/'); // Cambiar a localhost para local
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

// Llamada a la función para obtener los datos
obtenerDatos();

// Verifica si el cliente existe en la base de datos
const verificarNuevoCliente = () => {
  // Verifica si el ID de cliente existe
  const client = idClientes.filter(e => e.client == input.value);
  return client.length > 0;
};

// Escucha el evento 'click' en el botón de validación
if (btn_validar != null) {
  btn_validar.addEventListener('click', async e => {
    e.preventDefault(); // Prevenir el comportamiento por defecto del botón

    // Muestra el mensaje de "Verificando..."
    mensaje_verificando.style.display = 'block';
    mensaje_verificado.style.display = 'none';
    mensaje_no_verificado.style.display = 'none';

    // Espera a que los datos se obtengan correctamente antes de continuar
    await obtenerDatos();

    // Oculta el mensaje de "Verificando..." cuando termina la verificación
    mensaje_verificando.style.display = 'none';

    // Verifica si el cliente existe
    if (verificarNuevoCliente()) {
      // Si el cliente existe, muestra la siguiente sección
      section_A_Validar.style.display = 'block';
      section_de_validacion.style.display = 'none';
      mensaje_verificado.style.display = 'block';
      mensaje_no_verificado.style.display = 'none';
    } else {
      // Si no existe, muestra el mensaje de error
      section_A_Validar.style.display = 'none';
      mensaje_verificado.style.display = 'none';
      mensaje_no_verificado.style.display = 'block';
    }

    // Bandera en falso después de la validación
    const bandera = false;
  });
}
