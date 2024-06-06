import tkinter as tk
from tkinter import  Frame, ttk
from PIL import Image, ImageTk

import TKinterModernThemes as TKMT

from advanced_options import AdvancedOptions
from analyzer_frame import AnalyzerFrame
from theme_switcher import ThemeSwitcher
from downloader_frame import DownloaderFrame
from gui_helper_fns import load_config
from settings_frame import SettingsFrame
from submitter_frame import SubmitterFrame

class AssemblylineGUI(TKMT.ThemedTKinterFrame):
    def __init__(self, mode):
        super().__init__( "Assemblyline Incident Manager", 'azure', mode) #Title, Theme : ('park', 'sun-valley', 'azure'), Mode 
        self.config = load_config() # prepopulates assemblyline url, username, and apikeys

        #To change the application icon
        icon = Image.open('crane.png')
        photo = ImageTk.PhotoImage(icon)
        self.root.wm_iconphoto(True, photo)

        self.topbar = Frame(self.root)
        self.topbar.pack(fill='x')
        self.advanced_options = AdvancedOptions(self.topbar, self.tab_refresh)
        self.theme_switcher = ThemeSwitcher(self.topbar, self.change_theme)

        #Generates the GUI
        self.create_tabs()
        self.run()

    # Callback function for the advanced options selection. Rebuilds the gui to include/exclude the optional params
    def tab_refresh(self): 
        #get the current tab index before refreshing the tabs, the current_tab gets selected in the create_tabs method
        self.current_tab = self.tabController.index(self.tabController.select())
        self.tabController.destroy()
        self.create_tabs()

    # Callback function for switching between light and dark mode
    def change_theme(self):
        if(self.theme_switcher.get()):
            self.root.tk.call('set_theme', 'dark')
            self.mode = 'dark'
        else:
            self.root.tk.call('set_theme', 'light')
            self.mode = 'light'


    def on_tab_change(self, event):
        tab = event.widget.nametowidget(event.widget.select())
        event.widget.configure(height=tab.winfo_reqheight())

    #Initializes the tab frames for the different sections and adds them to the tabController
    def create_tabs(self):
        self.tabController = ttk.Notebook(self.root)
        
        
        self.submitter_tab = SubmitterFrame(self.tabController, config=self.config, advanced=self.advanced_options.advanced_enabled.get()).get_frame()
        self.analyzer_tab = AnalyzerFrame(self.tabController, config=self.config, advanced=self.advanced_options.advanced_enabled.get()).get_frame()
        self.downloader_tab = DownloaderFrame(self.tabController, config=self.config, advanced=self.advanced_options.advanced_enabled.get()).get_frame()
        self.settings_tab = SettingsFrame(self.tabController, config=self.config).get_frame()

        self.tabController.add(self.submitter_tab, text='Submitter')        
        self.tabController.add(self.analyzer_tab, text='Analyzer')
        self.tabController.add(self.downloader_tab, text='Downloader')
        self.tabController.add(self.settings_tab, text='Settings')

        #if the current tab exists (set in tab_refresh), select it
        #This prevents the tab from being reset to submitter when advanced mode is selected
        try: 
            self.tabController.select(self.current_tab)
        except: 
             None   

        self.tabController.pack(expand=True, fill='both')
        self.tabController.bind('<<NotebookTabChanged>>', self.on_tab_change)
        self.root.update_idletasks() # force refresh to update application height
        

if __name__ == "__main__": 
    AssemblylineGUI('dark') #default to dark mode