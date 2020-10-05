import pyautogui
import pygetwindow as gw
import time
import webbrowser
import subprocess
import json
import PySimpleGUI as sg

########################### TEMPORARY FXN ###########################
def closeTabs(x):
    for i in range(0,x):
        pyautogui.hotkey('ctrl', 'w')
        # sleep a bit or else ctrl+w pressed too fast in sucession!
        time.sleep(.4)

def altF4(x):
    for i in range(0,x):
        pyautogui.hotkey('alt', 'f4')
        # sleep a bit or else pressed too fast in sucession!
        time.sleep(.4)

def sleep(sec):
    print('sleep started')
    time.sleep(sec)
    print('sleep done')

def maxWindow():
    window = gw.getActiveWindow()
    window.maximize()

def minWindow():
    window = gw.getActiveWindow()
    window.minimize()

########################### HELPER FXNS ###########################
def loadDB():
    with open('db.json', 'r') as f:
        data = json.load(f)
        # Return db.json to use in other fxns
    return data

def rmNewlines(string):
    # removes newline at middle of string, as .strip() does not do that
    return string.replace('\n',' ')

def mrClean():
    print('Done cleaning string!')
########################### ACTIONS / EVENTS  ###########################
# X can be apps, folders, or sites
def openX():
    db = loadDB()
    key = ["apps", "folders", "sites"]
    for index in range(0,3):
        for item in db[key[index]]: #db[key[index]] is db["apps"]
            #loop will go thru one item at a time, run to if/else and eval that
            #then go back and do second item, till all items are done.
            #ea. item is one dict in list {'path': 'C:\\Program Files\\Mozilla'}
            # find path values:
            pathStr = item["path"]
            if key[index] == "apps":
                print('running apps placeholder...', pathStr)
                subprocess.Popen(pathStr)
                # testing purposes
                sleep(1.8)
                altF4(1)
            elif key[index] == "folders":
                #if a drive (D:\ E:\) is invalid, webbrowser opens IE!
                print('running folders placeholder...')
                webbrowser.open(pathStr)
                sleep(1.8)
                altF4(1)
            elif key[index] == "sites":
                # if there's two \\ slashes, then IE will open!
                webbrowser.open(pathStr)
                print('running webbrowser cmd to...', pathStr)
                # webbrowser.get('windows-default').open(pathStr, new=1)
                sleep(1.8)
                closeTabs(2)
        sleep(1)
########################### Load / Save / Parse ###########################
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
comboList = ['Python', 'JavaScript', 'Jobs']
def createMainWindow():
    sg.theme('DarkAmber')

    layout = [
    [sg.Text('Apps')],
    [sg.Multiline(size=(40, 10), key='-APPS TEXTBOX-', font='Any 14')],
    [sg.Text('Folders')],
    [sg.Multiline(size=(40, 10), key='-FOLDERS TEXTBOX-', font='Any 14')],
    [sg.Text('Sites')],
    [sg.Multiline(size=(40, 10), key='-SITES TEXTBOX-', font='Any 14')],
    [sg.Text('Select Workflow'), sg.Combo(comboList, size=(40, 30), key='-COMBO LIST-'), sg.Button('Load'), sg.Button('Launch!')],
    [sg.Button('Open All')],
    [sg.Button('Save'), sg.Button('Exit')]
    ]

    return sg.Window('App Title', layout, finalize=True)
# print('combo', type(sg.theme_list()), len(sg.theme_list()) )

def main():
    # this window object right now should have no user value
    window = createMainWindow()
    # Needs access to window obj
    def render():
        # gets data from DB, puts into a long string, then displays to GUI
        db = loadDB()
        appsStr = ""
        foldersStr = ""
        sitesStr = ""
        for index in range(0,3):
            try:
                appsStr += db["apps"][index]["path"] + '\n\n'
                foldersStr += db["folders"][index]["path"] + '\n\n'
                sitesStr += db["sites"][index]["path"] + '\n\n'
                # print('str @ index :', index, foldersStr)
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
        def checkEventBtn():
            # print('event clicked:', event)
            if event == 'Open Apps':
                print('open apps~!')
            # elif event == 'Open Folders':
            # elif event == 'Open Sites':
            elif event == 'Open All':
                openX()
        checkEventBtn()

# TEMPORARY FUNCTION CALLERS 123
def functionHandlers():
    openSites()
    openFolders(requestedFolders)

# functionHandlers()
main()


########################### TEMP FXN ###########################

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

#
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
