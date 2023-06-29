# neoChat

This a chat application using Django that allows users to create accounts, log in, view online users, start chats with online users, and restrict sending messages to offline users, along with the functionality of authorizing the user before entering a private chat so that each user can only see the conversations that they are a part of.

The messages are sent in real-time using Django Channels that uses WebSocket Protocol. Whenever a user clicks on another online user, they are routed to a private chatroom and all the messages are stored in the database.

## Instructions to run

I used Redis as the backing store for the channel layer, as recommended in the official documentaion of Django Channels. Since I'm on Windows, I seperately downloaded Docker to run and install Redis. 

Once the Docker Engine is open, run the Redis server using the command 

```
docker run --rm -p 6379:6379 redis:7
```

Install all the dependencies from the requirements.txt

Run the Django server from manage.py and open two different incognito windows to test out the chat app by logging in/ registering as different users in the two windows.


