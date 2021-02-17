# -*- coding: utf8 -*-

from os.path import isfile
from .Config import Config
from .Downloader import Downloader
from .Nginx import Nginx
from .Daemon import Daemon
from .SkinSystem import SkinSystem
from ..utils.ColorString import ColorString
from ..utils.CleanUp import CleanUp
from ..utils.utils import *

from ..core.Spigot import Spigot

import os
import io
import time
import shutil 

class Server:
    def __init__(self, config):
        self.config = config
        self.downloader = Downloader(self.config)
        
    def start(self):
        '''start minecraft server'''    
        if self.config.is_client:
            return

        is_return = False

        # 配置Nginx服务
        if self.config.nginx:
            Nginx.setup()
            is_return = True
        # 配置Minecraft长驻服务
        if self.config.deamon:
            Daemon.setup(self.config)
            is_return = True
        # 备份服务器地图文件
        if self.config.backup:
            self.backupWorld()
            is_return = True
        # 配置服务器皮肤系统
        if self.config.skin_system:
            SkinSystem.setup()
            is_return = True

        if is_return:
            return
        
        if self.config.isPure:
            self.downloader.downloadGameJSON()
            self.downloader.downloadServer()
            (serverJARFilePath, _, _) = self.serverJARFilePath()
            jarFilePath = serverJARFilePath
        elif self.config.isSpigot:
            if self.config.force_download or not os.path.exists(self.config.game_version_server_jar_file_path()):
                self.buildSpigotServer()
            jarFilePath = self.config.game_version_server_jar_file_path()
        elif self.config.isPaper:
            if self.config.force_download or not os.path.exists(self.config.game_version_server_jar_file_path()):
                self.downloader.downloadPaperServerJarFile()
            jarFilePath = self.config.game_version_server_jar_file_path()
        elif self.config.isForge:
            self.config.getForgeInfo()
            if self.config.force_download or not os.path.exists(self.config.game_version_server_jar_file_path()):
                self.buildForgeServer()
            jarFilePath = self.config.game_version_server_jar_file_path()
            if not os.path.exists(jarFilePath):
                jarFilePath = jarFilePath.replace(self.config.forgeInfo.fullVersion, self.config.forgeInfo.fullVersion + '-universal')
        else:
            print(ColorString.warn('Your choosed server is not exist!!!\nCurrently, there are three type server: pure/spigot/forge'))
            return

        jvm_opts = ' '.join([
            '-server',
            '-Xms' + self.config.mem_min,
            '-Xmx' + self.config.mem_max
        ])
        jarArgs = ['--forceUpgrade', 'nogui'] if (self.config.isSpigot or self.config.isPaper) and self.config.force_upgrade else ['nogui']
        self.startServer(self.startCommand(jvm_opts= jvm_opts, serverJARFilePath = jarFilePath, jarArgs = jarArgs))
        print(ColorString.confirm('Start Server Successfully!!!'))
    
    def serverJARFilePath(self):
        '''服务端运行需要的JAR文件所在路径'''
        server = self.config.game_version_json_obj().get('downloads').get('server')
        serverUrl = server.get('url')
        sha1 = server.get('sha1')
        serverJARFilePath = self.config.game_version_server_jar_file_path()
        return (serverJARFilePath, serverUrl, sha1)
    
    def downloadServer(self):    
        '''Download Server Jar File'''
        (serverJARFilePath, serverUrl, sha1) = self.serverJARFilePath()
        if not checkFileExist(serverJARFilePath, sha1):
            self.downloader.download(
                serverUrl,
                self.config.game_version_server_dir(), 
                self.config.game_version_server_jar_filename(), 
                prefix_desc='server jar file'
            )
        else:
            print("server jar file existed!")

    def startCommand(self, jvm_opts = '', serverJARFilePath = '', jarArgs = ['nogui']):
        '''construct server start command'''
        argList = [
            'java',
            jvm_opts,
            '-jar',
            serverJARFilePath
        ]
        argList.extend(jarArgs)
        cmd = ' '.join(argList)
        return cmd

    def checkEULA(self):
        return os.path.exists(self.config.game_version_server_eula_file_path())

    def startServer(self, cmd):
        '''启动minecraft服务器'''

        os.chdir(self.config.game_version_server_dir())

        # 如果没有eula.txt文件，则启动服务器生成
        if not self.checkEULA():
            if self.config.isForge:
                self.generateForgeServerEULA()
            else:
                os.system(cmd)

        # 同意eula
        with io.open(self.config.game_version_server_eula_file_path(), 'r', encoding = 'utf-8') as f:
            eula = f.read()
            checkEULA = eula.replace('false', 'true')
        with io.open(self.config.game_version_server_eula_file_path(), 'w', encoding = 'utf-8') as f:
            f.write(checkEULA)
        
        # 启动服务器
        
        if self.config.debug:
            print(cmd)

        os.system(cmd)

        # 设置服务器属性为离线模式
        with io.open(self.config.game_version_server_properties_file_path(), 'r', encoding = 'utf-8') as f:
            properties = f.read()
            if 'online-mode=false' in properties:
                offline_properties = None
            else:
                offline_properties = properties.replace('online-mode=true', 'online-mode=false')

        if offline_properties != None:
            with io.open(self.config.game_version_server_properties_file_path(), 'w', encoding = 'utf-8') as f:
                f.write(offline_properties)
                print(ColorString.confirm('Setting the server to offline mode, next launch this setting take effect!!!'))

        # 为服务器核心数据文件创建符号链接
        self.symlink_server_core_files_if_need()


    # 构建SpigotServer
    def buildSpigotServer(self):
        '''构建SpigotServer'''

        version = self.config.version
        spigot = Spigot(version)
        self.download(
            spigot.build_tool_jar, 
            self.config.game_version_server_build_dir(), 
            prefix_desc='spigot build tool jar file'
        )
        buildToolJarName = os.path.basename(spigot.build_tool_jar)
        buildToolJarPath = os.path.join(self.config.game_version_server_build_dir(), buildToolJarName)
        versionCmd = ' --rev ' + version if len(version) > 0 else 'lastest'
        linuxCmd = 'git config --global --unset core.autocrlf; java -jar ' + buildToolJarPath + versionCmd
        macCmd = 'export MAVEN_OPTS="-Xmx2G"; java -Xmx2G -jar ' + buildToolJarPath + versionCmd
        windowCmd = 'java -jar ' + buildToolJarPath + versionCmd
        cmd = macCmd if platformType() == 'osx' else linuxCmd if platformType() == 'linux' else windowCmd
        print(ColorString.warn('Start build the server jar file with build tool...'))
        os.chdir(self.config.game_version_server_build_dir())
        os.system(cmd)
        print(ColorString.confirm('Completed! And the spigot built server file generated!'))
        shutil.move(self.config.game_version_server_jar_file_path(isInBuildDir=True), self.config.game_version_server_jar_file_path())
        os.chdir(self.config.game_version_server_dir())
        shutil.rmtree(self.config.game_version_server_build_dir())
    
    # 构建Forge服务器
    def buildForgeServer(self):
        '''构建Forge服务器'''

        self.download(
            self.config.forgeInfo.forge_installer_url, 
            self.config.game_version_server_dir(), 
            prefix_desc='forge installer jar file'
        )

        installerJarFilePath = os.path.basename(self.config.forgeInfo.forge_installer_url)
        installServerCmd = 'java -jar ' + installerJarFilePath + ' --installServer'
        print(ColorString.warn('Start install the forge server jar file ...'))
        os.chdir(self.config.game_version_server_dir())
        os.system(installServerCmd)
        print(ColorString.confirm('Completed! And the forge server file generated!'))


    def generateForgeServerEULA(self):
        if self.config.isForge and not self.checkEULA(): 
            pure_server_jar = os.path.join(self.config.game_version_server_dir(), '.'.join(['minecraft_server',self.config.version,'jar']))
            boot_cmd = 'java -jar ' + pure_server_jar
            os.system(boot_cmd)

    def backupWorld(self):
        world_paths = self.config.game_version_server_world_dirs()
        if world_paths:            
            backup_path = self.config.game_version_server_world_backup_dir()
            now = time.localtime()
            fileName = '_'.join([time.strftime('%Y-%m-%dT%H:%M:%S', now), self.config.game_type, self.config.version]) + '.zip'
            world_backup_file = os.path.join(backup_path, fileName)

            def backupWorld_cleanUp():
                if os.path.isfile(world_backup_file) and os.path.exists(world_backup_file):
                    os.remove(world_backup_file)
                    print(ColorString.warn("Removed Invalid World Backup File: %s" % world_backup_file))

            print(ColorString.hint('Start Executing ZIP ...'))
            CleanUp.registerTask('backupWorld_cleanUp', backupWorld_cleanUp)
            zip(world_paths, world_backup_file)
            CleanUp.cancelTask('backupWorld_cleanUp')
            file_size = os.path.getsize(world_backup_file) / 1024.0 / 1024.0 / 1024.0
            print(ColorString.confirm("Completed! backuped world file(%.2fG): %s!!!" % (file_size, world_backup_file)))
        else: 
            print(ColorString.error('There is no world directory!!!'))

    def symlink_server_core_files_if_need(self):
        '''为服务器核心文件创建符号链接到共享目录，方便版本升级'''
        if self.config.symlink:
            # 软链接需要涉及的文件和目录
            destinations = [
                self.config.game_version_server_eula_file_path(),
                self.config.game_version_server_properties_file_path(),
                self.config.game_version_server_icon_file_path(),
                self.config.game_version_server_plugin_dir(),
            ]
            world_paths = self.config.game_version_server_world_dirs()
            if world_paths and len(world_paths) > 0:
                destinations.extend(self.config.game_version_server_world_dirs())

            # 遍历创建软链接
            for destination in destinations:
                # 软链接需要链接的源文件或源目录
                source = os.path.join(self.config.game_version_server_symlink_source_dir(),os.path.basename(destination))
                # 如果软链接生成的目录下有同名的文件和目录，则取个备份用的名称
                destination_backup = destination+'.before_symlink'

                if not os.path.exists(source):
                    if os.path.exists(destination):
                        shutil.move(destination, source)
                    else:
                        # 之前有备份过的同名文件和目录，则恢复同名的文件和目录
                        if os.path.exists(destination_backup):
                            shutil.move(destination_backup, destination)
                        continue

                # 如果已经创建了软链接，则跳过不再创建
                if os.path.islink(destination):
                    target = os.readlink(destination)
                    if os.path.normcase(target) == os.path.normcase(source):
                        continue
                
                # 如果软链接生成的目录下有同名文件或目录，则先进行备份
                if os.path.exists(destination):
                    shutil.move(destination, destination_backup)
                
                # 生成软链接
                os.symlink(source, destination, target_is_directory=os.path.isdir(source))
                print("%s -> %s" % (source, destination))