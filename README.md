![logo](images/server_member.jpg)

# [OrzMC](https://github.com/OrzGeeker/OrzMC)

一个具有在Ubuntu上部署`Minecraft`个人私服和启动`Minecraft`客户端功能的`Python`命令行工具

支持的Python版本: `>=2.7, <4`

支持的游戏版本: `>= 1.13` 正式版

支持的操作系统: `Windows`、`MacOS`及`Linux`,(需要自行配置JDK和Python运行环境)

支持`JDK 8`及以上版本，如果要启动Forge客户端，建议安装`JDK 8`，因为`Forge`类型的客户端目录不能运行最新版本的`JDK`

本工具已上传到`Python`包管理网站`PyPi`，可以使用`pip`进行搜索和安装。

如果你不习惯使用命令行运行客户端，你也可以使用另外一个第三方客户端软件`HMCL`，注意`HMCL`运行在`JDK 8`环境下，下载地址:

- <https://hmcl.huangyuhui.net>

- <https://github.com/huanghongxun/HMCL/releases>

## TODO

- [ ] 为私服游戏玩家创建微信公众号及群组，方便交流和形成社区
- [ ] 实现`RCON`协议用来远程控制`Minecraft`服务器，方便进行运维工作
- [ ] 优化项目代码结构，提高可读性和可维护性
- [ ] 工具添加自动安装JDK功能，为用户省去不必要的麻烦
- [ ] 为项目添加单元测试，保证工具的质量
- [ ] 使用`BMCLAPI`镜像服务，加速客户端文件及资源的下载速度，缩短玩家安装客户端的耗时
- [ ] 使用玩家在游戏中的各种沙雕截图制作表情包并发布，加强社区文化建设
- [ ] 尝试使用`Kivy`来做一个GUI版本的启动器

## Done

- [x] 添加了`PaperMC`服务器部署能力
- [x] 添加了`Spigot`服务器部署能力
- [x] 为项目添加了主页，方便浏览项目概况
- [x] 支持在`MacOS`上运行`Forge`客户端
- [x] 添加服务器手动备份世界地图能力
- [x] 添加客户端安装`Optifine`开启光影渲染的能力

## 视频介绍

- [Mac登录指北](https://www.bilibili.com/video/av66156010/)

## 文档

- [OrzMC工具使用说明书](https://github.com/OrzGeeker/OrzMC/wiki/OrzMC%E5%B7%A5%E5%85%B7%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E%E4%B9%A6)

- [Minecraft相关资源](https://github.com/OrzGeeker/OrzMC/wiki/Minecraft%E7%9B%B8%E5%85%B3%E8%B5%84%E6%BA%90)

- [服务器运营及相关配置指南](https://github.com/OrzGeeker/OrzMC/wiki/%E6%9C%8D%E5%8A%A1%E5%99%A8%E8%BF%90%E8%90%A5%E5%8F%8A%E9%85%8D%E7%BD%AE)

- [服务器版本升级指南](https://github.com/OrzGeeker/OrzMC/wiki/%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%89%88%E6%9C%AC%E5%8D%87%E7%BA%A7)

- [个人私服概况](https://github.com/OrzGeeker/OrzMC/wiki/%E4%B8%AA%E4%BA%BA%E7%A7%81%E6%9C%8D%E6%A6%82%E5%86%B5)

- [PaperMC个人私服插件列表及相关说明](https://github.com/OrzGeeker/OrzMC/wiki/Paper-Bukkit%E5%BC%80%E6%9C%8D%E6%8F%92%E4%BB%B6)

- [客户端开启光影渲染的方法](https://github.com/OrzGeeker/OrzMC/wiki/客户端开光影)

- [启动器制作方法](https://github.com/OrzGeeker/OrzMC/wiki/启动器制作)

- [基岩版本服务器部署](https://github.com/OrzGeeker/OrzMC/wiki/基岩版服务器部署)

- [Python 开发相关库](https://github.com/OrzGeeker/OrzMC/wiki/Python-Dev)

## 社区

![Minecraft Group](/images/minecraft_group.png)

**😎欢迎加入我们😎**