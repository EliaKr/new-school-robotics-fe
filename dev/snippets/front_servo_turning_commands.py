import RPi.GPIO as GPIO
from time import sleep

servopin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT)

pwm=GPIO.PWM(servopin, 50)
pwm.start(0)

pwm.ChangeDutyCycle(5) # left full position
sleep(1)
pwm.ChangeDutyCycle(6.25) # left soft position
sleep(1)
pwm.ChangeDutyCycle(7.5) # neutral position
sleep(1)
pwm.ChangeDutyCycle(8.75) # right soft position
sleep(1)
pwm.ChangeDutyCycle(10) # right full position
sleep(1)
pwm.ChangeDutyCycle(7.5) # neutral position
sleep(1)

pwm.stop()
GPIO.cleanup()

