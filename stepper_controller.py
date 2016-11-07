""" Stepper_controller.py

Stepper motor controller for Raspberry Pi 
n"""

from multiprocessing import Process, Pipe
from collections import namedtuple
import json
import logging
import os
import RPi.GPIO as GPIO
import shlex
import sys
import time

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
                step_time=0.0):
        """Construct a controller and it's pipe"""
        parent_end, child_end = Pipe()
        mc = cls( name, child_end, sequence, pins, pulse_time,
                  step_time)
        return Control(mc, parent_end)
    
    
    def __init__(self, name, conn, seq, pins,
                 pulse_time=0.002, step_time=0.0):
        self.name  = name
        self.pipe = conn
        self.seq = seq
        self.next = 0
        self.pins = pins
        self.pulse_time = pulse_time # time pins are set high
        self.step_time = step_time   # time between steps
        self.odometer = 0
        self.proc = Process(target=self.run, args=())
        self.proc.start()

    #
    # command parser loop
    #
    def run(self):
        try:
            #logger.debug('in run()')
            runit = True
            while(runit):
                # read a command
                raw_msg = self.pipe.recv()
                logger.debug('{} raw msg: {}'.format(self.name, raw_msg))
                parsed_msg = shlex.split(raw_msg) # [command, arg1, arg2...] 
                logger.debug('{} parsed msg: {}'.format( self.name, parsed_msg))
                #
                if not parsed_msg:
                    continue
                command = parsed_msg[0]
                if command == 'quit':
                    break
                elif command == 'step':
                    # step() wants a number, not a string
                    self.step( int(parsed_msg[1]) )
                # elif command == 'inquiry':
                #     print('doing inquiry')
                #     cmd, payload = raw_msg.split(' ', 1) # split at first blank
                #     self.inquiry(payload)
                elif command == 'get':
                    # get value from controller
                    self.get(parsed_msg)  # [get, var-name]
                else:
                    logger.info('unrecognized command: {}'.format(msg))
                # logger.debug('%s sending done msg', self.name)
                # self.pipe.send('{} done'.format(self.name))
        except Exception as ex:
            logger.info('%s Caught exeption: %s', self.name, ex)
            GPIO.cleanup(self.pins)
            raise ex
            sys.exit()


    def step(self, steps):
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
            time.sleep(self.step_time)

    
    def toggle_pins( self, pins, seq):
        """ set pins according to sequence tuple """
        # set pins, sleep for pulse time, then clear
        # we assume that setting pins takes negligible amount of time
        # fixme: use self.pins instead of arg?
        for i in zip(pins, seq):
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
    
    
    def get(self, parsed_msg):
        """return value of a member variable"""
        name = parsed_msg[1]
        value = getattr(self, name, None)
        reply = '{}: {}'.format(name, value)
        logger.debug(reply)
        self.pipe.send(reply)

    
    # def inquiry(self, payload):
    #     """ return values for variables in payload"""
    #     # payload is json dict in string format with {command:name, args:{}}
    #     # args is a dict with member names as key, None as value
    #     command_args = json.loads(payload)
    #     my_command = command_args['cmd']
    #     my_args = command_args['args']
    #     # lookup attribute in class via getattr. not found is None
    #     for k in my_args.keys():
    #         my_args[k] = getattr(self, k, None)
    #     # reply
    #     self.pipe.send(json.dumps(my_args))
        
    





