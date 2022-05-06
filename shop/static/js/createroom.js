const URL_ROOM = "/chat/api/v1/rooms/";


const getCookie = name => {
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


const addRoom = (path, id)=>{
    let room = path.split("/")[path.split("/").length -2];
    $.ajax({
        type:'POST',
        url:URL_ROOM,
        data:{
            name:room,
            product:Number(id),
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        success:()=>{window.location.pathname = '/chat/' + room + '/';},
        error:(er)=>console.log(er)
    })
}
