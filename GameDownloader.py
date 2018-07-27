from Mojang import Mojang
from Config import Config
import json
import requests
import os

class GameDownloader:

    def __init__(self):
        self.config = Config()

    def download(self, url, dir):
        filename = os.path.basename(url)
        with open(os.path.join(dir,filename),'wb') as f:
            f.write(requests.get(url).content)


    def downloadGame(self, version = '1.13'):
        self.version = version
        jsonStr = Mojang.get_release_game_json(version)
        self.game = json.loads(jsonStr)
        if jsonStr != None:
            version_json_path = self.config.version_json_path(version)
            with open(version_json_path,'w',encoding='utf-8') as f:
                f.write(Mojang.get_release_game_json(version))

# Client
    def downloadAssetIndex(self):
        index_json_url = self.game.get('assetIndex').get('url')
        filename = os.path.basename(index_json_url)
        index_json_str = requests.get(index_json_url).text
        self.assets = json.loads(index_json_str)
        with open(os.path.join(self.config.assets_indexes_dir(),filename),'w',encoding='utf-8') as f:
            f.write(index_json_str)

    def downloadAssetObjects(self):
        objects = self.assets.get('objects')
        for (path,object) in objects.items():
            hash = object.get('hash')
            url = os.path.join(Mojang.asset_base_url,hash[0:2],hash)
            object_dir = self.config.assets_objects_dir(hash)
            self.download(url,object_dir)
            print('.')

    def downloadAsset(self):
        self.downloadAssetIndex()
        self.downloadAssetObjects()



    def downloadClient(self):
        clientUrl = self.game.get('downloads').get('client').get('url')
        print('Downloading the client jar file ...')
        dir = os.path.join(self.config.GAME_VERSION_DIR,self.version)
        self.download(clientUrl,dir)
        print("Client Download Completed!")

    def startClient(self):
        # self.downloadClient()
        self.downloadAsset()

# Server

    def downloadServer(self):
        serverUrl = self.game.get('downloads').get('server').get('url')
        print('Downloading the server jar file ...')
        dir = os.path.join(self.config.GAME_VERSION_DIR,self.version)
        self.download(serverUrl,dir)
        print("Server Download Completed!")

    def startServer(self):
        self.downloadServer()


if __name__ == '__main__':
    game = GameDownloader()
    game.downloadGame()
    game.startClient()
    # game.startServer()