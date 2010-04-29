function render_edit_form(comment_id, form_name) {
    var cholder = jq("#"+comment_id).parent();
    var cform = jq("form[name="+form_name+"]",cholder);
    var url = jq(cform).attr("action");
    var cspan = jq("#span-forms-holder-"+comment_id);
    cspan.empty().hide();
    jq(cform).bind("submit", function(event){
        event.preventDefault();
    });
    jq("input", cform).attr("disabled", "disabled");
    jq.get(url,
    function(data){
        ddt = jq("form[name=edit_form]", data)[0];
        cspan.append(ddt).fadeIn();
        jq("input[name=form.button.Cancel]",cspan).attr("onclick", "javascript:remove_edit_form("+comment_id+",'"+form_name+"')");
    });
}

function remove_edit_form(comment_id, form_name) {
    var cholder = jq("#"+comment_id).parent();
    var cform = jq(cholder).find("form[name="+form_name+"]");
    var cspan = jq("#span-forms-holder-"+comment_id);
    jq("form",cspan).bind("submit", function(event){
        event.preventDefault();
    });
    jq("input", cholder).attr("disabled", '');
    cspan.fadeOut();
}
