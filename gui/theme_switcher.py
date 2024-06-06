from tkinter import IntVar, ttk, BooleanVar

from tooltip import CreateToolTip
from gui_helper_fns import LG_PADDING

# Dark Mode checkbox
class ThemeSwitcher: 
    def __init__(self, parent, control_fn):
        #callback function to trigger when checkbox is toggled
        self.control_fn = control_fn
          
        self.theme_val = BooleanVar()
        self.theme_switcher = ttk.Checkbutton(parent, text='Dark Mode', command=self.control_fn, variable=self.theme_val)
        self.theme_val.set(True)
        CreateToolTip(self.theme_switcher, text='Toggle between light and dark mode')
       
        self.theme_switcher.pack(side='left', **LG_PADDING)
    
    #returns the value of the checkbox
    def get(self):
        return self.theme_val.get()