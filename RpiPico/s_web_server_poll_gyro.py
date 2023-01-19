import network
import socket
import select
from time import sleep
import time
from picozero import pico_temp_sensor, pico_led, LED
import machine
from machine import Pin, I2C
from imu import MPU6050
from secret import ssid,password
#secret muotoa:
# ssid = 'nimi'
# password = 'ssid:n salasana'
# led = machine.Pin("LED", machine.Pin.OUT)
# led.on()
# sleep(0.2)
# led.off()

class gyro:
    from imu import MPU6050
    buf_len = 10
    bufidx = 0
    buf = [0]*buf_len
    bufx = [0]*buf_len
    bufy = [0]*buf_len
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    imu = MPU6050(i2c)
    Nrot = 0
    rottime = 0
    timezero = time.ticks_ms()
       
    def update_gyro(self):
        self.buf[self.bufidx] = self.imu.gyro.magnitude
        self.bufx[self.bufidx] = self.imu.gyro.x
        self.bufy[self.bufidx] = self.imu.gyro.y
        self.bufidx = self.bufidx + 1
        #Calculate N of rotations
        if self.bufidx > 9:
            self.bufidx = 0
            average = self.buf_average()
            self.Nrot = self.Nrot + average/360*(time.ticks_ms()-self.timezero)/1000
            print("Nrot " + str(self.Nrot) + " average=" + str(average) + "  tick_ms " + str(time.ticks_ms()) + "  " + str(self.timezero) + " " + str((time.ticks_ms()-self.timezero)/1000))
            self.timezero = time.ticks_ms()
        return self
    
    def buf_average(self):
        average = sum(self.buf)/self.buf_len
        return average

    def bufx_average(self):
        average = sum(self.bufx)/self.buf_len
        return average

    def bufy_average(self):
        average = sum(self.bufy)/self.buf_len
        return average

    def get_N_rot(self):
        return self.Nrot

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        pico_led.on()
        sleep(0.2)
        pico_led.off()
        sleep(0.8)
    ip = wlan.ifconfig()[0]    
    print(f'Connected on {ip}')
    pico_led.on()
    sleep(0.2)
    pico_led.off()
    sleep(0.8)
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    socket1 = socket.socket()
    socket1.bind(address)
    socket1.listen(1)
    return socket1    

def open_poll(socket1):
    #Link socket to poll
    poller = select.poll()
    poller.register(socket1, select.POLLIN)
    return poller

def webpage(kierroslkm,kulmanopeus,kulmanopeusx,kulmanopeusy):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            <p>Kierrosten lkm on %{kierroslkm}%</p>
            <p>Kulmanopeus on &{kulmanopeus}&</p>
            <p>Kulmanopeusx on *{kulmanopeusx}*</p>
            <p>Kulmanopeusy on #{kulmanopeusy}#</p>
            <p>Aika on ={time.ticks_ms()/1000}=</p>
            </body>
            </html>
            """
    return str(html)

def serve(socket1,poller):
    #Start a web server
    #Micropythonissa ei ole metodia socket.fileno()    #fd_to_socket = { socket1.fileno(): socket1,         }
    gr = gyro()  #Alusta gyroskooppi

    while True:
         gr = gr.update_gyro() #Mittaa gyro arvot joka kierroksella, jotta kierroslaskuri pysyy mukana ja liukuva keskiarvo pysyy tuoreissa arvoissa
         #print(str(gr.buf_average()) + " While loopin alussa")
         evts = poller.poll(50) #50 ms 
         for sock, evt in evts:
             
             # Retrieve the actual socket from its file descriptor          #s = fd_to_socket[fd]
             if evt and select.POLLIN:
                 if sock is socket1:  #Nähtävästi micropython palautta suoraan objektin, ei tarvise verrata file descriptoriin
                     #if sock == socket1.fileno():
                     client = socket1.accept()[0]
                     request = client.recv(1024)
                     request = str(request)
                     #Pyyntö voi olla pitkä, tarkista ekat merkit minkä tyyppinen pyyntö on
                     print(request[0:min([9,len(request)-1])]) 
                     html = webpage(gr.get_N_rot(),gr.buf_average(),gr.bufx_average(),gr.bufy_average())
                     client.send(html) 
                     client.close()    

try:
    ip = connect()
    socket1 = open_socket(ip)
    poller = open_poll(socket1)
    serve(socket1,poller)
except KeyboardInterrupt:
    machine.reset()  
