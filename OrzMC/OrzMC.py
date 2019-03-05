# -*- coding: utf8 -*-

from .GameDownloader import GameDownloader
import sys, getopt
from .Mojang import Mojang
from .utils import hint, ColorString
from .Config import Config


config = None

def start():

    global config

    is_client = True
    version = None
    username = None
    game_type = Config.GAME_TYPE_PURE
    mem_min = None
    mem_max = None

    try:

        opts, _ = getopt.getopt(sys.argv[1:], "sv:u:t:m:x:h", ["server", "version=", "username=", "game_type=", "mem_min=", "mem_max=", "help"])

        for o, a in opts:

            if o in ["-s", "--server"]:
                is_client = False

            if o in ["-v", "--version"]:
                if len(a) > 0:
                    version = a

            if o in ["-u", "--username"]:
                if len(a) > 0:
                    username = a

            if o in ["-t", "--game_type"]:
                if len(a) > 0:
                    game_type = a

            if o in ["-m" "--mem_min"]:
                if len(a) > 0:
                    mem_min = a

            if o in ["-x", "--mem_max"]:
                if len(a) > 0:
                    mem_max = a

            if o in ["-h", "--help"]:
                help()

        config = Config(is_client = is_client, version = version, username = username, game_type = game_type, mem_min = mem_min, mem_max = mem_max)
        
        # 交互前
        config.status()

        # 用户交互
        userInteraction()

        # 交互后
        config.status()

        if config.is_client:

            # 启动客户端
            startClient()
        else:
            # 启动服务端
            startServer()

    except getopt.GetoptError:

        print("The arguments is invalid!") 


def userInteraction():
    
    global config

    if config == None: 
        return 

    showVersionList()

    # 仅客户端显示
    showUserName()

    
def showVersionList():

    global config

    if config.version != None:
        return 

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
        config.version = releaseVersions[0] # 默认版本号

    select = hint(ColorString.warn('\nPlease select a version number of above list to %s %s ') % ('deploy' if not config.is_client else 'play' , ColorString.error('(default: %s):' % config.version)))
    if len(select) > 0:
        found = False
        for releaseVersion in releaseVersions: 
            if releaseVersion == select.strip():
                found = True
                config.version = releaseVersion
                print(ColorString.confirm('You choose the version: %s') % config.version)
        if not found:
            print(ColorString.warn('There is no such a release version game, use default!'))
    else:
        print(ColorString.confirm('You choose the default version(%s)!') % config.version)

def showUserName():

    global config

    if  not config.is_client or config.username != None:
        return 

    # 默认用户名
    config.username = "guest"

    u = hint(ColorString.warn('Please choose a username %s ') % ColorString.error('(default: %s):' % config.username))
    if len(u) > 0:
        config.username = u
        print(ColorString.confirm('You username in game is: %s') % config.username)
    else:
        print(ColorString.warn('Use the default username!!!'))


def startClient():
    global config
    GameDownloader(config).startClient()

def startServer():
    global config
    GameDownloader(config).deployServer()


def help():
    print("""
    NAME

        orzmc -- A command line tool for start minecraft client or deploy minecraft server

    Usage

        orzmc [-v client_version_number] [-u username] [-h]

            -s, --server
                deploy minecraft server, if there is no this flag, this command line tool start minecraft as default
        
            -v, --version  
                Specified the Minecraft clinet version number to start

            -u, --username 
                pick an username for player when start the client

            -t, --game_type
                Specified the type of game, such as "pure"/"spigot"/"forge"

            -m, --mem_min
                Specified the JVM initial memory allocation

            -x, --mem_max
                Specified the JVM max memory allocation

            -h, --help 
                show the command usage info

    """)
    exit(0)

    