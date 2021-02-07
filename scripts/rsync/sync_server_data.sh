#!/usr/bin/env bash
#-*- utf-8 -*-

MC_DIR=~/minecraft_world_backup/
SOURCE_DIR="${MC_DIR}/mcserver/"
DEST_DIR="ubuntu@mc.jokerhub.cn:~/$(basename ${MC_DIR})/$(basename ${SOURCE_DIR}))"

echo $SOURCE_DIR 
echo $DEST_DIR
rsync -zarv \
    $SOURCE_DIR \
    ubuntu@mc.jokerhub.cn:~/ \
    --exclude 'plugins/dynmap/*' \
    -n