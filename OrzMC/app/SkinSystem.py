# -*- coding: utf8 -*-
from ..utils.ColorString import ColorString
import os
import subprocess
import shutil

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
        if os.path.exists(skin_system_web_absolute_dir):
            cmd = f'sudo rm -rf {skin_system_web_absolute_dir}'
            os.system(cmd)
        cmd = f'sudo apt-get update || sudo apt-get install {bins} -y && '\
        f'cd {web_site_dir} && sudo git clone {skin_system_repo_url} && cd {skin_system_dir} && '\
        f'sudo git checkout `git tag | sort -V | grep -v "\-rc" | tail -1` && '\
        f'sudo rm -rf .git && sudo rm -rf .gitignore && sudo rm -rf *.md && cd .. && '\
        f'sudo chmod 775 -R {skin_system_web_absolute_dir} && sudo chown -R www-data:www-data {skin_system_web_absolute_dir}'
        if os.system(cmd) == 0:
            mysql_user = 'skinsystem'
            mysql_database = 'skinsrestorer'
            password = os.popen('head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13').read().strip()
            print(ColorString.hint(f'Creating MySQL user {mysql_user}:%s' % password))
            sql = f"DELETE FROM mysql.user WHERE user = '{mysql_user}';"\
            f"CREATE USER '{mysql_user}'@'localhost' IDENTIFIED BY '{password}';"\
            f"CREATE DATABASE {mysql_database};"\
            f"GRANT ALL PRIVILEGES ON {mysql_database} . * TO '{mysql_user}'@'localhost';"
            try:
                sql_cmd_echo = subprocess.Popen(["echo", f"{sql}"], stdout=subprocess.PIPE)
                sql_create_db = subprocess.Popen(['sudo', 'mysql'], stdin=sql_cmd_echo.stdout, stdout=subprocess.PIPE)
                sql_create_db.communicate()
                print(ColorString.confirm(f"MySQL user skinsystem:{password} was created"))
                print(ColorString.confirm("Have a nice day, remember to save your credentials!")) 
            except Exception as e:
                print(e)
            
