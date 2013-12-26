// Based on jquery-pjax by Chris Wanstrath
// https://github.com/defunkt/jquery-pjax/blob/master/LICENSE


if (window.history && window.history.pushState && !navigator.userAgent.match(/(iPod|iPhone|iPad|WebApps\/.+CFNetwork)/)) {

    $(function() {

        var active = false;
        var initial = true;

        var contents = function(html, tag) {
            if (html.indexOf('<' + tag + '>') >= 0) {
                return html.split('<' + tag + '>')[1].split('</' + tag + '>')[0];
            }
            return '';
        };

        var pjax = function(url, push) {
            $('.main').fadeTo(0, .5);
            $.get(url, {pjax: 1}, function(html) {
                $('.main').fadeTo(0, 1);
                var title = contents(html, 'title');
                var body = contents(html, 'body');
                if (push) {
                    if (!active) {
                        active = true;
                        window.history.replaceState({}, document.title);
                    }
                    window.history.pushState({url: url}, document.title, url);
                }
                document.title = title;
                document.getElementsByTagName('body')[0].innerHTML = body;
                setRatingClick()

$(function() {
    $('.reply').click(function() {
        $('.reply-form').hide();
        $(this).next('.reply-form').toggle();
    });
});

    $('.middle input:text, .middle input:password, textarea').addClass('input-xlarge');
    $('.control-group label').addClass('control-label');
                scrollTo(0, 0);
                if (window._gaq) {
                  _gaq.push(['_trackPageview']);
                }
            });
        };

        $('a').live('click', function(event) {
            var host = location.protocol + '//' + location.hostname
            if (this.href.substr('#') >= 0) {
                return false;
            } else if (this.href.indexOf(host) != 0 || event.which > 1 || event.metaKey || $(this).hasClass('no-pjax')) {
                return true;
            }
            pjax(this.href, true);
            return false;
        })

        $(window).bind('popstate', function(event) {
            if (initial) {
                initial = false;
                return;
            }
            if (event.state) {
                pjax(event.state.url || location.href);
            // } else {
            //     location = location.href;
            }
        });

        $.event.props.push('state');

    });
}
