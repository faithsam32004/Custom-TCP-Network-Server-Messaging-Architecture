from database import insert, find, connect
from authorisation import token, Hasher
import json


def status_line(input):
    if input['path']=='/' or input['path']=='/chat' or input['path']=='/registration' or input['path']=='/login':
        status_code=200
        res='OK'
    
    else:
        status_code=404
        res='Not Found'

    return f"HTTP/1.1 {status_code} {res}\r\n"


def response_header(body):
    Content_Type='text/html'
    Content_Length=len(body)

    return f"Content-Type: {Content_Type}\r\nContent-Length: {Content_Length}\r\n"


def assembler(input, body):
    statusLine=status_line(input)
    headers=response_header(body)
    
    return f"{statusLine}{headers}\r\n{body}"

def json_assembler(status, res, dictionary):
    body=json.dumps(dictionary)
    content_type="application/json"
    Content_Length=len(body)
    return f"HTTP/1.1 {status} {res}\r\nContent-Type: {content_type}\r\nContent-Length: {Content_Length}\r\n\r\n{body}"


def caller(input):
    # !!!! there is another way to start on this connection that is by opening one connection in server and using that connection for all the processes 
    # and close that when the server closes. Each server thread has its own connection but the issue with that is it will not well threads. !!!!!\
    
    connection=connect()
    if input['path']=="/login" and input['method']=='GET':

        #body="<html><body><h1>Welcome!</h1></body></html>"
        connection.close()
        body=open('frontend/login.html')
        final_body=body.read()
        body.close()   # we can use with statement to avoid this close at the end.
        return assembler(input, final_body)


    

    # this is final place where i need to implement the same thing as "/" by supplying the main page for chatting.
    elif input['path']=="/chat":
        body="<html><body><h1>Chat Room</h1></body></html>"
        connection.close()
        return assembler(input, body)



    
    
    elif input['path']=="/registration" and input['method']=='POST':

        #cannot use this way because cause http parser returns string not dictionary so have to use json to parse it convert to dict.
        # this is only applicable for body.
        body=json.loads(input['body'])
        name=body['username']
        password=body['password']

        hashed=Hasher(password)
        result=insert(connection, name, hashed)
        if result is None:
            connection.close()
            return json_assembler(200, "OK", {"status": "success"})
        else:
            connection.close()
            return json_assembler(409, "Not Okay", {"status": "failed"})


        # As i implemented the frontend, js is going to work with handling the pages html wont server the content by itself rather it will give status codes, data and such things
        # on the basis of which js will handle the html pages.

        # so we can remove the response and things like that and use the json assembler.


        #response="<html><body><h1>Registration Successful</h1></body></html>"


        # commented these lines cause i implemented the duplicate username check and for that conditions are needed.
        # connection.close()
        # return json_assembler(200, "OK", {"status": "success"})






    # GET path was not included in the beginning  i included it after knowing that we wont get the html page of registration without get directly if we want to to visit through
    # link.

    elif input['path']=='/registration' and input['method']=='GET':
        connection.close()
        body=open('frontend/register.html')
        final_body=body.read()
        body.close()   # we can use with statement to avoid this close at the end.
        return assembler(input, final_body)



    

    elif input['path']=='/chatlogic' and input['method']=='GET':
        connection.close()
        body=open('frontend/chatlogic.html')
        final_body=body.read()
        body.close()   # we can use with statement to avoid this close at the end.
        return assembler(input, final_body)




    

    elif input['path']=="/login" and input['method']=="POST":
        body=json.loads(input['body'])
        name=body['username']
        password=body['password']
        data=find(connection, name, password)
        if data != "NO DATA FOUND":
            tokken=token(data[0], data[1])

            connection.close()

            #commented after front-end
            #return assembler(input, f"<html><body><h1>{tokken}</h1></body></html>")
            return json_assembler(200, "OK", {"token": tokken})
        else:
            connection.close()

            #return assembler(input, "<html><body><h1>login failed</h1></body></html>")
            return json_assembler(401, "Unauthorized", {"status": "failed"})



        
    # !!! IMPORTANT!!!!
    # This is the piece of code which serves the js files according to the requests from browser.
    # A new concept which i learned that when we are dealing with browser apps each and every file has to be shared through server so that it can access it according to the 
    # needs.
    #  
    elif input['path'].endswith('.js'):
            file=input['path'][1:]
            connection.close()
            body=open(f'frontend/{file}')
            final_body=body.read()
            content_Length=len(final_body)
            body.close()   # we can use with statement to avoid this close at the end.
            return f"HTTP/1.1 200 Ok\r\nContent-Type: application/javascript\r\nContent-Length: {content_Length}\r\n\r\n{final_body}"


    
    # !! Same as js files added it when came to know that styles wont be applied until i send the css file as well.
    elif input['path'].endswith('.css'):
        file=input['path'][1:]
        connection.close()
        body=open(f'frontend/{file}')
        final_body=body.read()
        content_Length=len(final_body)
        body.close()
        return f"HTTP/1.1 200 Ok\r\nContent-Type: text/css\r\nContent-Length: {content_Length}\r\n\r\n{final_body}"
        




    else:
        body="<html><body><h1>Not Found</h1></body></html>"
        connection.close()
        return assembler(input, body)


# !!!!!!!!!! IMPORTANT
# Fixed the issues like typos, syntax error with claude.
# One more error which i came to know is the fact that js files need to be served when browser is in the picture cause when browser sees a js file in html and html is served 
# it requests for js file as well. So we need to serve js file as well.



