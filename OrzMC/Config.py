import os

class Config:

    BASE_PATH = os.getcwd()
    GAME_ROOT_DIR = os.path.join(BASE_PATH,'.minecraft')
    GAME_LIB_DIR = os.path.join(GAME_ROOT_DIR,'libraries')
    GAME_VERSION_DIR = os.path.join(GAME_ROOT_DIR,'versions')
    GAME_ASSET_DIR = os.path.join(GAME_ROOT_DIR,'assets')

    def __init__(self,version):
        self.version=version


    def version_json_path(self):
        '''Game Config JSON File Path'''
        return os.path.join(self.versionDir(),self.version+'.json')    

    # Client
    def assets_indexes_dir(self):
        '''Client Assets Index JSON File Directory'''
        dir = os.path.join(Config.GAME_ASSET_DIR,'indexes')
        os.makedirs(dir,exist_ok=True)
        return dir
    
    def assets_objects_dir(self, hash):
        '''Client Assets Object Directory'''
        dir = os.path.join(Config.GAME_ASSET_DIR,'objects',hash[0:2])
        os.makedirs(dir,exist_ok=True)
        return dir
    
    def versionDir(self):
        '''Client Version Related Directory'''
        dir = os.path.join(Config.GAME_VERSION_DIR,self.version)
        os.makedirs(dir,exist_ok=True)
        return dir

    def client_jar_path(self):
        '''Client Game JAR File Path'''
        return os.path.join(Config.GAME_VERSION_DIR,self.version,'client.jar')
    

    def client_library_dir(self, subpath = None):
        '''Client Dependiencies Libraries Directory'''
        dir = Config.GAME_LIB_DIR
        if None != subpath:
            subdir =  os.path.dirname(subpath)
            dir = os.path.join(dir,subdir)
        os.makedirs(dir,exist_ok=True)
        return dir
        
    def client_native_dir(self):
        '''Client Native Related dependencies Directory'''
        dir = os.path.join(self.GAME_VERSION_DIR, self.version, self.version + '-native')
        os.makedirs(dir,exist_ok=True)
        return dir

    # Server
    def server_jar_path(self):
        '''Server Game JAR File Path'''
        return os.path.join(Config.GAME_VERSION_DIR,self.version)        