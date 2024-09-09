import socket
import time

# Replace with the IP address of your Raspberry Pi Pico
HOST = '192.168.147.110'  # IP address of the Pico
PORT = 80             # Port number, should match the Pico's server

host = "raspberrypi5"
hostip = wifi.get_host_ip(host)
print(f"Host and IP: {host}, {hostip}")

def receive_gyro_data():
    try:
        # Create a socket and connect to the server (Pico)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Connecting to {HOST}:{PORT}...")
            s.connect((HOST, PORT))
            print("Connected!")

            # Receive data for 20 seconds
            start_time = time.time()
            while time.time() - start_time < 20:
                data = s.recv(1024)  # Receive up to 1024 bytes
                if not data:
                    break
                # Print received gyro data
                print(f"Received: {data.decode()}")
                time.sleep(0.01)  # Wait for the next batch of data

            print("Finished receiving data.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    receive_gyro_data()
