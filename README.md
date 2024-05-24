# [OrzMC](https://github.com/OrzGeeker/OrzMC)

一个专门对Minecraft进行Geek的工程项目。

- [主页](https://minecraft.jokerhub.cn)
- [Wiki](https://github.com/OrzGeeker/OrzMC/wiki/%E4%B8%BB%E9%A1%B5)


![logo](images/server_member.jpg)

## 目录结构

```bash
.
├── OrzMC                  # OrzMC CLI Python源码
├── OrzMCTest              # OrzMC CLI Python单元测试
├── images                 # README.md 引用的图片资源
├── paper_plugins_config   # Git子模块：主要是papermc开服插件的配置文件
├── plugin                 # Git子模块：自研PaperMC插件OrzMC
├── scripts                # Minecraft 服务器运维的一些工具脚本
├── skins                  # Minecraft 玩家皮肤
├── swift                  # Git子模块：Swift语言开发相关库以及一个macOS/iOS应用程序
├── webmc                  # Git子模块：主要探索使用Web浏览器连接服务器玩耍的可能性
├── website                # Minecraft 个人运营的网站，用来交流学习开服运营
└── wiki                   # 早期手动开服及维护时累的一些运维文档
```

## 命令行工具

使用 Python3 编写，可以运行在`Ubuntu/MacOS`系统上（系统需要配置有`JAVA`和`Python3`运行环境），功能包括:

1. 部署`Minecraft`私人服务器(Vanilla/Paper/spigot/forge)
2. 启动`Minecraft`客户端功能（Vanilla)
3. 支持的`1.13`以上正式版

工具已上传到`Python`包管理网站`[PyPi][orzmc-pypi]`，可以使用`pip`进行安装

```python
$ pip install orzmc
$ orzmc -h # 查看使用帮助
```

如果你有兴趣和我一起开发这个Python项目，拉项目到本地, 并配置开发环境，运行下面命令即可配置好开发环境：🤒

```bash
$ git clone --recurse-submodules \
      https://github.com/OrzGeeker/OrzMC.git && \
      cd OrzMC && ./config_orzmc_dev && pipenv shell
```

## 项目待办

- [ ] 自动安装JRE运行环境
- [ ] 并发下载提高文件下载速度

---

[orzmc-pypi]: <https://pypi.org/project/OrzMC/>