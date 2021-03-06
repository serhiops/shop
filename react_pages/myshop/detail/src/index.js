import React from 'react';
import ReactDOM from 'react-dom/client';
import ProductApp from './ProductApp';
import LikesApp from './LikesApp';
import $ from 'jquery';
import RatingApp from './RatingApp';
import CreateComentApp from './CreateComentApp';
import {FULL_PATH, PRODUCT} from './config';

const API = FULL_PATH+`/api/v1/react/${PRODUCT}/`;

$.ajax({
    type: 'GET',
    url: API,
    success: (data) => {
        const product = ReactDOM.createRoot(document.getElementById('product'));
        const likes = ReactDOM.createRoot(document.getElementById('likes'));
        const rating = ReactDOM.createRoot(document.getElementById('rating'));
        const coment_form = ReactDOM.createRoot(document.getElementById('coment-form'));

        product.render(
            <ProductApp product={data.product} images={data.images} company_name= {data.company_name} />
        );
        likes.render(
            <LikesApp likes={data.likes}
                dislikes={data.dislikes}
                product={data.product}
                current_user={data.current_user}
                is_disliked_by_current_user={data.is_disliked_by_current_user}
                is_liked_by_current_user={data.is_liked_by_current_user} />
        );
        rating.render(
            <RatingApp
                current_user_rating={data.current_user_rating}
                average_rating={data.average_rating}
                product={data.product}
                is_bought = {data.is_bought} />
        );
        coment_form.render(
            <CreateComentApp product={data.product}
            current_user={data.current_user}
            coments = {data.coments}
            is_bought = {data.is_bought}/>
        );
    }
})


