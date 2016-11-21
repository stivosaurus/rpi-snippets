from tkinter import *
import re
from tkinter import messagebox, filedialog


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):

        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Load the gcode file in and extract the filament value
    def get_filament_value(self, fileName):
        with open(fileName, 'r') as f_gcode:
            data = f_gcode.read()
            re_value = re.search('filament used = .*? \(([0-9.]+)', data)

            if re_value:
                value = float(re_value.group(1))
                return 'Volume of the print is {} cm3'.format(value)
            else:
                return 'Filament volume was not found in {}'.format(fileName)

    def read_gcode(self):
        root.fileName = filedialog.askopenfilename(filetypes=(("GCODE files", "*.gcode"), ("All files", "*.*")))
        self.value.set(self.get_filament_value(root.fileName))

    def client_exit(self):
        exit()

    def about_popup(self):
        messagebox.showinfo("About",
                            "Small software created by Bartosz Domagalski to find used filament parameters from Sli3er generated GCODE")

    # Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("Filament Data")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)
        help = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)
        help.add_command(label="About", command=self.about_popup)

        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)
        menu.add_cascade(label="Help", menu=help)

        # Creating the labels
        self.value = StringVar()
        l_instruction = Label(self, justify=CENTER, compound=TOP,
                              text="  Load GCODE file to find volume, \n weight and price of used filament.")
        l = Label(self, justify=CENTER, compound=BOTTOM, textvariable=self.value)
        #       l.place(x=85, y=45)
        l_instruction.pack()
        l.pack()

        l_instruction.pack()
        self.value = StringVar()
        l = Label(self, textvariable=self.value)
        l.pack()

        # Creating the button
        gcodeButton = Button(self, text="Load GCODE", command=self.read_gcode)
        gcodeButton.pack()
        #       gcodeButton.place(x=140, y=10)

        # status Bar
        status = Label(self, text="Waiting for file...", bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM, fill=X)


# root window created. Here, that would be the only window, but you can later have windows within windows.
root = Tk()
root.resizable(width=False, height=False);
# root.geometry("400x300")


# creation of an instance
app = Window(root)

# mainloop
root.mainloop()
