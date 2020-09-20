import pyautogui
import pygetwindow as gw
import time
import webbrowser
import subprocess

# import subprocess
#
# def openFolders():
#     subprocess.Popen(r'explorer "C:\Users\asus270\Desktop\Python2020"')
#     subprocess.Popen(r'explorer "C:\Users\asus270"')
#
# openFolders()

# Cross platform open folders
def openDirXPlatform():
    import webbrowser
    path = r'C:\Users\asus270\Evernote'
    webbrowser.open('file:///' + path)

openDirXPlatform()






requestedFolders = ['D:\\tcg', 'C:\\Users\\asus270', 'C:\\Dropbox\\~Programming\\projects']

print(requestedFolders)

# subprocess.Popen(r'explorer "C:\Users\asus270\Desktop\Python2020"')

def openFolders(folders):

    # currentFolders = []
    subprocess.Popen(r'explorer ' + requestedFolders[0])

    print('req. folders:', requestedFolders[0])

    for i in range(len(requestedFolders)):
        print('ted:', requestedFolders[i])

    # subprocess.Popen(r'explorer "C:\Users\asus270"')

    askToExit = input('Type x and press ENTER key to exit and CLOSE all programs and folders you opened: ')

    if askToExit == 'x':
        subprocess.call(["taskkill","/F","/IM","firefox.exe"])

        print('Exiting')
        time.sleep(.5)

openFolders(requestedFolders)









def closePrograms():
    subprocess.call([r'C:\Program Files\Mozilla Firefox\\firefox.exe'])
    time.sleep(1)

    # how to make sure all programs data saved, and not lose work? (ex word doc)
    askToExit = input('Type x and press ENTER key to exit and CLOSE all programs and folders you opened: ')

    if askToExit == 'x':
        subprocess.call(["taskkill","/F","/IM","firefox.exe"])

        print('Exiting')
        time.sleep(.5)


def maxWindow():
    window = gw.getActiveWindow()
    window.maximize()

def openSites():
    webbrowser.open('https://my.bluehost.com/web-hosting/cplogin', new=1)
    time.sleep(.3)
    maxWindow()

openSites()

loginBtn = [1707, 682]
wpBtn = [2700, 248]

def click(btnPos):
    pyautogui.click(btnPos[0], btnPos[1], duration=.3)

time.sleep(2)
click(loginBtn)
time.sleep(25)
click(wpBtn)
