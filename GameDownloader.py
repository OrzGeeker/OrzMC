from Mojang import Mojang
from Config import Config
import json
import requests
import os

class GameDownloader:

    def __init__(self, version):
        self._game=None
        self._assets=None
        self.config = Config(version)

    def download(self, url, dir):
        filename = os.path.basename(url)
        with open(os.path.join(dir,filename),'wb') as f:
            f.write(requests.get(url).content)

    def loadJSON(self, filePath):
        with open(filePath) as json_data:
            jsonObj = json.load(json_data)
            return jsonObj

    def downloadGameJSON(self):
        '''Download Game Json Configure File'''
        jsonStr = Mojang.get_release_game_json(self.config.version)
        if jsonStr != None:
            version_json_path = self.config.version_json_path()
            with open(version_json_path,'w',encoding='utf-8') as f:
                f.write(Mojang.get_release_game_json(self.config.version))
    
    def game(self):
        if self._game == None:
            self._game = self.loadJSON(self.config.version_json_path())
        return self._game
    
    def assets(self):
        if self._assets == None:
            index_json_url = self.game().get('assetIndex').get('url')
            index_json_path = os.path.join(self.config.assets_indexes_dir(), os.path.basename(index_json_url))
            self._assets = self.loadJSON(index_json_path)
        return self._assets

# Assets

    def downloadAssetIndex(self):
        index_json_url = self.game().get('assetIndex').get('url')
        index_json_str = requests.get(index_json_url).text
        index_json_path= os.path.join(self.config.assets_indexes_dir(), os.path.basename(index_json_url))
        with open(index_json_path,'w',encoding='utf-8') as f:
            f.write(index_json_str)

    def downloadAssetObjects(self):
        objects = self.assets().get('objects')
        total = len(objects)
        index = 0
        for (name,object) in objects.items():
            index = index + 1
            outInfo = '%d/%d(%s)' % (index, total, name)
            
            hash = object.get('hash')
            url = Mojang.assets_objects_url(hash)
            object_dir = self.config.assets_objects_dir(hash)

            try:
                self.download(url,object_dir)
                print(outInfo)
            except:
                print(outInfo + "FAILED!")
                continue
            

# Client

    def downloadClient(self):
        '''Download Client Jar File'''
        clientUrl = self.game().get('downloads').get('client').get('url')
        print('Downloading the client jar file ...')
        self.download(clientUrl,self.config.client_jar_path())
        print("Client Download Completed!")


# Server

    def downloadServer(self):
        '''Download Server Jar File'''
        serverUrl = self.game().get('downloads').get('server').get('url')
        print('Downloading the server jar file ...')
        self.download(serverUrl,self.config.server_jar_path())
        print("Server Download Completed!")


if __name__ == '__main__':
    game = GameDownloader('1.13')
    # game.downloadGameJSON()
    # game.downloadClient()
    # game.downloadServer()
    # game.downloadAssetIndex()
    game.downloadAssetObjects()