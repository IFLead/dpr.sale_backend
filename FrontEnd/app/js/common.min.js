$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function is_auth() {
        return $('#is_autorized').val() === 'true'
    }

    function is_verified() {
        return $('#is_verified').val() === 'true'
    }


    var default_filters = {
        category: -1,
        city: -1,
        district: -1,
        min_square: '',
        max_square: '',
        min_walls: '',
        max_walls: '',
        min_floor: '',
        max_floor: '',
        min_price: '',
        max_price: '',
        currency: 0
    };

    localStorage.setItem('filters', JSON.stringify(default_filters));

    localStorage.setItem('post_ids', JSON.stringify([]));

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

                $('.edit-buttons').addClass('hidden');
                $('.buttons-wrapper-form').removeClass('hidden');

                $('#profile_first_name_view').attr('hidden', false);
                $('#profile_first_name').attr('hidden', true);

                $('#profile_last_name_view').attr('hidden', false);
                $('#profile_last_name').attr('hidden', true);

                $('#profile_phone_view').attr('hidden', false);
                $('#profile_phone').attr('hidden', true);

                $('#profile_email_view').attr('hidden', false);
                $('#profile_email_view_label').css('display', 'block');

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

        $('#profile_first_name_view').attr('hidden', true);
        $('#profile_first_name').attr('hidden', false);

        $('#profile_last_name_view').attr('hidden', true);
        $('#profile_last_name').attr('hidden', false);

        $('#profile_phone_view').attr('hidden', true);
        $('#profile_phone').attr('hidden', false);

        $('#profile_email_view').attr('hidden', true);
        $('#profile_email_view_label').css('display', 'none');

        $('.buttons-wrapper-form').addClass('hidden');

        $('.edit-buttons').removeClass('hidden');
    });


    $('#cancel_change_profile').click(function () {

        $('.edit-buttons').addClass('hidden');
        $('.buttons-wrapper-form').removeClass('hidden');

        $('#profile_first_name_view').attr('hidden', false);
        $('#profile_first_name').attr('hidden', true);

        $('#profile_last_name_view').attr('hidden', false);
        $('#profile_last_name').attr('hidden', true);

        $('#profile_phone_view').attr('hidden', false);
        $('#profile_phone').attr('hidden', true);

        $('#profile_email_view').attr('hidden', false);
        $('#profile_email_view_label').css('display', 'block');
    });


    $('#phone').mask('+38-(000)-000-00-00');
    $('#profile_phone').mask('+38-(000)-000-00-00');
    $('#profile_phone_view').mask('+38-(000)-000-00-00');

    $('#sign_in_form').form({
        fields: {
            email: {
                identifier: 'id_login',
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

    $('#acc-signin').form();
    $('#settings_form').form();
    $('#pswd-rst').form();
    $('#reset-from-key').form();
    $('#pswd-change').form();
    $('#email_form').form();
    $('#allauth_sign_up').form();
    $('#mail_confirm').form();
    $('#email_btn_form').form();
    $('#add_email').form({
        fields: {
            id_email: {
                identifier: 'id_email',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите E-mail'
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
            last_name: {
                identifier: 'last_name',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите фамилию'
                    }
                ]
            },
            username: {
                identifier: 'id_username',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Введите логин'
                    }
                ]
            },
            email: {
                identifier: 'id_email',
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
                        type: 'integer[1..999999999]',
                        prompt: 'Только целые суммы'
                    }
                ]
            },
            rooms: {
                identifier: 'rooms_count',
                rules: [
                    {
                        type: 'integer[0..100]',
                        prompt: 'Укажите корректное количество комнат'
                    }
                ]
            },
            floor: {
                identifier: 'estate_floor',
                rules: [
                    {
                        type: 'integer[0..1000]',
                        prompt: 'Укажите корректное количество этажей'
                    }
                ]
            },
            storeys: {
                identifier: 'estate_storeys',
                rules: [
                    {
                        type: 'integer[0..1000]',
                        prompt: 'Укажите корректное количество этажности здания'
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
            },
            estate_currency_value: {
                identifier: 'estate_currency_value',
                rules: [{
                    type: 'empty',
                    prompt: 'Ошибка выбора валюты'
                }]
            }
        }
    });

    $('#estate_currency').dropdown({
        onChange: function () {
            $('#estate_currency_value').val($(this).dropdown('get value'));
        }
    }).dropdown('set selected', '0');


    $('#post_type').dropdown();


    $('#add_post').click(function () {
        if (is_auth()) {
            if (is_verified()) {
                $('#post_modal').modal('show');
            }
            else {
                noty('Ваш аккаунт ещё не подтвержден');
            }
        }
        else {
            noty('Войдите или зарегистрируйтесь');
        }

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
        location.href = '/sign_up';
    });

    $('#waterfall').NewWaterfall();


    $('#gallery').unitegallery({
        theme_enable_text_panel: false,
        slider_scale_mode: "down"
    });


    $('#get_number').click(function () {
        $(this).popup('show');
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

    if (window.innerWidth <= 370) {
        $('#closed_offers').text('Сделки');
    }

    $('#close_post_add_modal').click(function () {
        $('#post_modal').modal('hide');
    });

    $('#dashboard-add-post').click(function () {
        window.open('/admin/Main/post/add/');
    });

    $('#search_button').click(function () {
        $('#sorry_bro').attr('hidden', true);
        $('#waterfall li').remove();
        $('#waterfall').attr('hidden', true);
        $('#data_loader').addClass('active');

        var filters = {
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
        };

        localStorage.setItem('filters', JSON.stringify(filters));
        localStorage.setItem('post_ids', JSON.stringify([]));

        $.ajax({
            url: '/api/search',
            type: 'POST',
            data: filters,
            dataType: 'json',

            success: function (result) {

                $('#data_loader').removeClass('active');
                if (result.html) {
                    $('#waterfall').attr('hidden', false);
                    $('#waterfall').append(result.html);
                    $('#more_button').removeClass('hidden');
                }
                else {
                    $('#sorry_bro').attr('hidden', false);
                    $('#more_button').addClass('hidden');
                }
            }
        });
    });

    $('#more_button').click(function () {
        $('#sorry_bro').attr('hidden', true);
        $(this).addClass('loading disabled');
        var data = JSON.parse(localStorage.getItem('filters'));
        data['post_ids'] = JSON.parse(localStorage.getItem('post_ids'));
        $.ajax({
            url: '/api/load-more',
            type: 'GET',
            data: data,
            dataType: 'json',

            success: function (result) {
                console.log(result);
                $('#more_button').removeClass('loading disabled');

                if (result.html) {
                    $('#waterfall').append(result.html);
                }
                else {
                    noty('К сожалению, это все найденные объявления');
                }
                localStorage.setItem('post_ids', JSON.stringify(result.posts));
            }
        });

    });

    $('#commentary').bind('input propertychange', function () {
        if (this.value !== '') {
            $('#confirm_post_close').removeClass('disabled');
        }
        else {
            $('#confirm_post_close').addClass('disabled');
        }
    });

    $('#confirm_post_close').click(function () {

        if (confirm('Ваше объявление будет убрано из общего списка показа. Продолжить?')) {
            $.ajax({
                url: '/api/post/close/',
                type: 'POST',
                data: {
                    post_id: $('#main-content').data('post-id'),
                    commentary: $('#commentary').val()
                },
                dataType: 'json',

                success: function (result) {
                    location.href = '/';
                }
            });
        }
    });

    $('#top_post').click(function () {

        $.ajax({
            url: '/api/post/top/',
            type: 'POST',
            data: {
                post_id: $('#main-content').data('post-id')
            },
            dataType: 'json',

            success: function (result) {
                location.reload();
            }
        });
    });

    $('#untop_post').click(function () {

        $.ajax({
            url: '/api/post/untop/',
            type: 'POST',
            data: {
                post_id: $('#main-content').data('post-id')
            },
            dataType: 'json',

            success: function (result) {
                location.reload();
            }
        });
    });


    $('#verify_post').click(function () {

        $.ajax({
            url: '/api/post/verify/',
            type: 'POST',
            data: {
                post_id: $('#main-content').data('post-id')
            },
            dataType: 'json',

            success: function (result) {
                location.reload();
            }
        });
    });


    $('#unverify_post').click(function () {

        $.ajax({
            url: '/api/post/unverify/',
            type: 'POST',
            data: {
                post_id: $('#main-content').data('post-id')
            },
            dataType: 'json',

            success: function (result) {
                location.reload();
            }
        });
    });

    $('.verify_post_button').click(function () {

        $.ajax({
            url: '/api/post/verify/',
            type: 'POST',
            data: {
                post_id: $(this).parent().data('post-id')
            },
            dataType: 'json',

            success: function (result) {
                location.reload();
            }
        });
    });


    $('.delete_post_button').click(function () {

        $.ajax({
            url: '/api/post/delete/',
            type: 'POST',
            data: {
                post_id: $(this).parent().data('post-id')
            },
            dataType: 'json',

            success: function (result) {
                location.reload();
            }
        });
    });

    $('.verify_user_button').click(function () {

        $.ajax({
            url: '/api/user/verify/',
            type: 'POST',
            data: {
                user_id: $(this).parent().data('account-id')
            },
            dataType: 'json',

            success: function (result) {
                location.reload();
            }
        });
    });

    $('.unverify_user_button').click(function () {

        $.ajax({
            url: '/api/user/unverify/',
            type: 'POST',
            data: {
                user_id: $(this).parent().data('account-id')
            },
            dataType: 'json',

            success: function (result) {
                location.reload();
            }
        });
    });

    $('#user_type').dropdown();

    $("input:file").change(function () {
        var fileName = $(this).val().match(/\\([^\\]+)$/)[1];
        $(this).siblings('label').html(fileName);
        $(this).siblings('label').css('background-color', '#b5cc18');
    });

    // function changeImg() {
    //     var section = $('.heading-section');
    //
    //     setTimeout(function () {
    //        section.css('background', 'url(/static/img/svg/fit.svg), url(/static/img/real%20estate/1.jpg)');
    //        section.css('background-repeat', 'no-repeat');
    //        section.css('background-position', 'left, left bottom');
    //     }, 2500);
    // }
    //
    // setTimeout(changeImg(), 2500);

});
