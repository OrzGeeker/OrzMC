---
title: "Papermc"
date: 2019-12-10T13:06:35+08:00
draft: true
---

[PaperMC官网](https://papermc.io)

[Bukkit插件开发](https://bukkit.gamepedia.com/Setting_Up_Your_Workspace)

开发IDE目前还是建议使用**IntelliJ IDEA*&*: https://www.jianshu.com/p/2cbeb20409da


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

7. 



## 使用`Kotlin`编码

`Visual Studio Code`安装Kotlin相关插件：

1. Kotlin Language
2. Code Runner