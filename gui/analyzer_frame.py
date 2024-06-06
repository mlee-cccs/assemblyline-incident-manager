    
import csv
import tkinter as tk
from tkinter import Frame, Toplevel, messagebox
from tkinter import ttk

from tooltip import CreateToolTip
from gui_helper_fns import LG_PADDING, REPORT_FILE, SM_PADDING, add_flags_to_command, add_options_to_command, create_input, create_number_input, load_config, run_command


class AnalyzerFrame: 
    def __init__(self, parent, config, advanced):
        self.advanced = advanced # advanced mode enabled
        self.config= config
       
        self.analyzer_flags: dict = {}
        self.analyzer_options: dict = {}
        self.frame = self.create_analyzer_frame(parent)
      
    def get_frame(self):
        return self.frame

    def create_analyzer_frame(self, parent):
        self.analyzer_frame = Frame(parent)
       
        analyzer_required_frame = ttk.LabelFrame(self.analyzer_frame, text='Required')
        analyzer_optional_frame = ttk.LabelFrame(self.analyzer_frame, text='Optional')

        #
        # Required Params
        #
        self.analyzer_incident_num = create_input(analyzer_required_frame, "* Incident Number:")
        CreateToolTip(self.analyzer_incident_num, text='The incident number that each file is associated with.')

        #
        # Optional Params
        #
        self.analyzer_minimum_score = create_number_input(analyzer_optional_frame, "Minumum Score: ")
        CreateToolTip(self.analyzer_minimum_score, text='The minimum score for files that we want to query from Assemblyline.')
        self.analyzer_options['--min_score'] = self.analyzer_minimum_score

        analyzer_required_frame.pack(fill='both', **LG_PADDING)

        #enable options if advanced_mode is enabled
        if(self.advanced == 1):
            analyzer_optional_frame.pack(fill='both',  **LG_PADDING)
       

        ## pack the frames and analyze button
        analyze_button =ttk.Button(self.analyzer_frame, text="Analyze", command=self.run_analyzer)
        analyze_button.pack(anchor='e',  **SM_PADDING)
        
        #check if report file is present. If there is a report file, show the results button
        try:
            report = open(REPORT_FILE, 'r')
            results_button =ttk.Button(self.analyzer_frame, text='Results', command=self.analyzer_window)
            results_button.pack(anchor='e',**SM_PADDING)
        except FileNotFoundError:
            #Don't add results button
            None

        self.analyzer_frame.pack(fill='both',  **LG_PADDING)
        return self.analyzer_frame
    
    def analyzer_window(self):
        self.top = Toplevel()
        self.top.wm_title = ("Analysis Results")
        self.top.geometry('1200x600')
        #Create A Main frame
        main_frame = tk.Frame(self.top)
        main_frame.pack(fill=tk.BOTH,expand=1)

        # Create Frame for X Scrollbar
        sec = tk.Frame(main_frame)
        sec.pack(fill=tk.X,side=tk.BOTTOM)

        # Create A Canvas
        self.my_canvas = tk.Canvas(main_frame)
        self.my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1, padx=10, pady=10)

        # Add A Scrollbars to Canvas
        x_scrollbar = ttk.Scrollbar(sec,orient=tk.HORIZONTAL,command=self.my_canvas.xview)
        x_scrollbar.pack(side=tk.BOTTOM,fill=tk.X)
        y_scrollbar = ttk.Scrollbar(main_frame,orient=tk.VERTICAL,command=self.my_canvas.yview)
        y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        # Configure the canvas
        self.my_canvas.configure(xscrollcommand=x_scrollbar.set)
        self.my_canvas.configure(yscrollcommand=y_scrollbar.set)
        self.my_canvas.bind("<Configure>",lambda e: self.my_canvas.config(scrollregion= self.my_canvas.bbox(tk.ALL)))
        self.my_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel) 

      
        # Create Another Frame INSIDE the Canvas
        second_frame = tk.Frame(self.my_canvas)

        # Add that New Frame a Window In The Canvas
        self.my_canvas.create_window((0,0),window= second_frame, anchor="nw")
        try:
            report = open(REPORT_FILE, 'r')
            csvReport = csv.reader(report)
            _row = 0
            for line in csvReport:
                for str in line: 
                    str.replace('[', '') #remove brackets around each line
                    str.replace(']', '')

                    #create 'cell' for each item in file
                    #rough dynamic width to make the filename a bit larger and the score a bit smaller
                    tmp = tk.Entry(second_frame, width=(60 if line.index(str) == 0 else (30 if line.index(str) != 2 else 10  ) ), foreground='black', background='white') 
                    tmp.insert(0, str)
                    tmp.configure(state='readonly')
                    tmp.grid(row=_row,column=line.index(str) )
                _row += 1  #increment row
        except FileNotFoundError:
            messagebox.showerror("Error", f'Unable to find file: {REPORT_FILE}')


    def on_mouse_wheel(self, event):
        self.my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        

    def run_analyzer(self):
        self.config = load_config()
        
        url = self.config['url']
        username = self.config['username']
        apikey = self.config['apikey_read']

        incident_num = self.analyzer_incident_num.get()

        command = f"al-incident-analyzer --url={url} --username=\"{username}\" --apikey=\"{apikey}\" --incident_num={incident_num}"
        command = add_options_to_command(command, self.analyzer_options)
        command = add_flags_to_command(command, self.analyzer_flags)
        run_command(command)

 
