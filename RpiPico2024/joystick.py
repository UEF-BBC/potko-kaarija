#Demo for Rpi pico joystick
#
#VRy to physical 32 i.e. GP27 i.e. ADC1
#VRx to physical 31 i.e. GP26 i.e. ADC0
#Switch to physical 29 i.e. GP22

from machine import Pin, ADC
import utime

yAxis = ADC(Pin(27))
xAxis = ADC(Pin(26))

button = Pin(29,Pin.IN, Pin.PULL_UP)

while True:
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    buttonValue= button.value()
    print(str(xValue) +", " + str(yValue) + " -- " + str(buttonValue))
    utime.sleep(0.1)
