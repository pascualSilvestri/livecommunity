const bandera = false;
const idClientes = [];
const input = document.querySelector("#id_nuevo_cliente");
const inputNombre = document.querySelector("#nombre_nuevo_cliente");
// const input_idCliente = document.querySelector('#id_cliente')
const section_A_Validar = document.querySelector(".validacion-2");
const mensaje_verificado = document.querySelector(".mensaje-verificar-cliente");
const mensaje_no_verificado = document.querySelector(
  ".error-verificar-cliente"
);
const btn_validar = document.querySelector(".button-verificar-cliente");
const section_de_validacion = document.querySelector(
  ".verificar-nuevo-cliente"
);
const SKILLING_API_KEY =
  "985718aac52fb7bc9ac44335debf474b48a85dc4371f2b8ce01a658a85a84eada2615a8fd5946106d08e9699a2";

// async function obtenerDatos() {
//     try {

//         //http://127.0.0.1:8000/api/verificar/
//         //https://livecommunity.info/api/verificar/
//       const response = await fetch('http://127.0.0.1:8000/api/skilling/verificar/'); // cambiar a localhost para local
//       if (!response.ok) {
//         throw new Error('Error en la respuesta del servidor');
//       }
//       const data = await response.json();
//       console.log(data)
//       data['data'].forEach(element => {
//         idClientes.push(element);
//       });
//     } catch (error) {
//       console.error(error);
//     }
//   }

async function obtenerDatos() {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/skilling/proxy/${input.value}/`
    ); // cambiar a localhost para local
    if (!response.ok) {
      throw new Error("Error en la respuesta del servidor");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    return error;
  }
}

const verificarNuevoCliente = async () => {
  const data = await obtenerDatos();
  const cliente = data.registrations[0];

  if (cliente.Status == "VERIFIED") {
    return true;
  }
  return false;
};

if (btn_validar != null) {
  //le asocio un evento tipo blur validar cuando desenfoca
  btn_validar.addEventListener("click", async (e) => {
    if (await verificarNuevoCliente()) {
      //si cumple con los requerimientos se habilitas las siguientes secciones
      section_A_Validar.style.display = "block";
      section_de_validacion.style.display = "none";
      //Muestra mensaje de verificacion valida 3 egundos
    } else {
      //si no cumple no se muestran las siguientes secciones
      section_A_Validar.style.display = "none";
      mensaje_verificado.style.display = "none";
      mensaje_no_verificado.style.display = "block";
      // input_idCliente.value = ''
    }
  });
}
