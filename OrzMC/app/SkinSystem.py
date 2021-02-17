# -*- coding: utf8 -*-
from ..utils.ColorString import ColorString
import os

class SkinSystem:
    @classmethod
    def setup(cls):
        tools = [
            'mysql-server',
            'nginx',
            'php-fpm',
            'php-curl',
            'php-mysql',
            'php-gd',
            'git'
        ]
        print(ColorString.hint("installing skinsystem (%s)" % ColorString.warn(','.join(tools))))
        bins = ' '.join(tools)
        skin_system_repo_url = 'https://github.com/riflowth/SkinSystem'
        skin_system_dir = os.path.basename(skin_system_repo_url)
        web_site_dir = '/var/www'
        skin_system_web_absolute_dir = os.path.join(web_site_dir, skin_system_dir)
        cmd = f'sudo apt-get update || sudo apt-get install {bins} -y && '\
        f'cd {web_site_dir} && git clone {skin_system_repo_url} && cd {skin_system_dir} && '\
        f'git checkout `git tag | sort -V | grep -v "\-rc" | tail -1` && '\
        f'rm -rf .git && rm -rf .gitignore && rm -rf *.md && cd .. && '\
        f'chmod 775 -R {skin_system_web_absolute_dir} && chown -R www-data:www-data {skin_system_web_absolute_dir}'
        if os.system(cmd) == 0:
            password = os.popen('head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13').read().strip()
            print(ColorString.hint('Creating MySQL user skinsystem:%s' % password))
            sql = f"CREATE USER 'skinsystem'@'localhost' IDENTIFIED BY '{password}';"\
            f"CREATE DATABASE skinsrestorer;"\
            f"GRANT ALL PRIVILEGES ON skinsrestorer . * TO 'skinsystem'@'localhost';"
            cmd = f'echo {sql} | mysql'
            if os.system(cmd) == 0:
                print(ColorString.confirm(f"MySQL user skinsystem:{password} was created"))
                print(ColorString.confirm("Have a nice day, remember to save your credentials!")) 
            
