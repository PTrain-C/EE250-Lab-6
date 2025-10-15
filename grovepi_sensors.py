# grovepi_sensors.py
# Team members: Peter Connolly and Christopher Kim

import sys
sys.path.append('~/Dexter/GrovePi/Software/Python')
import time

# Grove Ultrasonic Ranger connected to digital port 2
ultrasonic_ranger = 2

# Potentiometer (rotary angle sensor) connected to analog port A0
potentiometer = 0
grovepi.pinMode(potentiometer, "INPUT")

# Clear LCD screen before starting main loop
setText("")  # one-time clear; subsequent writes use setText_norefresh

def pad16(s: str) -> str:
    """Return string exactly 16 chars wide to avoid ghosting on norefresh writes."""
    s = s[:16]
    return s + (" " * (16 - len(s)))

while True:
    try:
        # 1) Read distance in centimeters from Ultrasonic Ranger (raw integer)
        dist_cm = grovepi.ultrasonicRead(ultrasonic_ranger)  # returns int distance in cm

        # 2) Read threshold from rotary angle sensor (raw 0..1023)
        thresh = grovepi.analogRead(potentiometer)  # returns int 0..1023

        # 3) Determine presence and format LCD text
        # Top line: "<threshold>[ space][ OBJ PRES]"
        obj_present = dist_cm < thresh
        if obj_present:
            top = f"{thresh} OBJ PRES"
        else:
            top = f"{thresh} "

        # Bottom line: current raw ultrasonic measurement (just the integer)
        bottom = f"{dist_cm}"

        # Pad both lines to 16 characters so old characters don't linger
        top_padded = pad16(top)
        bottom_padded = pad16(bottom)

        # Write without refreshing to prevent blinking
        setText_norefresh(top_padded + "\n" + bottom_padded)

        # Modest polling rate; keeps CPU usage down and LCD steady
        time.sleep(0.2)

    except IOError:
        # Handle I2C or sensor read hiccups without crashing the loop
        print("Error")
        time.sleep(0.2)
