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
const ROOM_NAME = location.href.split("/")[location.href.split("/").length - 2]
const URL_POST = "/chat/api/v1/messages/"
const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data.type === 'POST') {
        let messageId = data.message_api.id;
        const msg = `<div id="author-message-${messageId}" style="max-width: 30%;">
                        <div style="margin-bottom: 1px;">
                            <button type="button" class="btn btn-light btn-sm" value ="${messageId}" id="update_${messageId}"onclick="updateMessage(this.value)">Update</button>
                            <button type="button" class="btn btn-light btn-sm" value="${messageId}" onclick="deleteMessage(this.value)">Delete</button>
                        </div>
                        <div id="message-${messageId}" class="active-message-cur-user">
                            ${data.message}
                        </div>
                    </div>`
        if (data.user.id === data.message_api.author) {
            $("#current-message").append(msg);
        } else {
            $("#current-message").append(`<div id="message-${ messageId }" class="active-message-other-user">${ data.message }</div><br><br>`);
        };
    } else if (data.type === 'PATCH'){
        $(`#message-${data.message.id}`).text(`${ data.message.message }`)
    } else if (data.type === 'DELETE'){
        if (data.user.id === data.message.author) {
            $(`#author-message-${data.message.id}`).html(`<div class="del-message-cur-user"><span class="del-message-text">Вы удалили сообщение</span></div>`);
        } else {
            $(`#author-message-${data.message.id}`).html(`<div class="del-message-other-user"><span class="del-message-text">Собеседник удалил сообщение</span></div><br><br>`)
        }
    }
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if(message.length>0){
        chatSocket.send(JSON.stringify({
            'message': message,
            'type': 'POST',
        }));
        messageInputDom.value = '';
    }
}

const deleteMessage = (id) => {
    chatSocket.send(JSON.stringify({
        'type':'DELETE',
        'message_id':Number(id)
    }))
}

const updateMessage = (id) => {
    let oldText = $(`#message-${id}`);
    oldText.removeClass("active-message-cur-user");
    $(`#message-${id}`).html(`<input id="chat-message-input" class="form-control" type="text" placeholder="Введите новое сообщение" value ="${oldText.text().trimStart().trimEnd()}">`);
    let updateButton = $(`#update_${id}`);
    updateButton.attr({ "class": "btn btn-success btn-sm", "onclick": "saveUpdateMessage(this.value)" });
    updateButton.text("Save");
}


const saveUpdateMessage = (id) => {
    let text = $(`#message-${id} input`).val();
    chatSocket.send(JSON.stringify({
        'message': text,
        'message_id': id,
        'type': "PATCH"
    }));
    $(`#message-${id}`).addClass("active-message-cur-user")
    let updateButton = $(`#update_${id}`);
    updateButton.attr({ "class": "btn btn-light btn-sm", "onclick": "updateMessage(this.value)" });
    updateButton.text("Update");
}