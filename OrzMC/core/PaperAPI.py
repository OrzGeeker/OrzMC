# -*- coding: utf8 -*-
# papermc: https://papermc.io
# api v1: https://paper.readthedocs.io/en/latest/site/api.html
# api v2: https://papermc.io/api/docs/swagger-ui/index.html?configUrl=/api/openapi/swagger-config

import urllib.request
import urllib.parse
import json

class PaperAPI:
    ''' api documentation: https://paper.readthedocs.io/en/stable/site/api.html '''
    API = 'https://papermc.io/api/%(API_VERSION)s/%(PROJECT_NAME)s/%(PROJECT_VERSION)s/%(BUILD_ID)s/download'
    @classmethod
    def downloadURLV1(cls, project_name = 'paper', project_version = None, build_id = 'latest'):
        return   PaperAPI.API % {
            'API_VERSION': 'v1',
            'PROJECT_NAME': project_name,
            'PROJECT_VERSION': project_version,
            'BUILD_ID': build_id   
        }

    BASE_URL = 'https://papermc.io'
    @classmethod
    def downloadURLV2(cls, version):
        url = 'https://papermc.io/api/'
        url +='v2/'
        url += 'projects/paper/'
        url += 'versions/%s' % version
        jsonResp = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        builds = jsonResp.get('builds')
        latest_build = max(builds)

        url += '/builds/%s' % latest_build
        jsonResp = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        jar_name = jsonResp.get('downloads').get('application').get('name')

        url += '/downloads/%s' % jar_name
        return url



