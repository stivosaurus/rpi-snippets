""" stepper_controller.py

Stepper motor controller for Raspberry Pi 
n"""

from multiprocessing import Process, Queue
import sys
import os
import time
import shlex
import logging
import RPi.GPIO as GPIO


class MotorController:
    """R-Pi stepper controller.
    language:
    step N  - do N rotation steps
    forward - set rotation direction
    reverse - set rotation direction
    quit    - kill subprocess
    """
    

    def __init__(self, name, msgque, seq, pins):
        self.name  = name
        self.que = msgque
        self.seq = seq
        self.next = 0
        self.pins = pins
        self.pulse_time = 0.001  # time pins are set high
        self.proc = Process(target=self.run, args=())
        self.proc.start()

        
    def run(self):
        try:
            
            runit = True
            while(runit):
                msg = shlex.split(self.que.get())
                if msg:
                    logging.debug('%s msg: %s', self.name, msg)
                    if msg[0] == 'quit':
                        break
                    if msg[0] == 'step':
                        # step() wants a number, not a string
                        self.step( int(msg[1]) )
        except Exception as ex:
            logging.info('Caught exeption: %s', ex)
            GPIO.cleanup(self.pins)
            #raise ex
            sys.exit()


    def step(self, steps, wait_time=0.0):
        """cycle motor steps number of steps"""
        logging.info("%s step %d", self.name, steps)
        # for each step, set the pins for the current pattern
        for s in range(steps):
            self.toggle_pins(self.pins,
                             self.next_sequence())
            time.sleep(wait_time)


    def toggle_pins( self, pins, seq):
        """ set pins according to sequence tuple """
        ##print( seq)
        # set pins for pulse time, then clear
        for i in zip(pins, seq):
            ##print(i)
            GPIO.output(i[0], i[1])
        time.sleep( self.pulse_time)
        GPIO.output( i[0], GPIO.LOW)


    def next_sequence(self):
        """ returns next tuple of values from sequece """
        seq = self.seq[self.next]
        # bump pointer
        # todo  handle reverse direction
        self.next += 1
        if self.next >= len(self.seq):
            self.next = 0
        return seq


    def send(self, msg):
        self.que.put(msg)






