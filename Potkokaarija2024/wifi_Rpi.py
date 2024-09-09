import socket
import platform
import socket

def get_device_info():
    # Get the hostname and IP address of the device
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address

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

if __name__ == "__main__":
    respond_to_device_query()