from OrzMC.Config import Config
import requests
import json
import os

class Mojang:

    version_list_url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
    asset_base_url = 'https://resources.download.minecraft.net/'

    versions = None

    @classmethod
    def get_version_list(cls):
        '''Get All Version Game Configuration And Cache it if need'''
        if None == Mojang.versions:
            cacheFilePath = os.path.join(Config.GAME_ROOT_DIR,os.path.basename(Mojang.version_list_url))
            resp = None
            if os.path.exists(cacheFilePath):
                with open(cacheFilePath,'r') as cache:
                    resp = json.load(cache)
                    print('Use Cache File For Game Version Manifest JSON File')
            else:
                resp = json.loads(requests.get(Mojang.version_list_url).text)
                with open(cacheFilePath,'w') as cacheFile:
                    json.dump(resp,cacheFile)
                    print('Download Game Version Manifest JSON File from Mojang server and cached')

            Mojang.versions = resp.get('versions')
        else:
            print('use cached info in memory')
            
        return Mojang.versions

    @classmethod
    def get_release_version_list(cls):
        versions = Mojang.get_version_list()
        release = list(filter(lambda version: version.get('type') == 'release', versions))
        return release


    @classmethod
    def get_release_game_json(cls, id):
        releases = list(filter(lambda release: release.get('id') == id, Mojang.get_release_version_list()))
        if len(releases) > 0 : 
            url = releases[0].get('url')
            hash = os.path.split(os.path.dirname(url))[-1]
            return (url, hash)
        else:
            return None
        
    @classmethod
    def assets_objects_url(cls,hash):
        return os.path.join(Mojang.asset_base_url,hash[0:2],hash)
    