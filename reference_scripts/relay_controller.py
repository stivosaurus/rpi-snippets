#!/usr/bin/python
 
 
# Author : Dennis Marney
# Distribution : Raspbian
# Python : 2.7
# GPIO   : RPi.GPIO v3.1.0a
# Version: 0.0.2
#a relay controller from the rasberry pi
 
#include these libs
import RPi.GPIO as GPIO
import os
from time import *
import time
from datetime import datetime
os.system("sudo services lightdm stop") 
#define vairiables and files paths
start=datetime.now()
relay = [37, 35, 33, 31, 40, 29, 38, 36 ]#the relays that control power
#relay = [40, 38 ,36, 32 ]#the relays that control power
inputs =[13, 15, 13] #input pins to handle charger state
relay_start = [800, 730, 800] #relay one start time
relay_end = [1600, 1630, 1600] #relay 1 end time
pause_timer = [0, 0, 0] #relay 1 pause on chargeed
battery_charged = [0, 0, 0] #charger state
delay = [100, 100, 0] 
 
 
#Setting up pin configuration
GPIO.setmode(GPIO.BOARD)
GPIO.setup(inputs, GPIO.IN)
GPIO.setwarnings(False)#re-used pins warning off
GPIO.setup(relay, GPIO.OUT)#setting pin to input [37, 35, 33, 31, 40, 29, 38, 36 ]
GPIO.output(relay, True)#set all relays to off
###########################################################
#so now we make a set of (IF) checks for each relay
#the def relay(): will be set up for each new realy as
#needed with a new call to each in the while loop
#
#
#
#
#
###########################################################
 
 
nowtime = strftime("%H%M", localtime())
 
def relay_control(whichone):
    nowtime = strftime("%H%M", localtime())#setting local time for test
    battery_charged[whichone] = GPIO.input(inputs[whichone])#setting charger 1 condition charged or not
    print "\n\n----------------------------------------------------------------------"
    print "battery stats %i , relay num %i " % (battery_charged[whichone], relay[whichone])#printing charger state 0 = fully charged 1 = charging or off
       
   
    print " relay start time %i  relay end time %i " % (relay_start[whichone], relay_end[whichone])
    print "pause timer = %i The time now is %s" %( pause_timer[whichone], datetime.now())
    if relay_end[whichone] <= int(nowtime) and pause_timer[whichone] > 0:
		pause_timer[whichone] = 0
	
    if relay_start[whichone] <= int(nowtime) and relay_end[whichone] >= int(nowtime) and pause_timer[whichone] <= int(nowtime):
        GPIO.output(relay[whichone], False)
 
        if battery_charged[whichone] == 0: # negative logic # state = 0 is battery charged negative logic
 
            pause_timer[whichone] = int(nowtime) + delay[whichone] #time that charging will resume
            print str(pause_timer[whichone]) + 'test1'
        else:
            pause_timer[whichone] = 0
    else:
        GPIO.output(relay[whichone], True)
        print str(relay[whichone]) + " off"
        print pause_timer[whichone]
 

while True:
    time.sleep(10)
    #relay(relay_1_start, relay_1_end, 35, pause_timer_1) sending to one function????????????????
    #relay(relay_2_start, relay_2_end, 37, pause_timer_2) sending to one function????????????????
    #would it work
 
    relay_control(0)
    relay_control(1)
    relay_control(2)


