import pyautogui
import pygetwindow as gw
import time
import webbrowser
import subprocess
import json
import PySimpleGUI as sg

# DEFAULT_SETTINGS = {}
KEYS_TO_ELEMENT_KEYS = {'combo_list': '-COMBO LIST-', 'apps_textbox': '-APPS TEXTBOX-', 'folders_textbox': '-FOLDERS TEXTBOX-', 'sites_textbox': '-SITES TEXTBOX-'}
# print('SETTINGS_KEYS_TO_ELEMENT_KEYS dict', KEYS_TO_ELEMENT_KEYS)

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

def delete(itemToDel):
    title = itemToDel
    print('Title', title)
    with open('db.json', 'r+') as f:
        db = json.load(f)

        del db[itemToDel]

        def writeToDB():
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(db, f, indent=2)
            f.truncate()     # remove remaining part
        writeToDB()

    # calling this fxn will clear GUI data
    # needs to be called at end of delete() fxn, or else title will NOT be removed from dropdown
    # because createMainWindow will pull data from DB. in other words: remove data from DB first,
    # then call for a new window.
    window = createMainWindow()

def rmNewlines(string):
    # removes newline at middle of string, as .strip() does not do that
    return string.replace('\n',' ').strip()

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
# to be used in layout sg.Combo(), or as keys
def getComboList():
    db = loadDB()
    comboList = []
    for key in db:
        comboList.append(key)
    return comboList

def createMainWindow():
    comboList = getComboList()
    sg.theme('DarkAmber')

    layout = [
    [sg.T('Select Workflow'), sg.Combo(comboList, size=(40, 30), key='-COMBO LIST-')],
    [sg.B('Open All'), sg.B('Load'), sg.B('Save'), sg.B('DELETE')],
    [sg.B('Exit')],
    [sg.T('Apps')],
    [sg.Multiline(size=(40, 10), key='-APPS TEXTBOX-', font='Any 14')],
    [sg.T('Folders')],
    [sg.Multiline(size=(40, 10), key='-FOLDERS TEXTBOX-', font='Any 14')],
    [sg.T('Sites')],
    [sg.Multiline(size=(40, 10), key='-SITES TEXTBOX-', font='Any 14')]
    ]

    window = sg.Window('App Title', layout, finalize=True)
    return window

def getTitle():
    window = createMainWindow()
    event, values = window.read()
    title = values['-COMBO LIST-']
    print('getTitle run...', event, values)
    print('got title:', values['-COMBO LIST-'])
    return title
# getTitle()
# print('testttt')

# gets data from DB, puts into a long string, then displays to GUI
def getDataForRender():
    db = loadDB()
    # print('values.... in getDataForRender()', values, 'type:', type(values))
    # print('values tuple', values[1]['-COMBO LIST-'])
# values['-COMBO LIST-']
    titleStr = "javascript"
    print('getDataForRender titleL:', titleStr)
    appsStr = ""
    foldersStr = ""
    sitesStr = ""
    # outer loop responsible for key
    for key in db[titleStr]:
        print('key: ', key)
        # inner loop responsible for going through array w/ dynamic num. of items
        for item in db[titleStr][key]:
            # print('iteemmm', item)
            if key == "apps":
                appsStr += item + '\n\n'
            elif key == "folders":
                foldersStr += item + '\n\n'
            elif key == "sites":
                sitesStr += item + '\n\n'
                # print('appppstrrr', appsStr)
                # print('.................................')
    # needs to return a dictionary:
    return {'combo_list': titleStr, 'apps_textbox': appsStr, 'folders_textbox': foldersStr, 'sites_textbox': sitesStr}



def fname(arg):
    print('hiiii', arg )
    # print('values testing', values)

