$(function() {
    //Função para Mostrar as mensagem padrões
    setTimeout(function() {
        $(".message_flash").hide('blind', {}, 1000)
    }, 3000);
});

function myFunction(id_div) {
    document.getElementById(id_div).classList.toggle("show");
}
