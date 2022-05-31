import $ from 'jquery';


const setError = (text, time = 8500) =>{
    $('#alerts').append(`<div class="alert alert-danger" role="alert">${text}</div>`);
    $('#alerts > div').fadeOut(time);
}
const setSuccess = (text, time = 8500)=>{
    $('#alerts').append(`<div class="alert alert-success" role="alert">${text}</div>`);
    $('#alerts > div').fadeOut(time);
}

export  {setError, setSuccess}