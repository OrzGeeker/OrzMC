# -*- coding: utf8 -*-

import os
from .utils import makedirs, platformType
from .Forge import Forge

class Config:
    '''Public Definitions'''
    GAME_TYPE_PURE = 'pure'
    GAME_TYPE_SPIGOT = 'spigot'
    GAME_TYPE_FORGE = 'forge'
    
    '''Private Definitions'''
    BASE_PATH = os.path.expanduser('~')
    GAME_ROOT_DIR = os.path.join(BASE_PATH,'.minecraft')
    GAME_VERSIONS_DIR = os.path.join(GAME_ROOT_DIR,'versions')

    def __init__(self, is_client=True, version=None, username=None, game_type=GAME_TYPE_PURE, mem_min=None, mem_max=None, debug = False):
        self.is_client = is_client
        self.version = version
        self.username = username
        self.mem_min = mem_min
        self.mem_max = mem_max
        self.isPure = (game_type == Config.GAME_TYPE_PURE)
        self.isSpigot = (game_type == Config.GAME_TYPE_SPIGOT)
        self.isForge = (game_type == Config.GAME_TYPE_FORGE)
        self.debug = debug

        if self.isPure:
            self.game_type = Config.GAME_TYPE_PURE
        elif self.isSpigot:
            self.game_type = Config.GAME_TYPE_SPIGOT
        elif self.isForge: 
            self.game_type = Config.GAME_TYPE_FORGE
        else:
            self.game_type = ''

    def getForgeInfo(self):
        if self.isForge:
            self.forgeInfo = Forge(version = self.version)
        else:
            self.forgeInfo = None

    def java_class_path_list_separator(self):
        return ';' if platformType() == 'windows' else ':'

    @classmethod
    def game_root_dir(cls):
        '''Game Root Dir'''
        makedirs(Config.GAME_ROOT_DIR)
        return Config.GAME_ROOT_DIR

    def game_versions_dir(self):
        '''Game Versions Dir'''
        makedirs(Config.GAME_VERSIONS_DIR)
        return Config.GAME_VERSIONS_DIR

    def game_version_dir(self):
        '''Version Related Directory'''
        version_dir = os.path.join(self.game_versions_dir(),self.version)
        makedirs(version_dir)
        return version_dir

    def game_version_json_file_path(self):
        return os.path.join(self.game_version_dir(), self.version + '.json')

    ### Client
    def game_version_client_dir(self):
        client_dir = os.path.join(self.game_version_dir(), 'client', Config.GAME_TYPE_PURE)
        makedirs(client_dir)
        return client_dir

    def game_version_client_assets_dir(self):
        assets_root_dir = os.path.join(self.game_version_client_dir(), 'assets')
        makedirs(assets_root_dir)
        return assets_root_dir

    def game_version_client_assets_indexs_dir(self):
        assets_indexs_dir = os.path.join(self.game_version_client_assets_dir(), 'indexes')
        makedirs(assets_indexs_dir)
        return assets_indexs_dir

    def game_version_client_assets_objects_dir(self, hash):
        assets_objects_dir = os.path.join(self.game_version_client_assets_dir(), 'objects', hash[0:2])
        makedirs(assets_objects_dir)
        return assets_objects_dir

    def game_version_client_jar_filename(self):
            return self.version + '.jar'

    def game_version_client_jar_file_path(self):
        jar_file_path = os.path.join(self.game_version_client_dir(), self.game_version_client_jar_filename())
        return jar_file_path

    def game_version_client_library_dir(self, subpath = None):
        lib_dir = os.path.join(self.game_version_client_dir(), 'libraries')
        if None != subpath:
            subdir =  os.path.dirname(subpath)
            lib_dir = os.path.join(lib_dir,subdir)
        makedirs(lib_dir)
        return lib_dir
    
    def game_version_client_native_library_dir(self):
        native_lib_dir = os.path.join(self.game_version_client_dir(),'native')
        makedirs(native_lib_dir)
        return native_lib_dir

    def game_version_forge_json_file_path(self):
        forge_json_file_name = '-'.join([self.version, self.forgeInfo.briefVersion]) + '.json'
        return os.path.join(self.game_version_client_dir(), forge_json_file_name)

    ### Server
    def game_version_server_dir(self):
        server_dir = os.path.join(self.game_version_dir(), 'server', self.game_type)
        makedirs(server_dir)
        return server_dir

    def game_version_server_jar_filename(self):
        if self.isForge:
            return self.forgeInfo.fullVersion + '.jar'
        elif self.isSpigot:
            return 'spigot-' + self.version + '.jar'
        elif self.isPure:
            return self.version + '.jar'
        else:
            return ''

    def game_version_server_jar_file_path(self, isInBuildDir=False):
        jar_file_path = os.path.join(self.game_version_server_build_dir() if isInBuildDir else self.game_version_server_dir(), self.game_version_server_jar_filename())
        return jar_file_path

    def game_version_server_eula_file_path(self):
        return os.path.join(self.game_version_server_dir(), 'eula.txt')

    def game_version_server_properties_file_path(self):
        return os.path.join(self.game_version_server_dir(), 'server.properties')

    def game_version_server_build_dir(self):
        build_path = os.path.join(self.game_version_server_dir(), 'build')
        makedirs(build_path)
        return build_path        
    