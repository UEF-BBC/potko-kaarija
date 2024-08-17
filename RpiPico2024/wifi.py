#Class for handling wifi connection
import network
import socket
import select
from time import sleep
import time
from picozero import pico_temp_sensor, pico_led, LED #from https://github.com/RaspberryPiFoundation/picozero
import machine
from machine import Pin, I2C
import uasyncio as asyncio
#print(asyncio.__version__)
import urequests
broadcast_port = 12345

#Change this to secret.py when using the code. Format is described in secret_template.py
from secret import secrets 
#secret luokan secrets muotoa:
# secrets[0].ssid = 'nimi'
# secrets[0].password = 'ssid:n salasana'

def connect_to_wifi(secrets):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    available_networks = wlan.scan()

    # Go through the available networks and connect to the first for which SSID and password are defined in secret.py
    ip = 0
    for network_ii in available_networks:
        ssid = network_ii[0].decode()  # Network name (SSID)
        for secretii in secrets:
            if ssid == secretii.ssid:
                wlan.connect(secretii.ssid, secretii.password)
                while not wlan.isconnected():
                    print('Waiting for connection...')
                    pico_led.on()
                    sleep(0.2)
                    pico_led.off()
                    sleep(0.6)
                    
                ip = wlan.ifconfig()[0]
                break
        if ip:
            break
                
    print(f'Connected to network {secretii.ssid} with ip {ip}')
    pico_led.on()
    return ip
    
# Function to send data over HTTP
def send_post_request(url, data):
    try:
        response = urequests.post(url, json=data)
        print('Response status:', response.status_code)
        print('Response text:', response.text)
        response.close()
    except Exception as e:
        print('Error:', e)

      
def request_device_info():

    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Broadcast a message to request device information
    message = "REQUEST_DEVICE_INFO"
    s.sendto(message.encode(), ('255.255.255.255', 12345))
    print("Broadcast request sent")

    # Listen for responses
    s.settimeout(5)  # 5 seconds timeout
    try:
        while True:
            data, addr = s.recvfrom(1024)
            print(f"Received from {addr}: {data.decode()}")
    except OSError as e:
        print("Timeout: No more responses")
    
    s.close()



try:
    ip = connect_to_wifi(secrets)

    # Call the function to start discovering devices
    #Could be made with mDNS (Multicast DNS) but seemed complicated
    #discover_devices(ip)
    request_device_info()

    url = 'https://httpbin.org/post'
    # Data to be sent
    data = {'key1': 'value1', 'key2': 'value2'}
    #send_post_request(url, data)

    print("All done")
    #socket1 = open_socket(ip)
    #poller = open_poll(socket1)
    #print("Ennen serveä")
    #serve(socket1,poller)
except KeyboardInterrupt:
    machine.reset()  