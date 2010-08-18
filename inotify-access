#!/usr/bin/env python

import sys
import os
import time
from optparse import OptionParser
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent

# needs: apt-get install python-pyinotify

class EventHandler(ProcessEvent):
    def __init__(self, file_dict):
        self.file_dict = file_dict
    def process_IN_ACCESS(self, event):
        file = os.path.join(event.path, event.name)
        if not self.file_dict.has_key(file):
            self.file_dict[file] = 1
        else:
            self.file_dict[file] += 1 

def main():

    parser = OptionParser(usage="usage: %prog [options] <dir-name>")
    parser.add_option("-r", "--recurse",
                  action="store_true", dest="recurse", default=False,
                  help="recurse: watch all files in the directory tree")
    parser.add_option('-t', '--timeout', dest='timeout', default=0, type='int',
                        help='Timeout in seconds before reporting stats (default: wait for control-c)') 
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        return -1

    watched_dir = args[0]

    print "Gathering file access stats for files in %s" % watched_dir
    print "hit control-c to exit"

    files = {}

    wm = WatchManager()
    mask = EventsCodes.IN_ACCESS
    handler = EventHandler(files)
    notifier = ThreadedNotifier(wm, handler)
    notifier.start()
    wdd = wm.add_watch(watched_dir, mask, rec=options.recurse)

    
    try:
        while True:
            if options.timeout == 0:
                time.sleep(60)
            else:
                time.sleep(options.timeout)
                break
    except KeyboardInterrupt:
        print "caught control-c\n"

    print "number of accesses (reads) per file:"
    for k,v in files.items():
        print "%s: %s" % (k,v)

    return 0

    
if __name__ == '__main__':
    sys.exit(main())

