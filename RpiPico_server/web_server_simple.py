import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from secret import ssid,password


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
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection    

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

def dataa():
    return str(23.1)

def serve(connection):
    #Start a web server
     while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request[0:min([9,len(request)-1])])
        speed = pico_temp_sensor.temp
        html = webpage(speed)
        client.send(html)
        client.close()    

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()  
