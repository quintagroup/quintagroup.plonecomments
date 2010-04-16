$(document).ready(function() {
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
            filter: '#content>*',
            formselector: 'form[name="edit_form"]',
            noform: function(el) {return noformerrorshow(el, 'redirect');},
            redirect: function () {return location.href;},
            closeselector: '[name=form.button.Cancel]'
        }
    );
});