import pyinotify
import subprocess
from processCanLog import *
from canmsgs import *

wm = pyinotify.WatchManager()
closeMask = pyinotify.IN_CLOSE_WRITE

# creates a log of the data dump
log = open('log.txt', 'w')

class EventHandler(pyinotify.ProcessEvent):

    # This method moves the candump files to a seperate dir to be processed,
    # then opens a new candump
    def process_IN_CLOSE_WRITE(self, event):

        print('Closing: ' + event.pathname + '\n')
        log.write('Closing: ' + event.pathname + '\n')

        print('Moving ' + event.name + '\n')
        log.write('Moving ' + event.name + '\n')

        # replace this directory with the directory that the can logs are saved to
        subprocess.call(['mv', event.name, '/home/pi/Documents/CAN/log'])

        # starts a new candump
        # replace can0 witht he name of your device
        subprocess.call(['candump', '-l', '-n', '100', 'can0'])
        

# creates a new handler object
handler = EventHandler()

# creates the notifier
notifier = pyinotify.Notifier(wm, handler)

# adds the directory to watch
# replace this directory with the directory that the can logs are saved to
wm.add_watch('/home/pi/Documents/CAN/', closeMask)


# loops continuosly
notifier.loop()
