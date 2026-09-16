# Custom TCP Network Server & Messaging Architecture


This is basically a custom made chat room with its own server, http server and parser along with the WebSocket framework. It's entirely built with python. It allows you to have real time chat with the people.



## Why I built this?
There are multiple reasons to build this project. First reason was the fact that I wanted to build something which would help me to know better about how networking works 
underneath, not just by using libraries and frameworks, but by building everything from scratch by reading the appropriate resources like RFC and implementing the protocols by 
myself. Before this, I tried to build an HTTP server and parser as part of my project, but due to some other commitments, I had to drop that idea. But after starting this 
project, I was certain that I wouldn't drop this idea for any reason and had a clear deadline in my mind, and I was able to complete it by that time. Apart from that, how the 
actual communication happens through the internet was something which I thought about a lot, and this project was something which could give me some good clarity about that, 
so I decided to pursue it.



## Features
- Real time messaging using WebSocket.
- Multiple users can chat at a time
- Duplicate name prevention
- Input is validated
- Username is displayed with each message
- JWT authentication
- User registration and login



## Technical merits
- Custom made http server and parser(RFC 7230)
- Custom Websocket handshake(RFC 6455)
- Custom binary encoder and decoder
- Thread safe broadcasting with locks
- Bcrypt password hashing
- Multithreaded server


## Tech stack
**Backend** - Python
**Frontend** - Javascript, Html, CSS

**Database** - PostgresSQL

**Libraries** - bcrypt(password hashing), struct(binary frame parsing), threading(multithreading), socket(raw TCP sockets), base64(Websocket handshake), hashlib(SHA1 for websocket), psycopg2(postgresSQL driver), pyJWT(JSON web token)

**Protocols** - TCP, HTTP(RFC 7230), WEBSOCKET(RFC 6455)

**NO Frameworks has been used.**




## Architecture

         Browser
            |
            |
    TCP Socket Server(server.py)
          -> Accepts Connections
          -> Spawns thread for clients
          -> Verifies JWT token(using function in auth.py when websocket connection is established.)
            |
            |
    HTTP Layer(http_server.py + http_parser.py)
          -> Parses http request
          -> Serves pages
          -> Return JSON responses
          -> Deals with registration and login
            |
            |----Registration
            |      ->auth.py hashes the password
            |      ->database.py stores the password
            |
            |
            |----Login
            |      -> database.py find the user
            |      -> auth.py verifies the password
            |      -> auth.py generates JWT token
            |
            |
      WebSocket Layer(web_handshake.py + websocket_frames.py)
          -> Performs Handshake
          -> Looks After real time messaging
          -> Broadcasts the message to all the clients
            |
            |
            |
     PostgresSQL(Database.py)
          -> Stores user credentials
          -> Retrieves user credentials for verification
        




## Steps to run
      
1. Clone the repo
2. Install the dependencies
    \```
    pip install -r requirements.txt
    \```
3. create the .env file with your:
    - DB_PASSWORD=your database password
    - JWT_KEY= you JWT secret key
4. Setup the postgresSQL 
    -> Just run the create function in database.py
5. Run Server (python server.py)
6. Open the browser(http://localhost:8000)




## What I learned

- How a TCP server works and low level networking basics behind that.
- The use of HTTP server and parser and how important it is in the world of networking.
- The use of Websocket, how the handshake happens. And how the data is sent as frames through websocket.
- How to decode the websocket frames, and what does each value in encoded frame indicate.
- I got to know a new thing that all static files like html, .js, .css files all need to be served through http server
- Establishing connection with postgresSQL and working with that using python
- Threading and thread safety with locks
- Handling race conditions
- Password hashing with bcrypt
- How browsers communicate with servers.
- Reading and implementing RFC specifications.



## Known Limitations

- The chat history is not stored which can be accessed later.
- There is no support for private messaging.
- No feature for notifications. 
- The time when a particular message was sent cannot be accessed or checked.
- No feature to search message.
- Image and files cannot be shared.
- Token stored in local storage is lost when page is refreshed.
- No chat room or channels.



## Future Improvements

- Include the chat history which can be accessed later.
- Feature to support sending images and files.
- Timestamps for messages.
- Add message search
- Feature to support private messaging.
- Implementing cookies instead of localstorage.
- Deploy on AWS using docker