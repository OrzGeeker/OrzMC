# -*- coding: utf8 -*-

from .Mojang import Mojang
from .Config import Config
from .utils import checkFileExist, isPy3, platformType
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

is_sigint_up = False
def sigint_handler(signum, frame):
    global is_sigint_up
    is_sigint_up = True
    print("Force Exit!")
    exit(-1)

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGHUP, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)


class GameDownloader:


    def __init__(self, version):
        self._game=None
        self._assets=None
        self._javaClassPathList = None
        self.config = Config(version)

    def download(self, url, dir):
        global is_sigint_up
        if is_sigint_up:
            return
        
        filename = os.path.basename(url)
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
        version_json_path = self.config.version_json_path()
        (url, hash) = Mojang.get_release_game_json(self.config.version)
        if not checkFileExist(version_json_path, hash):
            print("Download Game Json Configure File!")
            jsonStr = requests.get(url).text
            if jsonStr != None:
                if isPy3:
                    with open(version_json_path,'w',encoding='utf-8') as f:
                        f.write(jsonStr)
                else:
                    with open(version_json_path,'w') as f:
                        f.write(jsonStr.encode('utf-8'))
        else: 
            print("Game Json Configure File have been downloaded!")

    def game(self):
        if self._game == None:
            self._game = self.loadJSON(self.config.version_json_path())
        return self._game
    
    def assets(self):
        if self._assets == None:
            index_json_url = self.game().get('assetIndex').get('url')
            index_json_path = os.path.join(self.config.assets_indexes_dir(), os.path.basename(index_json_url))
            self._assets = self.loadJSON(index_json_path)
        return self._assets

    def javaClassPathList(self):
        if None == self._javaClassPathList:
            self._javaClassPathList = []
            libs = self.game().get('libraries')
            total = len(libs)
            
            errorMsg = []
            with progressbar.ProgressBar(max_value=total, prefix='javaClassPathList: ') as bar:
                for lib in libs: 
                    libName = lib.get('name')
                    downloads = lib.get('downloads')

                    rules = lib.get('rules')
                    if None != rules:
                        for rule in rules:
                            if None != rule:
                                if rule.get('action') == 'disallow':
                                    if rule.get('os').get('name') == platformType():
                                        errorMsg.append(libName + 'is disallowed')
                                        continue

                    libPath = None
                    url = None
                    sha1 = None
                    filePath = None
                    nativeKey = 'natives-'+ platformType()
                    if 'natives' in lib:
                        platform = lib.get('natives').get(platformType())
                        if platform == None:
                            errorMsg.append('Error: no platform jar - ' +  libName)
                            continue
                        else:
                            libPath = downloads.get('classifiers').get(platform).get('path')
                            url = downloads.get('classifiers').get(platform).get('url')
                            sha1 = downloads.get('classifiers').get(platform).get('sha1')
                            nativeFilePath = os.path.join(self.config.client_native_dir(),os.path.basename(url))
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
                            nativeFilePath = os.path.join(self.config.client_native_dir(),os.path.basename(url))
                            if not checkFileExist(nativeFilePath,sha1):
                                errorMsg.append("Not Exist: %s" % nativeFilePath)
                                continue
                            else:
                                self._javaClassPathList.append(nativeFilePath)
                                
                        libPath = downloads.get('artifact').get('path')
                        url = downloads.get('artifact').get('url')
                        sha1 = downloads.get('artifact').get('sha1')
                        libFilePath = os.path.join(self.config.client_library_dir(), libPath)
                        if not checkFileExist(libFilePath,sha1):
                            errorMsg.append("Not Exist: %s" % libFilePath)
                            continue            
                        else:
                            self._javaClassPathList.append(libFilePath)
            if(len(errorMsg) > 0):
                print('\n'.join(errorMsg))
            self._javaClassPathList.append(self.config.client_jar_path())
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
        index_json_path= os.path.join(self.config.assets_indexes_dir(), os.path.basename(index_json_url))
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
                object_dir = self.config.assets_objects_dir(hash)
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
                                    errorMsg.append(libName + 'is disallowed')
                                    continue

                libPath = None
                url = None
                nativeKey = 'natives-'+ platformType()
                if 'natives' in lib:
                    platform = lib.get('natives').get(platformType())
                    if platform == None:
                        errorMsg.append('Error: no platform jar - ' +  libName)
                        continue
                    else:
                        libPath = downloads.get('classifiers').get(platform).get('path')
                        url = downloads.get('classifiers').get(platform).get('url')
                        sha1 = downloads.get('classifiers').get(platform).get('sha1')
                        nativeFilePath = os.path.join(self.config.client_native_dir(),os.path.basename(url))
                        if not checkFileExist(nativeFilePath,sha1):
                            self.download(url,self.config.client_native_dir())
                        
                else:
                    classifiers = downloads.get('classifiers')
                    if classifiers and nativeKey in downloads.get('classifiers'):
                        url = downloads.get('classifiers').get(nativeKey).get('url')
                        sha1 = downloads.get('classifiers').get(platform).get('sha1')
                        nativeFilePath = os.path.join(self.config.client_native_dir(),os.path.basename(url))
                        if not checkFileExist(nativeFilePath,sha1):
                            self.download(url,self.config.client_native_dir())
                    
                    libPath = downloads.get('artifact').get('path')
                    url = downloads.get('artifact').get('url')
                    sha1 = downloads.get('artifact').get('sha1')
                    fileDir = self.config.client_library_dir(libPath)
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
        clientJARFilePath = os.path.join(self.config.versionDir(), os.path.basename(clientUrl))
        if not checkFileExist(clientJARFilePath, sha1):
            print('Downloading the client jar file ...')
            self.download(clientUrl,self.config.versionDir())
            print("Client Download Completed!")
        else:
            print("Client Jar File have been downloaded")

    def gameArguments(self, user, resolution):

        mainCls = self.game().get('mainClass')
        loggin = self.game().get('logging')
        classPathList = self.javaClassPathList()
        sep = ';' if platformType() == 'windows' else ':'
        classPath = sep.join(classPathList)
        (res_width, res_height) = resolution

        configuration = {
            # for game args
            "auth_player_name" : user,
            "version_name" : self.game().get('id'),
            "game_directory" : self.config.GAME_ROOT_DIR,
            "assets_root" : self.config.GAME_ASSET_DIR,
            "assets_index_name" : self.game().get('assets'),
            "auth_uuid" : ''.join(str(uuid.uuid1()).split('-')),
            "auth_access_token" : ''.join(str(uuid.uuid1()).split('-')),
            "user_type" : "Legacy",
            "version_type" : "OrzMC",
            "resolution_width":res_width if res_width else "",
            "resolution_height":res_height if res_height else "",
            # for jvm args
            "natives_directory": self.config.client_native_dir(),
            "launcher_name": "OrzMC",
            "launcher_version": '1.0',
            "classpath": classPath,

        }

        arguments = [os.popen('which java').read().strip() if platformType() != 'windows' else 'javaw ']

        jvmArgs = self.game().get('arguments').get('jvm')
        argPattern = u'\$\{(.*)\}'
        for arg in jvmArgs:
            if isinstance(arg, str) or not isPy3 and isinstance(arg, unicode):
                value_placeholder = re.search(argPattern,arg)
                if value_placeholder:
                    argValue = configuration.get(value_placeholder.group(1))
                    argStr = re.sub(argPattern,argValue,arg)
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
                    arguments.extend(arg.get('value'))

        arguments.append(mainCls)

        gameArgs = self.game().get('arguments').get('game')
        for arg in gameArgs:
            if isinstance(arg, str) or not isPy3 and isinstance(arg, unicode):
                value_placeholder = re.search(argPattern,arg)
                if value_placeholder:
                    argValue = configuration.get(value_placeholder.group(1))
                    argStr = re.sub(argPattern,argValue,arg)
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
                                        argStr = re.sub(argPattern,argValue,arg)
                                        arguments.append(argStr)
                                    else:
                                        arguments.append(arg)  


        arguments = ' '.join(arguments)
        return arguments

    def startCient(self, user, resolution = (None,None)):
        global is_sigint_up
        if is_sigint_up:
            return

        cmd = self.gameArguments(user,resolution)
        backgroundCmd = 'start ' + cmd if platformType == 'windows' else cmd + ' &'
        os.system(backgroundCmd)

