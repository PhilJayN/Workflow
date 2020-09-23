import pyautogui
import pygetwindow as gw
import time
import webbrowser
import subprocess
import json
import PySimpleGUI as sg


def writeToDb(dictValues):
    # print('you called writeToDb with dictValues', dictValues["web_sites"])
    #dictValues looks like: {'web_sites': 'a', 'web_sites0': 'b'}, access using dictValues['web_sites0'], NOT index num
    print('dictValues full:', dictValues)
    print('dictValues accessing w/ key set in PySimpleGUI layout code:', dictValues['web_sites0'])

    with open('db.json', 'r+') as f:
        data = json.load(f)
        # print(data["people"][0]["name"])
        for iii in range(0,2):
            # go through .json file structure:
            data["sites"][iii]["url"] = dictValues['web_sites' + str(iii)]
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f, indent=2)
            f.truncate()     # remove remaining part

def startGUI():
    sg.theme('DarkAmber')
    layout = [  [sg.Text('Your Sites')],
    [sg.Text('0'), sg.InputText('', key='web_sites0')],
    [sg.Text('1'), sg.InputText('', key='web_sites1')],
    # [sg.Text('Folders'), sg.InputText()],
    [sg.Button('Save'), sg.Button('Cancel')] ]

    window = sg.Window('Workflow', layout)
    # Event Loop, gets values of inputs
    while True:
        event, values = window.read()
        print('even loop value dict:', values)
        # print('data stuff:', type(values), values, 'len:', len(values))
        print('values:', values)

        writeToDb(values)

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
            window.close()
            # db only updates when user closes the GUI??

startGUI()

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



def click(btnPos):
    loginBtn = [1707, 682]
    wpBtn = [2700, 248]

    pyautogui.click(btnPos[0], btnPos[1], duration=.3)

# time.sleep(2)
# click(loginBtn)
# time.sleep(25)
# click(wpBtn)


# TEMPORARY FUNCTION CALLERS
def functionHandlers():
    openSites()
    openFolders(requestedFolders)

# functionHandlers()




# Cross platform open folders
# def openDirXPlatform():
#     import webbrowser
#     path = r'C:\Users\asus270\Evernote'
#     webbrowser.open('file:///' + path)
#
# openDirXPlatform()
