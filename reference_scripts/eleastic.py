from tkinter import *
trace = 0 
     
class CanvasEventsDemo: 
    def __init__(self, parent=None):
        canvas = Canvas(width=300, height=300, bg='white') 
        canvas.pack()
        canvas.bind('<ButtonPress-1>', self.onStart)  
        canvas.bind('<B1-Motion>',     self.onGrow)   
        canvas.bind('<Double-1>',      self.onClear)  
        canvas.bind('<ButtonPress-3>', self.onMove)
           
        self.canvas = canvas
        self.drawn  = None

    def onStart(self, event):
        self.start = event
        self.drawn = None

    def onGrow(self, event):                          
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = canvas.create_oval(self.start.x, self.start.y, event.x, event.y)
        if trace: print (objectId)
        self.drawn = objectId

    def onClear(self, event):
        event.widget.delete('all')

    def onMove(self, event):
        if self.drawn:            
            if trace: print (self.drawn)
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            canvas.move(self.drawn, diffX, diffY)
            self.start = event
    def moveRect(self, event):
        # Callback that will move our Rect object
        self.rect.move(event.x, event.y)
     
CanvasEventsDemo()
mainloop()

