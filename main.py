#!/usr/bin/python2

from multiprocessing import Process, Queue
import sys
import os
import time
import shlex
import cmd
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
YPINS = [29,31,33,37]
ZPINS = [40, 38, 36, 32]
GPIO.setup(XPINS + YPINS + ZPINS,
           GPIO.OUT,
           initial=GPIO.LOW)

# command interpreter class

class Hello(cmd.Cmd):
    """ simple command processor """

    def do_greet(self, line):
        print( 'hello ' + line)

    def do_EOF(self, line):
        print()
        return True

    def do_fwd(self, args):
        global current
        print( 'fwd ' + args)
        current.send('step ' + args)
    
                    

    def do_rev(self, args):
        print( ' NOT IMPL rev ' + args)

    def do_list(self, args):
        print('list')
        li = [n.name for n in controls]
        for i in range(len(li)):
            print(i, li[i])

    def do_use(self, arg):
        global current
        #print('use ' + arg)
        try:
            val = int(arg)
            if 0 <= val < len(controls):
                prompt.prompt = ('using %d > ' ) % val
                current = controls[val]
                print('using ' + current.name)
            else:
                print('bad number')
        except ValueError:
            print('bad arg for use')
            pass

    def do_current(self, line):
        global current
        print('current: ', current.name)

    def do_quit(self, line):
        global current
        current.send('quit')
    
    
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

        # list /dict of controllers
        controls = [] 
        # create a controller & its que.  add to our list of controls
        stepx = MotorController( 'stepx', Queue(), SEQ, XPINS)
        stepy = MotorController( 'stepy', Queue(), SEQ, YPINS)
        stepz = MotorController( 'stepz', Queue(), SEQ, ZPINS)
        controls.append(stepx)
        controls.append(stepy)
        controls.append(stepz)

        current = controls[0] # default to first in list



        # # run some commands
        # for con in controls:
        #     con.send( con.name) # send controller name. a NOOP cmd
        #     #time.sleep(1)

        # for con in controls:
        #     con.send( 'step 5')  # do some steps
        #     #time.sleep(1)


        # stepx.send('step 500')
        # stepy.send('step 600')
        # stepz.send('step 700')



        prompt = Hello()
        prompt.cmdloop()

    # time to quit

    except KeyboardInterrupt as ex:
        print('Caught exception: %s' % ex)
    finally:
        print('cleanup')
        # stop controller sub process
        for con in controls:
            con.send('quit')
            
        for c in controls:
            c.proc.join()
            GPIO.cleanup()

    
    







