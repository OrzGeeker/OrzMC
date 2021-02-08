# -*- coding: utf8 -*-

from ..utils.ColorString import ColorString
from .Version import *

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

# 工具版本号
ORZMC_VERSION_NUMBER_STR = ColorString.warn('OrzMC version: %s' % ORZMC_VERSION_NUMBER)

# BMCLAPI下载版权提示
BMCLAPI_DESC = ColorString.hint('\nCurrent file download service using ') + ColorString.confirm('BMCLAPI\n')