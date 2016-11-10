""" hello.py
command line interface to stepper_controller
"""

import cmd
import logging
import shlex

logger = logging.getLogger(__name__)

class Hello(cmd.Cmd):
    """ simple command processor """

    def __init__(self):
        super().__init__()
        self.controls = []
        self.current = 0

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
        return self.do_EOF(line)

    def do_EOF(self, line):
        """Exit program"""
        logger.debug("do EOF")
        print()
        return True  # to exit the command interpreter loop

    def do_step(self, args):
        """Mov N steps.  +N is forward, -N is reverse"""
        logger.debug("do_step() ")
        self.current.pipe.send('step ' + args)
        # do we need a status return here?
        # print(self.current.pipe.recv())

    def do_mov(self, args):
        """ move X Y Z  steps """
        """
        for now, we assume controllers are numbered 0, 1, 2
        """
        logger.debug("do mov: " + args)
        try:
            # x_steps, y_steps, z_steps
            steps = [i for i in shlex.split(args)]
            if len(steps) != 3:
                raise ValueError("wrong number of args")

            # send commands
            for con, st in zip(self.controls, steps):
                con.pipe.send('step ' + st)

            # # wait for returns
            # for con in self.controls:
            #     print(con.pipe.recv())
        except Exception as ex:
            logger.debug(ex)
        finally:
            return False

    def do_list(self, args):
        """ list available controllers"""
        ## fixme:  get process name from subprocess
        ## currently changing process name is not supported
        li = [n.process.name for n in self.controls]
        for i, name in enumerate(li):
            print(i, name)

    def do_use(self, arg):
        """ Use controller N from list"""
        try:
            val = int(arg)
            if 0 <= val < len(self.controls):
                self.current = self.controls[val]
                self.prompt = ('%s > ') % self.current.process.name
                print('using controller %s' % self.current.process.name)
            else:
                print('bad value for %d' % val)
        except ValueError:
            print('bad arg for use')
            pass

    def do_current(self, line):
        """Show name of current controller"""
        print('current: ', self.current.process.name)

    def do_quit(self, line):
        """Send 'quit' to current controller"""
        self.current.pipe.send('quit')

    def do_file(self, line):
        """ Read commands from a file instead of keyboard"""


        parsed = shlex.split(line)
        # save state
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

    def do_get(self, line):
        """ get value from controller"""
        self.current.pipe.send('get ' + line)
        # reply
        print(self.current.pipe.recv())

    def do_set(self, line):
        """ set value in controller. set name value"""
        try:
            if len(line.split(' ')) != 2:
                raise ValueError
            self.current.pipe.send('set ' + line)
            print(self.current.pipe.recv())
        except ValueError:
            print('wrong number of args')

    def do_junk(self, line):
        """ send some junk to controller for testing"""
        self.current.pipe.send('foo bar asdfdsf')

