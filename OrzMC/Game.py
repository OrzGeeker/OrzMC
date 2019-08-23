# -*- coding: utf8 -*-

from .Mojang import Mojang
from .Config import Config
from .Spigot import Spigot
from .Forge import Forge
from .OptiFine import OptiFine
from .CleanUp import CleanUp
from .PaperAPI import PaperAPI
from .utils import matchAndReplace, checkFileExist, isPy3, platformType, ColorString, writeContentToFile, zip
import json
import requests
import os
import sys
import signal
import uuid
import re
import hashlib
import time
import progressbar
import io
import shutil
import datetime

is_sigint_up = False
def sigint_handler(signum, frame):
    global is_sigint_up
    is_sigint_up = True
    print(ColorString.warn("\nForce Exit!"))
    CleanUp.executeCleanTask()
    exit(-1)

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

if platformType() != 'windows':
    signal.signal(signal.SIGHUP, sigint_handler)

class Game:

    def __init__(self, config = None):
        self._game=None
        self._forgeGame = None
        self._assets=None
        self._javaClassPathList = None
        self.config = config

    # 启动客户端
    def startClient(self):

        if not self.config.is_client:
            return 

        if self.config.isPure :
            self.downloadGameJSON()
            self.downloadClient()
            self.downloadAssetIndex()
            self.downloadAssetObjects()
            self.donwloadLibraries()
            self.writeLauncherProfilesJSON()
        elif self.config.isForge:
            self.config.getForgeInfo()
            if not os.path.exists(self.config.game_version_client_jar_file_path()) or not os.path.exists(self.config.game_version_forge_json_file_path()):
                self.extractForgeClient()
        else:
            ColorString.warn('Not Known Client!!!!')
            return

        user = self.config.username
        resolution = ('960', '540')

        global is_sigint_up
        if is_sigint_up:
            return
        
        cmd = self.gameArguments(user,resolution)
        backgroundCmd =  cmd + ' &'
        if platformType() == 'windows':
            backgroundCmd = ('start ' +  cmd) if not self.config.debug else cmd
            
        os.chdir(self.config.game_version_client_dir())
        os.system(backgroundCmd)
        
        self.formatOutputClientCmd(backgroundCmd)

    def formatOutputClientCmd(self, cmd):
        if self.config.debug and len(cmd) > 0: 
            for e in cmd.split(' '):
                if 'jar' in e:
                    for c in e.split(self.config.java_class_path_list_separator()):
                        print(c)
                else:
                    print(e)

    # 部署服务端
    def deployServer(self):
        '''deploy minecraft server'''

        if self.config.is_client:
            return

        if self.config.backup:
            self.backupWorld()
            return
        
        if self.config.isPure:
            self.downloadGameJSON()
            self.downloadServer()
            (serverJARFilePath, _, _) = self.serverJARFilePath()
            jarFilePath = serverJARFilePath
        elif self.config.isSpigot:
            if not os.path.exists(self.config.game_version_server_jar_file_path()):
                self.buildSpigotServer()
            jarFilePath = self.config.game_version_server_jar_file_path()
        elif self.config.isPaper:
            if not os.path.exists(self.config.game_version_server_jar_file_path()):
                self.downloadPaperServerJarFile()
            jarFilePath = self.config.game_version_server_jar_file_path()
        elif self.config.isForge:
            self.config.getForgeInfo()
            if not os.path.exists(self.config.game_version_server_jar_file_path()):
                self.buildForgeServer()
            jarFilePath = self.config.game_version_server_jar_file_path()
            if not os.path.exists(jarFilePath):
                jarFilePath = jarFilePath.replace(self.config.forgeInfo.fullVersion, self.config.forgeInfo.fullVersion + '-universal')
        else:
            print(ColorString.warn('Your choosed server is not exist!!!\nCurrently, there are three type server: pure/spigot/forge'))
            return

        mem_start = self.config.mem_min
        mem_max = self.config.mem_max

        jvm_opts = ' '.join([
            '-server',
            '-Xms' + mem_start,
            '-Xmx' + mem_max
        ])
        jarArgs = ['--forceUpgrade', 'nogui'] if (self.config.isSpigot or self.config.isPaper) and self.config.force_upgrade else ['nogui']
        self.startServer(self.startCommand(jvm_opts= jvm_opts, serverJARFilePath = jarFilePath, jarArgs = jarArgs))

    def download(self, url, dir, name = None):
        global is_sigint_up
        if is_sigint_up:
            return
        if name == None:
            filename = os.path.basename(url)
        else:
            filename = name
        with open(os.path.join(dir,filename),'wb') as f:
            f.write(requests.get(url).content)

    def loadJSON(self, filePath):
        with open(filePath) as json_data:
            jsonObj = json.load(json_data)
            return jsonObj

    def downloadGameJSON(self):
        global is_sigint_up
        if is_sigint_up:
            return

        '''Download Game Json Configure File'''
        version_json_path = self.config.game_version_json_file_path()
        (url, hash) = Mojang.get_release_game_json(self.config.version)
        if not checkFileExist(version_json_path, hash):
            print("Download Game Json Configure File!")
            jsonStr = requests.get(url).text
            writeContentToFile(jsonStr, version_json_path)
        else: 
            print("Game Json Configure File have been downloaded!")

    def game(self):
        if self._game == None:
            self._game = self.loadJSON(self.config.game_version_json_file_path())
        return self._game

    def forgeGame(self):
        if self._forgeGame == None:
            self._forgeGame = self.loadJSON(self.config.game_version_forge_json_file_path())
        return self._forgeGame
    
    def assets(self):
        if self._assets == None:
            index_json_url = self.game().get('assetIndex').get('url')
            index_json_path = os.path.join(self.config.game_version_client_assets_indexs_dir(), os.path.basename(index_json_url))
            self._assets = self.loadJSON(index_json_path)
        return self._assets

    def javaClassPathList(self):
        if None == self._javaClassPathList:
            self._javaClassPathList = []
            libs = self.game().get('libraries')
            total = len(libs)
            
            errorMsg = []
            with progressbar.ProgressBar(max_value=total, prefix='javaClassPathList: ') as bar:
                index = 0
                for lib in libs: 
                    libName = lib.get('name')
                    downloads = lib.get('downloads')

                    rules = lib.get('rules')
                    if None != rules:
                        for rule in rules:
                            if None != rule:
                                if rule.get('action') == 'disallow':
                                    if rule.get('os').get('name') == platformType():
                                        # errorMsg.append(libName + 'is disallowed')
                                        continue

                    libPath = None
                    url = None
                    sha1 = None
                    nativeKey = 'natives-'+ platformType()
                    if 'natives' in lib:
                        platform = lib.get('natives').get(platformType())
                        if platform == None:
                            # errorMsg.append('Error: no platform jar - ' +  libName)
                            continue
                        else:
                            libPath = downloads.get('classifiers').get(platform).get('path')
                            url = downloads.get('classifiers').get(platform).get('url')
                            sha1 = downloads.get('classifiers').get(platform).get('sha1')
                            nativeFilePath = os.path.join(self.config.game_version_client_native_library_dir(),os.path.basename(url))
                            if not checkFileExist(nativeFilePath,sha1):
                                errorMsg.append("Not Exist: %s" % nativeFilePath)
                                continue
                            else:
                                self._javaClassPathList.append(nativeFilePath)
                    else:
                        classifiers = downloads.get('classifiers')
                        if classifiers and nativeKey in downloads.get('classifiers'):
                            url = downloads.get('classifiers').get(nativeKey).get('url')
                            sha1 = downloads.get('classifiers').get(platform).get('sha1')
                            nativeFilePath = os.path.join(self.config.game_version_client_native_library_dir(),os.path.basename(url))
                            if not checkFileExist(nativeFilePath,sha1):
                                errorMsg.append("Not Exist: %s" % nativeFilePath)
                                continue
                            else:
                                self._javaClassPathList.append(nativeFilePath)
                                
                        libPath = downloads.get('artifact').get('path')
                        url = downloads.get('artifact').get('url')
                        sha1 = downloads.get('artifact').get('sha1')
                        if platformType() == 'windows' :
                            libPath = libPath.replace('/','\\')
                        libFilePath = os.path.join(self.config.game_version_client_library_dir(), libPath)
                        if not checkFileExist(libFilePath,sha1):
                            errorMsg.append("Not Exist: %s" % libFilePath)
                            continue            
                        else:
                            self._javaClassPathList.append(libFilePath)

                    index = index + 1
                    bar.update(index)
                    
            if(len(errorMsg) > 0):
                print('\n'.join(errorMsg))

            if self.config.isForge:
                forge_class_path = map(lambda lib:  os.path.join(self.config.game_version_client_library_dir(),lib.get('downloads').get('artifact').get('path')) ,self.forgeGame().get('libraries')) 
                self._javaClassPathList.extend(forge_class_path)

            self._javaClassPathList.append(self.config.game_version_client_jar_file_path())

        return self._javaClassPathList

