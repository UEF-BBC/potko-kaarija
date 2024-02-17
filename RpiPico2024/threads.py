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

def webpage(list0, listaverage):
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
            <p>list average is {listaverage}</p>
            <p>List 0 is {list0}</p>
            </body>
            </html>
            """
    return str(html)

# main function to run web server using blocking code
def web_server(ip,axmemory):

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
        axmemnewest=axmemory[-1]
        axmemaverage=sum(axmemory)/len(axmemory)
        lock.release()
        html = webpage(axmemnewest,axmemaverage )
        client.send(html)
        client.close()


# main control loop
def main_loop(axmemory):
    while True:
        ax=round(imu.accel.x,2)

        lock.acquire()
        axmemory.append(ax)
        axmemory.pop(0)
        lock.release()

        ay=round(imu.accel.y,2)
        az=round(imu.accel.z,2)
        gx=round(imu.gyro.x)
        gy=round(imu.gyro.y)
        gz=round(imu.gyro.z)
        inclination=imu.gyro.inclination
        tem=round(imu.temperature,2)
        print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",tem,"Inclination",inclination,"        ",end="\r")
        sleep(1)


#Setup Wifi connection
ip = connect()

axmemory = [0,0,0,0,0]

# run main control loop on second processor
second_thread = _thread.start_new_thread(main_loop, (axmemory,))

# main loop on first processor
# NOTE : webs server doesn't seem to run on second core (???)
try:
    ip = connect()
    s = open_socket(ip)
    web_server(s,axmemory)
except KeyboardInterrupt:
    machine.reset()