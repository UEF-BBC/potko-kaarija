import network
import socket
import time

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Connecting to network...')
        time.sleep(1)
    print('Connected to', ssid)
    print('Network config:', wlan.ifconfig())

def respond_to_discovery():
    connect_to_wifi('YourNetworkSSID', 'YourNetworkPassword')

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