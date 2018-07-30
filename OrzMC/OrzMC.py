from OrzMC.Mojang import Mojang
from OrzMC.Config import Config
import json
import requests
import os
import sys
import platform
import uuid
import re

class GameDownloader:


    def __init__(self, version):
        self._game=None
        self._assets=None
        self._javaClassPathList = None
        self.config = Config(version)

    def download(self, url, dir):
        filename = os.path.basename(url)
        with open(os.path.join(dir,filename),'wb') as f:
            f.write(requests.get(url).content)

    def loadJSON(self, filePath):
        with open(filePath) as json_data:
            jsonObj = json.load(json_data)
            return jsonObj

    def downloadGameJSON(self):
        '''Download Game Json Configure File'''
        jsonStr = Mojang.get_release_game_json(self.config.version)
        if jsonStr != None:
            version_json_path = self.config.version_json_path()
            with open(version_json_path,'w',encoding='utf-8') as f:
                f.write(Mojang.get_release_game_json(self.config.version))
    
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
            index = 0
            for lib in libs: 
                libName = lib.get('name')
                downloads = lib.get('downloads')

                rules = lib.get('rules')
                if None != rules:
                    for rule in rules:
                        if None != rule:
                            if rule.get('action') == 'disallow':
                                if rule.get('os').get('name') == self.platformType():
                                    print(libName + 'is disallowed')
                                    continue

                libPath = None
                url = None
                if 'natives' in lib:
                    platform = lib.get('natives').get(self.platformType())
                    if platform == None:
                        print('Error: no platform jar - ' +  libName)
                        continue
                    else:
                        libPath = downloads.get('classifiers').get(platform).get('path')
                        url = downloads.get('classifiers').get(platform).get('url')
                else:
                    libPath = downloads.get('artifact').get('path')
                    url = downloads.get('artifact').get('url')

                absLibFilePath = os.path.join(self.config.GAME_LIB_DIR,libPath)
                self._javaClassPathList.append(absLibFilePath)
       
        self._javaClassPathList.append(self.config.client_jar_path())
        return self._javaClassPathList

    def platformType(self):
        '''OS type'''
        system = {
            'Linux':'linux',
            'Darwin':'osx',
            'Windows': 'windows'
        }
        return system[platform.system()]

# Assets

    def downloadAssetIndex(self):
        '''Download Game Asset Index JSON file'''
        index_json_url = self.game().get('assetIndex').get('url')
        index_json_str = requests.get(index_json_url).text
        index_json_path= os.path.join(self.config.assets_indexes_dir(), os.path.basename(index_json_url))
        with open(index_json_path,'w',encoding='utf-8') as f:
            f.write(index_json_str)

    def downloadAssetObjects(self):
        '''Download Game Asset Objects'''
        objects = self.assets().get('objects')
        total = len(objects)
        index = 0
        for (name,object) in objects.items():
            index = index + 1
            outInfo = '%d/%d(%s)' % (index, total, name)
            
            hash = object.get('hash')
            url = Mojang.assets_objects_url(hash)
            object_dir = self.config.assets_objects_dir(hash)

            try:
                self.download(url,object_dir)
                print(outInfo)
            except:
                print(outInfo + "FAILED!")
                continue

# Library

    def donwloadLibraries(self):
        ''' download libraries'''
        libs = self.game().get('libraries')
        total = len(libs)
        index = 0
        for lib in libs: 
            libName = lib.get('name')
            downloads = lib.get('downloads')

            rules = lib.get('rules')
            if None != rules:
                for rule in rules:
                    if None != rule:
                        if rule.get('action') == 'disallow':
                            if rule.get('os').get('name') == self.platformType():
                                print(libName + 'is disallowed')
                                continue

            libPath = None
            url = None
            nativeKey = 'natives-'+ self.platformType()
            if 'natives' in lib:
                platform = lib.get('natives').get(self.platformType())
                if platform == None:
                    print('Error: no platform jar - ' +  libName)
                    continue
                else:
                    libPath = downloads.get('classifiers').get(platform).get('path')
                    url = downloads.get('classifiers').get(platform).get('url')
                    self.download(url,self.config.client_native_dir())
            else:
                classifiers = downloads.get('classifiers')
                if classifiers and nativeKey in downloads.get('classifiers'):
                    url = downloads.get('classifiers').get(nativeKey).get('url')
                    self.download(url,self.config.client_native_dir())
                else:
                    libPath = downloads.get('artifact').get('path')
                    url = downloads.get('artifact').get('url')
                    fileDir = self.config.client_library_dir(libPath)
                    self.download(url,fileDir)

            index = index + 1
            print('%s(%d/%d)' % (os.path.basename(url), index, total))
# Client

    def downloadClient(self):
        '''Download Client Jar File'''
        clientUrl = self.game().get('downloads').get('client').get('url')
        print('Downloading the client jar file ...')
        self.download(clientUrl,self.config.versionDir())
        print("Client Download Completed!")


    def gameArguments(self, maxMem, user):

        mainCls = self.game().get('mainClass')
        loggin = self.game().get('logging')
        classPathList = self.javaClassPathList()
        sep = ';' if self.platformType() == 'windows' else ':'
        classPath = sep.join(classPathList)


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
            # for jvm args
            "natives_directory": self.config.client_native_dir(),
            "launcher_name": "OrzMC",
            "launcher_version": '1.0',
            "classpath": classPath,

        }

        arguments = [os.popen('which java').read().strip()]


        jvmArgs = self.game().get('arguments').get('jvm')
        argPattern = '\$\{(.*)\}'
        for arg in jvmArgs:
            if isinstance(arg, str):
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
                    if rule.get('os').get('name') == self.platformType() and rule.get('action') == 'allow':
                        isValid = True
                        break
                if isValid:
                    arguments.extend(arg.get('value'))

        arguments.append(mainCls)

        gameArgs = self.game().get('arguments').get('game')
        for arg in gameArgs:
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

    def startCient(self, maxMem = 1024, user = "guest"):
        cmd = self.gameArguments(maxMem, user)
        os.system(cmd)

# Server
    def downloadServer(self):
        '''Download Server Jar File'''
        serverUrl = self.game().get('downloads').get('server').get('url')
        print('Downloading the server jar file ...')
        self.download(serverUrl,self.config.server_jar_path())
        print("Server Download Completed!")

def startClient():
    game = GameDownloader('1.13')
    game.downloadGameJSON()
    game.downloadClient()
    game.downloadServer()
    game.downloadAssetIndex()
    game.downloadAssetObjects()
    game.donwloadLibraries()
    game.startCient()