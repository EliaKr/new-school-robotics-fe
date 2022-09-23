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

# Red Mask
lower_red = np.array([0,50,50])
upper_red = np.array([10,255,255])
maskred0 = cv2.inRange(img_hsv, lower_red, upper_red)

lower_red = np.array([170,50,50])
upper_red = np.array([180,255,255])
maskred1 = cv2.inRange(img_hsv, lower_red, upper_red)

maskred = maskred0+maskred1

# Green Mask
lower_green = np.array([65,60,60])
upper_green = np.array([80,255,255])
maskgreen = cv2.inRange(img_hsv, lower_red, upper_red)

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
    pwm.ChangeDutyCycle(7.78) # neutral position

def softright():
    pwm.ChangeDutyCycle(8.5)

def right():
    pwm.ChangeDutyCycle(10) # right full position

def forward():
    tmc.runToPositionSteps(6000, MovementAbsRel.relative)

def fullforward():
    tmc.runToPositionSteps(25500, MovementAbsRel.relative)

def backward():
    tmc.runToPositionSteps(-6000, MovementAbsRel.relative)

def half_back():
    tmc.runToPositionSteps(3000, MovementAbsRel.relative)

def half_forward():
    tmc.runToPositionSteps(-3000, MovementAbsRel.relative)

def checkred():
    success, img = cam.read()
    kernel2 = np.ones((5, 5), np.float32)/25
    img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel2)
    img = cv.Flip(img, flipMode=-1)
    left = img[0:240, 200:600]
    output_img = left.copy()
    output_img[np.where(maskred==0)] = 0
    allpix = np.sum(output_img <= 255)
    blackpix = np.sum(output_img < 35)
    if blackpix < (allpix / 10):
        return(True)
    else:
        return(False)

def checkgreen():
    success, img = cam.read()
    kernel2 = np.ones((5, 5), np.float32)/25
    img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel2)
    img = cv.Flip(img, flipMode=-1)
    right = img[240:480, 200:600]
    output_img = right.copy()
    output_img[np.where(maskgreen==0)] = 0
    allpix = np.sum(output_img <= 255)
    blackpix = np.sum(output_img < 35)
    if blackpix < (allpix / 10):
        return(True)
    else:
        return(False)

# Main Code
while True:
    if GPIO.input(27) == GPIO.HIGH:
        while True:
            front = frontus()
            distright = rightus()
            distleft = leftus()
            if front >= 101 and distright >= 3 and distleft >= 3:
                forward()
                red = checkred()
                green = checkgreen()
                if red = True:
                    right()
                    forward()
                    center()
                elif green = True:
                    left()
                    forward()
                    center()
                else:
                    print("No Obstacles Detected")
            elif distright < 3:
                left()
                forward()
                center()
            elif distleft < 3:
                right()
                forward()
                center()
            else:
                if distright > distleft:
                    right()
                    fullforward()
                    center()
                else:
                    left()
                    fullforward()
                    center()

#
# if there is a problem with ir use ultrasonic
#

tmc.setMotorEnabled(False)
del tmc
