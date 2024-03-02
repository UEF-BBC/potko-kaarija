# non blocking web server using second core

import utime
import socket
import _thread
import random
import network
from settings import ssid, password
from time import sleep
from picozero import pico_temp_sensor, pico_led
from imu import MPU6050
from time import sleep
import machine
from machine import Pin, I2C
from gyro import gyro
print(f"{ssid}")

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

lock = _thread.allocate_lock()

# connect to WiFi
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
    addr = (ip, 80)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set a timeout in seconds
    #timeout_in_seconds = 2
    #s.settimeout(timeout_in_seconds)
    s.bind(addr)
    s.listen()
    return s

def webpage(Nrot, gyrotime):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <p>Number of rotations is -- {Nrot}</p>
            <p>Time in gyroscope is __ {gyrotime}</p>
            </body>
            </html>
            """
    return str(html)


# main control loop
def gyro_loop(Nrot_and_time):
    gr = gyro()
    while True:
        gr.update_gyro()
        rot_time = gr.get_Nrot_and_time()
        lock.acquire()
        Nrot_and_time[0] = rot_time[0] 
        Nrot_and_time[1] = rot_time[1] 
        print(f"Gyro loop Nrot {Nrot_and_time}")
        lock.release()

        sleep(0.2)

# main function to run web server using blocking code
def web_server(s):

    # run gyro control loop on second processor
    Nrot_and_time = [0.0,0.0]
    _thread.start_new_thread(gyro_loop, (Nrot_and_time,))
    # main web server loop
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while True:
        print("Waiting for a request")
        try:
            client, addr = s.accept()
            print("Received a request")
      
        except Exception as e:
            print("Error processing request:", str(e))
        try:
            #request = client.recv(1024)
            #if not request:
            #    break  # Break the loop if no data is received

            # Decode the received bytes to a string using UTF-8 encoding
            #request_str = request.decode('utf-8')
            #print("Received request:", request_str)

            for x in range(0,100):
                lock.acquire()
                Nrot = Nrot_and_time[0]
                gyrotime = Nrot_and_time[1]
                print(f"Nrot {Nrot} and time {gyrotime}")
                lock.release()

                # Process the request and generate HTML
                #html = webpage(Nrot, gyrotime)
                #client.send(html.encode('utf-8'))

                # Encode the HTML string as bytes before sending
                data_to_send = f"Nrot {Nrot} and time {gyrotime}"
                client.sendall(data_to_send.encode('utf-8'))
                sleep(0.5)


        finally:
            # Reset the timeout to prevent affecting subsequent operations
            #s.settimeout(None)
            # Close the client socket to release resources
            client.close()



#Setup Wifi connection
ip = connect()

led = Pin('LED', Pin.OUT)
for x in range(0,10):
    led.value(not led.value())
    sleep(0.2)


# main loop on first processor
# NOTE : webs server doesn't seem to run on second core (???)
try:
    s = open_socket(ip)
    web_server(s)
except KeyboardInterrupt:
    machine.reset()