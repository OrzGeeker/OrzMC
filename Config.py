import os

class Config:

    BASE_PATH = os.getcwd()
    GAME_ROOT_DIR = os.path.join(BASE_PATH,'.minecraft')
    GAME_LIB_DIR = os.path.join(GAME_ROOT_DIR,'libraries')
    GAME_VERSION_DIR = os.path.join(GAME_ROOT_DIR,'versions')
    GAME_ASSET_DIR = os.path.join(GAME_ROOT_DIR,'assets')

    def assets_indexes_dir(self):
        dir = os.path.join(Config.GAME_ASSET_DIR,'indexes')
        os.makedirs(dir,exist_ok=True)
        return dir
    
    def assets_objects_dir(self, hash):
        dir = os.path.join(Config.GAME_ASSET_DIR,'objects',hash[0:2])
        os.makedirs(dir,exist_ok=True)
        return dir
    
    def versionDir(self,version):
        dir = os.path.join(Config.GAME_VERSION_DIR,version)
        os.makedirs(dir,exist_ok=True)
        return dir

    def version_json_path(self,version):
        return os.path.join(self.versionDir(version),version+'.json')