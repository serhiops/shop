const CATEGORY = location.href.split("/")[location.href.split("/").length-2];
const URL_FILTER = "/api/v1/product_filter/";


$(document).ready(() => {
    setInterval(() => {
        let city = $("#cityInput").val();
        let beginPrice = $("#begin_priceInput").val();
        let endPrice = $("#end_priceInput").val();
        $.ajax({
            url: URL_FILTER,
            type: 'GET',
            scriptCharset: "utf-8",
            data: {
                city:city,
                begin_price:Number(beginPrice),
                end_price:()=>{
                    if(!endPrice)return 100000000000;
                    else return Number(endPrice);
                },
                category:CATEGORY
            },
            dataType: "json",
            success: response=> {
                $("#productsCount").empty();
                $("#productsCount").append(response);
             },
            error: function (rs, e) {
                console.log(rs.responseText);
            }
        });
    }, 1000)
})