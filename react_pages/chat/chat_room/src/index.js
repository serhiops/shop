import React from 'react';
import ReactDOM from 'react-dom/client';
import ChatsApp from './ChatsApp';
import $ from 'jquery';

const API = 'http://127.0.0.1:8000/chat/api/v1/rooms/'

$.ajax({
  type: 'GET',
  url: API,
  success: (data) => {
    const chats = ReactDOM.createRoot(document.getElementById('chats'));
    chats.render(
      <ChatsApp user_chats = {data.user_chats} current_user = {data.current_user} />
    );

  }

})


