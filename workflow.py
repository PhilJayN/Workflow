import json
import pyautogui
import PySimpleGUI as sg
import pygetwindow as gw
import subprocess
import os
import time
import webbrowser

from sys import platform as pf

# DEFAULT_SETTINGS = {}
KEYS_TO_ELEMENT_KEYS = {'combo_list': '-COMBO LIST-', 'apps_textbox': '-APPS TEXTBOX-', 'folders_textbox': '-FOLDERS TEXTBOX-', 'sites_textbox': '-SITES TEXTBOX-'}
# print('SETTINGS_KEYS_TO_ELEMENT_KEYS dict', KEYS_TO_ELEMENT_KEYS)
# This dict has no combo_list
ELEMENTS_DICT = {'apps_textbox': '-APPS TEXTBOX-', 'folders_textbox': '-FOLDERS TEXTBOX-', 'sites_textbox': '-SITES TEXTBOX-'}

########################### TEMPORARY FXN ###########################
def closeTabs():
    # for i in range(0,x):
    pyautogui.hotkey('ctrl', 'w')
    # sleep a bit or else ctrl+w pressed too fast in sucession!
    time.sleep(.8)

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

def fname(arg):
    print('hiiii', arg )

########################### HELPER FXNS ###########################
# to be used in layout sg.Combo(), or as keys
def getComboList():
    db = loadDB()
    comboList = []
    for key in db:
        comboList.append(key)
    return comboList

def getTitle(values):
    title = values['-COMBO LIST-']
    return title

def getDB(task, key, value):
    with open('db.json', 'r+') as f:
        db = json.load(f)
        if task == 'del':
            del db[key]
        else:
            db[key] = value
        def writeToDB():
            f.seek(0)        # reset file position to the beginning
            json.dump(db, f, indent=2)
            f.truncate()     # remove remaining part
        writeToDB()

def loadDB():
    with open('db.json', 'r') as f:
        data = json.load(f)
        # Return db.json file to use in other fxns
    return data

def delete(window, values):
    print('del fxn run w values: ', values)
    title = values["-COMBO LIST-"]
    print('Title', title)

    db = loadDB()
    print('keysssss in db BEFORE del:: ', list(db))

    try:
        getDB('del', title, None)
    except:
        print('Deletion error!')
########################### TEMP during testing###########################
    time.sleep(2)
    tempValue = {
    "apps": [
      "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
      "example",
      "orange"
    ],
    "folders": [
      "C:\\Users\\asus270\\AppData\\Local\\Programs\\Python\\Python36-32",
      "D:\\Archive\\acr"
    ],
    "sites": [
      "www.reddit.com/r/all",
      "www.google.com"
    ]
  }
    getDB(None, "example", tempValue)
########################### TEMP ###########################

    newDb = loadDB()
    print('keysssss in db after del: ', list(newDb))
    # sg.popup('DELETED!')
    render(window, "blank") # render needs to be called with a new title, or else error no title found

    # window = createMainWindow()
    # calling this fxn will clear GUI data, BUT creates a new window above old one!!
    # needs to be called at end of delete() fxn, or else title will NOT be removed from dropdown
    # because createMainWindow will pull data from DB. in other words: remove data from DB first,
    # then call for a new window.

def rmNewlines(string):
    # removes newline at middle of string, as .strip() only remove spaces at beginning and end
    return string.replace('\n',' ').strip()

def cleanData(str):
    print('inside cleanData str: ', str)
    newStr = ""
    # ignore cleaning if http is present, such as when address is copied from Chrome address bar: https://pysimplegui.readthedocs.io
    # fun fact for nerds like me: Chrome 69 update no longer shows www
    if 'www' not in str:
        if 'http' not in str:
            newStr = 'www.' + str
            print('BOTH cleaning conditions met, so result: ', newStr)
    # cleanData will either return edited newStr, or None. Be careful when returning None, will write to db "Null"
    return newStr
