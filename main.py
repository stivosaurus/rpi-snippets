#!/usr/bin/python3

from multiprocessing import Process, Queue
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
PINS = [13,15,16,18]
#PINS = [40, 38, 36, 32]
GPIO.setup(PINS,
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
        controls = []   
        # create a controller & its que.  add to our list of controls
        for nam in names:
            que = Queue()
            mc = MotorController( nam, que, SEQ, PINS)
            controls.append(mc)

        # run some commands
        for con in controls:
            con.que.put( con.name) # send controller name. a NOOP cmd
            #time.sleep(1)

        for con in controls:
            con.que.put( 'step 500')  # do some steps
            #time.sleep(1)

        # stop controller sub process
        for con in controls:
            con.que.put('quit')


        # time to quit
    except:
        ex = sys.exc_info()[0]
        print('Exception: %s' % ex)
    finally:
        print('cleanup')
        for c in controls:
            c.proc.join()
            GPIO.cleanup()

    
    







