
import json
from tkinter import Frame, ttk

from tooltip import CreateToolTip
from gui_helper_fns import ALIM_CONFIG_FILE, LG_PADDING, SM_PADDING, create_file_input, create_input


class SettingsFrame:

       def __init__(self, parent, config):
              self.config = config
              self.frame = self.create_settings_frame(parent)
     
       def get_frame(self):
              return self.frame
                 
       def create_settings_frame(self, parent): 
              self.settings_frame = Frame(parent)
              self.url = create_input(self.settings_frame, "URL:", default_value=self.config['url'])

              CreateToolTip(self.url, text='The target URL that hosts Assemblyline.')

              self.username = create_input(self.settings_frame, "Username:", default_value=self.config['username'])
              CreateToolTip(self.username, text='Your Assemblyline account username.')

              self.apikey_read = create_file_input(self.settings_frame, "API Key Path (readonly):", default_value=self.config['apikey_read'])
              CreateToolTip(self.apikey_read, text='A path to a file that contains only your Assemblyline account API key. \nNOTE: This API key requires read access for the submitter and write access for the analyzer and downloader.')

              self.apikey_write = create_file_input(self.settings_frame, "API Key Path (writeonly):", default_value=self.config['apikey_write'])
              CreateToolTip(self.apikey_write, text='A path to a file that contains only your Assemblyline account API key. \nNOTE: This API key requires read access for the submitter and write access for the analyzer and downloader.')


              self.settings_frame.pack(side='left', fill='both', **LG_PADDING)

              save_button =ttk.Button(self.settings_frame, text="Save", command=self.save_settings)
              save_button.pack( ipadx=10, anchor='e', **SM_PADDING)

              return self.settings_frame
       
       def save_settings(self): 
        config = {
            "url": self.url.get(),
            "username": self.username.get(),
            "apikey_read": self.apikey_read.get(),
            "apikey_write": self.apikey_write.get()
        }
        out_file = open(ALIM_CONFIG_FILE, 'w')
        json.dump(config, out_file)
        
   