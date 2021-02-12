# -*- coding: utf8 -*-

class Plugins:
    _singleton = None
    @classmethod
    def singleton(cls, config):
        '''单例方法'''
        if not Plugins._singleton:
            Plugins._singleton = Plugins(config)
        return Plugins._singleton

    def __init__(self, config):
        self.config = config

    def login(self):
        '''登录相关插件'''
        pass

    def permission(self):
        '''权限分配控制插件'''
        pass

    def skinSystem(self):
        '''皮肤系统插件'''
        pass

    def transfer(self):
        '''传送插件'''
        pass
    
    def webWorld(self):
        '''地图web浏览'''
        pass

    def recovery(self):
        '''恢复插件'''
        pass