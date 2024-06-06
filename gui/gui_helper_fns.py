import json
import subprocess
import tkinter as tk
from tkinter import Frame, IntVar, Label, Toplevel, filedialog, ttk
from tkinter import messagebox

ALIM_CONFIG_FILE = "ALIM_config.json"
REPORT_FILE = "report.csv" # must match al_incident_analyzer REPORT_FILE

#default paddings
SM_PADDING ={ 'padx' : 5, 'pady': 3}
LG_PADDING = {'padx': 10, 'pady':10}


#loads the url, username, and apikey path for use across the application
def load_config():
    try: 
        input = open(ALIM_CONFIG_FILE, 'r')
        config = json.load(input)
    except FileNotFoundError:
        out_file = open(ALIM_CONFIG_FILE, 'w')
        config= {
            "url": "",
            "username": "",
            "apikey_read": "",
            "apikey_write": ""
        }
        json.dump(config, out_file)
    return config

#
# Functions to create the different input widgets
#
def create_input( parent, label_text, default_value=''):
        frame =Frame(parent)
        frame.pack(fill="x", pady=2)

        label =Label(frame, text=label_text, width=20, anchor="w")
        label.pack(side="left")

        entry =ttk.Entry(frame)
        if(default_value != ''):
            entry.insert(0, default_value)
        entry.pack(side="right", fill="x", expand=True, **SM_PADDING)
        return entry
    
#number-only Entry
def create_number_input( parent, label_text, default_value=''):
        frame = Frame(parent)
        frame.pack(fill="x", pady=2)

        label = Label(frame, text=label_text, width=20, anchor="w")
        label.pack(side="left")
        
        validator = (frame.register(number_entry_validation),'%P')
        entry =ttk.Entry(frame)
        if(default_value != ''):
            entry.insert(0, default_value)
        entry.configure(validate='key', validatecommand=validator)
        entry.pack(side="right", fill="x", expand=True, **SM_PADDING)
        return entry

# validation to only allow number inputs in Entry widget    
def number_entry_validation( val):
        result = False
        if val.isdigit() or val == '':
            result = True
        return result
          
def create_checkbox( parent, label_text : str, flag: str, flag_dict: dict):
        frame=Frame(parent)
        frame.pack(fill='x', pady=3)

        index = flag
 
        flag_dict[index] = IntVar(value=0)
        check_button = ttk.Checkbutton(frame, text=label_text, variable=flag_dict[index])
        check_button.pack(expand=True, anchor='w')
    
        return check_button
        
def create_file_input(parent, label_text, default_value='',  is_directory=False):
        frame = Frame(parent)
        frame.pack(fill="x", pady=2)

        label = Label(frame, text=label_text, width=20, anchor="w")
        label.pack(side="left")

        entry =ttk.Entry(frame)
        if(default_value != ''):    
            entry.insert(0, default_value)
        entry.pack(side="left", fill="x", expand=True, **SM_PADDING)

        button_text = "Browse" if not is_directory else "Select Folder"
        button =ttk.Button(frame, text=button_text, command=lambda: browse_file(entry, is_directory))
        button.pack(side="right", **SM_PADDING)

        return entry

def browse_file(entry, is_directory):
        if is_directory:
            path = filedialog.askdirectory()
        else:
            path = filedialog.askopenfilename()
        
        #only change Entry value if a new path is selected
        if(len(path) > 0):
            entry.delete(0, tk.END)
            entry.insert(0, path)

# same setup as analyze_window, need to make own window so that it is scrollable 
# messagebox is a cleaner solution if the output gets reformatted 
def output_window( message, status):
    output_window = Toplevel()
    output_window.wm_title(status)
    output_window.geometry('1200x600')
    
    #Create A Main frame
    main_frame = tk.Frame(output_window)
    main_frame.pack(fill=tk.BOTH,expand=1)

    # Create Frame for X Scrollbar
    sec = tk.Frame(main_frame)
    sec.pack(fill=tk.X,side=tk.BOTTOM)

    # Create A Canvas
    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1, padx=10, pady=10)

    # Add A Scrollbars to Canvas
    x_scrollbar = ttk.Scrollbar(sec,orient=tk.HORIZONTAL,command=my_canvas.xview)
    x_scrollbar.pack(side=tk.BOTTOM,fill=tk.X)
    y_scrollbar = ttk.Scrollbar(main_frame,orient=tk.VERTICAL,command=my_canvas.yview)
    y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

    def on_mouse_wheel(event):
        my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    # Configure the canvas
    my_canvas.configure(xscrollcommand=x_scrollbar.set)
    my_canvas.configure(yscrollcommand=y_scrollbar.set)
    my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(tk.ALL)))
    my_canvas.bind_all("<MouseWheel>", on_mouse_wheel) 

      
    # Create Another Frame INSIDE the Canvas
    second_frame = tk.Frame(my_canvas)

    # Add that New Frame a Window In The Canvas
    my_canvas.create_window((0,0),window= second_frame, anchor="nw")
    textWidget = tk.Label(second_frame, text=message, justify='left')
    textWidget.pack(anchor='w', expand=True)

#
# Helpers for building the command
#
def add_flags_to_command(command: str, flag_arr: dict):
        for flag in flag_arr:
            if(flag_arr[flag].get() == 1):
                command = command+' '+flag
        return command

def add_options_to_command(command: str, options_arr: dict):
    for option in options_arr: 
            if(len(options_arr[option].get()) > 0):
                command = command+' '+option+'='+options_arr[option].get()        
    return command

def run_command(command):
        print(command) #for testing
        try:
            process = subprocess.Popen(command,shell=True, creationflags=subprocess.CREATE_NO_WINDOW, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            #always fire a yes to bypass overwrite [y/n] in scripts
            output, err = process.communicate(b"y")
            
            window = output_window(output.decode(), "Success")
            #messagebox.showinfo("Success", output.decode())
        except subprocess.CalledProcessError as e:
            window = output_window(e.output, "Error")
            #messagebox.showerror("Error", e.output)
