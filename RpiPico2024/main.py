#Demo for Rpi pico joystick
#
#VRy to physical 32 i.e. GP27 i.e. ADC1
#VRx to physical 31 i.e. GP26 i.e. ADC0
#Switch to physical 29 i.e. GP22

from machine import Pin, ADC
import utime
import wifi

yAxis = ADC(Pin(27))
xAxis = ADC(Pin(26))

button = Pin(22,Pin.IN, Pin.PULL_UP)

ip = wifi.connect_to_wifi()
host = "raspberrypi5"
hostip = wifi.get_host_ip(host)
print(f"Host and IP: {host}, {hostip}")

while True:
    xValue = xAxis.read_u16() #values between 0 and 65535
    yValue = yAxis.read_u16()
    buttonValue= button.value()
    print(str(xValue) +", " + str(yValue) + " -- " + str(buttonValue))
 
   #Scale from 0-1
    xValue = xValue/65535
    yValue = yValue/65535
 
    data = {'xValue': xValue, 'yValue': yValue, 'buttonValue': buttonValue}

     
    url = f"http://{hostip}:5000/echo"
    print(f"URL is {url}")
    print(f"data is {data}")
    wifi.send_post_request(url, data)

    utime.sleep(0.2)

