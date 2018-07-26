#!/usr/bin/env python3
# lwjgl dependiencs url: http://legacy.lwjgl.org/download.php.html

from __future__ import division
import math
import sys

import json
import os
import platform
import urllib.request
import uuid




def readJSON(version, maxMem, player, ):
    jsonFile =  os.path.join(gameVersionDir(version),version + '.json')
    with open(jsonFile,'r') as f:
        jsonObj = json.loads(f.read())

        args = jsonObj.get('minecraftArguments')
        mainCls = jsonObj.get('mainClass')
        id = jsonObj.get('id')
        assets = jsonObj.get('assets')

        # download assets
        assetIndex = jsonObj.get('assetIndex')
        assetsJSON = json.loads(urllib.request.urlopen(assetIndex.get('url')).read())
        print(assetsJSON)


        # download libraries
        libs = jsonObj.get('libraries')
        classPathList = []

        for lib in libs: 
            libName = lib.get('name')
            downloads = lib.get('downloads')

            rules = lib.get('rules')
            if None != rules:
                for rule in rules:
                    if None != rule:
                        if rule.get('action') == 'disallow':
                            if rule.get('os').get('name') == platformType():
                                print(libName + 'is disallowed')
                                continue

            libPath = None
            url = None
            if 'natives' in lib:
                platform = lib.get('natives').get(platformType())
                if platform == None:
                    print('Error: no platform jar - ' +  libName)
                    continue
                else:
                    libPath = downloads.get('classifiers').get(platform).get('path')
                    url = downloads.get('classifiers').get(platform).get('url')
            else:
                libPath = downloads.get('artifact').get('path')
                url = downloads.get('artifact').get('url')

            absPath = gameLibsDir() + '/' + libPath
            classPathList.append(absPath)
            fileDir = os.path.dirname(absPath)
            if not os.path.exists(fileDir) :
                os.makedirs(fileDir)

            if not os.path.exists(absPath):
                print(os.path.basename(absPath))
                urllib.request.urlretrieve(url,absPath,Schedule)
                print('\n')

        classPathList.append(os.path.join(gameVersionDir(version), version+'.jar'))
        sep = ';' if platformType == 'windows' else ':'
        classPath = sep.join(classPathList)

        arguments = [
            '-XX:+UseG1GC',
            '-XX:-UseAdaptiveSizePolicy',
            '-XX:-OmitStackTraceInFastThrow',
            '-Xms128M',
            '-Xmx' + str(maxMem) + 'm']

        arguments.append("-Dfml.ignoreInvalidMinecraftCertificates=true")
        arguments.append("-Dfml.ignorePatchDiscrepancies=true")
        arguments.append("-Djava.library.path=" + os.path.join(gameVersionDir(version),version + "-natives"))
        arguments.append('-cp')
        arguments.append(classPath)
        arguments.append(mainCls)

        args = args.split()

        uuidStr = ''.join(str(uuid.uuid1()).split('-'))

        dict = {
            '--username': player,
            '--version':id,
            '--assetIndex': assets,
            '--gameDir':gameRootDir(),
            '--assetsDir':gameAssetsDir(),
            '--uuid':uuidStr,
            '--accessToken':uuidStr,
            '--userType':'Legacy',
            '--versionType':'pyMC'
        }
        for i in range(0,len(args),2):
            key = args[i]
            value = dict.get(key)
            if None != value:
                args[i+1] = value
            
        args = ' '.join(args)

        arguments.append(args)
        
        arguments = ' '.join(arguments)

        cmd = os.popen('which java').read().strip() + ' ' + arguments

        # print(cmd)

        os.system(cmd)

def platformType():
    system = {
        'Linux':'linux',
        'Darwin':'osx',
        'Windows': 'windows'
    }
    return system[platform.system()]

def gameRootDir():
    return os.path.join(os.getcwd(), '.minecraft')

def gameLibsDir():
    return os.path.join(gameRootDir(),'libraries')

def gameVersionDir(version):
    return os.path.join(gameRootDir(),'versions',version)

def gameAssetsDir():
    return os.path.join(gameRootDir(),'assets')

def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    total = c
    cur = a * b
    cur = cur if cur < total else total
    progressbar(cur, total)

def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % ('=' * int(math.floor(cur * 50 / total)),percent))
    sys.stdout.flush()

if __name__== '__main__':
    readJSON('1.13', 1024, 'joker')
