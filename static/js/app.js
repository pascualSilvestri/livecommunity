function send_handle(){

  let nombre =document.getElementById("id_nombre").value;

  let apellido= document.getElementById("id_apellido").value;

  let userTelegram= document.getElementById("id_userTelegram").value;

  let email= document.getElementById("id_correo").value;

  let telefono= document.getElementById("id_telefono").value;

  let idAfiliado= document.getElementById("id_idAfiliado").value


  var win = window.open(`https://wa.me/541138658887?text=Mi%20nombre%20es%20${nombre}%20${apellido}%0AMi%20usuario%20de%20Telegram%20es%20${userTelegram}%0AMi%20email%20es%20${email}%0AMi%20telefono%20es%20${telefono}%0AMi%20IdAfiliado%20es%20${idAfiliado}%0A%0A%0A%20**POR FAVOR ADJUNTAR FOTO DE COMPROBANTE DE FONDEO DE LIBERTEX**`, '_blank');
  win.focus();
}