# Assets

    def downloadAssetIndex(self):

        global is_sigint_up
        if is_sigint_up:
            return

        '''Download Game Asset Index JSON file'''
        assetIndex = self.game().get('assetIndex')
        index_json_url = assetIndex.get('url')
        index_json_sha1 = assetIndex.get('sha1')
        index_json_path= os.path.join(self.config.game_version_client_assets_indexs_dir(), os.path.basename(index_json_url))
        if not checkFileExist(index_json_path,index_json_sha1):
            print("Download assetIndex JSON File")
            index_json_str = requests.get(index_json_url).text
            if isPy3:
                with open(index_json_path,'w',encoding='utf-8') as f:
                    f.write(index_json_str)
            else: 
                with open(index_json_path,'w') as f:
                    f.write(index_json_str.encode('utf-8'))               
        else:
            print("assetIndex JSON File have been downloaded")

    def downloadAssetObjects(self):
        global is_sigint_up
        if is_sigint_up:
            return

        '''Download Game Asset Objects'''
        objects = self.assets().get('objects')
        total = len(objects)

        errorMsg = []
        with progressbar.ProgressBar(max_value=total, prefix='assets objects: ') as bar:
            index = 0
            for (name,object) in objects.items():
                index = index + 1
                outInfo = '%d/%d(%s)' % (index, total, name)
                hash = object.get('hash')
                url = Mojang.assets_objects_url(hash)
                object_dir = self.config.game_version_client_assets_objects_dir(hash)
                object_filePath = os.path.join(object_dir,os.path.basename(url))
                if not checkFileExist(object_filePath, hash):
                    try:
                        self.download(url,object_dir)
                    except:
                        errorMsg.append(outInfo + "FAILED!")
                bar.update(index)
        
        if(len(errorMsg) > 0):
            print('\n'.join(errorMsg))
