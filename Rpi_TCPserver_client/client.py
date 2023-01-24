# client.py  
import socket
from time import sleep
import re

def utf8len(s):
    return len(s.encode('utf-8'))

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = '192.168.1.196'

port = 80


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # connection to hostname on the port.
    s.connect((host, port))

    s.send(bytes('Laheta_jotain','UTF-8'))
    # Receive no more than 1024 bytes
    tm = s.recv(512)                                     

    s.close()

    #Keräile muuttujat stringistä.
    st = str(tm)
    #print(f"{tm}")
    print(f"st stringin koko tavuina {utf8len(st)}")
    #kierrokset %, kulmanopeus &, Kulmanopeus x-akselin ympäri !, Kulmanopeus y-akselin ympäri #, Aika =
    substrings = ("%","&","*","#","=")
    values = [0]*len(substrings)
    if len(st)>30:
        for idx,sub in enumerate(substrings):
            k_1 = st.find(sub)+1
            k_2 = st.find(sub,k_1)
            values[idx] = float(st[k_1:k_2])
            #print(f"{sub} {k_1} ja {k_2} ja {values[idx]}")
    else:
        print(f"st on lyhyt: {st}")

    print(f"N={values[0]},  kulmanopeus={values[1]},  kulmanopeus_y={values[3]},  aika={values[4]}")
    sleep(1)
    