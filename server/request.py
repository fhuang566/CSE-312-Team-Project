class Request:
    new_line = b'\r\n'
    blank_line = b'\r\n\r\n'
    def __init__(self, http_request, handler):
        if(b'Content-Type: multipart/form-data' in http_request):
            [http_request,self.boundary] = buffer_form(http_request, handler)
        self.received_length = len(http_request)
        [request_line, self.header, self.body] = parse_request(http_request)
        [self.method, self.path, self.version] = request_line.decode().split(' ')

###################################
#  buffer the remain request body.
# 
# ##############       
def buffer_form(http_request, handler):
    length = get_form_length(http_request)
    cur_length = get_current_length(http_request)
    while cur_length < length:
        data = handler.request.recv(1024)
        cur_length += len(data)
        print('receiving:',cur_length, '/', length)        
        http_request += data
    endboundary = http_request[http_request.strip(b'\r\n').rfind(b'\r\n')+len(b'\r\n'): ]
    boundary = endboundary[ : -2]
    return [http_request, boundary]
def parse_request(data: bytes): #assume have data
    request_line = data[0: data.find(Request.new_line)] # http class
    header = data[data.find(Request.new_line)+len(Request.new_line): data.find(Request.blank_line)+len(Request.blank_line)] # http class
    index_before_content = data.find(Request.blank_line)+len(Request.blank_line)
    if data.find(Request.blank_line) == -1:
        body = b''
    else:
        body = data[index_before_content : ]
    return [request_line,header,body]
def get_length(header: bytes):
    index = header.find(b'Content-Length:')+len(b'Content-Length:')
    body = header[index : ]
def get_form_length(header:bytes):
    index = header.find(b'Content-Length:')+len(b'Content-Length:')
    body = header[index : ]
    return int(body[:body.find(Request.new_line)])
def get_current_length(header:bytes):
    index = header.find(Request.blank_line)
    if index == -1:
        return len(Request.blank_line)
    return (len(header) - index -len(Request.blank_line))
