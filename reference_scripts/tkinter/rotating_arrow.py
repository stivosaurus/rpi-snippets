
import math
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk # Python 3


class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.create_line(200,200, 200,200, tags=("line",), arrow="last")
        self.rotate()

    def rotate(self, angle=0):
        '''Animation loop to rotate the line by 10 degrees every 100 ms'''
        a = math.radians(angle)
        r = 50
        x0, y0 = (200,200)
        x1 = x0 + r*math.cos(a)
        y1 = y0 + r*math.sin(a)
        x2 = x0 + -r*math.cos(a)
        y2 = y0 + -r*math.sin(a)
        self.canvas.coords("line", x1,y1,x2,y2)
        self.after(100, lambda angle=angle+10: self.rotate(angle))

app = ExampleApp()
app.mainloop()
