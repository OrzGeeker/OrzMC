# OrzMC

A tool for deploying minecraft client and server

Only supports Python >=2.7, <4

Requires JDK 1.8 to be configured, not higher than this version, becuase forge cannot run on higher jdk versions such as 1.12!

# Introduction Video on YouTube(Need VPN in China)

- [A Brief Introduction for the project](https://youtu.be/gx-JeoW2K5I)

# Supported Minecraft Client Version

- supports versions of client `>= 1.13`

- you should make sure the version of the minecraft server that you will connect to is the same as that of the client.

- This Program has been uploaded into PyPI

# Supported Operating System

- mainly for MacOS.
- Maybe can run on windows, as a backup schema, not yet test on windows platform.

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
                Specified the type of game: "pure"/"spigot"/"forge" for server, "pure/forge" for client, default 'pure'

            -m, --mem_min
                Specified the JVM initial memory allocation

            -x, --mem_max
                Specified the JVM max memory allocation

            -V, --Verbose
                Output some debug info for bugfix

            -h, --help 
                show the command usage info
```

## Run Client

### run the pure client normally with latest version and default username

```bash
$ pip install orzmc
$ orzmc
```
![orzmc](screenshots/orzmc.png)

![Minecraft-Client](screenshots/minecraft-client.png)

### if you know the client version and your username

```bash
$ pip install orzmc
$ orzmc -v 1.13.2 -u player_name
```

### you can also runt the forge client

```bash
$ pip install orzmc
$ orzmc -t forge
```

![orzmc](screenshots/orzmc-forge.png)

![Minecraft-Forge-Client](screenshots/minecraft-forge-client.png)

## Deploy Server

### use default setting to deploy the pure server

default set jvm initial memory alloc `128M`, and max memory alloc `2G`

```bash
$ pip install orzmc
$ orzmc -s
```

### you can specify the initial memory and max memory alloced for the jvm with options `-s` and `-x` to run the minecraft server

```bash
$ pip install orzmc
$ orzmc -s -m 512M -x 2G -v 1.13.2
```

### you can also deploy the spigot/forge minecraft server with option `-t`

#### Spigot Server

```bash
$ pip install orzmc
$ orzmc -s -t spigot -m 512M -x 1G -v 1.13.2
```

#### Forge Server

```bash
$ pip install orzmc
$ orzmc -s -t forge -m 512M -x 1G -v 1.13.2
```

由于Forge包是用JDK 8编译的，所以建安装的JDK环境为JDK8系统，不要太高，目前不兼容，会出现无法部署Forge服务器的情况。

---

The game resources are saved under user's home directory, and named `.minecraft`

# Tips

This is not a game for one player, so you should invit someone you like to make you guys own beautiful world!!!

# TODO List

- [x] add Spigot Server deploy option
- [x] add a homepage for this project
- [x] support forge client and server on MacOS, Yep!!!🤪 
- [ ] add world backup function
- [ ] refine the project script for readable
- [ ] automation the process of installing JDK/JRE Runtime
- [ ] add some unit test case to guarantee quality
- [ ] create a Docker Mojang Mirror Server for personal CDN 

# Reference

- [SpigotMC](https://www.spigotmc.org/)
- [Minecraft Forge](https://files.minecraftforge.net)
- [Minecraft 中文资源站](http://www.minecraftxz.com)
- [Minecraft 中文百科](https://minecraft-zh.gamepedia.com/Minecraft_Wiki)
- [Minecraft 官方Wiki](https://minecraft.gamepedia.com/Minecraft_Wiki)
- [Minecraft 微软官方](https://www.minecraft.net/zh-hans/)
- [Minecraft 网易官方](http://mc.163.com)