# Server
    def serverJARFilePath(self):
            server = self.game().get('downloads').get('server')
            serverUrl = server.get('url')
            sha1 = server.get('sha1')
            serverJARFilePath = os.path.join(self.config.versionDir(), os.path.basename(serverUrl))
            return (serverJARFilePath, serverUrl, sha1)

    def downloadServer(self):
        '''Download Server Jar File'''
        (serverJARFilePath, serverUrl, sha1) = self.serverJARFilePath()
        if not checkFileExist(serverJARFilePath, sha1):
            print('Downloading the server jar file ...')
            self.download(serverUrl,self.config.server_jar_path())
            print("Server Download Completed!")
        else:
            print("Server Jar File have been downloaded")

    def deployServer(self):
        '''deploy minecraft server'''
        self.startServer(self.startCommand())

    def startCommand(self, mem='1024M'):
        '''construct server start command'''
        (serverJARFilePath, _, _) = self.serverJARFilePath()
        jvm_opts = ''
        cmd = 'java' + jvm_opts + ' -Xmx' + mem + ' -Xms' + mem + ' -jar ' + serverJARFilePath + ' nogui'
        return cmd

    def checkEULA(self):
        return os.path.exists(self.config.eula_path())

    def startServer(self, cmd):
        '''启动minecraft服务器'''
        os.chdir(self.config.server_deploy_path())
        
        # 如果没有eula.txt文件，则启动服务器生成
        if not self.checkEULA():
            os.system(cmd)

        # 同意eula
        with io.open(self.config.eula_path(), 'r', encoding = 'utf-8') as f:
            eula = f.read()
            checkEULA = eula.replace('false', 'true')
        with io.open(self.config.eula_path(), 'w', encoding = 'utf-8') as f:
            f.write(checkEULA)
        
        # 启动服务
        os.system(cmd)

