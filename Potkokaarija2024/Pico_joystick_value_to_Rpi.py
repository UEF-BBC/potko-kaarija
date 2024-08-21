#Send value read from joystick to Rpi using POST request
#
#VRy to physical 32 i.e. GP27 i.e. ADC1
#VRx to physical 31 i.e. GP26 i.e. ADC0
#Switch to physical 29 i.e. GP22
#
#To use Pico from VisualstudioCode, install MicroPico extension and start following task: >MicroPico: Configure project

from machine import Pin, ADC
import utime
import wifi_Pico as wifi
from picozero import pico_temp_sensor, pico_led, LED #from https://github.com/RaspberryPiFoundation/picozero
from time import sleep

def indicate_error(flashingdelayinseconds=0.1):
    for ii in range(10):
        pico_led.on()
        sleep(flashingdelayinseconds)
        pico_led.off()
        sleep(flashingdelayinseconds)

yAxis = ADC(Pin(27))
xAxis = ADC(Pin(26))

button = Pin(22,Pin.IN, Pin.PULL_UP)

#Connect to local wifi network
picoip = wifi.connect_to_wifi()
if picoip == 0:
    print("Failed to connect to wifi")
    while True:
        indicate_error()

#Define connection to Rpi which runs servo server
hostname = "raspberrypi5"
hostip = wifi.get_host_ip(hostname)
print(f"Hostname and IP: {hostname}, {hostip}")
if hostip == 0:
    print("Failed to get IP address for the host")
    while True:
        indicate_error(0.15)

#It is decided that the joystick values are sent via POST request to the Rpi on port 5000
url = f"http://{hostip}:5000/echo"
print(f"URL is {url}")

def send_joystick_data(x_value, y_value,buttonValue):
 
    data = {'xValue': x_value, 'yValue': y_value, 'buttonValue': buttonValue}

    payload = {'x': x_value, 'y': y_value}
    headers = {'Content-Type': 'application/json'}

    try:
        wifi.send_post_request(url, data)
    except Exception as e:
        print("Failed to send data:", e)


#Main code

   

#while True:
#    #Read values from joystick
#    xValue = xAxis.read_u16() #values between 0 and 65535
#    yValue = yAxis.read_u16()
#    buttonValue= button.value()
#    print(str(xValue) +", " + str(yValue) + " -- " + str(buttonValue))
#   #Scale from 0-1
#    xValue = xValue/65535
#    yValue = yValue/65535
 

#The following code is for the Pico to send data to Rpi when the button is pressed
button_was_pressed = False
last_x_value = 0
last_y_value = 0
last_change_time = 0
tolerance = 400

while True:
    button_value = button.value()
    
    if not button_was_pressed and button_value == 0:
        # Button is first pressed
        button_was_pressed = True
        last_x_value = xAxis.read_u16()
        last_y_value = yAxis.read_u16()
        last_change_time = utime.ticks_ms()
        
        xValue = current_x_value/65535
        yValue = current_y_value/65535            
        send_joystick_data(xValue, yValue,button_value)
    
    if button_was_pressed:
        current_x_value = xAxis.read_u16()
        current_y_value = yAxis.read_u16()
        
        # Send new data if joystick values have changed
        if abs(current_x_value - last_x_value)>tolerance or abs(current_y_value - last_y_value)>tolerance:
            last_x_value = current_x_value
            last_y_value = current_y_value
            last_change_time = utime.ticks_ms()  # Reset timer because values have changed
            
            xValue = current_x_value/65535
            yValue = current_y_value/65535            
            send_joystick_data(xValue, yValue,button_value)
        
        # Check if joystick values have not changed for 10 seconds
        if utime.ticks_diff(utime.ticks_ms(), last_change_time) > 10000:
            print("No change detected for 20 seconds. Stopping data transmission.")
            button_was_pressed = False

