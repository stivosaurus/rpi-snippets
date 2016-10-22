#!/usr/bin/python2

from multiprocessing import Process, Queue
import sys
import os
import time
import shlex
import cmd
import logging
from datetime import datetime

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

# command interpreter class

class Hello(cmd.Cmd):
    """ simple command processor """

    def preloop(self):
        print(
"""
Usage:
 List available controllers with 'list'
 Select a controller with 'use', then send commands.
 ? for help
 CTRL-D or EOF to exit
""")

    def do_greet(self, line):
        print( 'hello ' + line)

    def do_EOF(self, line):
        """Exit program"""
        print()
        return True

    def do_fwd(self, args):
        """Go forward N steps"""
        global current
        current.send('step ' + args)
    
                    

    def do_rev(self, args):
        """NOT IMPLEMENTED"""
        print( ' NOT IMPL rev ' + args)

    def do_list(self, args):
        """ list available controllers"""
        li = [n.name for n in controls]
        for i in range(len(li)):
            print(i, li[i])

    def do_use(self, arg):
        """ Use controller N from list"""
        global current
        try:
            val = int(arg)
            if 0 <= val < len(controls):
                current = controls[val]
                prompt.prompt = ('%s > ' ) % current.name
                print('using controller %s' % current.name)
            else:
                print('bad value for %d' % val)
        except ValueError:
            print('bad arg for use')
            pass

    def do_current(self, line):
        """Show name of current controller"""
        global current
        print('current: ', current.name)

    def do_quit(self, line):
        """Send 'quit' to current controller"""
        global current
        current.send('quit')
    
    
#
# main line
#

if __name__ == '__main__':
    try:
        # set up logging
        logging.basicConfig(filename='stepper.log',
                            level = logging.DEBUG)
        logging.info("Start: %s", datetime.now() )

        # process id
        logging.info('main pid: %d ',os.getpid())
        
        # create controllers and add to our list of controls
        #  each control has its own msg queue

        controls = []
        stepx = MotorController( 'stepx', Queue(), SEQ, XPINS)
        stepy = MotorController( 'stepy', Queue(), SEQ, YPINS)
        stepz = MotorController( 'stepz', Queue(), SEQ, ZPINS)
        controls.append(stepx)
        controls.append(stepy)
        controls.append(stepz)

        # log controller pids
        for con in controls:
            logging.info('%s pid: %d', con.name, con.proc.pid)
        

        current = controls[0] # default to first in list

        ## send some commands
        # stepx.send('step 500')
        # stepy.send('step 600')
        # stepz.send('step 700')

        # start command interpreter
        prompt = Hello()
        # put current controller name in prompt
        prompt.prompt = "%s > " % current.name
        prompt.cmdloop()

    # time to quit

    except KeyboardInterrupt as ex:
        print('Caught exception: %s' % ex)
    finally:
        logging.info('cleanup')
        # stop controller sub process
        for con in controls:
            con.send('quit')
            
        for con in controls:
            con.proc.join()
            GPIO.cleanup()
        logging.info('===== done ====')
        

    
    







