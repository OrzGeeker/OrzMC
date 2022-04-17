# [OrzMC](https://github.com/OrzGeeker/OrzMC)

一个终端命令行工具，使用Python 3+编写，它可以运行在`Ubuntu/MacOS`系统上（系统需要配置有`JAVA`和`Python3`运行环境），功能包括:

1. 部署`Minecraft`私人服务器(Vanilla/Paper/spigot/forge)
2. 启动`Minecraft`客户端功能（Vanilla)
3. 支持的`1.13`以上正式版

本工具已上传到`Python`包管理网站`PyPi`，可以使用`pip`进行搜索和安装。目前Python的官方源挂了，详情可了解: https://status.python.org
目前正在搭建python私有源

```python
$ python3 -m pip install pip_search && python3 -m pip install orzmc
$ orzmc -h # 查看使用帮助
```

如果你不习惯使用命令行运行客户端，你也可以使用第三方客户端软件`HMCL`

- [`HMCL`下载地址](https://github.com/huanghongxun/HMCL/releases)

## 项目待办

- [ ] 工具添加自动安装JDK功能，为用户省去不必要的麻烦
- [ ] 地图备份增量化自动化
- [ ] 为项目添加单元测试，保证工具的质量
- [ ] 实现`RCON`协议用来远程控制`Minecraft`服务器，方便进行运维工作
- [ ] 使用玩家在游戏中的各种沙雕截图制作表情包并发布，加强社区文化建设
- [ ] 自动备份地图并同步到私人NAS存储
- [ ] 尝试使用`Kivy`来做一个GUI版本的启动器
- [ ] 多线程下载，解决顺序同步下载文件的速度问题
- [ ] 优化命令工具的帮助文档，并配套使用示例

## 已完成功能

- [x] 添加Fabric装载器支持, 仅客户端
- [x] 使用`BMCLAPI`镜像服务(目前BMCLAPI存在资金问题，服务不稳定)，加速客户端文件及资源的下载速度，缩短玩家安装客户端的耗时
- [x] 服务器数据迁移功能
- [x] 提取指定版本游戏的BGM
- [x] 添加了`PaperMC`服务器部署能力
- [x] 添加了`Spigot`服务器部署能力
- [x] 为项目添加了[主页](https://minecraft.jokerhub.cn)
- [x] 支持在`MacOS`上运行`Forge`客户端
- [x] 添加服务器手动备份世界地图能力
- [x] 添加客户端安装`Optifine`开启光影渲染的能力
- [x] 为私服游戏玩家创建QQ群组，方便交流和形成社区
- [x] 支持基岩版客户端连接JAVA服务端 
- [x] 已支持服务端迁移部署，待写教程
- [x] QQ群(1056934080)已添加玩家上下线提示消息


# 私服 **[主页](https://minecraft.jokerhub.cn)**

![logo](images/server_member.jpg)

## 视频介绍

1. [启动器安装与服务器登录](https://www.bilibili.com/video/BV1nK4y1f7Yh/)
2. [客户端开启光影效果](https://www.bilibili.com/video/BV1sz4y1k7Hm/)
3. [命令、材质包导入及更换皮肤](https://www.bilibili.com/video/BV18A411x7EH)

## 相关文档

- [项目Wiki文档](https://github.com/OrzGeeker/OrzMC/wiki/%E4%B8%BB%E9%A1%B5)

## QQ玩家群

![Minecraft Group](images/minecraft_qq_group.jpg)

## 开发者

如果你有兴趣和我一起开发这个Python项目，拉项目到本地, 并配置开发环境，运行下面命令即可！🤒

```bash
$ git clone --recurse-submodules https://github.com/OrzGeeker/OrzMC.git && cd OrzMC && ./config_orzmc_dev && pipenv shell
```
