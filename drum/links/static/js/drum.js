
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
                container.find('.score').text(data.rating_sum);
            }
        }, 'json');

        return false;
    });
};

$(setRatingClick);
