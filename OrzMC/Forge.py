from bs4 import BeautifulSoup
import requests
from .utils import ColorString
import os

class Forge:

    def __init__(self, version):
        self.version = version
        self.fullVersion = None
        self.version_homePage = 'https://files.minecraftforge.net/maven/net/minecraftforge/forge/index_%s.html' % self.version
        print(ColorString.warn('parsing the forge installer download link...'))
        html = requests.get(self.version_homePage).text
        soup = BeautifulSoup(html, 'html.parser')
        installer = list(map(lambda i: i.parent.get('href'), soup.select('.classifier-installer')))[0]
        if len(installer) > 0:
            self.forge_installer_url = installer.split('&')[1].split('=')[1]
            self.fullVersion = '-'.join(os.path.basename(self.forge_installer_url).split('-')[0:-1])
            print(ColorString.confirm('Get the forge installer download link!!'))
        else:
            print(ColorString.error( 'Not Found Any Installer!!!!'))

            

