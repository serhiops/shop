import $ from 'jquery';

const MessageForm = ({chatSocket}) => {

    const sendMessage = () => {
        let message = $('#msg-input');
        chatSocket.send(JSON.stringify({
            'message': message.val(),
            'type': 'POST',
        }));
        message.val('');
    }
    return (
        <div style={{ "width": "75%", "float": "right" }}>
            <form typeof="post">
                <input className="form-control" type="text" style={{ "width": "79%", "float": "left" }} id='msg-input'/>
                <button type="button" className="btn btn-primary" style={{ "width": "20%", "float": "right" }} id='msg-send-button' onClick={sendMessage}>Send</button>
            </form>
        </div>
    );
}

export default MessageForm;