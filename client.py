import socket
import threading

connected=True
lock=threading.Lock()

cl_Address=socket.getaddrinfo('localhost', port=8000)
       

for family, type, proto, host, sock_addr in cl_Address:
    try:
        cl_socket=socket.socket(family, type)
        print(sock_addr)
        # connect=cl_socket.connect((sock_addr))
        connect=cl_socket.connect((sock_addr[0], 8000))

        def rec():
            global connected
            while True:
                with lock:
                    if not connected:
                        break 
                cl_rec=cl_socket.recv(2048)
                
                print("Message Received: ", cl_rec.decode())
                if cl_rec==b'':
                    cl_rec.close()
                    break
                if cl_rec.decode()=="0":
                    with lock:
                        connected=False

        def sen():
            global connected
            while True:
                with lock:
                    if not connected:
                        break

                inp=input("Enter the response: ")
                cl_socket.send(inp.encode())
                
                # cl_socket.close()
                # break

        receive_thread=threading.Thread(target=rec)
        receive_thread.start()

        send_thread=threading.Thread(target=sen)
        send_thread.start()
        
        receive_thread.join()
        send_thread.join()

        cl_socket.close()
        break

    except RuntimeError:
        cl_socket.close()
        # print("There is an error in the client code.")
        break