import React from 'react';
import getCookie from './getCookie';

let csrftoken = getCookie('csrftoken');

const CSRFToken = () => {
    return (
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken? csrftoken:''} />
    );
};
export default CSRFToken;