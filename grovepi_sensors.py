# grovepi_sensors.py
# Team members: Peter Connolly and Christopher Kim

import sys, os, time

# Ensure GrovePi example paths work even when run via SSH
sys.path.append(os.path.expanduser('~/Dexter/GrovePi/Software/Python'))
sys.path.append(os.path.expanduser('~/Dexter/GrovePi/Software/Python/grove_rgb_lcd'))

import grovepi
from grove_rgb_lcd import *

# -----------------------
# Port configuration
# -----------------------
# Ultrasonic Ranger on digital D2
ultrasonic_ranger = 2

# Rotary Angle Sensor (potentiometer) on analog A0
potentiometer = 0
grovepi.pinMode(potentiometer, "INPUT")

# -----------------------
# Helpers
# -----------------------
def pad16(s):
    """Return a string padded or trimmed to exactly 16 chars for stable norefresh writes."""
    s = str(s)
    if len(s) > 16:
        return s[:16]
    return s + (" " * (16 - len(s)))

# One-time clear, then only use norefresh
setText("")

# Optional: calm the LCD backlight to a neutral white
setRGB(255, 255, 255)

# -----------------------
# Main loop
# -----------------------
while True:
    try:
        # Read raw ultrasonic distance in cm (integer)
        dist_cm = grovepi.ultrasonicRead(ultrasonic_ranger)

        # Read raw threshold from rotary (0..1023)
        thresh = grovepi.analogRead(potentiometer)

        # Determine object presence using raw comparison
        obj_present = dist_cm < thresh

        # Top line: "<thresh> [OBJ PRES]"
        if obj_present:
            top_line = f"{thresh} OBJ PRES"
        else:
            top_line = f"{thresh} "

        # Bottom line: raw ultrasonic value
        bottom_line = f"{dist_cm}"

        # Pad to 16 chars to prevent ghost characters on norefresh writes
        top_line = pad16(top_line)
        bottom_line = pad16(bottom_line)

        # Non-refresh write per lab requirement
        setText_norefresh(top_line + "\n" + bottom_line)

        # Reasonable update rate
        time.sleep(0.2)

    except IOError:
        # Handle transient I2C or sensor hiccups without crashing
        # Keep LCD text as-is; just wait and retry
        time.sleep(0.2)
