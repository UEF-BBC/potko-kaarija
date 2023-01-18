#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
host = '127.0.0.1'          # Get local machine name
port = 80                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

print('hello')

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print(f'Got connection from {addr}')
   c.send(bytes('Thank you for connecting','UTF-8'))
   c.close()               # Close the connection