


# Import required libraries
import sys, os
import time
import RPi.GPIO as GPIO

# Use BOARD GPIO references
# physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Define GPIO signals to use
# Physical pins [13,15,16,18], [29,31,33,37], [40,38,36,32]
#one set for each stepper axis not set to any yet.
# GPIO17,GPIO22,GPIO23,GPIO24
#StepPinsX = [13,15,16,18]
#StepPinsY = [29,31,33,37]
StepPinsZ = [40,38,36,32]
# Set all pins as output
for pin in StepPinsX + StepPinsY + StepPinsZ:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet
#so far sequence is the same for each stepper just the pins change
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]

       
StepCount = len(Seq)
StepDir = 1# Set to 1 or 2 for clockwise
            # Set to -1 or -2 for anti-clockwise

# Read wait time from command line
if len(sys.argv)>1:
  WaitTime = int(sys.argv[1])/float(1000)
else:
  WaitTime = 10/float(1000)

# Initialise variables
StepCounter = 0
StepCount = len(Seq)
# Start main loop
while True:
  c = sys.stdin.read(1)
  print StepCounter,
  print Seq[StepCounter]

  for pin in range(0, 4):
    xpin = StepPins[pin]
    if Seq[StepCounter][pin]!=0:
      print " Enable GPIO %i" %(xpin)
      GPIO.output(xpin, True)
    else:
      GPIO.output(xpin, False)

  StepCounter += StepDir

  # If we reach the end of the sequence
  # start again
  if (StepCounter>=StepCount):
    StepCounter = 0
  if (StepCounter<0):
    StepCounter = StepCount+StepDir
  if ord(c) == 3:
    GPIO.cleanup()
    quit()
  
  # Wait before moving on
  # this is left over exit method i hyave ord() if above 
  #this maybe ok to delete AFTER testing
  try: 
    time.sleep(WaitTime)
    GPIO.output(xpin, False)
  except KeyboardInterrupt:
    print KeyboardInterrupt, " Clean UP"
    GPIO.cleanup()
    sys.exit()
