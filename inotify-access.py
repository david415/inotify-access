#!/usr/bin/env python

import sys
import os
import time
from optparse import OptionParser
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent


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

    parser = OptionParser(usage="usage: %prog [dir-name]")
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        return -1

    watched_dir = args[0]

    print "Gathering stats for %s" % watched_dir
    print "hit control-c to exit"

    file_hash = {}

    wm = WatchManager()
    mask = EventsCodes.IN_ACCESS
    handler = EventHandler(file_hash)
    notifier = ThreadedNotifier(wm, handler)
    notifier.start()
    wdd = wm.add_watch('/tmp', mask, rec=True)

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print "caught control-c"
        print "file_hash:"
        print file_hash
        return 0

    
if __name__ == '__main__':
    sys.exit(main())

