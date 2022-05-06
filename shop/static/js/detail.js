const URL_MARK = "/api/v1/marks/";
const PRODUCT_ID = Number(location.href.split("/")[location.href.split("/").length - 3]);
const URL_MARK_DETAIL = `/api/v1/get_mark/${PRODUCT_ID}/`;
const URL_COMENT = "/api/v1/coment/";
const URL_COMENT_DETAIL = `/api/v1/get_coments/${PRODUCT_ID}/`;
const RATING_URL = `/api/v1/get_rating/${PRODUCT_ID}/`;
const RATING_DETAIL_URL = "/api/v1/rating/";
const URL_DATA = "/api/v1/rating_marks_comentsList/";


const getCookie = name => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



/* LIKES */
const deleteMark = (id) => {
    $.ajax({
        type: "DELETE",
        url: URL_MARK + id,
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        success: function (data) { },
        error: function (data) { console.log(rs.responseText); }
    })
}

const setLike = (user, product) => {
    $.ajax({
        url: URL_MARK,
        type: 'POST',
        data: {
            like: true,
            product: product,
            user: user,
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        dataType: "json",
        success: function (response) { },
        error: function (rs, e) {
            console.log(rs.responseText);
        }
    });
}

const setDislike = (user, product) => {
    $.ajax({
        url: URL_MARK,
        type: 'POST',
        data: {
            dislike: true,
            product: product,
            user: user,
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        dataType: "json",
        success: function (response) { },
        error: function (rs, e) {
            console.log(rs.responseText);
        }
    });
}
const likesDetail = ( marks, user ) => {
    let likes = 0;
    let dislikes = 0;
    if (marks.length > 0) {
        for (let i of marks) {
            if (i.like) likes++;
            if (i.dislike) dislikes++;
        }
        for (let i of marks) {
            $("#mark").empty();
            if (i.like && !i.dislike && user.id === i.user) {
                let data = `
                    <button type="submit" value="${i.id}" class="btn btn-success active"  onclick="deleteMark(this.value)">Вы уже поставили лайк ${likes}</button>
                    <button type="submit" value="${i.user}" name="${i.product}" class="btn btn-danger" onclick="setDislike(this.value, this.name)">Dislike ${dislikes}</button>
                     `
                $("#mark").append(data);
                break;
            }
            else if (!i.like && i.dislike && user.id === i.user) {
                let data = `
                    <button type="submit" value="${i.user}" name="${i.product}" class="btn btn-success" onclick="setLike(this.value, this.name)" >Like ${likes}</button>
                    <button type="submit" value="${i.id}" class="btn btn-danger" onclick="deleteMark(this.value)">Вы уже поставили дизлайк ${dislikes}</button>
                     `
                $("#mark").append(data);
                break;
            }
            else {
                let data = `
                    <button type="submit" value="${user.id}" name="${PRODUCT_ID}" class="btn btn-success" id="like" onclick="setLike(this.value, this.name)" >Like ${likes}</button>
                    <button type="submit" value="${user.id}" name="${PRODUCT_ID}" class="btn btn-danger" id="dislike" onclick="setDislike(this.value, this.name)">Dislike ${dislikes}</button>
                    `
                $("#mark").append(data);
            }
        }
    }
    else {
        $("#mark").empty();
        let data = `
        <button type="submit" value="${user.id}" name="${PRODUCT_ID}" class="btn btn-success" id="like" onclick="setLike(this.value, this.name)" >Like ${likes}</button>
        <button type="submit" value="${user.id}" name="${PRODUCT_ID}" class="btn btn-danger" id="dislike" onclick="setDislike(this.value, this.name)">Dislike ${dislikes}</button>
        `
        $("#mark").append(data);
    }
}

/* ENDLIKES */

/* COMENTS */
$(document).on("submit", "#comentForm", e => {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: URL_COMENT,
        success: function ({ current_user }) {
            let text = $("#comentText").val();
            $.ajax({
                type: "POST",
                url: URL_COMENT,
                data: {
                    text: text,
                    author: current_user.id,
                    product: PRODUCT_ID,
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                },
                success: function (data) { document.getElementById("comentForm").reset(); },
                error: function (data) { console.log(data); }
            })
        },
        error: function (data) { console.log(data); }
    })
})

const deleteComent = (id) => {
    $.ajax({
        type: "DELETE",
        url: URL_COMENT + id,
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        success: function (data) { },
        error: function (data) { console.log(data); }
    })
}

let update = {
    status: false,
    id: 0,
    count: 0,
};

const updateComent = (id) => {
    if (update.status === false) {
        update.status = true;
        update.id = Number(id);
    }
}

const changeComent = (id) => {
    $.ajax({
        type: "Patch",
        url: URL_COMENT + id + "/",
        data: {
            text: $(`#inputText`).val(),
        },
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        success: function (data) {
            $("#updateComent").empty();
            update.status = false;
            update.id = 0;
            update.count = 0;
        },
        error: function (data) { console.log(data); }
    })
}


