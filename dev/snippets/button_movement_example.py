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

def forward():
        tmc.runToPositionSteps(60000, MovementAbsRel.relative)
        print("Forward")

tmc = TMC_2209(16, 20, 21)

# set whether the movement should be relative or absolute
#tmc.setMovementAbsRel(MovementAbsRel.relative)

# these functions change settings in the TMC register
tmc.setDirection_reg(True)
tmc.setVSense(True)
tmc.setCurrent(300)
tmc.setIScaleAnalog(True)
tmc.setInterpolation(True)
tmc.setSpreadCycle(False)
tmc.setMicrosteppingResolution(16)
tmc.setInternalRSense(False)

#print("---\n---")

# set the Accerleration and maximal Speed
tmc.setAcceleration(16000)
tmc.setMaxSpeed(4000)

#activate motor
tmc.setMotorEnabled(True)

while True:
        if GPIO.input(27) == GPIO.HIGH:
                forward()

tmc.setMotorEnabled(False)
del tmc
#GPIO.cleanup()
