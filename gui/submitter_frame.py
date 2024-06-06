from tkinter import Frame, Label, OptionMenu, StringVar, ttk

from tooltip import CreateToolTip
from gui_helper_fns import LG_PADDING, SM_PADDING, add_flags_to_command, add_options_to_command, create_checkbox, create_file_input, create_input, create_number_input, load_config, run_command

class SubmitterFrame: 
    def __init__(self, parent, config, advanced):
        self.advanced = advanced
        self.config= config
        self.parent = parent
        self.classifications = ('TLP:CLEAR', 'TLP:GREEN', 'TLP:AMBER', 'TLP:AMBER+STRICT')
        self.submitter_flags: dict = {}
        self.submitter_options: dict = {}
        self.frame = self.create_submitter_frame(parent)
   
         
    def get_frame(self):
        return self.frame

    def create_submitter_frame(self, parent):
        self.submitter_frame = Frame(parent)
        self.submitter_required_frame = ttk.LabelFrame(self.submitter_frame, text='Required')
        self.submitter_optional_frame = ttk.LabelFrame(self.submitter_frame, text='Optional')
       
        #
        # Required Params
        #
        self.submitter_path = create_file_input(self.submitter_required_frame, "* Path to scan:", is_directory=True)
        CreateToolTip(self.submitter_path, text='The directory path containing files that you want to submit to Assemblyline.')

        self.classifier = StringVar()
        self.class_frame = Frame(self.submitter_required_frame)
        self.class_frame.pack(fill="x", pady=2)
        class_label = Label(self.class_frame, text="* Classification", width=20, anchor="w")
        class_label.pack(side="left")
        self.submitter_classification = ttk.OptionMenu(self.class_frame, self.classifier, self.classifications[0], *self.classifications) # Add proper classifications here
        self.submitter_classification.pack(side="right", fill="x", expand=True, **SM_PADDING)
        
        #to change classification to a text input rather than the dropdown, comment out the above chunk of code and uncomment this next line
        #self.submitter_classification = create_input(self.submitter_required_frame, "* Classification:")
        CreateToolTip(self.submitter_classification, text='The classification level for each file submitted to Assemblyline.')

        self.submitter_incident_num = create_input(self.submitter_required_frame, "* Incident Number:")
        CreateToolTip(self.submitter_incident_num, text='The incident number for each file to be associated with.')

        submitter_required = ttk.Separator(self.submitter_frame, orient='horizontal')
        submitter_required.pack(**LG_PADDING)

        #
        # Optional Params
        #
        self.submitter_ttl = create_input(self.submitter_optional_frame, 'TTL:')
        CreateToolTip(self.submitter_ttl, text='The amount of time that you want your Assemblyline submissions to live on the Assemblyline system (in days).')
        self.submitter_options['--ttl'] = self.submitter_ttl

        ## some form of multiselect? right now is a comma-separated list (no spaces). Might need assemblyline api
        self.submitter_service_selection = create_input(self.submitter_optional_frame, 'Services:')   
        CreateToolTip(self.submitter_service_selection, text='A comma-separated list (no spaces!) of service names (case-sensitive) to send files to. If not provided, all services will be selected.')
        self.submitter_options['--service_selection'] = self.submitter_service_selection

        self.submitter_thread_count = create_number_input(self.submitter_optional_frame, 'Ingestion Threads:')
        CreateToolTip(self.submitter_thread_count, text='Number of threads that will ingest files to Assemblyline.')
        self.submitter_options['--threads'] = self.submitter_thread_count

        self.submitter_priority = create_input(self.submitter_optional_frame, 'Priority:')
        CreateToolTip(self.submitter_priority, text='Provide a priority number which will cause the ingestion to go to a specific priority queue.')
        self.submitter_options['--priority'] = self.submitter_priority

        #
        # Optional Flags
        #
        flag_label = ttk.Label(self.submitter_optional_frame, text='Flags:')
        flag_label.pack(anchor='w')
        self.submitter_fresh = create_checkbox(self.submitter_optional_frame, 'Fresh Submission', flag='-f' , flag_dict=self.submitter_flags)
        CreateToolTip(self.submitter_fresh, text='Restart ingestion from the beginning.')        

        self.submitter_resubmit_dynamic = create_checkbox(self.submitter_optional_frame, 'Resubmit Dynamic', flag='--resubmit-dynamic', flag_dict=self.submitter_flags)
        CreateToolTip(self.submitter_resubmit_dynamic, text='All files that score higher than 500 will be resubmitted for dynamic analysis.')

        self.submitter_alerts = create_checkbox(self.submitter_optional_frame, 'Generate Alerts', flag='--alert', flag_dict=self.submitter_flags)
        CreateToolTip(self.submitter_alerts, text='Generate alerts for this submission.')

        self.submitter_dedupe_hashes = create_checkbox(self.submitter_optional_frame, 'Dedup Hashes', flag='--dedup_hashes', flag_dict=self.submitter_flags)
        CreateToolTip(self.submitter_dedupe_hashes, text='Only submit files with unique hashes. If you want 100% file coverage in a given path, do not use this flag')

        self.submitter_do_not_verify_ssl = create_checkbox(self.submitter_optional_frame, 'Do Not Verify SSL On Submit', flag='--do-not-verify-ssl', flag_dict=self.submitter_flags)
        CreateToolTip(self.submitter_do_not_verify_ssl, text='Ignore SSL errors (insecure!)')

        ## pack the frames and submit button
        self.submitter_required_frame.pack(**LG_PADDING, fill='both')
        if(self.advanced == 1):
            self.submitter_optional_frame.pack(fill='both', **LG_PADDING)


        submit_button = ttk.Button(self.submitter_frame, text="Submit", command=self.run_submitter)
        submit_button.pack(anchor='e', **LG_PADDING)

        self.submitter_frame.pack( fill='both', **LG_PADDING)
        return self.submitter_frame

    def run_submitter(self):
        self.config = load_config() #refresh config

        url = self.config['url']
        username = self.config['username']
        apikey = self.config['apikey_write']

        path = self.submitter_path.get()
        #classification = self.submitter_classification.get()
        classification = self.classifier.get()
        incident_num = self.submitter_incident_num.get()


        command = f"al-incident-submitter --url={url} --username=\"{username}\" --apikey=\"{apikey}\" --path=\"{path}\" --classification={classification} --incident_num={str(incident_num)}"
        command = add_options_to_command(command, self.submitter_options)
        command = add_flags_to_command(command, self.submitter_flags)

        run_command(command)