const comentsDetail = (coments, user) => {
    $("#comentList").empty();
    for (let i of coments) {
        if (user.username !== i.author) {
            data = `
                <div class="card-header">
                    <span style="width: 75%;"">${i.author}</span>
                    <span style="float: right;">${i.created.slice(0, 16).replace("T", " ").replace("-", ".").replace("-", ".")}</span>
                </div>
                <div class="card-body">
                    <blockquote class="blockquote mb-0">
                        <small style="width: 50%;">${i.text}</small>
                    </blockquote>
                </div>`;
            $("#comentList").append(data);
        }
        else {
            if (update.status && update.id === i.id) {
                data = `
                    <div class="card-header">
                        <span style="width: 75%;">${i.author}</span>
                        <span style="float: right;">${i.created.slice(0, 16).replace("T", " ").replace("-", ".").replace("-", ".")}</span>
                    </div>
                    <div class="card-body">
                        <blockquote class="blockquote mb-0">
                            <input type = "text" id = "inputText" class="form-control" value = "${i.text}"/>        
                            <button type="button"class="btn btn-success" value = "${i.id}" style="float: right;" onClick="changeComent(this.value)">Сохранить</button>
                                    
                            </blockquote>
                    </div>`;
                if (update.count < 1) { $("#updateComent").append(data); }
                update.count++;
            }
            else {
                data = `
                    <div class="card-header">
                    <span style="width: 75%;">${i.author}</span>
                        <span style="float: right;">${i.created.slice(0, 16).replace("T", " ").replace("-", ".").replace("-", ".")}</span>
                    </div>
                    <div class="card-body">
                        <blockquote class="blockquote mb-0">
                            <small style="width: 50%;">${i.text}</small>         
                            <button type="button"class="btn btn-danger" style="float: right;" value="${i.id}" onClick="deleteComent(this.value)">Удалить</button>
                            <button type="button"class="btn btn-success" style="float: right;" value="${i.id}" onClick="updateComent(this.value)">Изменить</button>
                                    
                        </blockquote>
                    </div>`;
                $("#comentList").append(data);
            }
        }
    }
}
/* ENDCOMENTS */

/* RATING */
const getAverage = rating => {
    if (rating.length > 0) {
        let average = 0;
        rating.map(v => { average += v.rating });
        return average / rating.length;
    }
    return 0;
}

const changeRating = (id, value) => {
    $.ajax({
        type: "Patch",
        url: RATING_DETAIL_URL + id + "/",
        data: {
            rating: Number(value),
        },
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        success: function (data) { },
        error: function (data) { console.log(data); }
    })
}

const createRating = (value) => {
    $.ajax({
        type: "GET",
        url: "/api/v1/current_user/",
        success: function ({ user }) {
            $.ajax({
                type: "POST",
                url: RATING_DETAIL_URL,
                data: {
                    rating: Number(value),
                    user: user.id,
                    product: PRODUCT_ID,
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                },
                success: function (data) { },
                error: function (data) { console.log(data); }
            })
        },
        error: function (data) { console.log(data); }
    })
}

const deleteRating = (id) => {
    $.ajax({
        type: "DELETE",
        url: RATING_DETAIL_URL + id,
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        success: function (data) { },
        error: function (data) { console.log(rs.responseText); }
    })
}

const ratingDetail = (rating, user) => {
    let averageRating = `<p>Средний рейтинг : ${getAverage(rating)}</p>`;
    if (rating.length > 0) {
        for (let i of rating) {
            $("#rating").empty();
            if (i.user === user.id) {
                let data = `${averageRating}`
                for (let j = 1; j <= 5; j++) {
                    if (j === i.rating) {
                        data += `<button type="button" class="btn btn-outline-dark active" id="${i.id}" onclick="deleteRating(this.id)">${j}</button>`;
                    }
                    else {
                        data += `<button type="button" class="btn btn-outline-dark" id="${i.id}" value = "${j}" onclick="changeRating(this.id, this.value)">${j}</button>`;
                    }
                }
                $("#rating").append(data);
                break;
            }
            else {
                let data = `${averageRating}`;
                for (let j = 1; j <= 5; j++) {
                    data += `<button type="button" class="btn btn-outline-dark" value = "${j}" onclick="createRating(this.value)">${j}</button>`;
                }
                $("#rating").append(data);

            }
        }
    }
    else {
        $("#rating").empty();
        let data = `${averageRating}`;
        for (let j = 1; j <= 5; j++) {
            data += `<button type="button" class="btn btn-outline-dark" value = "${j}" onclick="createRating(this.value)">${j}</button>`;
        }
        $("#rating").append(data);
    }
}

/* ENDRATING */

/* MAIN */
$(() => {
    setInterval(() => {
        $.ajax({
            type: 'GET',
            url: URL_DATA,
            data: {
                productID: PRODUCT_ID,
            },
            success: ({ user, coments, marks, rating }) => {
                ratingDetail(rating, user);
                comentsDetail(coments, user);
                likesDetail(marks, user)
            },
            error: data => { console.log(data) }
        });
    }, 1000)
})
/* ENDMAIN */