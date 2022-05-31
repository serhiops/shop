import { useState } from "react";
import { KEY, URL_POST, URL_ORDER } from "../config";
import { setError } from "./Alert";
import getCookie from "../getCookie";
import $ from 'jquery';
import CSRFToken from "../csrfToken";

const Form = ({ product }) => {
    
    let [citys, setSitys] = useState([]);
    let [posts, setPosts] = useState([]);

    const getCitys = () => {
        const city = document.getElementById("input-city").value;
        let data = {
            "apiKey": KEY,
            "modelName": "Address",
            "calledMethod": "searchSettlements",
            "methodProperties": {
                "CityName": city,
                "Limit": "50",
                "Page": "1"
            },
            csrfmiddlewaretoken: getCookie('csrftoken')
        };
    
        fetch(URL_POST, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(data)
        })
            .then(res => {return res.json() })
            .then(({ data, errors, errorCodes }) => {
                try{
                    setSitys(data[0].Addresses);
                    getPosts(data[0].Addresses[0].MainDescription)
                } catch{}
            })
    }

    const getPosts = (city) => {
        let data = {
            "apiKey": KEY,
            "modelName": "Address",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "CityName": city,
                "Page": "1",
                "Language": "UA",
            },
            csrfmiddlewaretoken: getCookie('csrftoken')
        };
        fetch(URL_POST, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(data)
        })
            .then(res => { return res.json() })
            .then(({ data }) => {
                setPosts(data);
            });
    }

    const getSityFromSelect = (e) => {
        try{
            let city = document.getElementById('select-city').value;
            document.getElementById('input-city').value = city;
            let c = citys.filter(o=>{if (o.Present === city){return o}})
            getPosts(c[0].MainDescription);
        } catch{}
    }

    const getPostsFromSelect = () => {
        let post = document.getElementById('select-posts').value;
        document.getElementById('input-post').value = post;
    }

    const getPostsFromInput = () => {
        let n = document.getElementById("input-post").value;
        setPosts(posts.sort((a, b) => Number(a.Number) - Number(b.Number)));
        let arr = [];
        for (let i of posts) {
            if (i.Number === n) {
                arr = [i, ...posts.filter(a => a.Number !== n)];
                break;
            }
        }
        if (arr.length !== 0) setPosts(arr);
    }

    const createOrder = (e)=>{
        const city = document.getElementById('input-city').value;
        const post = document.getElementById('input-post').value;
        const number = document.getElementById('count-products').value;
        if (city.length<2 || post.length<3 ||number.length === 0 ){setError('Вы указали невалидные данные'); e.preventDefault(); return;}
        $.ajax({
            type:'POST',
            url:URL_ORDER,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
              },
            data:{
                salesman:product.salesman,
                product:product.id,
                post_office:post,
                city:city,
                number:number,
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
        })
    }

    

    return (
        <div>
            <form method="post" className="row g-3" id = 'post-form'>
                <CSRFToken/>
                <div className="row g-3">
                    <div className='col-md-7'>
                        <input className="form-control" type="text" id='input-city' onChange={getCitys} />
                    </div>
                    <div className='col-md-5'>
                        <select className="form-select"id='select-city' onClick={getSityFromSelect}>
                            {citys.map((c, index) =>
                                <option value={c.Present} key={index}>{c.Present}</option>
                            )}
                        </select>
                    </div>

                    <div className='col-md-7'>
                        <input className="form-control" type="text" id='input-post' onChange={getPostsFromInput} />
                    </div>
                    <div className='col-md-5'>
                        <select className="form-select" id='select-posts' onChange={getPostsFromSelect}>
                            {posts.map((p, index) =>
                                <option value={p.Description} key={index}>{p.Description}</option>
                            )}
                        </select>
                    </div>
                    <input className="form-control" type="text" id = 'count-products' placeholder="Количество единиц"/>
                    <button type="submit" className="btn btn-primary" onClick={createOrder}>Оформить заказ</button>
                </div>
            </form>
        </div>
    )
}

export default Form;