# OrzMC

A tool for deploying minecraft client and server

Only supports Python >=2.7, <4

Requires JDK 1.8 to be configured, not higher than this version, becuase forge cannot run on higher jdk versions such as 1.12!

# Supported Minecraft Client Version

- supports versions of client `>= 1.13`

- you should make sure the version of the minecraft server that you will connect to is the same as that of the client.

- This Program has been uploaded into PyPI

# Supported Operating System

- mainly for MacOS.
- If your operating system is Linux or windows, there is another launcher which is beautiful and flexable: [HMCL](https://hmcl.huangyuhui.net), you can use it play this game.

# Usage

`orzmc -h` to check the help info

```bash
$ orzmc -h

   NAME

        orzmc -- A command line tool for start minecraft client or deploy minecraft server

    Usage

        orzmc [-v client_version_number] [-u username] [-h]

            -s, --server
                deploy minecraft server, if there is no this flag, this command line tool start minecraft as default
        
            -v, --version  
                Specified the Minecraft clinet version number to start

            -u, --username 
                pick an username for player when start the client

            -t, --game_type
                Specified the type of game: "pure"/"spigot"/"forge" for server, "pure/forge" for client

            -m, --mem_min
                Specified the JVM initial memory allocation

            -x, --mem_max
                Specified the JVM max memory allocation

            -V, --Verbose
                Output some debug info for bugfix

            -h, --help 
                show the command usage info

            -f, --forceUpgrade
                when deploy spigot server, the option can upgrade your map from old game version

            -b, --backup
                backup your minecraft world into ~/minecraft_world_backup directory as zip file!
```

## Run Client

### run the pure client normally with latest version and default username

```bash
$ pip install orzmc
$ orzmc
```

### if you know the client version and your username

```bash
$ pip install orzmc
$ orzmc -v 1.14.2 -u player_name
```

### you can also run the forge client

```bash
$ pip install orzmc
$ orzmc -t forge
```

## Deploy Server

### use default setting to deploy the pure server

default set jvm initial memory alloc `512M`, and max memory alloc `2G`

```bash
$ pip install orzmc
$ orzmc -s
```

### you can specify the initial memory and max memory alloced for the jvm with options `-s` and `-x` to run the minecraft server

```bash
$ pip install orzmc
$ orzmc -s -m 512M -x 2G -v 1.14.2
```

### you can also deploy the spigot/forge minecraft server with option `-t`

#### Spigot Server

you should installed `jre` and `git` tools before you run commands below.

```bash
$ pip install orzmc
$ orzmc -s -t spigot -m 512M -x 1G -v 1.14.2
```

#### Forge Server

```bash
$ pip install orzmc
$ orzmc -s -t forge -m 512M -x 1G -v 1.14.2
```

由于Forge包是用JDK 8编译的，所以建安装的JDK环境为JDK8系统，不要太高，目前不兼容，会出现无法部署Forge服务器的情况。

---

The game resources are saved under user's home directory, and named `.minecraft`

This is not a game for one player, so you should invit someone you like to make you guys own beautiful world!!!

# TODO List

- [ ] fire an weixin public account and group for uses get newest information and communicate with each other
- [ ] implement RCON Protocol for remote control Minecraft Server
- [ ] add world backup function
- [ ] refine the project script for readable
- [ ] automation the process of installing JDK/JRE Runtime
- [ ] add some unit test case to guarantee quality
- [ ] create a Docker Mojang Mirror Server for personal CDN 

# Done List

- [x] add Spigot Server deploy option
- [x] add a homepage for this project
- [x] support forge client and server on MacOS, Yep!!!🤪 
- [x] backup your world map files

# Reference

- [SpigotMC](https://www.spigotmc.org/)
- [Minecraft Forge](https://files.minecraftforge.net)
- [CurseForge](https://minecraft.curseforge.com)(最新版的相关资源下载的最好的地方)
- [Minecraft 中文资源站](http://www.minecraftxz.com)(老旧版的资源下载站，不需要翻墙)
- [Minecraft 中文百科](https://minecraft-zh.gamepedia.com/Minecraft_Wiki)
- [Minecraft 官方Wiki](https://minecraft.gamepedia.com/Minecraft_Wiki)
- [Minecraft 微软官方](https://www.minecraft.net/zh-hans/)
- [Minecraft 网易官方](http://mc.163.com)
- [Query协议](https://wiki.vg/Query)
- [RCON协议](https://wiki.vg/RCON)

# Tips 

- 制作资源包，压缩是要在assets同级目录选择所有文件，而不是在父目录下压缩, 先进入`assets`目录下面, 再执行指令`zip -r resourcepack.zip ./*`生成压缩文件, 可以导出作为资源包使用. 查看资源包的`SHA-1`值使用: `echo -e "SHA-1: " "$(shasum -b resourcepack.zip | cut -d ' ' -f 1)"`
- 使用query协议查询服务器状态需要用到UDP协议，所以在云服务器上部署需要允许这个协议访问对应的端口

# 关于Mac上玩时，无线网络总是断开重连的总题解决方案

这个可能是因为网络问题, minecraft的bug列表中可以搜索到这个问题: [MC-98598](https://bugs.mojang.com/browse/MC-98598),提供了解决方案: JVM启动参数中指定使用`IPv4`: `-Djava.net.preferIPv4Stack=true`

# 测试你的服务器可以支持几个玩家同时在线

安装服务器网速测试工具`speedtest-cli`, 并测速:

```bash
$ pip install speedtest-cli
$ speedtest-cli
```

将得到的上下行网速填入下面网址对应页面的区域时, 并将服务器的内存大小也填入, 开始计算即可

[测试网址](http://canihostaminecraftserver.com)

# Spigot服务器支持将低版本游戏的地图更新到新版本

只需要在启动命令中添加 `--forceUpgrade` 选项，启动一次服务器地图更新后，启动服务器就不需要添加这个选项了。

Spigot的地图文件有三个目录：

- `world` 对应纯净服的主世界地图目录: `world`
- `world_nether` 对应纯净服的下界地图： `world/DIM-1`
- `world_the_end` 对应纯净服的末路之地地图: `world/DIM1`

从纯净服迁移到Spigot服时，将对应文件夹复制到对应目录下，重启服务即可完成地图迁移。

# 为服务器添加自定义图标

在服务器启动根目录下面(也就是和`jar`文件同一级目录下面), 放置`64x64`大小的`png`图片, 然后重新启动服务器.
这时再连接服务器时, 就会把自定义的`64x64`的图片展示出来.

# 添加自定义音乐播放

mp3转ogg指令: `ffmpeg -i origin.mp3 -map 0:a:0 output.ogg`

资源包目录定义:
```bash
├── assets
│   └── minecraft
│       ├── sounds
│       │   └── music
│       │       └── joker
│       │           └── joker.ogg
│       ├── sounds.json
│       └── textures
│           └── entity
│               ├── alex.png
│               └── steve.png
├── pack.mcmeta
└── pack.png
```

只需要在`minecraft`目录下创建`sounds`目录,用来存放声音文件`ogg`格式, 并且要确保播放的声音通道是音频通道的第一个通道. 然后创建同目录级别的`sounds.json`文件, 用来定义声音文件和游戏中声音事件的对应关系.

```json
{
    "music.joker": {
        "sounds": [
          {
            "name": "music/joker/joker",
            "stream": true,
            "volume": 1
          }
        ]
      }
}
```

如上, 定义了一个游戏声音事件`music.joker`, 它使用声音文件: `music/joker/joker`, 在游戏内, 可以使用指令`/playsound` 进行播放, 如果和命令方法配合使用, 则可以有其它的好玩的用法. ;-D

# 添加了Spigot服务systemd服务脚本

```bash
scripts/systemd/
└── minecraft.service

0 directories, 1 file
```

部署时将`minecraft.service`文件放入`/etc/systemd/system/`目录下面, 运行命令:

```
$ sudo systemctl daemon-reload    // 加载服务脚本
$ sudo systemctl start minecraft  // 启动服务
$ sudo systemctl stop minecraft   // 停止服务
$ sudo systemctl reload minecraft // 重新加载游戏
```

# 添加离线登录功能，用来保护帐号

参考这篇说明：<https://github.com/games647/FastLogin>

`Spigot`服务器添加插件:
- [ProtocolLib](https://github.com/dmulloy2/ProtocolLib/releases)：这个插件是`FastLogin`依赖插件
- [FastLogin](https://github.com/games647/FastLogin/releases)：这个用来处理登录，需要配合其它专门处理登录的插件使用
- [LoginSecurity](https://github.com/lenis0012/LoginSecurity-2/releases)： 用来处理离线模式下的用户登录

## 管理员命令
使用`/lac`移除密码并重新载入游戏

## 用户命令
使用`/register <password>` 注册用户密码
使用`/changepass <old> <new>` 变更用户密码
使用`/login <password>` 命令可以登录
使用`/logout` 可以登出


# 升级服务器版本时需要迁移的文件

```
.
├── eula.txt            // eula协议同意文件
├── plugins             // 服务器安装的插件
├── server-icon.png     // 服务器自定义图标
├── server.properties   // 服务器配置属性
├── world               // Spigot服务器主世界地图
├── world_nether        // Spigot服务器下界地图
└── world_the_end       // Spigot服务器末路之地地图
```