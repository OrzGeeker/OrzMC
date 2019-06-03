# -*- coding: utf8 -*-
class CleanUp:
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
        





