# -*- coding: utf8 -*-
from ..utils.ColorString import ColorString
import os
import subprocess
import shutil
from .Config import Config
import yaml

class SkinSystem:
    @classmethod
    def skin_restorer_plugin_config_file_path(cls):
        sr_plugin_config_file_path = os.path.join(Config.game_ftp_server_core_data_plugin_dir(),'SkinsRestorer','config.yml')
        if os.path.exists(sr_plugin_config_file_path) and os.path.isfile(sr_plugin_config_file_path):
            return sr_plugin_config_file_path
        else:
            return None

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
        skin_system_repo_url = 'https://github.com/OrzGeeker/SkinSystem'
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

        # mysql创建库表及用户
        if os.system(cmd) == 0:
            mysql_user = 'skinsystem'
            mysql_database = 'skinsrestorer'
            password = os.popen('head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13').read().strip()
            mysql_host = 'localhost'
            mysql_port = 3306
            enable_mysql = True

            print(ColorString.hint(f'Creating MySQL user {mysql_user}:%s' % password))
            sql = f"DELETE FROM mysql.user WHERE user = '{mysql_user}';"\
            f"DROP USER IF EXISTS '{mysql_user}'@'{mysql_host}';"\
            f"FLUSH PRIVILEGES;"\
            f"CREATE USER '{mysql_user}'@'{mysql_host}' IDENTIFIED WITH mysql_native_password BY '{password}';"\
            f"CREATE DATABASE IF NOT EXISTS {mysql_database};"\
            f"GRANT ALL PRIVILEGES ON {mysql_database} . * TO '{mysql_user}'@'{mysql_host}';"
            try:
                # 配置mysql数据库
                sql_cmd_echo = subprocess.Popen(["echo", f"{sql}"], stdout=subprocess.PIPE)
                sql_create_db = subprocess.Popen(['sudo', 'mysql'], stdin=sql_cmd_echo.stdout, stdout=subprocess.PIPE)
                sql_create_db.communicate()
                print(ColorString.confirm(f"MySQL user skinsystem:{password} was created"))
                print(ColorString.confirm("Have a nice day, remember to save your credensudotials!")) 

                # 写入 SkinRestorer 插件配置文件中
                sr_config_file_path = SkinSystem.skin_restorer_plugin_config_file_path()
                if sr_config_file_path:
                    with open (sr_config_file_path, 'r', encoding = 'utf-8') as cfg:
                        sr_config = yaml.full_load(cfg)
                        sr_config['MySQL']['Enabled'] = enable_mysql
                        sr_config['MySQL']['Host'] = mysql_host
                        sr_config['MySQL']['Port'] = mysql_port
                        sr_config['MySQL']['Database'] = mysql_database
                        sr_config['MySQL']['Username'] = mysql_user
                        sr_config['MySQL']['Password'] = password
                    with open(sr_config_file_path, 'w', encoding = 'utf-8') as cfg:
                        yaml.dump(sr_config, cfg)
                    print(ColorString.confirm('Skin Restorer config.yml write successfully!'))
            except Exception as e:
                print(e)
            
