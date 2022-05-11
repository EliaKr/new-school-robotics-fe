from TMC_2209.TMC_2209_StepperDriver import *
import time
from time import sleep
import RPi.GPIO as GPIO

GPIO.cleanup()

# initiate the TMC_2209 class
# use your pins for pin_step, pin_dir, pin_en here

servopin = 17
button = 27
state = 1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(19, GPIO.IN)
GPIO.setup(servopin, GPIO.OUT)

pwm=GPIO.PWM(servopin, 50)
pwm.start(0)

def forward():
        tmc.runToPositionSteps(-6000, MovementAbsRel.relative)
        print("Forward")

def backward():
    tmc.runToPositionSteps(6000, MovementAbsRel.relative)
    print("Backward")

def left():
        pwm.ChangeDutyCycle(5.2) # left full position
        state = 2

def center():
        pwm.ChangeDutyCycle(7.5) # neutral position
        state = 1

def right():
        pwm.ChangeDutyCycle(10) # right full position
        state = 3

center()

tmc = TMC_2209(16, 20, 21)

# set whether the movement should be relative or absolute
#tmc.setMovementAbsRel(MovementAbsRel.relative)

# these functions change settings in the TMC register
tmc.setDirection_pin(True)
tmc.setVSense(True)
tmc.setCurrent(500)
tmc.setIScaleAnalog(True)
tmc.setInterpolation(True)
tmc.setSpreadCycle(False)
tmc.setMicrosteppingResolution(8)
tmc.setInternalRSense(False)

#print("---\n---")

# set the Accerleration and maximal Speed
tmc.setAcceleration(16000)
tmc.setMaxSpeed(8000)

#activate motor
tmc.setMotorEnabled(True)

while True:
        if GPIO.input(18) == GPIO.LOW:
                right()
        elif GPIO.input(19) == GPIO.LOW:
                left()
        elif GPIO.input(button) == GPIO.HIGH:
                forward()
                backward()
        else:
                center()

tmc.setMotorEnabled(False)
del tmc
GPIO.cleanup()
