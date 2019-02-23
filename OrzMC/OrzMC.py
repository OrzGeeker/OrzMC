# -*- coding: utf8 -*-

from .GameDownloader import GameDownloader
import sys, getopt
from .Mojang import Mojang
from .utils import hint

version = ""
username = "guest"

def showVersionList(isShow = True):
    
    global version

    if not isShow: return

    allVersions = Mojang.get_version_list(update=True)
    releases = list(filter(lambda version: version.get('type') == 'release', allVersions))
    releaseVersions = list(map(lambda info: info.get('id', ''), releases))
    print('All Release Versions as follow: ')
    for releaseVersion in releaseVersions: 
        print(releaseVersion)
    
    if len(releaseVersions) > 0:
        version = releaseVersions[0]

    select = hint('Please select a version number of above list to play(default: %s): ' % version)
    if len(select) > 0:
        found = False
        for releaseVersion in releaseVersions: 
            if releaseVersion == select.strip():
                found = True
                version = releaseVersion
                print('You choose the version: %s' % version)
        if not found:
            print('There is no such a release version game!')
    else:
        print('You choose the default version(%s)!' % version)

def showUserName(isShow):

    if not isShow: return 

    global username

    u = hint('Please choose a username(default: %s): ' % username)
    if len(u) > 0:
        username = u
        print('You username in game is: %s' % username)


def startClient():

    isShowList = True
    isShowUserName = True

    global version
    global username

    try:
        opts, args = getopt.getopt(sys.argv[1:], "v:u:", ["version=", "username="])
        for o, a in opts:
            if o in ["-v", "--version"]:
                if len(a) > 0:
                    version = a
                    isShowList = False
            if o in ["-u", "--username"]:
                if len(a) > 0:
                    username = a
                    isShowUserName = False

        showVersionList(isShowList)
        showUserName(isShowUserName)
        game = GameDownloader(version)
        game.downloadGameJSON()
        game.downloadClient()
        game.downloadAssetIndex()
        game.downloadAssetObjects()
        game.donwloadLibraries()
        game.startCient(user=username)

    except getopt.GetoptError:
        print("The arguments is invalid!")

def downloadServer():
    
    global version

    mem_start = ""
    mem_max = ""
    isShowList = True

    try:

        opts, args = getopt.getopt(sys.argv[1:], "v:s:x:", ["version=", "mem_start=", "mem_max="])
        for o, a in opts:
            if o in ["-v", "--version"]:
                if len(a) > 0:
                    version = a
                    isShowList = False
            if o in ["-s", "--mem_start"]:
                if len(a) > 0:
                    mem_start = a
            if o in ["-x", "--mem_max"]:
                if len(a) > 0:
                    mem_max = a               

        showVersionList(isShowList)
        game = GameDownloader(version)
        game.downloadGameJSON()
        game.downloadServer()
        if len(mem_start) > 0 and len(mem_max) > 0 :
            game.deployServer(mem_start=mem_start, mem_max=mem_max)
        elif len(mem_start) > 0:
            game.deployServer(mem_start=mem_start)
        elif len(mem_max) > 0:
            game.deployServer(mem_max=mem_max)
        else :
            game.deployServer()
    except getopt.GetoptError:
        print("The arguments is invalid!") 