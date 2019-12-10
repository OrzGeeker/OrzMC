---
title: "Forge"
date: 2019-12-10T13:06:17+08:00
draft: false
---

[Forge仓库](https://github.com/OrzGeeker/MinecraftForge)




## Mod开发环境建立 - [参考文章](https://mcforge.readthedocs.io/en/latest/gettingstarted/)

1. 下载安装 [IntelliJ IDEA](https://www.jetbrains.com/idea/download)
2. 从[Forge官网](https://files.minecraftforge.net/)下载MDK文件，可能需要翻墙
3. 解压下载的MDK文件到一个空目录下
4. 使用**IntelliJ IDEA**打开**`build.gradle`**文件，并按工程导入。导入后会自动进行各种资源的下载，下载过程需要有VPN代理，因为文件有些在国外服务器上。VPN的话注意使用全局代理。
5. 完成后打开Gradle面板，运行 **genIntellijRuns**成功后，退出IntelliJ IDEA后重新打开。


