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

# Visual Studio Code + JAVA + Maven 开发环境搭建

1. `JDK`安装: `brew cask install oracle-jdk`

2. Apache-Maven安装：`$ brew install maven`

3. [编辑器`(Visual Studio Code)`安装](https://code.visualstudio.com)

4. `Visual Studio Code`插件安装: 
    - Maven for Java
    - Debugger for Java
    - Java Test Runner
    - Language Support for Java(TM)

5. 创建Maven项目工程：`Command + Shift + P`，输入`Maven: Create Maven Project`, 选择基于`maven-archetype-quickstart`最新版本创建项目, `GroupId`一般使用域名反写，用来定义包名。`ArtifactId`为工程文件夹的名称

6. 修改`pom.xml`文件，给Maven项目工程添加`API依赖`，可以是`Bukkit API`，也可以是`PaperMC API`, 或其它API

## 使用`Kotlin`编码

`Visual Studio Code`安装Kotlin相关插件：

1. Kotlin Language
2. Code Runner