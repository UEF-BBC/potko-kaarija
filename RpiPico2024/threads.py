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
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    return s

def webpage(Nrot, gyrotime):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>Number of rotations is {Nrot}</p>
            <p>Time in gyroscope is {gyrotime}</p>
            </body>
            </html>
            """
    return str(html)

# main function to run web server using blocking code
def web_server(ip,Nrot_and_time):

    # main web server loop
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = s.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        temperature = pico_temp_sensor.temp
        #html = webpage(temperature, state)
        lock.acquire()
        Nrot=Nrot_and_time[0]
        gyrotime=Nrot_and_time[1]
        lock.release()
        html = webpage(Nrot,gyrotime )
        client.send(html)
        client.close()


# main control loop
def main_loop(Nrot_and_time):
    gr = gyro()
    while True:
        gr.update_gyro()
  
        lock.acquire()
        Nrot_and_time = gr.get_Nrot_and_time()
        lock.release()

        sleep(0.1)


#Setup Wifi connection
ip = connect()

Nrot_and_time = [0,0]

# run main control loop on second processor
second_thread = _thread.start_new_thread(main_loop, (Nrot_and_time,))

# main loop on first processor
# NOTE : webs server doesn't seem to run on second core (???)
try:
    ip = connect()
    s = open_socket(ip)
    web_server(s,Nrot_and_time)
except KeyboardInterrupt:
    machine.reset()