import $ from 'jquery';
import React, {useState} from 'react';
import getCookie from "./getCookie";

const Rating = ({ current_user_rating, average_rating, product }) => {

    let [average_r, setAverageRating] = useState(average_rating);

    const addRating = (mark) => {
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/api/v1/react-mark/',
            data: {
                product: product.id,
                rating: Number(mark),
                csrfmiddlewaretoken: getCookie('csrftoken'),
            },
            success: (data) => {
                if (data.del) {
                    $(`#rating_${mark}`).removeClass("active");
                }
                else {
                    $('button[class$=active]').removeClass('active')
                    $(`#rating_${mark}`).addClass("active")
                }
                setAverageRating(data.average_rating);  //average_rating from response data
            },
            error: data => { console.log(data) }
        })
    }

    let count = [1, 2, 3, 4, 5]

    const RatingList = (rat) => {
        let rat_id = `rating_${rat}`
        if (current_user_rating && current_user_rating.rating === rat) {
            return <button key={rat} type="button" className="btn btn-outline-dark active" id={rat_id} onClick={addRating.bind(this, rat)}>{rat}</button>
        } else {
            return <button key={rat} type="button" className="btn btn-outline-dark" id={rat_id} onClick={addRating.bind(this, rat)}>{rat}</button>
        }
    }
    return (
        <div style={{ 'margin': '10px 0px' }}>
            <p>Средний рейтинг : {average_r}</p>
            <div className="btn-group" role="group">
                {count.map((index) =>
                    RatingList(index)
                )}
            </div>
        </div>
    );
}

export default Rating;
