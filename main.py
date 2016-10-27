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

    # def __init__(self):
    #     cmd.Cmd.__init__(self)
    

    # printed at start of lopo
    intro = """
Usage:
 List available controllers with 'list'
 Select a controller with 'use', then send commands.
 ? for help
 CTRL-D or EOF to exit
"""

    # def preloop(self):
    #     """stuff done *before* command loops starts """
    #     pass

    # def postcmd(self, stop, line):
    #     """ stuff done after *each* command """
    #     pass



    def do_greet(self, line):
        print( 'hello ' + line)

    def do_EOF(self, line):
        """Exit program"""
        logging.debug("do EOF")
        print()
        return True # to exit the command interpreter loop

    def do_fwd(self, args):
        """Go forward N steps"""
        global current
        current.send('step ' + args)
        print(status_que.get(timeout=10))


    def do_mov(self, args):
        """ move X Y Z  steps """
        """
        for now, we assume controllers are numbered 0, 1, 2
        """
        logging.debug("do mov: " + args)
        try:
            (x_steps, y_steps, z_steps) = [ i for i in shlex.split(args)]
            controls[0].send('step ' + x_steps)
            controls[1].send('step ' + y_steps)
            controls[2].send('step ' + z_steps)
            # wait for returns
            print(status_que.get(timeout=10))
            print(status_que.get(timeout=10))
            print(status_que.get(timeout=10))
            return False
        except Exception as ex:
            logging.debug(ex)
        
        
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

    def do_file(self, line):
        """ Read commands from a file instead of keyboard"""
        global current

        parsed = shlex.split(line)
        #save state
        old_use_rawinput = self.use_rawinput
        old_prompt = self.prompt

        self.useraw_input = False
        self.prompt = ""
        try:
            name = parsed[0]
            print('== executing from: %s' % name)
            with open(name, 'rt') as fi:
                lines = [l.strip() for l in fi.readlines()]
            # for li in lines:
            #     self.onecmd(li)  # execute single command
            # stuff contents of file into command loop
            self.cmdqueue = lines  
        except Exception as ex:
            print(ex)
        
        finally:
            # restore state
            self.lastcmd = ""
            self.use_rawinput = old_use_rawinput
            self.prompt = old_prompt
            #print('== done: %s' % name)



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
        
        # return messages from controllers
        status_que = Queue()
        
        # create controllers and add to our list of controls
        #  each control has its own msg queue

        controls = []
        stepx = MotorController( 'stepx', Queue(), status_que, SEQ, XPINS)
        stepy = MotorController( 'stepy', Queue(), status_que, SEQ, YPINS)
        stepz = MotorController( 'stepz', Queue(), status_que, SEQ, ZPINS)
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
