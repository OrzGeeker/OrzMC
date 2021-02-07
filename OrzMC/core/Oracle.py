# -*- coding: utf8 -*-
from ..utils.utils import platformType
from ..utils.ColorString import ColorString
import requests
import os
from tqdm import tqdm

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
        mb_chunk = 1024 * 1024
        mb_size = int(total_length / mb_chunk + 0.5)
        with open(Oracle.jdk_temp_filename(), 'wb') as f:
            desc = os.path.basename(Oracle.jdk_url())
            for chunk in tqdm(iterable=response.iter_content(mb_chunk),total=mb_size,unit='MB',desc=desc):
                f.write(chunk)

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