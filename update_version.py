# !/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import codecs

MAX = 1000
def update_version():
    updated_content = None
    new_version = None
    with codecs.open('setup.py', 'r', encoding='utf-8') as cfg:
        content = cfg.read()
        version_pattern = r'version\s*=\s*\"(\d+\.\d+\.\d+)\"'
        ret = re.search(version_pattern, content)
        if None != ret:
            old_version = ret.group(1)
            new_version = old_version.split('.')
            count = len(new_version)

            isValidVer = True and count > 0
            for num in new_version:
                if int(num) >= MAX:
                    isValidVer = False
                    break

            if  not isValidVer:
                print("The Version Number is not valid!!!")
                exit(-1)
            
            isReachMaxVer = True
            for num in new_version:
                if int(num) != MAX - 1:
                    isReachMaxVer = False
            if isReachMaxVer:
                print("The Version has reach the max version number!!!")
                exit(-1)

            lastIndex = count - 1
            index = lastIndex
            increase_index = lastIndex
            advance = 0
            while index >= 0:
                addition = int(new_version[index]) + advance + ( 1 if index == increase_index else 0)
                number = addition % MAX
                advance = addition / MAX
                new_version[index] = str(number)
                index = index - 1
            
            new_version = '.'.join(new_version)
            updated_content = content.replace(content[ret.start(1):ret.end(1)], new_version)
    
    if None != updated_content:
        with codecs.open('setup.py', 'w', encoding='utf-8') as cfg:
            cfg.write(updated_content)

        with codecs.open(os.path.join('OrzMC','app', 'Version.py'), 'w', encoding='utf-8') as version:
            version.write('ORZMC_VERSION_NUMBER=%s' % new_version)

if __name__ == '__main__':
    update_version()