
var contents = function(html, tag) {
    if (html.indexOf('<' + tag + '>') >= 0) {
        return html.split('<' + tag + '>')[1].split('</' + tag + '>')[0];
    }
    return '';
};

var setRatingClick = function() {
    // Drum hides the radio buttons for +1 -1 ratings, and uses
    // up/down arrow anchors. Attach click handlers to the arrow
    // anchors that when clicked, check the relevant hidden radio
    // button, and submits the form via AJAX. If the user is not
    // authenticated, the JSON response will include a ``location``
    // value to redirect to, otherwise it will contain the new
    // rating score, which we update the page with.
    $('.arrows a').click(function() {

        var arrow = $(this);
        var index = arrow.find('i').hasClass('icon-arrow-up') ? 1 : 0;
        var container = arrow.parent().parent();
        var form = container.find('form');

        form.find('input:radio')[index].checked = true;

        $.post(form.attr('action'), form.serialize(), function(data) {
            if (data.location) {
                location = data.location;
            } else {
                //container.find('.score').text(data.rating_sum);
                $('.main').fadeTo(0, .5);
                $.get(location.href, {pjax: 1}, function(html) {
                    $('.main').fadeTo(0, 1);
                    var body = contents(html, 'body');
                    document.getElementsByTagName('body')[0].innerHTML = body;
                    setRatingClick();
                });
            }
        }, 'json');

        return false;
    });
};

$(setRatingClick);
