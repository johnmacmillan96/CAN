import pyinotify
import subprocess
from processCanLog import *
from canmsgs import *

wm = pyinotify.WatchManager()
moveMask = pyinotify.IN_MOVED_TO

log = open('log.txt', 'w')

class EventHandler(pyinotify.ProcessEvent):
        
    # This method processes the candump log file
    def process_IN_MOVED_TO(self, event):
        print('Translating: ' + event.pathname + '\n')
        try:
            translateCAN(event.pathname)
            print('Finished translating ' + event.pathname + '\n')
        except NoTranslationData as error:
            print(error.args)
            
            
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wm.add_watch('/home/pi/Documents/CAN/log/', moveMask)

notifier.loop()
