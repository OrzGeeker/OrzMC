---
menu: 
  main:
    name: "客户端"
    weight: 2
toc: true
---

# 客户端启动器

游戏版本和Java版本的对应关系

---

|游戏版本|JAVA版本|
|:-------:|:----:|
|≧1.20.5| ≧21 |
|≧1.18  | ≧17 |
|≧1.17  | ≧16 |
|<1.17  | ≧8  |

---


## 自研 MacOS 平台启动器 - OrzMCApp

使用 Swift & SwiftUI 编写的MacOS平台启动器:
[代码仓库](https://github.com/OrzGeeker/OrzMCApp) -
[下载应用](https://github.com/OrzGeeker/OrzMCApp/releases/download/0.1.1/OrzMC_0.1.1_24_20250723_031710.zip)

![OrzMC_MacOS](/images/client/orzmc_macOS.png)

视频介绍👇

|     |     |
|:---:|:---:|
|||
|[![安装](/images/video_cover/orzmc_install.png)](https://www.bilibili.com/video/BV1b4HAeBERS)|[![使用](/images/video_cover/orzmc_usage.png)](https://www.bilibili.com/video/BV1hBtUeJE8y)|


---

## Python 命令行启动器 - OrzPythonMC

Mac/Linux系统可以使用：[代码仓库](https://github.com/OrzGeeker/OrzPythonMC) - [PyPI发布](https://pypi.org/project/OrzMC/)

![OrzMC_CLI_PY](/images/client/orzmc_cli_py.png)

安装方法:

```bash
# 安装应用到用户目录下
python3 -m pip install --user orzmc
# 添加用户二进制目录到环境变量
echo 'PATH=$PATH:'$(python3 -m site --user-base)/bin >> ~/.bashrc
# 使用添加的环境变量立即生效
source ~/.bashrc 
# 运行 orzmc 命令
orzmc
```

---

## 跨平台Java启动器 - HMCL

 [HMCL主页](https://hmcl.huangyuhui.net/) -
 [代码仓库](https://github.com/huanghongxun/HMCL) -
 [下载地址](https://ci.huangyuhui.net/job/HMCL/)

![HMCL_JAVA](/images/client/hmcl_java.png)

Windows安装运行：

```
下载 `*.exe` 文件，并鼠标双击运行
```

Unix/Linux/MacOS命令行运行：

```bash
# 下载 `*.jar`文件，并在命令行中使用`java -jar `命令运行
java -jar HMCL.jar 
```

HMCL 可以安装 Fraric 装载器，常用的 MOD 列表：

|名称|功能|
|:---|:---|
|[Reply MOD](https://www.replaymod.com/)|客户端视频录制|
