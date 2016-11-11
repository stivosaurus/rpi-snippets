#!/usr/bin/env python3

from multiprocessing import Pipe
import sys
import os
import time
import shlex
import cmd
import logging
import json
from datetime import datetime
from collections import namedtuple

import RPi.GPIO as GPIO
from motor_controller import StepperController
import hello

# stepper sequence example.  motor dependent
# SEQ = [(1,0,0,0),
#        (0,1,0,0),
#        (1,1,0,0),
#        (0,0,1,0),
#        (1,0,1,0),
#        (0,1,1,0),
#        (1,1,1,0),
#        (0,0,0,1)]

# for Berg's particular stepper
SEQ = [(1, 0, 0, 1),
       (1, 0, 0, 0),
       (1, 1, 0, 0),
       (0, 1, 0, 0),
       (0, 1, 1, 0),
       (0, 0, 1, 0),
       (0, 0, 1, 1),
       (0, 0, 0, 1)]


# define pins
# initialization is done in MotorController class
#
XPINS = [13, 15, 16, 18]
YPINS = [37, 33, 31, 29]
ZPINS = [32, 36, 38, 40]

#
# main line
#

if __name__ == '__main__':
    try:
        # set up logging
        logging.basicConfig(filename='stepper.log',
                            level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.info("Start: %s", datetime.now())

        # our process id
        logger.info('main pid: %d ', os.getpid())
        
        # create command interpreter
        prompt = hello.Hello()
        controls = prompt.controls

        # create controllers and add to our list of controls
        #  a control consists of a class ref and a pipe
        controls.append(StepperController.Factory('stepx', SEQ, XPINS))
        controls.append(StepperController.Factory('stepy', SEQ, YPINS))
        controls.append(StepperController.Factory('stepz', SEQ, ZPINS))
        prompt.onecmd('use 0')  # 1st controller is 'current'
        
        # log controller pids
        for con in prompt.controls:
            logger.info('{} pid: {}'.format(con.process.name,
                                            con.process.proc.pid))

        # put current controller name in prompt
        prompt.prompt = "%s > " % controls[0].process.name


        # run interpreter
        prompt.cmdloop()

    # time to quit
    except KeyboardInterrupt as ex:
        print('Caught exception: %s' % ex)
    finally:
        logger.info('cleanup')
        # stop controller sub process
        for con in prompt.controls:
            con.pipe.send('quit')

        for con in prompt.controls:
            con.process.proc.join()
            GPIO.cleanup()
        logger.info('===== done ====')
