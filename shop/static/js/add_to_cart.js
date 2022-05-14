const URL_POST = '/api/v1/add-to-cart/'
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

const addToCart = (id)=>{
    $.ajax({
        type:'POST',
        url:URL_POST,
        data:{
            product_id:Number(id),
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        success:({ text, type })=>{
            $('#alerts').html(`<div class ='alert alert-${type}'>${text}</div>`);
            window.scrollTo(0,0);
        },
        error:data=>{console.log(data)}
    })
}