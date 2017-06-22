### 安装Ruby
http://www.rubyinstaller.org/，去这里下载，然后安装。

### 安装Sass
安装好Ruby后，打开CMD命令，输入：
```
$ gem sources --remove https://rubygems.org/
$ gem sources -a https://ruby.taobao.org/
$ gem sources -l
*** CURRENT SOURCES ***
https://ruby.taobao.org
# 请确保只有 ruby.taobao.org
$ gem install sass
```

### 配置PHPStorm
打开Webstorm的设置界面，然后搜索File Watcher；
点击File Watchers界面的增加按钮；

在配置界面，除以下两项，其它都保持默认则可:
```
Watched Files:
  File type : Sass
Watcher Settings:
  Program:C:\Ruby24-x64\bin\sass.bat
  Arguments:--no-cache --update $FileName$:c2c/$FileNameWithoutExtension$.css
  // $Arguments:--no-cache --update 原sass文件:需要生成的css目标文件(可带路径)
```
