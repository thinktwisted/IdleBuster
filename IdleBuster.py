import win32api, time
import pyautogui as gui

def getIdleTime():
    '''A function to return the idle time of the PC in seconds'''
    return (win32api.GetTickCount() - win32api.GetLastInputInfo())/1000

run = True
validInput = False

while not validInput:
    idleTime = (gui.prompt('What is your idle time [1-60 minutes]?'))
    try:
        int(idleTime)
        break;
    except ValueError:
        continue
    except TypeError:
        exit()

idleTime = int(idleTime)*60
wiggleCount = 0
print('Target time [sec]: ' + str(idleTime))

while run:
    currentTime = getIdleTime()
    #print("Idle time [sec]: " + str(currentTime))
    if (currentTime) > idleTime:
        #currentPosition = gui.position()
        #gui.moveTo(currentPosition[0]+50, currentPosition[1]+50, duration=0.5)
        for i in range(2):
            gui.press('shift')
        #gui.moveTo(currentPosition[0], currentPosition[1], duration=1)
        print('Shift pressed idle time was %s' % str(currentTime))
        wiggleCount += 1
        try:
            for i in range(idleTime-5):
                time.sleep(1)
        except KeyboardInterrupt:
            print('Exiting, total wiggles: %s' % str(wiggleCount))
            run = False
    else:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('Exiting, total presses: %s' % str(wiggleCount))
            run = False
