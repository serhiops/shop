import React from 'react';
import ReactDOM from 'react-dom/client';
import Data from './Data';
import FormApp from './FormApp';
import { SALESMAN, PRODUCT_SLUG, URL_DATA } from './config'
import getCookie from './getCookie'
import $ from 'jquery'

$.ajax({
  type: 'POST',
  url: URL_DATA,
  data: {
    salesman: SALESMAN,
    product_slug: PRODUCT_SLUG,
    csrfmiddlewaretoken: getCookie('csrftoken'),
  },

  success: ({ salesman, product, current_user }) => {
    const data = ReactDOM.createRoot(document.getElementById('data'));
    const form = ReactDOM.createRoot(document.getElementById('form'));
    data.render(
      <React.StrictMode>
        <Data salesman={salesman} product={product} current_user={current_user} />
      </React.StrictMode>
    );
    form.render(
      <React.StrictMode>
        <FormApp product={product} />
      </React.StrictMode>
    )
  },
  error: (er) => { console.log(er) }
})


