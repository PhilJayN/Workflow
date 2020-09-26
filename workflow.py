import pyautogui
import pygetwindow as gw
import time
import webbrowser
import subprocess
import json
import PySimpleGUI as sg

########################### Load / Save Settings ###########################
def loadDB():
    with open('db.json', 'r') as f:
        data = json.load(f)
        # Return db.json to use in other fxns
    return data

# access DB, them dump to it
# def saveSettings(dictValues):
#     #dictValues looks like: {'web_sites': 'a', 'web_sites0': 'b'}, access using dictValues['web_sites0'], NOT index num
#     # print('dictValues accessing w/ key set in PySimpleGUI layout code:', dictValues['web_sites0'])
#     with open('db.json', 'r+') as f:
#         data = json.load(f)
#         # go through .json file structure:
#         for index in range(0,3):
#             data["sites"][index]["url"] = dictValues['web_sites' + str(index)]
#             f.seek(0)        # <--- should reset file position to the beginning.
#             json.dump(data, f, indent=2)
#             f.truncate()     # remove remaining part
#     # sg.popup('Saved!')


# responsible for cleaning (put str into array) user input and prep to put into DB, and in future, verifying it
def parseUserInput(input):
    print('input looks like:', input['-SITES TEXTBOX-'], type(input))
    with open('db.json', 'r+') as f:
        data = json.load(f)
        for index in range(0,3):

            arr = input['-SITES TEXTBOX-'].split()
            data["sites"][index]["url"] = arr[index]

            foldersArr = input['-FOLDERS TEXTBOX-'].split()
            data["folders"][index]["path"] = foldersArr[index]

            def writeToDB():
                f.seek(0)        # <--- should reset file position to the beginning.
                json.dump(data, f, indent=2)
                f.truncate()     # remove remaining part

            writeToDB()


# Needs access to window, pulls data from db, changes to strings, then displays to UI
def render():
    window = createMainWindow()
    # repeated variable, requires is render fxn is outside in its own scope
    db = loadDB()
    sitesStr = ""
    foldersStr = ""
    for index in range(0,3):
        sitesStr = sitesStr + db["sites"][index]["url"] + '\n\n'
        foldersStr = foldersStr + db["folders"][index]["path"] + '\n\n'

    window['-SITES TEXTBOX-'].update(sitesStr)
    window['-FOLDERS TEXTBOX-'].update(foldersStr)


########################### GUI ###########################
def createMainWindow():
    sg.theme('DarkAmber')

    layout = [
    [sg.Text('Apps')],
    [sg.Multiline(size=(40, 5), key='-APPS TEXTBOX-', font='Any 14')],
    [sg.Text('Folders')],
    [sg.Multiline(size=(40, 5), key='-FOLDERS TEXTBOX-', font='Any 14')],
    [sg.Text('Sites')],
    [sg.Multiline(size=(20, 5), key='-SITES TEXTBOX-', font='Any 20')],
    [sg.Button('Save'), sg.Button('Exit')] ]

    return sg.Window('App Title', layout, finalize=True)


def main():
    # this window object right now should have no user value, it's coming from createMainWindow fxn
    window = createMainWindow()
    # print('window obj:', window.read())


    render()
    # Event Loop, gets values of inputs
    while True:
        # reads the user input that you see in the GUI
        event, values = window.read()
        print('event loop value dict:', values)
        # print('values from user:', values['-SITES TEXTBOX-'])

        parseUserInput(values)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
            window.close()


# parseUserInput(values)


main()



# TEMPORARY FUNCTION CALLERS 123
def functionHandlers():
    openSites()
    openFolders(requestedFolders)

# functionHandlers()

# loadDB()














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











# Cross platform open folders
# def openDirXPlatform():
#     import webbrowser
#     path = r'C:\Users\asus270\Evernote'
#     webbrowser.open('file:///' + path)
#
# openDirXPlatform()
