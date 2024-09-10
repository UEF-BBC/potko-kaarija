#Gyroscope server run on Pico that reads data from gyroscope and sends it to the RasPi
import _thread
import utime as time
import socket
from gyro import gyro
import wifi_Pico as wifi


# Shared buffer to store gyroscope data
bufferNrot = []
bufferTime = []
buffer_size = 2
lock = _thread.allocate_lock()


# Initialize the gyro sensor
gyro_sensor = gyro()


# Function to calculate average of the buffer
def calculate_average():
    with lock:
        if len(bufferNrot) == 0:
            return 0
        return sum(bufferNrot) / len(bufferNrot)
    
# Get the newest value from the buffer
def get_newest_value():
    with lock:
        if len(bufferNrot) == 0:
            return 0
        return [bufferNrot[-1],bufferTime[-1]]

# Thread 1: Reading gyro data and updating buffer every 0.1 seconds
def read_gyro_thread():
    print("Start reading gyro data")
    global bufferNrot
    global bufferTime
    while True:
        # Read gyro data
        gyro_sensor.update_gyro()
        gyro_data = gyro_sensor.get_Nrot_and_time()

        # Safely update the buffer using the lock
        with lock:
            if len(bufferNrot) >= buffer_size:
                bufferNrot.pop(0)  # Remove oldest entry
                bufferTime.pop(0)  # Remove oldest entry
            bufferNrot.append(gyro_data[0])
            bufferTime.append(gyro_data[1])
        
        time.sleep(0.1)

# Thread 2: Wi-Fi connection and sending average buffer values
def wifi_server_thread():
    print("Start Wi-Fi server")
    # Initialize Wi-Fi connection and get IP address 
    objwifi = wifi.wifi()
    ip = objwifi.connect_to_wifi()

    #wait that client asks server name and IP and return it. After that the client can start to ask gyro data
    hostname, ip_address = objwifi.get_device_info()
    print(f'Hostname: {hostname}, IP address: {ip_address}')
    objwifi.respond_to_device_query()

    # Set up server socket
    addr_info = socket.getaddrinfo('0.0.0.0', 80)
    addr = addr_info[0][-1]

    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)
    print('Waiting for connection on port 80...')

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f'Client connected from {client_addr}')

        # Keep the connection open and send data for 20 seconds
        end_time = time.time() + 20
        while time.time() < end_time:
            avg_value = get_newest_value()
            response = f'{avg_value}\n'
            
            # Send response to the client
            try:
                client_socket.send(response.encode())
            except OSError:
                break  # Client might disconnect; break the loop
            
            time.sleep(0.1)  # Send data every 0.2 seconds
        
        client_socket.close()



# Start the threads
_thread.start_new_thread(read_gyro_thread, ())
#_thread.start_new_thread(wifi_server_thread, ())

# Main loop can do other things or remain idle
#while True:
#    time.sleep(1)
wifi_server_thread()