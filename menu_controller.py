import tkinter as tk
from motor_controller import StepperController
from multiprocessing import Pipe
from datetime import datetime
import logging
import sys
import os
import RPi.GPIO as GPIO
import string
import inspect
from tkinter import messagebox

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


shape = ''
x=0
y=0
ID = 1
b1 = "up"
xold, yold = None, None
con = None
trace = 0 
Colour = None
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
COUNT = 0
class Hello:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.folderpath = os.getcwd()
        self.Points = []
        self.Made = {}
        self.x =0
        self.y =0
        self.name_object = None
#------------------------------------------------------------#
#screen controlls
#------------------------------------------------------------#
        self.screen = tk.Canvas(self.frame, width = 600, height = 600, bg = 'black', cursor = 'dot', bd = 2)
        #default value for shape change so it dont get an error
        self.optionvar = tk.StringVar()
        self.optionvar = 'red'
        self.myfunc = self.screen.create_oval
        self.object = "Oval"
        self.object_count = 0
        #removed test objects
        '''
        self.screen.create_line(15, 25, 200, 25, fill = 'red')
        self.screen.create_line(300, 35, 300, 200, dash=(4, 2), fill = 'red')
        self.screen.create_line(55, 85, 155, 85, 105, 180, 55, 85, fill = 'red')
        self.screen.create_oval(110, 10, 210, 80, outline="gray", fill = 'red', width=2)
        self.screen.create_rectangle(230, 10, 290, 60, outline="gray", fill = 'red', width=2)
        '''
        
        #mouse events caught on screen
        self.screen.bind('<ButtonPress-1>', self.onStart)  
        self.screen.bind('<B1-Motion>',     self.onGrow)   
        self.screen.bind('<Double-1>',      self.onClear)
        self.screen.bind('<ButtonPress-3>', self.OnSelect)#for the move function
        #------------------------------------------------------------#
        #adding a right mouse action to total canvas/screen
        #------------------------------------------------------------#
        #------------------------------------------------------------#
        #odometer text
        #------------------------------------------------------------#
        self.odometerx = tk.StringVar()
        self.odometerx.set('odometer 0')
        self.Xodometer = tk.Label(self.frame, textvariable = self.odometerx)
        self.odometery = tk.StringVar()
        self.odometery.set('odometer 0')
        self.Yodometer = tk.Label(self.frame, textvariable = self.odometery)
        self.odometerz = tk.StringVar()
        self.odometerz.set('odometer 0')
        self.Zodometer = tk.Label(self.frame, textvariable = self.odometerz)
        #dropdown menu#dropdown menu
        self.object_var = tk.StringVar()
        # Use dictionary to map names to ages.
        self.choices = {'EDIT':''
            
        }
        
        self.editoption = tk.OptionMenu(self.frame, self.object_var, *self.choices)
        self.object_var.set('edit')

        self.editoption.grid(row = 1, column =0)

        #------------------------------------------------------------#
        #set up The images for buttons and logo
        #------------------------------------------------------------#
        self.clear_screen = tk.PhotoImage(file=self.folderpath + '/Images/aussie.png')
        self.logo_image = tk.PhotoImage(file=self.folderpath + '/Images/python_logo.png')
        self.logo = tk.Label(self.frame, image=self.logo_image)
        #FIXME the path to the images needs to be automatic
        #Fixed ^^^^^
        self.left_image_up = tk.PhotoImage(file=self.folderpath + '/Images/leftup.png')
        self.left_image_down = tk.PhotoImage(file=self.folderpath + '/Images/leftdown.png')
        self.right_image_up = tk.PhotoImage(file=self.folderpath + '/Images/rightup.png')
        self.right_image_down = tk.PhotoImage(file=self.folderpath + '/Images/rightdown.png')
        
        
        self.up_image_up = tk.PhotoImage(file=self.folderpath + '/Images/upup.png')
        self.up_image_down = tk.PhotoImage(file=self.folderpath + '/Images/leftdown.png')
        self.down_image_up = tk.PhotoImage(file=self.folderpath + '/Images/downup.png')
        self.down_image_down = tk.PhotoImage(file=self.folderpath + '/Images/downdown.png')
        


        #------------------------------------------------------------#
        #                      set up Buttons
        #------------------------------------------------------------# 

        self.CLEARSCREEN = tk.Button(self.frame, image=self.clear_screen, width = 75, command = self.ClearScreen)       

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
        
        self.spindleup = tk.Button(self.frame, text = 'Spindle UP', width = 10, command = self.ForwardZController, repeatdelay = 500, repeatinterval = 1)


        
        self.spindledown = tk.Button(self.frame, text = 'Spindle DOWN', width = 10, command = self.ReverseZController, repeatdelay = 500, repeatinterval = 1)


        #------------------------------------------------------------#
        #Quit Button and New window
        #------------------------------------------------------------#
        self.New_window_button = tk.Button(self.frame, text = 'New Window', width = 10, command = self.new_window)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 10, command = self.close_windows)


        #------------------------------------------------------------#
        #Object Buttons
        #------------------------------------------------------------#

        self.CircleButton = tk.Button(self.frame, text = 'Oval', width = 10, command = self.MyFunctionOval)
        #self.CircleButton.bind('ButtonPress-1',self.MyFunction('oval'))
        self.RectButton = tk.Button(self.frame, text = 'Rectangle', width = 10, command = self.MyFunctionRectangle)        
        #self.LineButton.bind('<ButtonPress-1>',self.MyFunctionLine)
        self.LineButton = tk.Button(self.frame, text = 'Lines', width = 10, command = self.MyFunctionLine)
        self.EditButton = tk.Button(self.frame, text = 'Edit', width = 10, command =self.MyFunctionEdit)

        self.MoveButton = tk.Button(self.frame, text = 'Move', width = 10, command =self.MyFunctiOnMove)
        #self.PolygonButton2 = tk.Button(self.frame, text = 'Quit', width = 10, command = self.close_windows)
        #self.PolygonButton3 = tk.Button(self.frame, text = 'Quit', width = 10, command = self.close_windows)        

        #------------------------------------------------self.count------------#
        #GRID layout of buttons on screen also do we need to have a 
        #different display manager pixel positon or pack() place() *grid()
        #------------------------------------------------------------#
        self.CLEARSCREEN.grid(rowspan = 3, row = 3, column = 2)
        
        self.logo.grid(row = 1, column = 1, columnspan = 3)
        
        self.Xodometer.grid(row = 0, column = 1)
        
        self.Yodometer.grid(row = 0, column = 2)
        
        self.Zodometer.grid(row = 0, column = 3)
        
        self.RIGHT_BUTTON.grid(row=3,column=6)
        
        self.LEFT_BUTTON.grid(row=3,column=4)
        
        self.DOWN_BUTTON.grid(row=4,column=5)
        
        self.UP_BUTTON.grid(row=2,column=5)
        
        self.spindleup.grid(row=5,column=1)
        
        self.spindledown.grid(row=5,column=2)
        
        self.quitButton.grid(row=9,column=1)
        
        self.New_window_button.grid(row=10,column=10)
        
        self.frame.grid(row=50,column=50)
        #put the screen on the master window
        self.screen.grid(rowspan = 10, row=1, column=11)
        #object buttons
        self.CircleButton.grid(row=6,column=1)
        self.RectButton.grid(row=6,column=2) 
        self.LineButton.grid(row=7,column=1) 
        self.EditButton.grid(row=7,column=2)
        self.MoveButton.grid(row=8, column=1)
        
