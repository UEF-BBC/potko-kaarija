import PCA9685
import time
 
pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)
 
pwm.setServoPulse(0,500) 

pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)
while True:
    setServoPulse(2,500)
    setServoPulse(3,1000)
    setServoPulse(4,1500)
    setServoPulse(5,2000)
    setServoPulse(6,2500)

    for i in range(500,2500,10):  
        pwm.setServoPulse(0,i)   
        time.sleep(0.02)     

    for i in range(2500,500,-10):
        pwm.setServoPulse(0,i) 
        time.sleep(0.02)  

#  def setServoPulse(self, channel, pulse):
#    "Sets the Servo Pulse,The PWM frequency must be 50HZ"
#    pulse = pulse*4096/20000        #PWM frequency is 50HZ,the period is 20000us
#    self.setPWM(channel, 0, int(pulse))