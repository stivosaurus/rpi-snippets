#!/usr/bin/python


#title
__author__ = "Dennis Marney"
__copyright__ = "Copyright 2016, The Stepper Project"
__credits__ = ["Steven Swayney"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dennis Marney"
__email__ = "mworlds@gmail,com"
__status__ = "Proto Type"
__date__ = "9th oct 2016"

#import Libraries
import RPi.GPIO as GPIO
import sys, time

#define the pins
GPIO.setmode(GPIO.BOARD)
# Define GPIO signals to use
# Physical pins 13,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
StepPinX = [13,15,16,18]
StepPinY= [40,38,36,32]
StepPinZ = [29,31,33,37]

#StepPins = [29,31,33,37]
# Set all pins as output
for pin in StepPinX:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
for pin in StepPinY:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
for pin in StepPinZ:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
#so all the pins on that list = low
#SO what we have now is to define the pins in a sequence
def step_x (step):
    if step == 0:
        GPIO.output(13,0)
        GPIO.output(15,0)
        GPIO.output(16,0)
        GPIO.output(18,0)
        
    if step == 1:
        GPIO.output(13,1)
        GPIO.output(15,0)
        GPIO.output(16,0)
        GPIO.output(18,0)
 
    if step == 2:
        GPIO.output(13,1)
        GPIO.output(15,1)
        GPIO.output(16,0)
        GPIO.output(18,0)

    if step == 3:
        GPIO.output(13,0)
        GPIO.output(15,1)
        GPIO.output(16,0)
        GPIO.output(18,0)

    if step == 4:
        GPIO.output(13,0)
        GPIO.output(15,1)
        GPIO.output(16,1)
        GPIO.output(18,0)
        
    if step == 5:
        GPIO.output(13,0)
        GPIO.output(15,0)
        GPIO.output(16,1)
        GPIO.output(18,0)

    if step == 6:
        GPIO.output(13,0)
        GPIO.output(15,0)
        GPIO.output(16,1)
        GPIO.output(18,1)

    if step == 7:
        GPIO.output(13,0)
        GPIO.output(15,0)
        GPIO.output(16,0)
        GPIO.output(18,1)  
        
    if step == 8:
        GPIO.output(13,1)
        GPIO.output(15,0)
        GPIO.output(16,0)
        GPIO.output(18,1)
        
               
def step_y (step):
    if step == 0:
        GPIO.output(32,0)
        GPIO.output(36,0)
        GPIO.output(38,0)
        GPIO.output(40,0)
        
    if step == 1:
        GPIO.output(32,1)
        GPIO.output(36,0)
        GPIO.output(38,0)
        GPIO.output(40,0)
 
    if step == 2:
        GPIO.output(32,1)
        GPIO.output(36,1)
        GPIO.output(38,0)
        GPIO.output(40,0)

    if step == 3:
        GPIO.output(32,0)
        GPIO.output(36,1)
        GPIO.output(38,0)
        GPIO.output(40,0)

    if step == 4:
        GPIO.output(32,0)
        GPIO.output(36,1)
        GPIO.output(38,1)
        GPIO.output(40,0)
        
    if step == 5:
        GPIO.output(32,0)
        GPIO.output(36,0)
        GPIO.output(38,1)
        GPIO.output(40,0)

    if step == 6:
        GPIO.output(32,0)
        GPIO.output(36,0)
        GPIO.output(38,1)
        GPIO.output(40,1)

    if step == 7:
        GPIO.output(32,0)
        GPIO.output(36,0)
        GPIO.output(38,0)
        GPIO.output(40,1)  
        
    if step == 8:
        GPIO.output(32,1)
        GPIO.output(36,0)
        GPIO.output(38,0)
        GPIO.output(40,1) 

def step_z (step):
    if step == 0:
        GPIO.output(29,0)
        GPIO.output(31,0)
        GPIO.output(33,0)
        GPIO.output(37,0)
        
    if step == 1:
        GPIO.output(29,1)
        GPIO.output(31,0)
        GPIO.output(33,0)
        GPIO.output(37,0)
 
    if step == 2:
        GPIO.output(29,1)
        GPIO.output(31,1)
        GPIO.output(33,0)
        GPIO.output(37,0)

    if step == 3:
        GPIO.output(29,0)
        GPIO.output(31,1)
        GPIO.output(33,0)
        GPIO.output(37,0)

    if step == 4:
        GPIO.output(29,0)
        GPIO.output(31,1)
        GPIO.output(33,1)
        GPIO.output(37,0)
        
    if step == 5:
        GPIO.output(29,0)
        GPIO.output(31,0)
        GPIO.output(33,1)
        GPIO.output(37,0)

    if step == 6:
        GPIO.output(29,0)
        GPIO.output(31,0)
        GPIO.output(33,1)
        GPIO.output(37,1)

    if step == 7:
        GPIO.output(29,0)
        GPIO.output(31,0)
        GPIO.output(33,0)
        GPIO.output(37,1)  
        
    if step == 8:
        GPIO.output(29,1)
        GPIO.output(31,0)
        GPIO.output(33,0)
        GPIO.output(37,1) 

def step_x_fast (step):
    if step == 0:
        GPIO.output(13,0)
        GPIO.output(15,0)
        GPIO.output(16,0)
        GPIO.output(18,0)
        
    if step == 1:
        GPIO.output(13,1)
        GPIO.output(15,0)
        GPIO.output(16,0)
        GPIO.output(18,0)
 


    if step == 2:
        GPIO.output(13,0)
        GPIO.output(15,1)
        GPIO.output(16,0)
        GPIO.output(18,0)

        
    if step == 3:
        GPIO.output(13,0)
        GPIO.output(15,0)
        GPIO.output(16,1)
        GPIO.output(18,0)
        
        


    if step == 4:
        GPIO.output(13,0)
        GPIO.output(15,0)
        GPIO.output(16,0)
        GPIO.output(18,1) 




step=0
stepy = 0
stepz = 0
forward_x = 0 #forward_x is the direction and speed of stepper
# 0 =stop 
# 1 =forward_x 8step cycle slow
# 2 =revers 8step cycle slow
# 3 = forward_x fast 4 step cycle +2 added to step
# 4 = forward_x fast 4 step cycle -2 added to step








forward_x = 1
forward_y = 1

forward_z = 1

        
while True:
    if forward_x == 1:
        step=step + 1
        step_x(step)
    if forward_x == 2:
        step=step + 1
        step_x_fast(step)
        if step > 4:
            step = 0
        

        
        step_x(0) 
    if step > 8:
        step = 0
    if step < 0:
        step = 8                  
    print(step)
    print(stepy)   
    print(stepz)
    #Y axis 
    if forward_y == 1:
        stepy=stepy+1
        step_y(stepy)
   
    if stepy > 8:
        stepy = 0 
        #Z axis                  
    if forward_z == 1:
        stepz=stepz+1
        step_z(stepz)
    if forward_z == 2:
        stepz=-1
        step_z(stepz)
    if forward_z == 3:
        step=+2
        step_z(stepz)
    if forward_z == 4:
        stepz=-2
        step_z(stepz)                
    if forward_z== 0:            
        step_z(0) 
    if stepz > 8:
        stepz = 0
    try:
        time.sleep(.001) 
    except KeyboardInterrupt:
        print KeyboardInterrupt, " Clean UP"
        GPIO.cleanup()
        sys.exit()                      
