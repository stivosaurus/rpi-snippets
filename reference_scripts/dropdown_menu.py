from Tkinter import *
import Tkinter as ttk 
from ttk import *
import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

if __name__ == '__main__':
    print "hello, this is line number", lineno()
    print 
    print 
    print "and this is line", lineno()

root = Tk()
root.title("Age Selector")

mainframe = Frame(root)                                 
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 10, padx = 10)

var = StringVar(root)

# Use dictionary to map names to ages.
choices = {
    'Bob': '35',
    'Garry': '45',
    'John': '32',
    'Hank': '64',
}
choices.update({'Tyrone': '21',})
option = OptionMenu(mainframe, var, *choices)
var.set('Bob')

option.grid(row = 1, column =1)

Label(mainframe, text="Age").grid(row = 2, column = 1)

age = StringVar()
# Bind age instead of var
age_ent = Entry(mainframe, text=age, width = 15).grid(column = 2, row = 2)

# change_age is called on var change.
def change_age(*args):
    age_ = choices[var.get()]
    age.set(age_)
# trace the change of var
var.trace('w', change_age)

root.mainloop()
