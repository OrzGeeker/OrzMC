# -*- coding: utf8 -*-

class CleanUp:

    is_sigint_up = False
    cleanTasks = {}

    @classmethod
    def registerTask(cls, key, value):
        CleanUp.cleanTasks[key] = value

    @classmethod
    def cancelTask(cls, key):
        if key in CleanUp.cleanTasks.keys():
            CleanUp.cleanTasks.pop(key)
    
    @classmethod
    def executeCleanTask(cls, key = None):
        if key == None: 
            for task in CleanUp.cleanTasks.values():
                task()
        else:
            if key in CleanUp.cleanTasks.keys():
                CleanUp.cleanTasks[key]() 
        
    @classmethod
    def sigint_handler(cls, signum, frame):
        CleanUp.is_sigint_up = True
        print(ColorString.warn("\nForce Exit!"))
        CleanUp.executeCleanTask()
        exit(-1)


import signal
from .utils import platformType
from .ColorString import ColorString
signal.signal(signal.SIGINT, CleanUp.sigint_handler)
signal.signal(signal.SIGTERM, CleanUp.sigint_handler)
if platformType() != 'windows':
    signal.signal(signal.SIGHUP, CleanUp.sigint_handler)
