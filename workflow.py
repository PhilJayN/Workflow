import pyautogui
import pygetwindow as gw
import time
import webbrowser
import subprocess
import json
import PySimpleGUI as sg

########################### ACTIONS / EVENTS  ###########################
# Cross platform open folders
def openDirXPlatform():
    path = r'C:\Users\asus270\Evernote'
    webbrowser.open('file:///' + path)

def closeTabs():
    # temp close tabs
    for i in range(0,7):
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(.5)

########################### Load / Save / Parse ###########################
def loadDB():
    with open('db.json', 'r') as f:
        data = json.load(f)
        # Return db.json to use in other fxns
    return data

# cleans (put str into array) user input, puts into DB, and in future, verifying it
def parseUserInput(input):
    with open('db.json', 'r+') as f:
        db = json.load(f)
        # logging.info(db)

        def count():
            count = []
            # item is "apps", or "folders", etc...
            for item in db:
                count.append(len(db[item]))
            return count
        # logging.info(type(count()))
        c = count()

        def modifyData(count, key, data):
            # print('modifyData running @: ', num)
            # Run loop depending on number of items in db list

            # print('foldersArr:', foldersArr)
            for ii in range(0,count):
                # db[key][ii]["path"] = "ffff"
                # arr = input['-SITES TEXTBOX-'].split()
                # db[key][ii]["path"] = arr[ii]
                print('data assigned:', data[ii])
                # data[ii] will run into "index out of range", if GUI value is empty!!
                db[key][ii]["path"] = data[ii]

        def getParam():
            count = c # [3,3,2]
            # print('tak', count)
            key = ["apps", "folders", "sites"]
            appsArr = input['-APPS TEXTBOX-'].split()
            foldersArr = input['-FOLDERS TEXTBOX-'].split()
            sitesArr = input['-SITES TEXTBOX-'].split()
            dataArr = [appsArr, foldersArr, sitesArr]

            # Run modifyData 3x there are 3 keys, which won't change
            for x in range(0,3):
                modifyData(count[x], key[x], dataArr[x])
        getParam()

        def writeToDB():
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(db, f, indent=2)
            f.truncate()     # remove remaining part
        writeToDB()

########################### GUI ###########################
def createMainWindow():
    sg.theme('DarkAmber')

    layout = [
    [sg.Text('Apps')],
    [sg.Multiline(size=(40, 5), key='-APPS TEXTBOX-', font='Any 14')],
    [sg.Text('Folders')],
    [sg.Multiline(size=(40, 5), key='-FOLDERS TEXTBOX-', font='Any 14')],
    [sg.Text('Sites')],
    [sg.Multiline(size=(40, 5), key='-SITES TEXTBOX-', font='Any 20')],
    [sg.Button('Open Apps')],
    [sg.Button('Open Folders')],
    [sg.Button('Open Sites')],
    [sg.Button('Open All')],
    [sg.Button('Save'), sg.Button('Exit')]
    ]

    return sg.Window('App Title', layout, finalize=True)

# def count():
#     db = loadDB()
#     print('db:', db, 'len of apps', len(db['apps']), 'len of db:', len(db))
#     count = []
#     # item is "apps", or "folders", etc...
#     for item in db:
#         print('item in db', item)
#         count.append(len(db[item]))
#     print('count array is:', count)
#     return count
# count()

def main():
    # this window object right now should have no user value
    window = createMainWindow()
    # Needs access to window obj
    def render():
        # gets data from DB, puts into a long string, then displays to GUI
        db = loadDB()
        appsStr = ""
        sitesStr = ""
        foldersStr = ""
        for index in range(0,3):
            try:
                print('current index:', index)
                appsStr += db["apps"][index]["path"] + '\n\n'
                foldersStr += db["folders"][index]["path"] + '\n\n'
                sitesStr += db["sites"][index]["path"] + '\n\n'
            except IndexError:
                pass
            continue

        window['-APPS TEXTBOX-'].update(appsStr)
        window['-FOLDERS TEXTBOX-'].update(foldersStr)
        window['-SITES TEXTBOX-'].update(sitesStr)
    render()

    # X can be apps, folders, or sites
    def openX():
        db = loadDB()
        # Open apps
        # for index in range(0,3):
        #     path = db["apps"][index]["path"]
        #     webbrowser.open('file:///' + path)
        for index in range(0,3):
            # Open folders
            path = db["folders"][index]["path"]
            # print('file:///' + path)
            webbrowser.open('file:///' + path)

            # # Open sites
            url = db["sites"][index]["url"]
            webbrowser.get('windows-default').open(url, new=1)

        # closeTabs()
    while True:
        # reads the user input that you see in the GUI
        event, values = window.read()
        # print('event loop value dict:', values)

        parseUserInput(values)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
            window.close()

        if event == 'Open All':
            openX()
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


#
# def openDirXPlatform():
#     path = r'C:\Users\asus270\Evernote'
#     ted = 'file:///' + path
#     webbrowser.open('file:///' + path)
#     print('full', ted )
#     # webbrowser.open('www.one.com')
#
# openDirXPlatform()


# def count():
#     db = loadDB()
#     a = len(db["apps"])
#     f = len(db["folders"])
#     s = len(db["sites"])
#     print(a)
# count()
