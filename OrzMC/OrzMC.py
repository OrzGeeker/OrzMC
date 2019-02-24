# -*- coding: utf8 -*-

from .GameDownloader import GameDownloader
import sys, getopt
from .Mojang import Mojang
from .utils import hint, ColorString

version = ""
username = "guest"

def showVersionList(isShow = True, isServer = False):
    
    global version

    if not isShow: return

    allVersions = Mojang.get_version_list(update=True)
    releases = list(filter(lambda version: version.get('type') == 'release', allVersions))
    releaseVersions = list(map(lambda info: info.get('id', ''), releases))
    print(ColorString.warn('\nAll Release Versions as follow:\n'))
    tabSpace = '\t'
    lineLeadingSpace = '  '
    versionInfo = lineLeadingSpace
    for index, releaseVersion in enumerate(releaseVersions): 
        versionInfo = versionInfo + str(releaseVersion)
        if (index + 1) % 9 == 0:
            versionInfo = versionInfo + '\n' + lineLeadingSpace
        else:
            versionInfo = versionInfo + tabSpace
    print(ColorString.string(versionInfo,ColorString.FG_GREEN,displayMode=ColorString.HIGHLIGHT))

    if len(releaseVersions) > 0:
        version = releaseVersions[0]

    select = hint(ColorString.warn('\nPlease select a version number of above list to %s %s ') % ('deploy' if isServer else 'play' , ColorString.error('(default: %s):' % version)))
    if len(select) > 0:
        found = False
        for releaseVersion in releaseVersions: 
            if releaseVersion == select.strip():
                found = True
                version = releaseVersion
                print(ColorString.confirm('You choose the version: %s') % version)
        if not found:
            print(ColorString.warn('There is no such a release version game, use default!'))
    else:
        print(ColorString.confirm('You choose the default version(%s)!') % version)

def showUserName(isShow):

    if not isShow: return 

    global username

    u = hint(ColorString.warn('Please choose a username %s ') % ColorString.error('(default: %s):' % username))
    if len(u) > 0:
        username = u
        print(ColorString.confirm('You username in game is: %s') % username)
    else:
        print(ColorString.warn('Use the default username!!!'))


def startClient():

    isShowList = True
    isShowUserName = True

    global version
    global username

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "v:u:h", ["version=", "username=","help"])
        for o, a in opts:
            if o in ["-v", "--version"]:
                if len(a) > 0:
                    version = a
                    isShowList = False
            if o in ["-u", "--username"]:
                if len(a) > 0:
                    username = a
                    isShowUserName = False
            if o in ["-h", "--help"]:
                help()

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
    isSpigotServer = False

    try:

        opts, _ = getopt.getopt(sys.argv[1:], "v:s:x:ho", ["version=", "mem_start=", "mem_max=","help", "spigot"])
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
            if o in ["-h", "--help"]:
                help(False)
            if o in ["-o", "--spigot"]:
                isSpigotServer = True


        showVersionList(isShowList, isServer=True)
        game = GameDownloader(version, isSpigot=isSpigotServer)
        if not isSpigotServer:
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


def help(isClient = True):

    if isClient:
        print("""
        NAME

            orzmc -- A command for start minecraft client

        Usage

            orzmc [-v client_version_number] [-u username] [-h]

                -v, --version  
                    Specified the Minecraft clinet version number to start

                -u, --username 
                    pick an username for player when start the client

                -h, --help 
                    show the client command usage info

        """)
    else:
        print("""
        NAME

            orzmcs -- A tool for deploy minecraft server

        Usage: 
           
            orzmcs [-v server_version_number] [-s memory_start] [-x memory_max] [-ho]

                -v, --version 
                    Specified the Minecraft server version number to deploy
                
                -s, --mem_start 
                    Specified the JVM initial memory allocation
                
                -x, --mem_max
                    Specified the JVM max memory allocation
                
                -h, --help
                    show the server command usage info
                
                -o, --spigot
                    deploy spigot server for performance boost

        """)
    exit(0)