#!/usr/bin/env bash
#-*- coding: utf-8 -*-

# NapCatQQ: https://github.com/NapNeko/NapCatQQ
# NapCatQQ Doc: https://napneko.github.io/zh-CN/

script_file="napcat.sh"
if [ ! -f $script_file ]; then
    # 本地不存在安装脚本，下载它
    curl -o $script_file https://nclatest.znin.net/NapNeko/NapCat-Installer/main/script/install.sh
fi

if command -v xvfb-run >/dev/null 2>&1; then
    # 已安装命令，直接运行
    xvfb-run -a qq --no-sandbox
else
    # 未安装命令，执行安装脚本
    sudo bash napcat.sh --force
fi

# 输入 xvfb-run -a qq --no-sandbox 命令启动。
# 保持后台运行 请输入 screen -dmS napcat bash -c "xvfb-run -a qq --no-sandbox"
# 后台快速登录 请输入 screen -dmS napcat bash -c "xvfb-run -a qq --no-sandbox -q QQ号码"
# Napcat安装位置 /opt/QQ/resources/app/app_launcher/napcat
# WEBUI_TOKEN 请自行查看/opt/QQ/resources/app/app_launcher/napcat/config/webui.json文件获取
# 注意, 您可以随时使用 screen -r napcat 来进入后台进程并使用 ctrl + a + d 离开(离开不会关闭后台进程)。
# 停止后台运行 请输入 screen -S napcat -X quit
