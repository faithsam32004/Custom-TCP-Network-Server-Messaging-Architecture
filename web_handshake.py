import hashlib
import base64




def cal_acceptKey(input):
    input=input+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    hashed=hashlib.sha1(input.encode()).digest() # sha1 does the hashing and digest converts it into a 20 byte binary hash, digest basically gives us the raw hash
    result=base64.b64encode(hashed) #this is used so that we can convert the bytes into printable text which can be sent over http 
    return result


def response(accept_key):
    status_line="101 Switching Protocols"
    upgrade="WebSocket"
    connection="Upgrade"
    key=(accept_key).decode()

    return f"HTTP/1.1 {status_line}\r\nUpgrade: {upgrade}\r\nConnection: {connection}\r\nSec-WebSocket-Accept: {key}\r\n\r\n" 

def handler(input, client_socket):
    data=input['headers']['Sec-WebSocket-Key'].strip()
    acceptKey=cal_acceptKey(data)
    final_response=response(acceptKey)
    client_socket.send(final_response.encode())