# Library

    def donwloadLibraries(self):

        global is_sigint_up
        if is_sigint_up:
            return

        ''' download libraries'''
        libs = self.game().get('libraries')
        total = len(libs)

        errorMsg = []
        with progressbar.ProgressBar(max_value=total, prefix='libraries: ') as bar:
            index = 0
            for lib in libs: 
                libName = lib.get('name')
                downloads = lib.get('downloads')

                rules = lib.get('rules')
                if None != rules:
                    for rule in rules:
                        if None != rule:
                            if rule.get('action') == 'disallow':
                                if rule.get('os').get('name') == platformType():
                                    # errorMsg.append(libName + 'is disallowed')
                                    continue

                libPath = None
                url = None
                nativeKey = 'natives-'+ platformType()
                if 'natives' in lib:
                    platform = lib.get('natives').get(platformType())
                    if platform == None:
                        # errorMsg.append('Error: no platform jar - ' +  libName)
                        continue
                    else:
                        libPath = downloads.get('classifiers').get(platform).get('path')
                        url = downloads.get('classifiers').get(platform).get('url')
                        sha1 = downloads.get('classifiers').get(platform).get('sha1')
                        nativeFilePath = os.path.join(self.config.game_version_client_native_library_dir(),os.path.basename(url))
                        if not checkFileExist(nativeFilePath,sha1):
                            self.download(url,self.config.game_version_client_native_library_dir())
                        
                else:
                    classifiers = downloads.get('classifiers')
                    if classifiers and nativeKey in downloads.get('classifiers'):
                        url = downloads.get('classifiers').get(nativeKey).get('url')
                        sha1 = downloads.get('classifiers').get(platform).get('sha1')
                        nativeFilePath = os.path.join(self.config.game_version_client_native_library_dir(),os.path.basename(url))
                        if not checkFileExist(nativeFilePath,sha1):
                            self.download(url,self.config.game_version_client_native_library_dir())
                    
                    libPath = downloads.get('artifact').get('path')
                    url = downloads.get('artifact').get('url')
                    sha1 = downloads.get('artifact').get('sha1')
                    fileDir = self.config.game_version_client_library_dir(libPath)
                    filePath=os.path.join(fileDir,os.path.basename(url))
                    if not checkFileExist(filePath,sha1):
                        self.download(url,fileDir)

                index = index + 1
                bar.update(index)

        if(len(errorMsg) > 0):
            print('\n'.join(errorMsg))
