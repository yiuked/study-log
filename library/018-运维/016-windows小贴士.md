* 为文件或者目录建立软连接.
在 `D:\wwwroot\tools\` 目录下创建`D:\php\vendor`文件夹的软链接，名称保持为`vendor`
命令：
```
  mklink /D D:\wwwroot\tools\vendor D:\php\vendor
```
>Note：/D 不能少，不加表示创建文件的软链接而不是文件夹

* 定时关机批处理
```
@echo off
cd /d D:\laravel\vagrant\Homestead
vagrant halt
set /p time=倒数关机秒数:
Shutdown -s -t %time%
pause
exit
```

* 去掉桌面快捷键图标批处理
```
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons" /v 29 /d "%systemroot%\system32\imageres.dll,196" /t reg_sz /f
taskkill /f /im explorer.exe
attrib -s -r -h "%userprofile%\AppData\Local\iconcache.db"
del "%userprofile%\AppData\Local\iconcache.db" /f /q
start explorer
```

* vagrant开机批处理
```
@echo off
cd /d D:\laravel\vagrant\Homestead\
vagrant up
pause
exit
```

* vagrant关机批处理
```
@echo off
cd /d D:\laravel\vagrant\Homestead
vagrant halt
pause
exit
```

* Windows中，带空格的目录常常不太好在程序中执行，需要对目录进行转化，比如加分号、转成URL编码、转义等。  
使用`dir /x`命令，查看目录的缩写，然后将缩写带入程序中执行更为方便:
 ```
2017/01/23  18:04    <DIR>          WINDOW~3     Windows Defender
2016/07/21  18:07    <DIR>          WI3CF2~1     Windows Kits
2016/06/27  12:57    <DIR>          WINDOW~1     Windows Mail
2019/03/14  09:05    <DIR>          WI54FB~1     Windows Media Player
2009/07/14  13:32    <DIR>          WINDOW~2     Windows NT
2016/06/27  12:57    <DIR>          WINDOW~4     Windows Photo Viewer
2016/06/27  12:57    <DIR>          WIBFE5~1     Windows Portable Devices
2016/06/27  12:57    <DIR>          WI4223~1     Windows Sidebar
2016/06/08  09:54    <DIR>          WIRESH~1     Wireshark
2016/11/14  09:27    <DIR>          YIWANP~1     yiwanplayer
 ```

* Windows 下 TortoiseGit 不显示图标?

  https://www.cnblogs.com/zhaoqingqing/p/7253879.html