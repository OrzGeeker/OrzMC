# -*- coding: utf8 -*-
from .Config import Config
from ..core.Mojang import Mojang
from .Constants import *
from ..utils.utils import hint

import os
import json

class Console:
    
    def __init__(self, config):
        '''初始化控制台实例'''
        self.config = config
        
    def userInteraction(self):
        '''控制台展示用户交互界面'''
        if self.config.version == None:
            # 如果没有提示版本参数，则展示可选版本号供用户选择
            self.showVersionList()

        if self.config.username == Config.GAME_DEFAULT_USERNAME and not self.config.is_extract_music:
            # 如果用户名为默认值时，提示用户选择一个自己的用户名进行游戏
            self.showUserName()

        # 客户端启动方式
        self.selectLauncherProfile()

    def showVersionList(self):
        '''控制台交互显示可选客户端版本号'''
        
        # 显示所有版本提示
        print(ALL_VERSIONS_HINT)
        releaseVersions = Mojang.get_release_version_id_list(update = True)

        versionInfo = LEADING_SPACE
        for index, releaseVersion in enumerate(releaseVersions): 
            versionInfo += VERSION_FORMATTER.format(str(releaseVersion))
            if (index + 1) % 5 == 0:
                versionInfo += '\n' + LEADING_SPACE
            else:
                versionInfo += TAB_SPACE
            if releaseVersion == '1.13': 
                break

        print(ColorString.confirm(versionInfo))

        if len(releaseVersions) > 0:
            self.config.version = releaseVersions[0] # 默认版本号

        select = hint(SELECT_VERSION_HINT % ('deploy' if not self.config.is_client else 'play' , DEFAULT_VERSION_HINT % self.config.version))

        if len(select) > 0:
            found = False
            for releaseVersion in releaseVersions: 
                if releaseVersion == select.strip():
                    found = True
                    self.config.version = releaseVersion
                    print(CHOOSED_VERSION % self.config.version)
            if not found:
                print(NOT_FOUND_VERSION)
        else:
            print(CHOOSED_DEFAULT_VERSION % self.config.version)

        print('\n')
    
    def showUserName(self):
        '''控制台交互输入玩家用户名'''
        
        # 只针对客户端有效
        if not self.config.is_client:
            return 

        u = hint(CHOOSE_USERNAME_HINT % self.config.username)

        if len(u) > 0:
            self.config.username = u
            print(CHOOSED_USERNAME % self.config.username)
        else:
            print(CHOOSED_DEFAULT_USERNAME)

        print('\n')


    def selectLauncherProfile(self):

        if not self.config.is_client or not self.config.isPure or not self.config.optifine:
            return 

        launcher_profiles_json_file_path = self.config.game_version_launcher_profiles_json_path()
        if os.path.exists(launcher_profiles_json_file_path):
            content = None
            with open(launcher_profiles_json_file_path, 'r') as f:
                content = json.load(f)
                profiles = content.get('profiles', None)
                count = len(profiles)
                if count > 0:
                    print(ColorString.warn("There are those profiles you can choose to launch: "))
                    index = 0
                    selectedIndex = 0
                    keys = profiles.keys()
                    for key in keys:
                        index = index + 1
                        if key == content['selectedProfile']:
                            selectedIndex = index
                        isSelected = '*' if key == content['selectedProfile'] else ' '
                        print(ColorString.hint('\t%s %s. %s' % (isSelected, index, key)))

                    options = "[1 - %s] " % count if count > 1 else ""
                    try:
                        input = hint(ColorString.warn("Which one you choose %s: " % options))
                        which = int(input) if input and len(input) > 0 else selectedIndex
                        if which >= 1 and which <= count:
                            selected_key = list(keys)[which - 1]
                            self.config.lastVersionId = profiles.get(selected_key).get('lastVersionId')
                            content['selectedProfile'] = selected_key
                        else: 
                            print(ColorString.error("There is no option you specified!"))
                            exit(-1)
                    except:
                        print(ColorString.error("There is no option you specified!"))
                        exit(-1)

            if content != None: 
                with open(launcher_profiles_json_file_path, 'w') as f: 
                    json.dump(content, f)