import PCA9685
 
pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

#500-2500 
pwm.setServoPulse(0,1500) 
pwm.setServoPulse(1,1500) 

 

 