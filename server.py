from http_parser import main
from http_server import caller
from web_handshake import handler
from websocket_frames import websocket_frame_loop
from authorisation import verify
import socket
import threading

s_connected=True
clients=[]
client_names={}
clients_lock=threading.Lock()
# Address = socket.getaddrinfo(host=socket.gethostname(), port=8000, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM, proto=0)
Address = socket.getaddrinfo('localhost', port=8000, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM, proto=0)
print(Address)
for family, type, proto, host, sock_addr  in Address:
    print(family, type, proto)
    print(sock_addr[0])
    print(socket.gethostname())
    try:
        sock= socket.socket(int(family), int(type))
        bind=sock.bind(('localhost', 8000))
        # connect=sock.connect(sock_addr) This should not be used in server it is used when client has to be connected to server socket.
        listen=sock.listen(5)

        def broadcast(received, client_socket):
            for client in clients:
                if client != client_socket:
                    client.send(received)

        def serv():
            while True:
                try:
                    new_sock, address = sock.accept()
                    #!!!uncomment the next two lines if there is an issue with keeping it in client thread.
                    # with clients_lock:
                    #     clients.append(new_sock)
                    # new_sock.send("You have been connected to the server.".encode())
                    

                    client_thread=threading.Thread(target=client_thr, args=(new_sock,))

                    client_thread.start()

                except:
                    print("There was an error")

        def client_thr(client_sock):
            while True:

                try:
                    recvd=client_sock.recv(2048)
                    if not recvd:
                        break
                    decoded_data=recvd.decode()
                    input=main(decoded_data)
                    if 'Upgrade' in input['headers']:
                        if '?' not in input['path']:
                            client_sock.send("HTTP/1.1 401 Unauthorized\r\n".encode())
                            break
                        else:
                            token_portion=input['path'].split('?')[1]
                            token=token_portion.split('=', 1)[1]
                            decoded=verify(token)
                            if decoded:
                                client_names[client_sock]=decoded["name"]
                                with clients_lock:
                                    clients.append(client_sock)
                                handler(input, client_sock)
                                websocket_frame_loop(client_names, clients, client_sock, clients_lock)
                            else:
                                client_sock.send("HTTP/1.1 401 Unauthorized\r\n".encode())
                                break

                            #!!!Done
                            # # Need to add the 401 response thing in both the conditions when token is rejected by the server (in the above section where break is there).

                        print(input['headers'])

                    else:
                        response=caller(input)
                        print(repr(response))
                        client_sock.send(response.encode())
                    
                    # broadcast(recvd, client_sock)
                    # broadcasting will come into picture when frames and web things comes this was only for terminal
                    # print(recvd.decode())
                except:
                    print (client_sock, "has been disconnected.")
                    if client_sock in clients:
                        with clients_lock:
                            clients.remove(client_sock)
                    break

        server_thread=threading.Thread(target=serv)

        server_thread.start()

        server_thread.join()

        sock.close()
        break

    except OSError: 
        print("There was an error related to system.")







# while s_connected:
                
            #     inp=input("Enter the message: ")
            #     sent=new_sock.send(inp.encode())
            #     recvd= new_sock.recv(2048)
                
            #     if recvd.decode()=='0':
            #         s_connected=False
            #     else:
            #         print(recvd.decode())



 # recvd=client_sock.recv(2048)

                # if not recvd:
                #     print (client_sock, "has been disconnected.")
                #     clients.remove(client_sock)
                #     client_sock.close()
                #     break
# This is something which will result in error so in order to overcome that we have to use try except otherwise a forceful end to the 
# connection will result in throwing error which has to treated gracefully.
