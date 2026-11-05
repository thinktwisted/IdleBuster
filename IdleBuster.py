#!python3
# IdleBuster.py - a simple program to keep your computer wake

import win32api, time
import ctypes

def getIdleTime():
    '''A function to return the idle time of the PC in seconds'''
    return (win32api.GetTickCount() - win32api.GetLastInputInfo())/1000

VK_SHIFT = 0x10
KEYEVENTF_KEYUP = 0x0002

def pressShift():
    '''A function to inject one Shift key press (down and up) via the Win32 API'''
    ctypes.windll.user32.keybd_event(VK_SHIFT, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, 0)

validInput = False
run = True

while not validInput:
    try:
        idleMinutes = int(input('What is your idle time [1-60 minutes]? '))
    except ValueError:
        continue
    if 1 <= idleMinutes <= 60:
        validInput = True
    else:
        print('%s is out of range, enter 1-60' % str(idleMinutes))

idleTime = idleMinutes*60
wiggleCount = 0
print('Idle time [sec]: ' + str(idleTime))

while run:
    currentTime = getIdleTime()
    if (currentTime) > idleTime-1.5:
        for i in range(2):
            pressShift()
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
