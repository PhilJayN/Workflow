import pyautogui
import pygetwindow as gw
import time
import webbrowser
import subprocess
import json
import PySimpleGUI as sg

########################### Load / Save Settings ###########################
def loadSettings():
    with open('db.json', 'r') as f:
        data = json.load(f)
        # Return db.json to use in other fxns
    return data

# access DB, them dump to it
def saveSettings(dictValues):
    #dictValues looks like: {'web_sites': 'a', 'web_sites0': 'b'}, access using dictValues['web_sites0'], NOT index num
    # print('dictValues accessing w/ key set in PySimpleGUI layout code:', dictValues['web_sites0'])
    with open('db.json', 'r+') as f:
        data = json.load(f)
        # go through .json file structure:
        for index in range(0,3):
            data["sites"][index]["url"] = dictValues['web_sites' + str(index)]
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f, indent=2)
            f.truncate()     # remove remaining part
    # sg.popup('Saved!')

def parseUserInput(input):
    print('input looks like:', input['-SITES TEXTBOX-'], type(input))
    with open('db.json', 'r+') as f:
        data = json.load(f)
        for index in range(0,3):

            arr = input['-SITES TEXTBOX-'].split()
            data["sites"][index]["url"] = arr[index]

            foldersArr = input['-FOLDERS TEXTBOX-'].split()
            data["folders"][index]["path"] = foldersArr[index]

            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f, indent=2)
            f.truncate()     # remove remaining part
    # sg.popup('Saved!')


########################### GUI ###########################
def startGUI():
    sg.theme('DarkAmber')
    # testInput = [sg.Text('3'), sg.InputText('', key='web_sites3')]
    # testInput,
    layout = [
    # [sg.Text('0'), sg.InputText('', key='web_sites0', size=(20,45) )],
    # [sg.Text('1'), sg.InputText('', key='web_sites1')],
    # [sg.Text('2'), sg.InputText('', key='web_sites2'), sg.Multiline(size=(20, 5), key='-SITES TEXTBOX-', font='Any 20')],
    [sg.Text('Apps')],
    [sg.Multiline(size=(40, 5), key='-APPS TEXTBOX-', font='Any 14')],
    [sg.Text('Folders')],
    [sg.Multiline(size=(40, 5), key='-FOLDERS TEXTBOX-', font='Any 14')],
    [sg.Text('Sites')],
    [sg.Multiline(size=(20, 5), key='-SITES TEXTBOX-', font='Any 20')],
    [sg.Button('Save'), sg.Button('Exit')] ]

    window = sg.Window('Workflow', layout, finalize=True)
    print('loadSettings return val is the json db:', loadSettings())
    db = loadSettings()

    def render():
        # repeated variable, requires is render fxn is outside in its own scope
        db = loadSettings()
        sitesStr = ""
        foldersStr = ""
        for index in range(0,3):
            sitesStr = sitesStr + db["sites"][index]["url"] + '\n\n'
            foldersStr = foldersStr + db["folders"][index]["path"] + '\n\n'

        window['-SITES TEXTBOX-'].update(sitesStr)
        window['-FOLDERS TEXTBOX-'].update(foldersStr)

    render()


    # Event Loop, gets values of inputs
    while True:
        event, values = window.read()
        print('even loop value dict:', values)
        # print('values from user:', values)
        print('values from user:', values['-SITES TEXTBOX-'])

        # saveSettings(values)
        parseUserInput(values)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
            window.close()








########################### TEMP FXN ###########################
def maxWindow():
    window = gw.getActiveWindow()
    window.maximize()

def minWindow():
    window = gw.getActiveWindow()
    window.minimize()

def closeTabs():
    # temp close tabs
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(.3)
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1)
    minWindow()

def exitPrompt():
    askToExit = input('Type x and press ENTER key to exit and CLOSE all programs and folders you opened: ')

    if askToExit == 'x':
        subprocess.call(["taskkill","/F","/IM","firefox.exe"])

        print('Exiting')
        time.sleep(.5)

requestedSites = ['https://www.udemy.com/course/automate/learn/lecture/3465864#questions/11019006',
                'https://automatetheboringstuff.com/2e/'
                ]

def openSites():
    for i in range(len(requestedSites)):
        print(i)
        webbrowser.open(requestedSites[i], new=1)
        time.sleep(.3)
        maxWindow()
        time.sleep(1)
    closeTabs()

requestedFolders = ['D:\\tcg', 'C:\\Users\\asus270', 'C:\\Dropbox\\~Programming\\projects']

def openFolders(folders):
    for i in range(len(requestedFolders)):
        subprocess.Popen(r'explorer ' + requestedFolders[i])
        print('req. folders:', requestedFolders[i])

def closePrograms():
    subprocess.call([r'C:\Program Files\Mozilla Firefox\\firefox.exe'])
    time.sleep(1)

    # how to make sure all programs data saved, and not lose work? (ex word doc)
    askToExit = input('Type x and press ENTER key to exit and CLOSE all programs and folders you opened: ')

    if askToExit == 'x':
        subprocess.call(["taskkill","/F","/IM","firefox.exe"])

        print('Exiting')
        time.sleep(.5)

# TEMPORARY FUNCTION CALLERS 123
def functionHandlers():
    openSites()
    openFolders(requestedFolders)

# functionHandlers()

startGUI()
loadSettings()










# Cross platform open folders
# def openDirXPlatform():
#     import webbrowser
#     path = r'C:\Users\asus270\Evernote'
#     webbrowser.open('file:///' + path)
#
# openDirXPlatform()
