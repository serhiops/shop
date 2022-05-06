const URL_USER = "/api/v1/user/";

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


$("#changeUserData").on("click", function () {
    let list = document.getElementById("dataList");
    try {
        let username = document.getElementById("username").textContent.split(":")[1].replace(" ", "");
        let name = document.getElementById("name").textContent.split(":")[1].replace(" ", "");
        let sername = document.getElementById("sername").textContent.split(":")[1].replace(" ", "");
        let phone = document.getElementById("phone").textContent.split(":")[1].replace(" ", "");
        let age = document.getElementById("age").textContent.split(":")[1].replace(" ", "");
        list.innerHTML = `
        <form id="postform" method="post">
                <li class="list-group-item">Никнейм : <input class="form-control" type="text" id="username" value = "${username}"/></li>
                <li class="list-group-item">Имя : <input class="form-control" type="text"  id="name" value = "${name}"/></li>
                <li class="list-group-item">Фамилия : <input class="form-control" type="text" id="sername" value = "${sername}"/></li>
                <li class="list-group-item">Номер телефона : <input class="form-control" type="text" id="phone" value = "${phone}"/></li>
                <li class="list-group-item">Возраст : <input class="form-control" type="text" id="age" value = "${age}"/></li>
                <input type="submit" class="btn btn-success"/>
        </form>
    `;
    document.getElementById("changeUserData").textContent = "Отменить";
    }
    catch {
        user_id = list.getAttribute("userid");
        $.ajax({
            type: "GET",
            url: URL_USER + user_id,
            success: function (user) { 
                list.innerHTML = `
                <li class="list-group-item" id="username">Никнейм : ${ user.username }</li>
                <li class="list-group-item" id="name">Имя : ${ user.first_name }</li>
                <li class="list-group-item" id="sername">Фамилия : ${ user.last_name }</li>
                <li class="list-group-item" id="email">Почта : ${ user.email }</li>
                <li class="list-group-item" id="phone">Номер телефона : ${ user.number_of_phone }</li>
                <li class="list-group-item" id="joined">На сайте с : ${user.date_joined.slice(0,16).replace("T", " ").replace("-",".").replace("-",".")}</li>
                <li class="list-group-item" id="age">Возраст : ${user.age}</li>
                `;
                document.getElementById("changeUserData").textContent = "Изменить данные";
            },
            error: function (data) { console.log(rs.responseText); }
        })
    }
})

$(document).on("submit", "#postform", function (e) {
    e.preventDefault();
    let list = document.getElementById("dataList");
    user_id = list.getAttribute("userid");
    $.ajax({
        type: "Patch",
        url: URL_USER + user_id + "/",
        data:{
            csrfmiddlewaretoken: getCookie('csrftoken'),
            first_name:$("#name").val(),
            last_name:$("#sername").val(),
            username:$("#username").val(),
            number_of_phone:$("#phone").val(),
            age:$("#age").val(),
        },
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        success:function(data){location.href=location.href;},
        error:function(data){console.log(data);}
    })
})