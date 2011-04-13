var common_content_filter = '#content>*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';
$(document).ready(function() {
    function redirectbasehref(el, responseText) {
        var mo = responseText.match(/<base href="(.+?)"/i);
        if (mo.length === 2) {
            return mo[1];
        }
        return location;
    }
    function noformerrorshow(el, noform) {
        var o = $(el);
        var emsg = o.find('dl.portalMessage.error');
        if (emsg.length) {
            o.children().replaceWith(emsg);
            return false;
        } else {
            return noform;
        }
    };
    $('div.comment form[name=edit], div.comment form[name=reply], div.comment form[name=report_abuse]').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter,//'#content>*',
            formselector: 'form[name="edit_form"]',
            noform: function(el) {return noformerrorshow(el, 'redirect');},
            redirect: redirectbasehref,
            closeselector: '[name=form.button.Cancel]'
        }
    );
});
