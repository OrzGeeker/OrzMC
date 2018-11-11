from .GameDownloader import GameDownloader
import sys, getopt
from .Mojang import Mojang

def showVersionList():
    allVersions = Mojang.get_version_list(update=True)
    for version in allVersions: 
        print(version)

def startClient():

    version = "1.13"
    username = "guest"

    # showVersionList()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "v:u:", ["version=", "username="])
        for o, a in opts:
            if o in ["-v", "--version"]:
                if len(a) > 0:
                    version = a
            if o in ["-u", "--username"]:
                if len(a) > 0:
                    username = a

        game = GameDownloader(version)
        game.downloadGameJSON()
        game.downloadClient()
        game.downloadServer()
        game.downloadAssetIndex()
        game.downloadAssetObjects()
        game.donwloadLibraries()
        game.startCient(user=username)

    except getopt.GetoptError:
        print("The arguments is invalid!")
    

