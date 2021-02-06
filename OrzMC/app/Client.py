# -*- coding: utf8 -*-
from .Config import Config
from .Downloader import Downloader
from ..utils.utils import *
from ..utils.ColorString import ColorString
from ..core.OptiFine import OptiFine
import os
import uuid
import datetime
import shutil

class Client:

    def __init__(self, config):
        self.config = config
        self.downloader = Downloader(self.config)
    
    def start(self):
        if not self.config.is_client:
            return 

        if self.config.isPure :
            self.downloader.downloadGameJSON()
            self.downloader.downloadClient()
            self.downloader.downloadAssetIndex()
            self.downloader.downloadAssetObjects()
            self.downloader.donwloadLibraries()
            self.writeLauncherProfilesJSON()
        elif self.config.isForge:
            self.config.getForgeInfo()
            if not os.path.exists(self.config.game_version_client_jar_file_path()) or not os.path.exists(self.config.game_version_forge_json_file_path()):
                self.extractForgeClient()
        else:
            ColorString.warn('Not Known Client!!!!')
            return

        user = self.config.username
        resolution = ('960', '540')

        if is_sigint_up():
            return
        
        cmd = self.gameArguments(user,resolution)
        backgroundCmd =  cmd + ' &'
        if platformType() == 'windows':
            backgroundCmd = 'start ' + cmd
            backgroundCmd = cmd
            
        os.chdir(self.config.game_version_client_dir())
        os.system(backgroundCmd)
        print(ColorString.confirm('Start Client Successfully!!!'))
        self.formatOutputClientCmd(backgroundCmd)

    '''如果是调试模式，则输出命令行指令内容'''
    def formatOutputClientCmd(self, cmd):
        if self.config.debug and len(cmd) > 0: 
            for e in cmd.split(' '):
                if 'jar' in e:
                    for c in e.split(self.config.java_class_path_list_separator()):
                        print(c)
                else:
                    print(e)

    '''提取java类相关启动参数'''
    def javaClassPathList(self):

        javaClassPathList = []

        libs = self.config.game_version_json_obj().get('libraries')
        total = len(libs)
        
        index = 0
        for lib in libs: 
            downloads = lib.get('downloads')

            rules = lib.get('rules')
            isContinue = False
            if None != rules:
                for rule in rules:
                    if None != rule:
                        if rule.get('action') == 'disallow':
                            if rule.get('os').get('name') == platformType():
                                isContinue

                        if rule.get('action') == 'allow':
                            allow_os = rule.get('os')
                            if allow_os and allow_os.get('name') != platformType():
                                isContinue = True

            if isContinue:
                continue

            libPath = None
            url = None
            sha1 = None
            nativeKey = 'natives-'+ platformType()
            if 'natives' in lib:
                platform = lib.get('natives').get(platformType())
                if platform == None:
                    continue
                else:
                    libPath = downloads.get('classifiers').get(platform).get('path')
                    url = downloads.get('classifiers').get(platform).get('url')
                    sha1 = downloads.get('classifiers').get(platform).get('sha1')
                    nativeFilePath = os.path.join(self.config.game_version_client_native_library_dir(),os.path.basename(url))
                    if not checkFileExist(nativeFilePath,sha1):
                        continue
                    else:
                        javaClassPathList.append(nativeFilePath)
            else:
                classifiers = downloads.get('classifiers')
                if classifiers and nativeKey in downloads.get('classifiers'):
                    url = downloads.get('classifiers').get(nativeKey).get('url')
                    sha1 = downloads.get('classifiers').get(platform).get('sha1')
                    nativeFilePath = os.path.join(self.config.game_version_client_native_library_dir(),os.path.basename(url))
                    if not checkFileExist(nativeFilePath,sha1):
                        continue
                    else:
                        javaClassPathList.append(nativeFilePath)
                        
                libPath = downloads.get('artifact').get('path')
                url = downloads.get('artifact').get('url')
                sha1 = downloads.get('artifact').get('sha1')
                if platformType() == 'windows' :
                    libPath = libPath.replace('/','\\')
                libFilePath = os.path.join(self.config.game_version_client_library_dir(), libPath)
                if not checkFileExist(libFilePath,sha1):
                    continue            
                else:
                    javaClassPathList.append(libFilePath)

            index = index + 1

        if self.config.isForge:
            forge_class_path = map(lambda lib:  os.path.join(self.config.game_version_client_library_dir(),lib.get('downloads').get('artifact').get('path')) ,self.config.game_version_json_obj().get('libraries')) 
            javaClassPathList.extend(forge_class_path)

        javaClassPathList.append(self.config.game_version_client_jar_file_path())

        return javaClassPathList


    def gameArguments(self, user, resolution):

        argPattern = r'\$\{(.*)\}'

        mainCls =  self.config.game_version_json_obj().get('mainClass')
        classPathList = self.javaClassPathList()

        if self.config.isPure and self.config.optifine:
            optifine_config = OptiFine.json_configuration(self.config)
            if optifine_config != None:
                mainCls = optifine_config.get('mainClass')
                optifine_jar_paths = OptiFine.library_optifine_jar_paths(self.config)
                classPathList = optifine_jar_paths + classPathList

        sep = self.config.java_class_path_list_separator()
        classPath = sep.join(classPathList)
        (res_width, res_height) = resolution

        configuration = {
            # for game args
            "auth_player_name" : user,
            "version_name" : self.forgeGame().get('id') if self.config.isForge else self.config.game_version_json_obj().get('id'),
            "game_directory" : self.config.game_version_client_dir(),
            "assets_root" : self.config.game_version_client_assets_dir(),
            "assets_index_name" : self.config.game_version_json_obj().get('assets'),
            "auth_uuid" : ''.join(str(uuid.uuid1()).split('-')),
            "auth_access_token" : ''.join(str(uuid.uuid1()).split('-')),
            "user_type" : "mojang",
            "version_type" : "release",
            "resolution_width":res_width if res_width else "",
            "resolution_height":res_height if res_height else "",
            # for jvm args
            "natives_directory": self.config.game_version_client_native_library_dir(),
            "launcher_name": "OrzMC",
            "launcher_version": '1.0',
            "classpath": classPath,

        }

        java_path = os.popen('which java' if platformType() != 'windows' else 'where java').read().strip()
        if ' ' in java_path:
            java_path = '\"' + java_path + '\"'

        if len(java_path) <= 0:
            ColorString.error('You should installl JDK to run Minecraft')
            exit(-1)

        java_path = 'java'

        arguments = [java_path]

        mem_min = self.config.mem_min
        mem_max = self.config.mem_max

        jvm_opts = [
            '-Xms%s' % mem_min,
            '-Xmx%s' % mem_max,
            '-Djava.net.preferIPv4Stack=true'
        ]
        arguments.extend(jvm_opts)

        game_arguments = self.config.game_version_json_obj().get('arguments')
        jvmArgs = game_arguments.get('jvm') if game_arguments != None else None

        if jvmArgs != None and self.config.isForge:
            jvmArgs.append('-Dfml.ignoreInvalidMinecraftCertificates=true')
            jvmArgs.append('-Dfml.ignorePatchDiscrepancies=true')

        if jvmArgs != None:
            for arg in jvmArgs:
                if isinstance(arg, str):
                    value_placeholder = re.search(argPattern,arg)
                    if value_placeholder:
                        argValue = configuration.get(value_placeholder.group(1))
                        argStr = matchAndReplace(argPattern,argValue,arg)
                        arguments.append(argStr)
                    else:
                        arguments.append(arg)

                elif isinstance(arg, dict):
                    isValid = False
                    rules = arg.get('rules')
                    for rule in rules:
                        if rule.get('os').get('name') == platformType() and rule.get('action') == 'allow':
                            isValid = True
                            break
                    if isValid:
                        value = arg.get('value')
                        if type(value) == list:
                            for i in range(0, len(value)):
                                s = value[i].split('=')
                                if len(s) == 2:
                                    arg = s[1]
                                    if ' ' in arg:
                                        s[1] = '\"' + arg + '\"'
                                        value[i] = '='.join(s)

                            arguments.extend(value)
                        else:
                            arguments.append(value)


        arguments.append(mainCls)

        gameArgs = game_arguments.get('game') if game_arguments != None else None

        if gameArgs != None:
            for arg in gameArgs:
                if isinstance(arg, str):
                    value_placeholder = re.search(argPattern,arg)
                    if value_placeholder:
                        argValue = configuration.get(value_placeholder.group(1))
                        argStr = matchAndReplace(argPattern,argValue,arg)
                        arguments.append(argStr)
                    else:
                        arguments.append(arg)
                elif isinstance(arg, dict):
                    for rule in arg.get('rules'):
                        if rule.get('action') == 'allow':
                            if rule.get('features').get('is_demo_user'):
                                if user ==  None:
                                    arguments.append(arg.get('value'))
                            if rule.get('features').get('has_custom_resolution'):
                                value = arg.get('value')
                                for arg in value:
                                    if isinstance(arg, str):
                                        value_placeholder = re.search(argPattern,arg)
                                        if value_placeholder:
                                            argValue = configuration.get(value_placeholder.group(1))
                                            argStr = matchAndReplace(argPattern,argValue,arg)
                                            arguments.append(argStr)
                                        else:
                                            arguments.append(arg)

        if self.config.isForge:
            arguments.extend(self.config.game_version_json_obj().get('arguments').get('game'))
        
        if self.config.isPure and self.config.optifine:
            optifine_config = OptiFine.json_configuration(self.config)
            if optifine_config != None:
                arguments.extend(optifine_config.get('arguments').get('game'))
        arguments = ' '.join(arguments)
        return arguments

    '''构建Forge客户端'''
    def extractForgeClient(self):
        
        self.download(
            self.config.forgeInfo.forge_installer_url, 
            self.config.game_version_client_dir(), 
            prefix_desc='forge installer jar file'
        )

        installerJarFilePath = os.path.basename(self.config.forgeInfo.forge_installer_url)
        extractForgeClientCmd = 'java -jar ' + installerJarFilePath

        print(ColorString.warn('Start install the forge client jar file ...'))
        os.chdir(self.config.game_version_client_dir())
        os.system(extractForgeClientCmd)
        print(ColorString.confirm('Completed! And the forge client file generated!'))

        forge_client_versions_dir = os.path.join(self.config.game_version_client_dir(), 'versions')
        pure_client_jar = os.path.join(forge_client_versions_dir, self.config.version, self.config.version + '.jar')
        dst_client_jar = os.path.join(self.config.game_version_client_dir(), os.path.basename(pure_client_jar))
        if os.path.exists(pure_client_jar) and not os.path.exists(dst_client_jar):
            shutil.move(pure_client_jar, self.config.game_version_client_dir())

        forge_version_full_name = os.path.basename(self.config.game_version_forge_json_file_path())
        (forge_version_name, _) = os.path.splitext(forge_version_full_name)
        forge_json_file = os.path.join(forge_client_versions_dir, forge_version_name, forge_version_full_name)
        print(forge_json_file)
        dst_forge_json_file = os.path.join(self.config.game_version_client_dir(), os.path.basename(forge_json_file))
        if os.path.exists(forge_json_file) and not os.path.exists(dst_forge_json_file):
            shutil.move(forge_json_file, self.config.game_version_client_dir())

        shutil.rmtree(forge_client_versions_dir)

    def writeLauncherProfilesJSON(self):
        launcher_profiles_json_file_path = self.config.game_version_launcher_profiles_json_path()
        if not os.path.exists(launcher_profiles_json_file_path):
            time = datetime.datetime.now().isoformat()
            version = self.config.version
            content = {
                'profiles': { 
                    version: {
                        'created': time,
                        'type': 'pure',
                        'name': version,
                        'lastVersionId': version,
                        'lastUsed': time
                    }
                },
                'selectedProfile': version,
                'authenticationDatabase': {}
            }

            launcher_profiles_json_file_content = json.dumps(content)

            with open(launcher_profiles_json_file_path,'w',encoding='utf-8') as f:
                f.write(launcher_profiles_json_file_content)