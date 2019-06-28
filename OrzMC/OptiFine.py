# -*- coding: utf8 -*-
import os
import json

class OptiFine:

    _configuration = None

    @classmethod
    def json_configuration(cls, config):
        if OptiFine._configuration == None:
            optifine_json_path = os.path.join(config.game_version_client_versions_dir(), config.lastVersionId, config.lastVersionId + '.json')
            if  'optifine' in config.lastVersionId.lower() and os.path.exists(optifine_json_path):
                with open(optifine_json_path, 'r') as f:
                    OptiFine._configuration = json.load(f)
        return OptiFine._configuration

    @classmethod
    def library_optifine_jar_paths(cls, config):
        ret = []
        optifine_library_dir = os.path.join(config.game_version_client_library_dir(), 'optifine')
        if 'optifine' in config.lastVersionId.lower() and os.path.exists(optifine_library_dir):
            for dirpath, _, filenames in os.walk(optifine_library_dir):
                for filename in filenames:
                    _, type = os.path.splitext(filename)
                    if type == '.jar':
                        path = os.path.join(dirpath, filename)
                        ret.append(path)
        return ret