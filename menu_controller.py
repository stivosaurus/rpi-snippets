import tkinter as tk
from motor_controller import StepperController
from multiprocessing import Pipe
from datetime import datetime
import logging
import sys
import os
import RPi.GPIO as GPIO


con = None
# for Berg's particular stepper
SEQ = [(1, 0, 0, 1),
       (1, 0, 0, 0),
       (1, 1, 0, 0),
       (0, 1, 0, 0),
       (0, 1, 1, 0),
       (0, 0, 1, 0),
       (0, 0, 1, 1),
       (0, 0, 0, 1)]

# define pins and initialize low
#
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
XPINS = [13, 15, 16, 18]
YPINS = [37, 33, 31, 29]
ZPINS = [32, 36, 38, 40]
GPIO.setup(XPINS + YPINS + ZPINS,
           GPIO.OUT,
           initial=GPIO.LOW)

class Hello:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        self.step1 = tk.Button(self.frame, text = 'step1', width = 25, command = self.step_controller('1'))
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.step1.pack()
        self.quitButton.pack()
        self.button1.pack()
        self.frame.pack()
    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)
    def close_windows(self):
        self.master.destroy()
    def step_controller(self, arg):
        logger.debug("do_step() ")
        global con
        con.pipe.send('step 10')
    

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()

def main():
    global con
     
    root = tk.Tk()

    # our process id
    logger.info('main pid: %d ', os.getpid())
            
    con = StepperController.Factory('stepx', SEQ, XPINS)
    app = Hello(root)
    root.mainloop()

if __name__ == '__main__':
            # set up logging
    logging.basicConfig(filename='controller_menu.log',
                            level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Start: %s", datetime.now())
    main()
