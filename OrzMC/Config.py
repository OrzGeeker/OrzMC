# -*- coding: utf8 -*-

import os
from .utils import makedirs, platformType
from .Forge import Forge

class Config:

    GAME_TYPE_PURE = 'pure'
    GAME_TYPE_SPIGOT = 'spigot'
    GAME_TYPE_FORGE = 'forge'
    
    BASE_PATH = os.path.expanduser('~')
    GAME_ROOT_DIR = os.path.join(BASE_PATH,'.minecraft')
    GAME_LIB_DIR = os.path.join(GAME_ROOT_DIR,'libraries')
    GAME_VERSION_DIR = os.path.join(GAME_ROOT_DIR,'versions')
    GAME_ASSET_DIR = os.path.join(GAME_ROOT_DIR,'assets')
    GAME_DEPLOY_DIR = os.path.join(GAME_ROOT_DIR, 'deploy')
    GAME_SPIGOT_DEPLOY_DIR = os.path.join(GAME_ROOT_DIR, 'spigot')
    GAME_FORGE_DEPLOY_DIR = os.path.join(GAME_ROOT_DIR, 'forge-server')
    GAME_FORGE_CLIENT_DIR = os.path.join(GAME_ROOT_DIR, 'forge-client')


    def __init__(self, is_client=True, version=None, username=None, game_type=GAME_TYPE_PURE, mem_min=None, mem_max=None):
        self.is_client = is_client
        self.version = version
        self.username = username
        self.game_type = game_type
        self.mem_min = mem_min
        self.mem_max = mem_max
        self.isSpigot = (self.game_type == Config.GAME_TYPE_SPIGOT)
        self.isForge = (self.game_type == Config.GAME_TYPE_FORGE)
        self.isPure = (self.game_type == Config.GAME_TYPE_PURE)

    def getForgeInfo(self):
        if self.isForge:
            self.forgeInfo = Forge(version = self.version)
        else:
            self.forgeInfo = None

    def status(self):
        print(self.is_client)
        print(self.version)
        print(self.username)
        print(self.game_type)

    def version_json_path(self):
        '''Game Config JSON File Path'''
        return os.path.join(self.versionDir(),self.version+'.json')    

    # Client
    def assets_indexes_dir(self):
        '''Client Assets Index JSON File Directory'''
        dir = os.path.join(Config.GAME_ASSET_DIR,'indexes')
        makedirs(dir)
        return dir
    
    def assets_objects_dir(self, hash):
        '''Client Assets Object Directory'''
        dir = os.path.join(Config.GAME_ASSET_DIR,'objects',hash[0:2])
        makedirs(dir)
        return dir
    
    def versionDir(self):
        '''Client Version Related Directory'''
        dir = os.path.join(Config.GAME_VERSION_DIR,self.version)
        makedirs(dir)
        return dir

    def client_jar_path(self):
        '''Client Game JAR File Path'''
        return os.path.join(Config.GAME_VERSION_DIR,self.version,'client.jar')

    def client_forge_jar_path(self):
        return os.path.join(Config.GAME_VERSION_DIR, self.version, self.forgeInfo.fullVersion + '.jar')        

    def client_library_dir(self, subpath = None):
        '''Client Dependiencies Libraries Directory'''
        dir = Config.GAME_LIB_DIR
        if None != subpath:
            subdir =  os.path.dirname(subpath)
            dir = os.path.join(dir,subdir)
        makedirs(dir)
        return dir
        
    def client_native_dir(self):
        '''Client Native Related dependencies Directory'''
        dir = os.path.join(self.GAME_VERSION_DIR, self.version, self.version + '-native')
        makedirs(dir)
        return dir

    def client_forge_path(self):
        path = Config.GAME_FORGE_CLIENT_DIR
        makedirs(path)
        return path

    # Server
    def server_jar_path(self):
        '''Server Game JAR File Path'''
        return os.path.join(Config.GAME_VERSION_DIR,self.version)

    def server_deploy_path(self):
        '''Server Deploy Path'''

        if self.isPure:
            deployPath = Config.GAME_DEPLOY_DIR
        elif self.isSpigot:
            deployPath = Config.GAME_SPIGOT_DEPLOY_DIR
        elif self.isForge:
            deployPath = Config.GAME_FORGE_DEPLOY_DIR
        else:
            deployPath = Config.GAME_DEPLOY_DIR

        makedirs(deployPath)
        return deployPath

    def eula_path(self):
        return os.path.join(self.server_deploy_path(), 'eula.txt')

    def properties_path(self):
        return os.path.join(self.server_deploy_path(), 'server.properties')
    
    def server_deploy_build_path(self):
        deployBuildPath = os.path.join(self.server_deploy_path(), 'build')
        makedirs(deployBuildPath)
        return deployBuildPath

    def server_spigot_jar_path(self, isInBuildDir=False):
        return os.path.join(self.server_deploy_build_path() if isInBuildDir else self.server_deploy_path(), 'spigot-' + self.version + '.jar')

    def server_craftbukkit_jar_path(self, isInBuildDir=False):
        return os.path.join(self.server_deploy_build_path() if isInBuildDir else self.server_deploy_path(), 'craftbukkit-' + self.version + '.jar')

    def server_forge_jar_path(self):
        return os.path.join(self.server_deploy_path(), self.forgeInfo.fullVersion + '.jar')