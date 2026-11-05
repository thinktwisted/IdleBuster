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

def askIdleMinutes():
    '''A function to prompt for the idle timeout until 1-60 minutes is given'''
    while True:
        try:
            idleMinutes = int(input('What is your idle time [1-60 minutes]? '))
        except ValueError:
            continue
        except (KeyboardInterrupt, EOFError):
            print('Exiting, no idle time given')
            return None
        if 1 <= idleMinutes <= 60:
            return idleMinutes
        print('%s is out of range, enter 1-60' % str(idleMinutes))

def main():
    idleMinutes = askIdleMinutes()
    if idleMinutes is None:
        return
    idleTime = idleMinutes*60
    wiggleCount = 0
    print('Idle time [sec]: ' + str(idleTime))
    try:
        while True:
            currentTime = getIdleTime()
            if currentTime > idleTime-1.5:
                for _ in range(2):
                    pressShift()
                    time.sleep(1)
                wiggleCount += 1
                print('%s - Shift pressed idle time was %s' % (str(wiggleCount), str(currentTime)))
            time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting, total idles avoided: %s' % str(wiggleCount))

if __name__ == '__main__':
    main()
