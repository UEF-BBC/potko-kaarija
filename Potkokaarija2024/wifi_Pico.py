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

def connect_to_wifi():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    available_networks = wlan.scan()

    # Go through the available networks and connect to the first for which SSID and password are defined in secret.py
    ip = 0
    ssidnames = []
    for network_ii in available_networks:
        ssid = network_ii[0].decode()  # Network name (SSID)
        ssidnames.append(ssid)
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
    if ip==0: # No network found
        ssid_secrets = [secretii.ssid for secretii in secrets] 
        print("No known network found")
        raise Exception(f'None of the networks {ssidnames} found in secrets ssid list {ssid_secrets}')
                
    print(f'Connected to network {secretii.ssid} with ip {ip}')
    pico_led.on()
    return ip
    
def get_device_info():
    # Get the hostname and IP address of the device
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address

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

    devices = []
    try:
        while True:
            data, addr = s.recvfrom(1024)
            print(f"Received from {addr}: {data.decode()}")
            hostname_ip = data.decode().split()
            devices.append({"hostname":hostname_ip[0], "ip":addr[0]})
    except OSError as e:
        print("Timeout: No more responses")
    
    s.close()
    return devices

def respond_to_device_query():
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('', 12345))  # Bind to port 12345

    while True:
        data, addr = s.recvfrom(1024)
        if data.decode() == "REQUEST_DEVICE_INFO":
            # Get device info
            hostname, ip_address = get_device_info()

            # Prepare response message
            response_message = f"{hostname} {ip_address}"
            s.sendto(response_message.encode(), addr)
            print(f"Sent response to {addr}: {response_message}")

def get_host_ip(wanted_hostname):
    # Get IP address of the host

    devices = request_device_info() #devices is a list of dictionaries with keys "hostname" and "ip"

    #Check if wanted_hostname is in the list
    host = False
    host_ip = 0
    for device in devices:
        if device["hostname"] == wanted_hostname:
            host = True
            host_ip = device["ip"]
            break
    return host_ip


# Function to send data over HTTP
def send_post_request(url, data):
    try:
        print('Sending POST request to', url)
        print('Sending data ', data)
        response = urequests.post(url, json=data)
        print("sent")
        print('Response status:', response.status_code)
        print('Response text:', response.text)
        response.close()
    except Exception as e:
        print('Error:', e)

if __name__ == "__main__":
    try:
        ip = connect_to_wifi()

        # Get the IP address of the host
        #host = "DESKTOP-4FRRIC4"
        host = "raspberrypi5"
        hostip = get_host_ip(host)
        print(f"Host and IP: {host}, {hostip}")

        # Data to be sent
        data = {'key1': 'value1', 'key2': 'value2'}
    
        url = 'https://httpbin.org/post'
        #send_post_request(url, data)
    
        url = hostip
        url = f"http://{hostip}:5000/echo"
        print(f"URL is {url}")
        print(f"data is {data}")
        send_post_request(url, data)

    
        print("All done")
        #socket1 = open_socket(ip)
        #poller = open_poll(socket1)
        #print("Ennen serveä")
        #serve(socket1,poller)
    except KeyboardInterrupt:
        machine.reset()  