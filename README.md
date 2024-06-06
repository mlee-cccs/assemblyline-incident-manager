# Assemblyline Incident Manager GUI
This program is a standalone GUI built to interact with the Assemblyline Incident Manager (ALIM) scripts. 
See: https://github.com/CybercentreCanada/assemblyline-incident-manager 

The repo was cloned from the above link, and all new files are contained within the assemblyline_incident_manager/gui folder. 

The gui/dist/ALIM folder contains everything needed to run the executable and connect to an Assemblyline instance with minimal user setup.
- simply run the ALIM.exe

NOTE: This application is mainly a proof-of-concept and likely contains bugs or other odd behaviour. If things aren't working as intended, try closing and restarting the application.

## Getting started
The ALIM.py file is the main file to run the gui. The executable has been generated using pyinstaller on the ALIM.py which creates the build and dist folders. 

The gui itself does not require the assemblyline_incident_manager files to run, it simply calls the scripts using a subprocess. 
The ALIM.py file itself will be functional if the assemblyline incident manager has been pip installed 

To compile the application from the ALIM.py file into a .exe, I used pyinstaller. The resulting exe will be in the dist folder. 
NOTE: You may need to move the crane.png to be in the same folder as the exe, or change the file path in the ALIM.py file.
```
pyinstaller ALIM.py --hideconsole --collect-data TKinterModernThemes
```

## Required Files
Crane.png - currently needs to be in the same folder as the ALIM.exe.
ALIM_config.json - will be created the first time the exe is executed. 
The report.csv and log files will be created by the application and scripts themselves.

## Usage
The application has the same functionality as the ALIM scripts, with improved usability.
See https://github.com/CybercentreCanada/assemblyline-incident-manager?tab=readme-ov-file#usage for more details on the underlying script usage 

- Ability to rerun scripts more easily on failure, without having to re-enter parameters.
- Easier to edit inputs, with reduced input errors.
  - number inputs only accept numerical characters.
  - Using the file explorer for file paths eliminates incorrect path entries.
- Easier to setup on a (compromised) machine as the executable contains all scripts and necessary python packages. No python or pip install necessary.  

## Example Usecase
Incident Response:
The application will be added to a compromised machine, and a clean machine.

On the compromised machine, a user will input their assemblyline instance url, username, and the path to the api key(write access). 

From the submitter tab, a user will select the path of the folder to submit, enter an incident number, and the submitter script will bulk upload all files to the assemblyline instance to be assessed. 

On the clean machine, a user enters the same assemblyline instance url, username, and the path to the apikey(read access). A user can select the analyzer tab to generate and view a csv report of the incident. The user is then able to use the downloader tab to redownload files under a certain score directly from assemblyline. 

## Codebase 
The GUI was built using Tkinter

The ALIM.py contains the main setup for the application as well as the tab structure creation and callback functions for various components

Each ALIM script has an associated file and frame within the gui 
- submitter_frame.py
- analyzer_frame.py
- downloader_frame.py

Additionally, a settings frame has been added to save some of the configuration used for all of the scripts. 

ALIM_config.json contains:
- the url of the assemblyline instance
- the username of the user on assemblyline 
- a path to the api keys (read and write) : Recommended to use two keys to reduce the exposure of the assemblyline instance to a compromised machine.

Some addition components that are included:
- tooltip.py : Hover tooltips to display the helptips for each available input option
- theme_switcher.py : Switch between light and dark mode
- advanced_options.py : Hide/Show optional inputs 

The gui_helper_fns.py contains most of the functions to create the inputs, as well as some helper functions to build the command being called. 

## Next Steps
- There are various bugs and odd behaviour to still be fixed in this iteration of the ALIM gui. Tkinter requires a lot of functionality to be manually built (e.g. resizable/scrollable windows).

- There is currently no validation to check that required inputs are filled. The script will just fail, and a user will need to read the error to see what went wrong. It would be good to turn the frames into a form that verifies all required inputs are present before trying to run the script.

- The bundled exe is currently reliant on external files (crane.png, ALIM_config.json, report.csv)
    - There is likely a better way to bundle this so that these files are internal to the program

- The current version of the gui is built standalone and only calls the ALIM scripts. 
    - This application would be improved if it was rebuilt to include an Assemblyline python client, and call the script functions directly. (integrate the gui and scripts together into a single application)
    - This would enable the gui to use the assemblyline apis.
    - e.g. service-selection could query the assemblyline api and have a selectable gui of the available services instead of a manual string entry. 
    - classifications are currently hardcoded. Could also query the available options from the assemblyline instance. 
- Could add progress indicators to the script execution.
