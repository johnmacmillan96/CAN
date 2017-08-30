import pyinotify
import subprocess
from processCanLog import *
from canmsgs import *

wm = pyinotify.WatchManager()
moveMask = pyinotify.IN_MOVED_TO

class EventHandler(pyinotify.ProcessEvent):
        
    # This method processes the candump log file
    def process_IN_MOVED_TO(self, event):
        print('Translating: ' + event.pathname + '\n')
        try:
            translateCAN(event.pathname)
            print('Finished translating ' + event.pathname + '\n')
        except NoTranslationData as error:
            print(error.args)
            
            
# creates a new handler object
handler = EventHandler()

# creates the notifier
notifier = pyinotify.Notifier(wm, handler)

# adds the directory to watch
# replace this directory with the directory that the can logs are saved to
wm.add_watch('/home/pi/Documents/CAN/log/', moveMask)

notifier.loop()
