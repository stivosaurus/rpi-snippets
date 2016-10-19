#!/usr/bin/python3

from multiprocessing import Process, Queue
import os
import time
import shlex


# stepper sequence.  motor dependent
SEQ = [(1,0,0,0),
       (0,1,0,0),
       (1,1,0,0),
       (0,0,1,0),
       (1,0,1,0),
       (0,1,1,0),
       (1,1,1,0),
       (1,1,1,1)]

PINS = [13,15,16,18]


class MotorController:
    """R-Pi stepper controller.
    language:
    step N  - do N rotation steps
    quit    - kill subprocess
    """

    def __init__(self, name, msgque):
        self.name  = name
        self.que = msgque
        self.seq = SEQ
        self.next = 0
        self.pins = PINS
        self.proc = Process(target=self.run, args=())
        self.proc.start()

    def run(self):
        runit = True
        while(runit):
            msg = shlex.split(self.que.get())
            if msg:
                print('msg:', msg)
                if msg[0] == 'quit':
                    break
                if msg[0] == 'step':
                    # step() wants a number, not a string
                    self.step( int(msg[1]) )

    def step(self, steps):
        """cycle motor steps number of steps"""
        print("step %d" % steps)
        # for each step, set the pins for the current pattern
        for s in range(steps):
            self.toggle_pins(self.seq[self.next],
                             self.pins)
            # cycle next ptr thru sequence
            self.next += 1
            if self.next >= len(self.seq):
                self.next = 0

    def toggle_pins( self,seq, pins):
        print(seq)
        # todo
        # set pins from sequence
        

def info(title):
    """ display some process info """
    print(title)
    #print('module name:', __name__)
    #print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print


#
# main line
#

if __name__ == '__main__':
    # process id
    print('\t= my pid:%d '% os.getpid())
    print('\t======')

    # names from controllers
    # names = ['stepX', 'stepY', 'stepZ']
    names = ['stepX']

    # list of controllers
    controls = []   
    # create a controller & its que.  add to our list of controls
    for nam in names:
            que = Queue()
            mc = MotorController( nam, que)
            controls.append(mc)

    # run some commands
    for con in controls:
        con.que.put( con.name) # send controller name. a NOOP cmd
    time.sleep(1)

    for con in controls:
        con.que.put( 'step 10')  # do some steps
    time.sleep(1)

    # stop controller sub process
    for con in controls:
        con.que.put('quit')

    
    # time to quit
    for c in controls:
        c.proc.join()







