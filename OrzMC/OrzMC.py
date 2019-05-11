# -*- coding: utf8 -*-

from .Game import Game
import sys, getopt
from .Mojang import Mojang
from .utils import hint, ColorString
from .Config import Config
from .Constants import *

config = None

def start():

    global config

    is_client = True
    version = None
    username = None
    game_type = Config.GAME_TYPE_PURE
    mem_min = '128M'
    mem_max = '2G'
    debug = False

    try:

        opts, _ = getopt.getopt(sys.argv[1:], "sv:u:t:m:x:Vh", ["server", "version=", "username=", "game_type=", "mem_min=", "mem_max=", "Verbose" ,"help"])

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

            if o in ["-m", "--mem_min"]:
                if len(a) > 0:
                    mem_min = a

            if o in ["-x", "--mem_max"]:
                if len(a) > 0:
                    mem_max = a

            if o in ["-V", "--Verbose"]:
                    debug = True

            if o in ["-h", "--help"]:
                help()

        # 生成配置信息对象
        config = Config(
            is_client = is_client,
            version = version,
            username = username,
            game_type = game_type,
            mem_min = mem_min,
            mem_max = mem_max,
            debug=debug
        )
        
        # 用户交互
        userInteraction(config)


        if config.is_client:
            # 启动客户端
            Game(config).startClient()
        else:
            # 启动服务端
            Game(config).deployServer()

    except getopt.GetoptError:

        print(OPTION_ERR_INFO) 


def userInteraction(config):
    
    if config == None: 
        return 

    # 显示可用版本信息
    showVersionList(config)

    # 仅客户端显示
    showUserName(config)

    
def showVersionList(config):

    if config.version != None:
        return 
    
    releaseVersions = Mojang.get_release_version_id_list(update = True)

    print(ALL_VERSIONS_HINT)

    versionInfo = LEADING_SPACE
    for index, releaseVersion in enumerate(releaseVersions): 
        versionInfo = versionInfo + VERSION_FORMATTER.format(str(releaseVersion))
        if (index + 1) % 5 == 0:
            versionInfo = versionInfo + '\n' + LEADING_SPACE
        else:
            versionInfo = versionInfo + TAB_SPACE
        if releaseVersion == '1.13': 
            break

    print(ColorString.string(versionInfo,ColorString.FG_GREEN,displayMode=ColorString.HIGHLIGHT))

    if len(releaseVersions) > 0:
        config.version = releaseVersions[0] # 默认版本号

    select = hint(SELECT_VERSION_HINT % ('deploy' if not config.is_client else 'play' , DEFAULT_VERSION_HINT % config.version))
    if len(select) > 0:
        found = False
        for releaseVersion in releaseVersions: 
            if releaseVersion == select.strip():
                found = True
                config.version = releaseVersion
                print(CHOOSED_VERSION % config.version)
        if not found:
            print(NOT_FOUND_VERSION)
    else:
        print(CHOOSED_DEFAULT_VERSION % config.version)

def showUserName(config):

    if config == None or not config.is_client or config.username != None:
        return 

    config.username = DEFAULT_USERNAME

    u = hint(CHOOSE_USERNAME_HINT % config.username)
    if len(u) > 0:
        config.username = u
        print(CHOOSED_USERNAME % config.username)
    else:
        print(CHOOSED_DEFAULT_USERNAME)

def help():
    print(HELP_INFO)
    exit(0)

    