########################### ACTIONS / EVENTS  ###########################
# open apps
def checkOS(key, item):
    if pf == "linux" or pf == "linux2":
        # xdg should work for both file and folders, on *nix
        print('On Linux!')
        if key == "apps":
            os.system("open " + item) # opens an app on Mac
        elif key == "folders":
            try:
                subprocess.Popen(["xdg-open", item])
                print('opened folders using XDG on linux success!')
            except:
                print('error, using webbrowser...')
                webbrowser.open('file:////' + item) # works for opening Mac directory
    elif pf == "darwin":
        print('On OS x!')
        if key == "apps":
            os.system("open " + item) # opens an app on Mac
        elif key == "folders":
            webbrowser.open('file:////' + item) # works for opening Mac directory
            # webbrowser.open('file:////Users/Phil/Desktop/Workflow-mac') #works for opening Mac directory
        # subprocess.Popen(["open", item])
        # os.system("open /Applications/Google\ Chrome.app")
        # os.system("open /Applications/TextEdit.app")
        # os.system("open /Applications/Automator.app")
        # print('using subprocess.run...')
        # print('using os.syst...')
        # print('using subprocess.call...')
        # subprocess.run('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        # os.system("""osascript -e 'tell app "Safari" to open'""")
        # subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "/Applications/TextEdit.app"])
        # CompletedProcess(args='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', returncode=0)
    elif pf == "win32":
        print('On Windows!')
        try:
            if key == "apps":
                subprocess.Popen(item)
            elif key == "folders":
                webbrowser.open(item)
        except:
            print('FileNotFoundError')

# X can be apps, folders, or sites
def openX(values):
    db = loadDB()
    title = getTitle(values)
    for key in db[title]: # dict of 3 items: "apps": [], "folders": [], "sites":[], key is apps, etc.
        for index, item in enumerate(db[title][key]): # go through each item in array
            # loop goes through one item at a time, runs to if/else, stays in inner loop until done w every item,
            # then goes back to outer loop, where key changes, rinse and repeat
            # print('INNER loop item at index ', index, ': ', item)
            if key == "apps":
                print('running apps placeholder...', item)
                # subprocess.Popen(item)
                # testing purposes
                checkOS(key, item)
                sleep(1.9)
                altF4(1)
            elif key == "folders":
                #if a drive (D:\ E:\) is invalid, webbrowser opens IE!
                # print('running folders placeholder...')
                checkOS(key, item)
                # webbrowser.open(item)
                sleep(1.2)
                altF4(1)
            elif key == "sites":
                # if there's two \\ slashes, then IE will open!
                print('running webbrowser.open...', item)
                webbrowser.get('windows-default').open(item, new=1)
                # webbrowser.open(item)
                sleep(2)
                closeTabs()
        sleep(1)
# openX()

########################### Load / Save ###########################
# cleans (put str into array) user input, puts into DB, and in future, verifying it
########################### GUI ###########################

def getInput(window, values):
    dbTemplate =  {"apps": [], "folders": [], "sites": []}
    templateKey = list(dbTemplate)
    title = getTitle(values)
    # ELEMENTS_DICT = {'apps_textbox': '-APPS TEXTBOX-', 'folders_textbox': '-FOLDERS TEXTBOX-', 'sites_textbox': '-SITES TEXTBOX-'}
    # purpose: targets elements on GUI and gets user data from input boxes
    for ind, key in enumerate(ELEMENTS_DICT): #key: 'apps_textbox', ELEMENTS_DICT[key] eval. hardcoded keys specified in layout
        newArr = rmNewlines(values[ELEMENTS_DICT[key]]).split("  ") # is now an array: ['apple', 'nuts', 'orange']
        # now add every item from processed array into template, one at a time
        # print('newArr', newArr, 'indxxxxx. curr:', ind)
        for index, item in enumerate(newArr):
            # print('current item', item, 'hardKey[ind]:', hardKey[ind])
            if templateKey[ind] == 'sites':
                cleanedItem = cleanData(item)
                # print('templateKey[ind] is now sites!', 'cleanedItem:', cleanedItem == "")
                # cleanData() can return an empty string, if so, just put into template the unmodified item in array
                # otherwise put in the cleanedItem
                if cleanedItem == "":
                    dbTemplate[templateKey[ind]].append(item)
                else:
                    dbTemplate[templateKey[ind]].append(cleanedItem)
            # this else is for other keys ("apps", "folders") to use
            else:
                dbTemplate[templateKey[ind]].append(item)
    # print('dbTemplate FINAL', dbTemplate)
    getDB(None, title, dbTemplate)
    # render needs to run here to "refresh GUI" after calling cleanData, or else GUI won't updated
    render(window, getTitle(values))

