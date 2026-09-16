import struct


def decoder(frame):
    byte0=frame[0]
    byte1=frame[1]

    # fin=byte0[0]
    # opcode=byte0[-1:-5]

    # mask=byte1[0]
    # payload=byte1[1:]
    # The frames include binary at first but it is hard for us so when we print hex for us just for code and when this is compared to payload which is decimal it converts decimal to binary to compare.
    # The frame contains two separate bytes. We combine them into a
    # 16-bit integer so that it can be compared with the decimal payload value.
    med_byte=struct.pack("!BB", byte0, byte1)
    final_byte=struct.unpack("!H", med_byte)[0]

    fin=final_byte >> 15 & 0x01
    opcode=final_byte >> 8 & 0x0F
    mask= final_byte >> 7 & 0x01 # what this does is that >> places 7 0s in the left and the mask value comes to the right most point then just fetch it
    payload= final_byte & 0x7F # In this case the payload is already 7 in length and placed at the very end so no need to move it just fetch it.
    
    # mask just tells us that whether the payload is masked or not if it is then we fetch the masking key and then use that to 
    # unmask the payload using the formula there in rfc. we basically use XOR to unmask it.
    
    Mask_starting=2

    # if the payload is greater than 125 than the length of the actual payload is stored in the next bytes of the frame
    if opcode==1:
        if payload==126:
            Mask_starting=4
            length= int.from_bytes(frame[2:4], "big")
        elif payload==127:
            Mask_starting=10
            length=int.from_bytes(frame[2:10], "big")
        elif payload<=125:
            length=payload

        Mask_ending=Mask_starting+4
        masking_key=frame[Mask_starting:Mask_ending]

        i=Mask_ending
        j=0

        decoded=[]

        while j<length:
            decoded.append(frame[i]^masking_key[j%4])
            i+=1
            j+=1

        # This way of converting into bytes works for integers, but it does not work for string.
        return bytes(decoded).decode('utf-8')
    else:
        return None


def encoder(input):
    input_bytes= input.encode("utf-8") #this cannot be used to convert integers to bytes for that struct has to be used.

    #what is this whole byte thing about and the numbers like 128, 64, 32 and all? !!!!!VERY IMPORTANT CONCEPT OF MEMORY!!!!!

    # We know the fact that 8 bits are there in one byte and each bit has one number assigned to it which shows us the size and location 
    # of the memory in byte. every letter, number and all has some values so according to those values the bits are filled and if that number
    # cannot fill the bit then that bit cannot be used. And when a particular byte is converted back to its original value the way the bits 
    # in the byte are filled is used to identify that particular value.


    # prompt in google (if i got the string or any input)
    fin=0x80
    opcode=0x1

    fin_opc_raw=0x81
    fin_opc=struct.pack("!B", fin_opc_raw) #
    payload_length=struct.pack("B", len(input_bytes))
    final_data=fin_opc+payload_length+input_bytes

    return final_data


# !!!!! LOCKS ARE NEEDED WHEN THREADS ARE WORKING TO MAKE CHANGES TO SOMETHING LIKE LIST WHICH IS BEING USED BY EACH THREAD. !!!!
# lock was implemented because there was race condition and some messages were not reaching the designated places. Placing the loop outside
# makes sure that list does not get altered before completing the sending of a particular message from a certain member. lock outside makes
# sure that it does not get altered without completing the sending of a specific message.


#!!!!! IMPORTANT THING TO BE KEPT IN MIND.
# the race issue was there when i run it on console without frontend but when i removed the lock and tested it after building the frontend it was working fine.
# but still when multiple threads are dealing with the same list or anything like that it is good to use lock.
def WebframeCaller(client_names, clients, frame, client_socket, clients_lock):
    data_for_server=decoder(frame)
    print(data_for_server)
    if data_for_server!=None:

        #The name which i have added to know who send the data needs encoding as well cause frames are always sent in bytes format nothing can be raw data.
        # We decode the data only because we need to unmask the data cause server cannot send masked data according to rfc.
        # What happens here is basically we get the data send by a user decode it for unmasking, encode it and broadcast the same data to other users.
        data_for_client=encoder(f"{client_names[client_socket]}:{data_for_server}")
        with clients_lock:
            for client in clients:
                if client!= client_socket:
                    try:
                            client.send(data_for_client)
                    except:
                            if client in clients:
                                    clients.remove(client)
    else:
        return "closed"



def websocket_frame_loop(client_names, clients, client_socket, clients_lock):
# The lock which was implemented was something which helped in order to solve a problem which was there because of threading. This helped
# me to get more idea about how race conditions are created in threading and how to solve those issues. 
    while True:
        try:
            web_received=client_socket.recv(2048)
            if web_received:
                connection_indicator=WebframeCaller(client_names, clients, web_received, client_socket, clients_lock)
                if connection_indicator=="closed":
                    with clients_lock:
                        if client_socket in clients:
                                clients.remove(client_socket)
                    break
            else:
                with clients_lock:
                    if client_socket in clients:
                            clients.remove(client_socket)
                break
                
        except Exception as e:
             with clients_lock:
                if client_socket in clients:
                    clients.remove(client_socket)
             print(f"There error is {e}")
             break


        


    






