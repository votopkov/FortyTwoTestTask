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
            $('.header_link').remove();
            $('.main-div').html('You have already logout !<a href="/"> Go to main</a> or ' +
                '<a href="/login/">Login</a>');
            $('#logout').replaceWith("<a  href='/login/'>Login</a>");
            $('.result, .hr, #requests').replaceWith(" ");

        }
    });
}

$(document).ready(function() {

<<<<<<< HEAD
  /*  $(".datepicker").datepicker({
        dateFormat: "yy-mm-dd",
        showButtonPanel: true,
        changeYear: true,
        yearRange: "1950:2010"
    });


*/

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
                    window.location.href = '/'
                }
                else {
                    $('.login-tip').remove();
                    $('.login-error').remove();
                    $('.login-form-title').prepend("<div class='text-danger login-tip'>" +
                        "Please enter a correct username and password.</div>")
                }}
        });
    });

=======
>>>>>>> ticket_8
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
                    // update message
                    if (msg.status == 'success') {
                        var message = "<div class='col-xs-12" +
                                  " bg-success prof_updated'>" +
                                  "Profile has been updated</div>";
                        $('input[value=Save]').before(message)
                    } else {
                        var message = "<div class='col-xs-12" +
                                  " bg-danger prof_updated'>" +
                                  "Profile is not updated</div>";
                        $('input[value=Save]').before(message)
                    }
                    // image update
                    if ($('div.div_image_preview').attr('img') == 'no-img') {
                        if (msg.image_src !== '') {
                            $('div.div_image_preview').append('<img width="200"' +
                            'src="' + msg.image_src + '"></img>');
                        }
                        $('div.div_image_preview').attr('img', '')
                    } else {
                        $('div.div_image_preview > img').attr("src", msg.image_src);
                    }
                }

            };
            update_profile_form.ajaxSubmit(options);
            return false
        }
    });
});
