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
