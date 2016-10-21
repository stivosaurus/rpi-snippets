#!/usr/bin/python3

from multiprocessing import Process, Queue
import sys
import os
import time
import shlex
import RPi.GPIO as GPIO
from stepper_controller import MotorController


# stepper sequence.  motor dependent
# SEQ = [(1,0,0,0),
#        (0,1,0,0),
#        (1,1,0,0),
#        (0,0,1,0),
#        (1,0,1,0),
#        (0,1,1,0),
#        (1,1,1,0),
#        (0,0,0,1)]

# for Berg's particular stepper

SEQ = [(1,0,0,1),
       (1,0,0,0),
       (1,1,0,0),
       (0,1,0,0),
       (0,1,1,0),
       (0,0,1,0),
       (0,0,1,1),
       (0,0,0,1)]

# define pins and initialize low
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
XPINS = [13,15,16,18]
YPINS = [37,33,31,29]
ZPINS = [32, 36, 38, 40]
GPIO.setup(XPINS + YPINS + ZPINS,
           GPIO.OUT,
           initial=GPIO.LOW)

#
# main line
#

if __name__ == '__main__':
    try:
        # process id
        print('\t= my pid:%d '% os.getpid())
        print('\t======')
        
        # names from controllers
        #   names = ['stepX', 'stepY', 'stepZ']
        names = ['stepX']

        # list of controllers
        # create a controller & its que.  add to our list of controls
        stepx = MotorController( 'stepx', Queue(), SEQ, XPINS)
        stepy = MotorController( 'stepy', Queue(), SEQ, YPINS)
        stepz = MotorController( 'stepz', Queue(), SEQ, ZPINS)
        controls = [stepx, stepy, stepz]

        # run some commands
        for con in controls:
            con.send( con.name) # send controller name. a NOOP cmd
            #time.sleep(1)

        for con in controls:
            con.send( 'step 5')  # do some steps
            #time.sleep(1)


        stepx.send('step 5000')
        stepy.send('step 6000')
        stepz.send('step 7000')

        # stop controller sub process
        for con in controls:
            con.send('quit')

        # time to quit
    except KeyboardInterrupt:
        ex = sys.exc_info()[0]
        print('Exception: %s' % ex)
    finally:
        print('cleanup')
        for c in controls:
            c.proc.join()
            GPIO.cleanup()

    
    







