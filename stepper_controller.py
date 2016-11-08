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
import traceback

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
        mc = cls(name, child_end, sequence, pins, pulse_time,
                 step_time)
        return Control(mc, parent_end)

    def __init__(self, name, conn, seq, pins,
                 pulse_time=0.002, step_time=0.0):
        self.name = name
        self.pipe = conn
        self.seq = seq
        self.next = 0
        self.pins = pins
        self.pulse_time = pulse_time  # time pins are set high
        self.step_time = step_time   # time between steps
        self.odometer = 0
        self.proc = Process(target=self.run, args=())
        self.proc.start()

    #
    # command parser loop
    #
    def run(self):
        try:
            runit = True
            while(runit):
                # read a command. append a space for easier parsing
                raw_msg = self.pipe.recv() + ' '
                cmd, rest = raw_msg.split(' ', 1)  # split off command
                logger.debug('{} msg: {}, {}'.format(self.name,
                                                     cmd, rest))
                try:
                    func = getattr(self, 'do_' + cmd)
                except AttributeError:
                    logger.info('{}: no such command: {}'.format(self.name,
                                                                 cmd))
                else:
                    func(rest)
        except Exception as ex:
            logger.info('%s Caught exeption: %s', self.name, ex)
            traceback.print_exc()
            print()
        finally:
            logger.debug('finally!')
            GPIO.cleanup(self.pins)

    def do_step(self, line):
        """cycle motor steps number of steps.  syntax: step N"""
        steps = int(line)
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
            self.odometer += direction
            time.sleep(float(self.step_time))

    def toggle_pins(self, pins, seq):
        """ set pins according to sequence tuple """
        # set pins, sleep for pulse time, then clear
        # we assume that setting pins takes negligible amount of time
        # fixme: use self.pins instead of arg?
        for i in zip(pins, seq):
            GPIO.output(i[0], i[1])
        #
        time.sleep(float(self.pulse_time))
        GPIO.output(pins, GPIO.LOW)

    def next_sequence(self, direction):
        """ returns next tuple of values from sequece """
        # bump pointer
        # todo  handle reverse direction
        # print (direction) added the variable direction which hold 1 or -1

        self.next += direction
        if self.next < 0:
            self.next = len(self.seq) - 1
        if self.next >= len(self.seq):
            self.next = 0
        seq = self.seq[self.next]
        return seq

    def do_quit(self, line):
        """ we're done! """
        # pin cleanup happens in finally clause of run()
        sys.exit()

    def do_get(self, line):
        """return value of a member variable"""
        name = shlex.split(line)[0]
        value = getattr(self, name, None)
        reply = '{}: {}'.format(name, value)
        logger.debug(reply)
        self.pipe.send(reply)

    def do_set(self, line):
        """ set value in controller. syntax: set name value """
        name, value = line.split()
        logger.debug('{}: {}'.format(name, value))
        try:
            # does it exist? then set it
            getattr(self, name)
            setattr(self, name, value)
            reply = 'OK'
        except AttributeError:
            reply = 'invalid attribute: {}'.format(name)
            logger.debug(reply)
        finally:
            self.pipe.send(reply)
