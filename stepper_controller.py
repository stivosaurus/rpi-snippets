""" stepper_controller.py

Stepper motor controller for Raspberry Pi 
n"""

from multiprocessing import Process, Pipe
import sys
import os
import time
import shlex
import logging
from collections import namedtuple
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

# container for the controllers we create
Control = namedtuple('Control', 'process pipe')

class MotorController(object):
    """Raspberry Pi stepper motor controller.
    language:
    step N  - do N rotation steps
    forward - set rotation direction
    reverse - set rotation direction
    quit    - kill subprocess
    """

    @classmethod
    def Factory(cls,  # class
                name,
                sequence,
                pins,
                pulse_time=0.002,
                wait_time=0.0):
        """Construct a controller and it's pipe"""
        parent_end, child_end = Pipe()
        mc = cls( name, child_end,
                              sequence, pins,
                              pulse_time, wait_time)
        return Control(mc, parent_end)
    
    
    def __init__(self, name, conn, seq, pins, pulse_time=0.002, wait_time=0.0):
        self.name  = name
        self.conn = conn
        self.seq = seq
        self.next = 0
        self.pins = pins
        self.pulse_time = pulse_time # time pins are set high
        self.proc = Process(target=self.run, args=())
        self.proc.start()

        
    def run(self):
        try:
            #logger.debug('in run()')
            runit = True
            while(runit):
                # read a command
                raw_msg = self.conn.recv()
                logger.debug('{} raw msg: {}'.format(self.name, raw_msg))
                msg = shlex.split(raw_msg)
                if msg:
                    logger.debug('%s msg: %s', self.name, msg)
                    if msg[0] == 'quit':
                        break
                    elif msg[0] == 'step':
                        # step() wants a number, not a string
                        self.step( int(msg[1]) )
                    else:
                        logger.info('unrecognized command: {}', msg)
                logger.debug('%s sending done msg', self.name)
                self.conn.send('{} be done'.format(self.name))
        except Exception as ex:
            logger.info('%s Caught exeption: %s', self.name, ex)
            GPIO.cleanup(self.pins)
            raise ex
            sys.exit()


    def step(self, steps, wait_time=0.0):
        """cycle motor steps number of steps"""
        logger.info("%s step %d", self.name, steps)
        if steps < 0:
            direction = -1
            steps = abs(steps)
        else:
            direction = 1
        # for each step, set the pins for the current pattern
        for s in range(steps):
            self.toggle_pins(self.pins,
                             self.next_sequence(direction))
            time.sleep(wait_time)


    def toggle_pins( self, pins, seq):
        """ set pins according to sequence tuple """
        ##print( seq)
        # set pins, wait for pulse time, then clear
        # we assume that setting pins takes negligible amount of time
        for i in zip(pins, seq):
            ##print(i)
            GPIO.output(i[0], i[1])
        #
        time.sleep( self.pulse_time)
        GPIO.output( pins, GPIO.LOW)


    def next_sequence(self, direction):
        """ returns next tuple of values from sequece """
        # bump pointer
        # todo  handle reverse direction
        #print (direction) added the variable direction which hold 1 or -1

        self.next += direction
        if self.next < 0:
            self.next = len(self.seq)-1
        if self.next >= len(self.seq):
            self.next = 0
        seq = self.seq[self.next]
        return seq


    def send(self, msg):
        self.conn.send(msg)






