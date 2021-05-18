#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import time
import sys
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


verbose = int(os.environ.get('VERBOSE', 1))
directory = os.environ.get('DIRECTORY',  os.path.join('tmp'))

if __name__ == "__main__":
    if verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    event_handler = LoggingEventHandler()

    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
