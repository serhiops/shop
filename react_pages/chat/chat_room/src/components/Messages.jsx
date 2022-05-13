import './styles/Styles.css'

const Messages = ({ messages, current_user, changeMessageFoo, deleteMessageFoo }) => {
    const getListMessages = (message) => {
        if (message.author === current_user.id) {
            if (!message.is_active) {
                return <div style={{ 'maxWidth': '30%' }} key={message.id}>
                    <div className="del-message-cur-user">
                        <span className="del-message-text">Вы удалили сообщение</span>
                    </div>
                </div>
            } else {
                return <div id={`author-message-${message.id}`} style={{ 'maxWidth': '30%' }} key={message.id}>
                    <div style={{ "marginBottom": "1px" }}>
                        <button type="button" className="btn btn-light btn-sm" id={`update-${message.id}`} onClick={changeMessageFoo.bind(this, message.id)}>Update</button>
                        <button type="button" className="btn btn-light btn-sm" onClick={deleteMessageFoo.bind(this, message.id)}>Delete</button>
                        {message.created !== message.updated ? <small style={{ "fontSize": "13px" }}>Изменено</small> : <div />}
                    </div>
                    <div id={`message-${message.id}`} className='active-message-cur-user'>
                        {message.message}
                    </div>

                </div>
            }
        } else {
            if (!message.is_active) {
                return <div key={message.id}>
                    <br />
                    <div className="del-message-other-user">
                        <span className="del-message-text">Собеседник удалил сообщение</span>
                        <div />
                    </div>
                    <br />
                    <br />
                </div>
            } else {
                return <div key={message.id}>
                    {message.created !== message.updated ? <div><div style={{ "float": "right" }}> <small className='change-text-other-user'>Изменено</small></div><br /></div> : <div></div>}
                    <div id="message-{{ i.pk }}" className="active-message-other-user">
                        {message.message}
                    </div>
                    <br />
                    <br />
                </div>
            }
        }
    }
    return (
        <div>
            {messages.map(message =>
                getListMessages(message)
            )}
        </div>
    )
}


export default Messages;