def main():
    # print('render running with title:')
    # this window object right now should have no user value
    window = createMainWindow()

    # Needs access to window obj
    def render():
        print('render window', 'adsf')
        dict = getDataForRender()
        # KEYS_TO_ELEMENT_KEYS = {'combo_list': '-COMBO LIST-', 'apps_textbox': '-APPS TEXTBOX-', 'folders_textbox': '-FOLDERS TEXTBOX-', 'sites_textbox': '-SITES TEXTBOX-'}
        for key in KEYS_TO_ELEMENT_KEYS:
            window[KEYS_TO_ELEMENT_KEYS[key]].update(dict[key])
    render()

    def loadWorkflow(values):
        print('workflow load... title:', values['-COMBO LIST-'])
        title = values['-COMBO LIST-']
        render()

    while True:
        # reads user input in GUI, values is {}
        event, values = window.read()
        # fname(values)
        # render(values)
        loadWorkflow(values)
        print('values.... in whileTrue()', values, 'type:', type(values))
        # values dict: {'-COMBO LIST-': 'python', '-APPS TEXTBOX-': 'apple\n\nnuts\n\norange\n\n\n', '-FOLDERS TEXTBOX-': 'C:\\Users\\asus270\\AppData\\Local\\Programs\\Python\\Python36-32\n\nD:\\Archive\\acr\n\n\n', '-SITES TEXTBOX-': 'www.reddit.com/r/all\n\nwww.google.com\n\n\n'}

        # don't remove yet:
        # parseUserInput(values)

        def getUserData():
            with open('db.json', 'r+') as f:
                db = json.load(f)
                dbTemplate =  {"apps": [], "folders": [], "sites": []}

                def getParam():
                    hardKey = ["title", "apps", "folders", "sites"]
                    title = getTitle()
                    # KEYS_TO_ELEMENT_KEYS = {'combo_list': '-COMBO LIST-', 'apps_textbox': '-APPS TEXTBOX-', 'folders_textbox': '-FOLDERS TEXTBOX-', 'sites_textbox': '-SITES TEXTBOX-'}
                    for ind, key in enumerate(KEYS_TO_ELEMENT_KEYS):
                        # try:
                        # print('test values', values[KEYS_TO_ELEMENT_KEYS[key]])
                        # print('test key', key)
                        if key == 'combo_list':
                            print('key is combo_list', key)
                            # dbTemplate[title] = dbTemplate.pop("temp")
                            continue
                        # print('KEYS_TO_ELEMENT_KEYS:', key)
                        #key is now apps_textbox
                        newArr = rmNewlines( values[KEYS_TO_ELEMENT_KEYS[key]] ).split("  ")
                        #is now an array: ['apple', 'nuts', 'orange']
                        print('newArrayy', newArr, 'indxxxxx. curr:', ind)
                        # for index, item in enumerate(newArr):
                        for index, item in enumerate(newArr):
                            print('current item', item)
                            dbTemplate[hardKey[ind]].append(item)
                getParam()
                print('TEMPppppppp:', dbTemplate)
                db["asdfjklkldsfg"] = dbTemplate
                db[getTitle()] = dbTemplate

                def writeToDB():
                    f.seek(0)        # <--- should reset file position to the beginning.
                    json.dump(db, f, indent=2)
                    f.truncate()     # remove remaining part
                writeToDB()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
            window.close()

        ########## EVENTS #########
        def checkEventBtn():
            # print('event clicked:', event)
            if event == 'Save':
                print('saving!!')
                getUserData()
            elif event == 'Load':
                print('load')
                # loadWorkflow()
            elif event == 'Open All':
                # openX()
                print('test')
            elif event == 'DELETE':
                print('values', values["-COMBO LIST-"])
                # the value is the currently selected item from the dropdown menu
                delete(values["-COMBO LIST-"])
                # window['-COMBO LIST-'].update('fffff')
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





        # for index in range(0, 3):
        #     for key in db["python"]:
        #         # iterates thru 3 keys: apps, then folders, then sites
        #         # print("db python:", db["python"])
        #         # print('deeper', key[index])
        #         print("current key: ", key)
        #         print('an array:', db["python"][key]) #gives an array
        #         print('item in array:', db["python"][key][index]) #gives 1 item in array
        #         # db["python"][key][index] = "teddd"
        #         # appsStr += db["python"][key][index] + '\n\n'
        #         # print('appsStr final :', appsStr)


        # for title in db:
        #     # print('TITLESDFASDF:', title)
        #     # db[title] is db["python"], eval to dict, of 3 keys: apps, folders, sites
        #     for index, key in enumerate(db[title]["apps"]):
        #         # print('testd', db[title][key][index])
        #         print('keeeey', key)
        #
        #
        #         # for key in db[title][key]:
        #         #     print('keeeey', key)
        #
        #             # print('db[title][key]', db[title][key][index])
        #         # print('index: ', index, 'key: ', key)
        #         # print('bbbbb', db[title][key][index] )
        #         # appsStr += db[title][key][index] + '\n\n'
        #         # foldersStr += db["folders"][index]["path"] + '\n\n'
        #         # sitesStr += db["sites"][index]["path"] + '\n\n'
        #         # print('appsStr FINAL:', appsStr)
        #
        #
        #         # db["python"]["apps", "sites"...][0]
        #         #     db[title[index]][key[index]]
        #         # for key in db[key][title[index]]:
        #         # title += db[]
        #         # print('str @ index :', index, foldersStr)
        # # print('db[index]', db["python"])
        # # db has 3 dict. items, access using db["python"]
        # # outer loop goes through all titles ("python", "jobs", etc..) of db
        # for index in range(0,len(db)):
        #
        #     # print('ted', db[ title[index] ] )
        #     try:
        #         #first iter. db[index] is "python", 2 is "javascript"...
        #         for key in db[index]:
        #             # db[index][key][index]
        #             print('asdfasdf', db[index][key][index])
        #
        #     except IndexError:
        #         pass
        #     continue



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

                        # print('hardKey[index]', hardKey[index], 'newArr[index]', newArr[index] )
                        # if hardKey[index] == "apps":
                        #     dbTemplate[title]["apps"].append(item)
                        #
                        # elif hardKey[index] == "folders":
                        #     dbTemplate[title]["folders"].append(item)
                        #
                        # elif hardKey[index] == "sites":
                        #     dbTemplate[title]["sites"].append(item)
                        # print('window key stuff', window[KEYS_TO_ELEMENT_KEYS[key]].split(" ") )
                    # except AttributeError:
                    #     pass
                    # continue


                    # appsArr = rmNewlines(values['-APPS TEXTBOX-']).split("  ")
                    # foldersArr = rmNewlines(values['-FOLDERS TEXTBOX-']).split("  ")
                    # # print('apps values:', values['-APPS TEXTBOX-'], 'folders values: ', values['-FOLDERS TEXTBOX-'])
                    # sitesArr = rmNewlines(values['-SITES TEXTBOX-']).split("  ")
                    # dataArr = [appsArr, foldersArr, sitesArr]

                        # for index in range(0,len(db)):
                        #
                        #     # print('ted', db[ title[index] ] )
                        #     try:
                        #         #first iter. db[index] is "python", 2 is "javascript"...
                        #         for key in db[index]:
                        #             # db[index][key][index]
                        #             print('asdfasdf', db[index][key][index])
                        #
                        #     except IndexError:
                        #         pass
                        #     continue
