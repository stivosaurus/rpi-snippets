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
__date__ = "10th oct 2016"

#import Libraries
import RPi.GPIO as GPIO
import sys, time, os, itertools

#define the pins
GPIO.setmode(GPIO.BOARD)
StepPin = [13,15,16,18,40,38,36,32.29,31,33,37]
StepPinX = [13,15,16,18]
StepPinY= [40,38,36,32]
StepPinZ = [29,31,33,37]
step = 0
stepy = 0
pin = 13
#StepPins = [29,31,33,37]
# Set all pins as output
for pin in StepPinY:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
for pin in StepPinX:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)


stepsy = [40,(40,38),38,(38,36),36,(36,32),32,(32,40)]
stepsy = itertools.cycle(iter(stepsy))
stepsyrev = [(40,32),32,(32,36),36,(36,38),38,(38,40),40]
stepsyrev=itertools.cycle(iter(stepsyrev))
stepsx = [13,(13,15),15,(15,16),16,(16,18),18,(18,13)]
stepsx = itertools.cycle(iter(stepsx))
def stepX (): 

    try:
        pin = stepsx.next()
        print(pin)
    except StopIteration:
        pin = stepsx.next()
    GPIO.output(pin,1)
    time.sleep(.003)
    GPIO.output(pin,0)


def stepY ():
    
     
    try:
        pin = stepsy.next()
        print(pin)
    except StopIteration:
        pin = stepsy.next()
    GPIO.output(pin,1)
    time.sleep(.005)
    GPIO.output(pin,0)
def stepYrev(): 
    pin = stepsyrev.next()
    GPIO.output(pin,1)
    time.sleep(.003)
    GPIO.output(pin,0)



while True:
    stepX()

    stepY()
        
    try:
        time.sleep(.003) 
    except KeyboardInterrupt:
        print KeyboardInterrupt, " Clean UP"
        GPIO.cleanup()
        sys.exit()      
    

    
