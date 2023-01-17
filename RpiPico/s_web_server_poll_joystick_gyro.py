import network
import socket
import select
from time import sleep
import time
from picozero import pico_temp_sensor, pico_led
import machine
from machine import Pin, ADC, I2C
from imu import MPU6050
from secret import ssid,password
#secret muotoa:
# ssid = 'nimi'
# password = 'ssid:n salasana'


class gyro:
    from imu import MPU6050
    buf_len = 10
    bufidx = 0
    buf = [0]*buf_len
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    imu = MPU6050(i2c)
    Nrot = 0
    rottime = 0
    timezero = time.ticks_ms()
       
    def update_gyro(self):
        self.buf[self.bufidx] = self.imu.gyro.magnitude
        self.bufidx = self.bufidx + 1
        #rottime = rottime + 
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
    
    def get_N_rot(self):
        return self.Nrot


class joystick:
    VRX = ADC(Pin(27))
    VRY = ADC(Pin(26))
    SW = Pin(22,Pin.IN, Pin.PULL_UP)
    middleX = 32500
    middleY = 32500
    minX = 336
    minY = 336
    maxX = 65535
    maxY = 65535
    calibration = (minX,minY,middleX,middleY,maxX,maxY)
    xAxis = 0
    yAxis = 0
    switch = 0
    normed_position=0.5
    print("In constructor " +  str(calibration))
    
    def read_value(self):
        self.xAxis = self.VRX.read_u16()
        self.yAxis = self.VRY.read_u16()
        self.switch = self.SW.value()
    
        print("X-axis: " + str(self.xAxis) + ", Y-axis: " + str(self.yAxis) + ", Switch " + str(self.switch))
        if self.switch == 0:
            print("Push button pressed!")
        print(" ")
        
        if self.xAxis>self.calibration[3]:
            print("In position norming " +  str(self.calibration))
            self.normed_position = (self.xAxis-self.calibration[3])/self.calibration[4]+0.5
        else:
            self.normed_position = (self.xAxis-self.calibration[0])/self.calibration[3]*0.5

        self.normed_position = max((0,self.normed_position))
        self.normed_position = min((1,self.normed_position))
        
        return self

    def return_normed_position(self):
        return self.normed_position

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

def webpage(joystickin_asento,kierroslkm,kulmanopeus):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            <p>Joystickin asento on |{joystickin_asento}|</p>
            <p>Kierrosten lkm on %{kierroslkm}%</p>
            <p>Kulmanopeus on &{kulmanopeus}&</p>
            <p>Aika on "{time.ticks_ms()/1000}"</p>
            </body>
            </html>
            """
    return str(html)

def serve(socket1,poller,joystick):
    #Start a web server
    #Micropythonissa ei ole metodia socket.fileno()    #fd_to_socket = { socket1.fileno(): socket1,         }
    gr = gyro()  
    #gr = gr.imu.gyro_range(2)
    #print("Gyro range on " + str(gr.imu.gyro_range()))
    while True:
         gr = gr.update_gyro()
         #print(str(gr.buf_average()) + " True alussa")
         evts = poller.poll(50)
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
                     print(str(joystick.xAxis) + "," + str(joystick.normed_position))
                     #temperature = pico_temp_sensor.temp
                     joystick = joystick.read_value()
                     html = webpage(joystick.return_normed_position(),gr.get_N_rot(),gr.buf_average())
                     client.send(html) #Lähety omaan polliin?
                     client.close()    

try:
    joystick = joystick()
    joystick = joystick.read_value()
    print(joystick.return_normed_position())
    
    ip = connect()
    socket1 = open_socket(ip)
    poller = open_poll(socket1)
    serve(socket1,poller,joystick)
except KeyboardInterrupt:
    machine.reset()  
