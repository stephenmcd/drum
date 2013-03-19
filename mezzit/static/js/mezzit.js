$(function() {
    $('.arrows a').click(function() {
        var arrow = $(this);
        var i = arrow.find('i').hasClass('icon-arrow-up') ? 1 : 0;
        var container = arrow.parent().parent();
        var form = container.find('form');
        form.find('input:radio')[i].checked = true;
        $.post(form.attr('action'), form.serialize(), function(data) {
            container.find('.score').text(data.rating_sum);
        }, 'json');
        return false;
    });
});
