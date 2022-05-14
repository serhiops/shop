const URL_USER = "/api/v1/user/";
const URL_CURENTUSER = "/api/v1/current_user/"
const PRODUCT_ID = Number(location.href.split("/")[location.href.split("/").length - 3]);
const URL_ORDERING = `/api/v1/get_ordering/`;
const URL_POST_OFICES = "/api/v1/post_ofices/";

function getCookie(name) {
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

$("#changeData").on("click", (e) => {
    let list = document.getElementById("userData");
    try {
        let full_name = document.getElementById("name").textContent.split(":")[1].replace(/\s+/g, ' ').replace(" ", "").split(" ");
        let phone = document.getElementById("phone").textContent.split(":")[1].replace(" ", "");
        let city = document.getElementById("city").textContent.split(":")[1].replace(" ", "");
        list.innerHTML = `
        <form id="postform" method="post"> 
        <li class="list-group-item" >Имя: <input type="text"  id="name" class="form-control" value = "${full_name[0]}"/></li>
        <li class="list-group-item" >Фамилие: <input type="text"  id="sername" class="form-control" value = "${full_name[1]}"/></li>
        <li class="list-group-item" >Контактный номер : <input type="text"  id="phone" class="form-control" value = "${phone}"/></li>
        <li class="list-group-item" >Город : <input type="text"  id="city" class="form-control" value = "${city}"/></li>
        <input type="submit" class="btn btn-success form-control"/>
        </form>
        `;
        $("#changeData").text("Отменить")
        $("#orderingForm").hide();
    }
    catch {
        $.ajax({
            type: "GET",
            url: URL_ORDERING,
            data: {
                productID: PRODUCT_ID
            },
            success: function ({ user, salesman, product }) {
                list.innerHTML = `
                <li class="list-group-item">Продавец : ${salesman.first_name}  ${salesman.last_name}</li>
                <li class="list-group-item" id="name">Покупатель : ${user.first_name}  ${user.last_name}</li>
                <li class="list-group-item" id="phone">Контактный номер : ${user.number_of_phone}</li>
                <li class="list-group-item" id="city">Город : ${user.city}</li>
                <li class="list-group-item">Товар : ${product.name}</li>
                <li class="list-group-item">Цена : ${product.price}</li>
                `;
                document.getElementById("changeData").textContent = "Изменить личные данные";
                $("#orderingForm").show();
            },
            error: function (data) { console.log(data); }
        })
    }
})

$(document).on("submit", "#postform", function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: URL_CURENTUSER,
        success: function ({ user }) {
            $.ajax({
                type: "Patch",
                url: URL_USER + user.id + "/",
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    first_name: $("#name").val(),
                    last_name: $("#sername").val(),
                    number_of_phone: $("#phone").val(),
                    city: $("#city").val(),
                },
                headers: { "X-CSRFToken": getCookie('csrftoken') },
                success: function (data) { location.href = location.href; },
                error: function (data) { console.log(data); }
            })
        }
    })
})


$(() => {
    let city = $("#userData #city").text().replace(/\s+/g, ' ').split(" ");
    let options = $("#id_post_office");
    $.ajax({
        type: "GET",
        url: URL_POST_OFICES,
        data: {
            city: city[city.length - 1],
        },
        success: function (data) {
            options.empty();
            options.append(`<option value='0' selected disabled>Выберите почтовое отделение</option>`);
            for (let i of data) {
                options.append(`<option value='${i.id}'>${i.name}</option>`);
            }
        },
        error: function (data) { console.log(data); }
    })

})
