from django.shortcuts import render

def user_chats(request):
    return render(request, 'chat/react_pages/user_chats/index.html', {'user_chatsreact':True})
