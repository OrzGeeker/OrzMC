# -*- coding: utf8 -*-
from json import decoder
from ..utils.utils import *
from ..utils.ColorString import ColorString
from ..core.PaperAPI import PaperAPI
from ..core.Mojang import Mojang
from ..core.Spigot import Spigot
from ..core.Forge import Forge
from ..core.OptiFine import OptiFine
from ..core.BMCLAPI import BMCLAPI

from tqdm import tqdm
import requests
import shutil

class Downloader:

    def __init__(self, config):
        self.config = config

    def downloadGameJSON(self):
        '''Download Game Json Configure File'''

        if is_sigint_up():
            return

        version_json_path = self.config.game_version_json_file_path()
        (url, hash) = Mojang.get_release_game_json(self.config.version)
        if not checkFileExist(version_json_path, hash):
            print("Download Game Json Configure File!")
            jsonStr = requests.get(url).text
            writeContentToFile(jsonStr, version_json_path)
        else: 
            print("Game Json Configure File have been downloaded!")

    def downloadClient(self):
        '''Download Client Jar File'''
        if is_sigint_up():
            return  

        client = self.config.game_version_json_obj().get('downloads').get('client')
        clientUrl = client.get('url')
        sha1 = client.get('sha1')
        clientJARFilePath = self.config.game_version_client_jar_file_path()
        if not checkFileExist(clientJARFilePath, sha1):
            self.download(
                clientUrl,
                os.path.dirname(clientJARFilePath), 
                self.config.game_version_client_jar_filename(), 
                prefix_desc='client jar file'
            )
        else:
            print("client jar file existed!")

    
    def downloadAssetIndex(self):
        '''Download Game Asset Index JSON file'''
        if is_sigint_up():
            return

        assetIndex = self.config.game_version_json_obj().get('assetIndex')
        index_json_url = assetIndex.get('url')
        index_json_sha1 = assetIndex.get('sha1')
        index_json_path= os.path.join(self.config.game_version_client_assets_indexs_dir(), os.path.basename(index_json_url))
        if not checkFileExist(index_json_path,index_json_sha1):
            print("Download assetIndex JSON File")
            index_json_str = requests.get(index_json_url).text
            with open(index_json_path,'w',encoding='utf-8') as f:
                f.write(index_json_str)
        else:
            print("assetIndex JSON File have been downloaded")
    
    def downloadAssetObjects(self):
        '''Download Game Asset Objects'''
        objects = self.config.game_version_json_assets_obj().get('objects')
        total = len(objects)

        index = 0
        for (name,object) in objects.items():

            if is_sigint_up():
                return

            index = index + 1
            hash = object.get('hash')
            url = Mojang.assets_objects_url(hash)
            object_dir = self.config.game_version_client_assets_objects_dir(hash)
            object_filePath = os.path.join(object_dir,os.path.basename(url))
            if not checkFileExist(object_filePath, hash):
                prefix_desc = 'assets objects %d/%d(%.2f%%)' % (index, total, 100.0 * index / total)
                self.download(url,object_dir, prefix_desc=prefix_desc)
            
            # 收集ogg音乐文件
            if self.config.is_extract_music:
                path, type = os.path.splitext(name)
                filename = path.replace(os.sep, '_') + '.mp3'
                if type == '.ogg':
                    target_file_path = os.path.join(self.config.game_version_client_mp3_dir(),filename)
                    convertOggToMap3(object_filePath, target_file_path)

        if self.config.is_extract_music:
            music_dir = os.path.dirname(self.config.game_version_client_mp3_dir())
            print(ColorString.confirm('music has been extracted to dir: %s' % music_dir))
            exit(0)

    def donwloadLibraries(self):
        ''' download libraries'''
        libs = self.config.game_version_json_obj().get('libraries')
        total = len(libs)

        index = 0
        for lib in libs: 

            if is_sigint_up():
                return

            index = index + 1
            prefix_desc = 'libraries %d/%d' % (index, total)
            downloads = lib.get('downloads')
            rules = lib.get('rules')

            isContinue = False
            if None != rules:
                for rule in rules:
                    if None != rule:
                        if rule.get('action') == 'disallow':
                            if rule.get('os').get('name') == platformType():
                                isContinue = True

                        if rule.get('action') == 'allow':
                            allow_os = rule.get('os')
                            if allow_os and allow_os.get('name') != platformType():
                                isContinue = True

            if isContinue: 
                continue

            libPath = None
            url = None
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
                        self.download(url,self.config.game_version_client_native_library_dir(), prefix_desc=prefix_desc)
                    
            else:
                classifiers = downloads.get('classifiers')
                if classifiers and nativeKey in downloads.get('classifiers'):
                    url = downloads.get('classifiers').get(nativeKey).get('url')
                    sha1 = downloads.get('classifiers').get(platform).get('sha1')
                    nativeFilePath = os.path.join(self.config.game_version_client_native_library_dir(),os.path.basename(url))
                    if not checkFileExist(nativeFilePath,sha1):
                        self.download(url,self.config.game_version_client_native_library_dir(), prefix_desc=prefix_desc)
                
                libPath = downloads.get('artifact').get('path')
                url = downloads.get('artifact').get('url')
                sha1 = downloads.get('artifact').get('sha1')
                fileDir = self.config.game_version_client_library_dir(libPath)
                filePath=os.path.join(fileDir,os.path.basename(url))
                if not checkFileExist(filePath,sha1):
                    self.download(url,fileDir, prefix_desc=prefix_desc)

    def downloadPaperServerJarFile(self):
        '''下载Paper服务端JAR文件'''
        url = None
        if self.config.api == 'v1':
            url = PaperAPI.downloadURLV1(
                project_name = 'paper',
                project_version = self.config.version,
                build_id = 'latest'
            )
        elif self.config.api == 'v2':
            url = PaperAPI.downloadURLV2(
                version = self.config.version
            )

        if url and len(url) > 0:
            self.download(
                url, 
                self.config.game_version_server_dir(), 
                self.config.game_version_server_jar_filename(), 
                prefix_desc='paper server file'
            )


    retry_count = 0
    MAX_RETRY_COUNT = 3
    def download(self, url, dir, name = None, prefix_desc = None):
        '''通用下载方法'''
        original_url = url
        original_dir = dir
        original_name = name
        oritinal_prefix_desc = prefix_desc

        url = self.redirectUrl(url=url)

        if is_sigint_up():
            return

        if name == None:
            filename = os.path.basename(url)
        else:
            filename = name
        
        try:
            # 临时文件中转目录
            target_file = os.path.join(dir,filename)
            download_temp_file = os.path.join(self.config.game_download_temp_dir(), filename)
            
            total_size = int(requests.head(url).headers["Content-Length"])
            kb_chunk_size = 1024 # 单位: 1K
            mb_chunk_size = 1024 * 1024 # 单位: 1M
            
            # 大于10M的通过流式下载
            if total_size > 10 * mb_chunk_size:
                mb_size = int(total_size / mb_chunk_size + 0.5)
                res = requests.get(url, stream = True)
                # 先下载到临时目录
                with open(download_temp_file,'wb') as f:
                    desc = ((prefix_desc + ' - ') if len(prefix_desc) > 0 else  '') + 'downloading: %s(%sMB)' % (filename, mb_size)
                    for chunk in tqdm(iterable=res.iter_content(mb_chunk_size),total=mb_size,unit='MB',desc=desc):
                        f.write(chunk)

                # 下载并写入临时目录后，移动到目标位置, 如果目标位置已存在文件，先删除
                if os.path.exists(target_file):
                    os.remove(target_file)
                # 移动临时文件到目标位置
                shutil.move(download_temp_file, target_file)
            else:
                # 小于10M的直接下载到内存，然后转存
                with open(target_file, 'wb') as f:
                    f.write(requests.get(url).content)
                kb_size = int(total_size / kb_chunk_size + 0.5)
                desc = (prefix_desc + ' - ' if len(prefix_desc) > 0 else '') + ('%s(%sKB)' % (os.path.basename(url), kb_size))
                print(desc)

            # 下载成功，重置重试次数
            if Downloader.retry_count > 0:
                Downloader.retry_count = 0

        except Exception as e:
            # 如果下载失败, 则提示
            print(e)
            print(ColorString.error('download failed: %s' % url))

            sleep(1)
            Downloader.retry_count += 1
            if Downloader.retry_count <= Downloader.MAX_RETRY_COUNT:
                print(ColorString.warn('[%s]retry download: %s' % (Downloader.retry_count, original_url)))
                self.download(original_url, original_dir, original_name, oritinal_prefix_desc)
            else:
                print(ColorString.error('retry %s times and failed! jump to donwload next url' % Downloader.MAX_RETRY_COUNT))
                Downloader.MAX_RETRY_COUNT = 0

    def redirectUrl(self,url):

        domain = getUrlDomain(url)
        if domain and self.config.is_client and self.config.bmclapi:
            redirected_url = changeUrlDomain(url, BMCLAPI.mojang_bmclapi_domain_map[domain])
            if self.config.debug:
                print(redirected_url)
            return redirected_url

        return url