# Client

    def downloadClient(self):
        global is_sigint_up
        if is_sigint_up:
            return  

        '''Download Client Jar File'''
        client = self.game().get('downloads').get('client')
        clientUrl = client.get('url')
        sha1 = client.get('sha1')
        clientJARFilePath = self.config.game_version_client_jar_file_path()
        if not checkFileExist(clientJARFilePath, sha1):
            print('Downloading the client jar file ...')
            self.download(clientUrl,os.path.dirname(clientJARFilePath), self.config.game_version_client_jar_filename())
            print("Client Download Completed!")
        else:
            print("Client Jar File have been downloaded")

    def gameArguments(self, user, resolution):

        argPattern = r'\$\{(.*)\}'

        mainCls =  self.forgeGame().get('mainClass') if self.config.isForge else self.game().get('mainClass')
        classPathList = self.javaClassPathList()

        if self.config.isPure and self.config.optifine:
            optifine_config = OptiFine.json_configuration(self.config)
            if optifine_config != None:
                mainCls = optifine_config.get('mainClass')
                optifine_jar_paths = OptiFine.library_optifine_jar_paths(self.config)
                classPathList = optifine_jar_paths + classPathList

        sep = self.config.java_class_path_list_separator()
        classPath = sep.join(classPathList)
        (res_width, res_height) = resolution

        configuration = {
            # for game args
            "auth_player_name" : user,
            "version_name" : self.forgeGame().get('id') if self.config.isForge else self.game().get('id'),
            "game_directory" : self.config.game_version_client_dir(),
            "assets_root" : self.config.game_version_client_assets_dir(),
            "assets_index_name" : self.game().get('assets'),
            "auth_uuid" : ''.join(str(uuid.uuid1()).split('-')),
            "auth_access_token" : ''.join(str(uuid.uuid1()).split('-')),
            "user_type" : "mojang",
            "version_type" : "release",
            "resolution_width":res_width if res_width else "",
            "resolution_height":res_height if res_height else "",
            # for jvm args
            "natives_directory": self.config.game_version_client_native_library_dir(),
            "launcher_name": "OrzMC",
            "launcher_version": '1.0',
            "classpath": classPath,

        }

        arguments = [os.popen('which java').read().strip() if platformType() != 'windows' else 'java ' if self.config.debug else  'javaw ']

        mem_min = self.config.mem_min
        mem_max = self.config.mem_max

        jvm_opts = [
            '-Xms%s' % mem_min,
            '-Xmx%s' % mem_max,
            '-Djava.net.preferIPv4Stack=true'
        ]
        arguments.extend(jvm_opts)

        game_arguments = self.game().get('arguments')
        jvmArgs = game_arguments.get('jvm') if game_arguments != None else None

        if jvmArgs != None and self.config.isForge:
            jvmArgs.append('-Dfml.ignoreInvalidMinecraftCertificates=true')
            jvmArgs.append('-Dfml.ignorePatchDiscrepancies=true')

        if jvmArgs != None:
            for arg in jvmArgs:
                if isinstance(arg, str) or not isPy3 and isinstance(arg, unicode):
                    value_placeholder = re.search(argPattern,arg)
                    if value_placeholder:
                        argValue = configuration.get(value_placeholder.group(1))
                        argStr = matchAndReplace(argPattern,argValue,arg)
                        arguments.append(argStr)
                    else:
                        arguments.append(arg)

                elif isinstance(arg, dict):
                    isValid = False
                    rules = arg.get('rules')
                    for rule in rules:
                        if rule.get('os').get('name') == platformType() and rule.get('action') == 'allow':
                            isValid = True
                            break
                    if isValid:
                        value = arg.get('value')
                        if type(value) == list:
                            for i in range(0, len(value)):
                                s = value[i].split('=')
                                if len(s) == 2:
                                    arg = s[1]
                                    if ' ' in arg:
                                        s[1] = '\"' + arg + '\"'
                                        value[i] = '='.join(s)

                            arguments.extend(value)
                        else:
                            arguments.append(value)


        arguments.append(mainCls)

        gameArgs = game_arguments.get('game') if game_arguments != None else None

        if gameArgs != None:
            for arg in gameArgs:
                if isinstance(arg, str) or not isPy3 and isinstance(arg, unicode):
                    value_placeholder = re.search(argPattern,arg)
                    if value_placeholder:
                        argValue = configuration.get(value_placeholder.group(1))
                        argStr = matchAndReplace(argPattern,argValue,arg)
                        arguments.append(argStr)
                    else:
                        arguments.append(arg)
                elif isinstance(arg, dict):
                    for rule in arg.get('rules'):
                        if rule.get('action') == 'allow':
                            if rule.get('features').get('is_demo_user'):
                                if user ==  None:
                                    arguments.append(arg.get('value'))
                            if rule.get('features').get('has_custom_resolution'):
                                value = arg.get('value')
                                for arg in value:
                                    if isinstance(arg, str):
                                        value_placeholder = re.search(argPattern,arg)
                                        if value_placeholder:
                                            argValue = configuration.get(value_placeholder.group(1))
                                            argStr = matchAndReplace(argPattern,argValue,arg)
                                            arguments.append(argStr)
                                        else:
                                            arguments.append(arg)

        if self.config.isForge:
            arguments.extend(self.forgeGame().get('arguments').get('game'))
        
        if self.config.isPure and self.config.optifine:
            optifine_config = OptiFine.json_configuration(self.config)
            if optifine_config != None:
                arguments.extend(optifine_config.get('arguments').get('game'))
        arguments = ' '.join(arguments)
        return arguments


