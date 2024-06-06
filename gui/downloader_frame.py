import tkinter as tk
from tkinter import Frame, ttk

from tooltip import CreateToolTip
from gui_helper_fns import LG_PADDING, add_flags_to_command, add_options_to_command, create_checkbox, create_file_input, create_input, create_number_input, load_config, run_command

class DownloaderFrame: 
    def __init__(self, parent, config, advanced):
        self.advanced =advanced
        self.config= config
       
        self.downloader_flags: dict = {}
        self.downloader_options: dict = {}
        self.frame = self.create_downloader_frame(parent)
 
         
    def get_frame(self):
        return self.frame

    def create_downloader_frame(self, parent):
        self.downloader_frame = Frame(parent)

        downloader_required_frame = ttk.LabelFrame(self.downloader_frame, text='Required')
        downloader_optional_frame = ttk.LabelFrame(self.downloader_frame, text='Optional')

        #
        # Required Params
        #
        self.downloader_incident_num = create_input(downloader_required_frame, "* Incident Number:")
        CreateToolTip(self.downloader_incident_num, text='The incident number that each file is associated with.')
        
        self.downloader_max_score = create_number_input(downloader_required_frame, "* Max Score:")
        CreateToolTip(self.downloader_max_score, text='The maximum score for files that we want to download from Assemblyline.')
        
        self.downloader_download_path = create_file_input(downloader_required_frame, "* Download Path:", is_directory=True)
        CreateToolTip(self.downloader_download_path, text='The path to the folder that we will download files to.')
        
        self.downloader_upload_path = create_file_input(downloader_required_frame, "* Upload Path:", is_directory=True)
        CreateToolTip(self.downloader_upload_path, text='The base path from which the files were ingested from on the compromised system.')

        downloader_required = ttk.Separator(self.downloader_frame, orient='horizontal')
        downloader_required.pack(**LG_PADDING)

        #
        # Optional Params
        #
        self.downloader_thread_count = create_number_input(downloader_optional_frame, 'Download Threads:')
        CreateToolTip(self.downloader_thread_count, text='The number of threads that will be created to facilitate downloading the files.')
        self.downloader_options['--num_of_downloaders'] = self.downloader_thread_count

        self.downloader_do_not_verify_ssl = create_checkbox(downloader_optional_frame, 'Do Not Verify SSL', flag='--do-not-verify-ssl', flag_dict=self.downloader_flags)
        CreateToolTip(self.downloader_do_not_verify_ssl, text='Verify SSL when creating and using the Assemblyline Client.')

        ## pack the frames and download button 
        downloader_required_frame.pack(fill='both', **LG_PADDING)
       
        if(self.advanced == 1):
            downloader_optional_frame.pack(fill='both', **LG_PADDING)
        self.downloader_frame.pack(fill='both', **LG_PADDING)

        download_button =ttk.Button(self.downloader_frame, text="Download", command=self.run_downloader)
        download_button.pack(anchor='e', **LG_PADDING)
        return self.downloader_frame

    def run_downloader(self):
        self.config = load_config()

        url = self.config['url']
        username = self.config['username']
        apikey = self.config['apikey_read']

        incident_num = self.downloader_incident_num.get()
        max_score = self.downloader_max_score.get()
        download_path = self.downloader_download_path.get()
        upload_path = self.downloader_upload_path.get()

        command = f"al-incident-downloader --url={url} --username=\"{username}\" --apikey=\"{apikey}\" --incident_num={incident_num} --max_score={max_score} --download_path=\"{download_path}\" --upload_path=\"{upload_path}\""
        command = add_options_to_command(command, self.downloader_options)
        command = add_flags_to_command(command, self.downloader_flags)
        run_command(command)

