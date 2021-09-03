# -*- coding: utf8 -*-
import os
import json
import re
from ..utils.utils import makedirs

# https://fabricmc.net/use/

class Fabric:

    _configuration = None

    @classmethod
    def json_configuration(cls, config):
        if Fabric._configuration == None:
            fabric_json_path = os.path.join(config.game_version_client_versions_dir(), config.lastVersionId, config.lastVersionId + '.json')
            if  'fabric' in config.lastVersionId.lower() and os.path.exists(fabric_json_path):
                with open(fabric_json_path, 'r') as f:
                    Fabric._configuration = json.load(f)
        return Fabric._configuration

    @classmethod
    def library_fabric_jar_paths(cls, config):
        ret = []
        for (url, file_path) in Fabric.downloadLibrariesMap(config).items():
            ret.append(file_path)
        return ret

    @classmethod
    def jvmOpts(cls, config):
        ret = []
        for o in Fabric.json_configuration(config).get('arguments').get('jvm'):
            o = re.sub(r'\s','',o)
            ret.append(o)
        return ret

    @classmethod
    def downloadLibrariesMap(cls, config):
        ret = {}
        for l in Fabric.json_configuration(config).get('libraries'):
            name = l.get('name')
            splits = name.split(':')
            splits = splits[0].split('.') + splits[1:]
            file_name = '-'.join(splits[-2:]) + '.jar'
            dir_path = os.path.join(config.game_version_client_library_dir(),*splits)
            makedirs(dir_path)
            url_path ='/'.join(splits + [file_name])
            url = l.get('url') + url_path
            ret[url] = os.path.join(dir_path, file_name)
        return ret
