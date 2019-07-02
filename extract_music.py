# -*- coding: utf-8 -*-
#!/usr/bin/env python

import getopt
import sys
import os
import json


def extract():
    try:

        opts, _ = getopt.getopt(sys.argv[1:], "g:e:", ["game_dir=", "extract_dir="])

        game_dir = None
        extract_dir = None
        for o, a in opts:
            if o in ["-g", "--game_dir"]:
                game_dir = a

            if o in ["-e", "--extract_dir"]:
                extract_dir = a

        if game_dir == None or extract_dir == None or not os.path.isdir(game_dir):
            print("You should provide both the game_dir path and extract_dir path!!!")
            exit(-1)

        if not os.path.isdir(extract_dir):
            os.makedirs(extract_dir)
        
        indexes_dir = os.path.join(game_dir, 'assets', 'indexes')
        objects_dir = os.path.join(game_dir, 'assets', 'objects')
        assets_json_file_path = None
        for dirpath, _, filenames in os.walk(indexes_dir):
            for filename in filenames:
                _, type = os.path.splitext(filename)
                if type == '.json':
                    assets_json_file_path = os.path.join(dirpath, filename)
                    break
        if os.path.exists(assets_json_file_path):
            with open(assets_json_file_path, 'r') as f:
                objects = json.load(f).get('objects')
                for key in objects:
                        filename, type = os.path.splitext(key)
                        if type == '.ogg':
                            filename = '_'.join(filename.split('/')[2::])
                            hash = objects[key].get('hash')
                            source_object_path = os.path.join(objects_dir,hash[0:2],hash)
                            dst_object_path = os.path.join(extract_dir,filename + '.wav')
                            cmd = 'ffmpeg -i ' + source_object_path + ' ' + dst_object_path
                            os.system(cmd)
                            print(filename + u'.wav extracted!')

                        


    except getopt.GetoptError, error:
        print(error)
        exit(-1)


if __name__ == '__main__':
    extract()