from tkinter import IntVar, ttk

from tooltip import CreateToolTip
from gui_helper_fns import LG_PADDING

# Advanced Options checkbox
class AdvancedOptions: 
    def __init__(self, parent, control_fn):
        #callback function to trigger when checkbox is toggled
        self.control_fn = control_fn
          
        self.advanced_enabled = IntVar()
        self.advanced_options = ttk.Checkbutton(parent, text='Advanced Options', command=self.control_fn, variable=self.advanced_enabled)
        CreateToolTip(self.advanced_options, text='Advanced mode provides more customization options. \nNote: checking this will clear all inputs')
       
        self.advanced_options.pack(side='right', **LG_PADDING)
    
    #returns the value of the checkbox (1 or 0)
    def get(self):
        return self.advanced_enabled.get()