from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import Message

import redis

conn = redis.Redis('localhost',decode_responses=True)

online_users = []
for i in range(0, conn.llen('UserList')):
    if conn.lindex('UserList', i) not in online_users:
        online_users.append(conn.lindex('UserList', i))

print(online_users)

# Create your views here.

def room(request, room_name):

    # checking if user is allowed or not
    permission = False

    room_name_components = room_name.split('-')
    auth_user1_id = int(room_name_components[1])
    auth_user2_id = int(room_name_components[2])

    if auth_user1_id>auth_user2_id:
        messages.info(request, 'Invalid Chat!')
        return redirect('home')

    if request.user.id==auth_user1_id:
        permission = True
        other_user = get_user_model().objects.filter(id=auth_user2_id)[0]

    elif request.user.id==auth_user2_id:
        permission = True
        other_user = get_user_model().objects.filter(id=auth_user1_id)[0]
    else:
        messages.info(request, 'You are not authorized to enter this chat!')
        return redirect('home')

    # retrieving previously stored messages
    
    threads = ['chat-{}-{}'.format(auth_user1_id,auth_user2_id),'chat-{}-{}'.format(auth_user2_id,auth_user1_id)]
    prev_chats = Message.objects.filter(Q(thread_name=threads[0])|Q(thread_name=threads[1])).order_by('timestamp')

    context = {
        "room_name": room_name,
        "permission": permission,
        "other_user": other_user,
        "prev_chats": prev_chats,
        "online_users": online_users,       
    }

    return render(request, "chatapp/conversation.html", context)
