# grovepi_sensors.py
# Names: Peter Connolly and Christopher Kim
# Lab 6 – GrovePi Sensors

import time, sys, os
sys.path.append(os.path.expanduser('~/Dexter/GrovePi/Software/Python'))
import grovepi
from grove_rgb_lcd import *

# Ports
ultrasonic_ranger = 2          # D2
potentiometer = 0              # A0
grovepi.pinMode(potentiometer, "INPUT")

setText("")                    # clear LCD once

while True:
    try:
        # Read sensors
        distance = grovepi.ultrasonicRead(ultrasonic_ranger)   # cm
        threshold = grovepi.analogRead(potentiometer)          # 0–1023

        # Format display lines
        if distance < threshold:
            top = f"{threshold} OBJ PRES"
        else:
            top = f"{threshold} "
        bottom = str(distance)

        # Show values without refresh flicker
        setText_norefresh(top + "\n" + bottom)

        time.sleep(0.2)   # gentle update rate

    except IOError:
        print("Error")
        time.sleep(0.2)
