import pyautogui
import pygetwindow as gw
import time
import webbrowser
import subprocess
import json
import PySimpleGUI as sg

########################### MISC ###########################
def rmNewlines(string):
    # removes newline at middle of string, as .strip() does not do that
    return string.replace('\n',' ')
########################### ACTIONS / EVENTS  ###########################
# Cross platform open folders
def openDirXPlatform():
    # if there's two slashes, then IE will open!
    path = r'C:\Program Files\Mozilla Firefox'
    webbrowser.open('file:///' + path)

def closeTabs():
    # temp close tabs
    for i in range(0,7):
        pyautogui.hotkey('ctrl', 'w')
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

# X can be apps, folders, or sites
def openX():
    db = loadDB()
    key = ["apps", "folders", "sites"]
    # newData = ["one", "two", "three"]
    for index in range(0,3):
        # print('current key: ', key[index])
        for item in db[key[index]]:
            # find path values:
            pathStr = item["path"]
            if key[index] == "apps":
                # subprocess.Popen(pathStr)
                print('opening apps placeholder...')
            elif key[index] == "folders":
                webbrowser.open('file:///' + pathStr)
            elif key[index] == "sites":
                webbrowser.open(pathStr)
                # webbrowser.get('windows-default').open(url, new=1)
        time.sleep(.7)
########################### Load / Save / Parse ###########################
def loadDB():
    with open('db.json', 'r') as f:
        data = json.load(f)
        # Return db.json to use in other fxns
    return data

# cleans (put str into array) user input, puts into DB, and in future, verifying it
def parseUserInput(values):
    with open('db.json', 'r+') as f:
        db = json.load(f)
        def count():
            count = []
            # item is "apps", or "folders", etc...
            for item in db:
                count.append(len(db[item]))
            return count
        c = count()

        def modifyData(count, key, data):
            # Run loop depending on number of items in db list
            # print('foldersArr:', foldersArr)
            for ii in range(0,count):
                # print('data assigned:', data[ii])
                # data[ii] will run into "index out of range", if GUI value is empty!!
                db[key][ii]["path"] = data[ii]

        def getParam():
            count = c # [3,3,2]
            key = ["apps", "folders", "sites"]
            # get values from GUI boxes:
            appsArr = rmNewlines(values['-APPS TEXTBOX-']).split("  ")
            foldersArr = rmNewlines(values['-FOLDERS TEXTBOX-']).split("  ")
            # print('apps values:', values['-APPS TEXTBOX-'], 'folders values: ', values['-FOLDERS TEXTBOX-'])
            sitesArr = rmNewlines(values['-SITES TEXTBOX-']).split("  ")
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

def main():
    # this window object right now should have no user value
    # is the fxn being called now?
    window = createMainWindow()
    # Needs access to window obj
    def render():
        # gets data from DB, puts into a long string, then displays to GUI
        db = loadDB()
        # will end up as a long string:
        appsStr = ""
        foldersStr = ""
        sitesStr = ""
        for index in range(0,3):
            try:
                appsStr += db["apps"][index]["path"] + '\n\n'

                foldersStr += db["folders"][index]["path"] + '\n\n'
                # print('str @ index :', index, foldersStr)
                sitesStr += db["sites"][index]["path"] + '\n\n'
            except IndexError:
                pass
            continue
        # print('appsStr final :', appsStr)
        window['-APPS TEXTBOX-'].update(appsStr)
        window['-FOLDERS TEXTBOX-'].update(foldersStr)
        window['-SITES TEXTBOX-'].update(sitesStr)
    render()

    while True:
        # reads the user input that you see in the GUI
        #values is a dict
        event, values = window.read()

        parseUserInput(values)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
            window.close()

        ########## EVENTS #########
        def checkEvent():
            # print('event clicked:', event)
            if event == 'Open Apps':
                print('open apps~!')
            # elif event == 'Open Folders':
            # elif event == 'Open Sites':
            elif event == 'Open All':
                openX()
                print('test')
        checkEvent()

# TEMPORARY FUNCTION CALLERS 123
def functionHandlers():
    openSites()
    openFolders(requestedFolders)
# functionHandlers()
main()


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

def closePrograms():
    subprocess.call([r'C:\Program Files\Mozilla Firefox\\firefox.exe'])
    time.sleep(1)

    # how to make sure all programs data saved, and not lose work? (ex word doc)
    askToExit = input('Type x and press ENTER key to exit and CLOSE all programs and folders you opened: ')

    if askToExit == 'x':
        subprocess.call(["taskkill","/F","/IM","firefox.exe"])

        print('Exiting')
        time.sleep(.5)


# requestedSites = ['https://www.udemy.com/course/automate/learn/lecture/3465864#questions/11019006',
#                 'https://automatetheboringstuff.com/2e/'
#                 ]
#
# def openSites():
#     for i in range(len(requestedSites)):
#         print(i)
#         webbrowser.open(requestedSites[i], new=1)
#         time.sleep(.3)
#         maxWindow()
#         time.sleep(1)
#     closeTabs()
#
# requestedFolders = ['D:\\tcg', 'C:\\Users\\asus270', 'C:\\Dropbox\\~Programming\\projects']
#
# def openFolders(folders):
#     for i in range(len(requestedFolders)):
#         subprocess.Popen(r'explorer ' + requestedFolders[i])
#         print('req. folders:', requestedFolders[i])



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
