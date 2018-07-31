from OrzMC.Config import Config
import requests
import json
import os

class Mojang:

    version_list_url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
    asset_base_url = 'https://resources.download.minecraft.net/'

    @classmethod
    def get_version_list(cls):
        '''Get All Version Game Configuration And Cache it if need'''

        resp = None
        if os.path.exists(cacheFilePath):
            with open(cacheFilePath,'r') as cache:
                resp = json.load(cache)
        else:
            resp = json.loads(requests.get(Mojang.version_list_url).text)
            with open(cacheFilePath,'w') as cacheFile:
                json.dump(resp,cacheFile)

        versions = resp.get('versions')
        
        return versions

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
            jsonStr = requests.get(url).text
            return jsonStr
        else:
            return None
        
    @classmethod
    def assets_objects_url(cls,hash):
        return os.path.join(Mojang.asset_base_url,hash[0:2],hash)
    