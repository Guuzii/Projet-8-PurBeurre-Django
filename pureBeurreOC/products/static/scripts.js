// set mastHead margin-top depending on mainNav height
$(document).ready(() => {
    var navHeight = $("#mainNav").css("height");
    $(".head").css("margin-top", navHeight);
});