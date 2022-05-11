from TMC_2209.TMC_2209_StepperDriver import *
import time
import RPi.GPIO as GPIO

GPIO.cleanup()

# initiate the TMC_2209 class
# use your pins for pin_step, pin_dir, pin_en here

button = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(19, GPIO.IN)

def forward():
        tmc.runToPositionSteps(6000, MovementAbsRel.relative)
        print("Forward")

def backward():
        tmc.runToPositionSteps(-6000, MovementAbsRel.relative)
        print("Backward")

tmc = TMC_2209(16, 20, 21)

# set whether the movement should be relative or absolute
#tmc.setMovementAbsRel(MovementAbsRel.relative)

# these functions change settings in the TMC register
tmc.setDirection_pin(True)
tmc.setVSense(True)
tmc.setCurrent(400)
tmc.setIScaleAnalog(True)
tmc.setInterpolation(True)
tmc.setSpreadCycle(False)
tmc.setMicrosteppingResolution(8)
tmc.setInternalRSense(False)

#print("---\n---")

# set the Accerleration and maximal Speed
tmc.setAcceleration(16000)
tmc.setMaxSpeed(6000)

#activate motor
tmc.setMotorEnabled(True)

while True:
        if GPIO.input(18) == GPIO.LOW:
                forward()
        if GPIO.input(19) == GPIO.LOW:
                backward()
tmc.setMotorEnabled(False)
del tmc
GPIO.cleanup()
