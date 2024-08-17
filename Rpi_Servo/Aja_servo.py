import PCA9685
import time
 
pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)
 
pwm.setServoPulse(0,500) 

pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(200)
while True:
    # setServoPulse(2,2500)
    for i in range(500,2500,10):  
        pwm.setServoPulse200(0,i)   
        time.sleep(0.02)     

    for i in range(2500,500,-10):
        pwm.setServoPulse200(0,i) 
        time.sleep(0.02)  

#  def setServoPulse(self, channel, pulse):
#    "Sets the Servo Pulse,The PWM frequency must be 50HZ"
#    pulse = pulse*4096/20000        #PWM frequency is 50HZ,the period is 20000us
#    self.setPWM(channel, 0, int(pulse))