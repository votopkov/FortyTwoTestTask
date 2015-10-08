function logout() {
    user_id = $('#logout').attr('user_id');
    $.ajax({
        type: 'GET',
        url: '/logout/',
        data: {
            user_id: user_id
        },
        beforeSend: function(){
            $('.indicator').css('display', 'block');
        },
        error: function(xhr, textStatus) {
            alert([xhr.status, textStatus]);
            $('.indicator').css('display', 'none');
        },
        success: function(msg) {
            $('.indicator').css('display', 'none');
            $('.main-div').html('You have already logout <a href="/"> Go to main</a>');
            $('#logout').replaceWith("<a  href='{% url 'task:login' %}'>Login</a>");
            $('.result, .hr, #requests').replaceWith(" ");

        }
    });
}

$(document).ready(function() {

    $(".datepicker").datepicker({
        dateFormat: "yy-mm-dd",
        showButtonPanel: true,
        changeYear: true,
        yearRange: "1950:2010"
    });

    // get 10 requests
    $('body').attr('new_request', 0);
    load_requests = function () {
        if ($('body').attr('new_request') == '0' || $('body').attr('new_request') == undefined) {
            var new_request = 0;
        } else {
            var new_request = $('body').attr('new_request')
        }
        var last_request = $('a[last_request]').attr('last_request');
        $.ajax({
            type: 'GET',
            url: '/request_list_ajax/',
            context: {last_request: last_request, new_request: new_request},
            success: function (msg) {
                var result = "";
                var i = 0;
                $.each(msg, function (key) {
                    if (msg[key]['pk']) {
                        if (i==0) {
                            if (msg[key]['pk'] != last_request && last_request != undefined){
                                new_request = parseInt(new_request) + parseInt(msg[key]['pk']) - parseInt(last_request);
                                if (new_request > 1){
                                    document.title = new_request + " new requests";
                                } else {
                                    document.title = new_request + " new request";
                                }
                                $('body').attr('new_request', new_request)
                            }
                            result += '<tr><td><a last_request=' + msg[key]['pk'] + ' href=\'/request_detail/' + msg[key]['pk'] + '/\'>' + msg[key]['pk'] + '</a></td>';
                        } else {
                            result += '<tr><td><a href=\'/request_detail/' + msg[key]['pk'] + '/\'>' + msg[key]['pk'] + '</a></td>';
                        }

                    }i++;
                    $.each(msg[key]['fields'], function (k, val) {
                        if (k !== 'request' && k !== 'title' && k !== 'pub_date') {
                            result += '<td>' + val + '</td>';
                        } else if (k == 'pub_date') {
                            result += '<td>' + val.slice(0, 19).replace("T"," ") + '</td>';
                        }

                    });
                    $('.result').replaceWith('<div class="col-xs-12 result"><table class="table table-bordered text-center"><tr><th>ID</th><th>Date</th><th>Path</th></tr><tr>' + result + '</tr></table></div>');
                });
                setTimeout(load_requests, 3000);
            }
        });
    };
    load_requests();
    $(document).hover(function (){
        document.title = "Request list";
        $('body').attr('new_request', 0)
    });

// login
    $('#login_form').submit(function(e) {
        e.preventDefault();
        username = $('#id_username').val();
        password = $('#id_password').val();
        csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: 'POST',
            url: '/login/',
            data: {
                username: username,
                password: password,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            },
            beforeSend: function(){
                $('.indicator').css('display', 'block');
                $(this).prop('disabled', true)
            },
            error: function(xhr, textStatus) {
                alert([xhr.status, textStatus]);
                $('.indicator').css('display', 'none');
            },
            success: function(msg) {
                $('.indicator').css('display', 'none');
                if (msg.is_ok){
                    $('.login-tip').remove();
                    $('.login-form-title').before("<div class='text-success login-tip'>" +
                        "Your are log in!" +
                        "<div><a href='/'>refresh page</a></div></div>").remove();
                    $('#login_form, .prompt').remove();

                }else {
                    $('.login-tip').remove();
                    $('.login-error').remove();
                    $('.login-form-title').prepend("<div class='text-danger login-tip'>" +
                        "Please enter a correct username and password.</div>")
                }}
        });
    });

// update profile
    var update_profile_form = $('#update-profile-form');
    $.validator.addMethod(
        "validateDate",
        function(value) {
            // put your own logic here, this is just a (crappy) example
            return value.match(/^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$/);
        },
        "Please enter a date in the format yyyy-dd-mm"
    );

    update_profile_form.validate({
        rules: {
            name: {
                required: true,
                minlength: 3
            },
            date_of_birth: {
                validateDate: true
            },
            last_name: {
                required: true,
                minlength: 3
            },
            email: {
                email: true
            },
            jabber: {
                email: true
            }
        },
        messages: {
            name: {
                required: "* Please enter your name",
                minlength: "* Name can not be less than 3 symbols"
            },
            last_name: {
                required: "* Please enter last_name",
                minlength: "* Last Name can not be less than 3 symbols"
            },
            email: {
                email: "* Please enter a valid email address",
                required: "* Email field is required"
            },
            jabber: {
                email: "* Please enter a valid jabber address",
                required: "* Jabber field is required"
            }
        }, submitHandler: function () {
            var options = {
                data: $(this).serialize(),
                beforeSend: function () {
                    $('.prof_updated').remove();
                    $('.indicator').css('display', 'block');
                    $(this).prop('disabled', true)
                },
                error: function (xhr, textStatus) {
                    alert([xhr.status, textStatus]);
                    $('.indicator').css('display', 'none');
                },
                success: function (msg) {
                    $('.indicator').css('display', 'none');
                    $('input[value=Save]').before(msg.msg);
                    $('div.div_image_preview > img').attr("src", msg.image_src);

                }

            };
            update_profile_form.ajaxSubmit(options);
            return false
        }
    });
});
