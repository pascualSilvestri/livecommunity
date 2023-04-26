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


const verificarNuevoCliente = (input,array)=>{
    for(const element of array){
        if(input.value==element){
            return true
        }
    }
}

if(input != null){
    input.addEventListener('blur', e => {
        const redex = /^[0-9]{10,}$/
        if(!verificarNuevoCliente(input,idClientes)&&redex.test(input.value)){
            section_A_Validar.style.display = 'block'
        }else{
            section_A_Validar.style.display = 'none'
        }
        

    })
    
}


