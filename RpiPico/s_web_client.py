#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
#host = '127.0.0.1'          # Get local machine name
host = '192.168.1.196'          # Get local machine name
print(f'Host on {host}')
port = 80                # Reserve a port for your service.

s.connect((host, port))
s.send(bytes('testi','UTF-8'))
print(f'{s.recv(1024)}')
s.close()                     # Close the socket when done