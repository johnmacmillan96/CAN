import pyinotify
import subprocess
from translation import *
from canmsgs import *

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CLOSE_WRITE

class EventHandler(pyinotify.ProcessEvent):
    # This method processes the IN_CLOSE_WRITE event
    def process_IN_CLOSE_WRITE(self, event):
        print('Closing: ' + event.pathname + '\n')
        # starts a new candump
        print('Opening new camdump...\n')
        subprocess.call(['candump', '-l', '-n', '10', 'vcan0'])
        print('Translating: ' + event.pathname + '\n')
        try:
            translateCAN(event.pathname)
        except NoTranslationData as error:
            print(error.args)
            
            

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wm.add_watch('/home/pi/Documents/CAN/', mask)

notifier.loop()
