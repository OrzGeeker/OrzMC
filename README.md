# [OrzMC](https://github.com/OrzGeeker/OrzMC)

一个专门对Minecraft进行Geek的工程项目。

![logo](images/server_member.jpg)

包含多个子模块：
- 命令行工具
- MacOS平台启动器
- [HomePage](https://minecraft.jokerhub.cn)

## Python 命令行工具

一个终端命令行工具，使用Python 3+编写，它可以运行在`Ubuntu/MacOS`系统上（系统需要配置有`JAVA`和`Python3`运行环境），功能包括:

1. 部署`Minecraft`私人服务器(Vanilla/Paper/spigot/forge)
2. 启动`Minecraft`客户端功能（Vanilla)
3. 支持的`1.13`以上正式版

本工具已上传到`Python`包管理网站`PyPi`，可以使用`pip`进行搜索和安装

```python
$ pip install orzmc
$ orzmc -h # 查看使用帮助
```

如果你有兴趣和我一起开发这个Python项目，拉项目到本地, 并配置开发环境，运行下面命令即可！🤒

```bash
$ git clone --recurse-submodules \
      https://github.com/OrzGeeker/OrzMC.git && \
      cd OrzMC && ./config_orzmc_dev && pipenv shell
```

## 项目待办

- [ ] 工具添加自动安装JDK功能，为用户省去不必要的麻烦
- [ ] 多线程下载，解决顺序同步下载文件的速度问题

## 视频介绍

1. [启动器安装与服务器登录](https://www.bilibili.com/video/BV1nK4y1f7Yh/)
2. [客户端开启光影效果](https://www.bilibili.com/video/BV1sz4y1k7Hm/)
3. [命令、材质包导入及更换皮肤](https://www.bilibili.com/video/BV18A411x7EH)

## 相关文档

- [项目Wiki文档](https://github.com/OrzGeeker/OrzMC/wiki/%E4%B8%BB%E9%A1%B5)