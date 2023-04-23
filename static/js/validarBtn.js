const btn_continuar = document.querySelector('.cta');

const btn_check = document.querySelector('.substituted')

const main = document.querySelector('.main-afiliado')

btn_check.addEventListener('change',e=>{
    if(e.target.checked){
        btn_continuar.removeAttribute('hidden')
    }
    else{
        btn_continuar.setAttribute('hidden','true')
    }
})


btn_continuar.addEventListener('click',e=>{
    main.removeAttribute('hidden')
})