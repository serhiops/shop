import MessageForm from "./MessageForm";
import $, { error } from 'jquery';
import React from "react";
import Messages from "./Messages";

const HOST = window.location.host /* "127.0.0.1:8000" */
const URL_GET_MESSAGES = 'http://127.0.0.1:8000/chat/api/v1/messages/'

class Chats extends React.Component {
    constructor({ user_chats, current_user, }) {
        super();
        this.state = {
            current_messages: [],
            current_user: current_user,
            user_chats: user_chats,
            chatSocket: WebSocket,
            changeMessageFoo: this.updateMessage,
        };
    }
    getMessages = (id) => {
        $.ajax({
            type: 'GET',
            url: URL_GET_MESSAGES,
            data: {
                room: id
            },
            success: ({ room }) => {
                try{
                    this.state.chatSocket.close()
                } catch{}
                $('#messages-area').removeAttr('hidden');
                $('button[class$=active]').removeClass('active');
                $(`#room-${id}`).addClass('active');
                this.setState({
                    current_messages: room.messages,
                    current_room: room.name,
                    chatSocket: new WebSocket('ws://' + HOST + '/ws/chat/' + room.name + '/'),
                });
            },
            error: data => { console.log(data) }
        })
    }
    deleteMessage = (id) => {
        this.state.chatSocket.send(JSON.stringify({
            'type': 'DELETE',
            'message_id': id
        }))
    }
    updateMessage = (id) => {
        const oldText = $(`#message-${id}`);
        oldText.removeClass();
        $(`#message-${id}`).html(`<input class="form-control" id = 'change-msg-form' type="text" value='${oldText.text()}'/>`);
        this.setState({
            changeMessageFoo: this.updateMessageSave
        });
        $(`#update-${id}`).text('Save').removeClass().addClass('btn btn-success btn-sm');
    }
    updateMessageSave = (id) => {
        const message = $('#change-msg-form').val();
        this.state.chatSocket.send(JSON.stringify({
            'type': 'PATCH',
            'message': message,
            'message_id': id,
        }));
    }
    componentDidUpdate() {
        this.state.chatSocket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            switch (data.type) {
                case 'POST':
                    this.setState({
                        current_messages: [...this.state.current_messages, data.message_api]
                    })
                    break;
                case 'DELETE':
                    this.state.current_messages.forEach((mes) => {
                        if (mes.id === data.message.id) {
                            mes.is_active = false
                        }
                    })
                    this.setState({
                        current_messages: this.state.current_messages
                    })
                    break;
                case 'PATCH':
                    if (data.message.author === this.state.current_user.id) {
                        $(`#message-${data.message.id}`).addClass('active-message-cur-user').html("");
                        $(`#update-${data.message.id}`).text('Update').removeClass().addClass('btn btn-light btn-sm');
                    }
                    this.state.current_messages.forEach(message => {
                        if (message.id === data.message.id) {
                            message.message = data.message.message;
                            message.updated = data.message.updated;
                        }
                    })
                    this.setState({
                        changeMessageFoo: this.updateMessage,
                        current_messages: this.state.current_messages
                    });
                    break;
                default:
                    error('No such type!!!');
            }
        }
    }
    render() {
        return (
            <div>
                <div hidden id="messages-area">
                    <div style={{ "float": "right", "border": "1px solid black", "width": "75%", "height": "90vh", "overflow": "auto" }} id="messages-block">
                        <Messages messages={this.state.current_messages}
                            current_user={this.state.current_user}
                            chatSocket={this.state.chatSocket}
                            changeMessageFoo={this.state.changeMessageFoo}
                            deleteMessageFoo={this.deleteMessage} />
                    </div>
                    <MessageForm chatSocket={this.state.chatSocket} />
                </div>
                <div style={{ "maxWidth": "25%" }}>
                    {this.state.user_chats.map((chat) =>
                        <button className="list-group-item list-group-item-action" id={`room-${chat.id}`} key={chat.id} onClick={this.getMessages.bind(this, chat.id)}>
                            <div className="d-flex w-100 justify-content-between">
                                <h5 className="mb-1">{chat.product.name}</h5>
                            </div>
                            <p className="mb-1">
                                {!this.state.current_user.is_salesman ? chat.salesman.username : chat.user.username}
                            </p>
                        </button>
                    )}
                </div>
            </div>
        )
    }
}
export default Chats;