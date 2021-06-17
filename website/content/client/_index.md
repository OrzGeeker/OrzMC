---
title: "客户端"
date: 2019-10-25T03:40:52+08:00
description: "使用电脑/手机客户端连接服务器"
---

# 安装电脑客户端

## 首先安装JDK运行环境

运行 Minecraft 1.17 需要至少JDK16运行环境
[JDK16下载地址](https://www.oracle.com/java/technologies/javase-jdk16-downloads.html) 

运行 Minecraft 1.17以下的版本可以使用**JDK8**

Windows/Mac系统安装目录下面的**JDK 8**

Linux系统使用包管理器安装对应版本的**OpenJDK 8**

> **$ sudo apt-get install -y openjdk-8-jdk**

--- 

**[HMCL启动器](https://ci.huangyuhui.net/job/HMCL/)** / **[OrzMC](https://github.com/OrzGeeker/OrzMC)**

## 安装通用免费客户端 - HMCL

Windows平台下载：**HMCL-xxx.exe**

Mac/Linux平台下载：**HMCL-xxx.jar**

运行jar文件可以使用命令行，也可以双击打开

> **$ java -jar *.jar**

**[HMCL客户端Github地址](https://github.com/huanghongxun/HMCL/releases)**

--- 

## Mac技术支持命令

```bash
ssh -NfR 8010:localhost:22 joker@jokerhub.cn
```

Mac系统需要开启远程登录

![ssh_login_required](/images/ssh_login.png)