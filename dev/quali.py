from TMC_2209.TMC_2209_StepperDriver import *
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# define GPIO pins
lefttrig = 22
leftecho = 4
righttrig = 23
rightecho = 10
fronttrig = 6
frontecho = 13
servo = 17

# set up GPIO pins
GPIO.setup(lefttrig,GPIO.OUT)
GPIO.setup(leftecho,GPIO.IN)
GPIO.setup(righttrig,GPIO.OUT)
GPIO.setup(rightecho,GPIO.IN)
GPIO.setup(fronttrig,GPIO.OUT)
GPIO.setup(frontecho,GPIO.IN)
GPIO.setup(servo,GPIO.IN)

# initiate the TMC_2209 class
# use your pins for pin_step, pin_dir, pin_en here
tmc = TMC_2209(16, 20, 21)

# these functions change settings in the TMC register
tmc.setDirection_reg(True)
tmc.setVSense(True)
tmc.setCurrent(300)
tmc.setIScaleAnalog(True)
tmc.setInterpolation(True)
tmc.setSpreadCycle(False)
tmc.setMicrosteppingResolution(16)
tmc.setInternalRSense(False)

tmc.setAcceleration(16000)
tmc.setMaxSpeed(5000)

tmc.setMotorEnabled(True)

# Start Servo
pwm=GPIO.PWM(servo, 50)
pwm.start(0)

# Define Main Functions
def rightus():
    GPIO.output(rightrig, True)
    time.sleep(0.00001)
    GPIO.output(rightrig, False)
    while GPIO.input(rightecho)==0:
        pulse_start = time.time()
    while GPIO.input(rightecho)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return(distance)
    
def leftus():
    GPIO.output(lefttrig, True)
    time.sleep(0.00001)
    GPIO.output(lefttrig, False)
    while GPIO.input(rightecho)==0:
        pulse_start = time.time()
    while GPIO.input(rightecho)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return(distance)
    
def frontus():
    GPIO.output(fronttrig, True)
    time.sleep(0.00001)
    GPIO.output(fronttrig, False)
    while GPIO.input(frontecho)==0:
        pulse_start = time.time()
    while GPIO.input(frontecho)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return(distance)

def left():
    pwm.ChangeDutyCycle(5.5) # left full position

def center():
    pwm.ChangeDutyCycle(7.5) # neutral position
    
def right():
    pwm.ChangeDutyCycle(9.5) # right full position
    
def forward():
    tmc.runToPositionSteps(-6000, MovementAbsRel.relative)
def backward():
    tmc.runToPositionSteps(6000, MovementAbsRel.relative)
    
# Main Code
while True:
    if frontus() >= 40
        while frontus() >= 40:
             forward()
    else:
        if rightus() >= leftus():
            right()
            forward()
        elif leftus() >= rightus():
            left()
            forward()

tmc.setMotorEnabled(False)
del tmc