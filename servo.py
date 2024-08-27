from time import sleep
import pigpio

# Set pin and freq
# pigpiod must be running
# Rpi.GPIO doesn't have good PWM, pigpio uses hardware pwm
PIN = 24
pwm = pigpio.pi()
pwm.set_mode(PIN, pigpio.OUTPUT)
pwm.set_PWM_frequency(PIN, 100)

def rotate_90():
    # Rotate to 90 deg
    pwm.set_servo_pulsewidth(PIN, 2500)


def rotate_0():
    # Rotate to 0, 0 for our setup is about 20 deg clockwise
    pwm.set_servo_pulsewidth(PIN, 500)
    

def stop():
    pwm.stop(0)
    GPIO.cleanup() 
   
def set_rotation(n):
    pwm.set_servo_pulsewidth(PIN, n)
