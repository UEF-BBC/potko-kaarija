import PCA9685
import socket
from time import sleep

pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = '192.168.1.196'

port = 80

while True:
    # connection to hostname on the port.
    s.connect((host, port))       

    s.send(bytes('Laheta_jotain','UTF-8'))
    # Receive no more than 1024 bytes
    tm = s.recv(1024)                                     

    s.close()

    print(f"{tm}")
      
    print(type(tm))
    
    strhtml = str(tm)
    print(strhtml)
     
    pwm.setServoPulse(0,500)
    sleep(3)
