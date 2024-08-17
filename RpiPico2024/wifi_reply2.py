import socket
import platform
import socket

def get_device_info():
    # Get the hostname and IP address of the device
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address

def respond_to_requests():
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

if __name__ == "__main__":
    respond_to_requests()