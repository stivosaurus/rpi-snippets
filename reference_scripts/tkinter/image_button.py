# toggle a Tkinter button up/down 
# using images and no button border
# tested with Python 2.7 and Python 3.2 by vegaseat
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
def motion_up(up):
    button.config(image=image_up)
def motion_down(down):
    button.config(image=image_down)

root = tk.Tk()
root.title("up/down button no border")
# pick GIF images you have in the working directory
# or give full path
image_up = tk.PhotoImage(file='leftup.png')
image_down = tk.PhotoImage(file='leftdown.png')
# create a button to display the image
# use bd or borderwidth zero for no border
# start with button image up
button = tk.Label(root, image=image_up,command = None)
button.bind('<ButtonRelease-1>',motion_up)
button.bind('<Button-1>',motion_down)
# position the widgets
button.grid(row=1, column=1, padx=130)
root.mainloop()
