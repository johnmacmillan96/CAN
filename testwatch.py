import time

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.001)
            continue
        yield line



logfile = open('candump-2017-08-07_220203.log')
loglines = follow(logfile)

for line in loglines:
    print line

               
