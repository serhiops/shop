const URL_ROOM = '/chat/api/v1/rooms/';
const URL_TO_CHATROOM = '/chat/user_chats/'

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


const addRoom = (id)=>{
    $.ajax({
        type:'POST', 
        url:URL_ROOM,
        data:{
            product:Number(id),
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        success:()=>{window.location.pathname = URL_TO_CHATROOM;},
        error:(er)=>console.log(er)
    })
}