# Server
    def serverJARFilePath(self):
            server = self.game().get('downloads').get('server')
            serverUrl = server.get('url')
            sha1 = server.get('sha1')
            serverJARFilePath = self.config.game_version_server_jar_file_path()
            return (serverJARFilePath, serverUrl, sha1)

    def downloadServer(self):
        '''Download Server Jar File'''
        (serverJARFilePath, serverUrl, sha1) = self.serverJARFilePath()
        if not checkFileExist(serverJARFilePath, sha1):
            print('Downloading the server jar file ...')
            self.download(serverUrl,self.config.game_version_server_dir(), self.config.game_version_server_jar_filename())
            print("Server Download Completed!")
        else:
            print("Server Jar File have been downloaded")


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
        
        # 启动服务
        
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

    # 构建SpigotServer
    def buildSpigotServer(self):
        '''构建SpigotServer'''

        version = self.config.version
        spigot = Spigot(version)
        print(ColorString.warn('Start download the spigot build tool jar file...'))
        self.download(spigot.build_tool_jar, self.config.game_version_server_build_dir())
        print(ColorString.confirm('Build tool jar download completed!!!'))
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
    
    def extractForgeClient(self):
        '''构建Forge客户端'''
        print(ColorString.warn('Start download the forge installer jar file...'))
        self.download(self.config.forgeInfo.forge_installer_url, self.config.game_version_client_dir())
        print(ColorString.confirm('Forge installer jar download completed!!!'))

        installerJarFilePath = os.path.basename(self.config.forgeInfo.forge_installer_url)
        extractForgeClientCmd = 'java -jar ' + installerJarFilePath

        print(ColorString.warn('Start install the forge client jar file ...'))
        os.chdir(self.config.game_version_client_dir())
        os.system(extractForgeClientCmd)
        print(ColorString.confirm('Completed! And the forge client file generated!'))

        forge_client_versions_dir = os.path.join(self.config.game_version_client_dir(), 'versions')
        pure_client_jar = os.path.join(forge_client_versions_dir, self.config.version, self.config.version + '.jar')
        dst_client_jar = os.path.join(self.config.game_version_client_dir(), os.path.basename(pure_client_jar))
        if os.path.exists(pure_client_jar) and not os.path.exists(dst_client_jar):
            shutil.move(pure_client_jar, self.config.game_version_client_dir())

        forge_version_full_name = os.path.basename(self.config.game_version_forge_json_file_path())
        (forge_version_name, _) = os.path.splitext(forge_version_full_name)
        forge_json_file = os.path.join(forge_client_versions_dir, forge_version_name, forge_version_full_name)
        print(forge_json_file)
        dst_forge_json_file = os.path.join(self.config.game_version_client_dir(), os.path.basename(forge_json_file))
        if os.path.exists(forge_json_file) and not os.path.exists(dst_forge_json_file):
            shutil.move(forge_json_file, self.config.game_version_client_dir())

        shutil.rmtree(forge_client_versions_dir)

    def writeLauncherProfilesJSON(self):
        launcher_profiles_json_file_path = self.config.game_version_launcher_profiles_json_path()
        if not os.path.exists(launcher_profiles_json_file_path):
            time = datetime.datetime.now().isoformat()
            version = self.config.version
            content = {
                'profiles': { 
                    version: {
                        'created': time,
                        'type': 'pure',
                        'name': version,
                        'lastVersionId': version,
                        'lastUsed': time
                    }
                },
                'selectedProfile': version,
                'authenticationDatabase': {}
            }

            launcher_profiles_json_file_content = json.dumps(content)

            if isPy3:
                with open(launcher_profiles_json_file_path,'w',encoding='utf-8') as f:
                    f.write(launcher_profiles_json_file_content)
            else: 
                with open(launcher_profiles_json_file_path,'w') as f:
                    f.write(launcher_profiles_json_file_content.encode('utf-8')) 

    # 构建Forge服务器
    def buildForgeServer(self):
        '''构建Forge服务器'''

        print(ColorString.warn('Start download the forge installer jar file...'))
        self.download(self.config.forgeInfo.forge_installer_url, self.config.game_version_server_dir())
        print(ColorString.confirm('Forge installer jar download completed!!!'))

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
            print(ColorString.confirm("Completed! backuped world file: %s!!!" % world_backup_file ))
        else: 
            print(ColorString.error('There is no world directory!!!'))


    def downloadPaperServerJarFile(self):
        url = PaperAPI.downloadURL(
                api_version = 'v1',
                project_name = 'paper',
                project_version = self.config.version,
                build_id = 'latest'
            )
        if url and len(url) > 0:
            print(ColorString.hint("Downloading Paper Server Jar File!!!"))
            self.download(url, self.config.game_version_server_dir(), self.config.game_version_server_jar_filename())
            print(ColorString.confirm("Paper Server Jar File Downloaded!!"))