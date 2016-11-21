import ScrolledText
import sys
import tkFileDialog
import Tkinter
 
 
########################################################################
class RedirectText(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, text_ctrl):
        """Constructor"""
        self.output = text_ctrl
 
    #----------------------------------------------------------------------
    def write(self, string):
        """"""
        self.output.insert(Tkinter.END, string)
 
 
########################################################################
class MyApp(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Redirect")
        self.frame = Tkinter.Frame(parent)
        self.frame.pack()
 
        self.text = ScrolledText.ScrolledText(self.frame)
        self.text.pack()
 
        # redirect stdout
        redir = RedirectText(self.text)
        sys.stdout = redir
 
        btn = Tkinter.Button(self.frame, text="Open file", command=self.open_file)
        btn.pack()
 
    #----------------------------------------------------------------------
    def open_file(self):
        """
        Open a file, read it line-by-line and print out each line to
        the text control widget
        """
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = '/home'
        options['parent'] = self.root
        options['title'] = "Open a file"
 
        with tkFileDialog.askopenfile(mode='r', **options) as f_handle:
            for line in f_handle:
                print (line)
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tkinter.Tk()
    root.geometry("800x600")
    app = MyApp(root)
    root.mainloop()
