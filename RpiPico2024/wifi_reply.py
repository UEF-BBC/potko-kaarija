import network
import socket
import time
import sys
import os
sys.path.append('/home/pi/Desktop')
from secret import secrets 


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


def respond_to_discovery():
    connect_to_wifi(secrets)

    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('', 12345))  # Bind to the same port as the request

    # Get device IP address
    ip_address = network.WLAN(network.STA_IF).ifconfig()[0]
    device_name = 'device_name'  # Set a unique name for this device

    while True:
        data, addr = s.recvfrom(1024)
        if data.decode().startswith('GET_IP:'):
            requested_name = data.decode().split(':')[1]
            if requested_name == device_name:
                response_message = f'{device_name} {ip_address}'
                s.sendto(response_message.encode(), addr)
                print(f'Sent IP address of {device_name} to {addr}')
    
    s.close()

# Run the response function
respond_to_discovery()