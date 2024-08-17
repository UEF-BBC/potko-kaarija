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

      
def request_ip_address(device_name):

    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('', 12345))  # Bind to an arbitrary port

    # Send broadcast request
    request_message = f'GET_IP:{device_name}'
    s.sendto(request_message.encode(), ('255.255.255.255', 12345))
    print(f'Broadcast request for {device_name} sent')

    # Listen for responses
    s.settimeout(3)  # Set timeout for receiving responses
    try:
        while True:
            data, addr = s.recvfrom(1024)
            response = data.decode()
            if response.startswith(device_name):
                print(f'{device_name} IP address is {response.split()[1]}')
                break
    except OSError:
        print('Timeout or other error occurred')
    
    s.close()



try:
    ip = connect_to_wifi(secrets)

    # Call the function to start discovering devices
    #Could be made with mDNS (Multicast DNS) but seemed complicated
    #discover_devices(ip)
    request_ip_address('raspberrypi5')

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