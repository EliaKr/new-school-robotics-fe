from TMC_2209.TMC_2209_StepperDriver import *
import time

# initiate the TMC_2209 class
# use your pins for pin_step, pin_dir, pin_en here

tmc = TMC_2209(16, 20, 21)

# set whether the movement should be relative or absolute
tmc.setMovementAbsRel(MovementAbsRel.relative)

# these functions change settings in the TMC register
tmc.setDirection_reg(True)
tmc.setVSense(True)
tmc.setCurrent(300)
tmc.setIScaleAnalog(True)
tmc.setInterpolation(True)
tmc.setSpreadCycle(False)
tmc.setMicrosteppingResolution(16)
tmc.setInternalRSense(False)

print("---\n---")

# set the Accerleration and maximal Speed
tmc.setAcceleration(60000)
tmc.setMaxSpeed(48000)

#activate motor
tmc.setMotorEnabled(True)
