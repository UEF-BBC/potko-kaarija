#Joystickin tietojen luku
#  https://microcontrollerslab.com/joystick-module-raspberry-pi-pico/.
from machine import Pin, ADC, PWM
from time import sleep



VRX = ADC(Pin(27))
VRY = ADC(Pin(26))
SW = Pin(22,Pin.IN, Pin.PULL_UP)

X = [0]*100
Y = [0]*100

calibrate=False
def calibrate_joystick(calibrate):
    if calibrate:
        for ii in range(100):
            xAxis = VRX.read_u16()
            yAxis = VRY.read_u16()
            X[ii]=xAxis
            Y[ii]=yAxis
            sleep(0.05)
            print("X-axis: " + str(xAxis) + ", Y-axis: " + str(yAxis))
            print(" ")

        middleX = sum(X[0:4])/5
        middleY = sum(Y[0:4])/5
        minX = min(X)
        minY = min(Y)
        maxX = max(X)
        maxY = max(Y)
    else:
        middleX = 32500
        middleY = 32500
        minX = 336
        minY = 336
        maxX = 65535
        maxY = 65535
    calibration = (minX,minY,middleX,middleY,maxX,maxY)
    return calibration
calibration = calibrate_joystick(calibrate)
servo_range = (2000,9000)


print("Middle X,Y: "+str(calibration[2])+","+str(calibration[3]))
print("min X,Y: "+str(calibration[0])+" "+str(calibration[1]))
print("max X,Y: "+str(calibration[4])+" "+str(calibration[5]))


pwm = PWM(Pin(3))
pwm.freq(50)

while True:
    
    xAxis = VRX.read_u16()
    yAxis = VRY.read_u16()
    switch = SW.value()
    
    print("X-axis: " + str(xAxis) + ", Y-axis: " + str(yAxis) + ", Switch " + str(switch))
    if switch == 0:
        print("Push button pressed!")
    print(" ")
    sleep(0.1)
    
    if xAxis>calibration[3]:
        position1 = (xAxis-calibration[3])/calibration[4]+0.5
    else:
        position1 = (xAxis-calibration[0])/calibration[3]*0.5
    
    print(str(position1))
    position = position1*(servo_range[1]-servo_range[0])+servo_range[0]
    print(str(position))
    pwm.duty_u16(int(position))

#    for position in range(1000,9000,50):
#        pwm.duty_u16(position)
#        sleep(0.01)
#    for position in range(9000,1000,-50):
#        pwm.duty_u16(position)
#        sleep(0.01)