#----------------------------------------------------------#
#left/right up/down button images
#----------------------------------------------------------#        
    def Left_Motion_up(self):
        self.LEFT_BUTTON.config(image=self.left_image_up)
        self.LEFT_BUTTON.update()
        
    def Left_Motion_down(self):
        self.LEFT_BUTTON.config(image=self.left_image_down)
        self.LEFT_BUTTON.update()

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
        
        
    #open a new window future plan to use as file dialog   
    def new_window(self):
        print("new window",  lineno())
        self.newWindow = tk.Toplevel(self.master)
        self.app = Zero(self.newWindow)

    #TODO make a better method to killall to end program 
    #maybe pid the PROCESSES that are running
    def close_windows(self):
        self.master.destroy()
        os.system('killall python3')
#------------------------------------------------------#
# update the Position on the arrow buttons left, right
#------------------------------------------------------#
    def leftXController(self):
        logger.debug("do_stepx() ")
        self.xController( 'step -1')
        #
        # con0.pipe.send('step -1')
        # con0.pipe.send('get odometer 0')
        # text = (con0.pipe.recv())
        # text = text.strip('odometer: ')
        # self.odometerx.set("Odometer: %s"%(text))
        # #adding the draw line function to the stepper motors move buttons
        # self.screen.create_line(self.x, self.y, int(text), self.y, smooth=True, fill = 'red')
        # self.x = int(text)
        # print (self.x)

    
    def rightXController(self):
        logger.debug("do_stepx() ")
        self.xController( 'step 1')
        #
        # con0.pipe.send('step 1')
        # con0.pipe.send('get odometer 0')
        # text = (con0.pipe.recv())
        # text = text.strip('odometer: ')
        # self.odometerx.set("Odometerx: %s"%(text))
        # self.screen.create_line(self.x,self.y,int(text),self.y,smooth=True, fill = 'red')
        # self.x = int(text)
        # print (self.x)

    def xController(self, step_cmd ):
        """ common controller code """
        con0.pipe.send(step_cmd)
        con0.pipe.send('get odometer 0')
        text = (con0.pipe.recv())
        text = text.strip('odometer: ')
        self.odometerx.set("Odometer: %s"%(text))
        #adding the draw line function to the stepper motors move buttons
        self.screen.create_line(self.x, self.y, int(text), self.y, smooth=True, fill = 'red')
        self.x = int(text)
        print (self.x , lineno())


