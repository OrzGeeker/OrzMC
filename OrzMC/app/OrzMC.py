# -*- coding: utf8 -*-

import argparse
from .Config import Config
from .Game import Game

# argparse 使用文档：https://docs.python.org/3/library/argparse.html
def parse_args():
    '''命令行参数解析'''
    parser = argparse.ArgumentParser(description='A command line tool for start Minecraft client or deploy minecraft server')

    # Tool
    parser.add_argument('-v', metavar='version', dest='version', help='Specified the Minecraft clinet version number to start')

    # Minecraft
    parser.add_argument('-u', metavar='username', default=Config.GAME_DEFAULT_USERNAME, dest='username', help='pick an username(default: %(default)s) for player when start the client')
    server_type_choices = [Config.GAME_TYPE_PURE, Config.GAME_TYPE_FORGE, Config.GAME_TYPE_SPIGOT, Config.GAME_TYPE_PAPER]
    client_type_choices = [Config.GAME_TYPE_PURE, Config.GAME_TYPE_FORGE]
    type_choices = list(set(server_type_choices + client_type_choices))
    sep = '/'
    type_help_info = 'Specified the type of game: "%s" for server, "%s" for client' % (sep.join(server_type_choices), sep.join(client_type_choices))
    parser.add_argument('-t', default=Config.GAME_TYPE_PURE, choices=type_choices, metavar='type', dest='type', help=type_help_info)
    
    # JVM
    parser.add_argument('-m', default='512M', metavar='minmem', dest='minmem', help='Specified the JVM initial memory allocation(default: %(default)s)')
    parser.add_argument('-x', default='2G', metavar='maxmem', dest='maxmem', help='Specified the JVM max memory allocation(default:%(default)s)')
    
    # Flags
    parser.add_argument('-s','--server', default=False, action='store_true', help='deploy minecraft server, if there is no this flag, this command line tool start minecraft as default')
    parser.add_argument('-f','--force_upgrade_world', default=False, action='store_true', help='when deploy spigot/paper server, the option can upgrade your map from old game version')
    parser.add_argument('-b','--backup_world', default=False, action='store_true', help='backup your minecraft world into ~/minecraft_world_backup directory as zip file!')
    parser.add_argument('-o','--optifine', default=False, action='store_true', help='if you have installed optifine for client, you can add this option to launch client with optifine be activated')
    parser.add_argument('-D','--debug', default=False, action='store_true', help='Run Command in Debug Mode')
    parser.add_argument('-V','--verbose', default=False, action='store_true', help='Output some debug info for bugfix')

    args = parser.parse_args()

    return args


def start():
    '''启动游戏'''
    Game(Config(parse_args())).start()
