#!/usr/bin/python2

from multiprocessing import Process, Pipe
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
from stepper_controller import MotorController

# stepper sequence exampe.  motor dependent
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

#
# define pins and initialize low
#
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


    def do_exit(self, line):
        """ exit program"""
        return self.do_EOF( line)

    def do_EOF(self, line):
        """Exit program"""
        logger.debug("do EOF")
        print()
        return True # to exit the command interpreter loop

    def do_fwd(self, args):
        """Go forward N steps"""
        global current
        logger.debug("do_fwd() ")
        current.pipe.send('step ' + args)
        print( current.pipe.recv())  # timeout?


    def do_mov(self, args):
        """ move X Y Z  steps """
        """
        for now, we assume controllers are numbered 0, 1, 2
        """
        logger.debug("do mov: " + args)
        try:
            # x_steps, y_steps, z_steps
            steps = [ i for i in shlex.split(args)]
            if len(steps) != 3:
                raise ValueError("wrong number of args")

            # send commands
            for con, st in zip(controls, steps):
                con.pipe.send('step ' + st)

            # wait for returns
            for con in controls:
                print(con.pipe.recv())
        except Exception as ex:
            logger.debug(ex)
        finally:
            return False
        
        
    def do_rev(self, args):
        """NOT IMPLEMENTED"""
        print( ' NOT IMPL rev ' + args)

    def do_list(self, args):
        """ list available controllers"""
        li = [n.process.name for n in controls]
        for i, name in enumerate(li):
            print(i, name)


    def do_use(self, arg):
        """ Use controller N from list"""
        global current
        try:
            val = int(arg)
            if 0 <= val < len(controls):
                current = controls[val]
                prompt.prompt = ('%s > ' ) % current.process.name
                print('using controller %s' % current.process.name)
            else:
                print('bad value for %d' % val)
        except ValueError:
            print('bad arg for use')
            pass
        

    def do_current(self, line):
        """Show name of current controller"""
        global current
        print('current: ', current.process.name)

    def do_quit(self, line):
        """Send 'quit' to current controller"""
        global current
        current.pipe.send('quit')

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
            raise ex
        finally:
            # restore state
            self.lastcmd = ""
            self.use_rawinput = old_use_rawinput
            self.prompt = old_prompt

    def do_inquiry(self, line):
        """ query values from stepper controller"""
        global current

        command = 'inquiry ' + json.dumps({ "cmd":"get",
                                            "args":{'odometer':None,
                                                    'pulse_time':None,
                                                    'step_time':None }
        })
        current.pipe.send(command)

        reply = current.pipe.recv()
        print(reply)




#
# main line
#

if __name__ == '__main__':
    try:
        # set up logging
        logging.basicConfig(filename='stepper.log',
                            level = logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.info("Start: %s", datetime.now() )

        # our process id
        logger.info('main pid: %d ',os.getpid())
        
        # create controllers and add to our list of controls
        #  a control consists of a class ref and a pipe
        controls = []
        controls.append(MotorController.Factory('stepx', SEQ, XPINS))
        controls.append(MotorController.Factory('stepy', SEQ, YPINS))
        controls.append(MotorController.Factory('stepz', SEQ, ZPINS))

        # log controller pids
        for con in controls:
            logger.info('{} pid: {}'.format(con.process.name,
                                            con.process.proc.pid))

        current = controls[0]  # default to first in list

        # create command interpreter
        prompt = Hello()
        
        # put current controller name in prompt
        prompt.prompt = "%s > " % current.process.name

        # run interpreter
        prompt.cmdloop()

    # time to quit
    except KeyboardInterrupt as ex:
        print('Caught exception: %s' % ex)
    finally:
        logger.info('cleanup')
        # stop controller sub process
        for con in controls:
            con.pipe.send('quit')
            
        for con in controls:
            con.process.proc.join()
            GPIO.cleanup()
        logger.info('===== done ====')
