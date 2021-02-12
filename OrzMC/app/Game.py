# -*- coding: utf8 -*-

from .Config import Config
from .Console import Console
from .Client import Client
from .Server import Server

from ..utils.utils import *
from ..utils.ColorString import ColorString
from ..core.Oracle import Oracle
from .Downloader import Downloader

class Game:

    def __init__(self, config):
        self.config = config
        self.console = Console(self.config)
        self.game = Client(self.config) if self.config.is_client else Server(self.config)
        
    def start(self):

        # 检查是否安装JDK
        Oracle.install_jdk()

        # 控制台用户交互展示
        self.console.userInteraction()

        try:
            #启动游戏
            self.game.start()
            
        except Exception as e:
            print(e)
            print(ColorString.warn('Start Failed!!!'))