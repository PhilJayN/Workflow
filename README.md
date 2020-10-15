# Workflow
- A Python GUI to launch applications, folders, and web sites.

![Image of Program](https://github.com/PhilJayN/Images/blob/main/Workflow.PNG)

## Platform
Created and tested on Windows 10. Mac (opening web sites can be glitchy) and Linux is a work in progress.

## Index
- [About](#about)
- [Usage](#usage)
  - [Installation](#installation-for-beginners)
- [Development](#development)
- [Build](#build)

## About
Do you switch projects often? Do you dread having to manually open applications, navigate to various folders, and launch web sites? No need to do that anymore.

## Usage
Copy and paste paths in the input boxes. Websites do not need to have "www" in it, as the program will
auto add that. Best method is to navigate to a site on your browser, then copy and paste to avoid typos.

Every paths should have a newline. Not only is it easier for the eyes, but there is a known bug without a new line.
### Windows 10
To find paths for a folder, right click on folder, then click properties, then copy the path in the "Location"

### Mac OS
Mac OS application names can be found in your "Applications" folder. For example, the standard
path for Firefox is
```
/Applications/Firefox.app
```
You can change the program name to anything you need, as long as the program is installed,
like so:
```
/Applications/iTunes.app
```
Folder paths look like this:
```
Users/yourUserName/Desktop/Workflow-mac
```

### Linux
In progress

### Installation for beginners
- Install Python 3 (.exe will be available soon)
- Install [pip](https://pip.pypa.io/en/stable/installing/) (module installer to install dependencies).
"pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from python.org"
```
pip install PySimpleGUI
```
- Download and extract zip file contents anywhere you want.
- Run the workflow.py. DONE.
- If doesn't work, open a terminal window, navigate to project directory, run command to launch program:
```
python workflow.py

```

## Development
If you want to contribute, even if you are a beginner, feel free to do so.

### Build
.exe file currently in progress
