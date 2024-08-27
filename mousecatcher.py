import asyncio
import random
import RPi.GPIO as GPIO
import time
import servo
import random
import requests

# Configure sensor input
GPIO.setmode(GPIO.BOARD)
pir = 16
GPIO.setup(pir, GPIO.IN)
print("Waiting for sensor to settle")
time.sleep(1)
# Ensure servo is at 0
servo.rotate_0()
print("Ready!")

# Read/Increment the mouse counter
def increment_counterfile():
    path = "/root/mousecatcher/web/data"
    cur_val = 0
    try:
        with open(path, 'r') as f:
            cur_val = int(f.read())
    except Exception as e:
        print(f"Couldnt get current value,  assuming its 0. {e}")

    try:
        with open(path,  'w') as f:
            new_val = int(cur_val) + 1
            f.write(str(new_val))
    except Exception as e:
        print(f"Couldn't set counter {e}")

# Push alert to kuma
def kuma_push():
    url = "https://kuma.uninspired.dev/api/push/AOdz0TbNqD?status=up&msg=OK&ping="
    requests.get(url)

#Watch the sensor, sleep for half a second, check the sensor. 
#Adjust sensor pots to have proper delays/waits. Currently fully counterclockwise on both
def monitor_sensor():
    while True:
        time.sleep(.5)
        value = GPIO.input(pir)
        # Motion detected
        if value == 1:
            # Wait a random time, let them eat
            sleep_random = random.randrange(2,8)
            print(f"Motion detected! Sleeping for {sleep_random} second to trick the mouse")
            # Detection, so increment counter file
            increment_counterfile()
            # Send alert
            kuma_push()
            # Sleep before rotating servo 90. This lets the lid fall
            time.sleep(sleep_random)
            servo.rotate_90()
            print(f"Sleeping 5 seconds so the lid can settle")
            time.sleep(5)
            print(f"Lid settled, setting latch back")
            servo.rotate_0()


def main():
    monitor_sensor()

# Run the main event loop
asyncio.run(main())
