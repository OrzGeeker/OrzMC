# -*- coding: utf8 -*-
from ..core.Oracle import Oracle
from ..utils.ColorString import ColorString
from ..utils.utils import *
from .Config import Config
import argparse
import re
import os

def install_jdk():
    Oracle.install_jdk()

def uninstall_jdk():
    Oracle.execute_uninstall_jdk()

def rsync_server_core_data():
    '''服务器迁移时用来迁移服务器核心数据'''
    #命令行参数解析 argparse 使用文档：https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='use rsync command to sync the minecraft server core data to other location or host')

    # Tool
    parser.add_argument('-s', metavar='source', dest='source', help='Specified the source file or dir to sync')
    parser.add_argument('-d', metavar='destination', dest='destination', help='Specified the destination dir to sync')
    parser.add_argument('-y', '--yes', default=False, action='store_true', help='ask yes when require user select')
    args = parser.parse_args()
    
    source = args.source
    destination = args.destination

    ftp_server_base_dir_name = os.path.basename(Config.game_ftp_server_base_dir())
    server_core_data_dir_name = os.path.basename(Config.game_ftp_server_core_data_backup_dir())

    server_core_data_dir_path = os.path.join(os.path.expanduser('~'),"%s/%s" % (ftp_server_base_dir_name, server_core_data_dir_name))
    if not source and os.path.exists(server_core_data_dir_path):
        source = server_core_data_dir_path
        if os.path.isdir(server_core_data_dir_path):
            source += '/*' 

    def check_args(source, destination):
        if not destination or not source:
            print(ColorString.warn('You should provide both source and destination argument for this command, destination can be a (local dir/file) remote host (example: ubuntu@mc.jokerhub.cn)'))
            exit(-1)

    def execute_sync(source, destination, test = True):
        check_args(source, destination)

        pattern = re.compile(r'\w+@\w+')
        dest = destination.strip()
        source = source.strip()
        match = re.match(pattern, dest)
        if match:
            ftp_server_base_dir_name = os.path.basename(Config.game_ftp_server_base_dir())
            
            sync_file_dir_name = os.path.basename(source)
            if not os.path.exists(source):
                segments = list(os.path.split(source))[0:-1]
                sync_file_dir_name = os.path.basename(os.path.join(*segments))
                dest += ':~/%s/%s' % (ftp_server_base_dir_name,sync_file_dir_name)
            else:
                dest += ':~/%s/' % (ftp_server_base_dir_name)

        rsync_cmd = 'rsync -zarvh %s %s ' % (source, dest)
        rsync_cmd += "--exclude 'plugins/dynmap/*'"
        if test:
            rsync_cmd += ' -n'

        os.system(rsync_cmd)

        if test:
            print('\ncommand: %s' % ColorString.confirm(rsync_cmd))
            print(ColorString.hint("Run in Fake Mode!"))

    check_args(source = source, destination = destination)
    execute_sync(source = source, destination = destination, test = True)

    confirm = ['Y','y','Yes','yes']
    cancel = ['N','n','No','no']
    while True:
        a = hint(ColorString.confirm('\nAre you confirm want to execute this operation? [%s] ' % ('/'.join(confirm) + '|' + '/'.join(cancel))))
        if a in confirm:
            execute_sync(source=source, destination = destination, test = False)
            break
        elif a in cancel:
            break
        else:
            print(ColorString.warn('Your input is invalid, Please try again!'))

