$(document).ready(function () {


    $('#clear_button').click(function () {

        $('#category, #city, #district').dropdown('clear');
        $('#district').addClass('disabled');
        $('#min_price, #min_walls, #max_walls, #max_price, #min_square, #max_square, #min_floor, #max_floor').val('');

    });

    $('.special.cards .image').dimmer({
        on: 'hover'
    });

    $('.currency-filter').click(function () {
        $('.currency-filter').dropdown('set value', $(this).dropdown('get value')).dropdown('set text', $(this).dropdown('get text'));
    });

    $('#profile_button').popup({
        preserve: true,
        on: 'click',
        closable: true,
        position: 'bottom center',
        delay: {
            show: 300,
            hide: 300
        }
    });

    $('#sign_in_modal').modal();

    $('#post_modal').modal();

    $('#delete_post_modal').modal();

    $('#history_modal').modal();

    $('#settings_modal').modal(
        {
            onHidden: function () {
                $('#profile_first_name').attr('readonly', true);
                $('#profile_last_name').attr('readonly', true);
                $('#profile_username').attr('readonly', true);
                $('#profile_email').attr('readonly', true);
                $('.edit-buttons').addClass('hidden');
                $('.buttons-wrapper-form').removeClass('hidden');
            }
        }
    );

    $('#sign_in').click(function () {
        $('#sign_in_modal').modal('show');
        $('#profile_button').popup('hide');
    });

    $('#settings_button').click(function () {
        $('#settings_modal').modal('show');
        $('#profile_button').popup('hide');
    });

    $('#history_button').click(function () {
        $('#history_modal').modal('show');
        $('#profile_button').popup('hide');
    });


    $('#change_profile').click(function () {
        $('#profile_first_name').attr('readonly', false);
        $('#profile_last_name').attr('readonly', false);
        $('#profile_phone').attr('readonly', false);
        $('#profile_email').attr('readonly', false);
        $('.buttons-wrapper-form').addClass('hidden');
        $('.edit-buttons').removeClass('hidden');
    });


    // todo сделать отмену как на фасторане в будущем
    $('#cancel_change_profile').click(function () {
        $('.edit-buttons').addClass('hidden');
        $('.buttons-wrapper-form').removeClass('hidden');
        $('#profile_first_name').attr('readonly', true);
        $('#profile_last_name').attr('readonly', true);
        $('#profile_phone').attr('readonly', true);
        $('#profile_email').attr('readonly', true);
    });

    $('#phone_number').mask('+38-(000)-000-00-00');
    $('#profile_phone').mask('+38-(000)-000-00-00');

    $('#sign_in_form').form({
        fields: {
            email: {
                identifier: 'email',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите E-mail адрес'
                    }
                ]
            },
            password: {
                identifier: 'password',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите пароль'
                    },
                    {
                        type: 'minLength[6]',
                        prompt: 'Длина пароля должна быть больше {ruleValue} символов'
                    }
                ]
            }
        }
    });


    $('#sign_up_form').form({
        fields: {
            first_name: {
                identifier: 'first_name',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите имя'
                    }
                ]
            },
            second_name: {
                identifier: 'second_name',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите фамилию'
                    }
                ]
            },
            username: {
                identifier: 'username',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите логин'
                    }
                ]
            },
            email: {
                identifier: 'email',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите E-mail'
                    }
                ]
            },
            password1: {
                identifier: 'password1',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите пароль'
                    },
                    {
                        type: 'minLength[6]',
                        prompt: 'Длина пароля должна быть больше {ruleValue} символов'
                    }
                ]
            },
            password2: {
                identifier: 'password2',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите пароль'
                    },
                    {
                        type: 'match[password1]',
                        prompt: 'Пароли не совпадают'
                    }
                ]
            },
            phone: {
                identifier: 'phone',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите номер телефона'
                    }
                ]
            },
            user_type: {
                identifier: 'user_type',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Укажите тип пользователя'
                    }
                ]
            }
        }
    });


    $('#add_post_form').form({
        fields: {
            title: {
                identifier: 'title',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите заголовок'
                    }
                ]
            },
            post_type: {
                identifier: 'post_type',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Выберите рубрику'
                    }
                ]
            },
            description: {
                identifier: 'description',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите описание'
                    }
                ]
            },
            price: {
                identifier: 'estate_price',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Укажите цену'
                    }
                ]
            },
            rooms: {
                identifier: 'rooms_count',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Укажите количество комнат'
                    }
                ]
            },
            square: {
                identifier: 'square',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Укажите площадь'
                    }
                ]
            },
            estate_city: {
                identifier: 'estate_city',
                rules: [{
                    type: 'empty',
                    prompt: 'Выберите город'
                }]
            },
            estate_district: {
                identifier: 'estate_district',
                rules: [{
                    type: 'empty',
                    prompt: 'Выберите район'
                }]
            }
        }
    });

    $('#estate_currency').dropdown('set selected', '0');
    $('#post_type').dropdown();


    $('#add_post').click(function () {
        $('#post_modal').modal('show');
    });

    $('#hidden-new-file1').on('change', function () {
        $('#test1').attr('src', $('#hidden-new-file1').val());
    });

    function noty(text) {
        var body = $('body');
        body.append('<div class="ui negative message noty">\n' +
            '    <div class="header">\n' + text + '\n' +
            '    </div>\n' +
            '</div>');

        var noty = $('.noty');
        noty.animate({'opacity': '1'}, 500);

        setTimeout(function () {
            noty.fadeOut(500);
        }, 2500);

        setTimeout(function () {
            noty.remove();
        }, 3500);

    }

    $('#sign_up').click(function () {
        noty('Войдите или зарегистрируйтесь');
    });

    $('#waterfall').NewWaterfall();


    $('#gallery').unitegallery({
        theme_enable_text_panel: false,
        slider_scale_mode: "down"
    });


    $('#get_number').popup({
        on: 'click'
    });


    $('#syo').syotimer({
        lang: 'rus',
        year: 2017,
        month: 10,
        day: 7,
        hour: 15,
        minute: 0
    });

    $('#global-page .menu .item').tab({
        context: $('#global-page')
    });


    $('#account-wtrfl').NewWaterfall();
    $('#closed-wtrfl').NewWaterfall();
    $('#post-wtrfl').NewWaterfall();

    $('#delete_form').form({
        fields: {
            reason: {
                identifier: 'reason',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Выберите причину удаления'
                    }
                ]
            },
            comment: {
                identifier: 'commentary',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Напишите комментарий'
                    }
                ]
            }
        }
    });

    $('#close_post').click(function () {
        $('#delete_post_modal').modal('show');
    });

    $('#city').dropdown({
        onChange: function (value) {

            $('#district').dropdown('set selected', -1);
            $('#district-list div').not(':first').remove();

            if (value !== '' && value !== '-1') {
                $.ajax({
                    url: '/api/districts/',
                    type: 'GET',
                    data: {
                        city_id: value
                    },
                    dataType: 'json',

                    success: function (result) {
                        $('#district').removeClass('disabled');
                        for (var i = 0; i < result.length; i++) {
                            $('#district-list').append('<div class="item" data-value=" ' + result[i].id + ' ">' + result[i].name + '</div>');
                        }
                    }
                });
            }
            if (value === '-1') {
                $('#district').addClass('disabled');
            }
        }
    }).dropdown('set selected', -1);

    $('#estate_city').dropdown({

        onChange: function (value) {

            // $('#estate_district').dropdown('set selected', -1);
            $('#estate_district option').remove();

            if (value !== '' && value !== '-1') {
                $.ajax({
                    url: '/api/districts/',
                    type: 'GET',
                    data: {
                        city_id: value
                    },
                    dataType: 'json',

                    success: function (result) {
                        $('#estate_district').removeClass('disabled');
                        for (var i = 0; i < result.length; i++) {
                            $('#estate_district').append($("<option/>", {
                                value: result[i].id,
                                text: result[i].name
                            }));
                        }
                    }
                });
            }
            if (value === '-1') {
                $('#estate_district').addClass('disabled');
            }
        }
    });

    $('#district').dropdown('set selected', -1);
    $('#post_type').dropdown('set selected', -1);
    $('#estate_district').dropdown();
    $('#category').dropdown('set selected', -1);
    $('.currency-filter').dropdown('set selected', '0');

    if (window.innerWidth >= 992) {
        $('#sticky').stick_in_parent();
    }
    $('#close_post_add_modal').click(function () {
        $('#post_modal').modal('hide');
    });

    $('#dashboard-add-post').click(function () {
        window.open('http://127.0.0.1:8000/admin/Main/post/add/');
    });

    $('#search_button').click(function () {
        $.ajax({
            url: '/api/search',
            type: 'POST',
            data: {
                category: $('#category').dropdown('get value'),
                city: $('#city').dropdown('get value'),
                district: $('#district').dropdown('get value'),
                min_square: $('#min_square').val(),
                max_square: $('#max_square').val(),
                min_walls: $('#min_walls').val(),
                max_walls: $('#max_walls').val(),
                min_floor: $('#min_floor').val(),
                max_floor: $('#max_floor').val(),
                min_price: $('#min_price').val(),
                max_price: $('#max_price').val(),
                currency: $($('.currency-filter')[0]).dropdown('get value')
            },
            dataType: 'json',

            success: function (result) {
               console.log(result);
            }
        });
    });

});
