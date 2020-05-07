---
title: "Papermc"
date: 2019-12-10T13:06:35+08:00

draft: false
---

## 推荐使用的插件模板创建方式

- 项目模板搭建方式请参看：<https://minecraftdev.org/>
- 调试插件的方式请参看: <https://youtu.be/1B4JGzs0BCc>

---

## 服主个人Geek的方式

1. [Spigot插件开发](https://www.spigotmc.org/wiki/spigot-plugin-development/)

2. [Bukkit插件开发](https://bukkit.gamepedia.com/Setting_Up_Your_Workspace)

3. [PaperMC官网](https://papermc.io)

开发IDE建议使用**[IntelliJ IDEA](https://www.jetbrains.com/idea/)**

`Spigot插件开发`中有**IEAD**配置手动依赖和**Maven**项目管理两种方式

`Bukkit插件开发`中有开发插件的基础知识结构介绍

`PaperMC`中可以依赖针对`papermc`的服务端API

获取**Bukkit**、**CraftBukkit**、**Spigot**、**Spigot-API**，使用[BuildTools.jar](https://www.spigotmc.org/wiki/buildtools/)

**开发模板: https://github.com/OrzGeeker/OrzMCDev**


## 名词解释

- Paper-API: 一种增强版本的 `Bukkit API`
- Paper-Server: 一种支持`Paper-API`的`Minecraft`服务端，专注于性能提升

## Kotlin开发环境配置

```base
$ curl -s https://get.sdkman.io | bash
$ source "~/.sdkman/bin/sdkman-init.sh"
$ sdk install kotlin
$ sdk list kotlin
$ sdk use kotlin 1.3.72
$ 
```