#------------------------------------------------------#
# update the Position on the arrow buttons up, down or
#forward and back looking from top down on a plane
#------------------------------------------------------#

    def upYController(self):
        logger.debug("do_stepy() ")
        con1.pipe.send('step -1')
        con1.pipe.send('get odometer 1')
        text = (con1.pipe.recv())
        text = text.strip('odometer: ')
        self.odometery.set("Odometery: %s"%(text))
        self.screen.create_oval(self.x,self.y,self.x,int(text),smooth=True, fill = 'red')
        self.y = int(text)
        print (self.y , lineno())  


    def downYController(self):
        logger.debug("do_stepy() ")
        con1.pipe.send('step 1')
        con1.pipe.send('get odometer 1')
        text = (con1.pipe.recv())
        text = text.strip('odometer: ')
        self.odometery.set("Odometery: %s"%(text)) 
        self.screen.create_line(self.x,self.y,self.x,int(text),smooth=True, fill = 'red')
        self.y = int(text)
        print (self.y, lineno()) 

#--------------------------------------------------------#
# update the Position on the arrow buttons yet to be defined
#--------------------------------------------------------#

    def ForwardZController(self):
        logger.debug("do_stepz() ")
        con2.pipe.send('step 1')
        con2.pipe.send('get odometer 2')
        text = (con2.pipe.recv())        
        text = text.strip('odometer: ')
        self.odometerz.set("Odometery: %s"%(text))
        
        
    def ReverseZController(self):
        logger.debug("do_stepz() ")
        con2.pipe.send('step -1')
        con2.pipe.send('get odometer 2')
        text = (con2.pipe.recv())
        text = text.strip('odometer: ')
        self.odometerz.set("Odometery: %s"%(text))



    def ClearScreen(self):
        self.screen.delete('all')
#------------------------------------------------------#
#Not Defined yet maybe not used the odometer call
#--------------------------------------

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


#-----------------------------------------------------------#
#we define the mouse movement and the draw method
#	circle  centerx, centery,  radius
#-----------------------------------------------------------#
#FIXME self.choices.update({'object_type': '21',}) needs to be updated every new object


    def onStart(self, event):
        self.start = event
        self.drawn = None
        self.object_count = self.object_count + 1
    def onGrow(self, event):    
        if self.drawn: self.screen.delete(self.drawn)
        #this is the line that makes the object I need to have it in 
        #an if statement to deside wether to create of edit an object
        if self.edit_type == 0:
            objectId = self.myfunc(self.start.x, self.start.y, event.x, event.y, width = 2)
            self.drawn = objectId
            global choices
            print(self.object, self.drawn, lineno())
            #here is where we add to dropdown menu but its not updating
            self.choices.update({self.object + str(self.object_count): self.drawn})
            print(self.choices, lineno())
        elif self.edit_type == 1:
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            
            #self.screen.find_closest(event.x, event.y)
            #make it select an object and hold same object till finnished
            self.myfunc(self.name_object, int(self.co_ords[0]+diffX), int(self.co_ords[1]+diffY), int(self.co_ords[2]), int(self.co_ords[3]))
            #x1, y1, x2, y2 = self.screen.coords(self.drawn)
        else:
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            self.myfunc(self.name_object, int(self.co_ords[0]+diffX), int(self.co_ords[1]+diffY), int(self.co_ords[2]+diffX), int(self.co_ords[3]+diffY))
       
            
        if self.Colour == 0:
            self.screen.itemconfig(self.drawn, fill = 'red', tags=("one", "two"))
        else:
            self.screen.itemconfig(self.drawn, outline = 'green')
        if trace: print (self.drawn, lineno())
        #lines bellow show keywords and methods for config 
        #commented out to see options from one object scroll
        #to botom of this file
        #help(self.screen)#this option returns the size x y and position x y
        #print(self.screen.itemconfig(ID))
        #print(objectId , self.object ,self.start.x, self.start.y, event.x, event.y)

    def onClear(self, event):
        event.widget.delete(sel,self.drawn)


        '''I have fixed this
        #FIXME Need to hold the object editing id in a variable that cant be change
        # or change whgen moving the mouse TODO self.screen.find_closest(event.x, event.y)
        #make it select a object and hold same object till finnished'''

    
    def OnSelect(self, event):
        #This right click event selects object to edit or move
        self.name_object = self.screen.find_closest(event.x, event.y)    
        self.co_ords = self.screen.coords(self.name_object)
        print (self.screen.type(self.name_object), self.name_object, (self.screen.coords(self.name_object))) 
        #print(self.screen.itemcget(self.name_object,)) 
        
