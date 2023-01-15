import network
import socket
import select
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from secret import ssid,password
#secret muotoa:
# ssid = 'nimi'
# password = 'ssid:n salasana'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]    
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    socket1 = socket.socket()
    socket1.bind(address)
    socket1.listen(1)
    return socket1    

def open_poll(socket1):
    #Link socket to poll
    poller = select.poll()
    poller.register(socket1, select.POLLIN)
    return poller

def webpage(temperature):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            <p>Temp is {temperature}</p>
            </body>
            </html>
            """
    return str(html)

def serve(socket1,poller):
    #Start a web server
    #Micropythonissa ei ole metodia socket.fileno()    #fd_to_socket = { socket1.fileno(): socket1,         }
    while True:
         evts = poller.poll(5000)
         for sock, evt in evts:
             # Retrieve the actual socket from its file descriptor          #s = fd_to_socket[fd]
             if evt and select.POLLIN:
                 if sock is socket1:  #Nähtävästi micropython palautta suoraan objektin, ei tarvise verrata file descriptoriin
                     #if sock == socket1.fileno():
                     client = socket1.accept()[0]
                     request = client.recv(1024)
                     request = str(request)
                     #Pyyntö voi olla pitkä, tarkista ekat merkit minkä tyyppinen pyyntö on
                     print(request[0:min([9,len(request)-1])]) 
                     temperature = pico_temp_sensor.temp
                     html = webpage(temperature)
                     client.send(html) #Lähety omaan polliin?
                     client.close()    

try:
    ip = connect()
    socket1 = open_socket(ip)
    poller = open_poll(socket1)
    serve(socket1,poller)
except KeyboardInterrupt:
    machine.reset()  
