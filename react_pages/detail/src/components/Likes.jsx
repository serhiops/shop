import React, {useState} from "react"
import $ from 'jquery';
import getCookie from "./getCookie";

const Likes = ({ likes, dislikes, product, current_user,is_liked_by_current_user,is_disliked_by_current_user }) => {

    let text_like = 'Like';
    let text_dislike = 'Dislike';
    if (is_liked_by_current_user)text_like='Liked';
    else if(is_disliked_by_current_user)text_dislike='Disliked'
    
    let [text_l, setTextLike] = useState(text_like);
    let [text_d, setTextDislike] = useState(text_dislike);
    let [count_likes, setLikes] = useState(likes);
    let [count_dislikes, setDislikes] = useState(dislikes);

    const addLike = () => {
        $.ajax({
            type: 'POST',
            url: `http://127.0.0.1:8000/api/v1/react/`,
            data: {
                product: product.id,
                user: current_user.id,
                like: true,
                csrfmiddlewaretoken: getCookie('csrftoken'),
            },
            success: (data) => {
                if (text_l === 'Like' && text_d === 'Dislike') {
                    setTextLike('Liked');
                    setLikes(count_likes+1);
                }
                else if (text_l === 'Liked' && text_d === 'Dislike') {
                    setTextLike("Like");
                    setLikes(count_likes-1);
                }
                else if (text_l === 'Like' & text_d === 'Disliked') {
                    setTextLike('Liked');
                    setTextDislike('Dislike');
                    setLikes(count_likes+1);
                    setDislikes(count_dislikes-1)
                };
            },
            error: (data) => { console.log(data) }
        })
    }
    const addDislike = () => {
        $.ajax({
            type: 'POST',
            url: `http://127.0.0.1:8000/api/v1/react/`,
            data: {
                product: product.id,
                user: current_user.id,
                dislike: true,
                csrfmiddlewaretoken: getCookie('csrftoken'),
            },
            success: (data) => {
                if (text_d === 'Dislike' && text_l === 'Like') {
                    setTextDislike('Disliked');
                    setDislikes(count_dislikes+1)
                }
                else if (text_d === 'Disliked' && text_l === 'Like') {
                    setTextDislike('Dislike');
                    setDislikes(count_dislikes-1)
                }
                else if (text_d === 'Dislike' && text_l === 'Liked') {
                    setTextDislike('Disliked');
                    setTextLike('Like');
                    setLikes(count_likes-1);
                    setDislikes(count_dislikes+1);
                };
            },
            error: (data) => { console.log(data) }
        })
    }

    return (
        <div className="btn-group" role="group" aria-label="Basic mixed styles example" style={{ "float": "right" }}>
            <button type="button" className="btn btn-success" onClick={addLike}>{text_l} {count_likes}</button>
            <button type="button" className="btn btn-danger" onClick={addDislike}>{text_d} {count_dislikes}</button>
        </div>
    );
}


export default Likes;