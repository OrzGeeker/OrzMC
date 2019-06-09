# -*- coding: utf8 -*-
class PaperAPI:
    ''' api documentation: https://paper.readthedocs.io/en/stable/site/api.html '''
    API = 'https://papermc.io/api/%(API_VERSION)s/%(PROJECT_NAME)s/%(PROJECT_VERSION)s/%(BUILD_ID)s/download'

    @classmethod
    def downloadURL(cls, api_version = 'v1', project_name = 'paper', project_version = None, build_id = 'latest'):
        return   PaperAPI.API % {
            'API_VERSION': api_version,
            'PROJECT_NAME': project_name,
            'PROJECT_VERSION': project_version,
            'BUILD_ID': build_id   
        }

