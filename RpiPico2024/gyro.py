#import select
from utime import sleep
import utime as time
from picozero import pico_temp_sensor, pico_led, LED
import machine
from machine import Pin, I2C
from imu import MPU6050

# Conversion factor for g to m/s²
g_to_m_s2 = 9.80665

class gyro():
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
    velocity = {'x': 0, 'y': 0, 'z': 0}
    # Time management
    prev_time = time.ticks_ms()
    
    def __init__(self):
        print("Gyro initialisoinnissa")
       
    def update_gyro(self):
        self.buf.append(self.imu.gyro.magnitude)
        self.bufx.append(self.imu.gyro.x)
        self.bufy.append(self.imu.gyro.y)
        self.buf.pop(0)
        self.bufx.pop(0)
        self.bufy.pop(0)
        #print("Update gyrossa")
     
        #Calculate N of rotations
        average = self.buf_average()
        self.Nrot = self.Nrot + average/360*(time.ticks_ms()-self.timezero)/1000
        #print("Nrot " + str(self.Nrot) + " average=" + str(average) + "  tick_ms " + str(time.ticks_ms()) + "  " + str(self.timezero) + " " + str((time.ticks_ms()-self.timezero)/1000))
        self.timezero = time.ticks_ms()

        #Calculate velocity. NOTE! Velocity calculation is not very robust and should be improved.
        # Get current time and calculate time delta in seconds
        current_time = time.ticks_ms()
        delta_time = (time.ticks_diff(current_time, self.prev_time)) / 1000.0  # Convert ms to seconds
        self.prev_time = current_time
        accel_data = self.imu.accel.xyz
        #print(f"Acceldata: {accel_data}")
        accel_data_m_s2 = {
        'x': accel_data[0] * g_to_m_s2,
        'y': accel_data[1] * g_to_m_s2,
        'z': accel_data[2] * g_to_m_s2
        }
        # Integrate acceleration to get velocity (v = v0 + a * dt)
        self.velocity['x'] += accel_data_m_s2['x'] * delta_time
        self.velocity['y'] += accel_data_m_s2['y'] * delta_time
        self.velocity['z'] += accel_data_m_s2['z'] * delta_time
        #print(f"deltatime: {delta_time}")

         

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

    def get_Nrot_and_time(self):
        #Returns number of rotations and time in seconds from the generation of the object
        return [self.Nrot,time.ticks_ms()/1000]

    def gyro_test(self):
        try:
            count = 0

            while True:
                #gr = gr.update_gyro() #Mittaa gyro arvot joka kierroksella, jotta kierroslaskuri pysyy mukana ja liukuva keskiarvo pysyy tuoreissa arvoissa
                #print(str(gr.buf_average()) + " While loopin alussa")
                #await asyncio.sleep(0)
                self.update_gyro()
                count = count + 1

                if count % 10 == 0:
                    gyrotulos = self.get_Nrot_and_time() \
                        + [gr.buf_average(),gr.bufx_average(),gr.bufy_average()]
                    print(f"Nrot,timems,bufave,bufxave,bufyave: {gyrotulos}") 
                    print(f"{self.get_Nrot_and_time()}")
                    #print(f"Velocity: {self.velocity['x']}, {self.velocity['y']}, {self.velocity['z']}")
                sleep(0.1)
        
        except KeyboardInterrupt:
            machine.reset()  




if __name__ == "__main__":
    print("Gyro testi")
    gr = gyro()
    gr.gyro_test()
 