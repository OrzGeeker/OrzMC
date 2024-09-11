#!/usr/bin/env bash
#-*- coding: utf-8 -*-

# NapCatQQ: https://github.com/NapNeko/NapCatQQ
# NapCatQQ Doc: https://napneko.github.io/zh-CN/

script_file="napcat.sh"
if [ ! -f $script_file ]; then
    # 本地不存在安装脚本，下载它
    curl -o $script_file https://nclatest.znin.net/NapNeko/NapCat-Installer/main/script/install.sh
if

if command -v xvfb-run >/dev/null 2>&1; then
    # 已安装命令，直接运行
    xvfb-run -a qq --no-sandbox
else
    # 未安装命令，执行安装脚本
    sudo bash napcat.sh
fi