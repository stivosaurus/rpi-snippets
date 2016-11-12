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
        self.odometery = tk.StringVar()
        self.odometery.set('odometer 0')
        self.Yodometer = tk.Label(self.frame, textvariable = self.odometery)
        self.logo_image = tk.PhotoImage(file='/home/berg/bin/rpi-snippets/Images/python_logo.png')
        self.logo = tk.Label(self.frame, image=self.logo_image)
        self.left_image_up = tk.PhotoImage(file='/home/berg/bin/rpi-snippets/Images/leftup.png')
        self.left_image_down = tk.PhotoImage(file='/home/berg/bin/rpi-snippets/Images/leftdown.png')
        self.right_image_up = tk.PhotoImage(file='/home/berg/bin/rpi-snippets/Images/rightup.png')
        self.right_image_down = tk.PhotoImage(file='/home/berg/bin/rpi-snippets/Images/rightdown.png')
        
        
        self.up_image_up = tk.PhotoImage(file='/home/berg/bin/rpi-snippets/Images/upup.png')
        self.up_image_down = tk.PhotoImage(file='/home/berg/bin/rpi-snippets/Images/leftdown.png')
        self.down_image_up = tk.PhotoImage(file='/home/berg/bin/rpi-snippets/Images/downup.png')
        self.down_image_down = tk.PhotoImage(file='/home/berg/bin/rpi-snippets/Images/downdown.png')
        
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 10, command = self.new_window)
        

        self.LEFT_BUTTON = tk.Button(self.frame, image=self.left_image_up, width = 50, command = self.leftXController, repeatdelay = 500, repeatinterval = 1)
        self.LEFT_BUTTON.bind('<ButtonRelease-1>',self.Left_Motion_up())
        self.LEFT_BUTTON.bind('<Button-1>',self.Left_Motion_down())

        self.RIGHT_BUTTON = tk.Button(self.frame, image = self.right_image_up, width = 50, command = self.rightXController, repeatdelay = 500, repeatinterval = 1)
        self.RIGHT_BUTTON.bind('<ButtonRelease-1>',self.Right_Motion_up())
        self.RIGHT_BUTTON.bind('<Button-1>',self.Right_Motion_down())
        
        self.UP_BUTTON = tk.Button(self.frame, image=self.up_image_up, width = 50, command = self.upYController, repeatdelay = 500, repeatinterval = 1)        
        self.UP_BUTTON.bind('<ButtonRelease-1>',self.Right_Motion_up())
        self.UP_BUTTON.bind('<Button-1>',self.Right_Motion_down())
        
        self.DOWN_BUTTON = tk.Button(self.frame, image=self.down_image_up, width = 50, command = self.downYController, repeatdelay = 500, repeatinterval = 1)
        self.DOWN_BUTTON.bind('<ButtonRelease-1>',self.Right_Motion_up())
        self.DOWN_BUTTON.bind('<Button-1>',self.Right_Motion_down())
        
        self.use2 = tk.Button(self.frame, text = 'usez', width = 10, command = self.UseZController, repeatdelay = 500, repeatinterval = 1)


        
        self.stepRev2 = tk.Button(self.frame, text = 'stepRevz', width = 10, command = self.UseZRevController, repeatdelay = 500, repeatinterval = 1)



        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 10, command = self.close_windows)
        self.logo.grid(row = 1, column = 1, columnspan = 3)
        self.Xodometer.grid(row = 0, column = 1)
        self.Yodometer.grid(row = 0, column = 2)
        
        self.RIGHT_BUTTON.grid(row=3,column=6)
        self.LEFT_BUTTON.grid(row=3,column=4)
        
        self.DOWN_BUTTON.grid(row=4,column=5)
        self.UP_BUTTON.grid(row=2,column=5)
        
        self.use2.grid(row=5,column=1)
        self.stepRev2.grid(row=5,column=2)
        self.quitButton.grid(row=9,column=1)
        self.button1.grid(row=10,column=1)
        self.frame.grid(row=11,column=1)
#left and right button images        
    def Left_Motion_up(self):
        self.LEFT_BUTTON.config(image=self.left_image_up)
        
    def Left_Motion_down(self):
        self.LEFT_BUTTON.config(image=self.left_image_down)
        
    def Right_Motion_up(self):
        self.RIGHT_BUTTON.config(image=self.right_image_up)
        
    def Right_Motion_down(self):
        self.RIGHT_BUTTON.config(image=self.right_image_down)
        
    def Up_Motion_up(self):
        self.LEFT_BUTTON.config(image=self.up_image_up)
        
    def Up_Motion_down(self):
        self.LEFT_BUTTON.config(image=self.up_image_down)
        
    def Down_Motion_up(self):
        self.DOWN_BUTTON.config(image=self.down_image_up)
        
    def Down_Motion_down(self):
        self.DOWN_BUTTON.config(image=self.down_image_down)
        
        
        
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

    def leftXController(self):
        logger.debug("do_stepx() ")
        con0.pipe.send('step -1')
        con0.pipe.send('get odometer 0')
        text = (con0.pipe.recv())
        text = text.strip('odometer: ')
        self.odometerx.set("Odometer: %s"%(text))

    def upYController(self):
        logger.debug("do_stepy() ")
        con1.pipe.send('step 1')
        con1.pipe.send('get odometer 1')
        text = (con1.pipe.recv())
        text = text.strip('odometer: ')
        self.odometery.set("Odometery: %s"%(text))  



    def UseZController(self):
        logger.debug("do_stepz() ")
        con2.pipe.send('step 1')
        con2.pipe.send('get odometer 2')
        print(con2.pipe.recv())

    def rightXController(self):
        logger.debug("do_stepx() ")
        con0.pipe.send('step 1')
        con0.pipe.send('get odometer 0')
        text = (con0.pipe.recv())
        text = text.strip('odometer: ')
        self.odometerx.set("Odometerx: %s"%(text))

    def downYController(self):
        logger.debug("do_stepy() ")
        con1.pipe.send('step -1')
        con1.pipe.send('get odometer 1')
        text = (con1.pipe.recv())
        text = text.strip('odometer: ')
        self.odometery.set("Odometery: %s"%(text))  


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
