import pyinotify
import subprocess
from translationID import *
from canmsgs import *

wm = pyinotify.WatchManager()
closeMask = pyinotify.IN_CLOSE_WRITE
#moveMask = pyinotify.IN_MOVED_TO

log = open('log.txt', 'w')

# PRETTY BAD EDGECASE HERE, NEED TO FIX!!
# LEAVES THE LAST TWO FILES UNPROCESSED

class EventHandler(pyinotify.ProcessEvent):

    # This method moves the candump files to a seperate dir to be processed
    def process_IN_CLOSE_WRITE(self, event):

        print('Closing: ' + event.pathname + '\n')
        log.write('Closing: ' + event.pathname + '\n')

        print('Moving ' + event.name + '\n')
        log.write('Moving ' + event.name + '\n')

        subprocess.call(['mv', event.name, '/home/pi/Documents/CAN/raw'])

        # starts a new candump
        # print('Opening new camdump...\n')
        # subprocess.call(['candump', '-l', '-n', '100', 'vcan0'])
        subprocess.call(['candump', '-l', '-n', '100', 'can0,284:7ff,5A9:7ff,1DB:7ff'])
        
##    # This method processes the candump files
##    def process_IN_MOVED_TO(self, event):
##        print('Translating: ' + event.pathname + '\n')
##        try:
##            translateCAN(event.pathname)
##            print('Finished translating ' + event.pathname + '\n')
##        except NoTranslationData as error:
##            print(error.args)
##            
            

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wm.add_watch('/home/pi/Documents/CAN/', closeMask)
#wm.add_watch('/home/pi/Documents/CAN/raw/', moveMask)

notifier.loop()
