! function($, window, document, _undefined) {
    "use strict";

    XF.PlayNow = XF.Element.newHandler({
        options: {},

        init: function() {
            var $hostnameCopy = $('.p-header-playNow-hostname-copy');
            var $hostnameTooltip = $('.p-header-playNow-hostname-tooltip');

            var client = new ClipboardJS('.p-header-playNow-hostname-copy');
            var copied = false;
            var defaultTooltip = $hostnameTooltip.html();

            client.on('success', function(event) {
                if (copied) return;

                copied = true;

                $hostnameTooltip.html('Copied to Clipboard!');

                setTimeout(function() {
                    copied = false;
                    $hostnameTooltip.html(defaultTooltip);
                }, 3000);
            });

            $hostnameCopy
                .on('mouseenter', function() {
                    $hostnameTooltip.addClass('display')
                })
                .on('mouseleave', function() {
                    $hostnameTooltip.removeClass('display')
                });
        }
    });

    XF.Element.register('play-now', 'XF.PlayNow');
}
(jQuery, window, document);