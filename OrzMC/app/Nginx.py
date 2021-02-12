# -*- coding: utf8 -*-
from .Config import Config
from ..utils.ColorString import ColorString
import os

class Nginx:
    @classmethod
    def setup(cls):
        '''配置并启动nginx'''
        nginx_config_file = Config.game_version_server_nginx_file_path()
        try:
            with open(nginx_config_file, 'w', encoding='utf-8') as cfg:
                cfg.write('\n'.join([
                    Nginx.web_file_server_conf(), 
                    Nginx.web_live_map_conf(), 
                    Nginx.web_skin_system_conf(),
                ]))
                print(ColorString.confirm('Nginx conf file location: %s' % nginx_config_file))
            
            # 创建nginx配置文件软链接
            nginx_conf_dir = '/etc/nginx/conf.d'
            if os.path.exists(nginx_conf_dir) and os.path.isdir(nginx_conf_dir):
                minecraft_nginx_conf_file = os.path.join(nginx_conf_dir, os.path.basename(nginx_config_file))
                cmd = 'sudo ln -snf %s %s && sudo nginx -s stop && sudo nginx -s reload && sudo nginx ' % (nginx_config_file, minecraft_nginx_conf_file)
                ret = os.system(cmd)
                if ret == 0:
                    print(ColorString.confirm('Create symbol link file: %s' % minecraft_nginx_conf_file))
        except Exception as e:
            print(e)
            print(ColorString.error('Config Nginx for Minecraft Failed!!!'))
            exit(-1)

    @classmethod
    def setupSSL(cls):
        '''配置nginx服务支持https'''
        cmd = 'eval "$(curl -sL https://raw.githubusercontent.com/wangzhizhou/Linux_scripts/master/https/certbot_nginx_ubuntu18.04.sh)"'
        os.system(cmd)

    
    @classmethod
    def web_file_server_conf(cls):
        '''配置minecraft文件服务器'''
        port=80
        file_server_root_dir = Config.game_ftp_server_base_dir()
        server_domain = 'download.jokerhub.cn'

        return f"""
# 我的世界文件服务器
server {{
    listen {port};
    server_name {server_domain};
    root {file_server_root_dir};

    autoindex on;
    autoindex_exact_size off;
    autoindex_localtime on;

    location / {{
        try_files $uri $uri/ =404;
    }}
}}
"""

    @classmethod
    def web_skin_system_conf(cls):
        '''配置minecraft皮肤系统'''
        port=80
        file_server_root_dir = '/var/www/SkinSystem'
        server_domain = 'skin.jokerhub.cn'
        fastcgi_pass = 'unix:/run/php/php7.2-fpm.sock'
        return f"""
# Minecraft SkinSystem
server {{
    listen {port};
    server_name {server_domain};
    root {file_server_root_dir};

    # Add index.php to the list if you are using PHP
    index index.php index.html index.htm index.nginx-debian.html;
    location / {{
        try_files $uri $uri/ =404;
    }}

    # pass PHP scripts to FastCGI server
    location ~ \.php$ {{
        include snippets/fastcgi-php.conf;
        # With php-fpm (or other unix sockets):
        fastcgi_pass {fastcgi_pass};
    }}
}}
"""

    @classmethod
    def web_live_map_conf(cls):
        '''配置minecraft地图'''
        port=80
        server_domain = 'map.jokerhub.cn'
        return f"""
server {{
    listen {port};
    server_name {server_domain};
    location / {{
        proxy_pass      http://localhost:8123;
    }}
}}
"""