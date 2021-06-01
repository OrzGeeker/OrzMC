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
                cfg.write('\n'.join(filter(lambda x: x != None,[
                    Nginx.web_file_server_conf(), 
                    Nginx.web_live_map_conf(), 
                    Nginx.web_skin_system_conf(),
                ])))
                print(ColorString.confirm('Nginx conf file location: %s' % nginx_config_file))
            
            # 创建nginx配置文件软链接
            nginx_conf_dir = '/etc/nginx/conf.d'
            if os.path.exists(nginx_conf_dir) and os.path.isdir(nginx_conf_dir):
                minecraft_nginx_conf_file = os.path.join(nginx_conf_dir, os.path.basename(nginx_config_file))
                cmd = 'sudo ln -snf %s %s' % (nginx_config_file, minecraft_nginx_conf_file)
                ret = os.system(cmd)
                if ret == 0:
                    print(ColorString.confirm('Create symbol link file: %s' % minecraft_nginx_conf_file))

                nginx_process_number = int(os.popen('ps -ef | grep nginx | grep -v grep | wc -l').read().strip())
                cmd = None
                if nginx_process_number > 0:
                    cmd = 'sudo nginx -s reload'
                else:
                    cmd = 'sudo nginx'

                if cmd:
                    ret = os.system(cmd)
                    if ret == 0:
                        print(ColorString.confirm('minecraft nginx config successfully!'))
                    else:
                        print(ColorString.error('minecraft nginx config failed!'))
                # 配置HTTPS
                Nginx.setupSSL()
        except Exception as e:
            print(e)
            print(ColorString.error('Config Nginx for Minecraft Failed!!!'))
            exit(-1)

    @classmethod
    def setupSSL(cls):
        '''配置nginx服务支持https'''

        cmd = 'sudo apt-get update ||'\
        'sudo apt-get install -y software-properties-common &&'\
        'sudo add-apt-repository -y universe &&'\
        'sudo add-apt-repository -y ppa:certbot/certbot &&'\
        'sudo apt-get update ||'\
        'sudo apt-get install -y certbot python3-certbot-nginx &&'\
        'sudo certbot --nginx'
        if os.system(cmd) == 0:
            print(ColorString.confirm('Config HTTPS successfully!'))
        else:
            print(ColorString.error("Config HTTPS failed!"))

    
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
        php_fpm_bin_path = os.popen("whereis php-fpm | cut -d ' ' -f 2").read().strip()
        if not os.path.exists(php_fpm_bin_path):
            print(ColorString.error('You have not install php environment!!!'))
            return None
        php_fpm_version = os.path.basename(php_fpm_bin_path).replace('php-fpm','')
        fastcgi_pass = f'unix:/run/php/php{php_fpm_version}-fpm.sock'
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

    @classmethod
    def web_live_blue_map_conf(cls):
        '''配置minecraft 3D高清地图'''
        port=80
        server_domain = 'world.jokerhub.cn'
        return f"""
server {{
    listen {port};
    server_name {server_domain};
    location / {{
        proxy_pass      http://localhost:8100;
    }}
}}
"""
