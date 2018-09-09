from .Config import Config
import requests
import json
import os

class Mojang:

    version_list_url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
    asset_base_url = 'https://resources.download.minecraft.net/'

    versions = None

    @classmethod
    def get_version_list(cls):
        '''Get All Version Game Configuration'''
        localFilePath = os.path.join(Config.GAME_ROOT_DIR,os.path.basename(Mojang.version_list_url))
        resp = None
        if os.path.exists(localFilePath):
            with open(localFilePath,'r') as localFile:
                resp = json.load(localFile)
                print('Use Local File For Game Version Manifest JSON File')
        else:
            resp = json.loads(requests.get(Mojang.version_list_url).text)
            with open(localFilePath,'w') as localFile:
                json.dump(resp,localFile)
                print('Download Game Version Manifest JSON File from Mojang server and cached')


        Mojang.versions = resp.get('versions')    
        return Mojang.versions

    @classmethod
    def get_release_version_list(cls):
        '''Get Game Release Version List'''
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
    