##  WSL 详解

WSL与WSL2在多开的情况下，IP地址都是一样的，因此不适用制作集群的情况，适合玩单个服务的情况

### 一、安装WSL2 

#### 1.1 安装WSL2环境要求

对于 x64 系统：**版本 1903**或更高版本，**版本 18362 或**更高版本

#### 1.2  启用虚拟机功能

安装WSL2，需要启用虚拟机功能，需要在PowerShell中运行以下命令，执行完成后重启

```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

#### 1.3 安装Linux内核更新包

[用于 x64 计算机的 WSL2 Linux 内核更新包 (windows.net)](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)

#### 1.4 切换版本

```
wsl --set-default-version 2
```



### 二、WSL2

#### 2.1 WSL与WSL2比较

| 特征                                   | WSL1 | WSL2 |
| -------------------------------------- | ---- | ---- |
| Windows和Linux之间的集成               | ✓    | ✓    |
| 快速启动时间                           | ✓    | ✓    |
| 小资源足迹                             | ✓    | ✓    |
| 与当前版本的VMware和VirtualBox一起运行 | ✓    | ✓    |
| 托管虚拟机                             | ✕    | ✓    |
| 完整的Linux内核                        | ✕    | ✓    |
| 全面的系统调用兼容性                   | ✕    | ✓    |
| 跨OS文件系统的性能                     | ✓    | ✕    |

#### 2.2 WSL2 新特性

* WSL 2使用了VM，但效率上与WSL一样快

* 完整的Linux内核

* 提高文件IO性能

  如git clone，npm install，apt更新，apt升级等，在WSL这些操作非常的慢。

* 对Docker应用支持更好

* WSL与WSL2可以并在

  通过以下命令可以切换版本

  ```
  wsl --set-default-version 2
  ```

* WSL 2 的行为将更像虚拟机，例如：WSL 2 的 IP 地址与主机不同

#### 2.3 切换WSL2

如果在使用过程，原来在WSL1下安装系统，需要切换到WSL下，可以通过以下命令进行切换

```
PS C:\Users\yiuked> wsl --set-version centos7 2
正在进行转换，这可能需要几分钟时间...
有关与 WSL 2 的主要区别的信息，请访问 https://aka.ms/wsl2
转换完成。
PS C:\Users\yiuked> wsl --list -v
  NAME        STATE           VERSION
* ubuntu16    Stopped         1
  centos7     Stopped         2
  xb24        Stopped         1
```

#### 2.4 常用命令

* 快速进入某个系统

  ```
  wsl -d centos7
  ```


* 重启时reboot时出现Failed to talk to init daemon

  ```
  reboot -f
  ```

  

### 三、安装Liunx

在Mircrosoft Store中搜索Linux安装则可。

###  四、Windows Terminal 终端工具

在Mircrosoft Store中搜索Windows Terminal安装则可。如果需要添加右键菜单中，复制以下命令，另存.reg文件，修改your_name后运行则可：

```
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\Background\shell\wt]
@="Windows terminal here"

[HKEY_CLASSES_ROOT\Directory\Background\shell\wt\command]
@="C:\\Users\\your_name\\AppData\\Local\\Microsoft\\WindowsApps\\wt.exe -d ."

```


- 查看wsl目录 

`可以通过cmd命令 \\wsl$ 来打开wsl的物理路径`