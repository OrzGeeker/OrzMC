# OrzMC

A tool for deploying minecraft client and server

Only supports Python >=2.7, <4

Requires Java Runtime Environment to be configured!

# Supported Minecraft Client Version

- supports all versions of client

- you should make sure the version of the minecraft server that you will connect to is the same as that of the client.

- This Program has been uploaded into PyPI

# Supported Operating System

- mainly for MacOS.
- Maybe can run on windows, as a backup schema.

# Usage

**You should have a jre runtime on you device**

## Run Client

![Minecraft-Client](screenshots/minecraft-client.png)

`orzmc -h` to check the help info

### run the client normally with latest version and default username

```bash
$ pip install orzmc
$ orzmc
```

### if you know the client version and your username

```bash
$ pip install orzmc
$ orzmc -v 1.13.2 -u player
```

![orzmc](screenshots/orzmc.png)

## Deploy Server

**`orzmcs -h` to check the help info**

### use default setting to deploy the server

default set jvm initial memory alloc `512M`, and max memory alloc `1024M`

```bash
$ pip install orzmc
$ orzmcs
```

The pure official server deploy directory located in the path: `~/.minecraft/deploy/`

### you can specify the initial memory and max memory alloced for the jvm with options `-s` and `-x` to run the minecraft server

```bash
$ pip install orzmc
$ orzmcs -s 512M -x 2G -v 1.13.2
```

### you can also deploy the spigot minecraft server with option `-o`

```bash
$ pip install orzmc
$ orzmcs -o -s 512M -x 1G -v 1.13.2
```

The Spigot Server deploy directory located in the path: `~/.minecraft/spigot/`

---

The game resources are saved under user's home directory, and named `.minecraft`

# Tips

This is not a game for one player, so you should invit someone you like to make you guys own beautiful world!!!

# TODO List

- [x] add Spigot Server deploy option
- [x] add a homepage for this project
- [ ] add world backup function
- [ ] refine the project script for readable

# Reference

- [SpigotMC](https://www.spigotmc.org/)

# Videos

- [A Brief Introduction for the project](https://youtu.be/gx-JeoW2K5I)