import tkinter as tk
from motor_controller import StepperController
from multiprocessing import Pipe
from datetime import datetime
import logging
import sys
import os
import RPi.GPIO as GPIO
import string

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
        self.odometerx = tk.StringVar()
        self.odometerx.set('odometer 0')
        self.Xodometer = tk.Label(self.frame, textvariable = self.odometerx)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 10, command = self.new_window)
        self.use0 = tk.Button(self.frame, text = 'LEFT', width = 10, command = self.UseXController, repeatdelay = 500, repeatinterval = 1)
        self.use1 = tk.Button(self.frame, text = 'UP', width = 10, command = self.UseYController, repeatdelay = 500, repeatinterval = 1)
        self.use2 = tk.Button(self.frame, text = 'usez', width = 10, command = self.UseZController, repeatdelay = 500, repeatinterval = 1)
        self.stepRev0 = tk.Button(self.frame, text = 'RIGHT', width = 10, command = self.UseXRevController, repeatdelay = 500, repeatinterval = 1)
        self.stepRev1 = tk.Button(self.frame, text = 'DOWN', width = 10, command = self.UseYRevController, repeatdelay = 500, repeatinterval = 1)
        self.stepRev2 = tk.Button(self.frame, text = 'stepRevz', width = 10, command = self.UseZRevController, repeatdelay = 500, repeatinterval = 1)

        self.odomX = tk.Button(self.frame, text = 'Odometer X', width = 10, command = self.OdomXController)
        self.odomY = tk.Button(self.frame, text = 'Odometer Y', width = 10, command = self.OdomYController)
        self.odomZ = tk.Button(self.frame, text = 'Odometer Z', width = 10, command = self.OdomZController)

        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 10, command = self.close_windows)
        self.Xodometer.grid(row = 0, column = 2)
        self.odomX.grid(row=0,column=1)
        self.odomY.grid(row=1,column=1)
        self.odomZ.grid(row=2,column=1)
        self.use0.grid(row=3,column=1)
        self.use1.grid(row=4,column=1)
        self.use2.grid(row=5,column=1)
        self.stepRev0.grid(row=3,column=2)
        self.stepRev1.grid(row=4,column=2)
        self.stepRev2.grid(row=5,column=2)
        self.quitButton.grid(row=9,column=1)
        self.button1.grid(row=10,column=1)
        self.frame.grid(row=11,column=1)
    def new_window(self):
        print("new window")
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)


    def close_windows(self):
        self.master.destroy()
        con0.pipe.send('exit')
        con1.pipe.send('exit')
        con2.pipe.send('exit')
        os.system('killall python3')

    def UseXController(self):
        logger.debug("do_stepx() ")
        con0.pipe.send('step 1')
        con0.pipe.send('get odometer 0')
        text = (con0.pipe.recv())
        text = text.strip('odometer: ')
        self.odometerx.set("Odometer: %s"%(text))

    def UseYController(self):
        logger.debug("do_stepy() ")
        con1.pipe.send('step 1')
        con1.pipe.send('get odometer 1')
        print(con1.pipe.recv())  



    def UseZController(self):
        logger.debug("do_stepz() ")
        con2.pipe.send('step 1')
        con2.pipe.send('get odometer 2')
        print(con2.pipe.recv())

    def UseXRevController(self):
        logger.debug("do_stepx() ")
        con0.pipe.send('step -1')
        con0.pipe.send('get odometer 0')
        text = (con0.pipe.recv())
        text = text.strip('odometer: ')
        self.odometerx.set("Odometer: %s"%(text))

    def UseYRevController(self):
        logger.debug("do_stepy() ")
        con1.pipe.send('step -1')
        con1.pipe.send('get odometer 1')
        print(con1.pipe.recv())  


    def UseZRevController(self):
        logger.debug("do_stepz() ")
        con2.pipe.send('step -1')
        con2.pipe.send('get odometer 2')
        print(con2.pipe.recv())

    def OdomXController(self):
        logger.debug("do_stepz() ")
        print('i ranz')
        con0.pipe.send('get odometer 0')


    def OdomYController(self):
        logger.debug("do_stepz() ")
        print('i ranz')
        con1.pipe.send('get odometer 1')
        print(con1.pipe.recv())

    def OdomZController(self):
        logger.debug("do_stepz() ")
        print('i ranz')
        con2.pipe.send('get odometer 2')
        print(con2.pipe.recv()) 

  

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.grid()
        self.frame.grid()
    def close_windows(self):
        self.master.destroy()

def main():
    global con0
    global con1
    global con2
    root = tk.Tk()

    # our process id
    logger.info('main pid: %d ', os.getpid())
            
    con0 = StepperController.Factory('stepx', SEQ, XPINS)
    con1 = StepperController.Factory('stepy', SEQ, YPINS)
    con2 = StepperController.Factory('stepz', SEQ, ZPINS)
    app = Hello(root)
    root.mainloop()

if __name__ == '__main__':
            # set up logging
    logging.basicConfig(filename='controller_menu.log',
                            level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Start: %s", datetime.now())
    main()
