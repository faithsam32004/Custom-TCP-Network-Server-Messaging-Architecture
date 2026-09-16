



test_request = "GET /chat HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\n\r\n<body>"



def splitHeader(Headers):
    Headers= str.split(Headers, '\r\n', 1)
    return Headers

def splitListHeader(HeaderList):
    Header= str.split(HeaderList, '\r\n')
    return Header

def requestLine(line):
    requestData=str.split(line)
    return requestData

def parseHeaderLine(HeaderLine):
    headerInfo=str.split(HeaderLine, ":",1)
    return headerInfo

def splitBody(body):
    header=str.split(body, '\r\n\r\n', 1)
    return header

def LoopHeaderLine(HeaderLineList):
    result={}
    for i in HeaderLineList:
        temp=parseHeaderLine(i)
        result[temp[0]]=temp[1]

    return result



def main(input):
    final_output={}
    body=splitBody(input)
    headers=splitListHeader(body[0])
    request_line=requestLine(headers[0])
    final_output['method']=request_line[0]
    final_output['path']=request_line[1]
    final_output['version']=request_line[2]

    dictOfHeaders=LoopHeaderLine(headers[1:])

    final_output['headers']=dictOfHeaders
    final_output['body']=body[1]

    return(final_output)
        



