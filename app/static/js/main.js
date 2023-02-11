// owl карусель в товарах
$(document).ready(function() {
    dotcount = 1;

    $(".owl-carousel").owlCarousel({
        items: 1,
        margin: 10,
        nav: false,
        autoHeight: true
    });

    $('.owl-dot').each(function() {
        $(this).addClass('dotnumber' + dotcount);
        $(this).attr('data-info', dotcount);
        dotcount = dotcount + 1;
    });

    slidecount = 1;

    $('.owl-item').not('.cloned').each(function() {
        $(this).addClass('slidenumber' + slidecount);
        slidecount = slidecount + 1;
    });

    $('.owl-dot').each(function() {
        grab = $(this).data('info');
        slidegrab = $('.slidenumber' + grab + ' img').attr('src');
        var slide = '<img src="' + slidegrab + '">';
        $(this).append(slide)
    });

    amount = jQuery('.owl-dot').length;
    gotowidth = 100 / amount;

    $('.owl-dot').css("width", gotowidth + "%");
    newwidth = $('.owl-dot').width();
    $('.owl-dot').css("height", newwidth + "px");

});
// конец owl карусель в товарах ----------

// открытие вопрос-ответ
$(document).ready(function() {
    //прикрепляем клик по заголовкам acc-head
    $('.shop-detail-faq-item__title').on('click', open_accordion);
});
function open_accordion(){
//скрываем все кроме того, что должны открыть
    $('.shop-detail-faq-item__text').not($(this).next()).slideUp(500);
// открываем или скрываем блок под заголовоком, по которому кликнули
    $(this).next().slideToggle(1000);
}
