import pyinotify
import subprocess
from translationID import *
from canmsgs import *

wm = pyinotify.WatchManager()
moveMask = pyinotify.IN_MOVED_TO

log = open('log.txt', 'w')

class EventHandler(pyinotify.ProcessEvent):
        
    # This method processes the candump files
    def process_IN_MOVED_TO(self, event):
        print('Translating: ' + event.pathname + '\n')
        try:
            translateCAN(event.pathname)
            print('Finished translating ' + event.pathname + '\n')
        except NoTranslationData as error:
            print(error.args)
            
            
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wm.add_watch('/home/pi/Documents/CAN/raw/', moveMask)

notifier.loop()
