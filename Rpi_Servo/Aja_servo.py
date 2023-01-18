import PCA9685
 
pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)
 
pwm.setServoPulse(0,500) 
 

 