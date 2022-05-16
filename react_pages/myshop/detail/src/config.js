const DEBUG = false

let HOST = null;
let PRODUCT = null;
let PROTOCOL = null;
if (DEBUG===false){
    HOST = window.location.host;
    PRODUCT = window.location.pathname.split('/')[2];
    PROTOCOL = window.location.protocol;
} else{
    PRODUCT = 2;
    HOST = '127.0.0.1:8000';
    PROTOCOL = 'http:'
}

const FULL_PATH = PROTOCOL + '//'+ HOST;

export {HOST, PRODUCT, PROTOCOL, FULL_PATH}