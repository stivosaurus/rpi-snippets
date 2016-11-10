from Tkinter import *

class Rect(object):
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        coord = self.getCoordinates()
        self.rect = self.canvas.create_rectangle(coord[0], coord[1],
                                                 coord[2], coord[2],
                                                 fill="blue")

    def getCoordinates(self):
        # Used to define the sides of the rect based on a starting x,y position.
        left = -self.width/2 + self.x
        top = -self.height/2 + self.y
        right = self.width/2 + self.x
        bottom = self.height/2 + self.y
        return left, top, bottom, right

    def move(self, x, y):
        # Move the Rect object to a new location.  What is called to by the
        # UI callback moveRect()
        deltaX = x - self.x
        deltaY = y - self.y
        self.canvas.move(self.rect, deltaX, deltaY)
        self.x = x
        self.y = y

class App(object):

    def __init__(self, width=256, height=256):
        self.width = width
        self.height = height

        self.root = Tk()
        self.root.title("tkinter_test01")
        self.root.geometry("%sx%s"%(self.width, self.height))

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        # Bind the event to move our Rect:
        self.canvas.bind("<Motion>", self.moveRect)
        self.canvas.pack()

        # Create our Rect object:
        self.rect = Rect(self.canvas, 32, 32)

        self.root.mainloop()

    def moveRect(self, event):
        # Callback that will move our Rect object
        self.rect.move(event.x, event.y)

if __name__ == "__main__":
    App()
