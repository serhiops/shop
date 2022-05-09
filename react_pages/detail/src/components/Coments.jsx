

const Coments = ({ current_user, coments, changeComentFoo, deleteComentFoo }) => {

    const List = (coment) => {
        let change_id = `change_${coment.id}`
        if (coment.author === current_user.username) {
            return <div className="card" key={coment.id}>
                <div className="card-header">
                    <span style={{ 'width': '50%' }}>{coment.author}</span>
                    <span style={{ 'float': 'right' }}>{coment.created.slice(0, 16).replace("T", " ").replace("-", ".").replace("-", ".")}</span>
                </div>
                <div className="card-body">
                    <span className="card-text" id={coment.id} style={{ 'width': '70%' }}>{coment.text}</span>
                    <div style={{ 'float': 'right' }}>
                        <div className="btn-group" role="group" aria-label="Basic mixed styles example">
                            <button type="button" id={change_id} className="btn btn-success" onClick={changeComentFoo.bind(this, coment.id)}>Change</button>
                            <button type="button" className="btn btn-danger" onClick={deleteComentFoo.bind(this, coment.id)}>Delete</button>
                        </div>
                    </div>
                </div>
            </div>
        }
        return <div className="card" key={coment.id}>
            <div className="card-header">
                <span style={{ 'width': '50%' }}>{coment.author}</span>
                <span style={{ 'float': 'right' }}>{coment.created.slice(0, 16).replace("T", " ").replace("-", ".").replace("-", ".")}</span>
            </div>
            <div className="card-body">
                <p className="card-text" id={coment.id}>{coment.text}</p>
            </div>
        </div>

    }
    return (
        <div style={{'width':'100%'}}>
            {coments.map((coment) =>
                List(coment)
            )}
        </div>
    );
};

export default Coments;