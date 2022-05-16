import React from "react";
import $ from 'jquery';
import Coments from './Coments';
import getCookie from "./getCookie";
import { FULL_PATH } from "../config";


class CreateComent extends React.Component {
    constructor({ product, current_user, coments, is_bought }) {
        super();
        this.state = {
            product: product,
            current_user: current_user,
            coments: coments,
            is_bought:is_bought,
            OnClickComentFoo: this.changeComent
        }
    }
    changeComent = (id) => {
        let oldText = $(`#${id}`).text();
        $(`#${id}`).html(`<input class="form-control" type="text" id ='${id}' value='${oldText}'><div id="validationComentChangeText"></div>`);
        $(`#change_${id}`).text("Save");
        this.setState({ OnClickComentFoo: this.saveComent })
    }
    addComent = () => {
        let text = $('#comentForm');
        if(text.val().trim().length>=5){
            $.ajax({
                type: 'POST',
                url:FULL_PATH+"/api/v1/coment/",
                data: {
                    text: text.val(),
                    product: this.state.product.id,
                    user: this.state.current_user.id,
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                },
                success: data => {
                    this.setState({
                        coments: [data, ...this.state.coments]
                    })
                    text.val('');
                    $('#comentForm').removeClass('is-invalid');
                    $('#validationComentCreate').removeClass('invalid-feedback').text('');
                },
                error: data => { console.log(data) }
            })
        } else{
            $('#comentForm').addClass('is-invalid');
            $('#validationComentCreate').addClass('invalid-feedback').text('В тексте коментария должно быть не меньше 5 символов');
        }
    }
    saveComent = (id) => {
        let text = $('input').val();
        if(text.trim().length>=5){
            $.ajax({
                type: 'PATCH',
                url: FULL_PATH+`/api/v1/coment/${id}/`,
                data: {
                    text: text,
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                },
                headers: { "X-CSRFToken": getCookie('csrftoken') },
                success: data => {
                    $(`#${id}`).html(`<span className="card-text" id=${id} style={{ 'width': '70%' }}>${text}</span>`);
                    $(`#change_${id}`).text("Update");
                    this.setState({
                        OnClickComentFoo: this.changeComent
                    })
                },
                error: data => console.log(data)
            })
        } else {
            $('input').addClass('is-invalid');
            $('#validationComentChangeText').addClass('invalid-feedback').text('В тексте коментария должно быть не меньше 5 символов');
        }
    }
    deleteComent = (id) => {
        $.ajax({
            type: 'DELETE',
            url: FULL_PATH+`/api/v1/coment/${id}/`,
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            success: data => {
                this.setState({
                    coments: this.state.coments.filter(coment => {
                        if (coment.id !== id) return coment
                    }
                    )
                })
            },
            error: data => { console.log(data) }
        })
    }
    render() {
        return (
            <div>
                {this.state.is_bought?<div className="mb-3">
                    <label className="form-label">Добавте коментарий</label>
                    <textarea className="form-control" id="comentForm" rows="3"></textarea>
                    <div id="validationComentCreate"></div>
                    <button type="button" className="btn btn-primary" id="send_coment" style={{ 'margin': '10px 0px 0px 0px' }} onClick={this.addComent}>Отправить</button>
                </div>:<div></div>}
                <Coments current_user={this.state.current_user}
                    coments={this.state.coments}
                    changeComentFoo={this.state.OnClickComentFoo}
                    deleteComentFoo={this.deleteComent} />
            </div>
        )
    }
}

export default CreateComent;