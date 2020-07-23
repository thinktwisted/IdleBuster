#!python3
# IdleBuster.py - a simple program to keep your computer wake

import win32api, time
import pyautogui as gui

def getIdleTime():
    '''A function to return the idle time of the PC in seconds'''
    return (win32api.GetTickCount() - win32api.GetLastInputInfo())/1000

validInput = False
run = True

while not validInput:
    idleTime = input('What is your idle time [1-60 minutes]? ')
    try:
        int(idleTime)
        break;
    except ValueError:
        continue
    except TypeError:
        exit()

idleTime = int(idleTime)*60
wiggleCount = 0
print('Idle time [sec]: ' + str(idleTime))

while run:
    currentTime = getIdleTime()
    if (currentTime) > idleTime-1.5:
        for i in range(2):
            gui.press('shift')
            time.sleep(1)
        wiggleCount += 1
        print('%s - Shift pressed idle time was %s' % (str(wiggleCount), str(currentTime)))
        try:
            for i in range(idleTime-2):
                time.sleep(1)
        except KeyboardInterrupt:
            print('Exiting, total idles avoided: %s' % str(wiggleCount))
            run = False
    else:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('Exiting, total idles avoided: %s' % str(wiggleCount))
            run = False
