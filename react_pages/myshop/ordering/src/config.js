const DEBUG = true;

let HOST = null;
let PROTOCOL = null;
let SALESMAN = null;
let PRODUCT_SLUG = null;
const KEY = '8ce1b1742686b544f5c622b7532b49d5'

if (DEBUG === false) {
    HOST = window.location.host;
    SALESMAN = Number(window.location.pathname.split('/')[window.location.pathname.split('/').length - 3]);
    PRODUCT_SLUG = window.location.pathname.split('/')[window.location.pathname.split('/').length - 2]
    PROTOCOL = window.location.protocol;
} else {
    SALESMAN = 2;
    PRODUCT_SLUG = 'lg-oled77z19';
    HOST = '127.0.0.1:8000';
    PROTOCOL = 'http:'
}
const FULL_PATH = PROTOCOL + '//' + HOST;
const USER_URL = FULL_PATH+ '/api/v1/user/';
const URL_POST = 'https://api.novaposhta.ua/v2.0/json/';
const URL_ORDER = FULL_PATH + '/api/v1/create-ordering/';
const URL_DATA = FULL_PATH + '/api/v1/ordering/';
export { HOST, PROTOCOL, FULL_PATH, 
        SALESMAN, PRODUCT_SLUG, USER_URL, 
        KEY, URL_POST, URL_ORDER, URL_DATA }