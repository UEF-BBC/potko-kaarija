# client.py  
import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = '192.168.1.196'

port = 80

# connection to hostname on the port.
s.connect((host, port))       

s.send(bytes('Laheta_jotain','UTF-8'))
# Receive no more than 1024 bytes
tm = s.recv(1024)                                     

s.close()

print(f"{tm}")