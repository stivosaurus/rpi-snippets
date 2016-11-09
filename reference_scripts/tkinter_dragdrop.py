from tkinter import Tk, Listbox
from tkinter.constants import *
import win32con
import pythoncom
import pywintypes
import win32com.server.policy
from win32com.shell import shell, shellcon

class DropTarget(win32com.server.policy.DesignatedWrapPolicy):
    _reg_progid_ = "Python.DropTarget" 
    _reg_clsid_ = "{411c82bc-d2c4-4a67-a8fa-6a94996190bd}"
    _reg_desc_ = "OLE DND Drop Target"
    _com_interfaces_ = [pythoncom.IID_IDropTarget]
    _public_methods_ = ['DragEnter', 'DragOver', 'DragLeave', 'Drop']

    data_format = (
      win32con.CF_HDROP, 
      None,
      pythoncom.DVASPECT_CONTENT, 
      -1, 
      pythoncom.TYMED_HGLOBAL)

    def __init__ (self, hwnd):
        self.hwnd = hwnd
        self.drop_effect = shellcon.DROPEFFECT_COPY
        self._wrap_(self)
        self.register()

    def DragEnter (self, data_object, key_state, point, effect):
        try:
            data_object.QueryGetData(self.data_format)
            self.drop_effect = shellcon.DROPEFFECT_COPY
        except pywintypes.com_error:
            self.drop_effect = shellcon.DROPEFFECT_NONE
        return self.drop_effect

    def DragOver (self, key_state, point, effect):
        return self.drop_effect

    def DragLeave(self): pass

    def Drop(self, data_object, key_state, point, effect):
        global text_list
        try:
            data_object.QueryGetData(self.data_format)
            data = data_object.GetData(self.data_format)
            n_files = shell.DragQueryFileW(data.data_handle, -1)
            text_list = []
            for n in range(min(n_files, 20)):
                text = format(n + 1, '>2') + '. '
                text += shell.DragQueryFileW(data.data_handle, n)
                text_list.append(text)
        except pywintypes.com_error:
            text_list = ["Unsupported data format"]

    def register(self):
        try:
            pythoncom.RegisterDragDrop(self.hwnd, 
              pythoncom.WrapObject(self, 
                pythoncom.IID_IDropTarget, 
                pythoncom.IID_IDropTarget))
        except pywintypes.com_error:
            global text_list
            text_list = ["COM failure!"]

def update_list():
    listbox.delete(0, END)
    for t in text_list:
        listbox.insert(END, t)
    root.after(100, update_list)

root = Tk()
root.geometry('720x360')
listbox = Listbox(root, font=("Courier", 10, "normal"))
listbox.pack(fill=BOTH, expand=1)
text_list = ['Drag files to this window.']

hwnd = root.winfo_id()
pythoncom.OleInitialize()

root.after(100, update_list)
root.after(200, DropTarget, hwnd)
root.mainloop()
