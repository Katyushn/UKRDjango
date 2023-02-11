$(document).ready(function() {
    // menu
    function menu_selected_hide(){
        $('.field-category').css('display', 'none');
        $('.field-post').css('display', 'none');
        $('.field-product').css('display', 'none');
        $('.field-template').css('display', 'none');
        $('.field-link').css('display', 'none');
        if ($('#id_type').val() == 'category') {
            $('.field-category').css('display', 'block');
        }
        if ($('#id_type').val() == 'article') {
            $('.field-post').css('display', 'block');
        }
        if ($('#id_type').val() == 'product') {
            $('.field-product').css('display', 'block');
        }
        if ($('#id_type').val() == 'template') {
            $('.field-template').css('display', 'block');
        }
        if ($('#id_type').val() == 'link') {
            $('.field-link').css('display', 'block');
        }
    }
    menu_selected_hide();

    $('#id_type').change(function () {
        menu_selected_hide();
    });


});
