// set mastHead margin-top depending on mainNav height
$(document).ready(() => {
    var navHeight = $("#mainNav").css("height");
    $(".head").css("margin-top", navHeight);
});

// visual effect on product card hover
$(".product-card .hover-div ").mouseenter((e) => {
    $(e.target).parent().animate({
        margin: "12px"
    }, 100);
});

$(".product-card .hover-div").mouseleave((e) => {
    $(e.target).parent().animate({
        margin: "15px"
    }, 100);
});

$(".product-card .hover-div").click((e) => {
    window.location.assign('/products/details/' + $(e.target).attr("data"));
});