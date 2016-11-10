#!/usr/bin/python
"""
- read output from a subprocess in a background thread
- show the output in the GUI
"""
import sys
from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread

try:
    import Tkinter as tk
    from Queue import Queue, Empty
except ImportError:
    import tkinter as tk # Python 3
    from queue import Queue, Empty # Python 3

def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return
        
import math

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

class DisplaySubprocessOutputDemo:
    def __init__(self, root):
        self.root = root

        # start dummy subprocess to generate some output
        self.process = Popen([sys.executable, "-u", "-c", dedent("""
            import itertools, time

            for i in itertools.count():
                print("%d.%d" % divmod(i, 10))
                time.sleep(0.1)
            """)], stdout=PIPE)

        # launch thread to read the subprocess output
        #   (put the subprocess output into the queue in a background thread,
        #    get output from the queue in the GUI thread.
        #    Output chain: process.readline -> queue -> label)
        q = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        t = Thread(target=self.reader_thread, args=[q])
        t.daemon = True # close pipe if GUI process exits
        t.start()

        # show subprocess' stdout in GUI
        self.label = tk.Label(root, text="  ", font=(None, 200))
        self.label.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')
        self.update(q) # start update loop
        #logo = PhotoImage(file="../images/python_logo_small.gif")
        w1 = tk.Label(root, image='').pack(side="right")
        explanation = """At present, only GIF and PPM/PGM
        formats are supported, but an interface 
        exists to allow additional image file
        formats to be added easily."""
        w2 = tk.Label(root,                   
                   padx = 10, 
                   text=explanation).pack(side="left")
        app = ExampleApp()
        

    def reader_thread(self, q):
        """Read subprocess output and put it into the queue."""
        try:
            with self.process.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    q.put(line)
        finally:
            q.put(None)

    def update(self, q):
        """Update GUI with items from the queue."""
        for line in iter_except(q.get_nowait, Empty): # display all content
            if line is None:
                self.quit()
                return
            else:
                self.label['text'] = line # update GUI
                break # display no more than one line per 40 milliseconds
        self.root.after(40, self.update, q) # schedule next update

    def quit(self):
        self.process.kill() # exit subprocess if GUI is closed (zombie!)
        self.root.destroy()


root = tk.Tk()
app = DisplaySubprocessOutputDemo(root)
root.protocol("WM_DELETE_WINDOW", app.quit)
# center window
root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
root.mainloop()
