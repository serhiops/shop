const URL_PATCH = '/api/v1/product-sending/'

getCookie = name => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const acceptOrder = (id) => {
    $.ajax({
        type: 'PATCH',
        url: URL_PATCH + id + '/',
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        data: {
            id: Number(id),
            is_take: true
        },
        success: data => {
            $(`#product-${id}`).html('');
            $('#alerts').html(`<div class ='alert alert-success'>Вы приняли заказ ${data.product_name}</div>`);
            window.scrollTo(0, 0);

        },
        error: data => { console.log(data) },
    })
}

const sendingOrder = (id) => {
    $.ajax({
        type: 'PATCH',
        url: URL_PATCH + id + '/',
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        data: {
            id: Number(id),
            is_sent: true,
        },
        success: data => {
            $(`#product-${id} #card-footer`).addClass('card-footer bg-transparent border-success').html('<b>Ждем подтверждения посылки получателем</b> ').removeAttr('style');
            $('#alerts').html(`<div class ='alert alert-success'>Заказ отмечен как отправленный!</div>`);
            window.scrollTo(0, 0);
        },
        error: data => { console.log(data) }
    })
}