def createMainWindow():
    comboList = getComboList()
    sg.theme('DarkAmber')

    layout = [
    [sg.T('1. Select Workflow'), sg.Combo(comboList, size=(40, 30), key='-COMBO LIST-')],
    [sg.T('2.'), sg.B('Load')],
    [sg.T('3.'), sg.B('Open All'), sg.T('Apps, Folders, Sites')],
    [sg.T('3.'), sg.B('Save'), sg.T('or'), sg.B('DELETE')],
    [sg.B('Exit')],
    [sg.Text('_'*60)],
    [sg.T('Apps')],
    [sg.Multiline(size=(40, 10), key='-APPS TEXTBOX-', font='Any 14')],
    [sg.T('Folders')],
    [sg.Multiline(size=(40, 10), key='-FOLDERS TEXTBOX-', font='Any 14')],
    [sg.T('Sites')],
    [sg.Multiline(size=(40, 10), key='-SITES TEXTBOX-', font='Any 14')]
    ]

    window = sg.Window('App Title', layout, finalize=True)
    return window

# gets data from DB, puts into a long string, then displays to GUI
def getDataForRender(title):
    db = loadDB()
    if db["metadata"] == "new":
        getDB("modify", "metadata", "old")
        return {'combo_list': 'example', 'apps_textbox': 'pathtoapps', 'folders_textbox': 'apthffff', 'sites_textbox': 'testsgd'}
    else:
        titleStr = title
        appsStr = ""
        foldersStr = ""
        sitesStr = ""
        # outer loop responsible for key
        for key in db[titleStr]:
            # inner loop responsible for going through array w/ dynamic num. of items
            for item in db[titleStr][key]:
                # print('iteemmm', item)
                if key == "apps":
                    appsStr += item + '\n\n'
                elif key == "folders":
                    foldersStr += item + '\n\n'
                elif key == "sites":
                    sitesStr += item + '\n\n'
                    # print('.................................')
        # needs to return a dictionary:
        return {'combo_list': titleStr, 'apps_textbox': appsStr, 'folders_textbox': foldersStr, 'sites_textbox': sitesStr}

def render(window, title): # Needs access to window obj
    dict = getDataForRender(title)
    # KEYS_TO_ELEMENT_KEYS = {'combo_list': '-COMBO LIST-', 'apps_textbox': '-APPS TEXTBOX-', 'folders_textbox': '-FOLDERS TEXTBOX-', 'sites_textbox': '-SITES TEXTBOX-'}
    try:
        for key in KEYS_TO_ELEMENT_KEYS:
            window[KEYS_TO_ELEMENT_KEYS[key]].update(dict[key])
            window['-COMBO LIST-'].update(values=getComboList())
    except:
        print('key error!')

def loadWorkflow(window, values):
    print('loadWorkflow got title: ', values['-COMBO LIST-'])
    title = values['-COMBO LIST-']
    render(window, title)

def main():
    # this window object right now should have no user value
    window = createMainWindow()
    render(window, "python")
    while True:
        # reads user input in GUI
        event, values = window.read()
        # values dict: {'-COMBO LIST-': 'python', '-APPS TEXTBOX-': 'apple\n\nnuts\n\norange\n\n\n', '-FOLDERS TEXTBOX-': 'C:\\Users\\asus270\\AppData\\Local\\Programs\\Python\\Python36-32\n\nD:\\Archive\\acr\n\n\n', '-SITES TEXTBOX-': 'www.reddit.com/r/all\n\nwww.google.com\n\n\n'}
        ########## EVENTS #########
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
            window.close()
        if event == 'Save':
            # print('saving!!')
            getInput(window, values)
        elif event == 'Load':
            print('load')
            loadWorkflow(window, values)
        elif event == 'Open All':
            openX(values)
            print('test')
        elif event == 'DELETE':
            print('values', values["-COMBO LIST-"])
            delete(window, values)
main()
