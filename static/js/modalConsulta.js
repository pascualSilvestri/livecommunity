
const modalmask = document.querySelector('.modalmask');
const btn_consulta = document.querySelectorAll('.btn-consultar-container');
const close = document.querySelector('.close');
const btn_consulta_submit = document.querySelector('#btn_consulta_submit');
let id_user = ''
let ubicacion = ''

btn_consulta.forEach(btn => {
    btn.addEventListener('click', () => {
        ubicacion = btn.getAttribute('data-ubicacion');
        id_user = btn.getAttribute('data-id');
        modalmask.style.display = 'block';
    });

});

close.addEventListener('click', () => {
    modalmask.style.display = 'none';
}
);


btn_consulta_submit.addEventListener('click', async (e) => {
    e.preventDefault();
    const enviarInfor = await fetch('consulta/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre: document.querySelector('#firstname').value,
            email: document.querySelector('#email').value,
            telefono: document.querySelector('#telefono').value,
            consulta: document.querySelector('#consulta').value,
            ubicacion: ubicacion,
            id_user: id_user != ''  ? id_user : 'LM500S'
        })
    });
    
    const respuesta = await enviarInfor.json();
    if (respuesta.status === 200) {
        modalmask.style.display = 'none';
    } else {
        alert('Error al enviar la consulta');
    }

});