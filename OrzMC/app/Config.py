# -*- coding: utf8 -*-

import os, json
from ..utils.utils import *
from ..core.Forge import Forge

class Config:
    '''Public Definitions'''
    GAME_DEFAULT_USERNAME = "guest"
    GAME_TYPE_PURE = 'vanilla'
    GAME_TYPE_SPIGOT = 'spigot'
    GAME_TYPE_FORGE = 'forge'
    GAME_TYPE_PAPER = 'paper'
    
    '''Private Definitions'''
    BASE_PATH = os.path.expanduser('~')
    GAME_ROOT_DIR = os.path.join(BASE_PATH,'minecraft')
    GAME_VERSIONS_DIR = os.path.join(GAME_ROOT_DIR,'versions')


    def __init__(self,args):

        # 调试信息
        if args.debug:
            print(args)

        self.is_client = not args.server
        self.version = args.version
        self.username = args.username
        self.mem_min = args.minmem
        self.mem_max = args.maxmem
        self.is_extract_music = args.extract_music
        self.symlink = args.symlink
        self.bmclapi = args.bmclapi
        self.nginx = args.nginx
        self.deamon = args.deamon
        self.skin_system = args.skin_system

        game_type = args.type
        self.isPure = (game_type == Config.GAME_TYPE_PURE)
        self.isSpigot = (game_type == Config.GAME_TYPE_SPIGOT)
        self.isForge = (game_type == Config.GAME_TYPE_FORGE)
        self.isPaper = (game_type == Config.GAME_TYPE_PAPER)
        if self.isPure:
            self.game_type = Config.GAME_TYPE_PURE
        elif self.isSpigot:
            self.game_type = Config.GAME_TYPE_SPIGOT
        elif self.isPaper:
            self.game_type = Config.GAME_TYPE_PAPER
        elif self.isForge: 
            self.game_type = Config.GAME_TYPE_FORGE
        else:
            self.game_type = ''

        self.debug = args.debug
        self.force_upgrade = args.force_upgrade_world
        self.backup = args.backup_world
        self.optifine = args.optifine
        self.api = args.api
        self.force_download = args.force_download

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

    def game_version_client_library_dir(self, subpath = None):
        lib_dir = os.path.join(self.game_version_client_dir(), 'libraries')
        if None != subpath:
            subdir =  os.path.dirname(subpath)
            lib_dir = os.path.join(lib_dir,subdir)
        makedirs(lib_dir)
        return lib_dir
    
    def game_version_client_versions_dir(self):
        dir = os.path.join(self.game_version_client_dir(),'versions')
        makedirs(dir)
        return dir

    def game_version_client_versions_version_dir(self):
        dir = os.path.join(self.game_version_client_versions_dir(), self.version)
        makedirs(dir)
        return dir

    def game_version_client_native_library_dir(self):
        native_lib_dir = os.path.join(self.game_version_client_versions_version_dir(), self.version + '-natives')
        makedirs(native_lib_dir)
        return native_lib_dir

    def game_version_json_file_path(self):
        return os.path.join(self.game_version_client_versions_version_dir(), self.version + '.json')

    def game_version_client_jar_filename(self):
        return self.version + '.jar'

    def game_version_client_jar_file_path(self):
        jar_file_path = os.path.join(self.game_version_client_versions_version_dir(), self.game_version_client_jar_filename())
        return jar_file_path

    def game_version_forge_json_file_path(self):
        forge_json_file_name = '-'.join([self.version, self.forgeInfo.briefVersion]) + '.json'
        return os.path.join(self.game_version_client_dir(), forge_json_file_name)
    
    def game_version_launcher_profiles_json_path(self):
        return os.path.join(self.game_version_client_dir(), 'launcher_profiles.json')

    def game_version_json_obj(self):
        return loadJSON(self.game_version_forge_json_file_path() if self.isForge else self.game_version_json_file_path())

    def game_version_json_assets_obj(self):
        index_json_url = self.game_version_json_obj().get('assetIndex').get('url')
        index_json_path = os.path.join(self.game_version_client_assets_indexs_dir(), os.path.basename(index_json_url))
        return loadJSON(index_json_path)

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
        elif self.isPaper:
            return 'paper-' + self.version + '.jar'
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
    
    def game_version_server_world_dirs(self):
        worldName = 'world'
        properties_file_path = self.game_version_server_properties_file_path()

        if os.path.exists(properties_file_path):
            with open(properties_file_path, 'r') as f:
                for line in f.readlines():
                    if 'level-name' in line:
                        worldName = line.strip('\n').split('=')[1]
        else:
            return None

        game_dir = self.game_version_server_dir()

        world_dirs = []
        world_dir = os.path.join(game_dir,worldName)
        if world_dir and os.path.exists(world_dir):
            world_dirs.append(world_dir)

        if self.isSpigot or self.isPaper:
            world_nether_dir = world_dir + '_nether'
            world_the_end_dir = world_dir + '_the_end'
            if world_nether_dir and os.path.exists(world_nether_dir):
                world_dirs.append(world_nether_dir)
            if world_the_end_dir and os.path.exists(world_the_end_dir):
                world_dirs.append(world_the_end_dir)

        if len(world_dirs):
            return world_dirs
        else:
            return None

    def game_version_server_icon_file_path(self):
        return os.path.join(self.game_version_server_dir(), 'server-icon.png')

    def game_version_server_plugin_dir(self):
        return os.path.join(self.game_version_server_dir(),'plugins') if self.isPaper else None

    def game_version_server_world_backup_dir(self):
        game_world_backup_dir = os.path.join(Config.game_ftp_server_base_dir(), 'game_backup')
        makedirs(game_world_backup_dir)
        return game_world_backup_dir
    
    def game_version_server_symlink_source_dir(self):
        symlink_destination_dir = Config.game_ftp_server_core_data_backup_dir()
        makedirs(symlink_destination_dir)
        return symlink_destination_dir

    def game_version_client_mp3_dir(self):
        mp3_dir = os.path.join(Config.game_ftp_server_base_dir(),'client_music', self.version)
        makedirs(mp3_dir)
        return mp3_dir
        
    def game_download_temp_dir(self):
        download_temp_dir = os.path.join(Config.GAME_ROOT_DIR, 'download_tmp_dir')
        makedirs(download_temp_dir)
        return download_temp_dir

    @classmethod
    def game_ftp_server_base_dir(cls):
        ftp_base_dir = os.path.join(Config.BASE_PATH, 'minecraft_world_backup')
        makedirs(ftp_base_dir)
        return ftp_base_dir
        
    @classmethod
    def game_ftp_server_core_data_backup_dir(cls):
        server_core_data_backup_dir = os.path.join(Config.game_ftp_server_base_dir(),'mcserver')
        makedirs(server_core_data_backup_dir)
        return server_core_data_backup_dir

    @classmethod
    def game_ftp_server_core_data_plugin_dir(cls):
        plugins_dir = os.path.join(Config.game_ftp_server_core_data_backup_dir(), 'plugins')
        makedirs(plugins_dir)
        return plugins_dir

    @classmethod
    def game_config_dir(cls):
        game_config_dir = os.path.join(Config.GAME_ROOT_DIR, 'configurations')
        makedirs(game_config_dir)
        return game_config_dir

    @classmethod
    def game_version_server_nginx_file_path(cls):
        nginx_conf_file_path = os.path.join(Config.game_config_dir(),'nginx_minecraft.conf')
        return nginx_conf_file_path

    @classmethod
    def game_version_server_systemctl_conf_file_path(cls):
        systemctl_conf_file_path = os.path.join(Config.game_config_dir(),'minecraft.service')
        return systemctl_conf_file_path