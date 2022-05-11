import RPi.GPIO as GPIO
import time

s2 = 1 # Raspberry Pi Pin 35
s3 = 25 # Raspberry Pi Pin 33
out = 9 # Pin 37
led = 11

NUM_CYCLES = 10

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(out,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(s2,GPIO.OUT)
    GPIO.setup(s3,GPIO.OUT)
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led, GPIO.HIGH)

def read_value(a0, a1):
    GPIO.output(s2, a0)
    GPIO.output(s3, a1)

    # Give the sensor some time to adjust
    time.sleep(0.1)

    # Wait for a full cycle (this will make sure we only count full cycles)
    GPIO.wait_for_edge(out, GPIO.FALLING)
    GPIO.wait_for_edge(out, GPIO.RISING)

    start = time.time()

    GPIO.wait_for_edge(out, GPIO.FALLING)

    # The time that passed while we were waiting
    # for the out to change
    return (time.time() - start) * 1000000

def loop():
    while(True):
      print("r = ", read_value(GPIO.LOW, GPIO.LOW))
      time.sleep(0.1)

      print("g = ", read_value(GPIO.HIGH, GPIO.HIGH))
      time.sleep(0.1)

      print("b = ", read_value(GPIO.LOW, GPIO.HIGH))
      time.sleep(1)

if name=='main':
    setup()

    try:
        loop()
    except KeyboardInterrupt:
        GPIO.output(led, GPIO.LOW)
        GPIO.cleanup()
