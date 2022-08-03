#!/usr/bin/env python3
import serial
if __name__ == '__main__':
    serKierros = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    serKierros.reset_input_buffer()
    serUS = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    serUS.reset_input_buffer()
    while True:
        if serKierros.in_waiting > 0:
            line = serKierros.readline().decode('utf-8').rstrip()

            print(line)

        if serUS.in_waiting > 0:
            line = serUS.readline().decode('utf-8').rstrip()

            print(line)
            