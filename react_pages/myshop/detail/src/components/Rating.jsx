import $ from 'jquery';
import React, { useState } from 'react';
import getCookie from "./getCookie";
import { FULL_PATH } from '../config';

const Rating = ({ current_user_rating, average_rating, product, is_bought }) => {

    let [average_r, setAverageRating] = useState(average_rating);

    const addRating = (mark) => {
        $.ajax({
            type: 'POST',
            url: FULL_PATH+'/api/v1/react-mark/',
            data: {
                product: product.id,
                rating: Number(mark),
                csrfmiddlewaretoken: getCookie('csrftoken'),
            },
            success: (data) => {
                if (data.del) {
                    $(`#rating-${mark}`).removeClass("active");
                }
                else {
                    $('button[class$=active]').removeClass('active')
                    $(`#rating-${mark}`).addClass("active")
                }
                setAverageRating(data.average_rating);
            },
            error: data => { console.log(data) }
        })
    }

    const count = [1, 2, 3, 4, 5]

    const RatingList = (rat) => {
        if (current_user_rating && current_user_rating.rating === rat) {
            return <button key={rat} type="button" className="btn btn-outline-dark active" id={`rating-${rat}`} onClick={addRating.bind(this, rat)}>{rat}</button>
        } else {
            return <button key={rat} type="button" className="btn btn-outline-dark" id={`rating-${rat}`} onClick={addRating.bind(this, rat)}>{rat}</button>
        }
    }
    return (
        <div style={{ 'margin': '10px 0px' }}>
            {is_bought ?
                <div>
                    <p>Средний рейтинг : {average_r}</p>
                    <div className="btn-group" role="group">
                        {count.map((index) =>
                            RatingList(index)
                        )}
                    </div>
                </div> : <div></div>}
        </div>
    );
}

export default Rating;
