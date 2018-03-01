# -*- coding: utf-8 -*-
import socket
import os
import argparse



# def get_response(request):
     


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
parser = argparse.ArgumentParser()

parser.add_argument("dir", type = str,
                    help="directory")

parser.add_argument("-p","--port", type = int,
                    help="port")
args = parser.parse_args()

#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', args.port or 8080))  #Bind the socket to address
server_socket.listen(1)  #Listen for connections made to the socket. 
                         #The backlog argument specifies the maximum number of queued connections

print 'Started'

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        #Accept a connection. The socket must be bound to an address and listening for connections. The return value is a pair (conn, address) 
        #where conn is a new socket object usable to send and receive data on the connection, 
        #and address is the address bound to the socket on the other end of the connection

        print 'Got new client', client_socket.getsockname()  #Return the socket’s own address. This is useful to find out the port number of an IPv4/v6 socket, for instance.
        request_string = client_socket.recv(2048) 

         #Receive data from the socket. The return value is a string representing the data received

       # client_socket.send(get_response(request_string))  #Send data to the socket. The socket must be connected to a remote socket
       # GET / HTTP/1.1

        if "GET / HTTP/1" in request_string:
            #print "TRUEEEE"
            n = request_string.rindex("User-Agent")
            len_user = len("User-Agent")
            n1 = request_string.find("\n",n)
            user_agent = request_string[n + len_user:n1]

            client_socket.sendall("""HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<title>Hello mister!</title>
</head>
<body>
<p>Hello mister!</p>
<p>You are{}:</p>
</body>
</html>
""".format(user_agent)) 

        elif "GET /media/ HTTP/1" in request_string and not(".txt" in request_string):
            directory = args.dir 
            files = os.listdir(directory) 
            #print(files)

            def f(x):
                return "<li>" + str(x) + "</li>"
            
            files  = map(f,files)
            list_li_html = ""
            for el in files:
                list_li_html += el
            
            request = """HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<title>List of files in /files</title>
</head>
<body>
<p>Files</p>
<ul type ="circle">
{}
</ul>
</body>
</html>
""".format(list_li_html)
            client_socket.sendall(request)
            
        elif "GET /media/" in request_string and ".txt" in request_string:


            directory = args.dir
            dot_pos = request_string.index(".")
            mdia_pos = request_string.index("media")
            full_path = directory + "/" +request_string[mdia_pos + 6:dot_pos] + request_string[dot_pos:dot_pos + 4]
            #print full_path
            if not(os.path.exists(full_path)):
                print("File not found")
                client_socket.sendall("""HTTP/1.0 404 Not Found
                Content-Type: text/html

                    <html>
                    <head>
                    <title>404 Not Found</title>
                    </head>
                    <body>
                    404 Not Found
                    </body>
                    </html>
                    """)
                #server_socket.close()
                #exit()


            files = os.listdir(directory)
            
            for el in files:
                if el in request_string:
                    f = open(directory + "/" + el,'r')
                    content_file = f.read()
                    request = """HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<title>List of files in /files</title>
</head>
<body>
<p>File {0}</p>
<p>{1}</p>
</body>
</html>
""".format(el,content_file)
                    client_socket.sendall(request)
                    f.close()
                    break
        elif "GET /test/ HTTP/1" in request_string:
            l =[]
            l = request_string.split("\n")
            def f1(x):
                return "<p>" + x + "</p>"

            l = map(f1,l)
            req_from_file = ''.join(l)

            request = """HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<title>Test /files</title>
</head>
<body>
{}
</body>
</html>""".format(req_from_file)

            client_socket.sendall(request)
        else:
            request = """HTTP/1.0 404 Not found
Content-Type: text/html

<html>
<head>

</head>
<body>
Page not found
</body>
</html>"""
            client_socket.sendall(request)
                    
    except KeyboardInterrupt:  #If I press Ctrl+C
        print 'Stopped'
        server_socket.close()  #Close the socket. All future operations on the socket object will fail
        exit()
