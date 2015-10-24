

$(document).ready(function() {

    $('#create_task_form').validate({
        rules: {
            title: {
                required: true,
                minlength: 3
            },
            description: {
                required: true,
                minlength: 3
            },
            messages: {
                title: {
                    required: "* Please enter task name",
                    minlength: "* Title can not be less than 3 symbols"
                },
                description: {
                    required: "* Please enter task description",
                    minlength: "* Description can not be less than 3 symbols"
                }
            }
        }
    });

});


function edit_form(current_element) {
    // get csrftoken
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    // get information about task
    var id = $(current_element).attr('id');
    var task_title_text = $(current_element).parents('.task_item').children('.title-parent').children('.task-title-name').text();
    var task_item_html = $(current_element).parents('.task_item').html();
    var task_description_text = $(current_element).parents('.task_item').children('.description-parent').children('.task-description').text();

    var task_status_text = $(current_element).parents('.task_item').children('.status-parent').children('.task-status').text();
    var task_status = $(current_element).parents('.task_item').children('.status-parent').children('.task-status').attr('status');

    // replace button on submit
    task_item_html = task_item_html.replace('<button onclick="edit_form(this)" id="'
        + id + '" class="btn btn-default task_edit_button">' +
        'Edit task</button>', '<button id="' + id  + '" onclick=form_validate(this.id) class="btn btn-default task_edit_button"' +
        '>Edit</button>');

    var form = "<form class='edit_form ui-state-default' id='" + id + "' method='POST' action=/edit_task/></form>";

    // get task title html
    var div_task_title_html = '<div class="task-title">Title: </div>' +
        '<div class="task-title-name">' + task_title_text + '</div>';
    var title_input = '<label>Title</label><input class="form-control title-input" id="id_title" type="text" name="title" ' +
        'value="' + task_title_text + '">';
    task_item_html = task_item_html.replace(div_task_title_html, title_input);

    // get task description
    var task_description_html = '<div class="task-description-title">Description</div><div ' +
        'class="task-description">' + task_description_text + '</div>';
    var description_textarea = '<label>Description</label><textarea id="id_description"' +
        'name="description" class="form-control" cols=30, rows=10>' + task_description_text + '</textarea>';
    task_item_html = task_item_html.replace(task_description_html, description_textarea);
    // get task status
    var task_status_html = '<div class="task-title">Status: </div><div class="task-status" status="' + task_status + '"' +
        '>' + task_status_text + '</div>';
    var status_select;
    if (task_status == 1) {
        status_select = '<label>Status</label><select class="form-control" id="id_status" name="status">' +
            '<option value="1"">Выполнено</option><option value="2">Не выполнено</option></select>'
    } else {
        status_select = '<label>Status</label><select class="form-control" id="id_status" name="status">' +
            '<option value="2"">Не выполнено</option><option value="1">Выполнено</option></select>'
    }

    task_item_html = task_item_html.replace(task_status_html, status_select);

    $(current_element).parents('.task_item').replaceWith(form);
    form_id = "#" + id;
    $(form_id).append("<input type='hidden' name='csrfmiddlewaretoken' value='" + csrftoken + "'>" +
        "<input type='hidden' name='id' value='" + id + "'>" + task_item_html);
}

function form_validate(identify) {
    var id_form = "#" + identify;
    $(id_form).validate({
        rules: {
            title: {
                required: true,
                minlength: 3
            },
            description: {
                required: true,
                minlength: 3
            },
            messages: {
                title: {
                    required: "* Please enter task name",
                    minlength: "* Title can not be less than 3 symbols"
                },
                description: {
                    required: "* Please enter task description",
                    minlength: "* Description can not be less than 3 symbols"
                }
            }
        }, submitHandler: function () {
            var options = {
                beforeSend: function () {
                    $('.indicator').css('display', 'block');
                }
            };
            $(id_form).ajaxSubmit(options)
        }
    });
}