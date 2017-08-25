import pyinotify
import subprocess
from processCanLog import *
from canmsgs import *

wm = pyinotify.WatchManager()
closeMask = pyinotify.IN_CLOSE_WRITE

log = open('log.txt', 'w')

class EventHandler(pyinotify.ProcessEvent):

    # This method moves the candump files to a seperate dir to be processed,
    # then opens a new candump
    def process_IN_CLOSE_WRITE(self, event):

        print('Closing: ' + event.pathname + '\n')
        log.write('Closing: ' + event.pathname + '\n')

        print('Moving ' + event.name + '\n')
        log.write('Moving ' + event.name + '\n')

        subprocess.call(['mv', event.name, '/home/pi/Documents/CAN/log'])

        # starts a new candump
        subprocess.call(['candump', '-l', '-n', '100', 'can0,1DB:7ff,284:7ff,5A9:7ff,5BC:7ff,55B:7ff'])
        

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wm.add_watch('/home/pi/Documents/CAN/', closeMask)

notifier.loop()
