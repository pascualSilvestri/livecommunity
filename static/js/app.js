function send_handle(){

  let nombre=document.getElementById("nombre").value;

  let apellido= document.getElementById("apellido").value;

  let userTelegram= document.getElementById("userTelegram").value;

  let email= document.getElementById("email").value;

  let telefono= document.getElementById("telefono").value;

  let comprobante = document.getElementById('comprobante').value

  
  var win = window.open(`https://wa.me/3624297648?text=Mi%20nombre%20es%20${nombre}%20${apellido}%0AMi%20usuario%20de%20Telegram%20es%20${userTelegram}%0AMi%20email%20es%20${email}%0AMi%20telefono%20es%20${telefono}`, '_blank');
  win.focus();
}