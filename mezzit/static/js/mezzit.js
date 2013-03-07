$(function() {
    $('.arrows a').click(function() {
        var arrow = $(this);
        var i = arrow.find('i').hasClass('icon-arrow-up') ? 1 : 0;
        var form = arrow.parent().parent().find('form');
        form.find('input:radio')[i].checked = true;
        form.submit();
        return false;
    });
});
