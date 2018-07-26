from Mojang import Mojang
from Config import Config

class GameDownloader:

    def __init__(self):
        self.config = Config()

    def downloadGame(self, version = '1.13'):
        jsonStr = Mojang.get_release_game_json(version)
        if jsonStr != None:
            version_json_path = self.config.version_json_path(version)
            with open(version_json_path,'w',encoding='utf-8') as f:
                f.write(Mojang.get_release_game_json(version))


    def downloadAsset(self):
        pass

    def startClient(self):
        pass

    def startServer(self):
        pass


if __name__ == '__main__':
    game = GameDownloader()
    game.downloadGame()
    game.downloadAsset()
    game.startClient()