#flipping functions to suit desired object shape rect and oval or edit and move

    def MyFunctionOval(self):
        self.myfunc = self.screen.create_oval
        self.object = "Oval"
        self.Colour = 1
        self.edit_type = 0 
    def MyFunctionRectangle(self):
        self.myfunc = self.screen.create_rectangle 
        self.object = "Rectangle"
        self.Colour = 1
        self.edit_type = 0      
    def MyFunctionLine(self):
        self.myfunc = self.screen.create_line 
        self.object = "Line"
        self.Colour = 0
        self.edit_type = 0
    def MyFunctionEdit(self):
        self.myfunc = self.screen.coords 
        self.edit_type = 1
        if self.name_object == None: messagebox.showinfo("Warning", "You need to right click an object before you can edit or move")
          
    def MyFunctiOnMove(self):
        self.myfunc = self.screen.coords 
        self.edit_type = 2
        if self.name_object == None: messagebox.showinfo("Warning", "You need to right click an object before you can edit or move")
        
        #choices.update({str(self.object): str(self.name_object)})


#to edit a object .itemconfig(<object id>, fill="blue") 
# change color 
#,.coords(i, new_xy) 
# change coordinates      
        
        
#------------------------------------------------------#
# Class for file dialog not used yet
#------------------------------------------------------#  

class Zero:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.grid()
        self.frame.grid()
    def close_windows(self):
        self.master.destroy()



#------------------------------------------------------#
#                 Main Program loop
#------------------------------------------------------#

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
    logger.info(os.getcwd())
    main()
    
    
    
    
    
    '''keyword for objects 
    {'width': ('width', '', '', '1.0', '2.0'), 'activeoutline': ('activeoutline', '', '', '', ''), 'activestipple': ('activestipple', '', '', '', ''), 'outline': ('outline', '', '', 'black', 'black'), 'activedash': ('activedash', '', '', '', ''), 'fill': ('fill', '', '', '', 'green'), 'offset': ('offset', '', '', '0,0', '0,0'), 'activefill': ('activefill', '', '', '', ''), 'activewidth': ('activewidth', '', '', '0.0', '0.0'), 'dashoffset': ('dashoffset', '', '', '0', '0'), 'disableddash': ('disableddash', '', '', '', ''), 'disabledwidth': ('disabledwidth', '', '', '0.0', '0'), 'disabledoutline': ('disabledoutline', '', '', '', ''), 'outlinestipple': ('outlinestipple', '', '', '', ''), 'disabledfill': ('disabledfill', '', '', '', ''), 'disabledstipple': ('disabledstipple', '', '', '', ''), 'disabledoutlinestipple': ('disabledoutlinestipple', '', '', '', ''), 'tags': ('tags', '', '', '', 'Oval'), 'activeoutlinestipple': ('activeoutlinestipple', '', '', '', ''), 'stipple': ('stipple', '', '', '', ''), 'outlineoffset': ('outlineoffset', '', '', '0,0', '0,0'), 'state': ('state', '', '', '', ''), 'dash': ('dash', '', '', '', '')}
    '''
