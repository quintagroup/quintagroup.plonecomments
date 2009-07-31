function render_abuse_report_form(comment_id) {
    jq('form.report_abuse').bind("submit", function(event){
        event.preventDefault();
    });
    var render_button = 'input#input-render-abuse-cancel-' + comment_id;
    jq(render_button).attr('disabled', 'disabled');
    var form = 'span#span-reply-form-' + comment_id;
    jq(form).slideToggle(500);
    var holder = 'span#span-reply-form-holder-' + comment_id;
    var cancel_button = holder + ' input#input-report-abuse-cancel';
    var qq = jq(cancel_button);
    jq(cancel_button).attr('comment_id', comment_id);
}

function remove_abuse_report_form(comment_id, html) {
    jq('form.report_abuse').bind("submit", function(event){
        event.preventDefault();
    });
    var form = 'span#span-reply-form-' + comment_id;
    jq(form).fadeOut();
    var render_button = 'input#input-render-abuse-cancel-' + comment_id;
    jq(render_button).attr('disabled', '');
    if (html != undefined) {
        var holder = 'span#span-abuse-count-holder-' + comment_id;
        jq(holder).append(html);
    }
}

kukit.actionsGlobalRegistry.register("remove_abuse_report_form", function(oper) {
    var comment_id = oper.parms.comment_id;
    var html = oper.parms.html
    remove_abuse_report_form(comment_id, html);
});
kukit.commandsGlobalRegistry.registerFromAction('remove_abuse_report_form', kukit.cr.makeSelectorCommand);
