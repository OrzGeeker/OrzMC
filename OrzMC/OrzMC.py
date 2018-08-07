from OrzMC.GameDownloader import GameDownloader

def startClient():
    game = GameDownloader('1.13')
    game.downloadGameJSON()
    game.downloadClient()
    game.downloadServer()
    game.downloadAssetIndex()
    game.downloadAssetObjects()
    game.donwloadLibraries()
    game.startCient(user='guest')