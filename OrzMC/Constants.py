# -*- coding: utf8 -*-
# 帮助信息
HELP_INFO = """
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
                Specified the type of game: "pure"/"spigot"/"forge" for server, "pure/forge" for client

            -m, --mem_min
                Specified the JVM initial memory allocation

            -x, --mem_max
                Specified the JVM max memory allocation

            -V, --Verbose
                Output some debug info for bugfix

            -h, --help 
                show the command usage info
"""

# 默认用户名
DEFAULT_USERNAME = "guest"

# 命令行输入选项错误提示信息
OPTION_ERR_INFO = "The option is invalid!"

from .utils import ColorString
# 选择版本
ALL_VERSIONS_HINT = ColorString.warn('\nAll Release Versions as follow:\n')
TAB_SPACE = ''
LEADING_SPACE = '  '
VERSION_FORMATTER='{:10}'
SELECT_VERSION_HINT = ColorString.warn('\nPlease select a version number of above list to %s %s ')
DEFAULT_VERSION_HINT = ColorString.error('(default: %s):')
CHOOSED_VERSION = ColorString.confirm('You choose the version: %s')
NOT_FOUND_VERSION = ColorString.warn('There is no such a release version game, use default!')
CHOOSED_DEFAULT_VERSION = ColorString.confirm('You choose the default version(%s)!')

# 选择用户名
CHOOSE_USERNAME_HINT = ColorString.warn('Please choose a username %s ') % ColorString.error('(default: %s):')
CHOOSED_USERNAME = ColorString.confirm('You username in game is: %s')
CHOOSED_DEFAULT_USERNAME = ColorString.warn('Use the default username!!!')