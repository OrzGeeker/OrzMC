# -*- coding: utf8 -*-
from ..utils.utils import platformType
from ..utils.ColorString import ColorString
import requests
import os
import progressbar

def install_jdk():
    Oracle.install_jdk()

def uninstall_jdk():
    Oracle.execute_uninstall_jdk()

class Oracle:

    ''' 
    # Example Download Link
    ## Windows： 
    - https://download.oracle.com/otn-pub/java/jdk/12.0.2+10/e482c34c86bd4bf8b56c0b35558996b9/jdk-12.0.2_windows-x64_bin.exe

    ## MacOS:
    - https://download.oracle.com/otn-pub/java/jdk/12.0.2+10/e482c34c86bd4bf8b56c0b35558996b9/jdk-12.0.2_osx-x64_bin.dmg

    ## Ubuntu:
     https://download.oracle.com/otn-pub/java/jdk/12.0.2+10/e482c34c86bd4bf8b56c0b35558996b9/jdk-12.0.2_linux-x64_bin.deb
    '''

    VERSION_LATEST = ('12.0.2','10', 'e482c34c86bd4bf8b56c0b35558996b9')

    JDK_NAME = {
        'windows': 'windows-x64_bin.exe',
        'osx': 'osx-x64_bin.dmg',
        'linux': 'linux-x64_bin.deb'
    }

    @classmethod
    def install_jdk(cls, version = VERSION_LATEST):

        if not Oracle.check_jdk_installed():
            try:
                Oracle.download_jdk()  
                if not Oracle.execute_install_jdk():
                    print(ColorString.warn('Install JDK Failed!'))
                    exit(0)
                else:
                    input(ColorString.hint('Press Enter to continue...'))
            except Exception as e:
                print(e)
            finally:
                if Oracle.check_jdk_installed():
                    os.remove(Oracle.jdk_temp_filename())
        else:
            print('\n')

    @classmethod
    def check_jdk_installed(cls):
        return os.system('java -version') == 0

    @classmethod
    def download_jdk(cls):
        headers = {
            'user-agent': 'OrzMC'
        }

        cookies = {
            'oraclelicense': 'accept-securebackup-cookie'
        }
        requests.packages.urllib3.disable_warnings()
        response = requests.get(Oracle.jdk_url(), stream=True, verify=False, allow_redirects=True, cookies = cookies, headers = headers)
        total_length = int(response.headers.get('content-length'))
        widgets = [
            'Download JDK: ',
            progressbar.Percentage(),
            ' ',
            progressbar.Bar(marker='#', left='[', right=']'),
            ' ',
            progressbar.ETA(),
            ' ',
            progressbar.FileTransferSpeed()
        ]
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()
        count = 0
        with open(Oracle.jdk_temp_filename(), 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    count += len(chunk)
                pbar.update(count)
            pbar.finish()

    @classmethod
    def jdk_url(cls):
        (version, build, hash) = Oracle.VERSION_LATEST
        return 'https://download.oracle.com/otn-pub/java/jdk/%s+%s/%s/jdk-%s_%s' % (version, build, hash, version, Oracle.jdk_name())

    @classmethod
    def jdk_name(cls):
        return Oracle.JDK_NAME.get(platformType())

    @classmethod
    def jdk_temp_filename(cls):
        return 'jdk-' + Oracle.jdk_name()

    @classmethod
    def execute_install_jdk(cls):
        return Oracle.execute_commands(Oracle.commands().get(platformType()).get('install'))

    @classmethod
    def execute_uninstall_jdk(cls):
        return Oracle.execute_commands(Oracle.commands().get(platformType()).get('uninstall'))

    @classmethod
    def execute_commands(cls, cmds, hint = ColorString.hint('May be you should input the user password to continue')):
        print(hint)
        if isinstance(cmds, list):
            ret = True
            for cmd in cmds:
                cur_ret =(os.system(cmd) == 0)
                if not cur_ret:
                    print('cmd: %s failed' % cmd)
                    ret = False
                    break
            return ret
        else:
            return False

    @classmethod
    def commands(cls):
        return  {
            'windows': {
                'install': [
                    
                ],
                'uninstall': [

                ]
            },
            'osx': {
                'install': [
                    'open ' + Oracle.jdk_temp_filename(),
                ],
                'uninstall': [
                    'sudo rm -R /Library/Java/JavaVirtualMachines/jdk-%s.jdk' % Oracle.VERSION_LATEST[0],
                    'sudo pkgutil --forget com.oracle.jdk-%s' % Oracle.VERSION_LATEST[0]
                ]
            },
            'linux': {
                'install': [
                ],
                'uninstall': [

                ]
            }
        }

    # 断点续传原理
    # @classmethod
    # def download(url, file_path):
    #     # 第一次请求是为了得到文件总大小
    #     r1 = requests.get(url, stream=True, verify=False)
    #     total_size = int(r1.headers['Content-Length'])

    #     # 这重要了，先看看本地文件下载了多少
    #     if os.path.exists(file_path):
    #         temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
    #     else:
    #         temp_size = 0
    #     # 显示一下下载了多少   
    #     print(temp_size)
    #     print(total_size)
    #     # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
    #     headers = {'Range': 'bytes=%d-' % temp_size}  
    #     # 重新请求网址，加入新的请求头的
    #     r = requests.get(url, stream=True, verify=False, headers=headers)

    #     # 下面写入文件也要注意，看到"ab"了吗？
    #     # "ab"表示追加形式写入文件
    #     with open(file_path, "ab") as f:
    #         for chunk in r.iter_content(chunk_size=1024):
    #             if chunk:
    #                 temp_size += len(chunk)
    #                 f.write(chunk)
    #                 f.flush()

    #                 ###这是下载实现进度显示####
    #                 done = int(50 * temp_size / total_size)
    #                 sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
    #                 sys.stdout.flush()
    #     print()  # 避免上面\r 回车符
