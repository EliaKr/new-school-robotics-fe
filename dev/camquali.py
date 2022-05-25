from TMC_2209.TMC_2209_StepperDriver import *
import time
import RPi.GPIO as GPIO
import cv2
import numpy
GPIO.setmode(GPIO.BCM)

# define GPIO pins
lefttrig = 22
leftecho = 4
righttrig = 23
rightecho = 10
fronttrig = 6
frontecho = 13
servo = 17
leftir = 18
rightir = 19
button = 27

# set up GPIO pins
GPIO.setup(lefttrig,GPIO.OUT)
GPIO.setup(leftecho,GPIO.IN)
GPIO.setup(righttrig,GPIO.OUT)
GPIO.setup(rightecho,GPIO.IN)
GPIO.setup(fronttrig,GPIO.OUT)
GPIO.setup(frontecho,GPIO.IN)
GPIO.setup(servo,GPIO.OUT)
GPIO.setup(leftir,GPIO.IN)
GPIO.setup(rightir,GPIO.IN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# OpenCV setup
cam = cv2.VideoCapture(0)

# initiate the TMC_2209 class
# use your pins for pin_step, pin_dir, pin_en here
tmc = TMC_2209(16, 20, 21)

# these functions change settings in the TMC register
tmc.setDirection_reg(True)
tmc.setVSense(True)
tmc.setCurrent(400)
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
    GPIO.output(righttrig, True)
    time.sleep(0.00001)
    GPIO.output(righttrig, False)
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
    while GPIO.input(leftecho)==0:
        pulse_start = time.time()
    while GPIO.input(leftecho)==1:
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
    pwm.ChangeDutyCycle(5) # left full position

def softleft():
    pwm.ChangeDutyCycle(6.5)

def center():
    pwm.ChangeDutyCycle(7.5) # neutral position

def softright():
    pwm.ChangeDutyCycle(8.5)

def right():
    pwm.ChangeDutyCycle(10) # right full position

def forward():
    tmc.runToPositionSteps(6000, MovementAbsRel.relative)

def backward():
    tmc.runToPositionSteps(-6000, MovementAbsRel.relative)

def half_back():
    tmc.runToPositionSteps(3000, MovementAbsRel.relative)

def half_forward():
    tmc.runToPositionSteps(-3000, MovementAbsRel.relative)

# Raspberry Pi Camera resolution 2592x1944
# Main Code
while True:
    if GPIO.input(27) == GPIO.HIGH:
        while True:
            front = frontus()
            if front <= 350 and front >= 81:
                forward()
            elif front < 81:
                right()
                forward()
                center()
            else:
                img = cam.read()
                #crop left wall
                #cropped = img[start_row:end_row, start_col:end_col]
                right_wall = img[0:1944, 0:1000]
                left_wall = img[0:1944, 1592:2592]
                allpixleft = np.sum(left_wall <= 255)
                blackpixleft = np.sum(left_wall < 50)
                percblackleft = (blackpixleft / allpixleft) * 100
                print('Percentage of black pixels at the left side:', percblackleft, "%")
                allpixright = np.sum(right_wall <= 255)
                blackpixright = np.sum(right_wall < 50)
                percblackright = (blackpixright / allpixright) * 100
                print('Percentage of black pixels at the right side:', percblackright, "%")
                
                if percblackleft > 60:
                    right()
                    forward()
                    center()
                elif percblackright > 60:
                    left()
                    forward()
                    center()
                elif percblackleft < percblackright:
                    soft_left()
                    half_forward()
                    center()
                elif percblackleft > percblackright:
                    soft_right()
                    half_forward()
                    center()

#
# if there is a problem with ir use ultrasonic
#

tmc.setMotorEnabled(False)
del tmc
