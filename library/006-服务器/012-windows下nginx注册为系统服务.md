首先下一个软件用来帮助我们注册为系统服务
https://github.com/kohsuke/winsw/

建立名为`nginxd.xml`文件，并添加内容
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<service>
	<id>nginx</id>[标识名，net start nginx 就以为名为准]
	<name>nginx</name>[服务名]
	<description>nginx</description>[描述]
	<executable>D:\nginx-1.11.4\nginx.exe</executable>[文件执行路径]
	<logpath>D:\nginx-1.11.4\</logpath>[日志文件路径]
	<logmode>roll</logmode>[日志模块]
	<depend></depend>
	<startargument></startargument>[启动参数]
	<stopargument>-s stop</stopargument>[关闭参数]
</service>
```
[]中的内容为备注内容，请自行删除.  
配置配置完后，将下载的`winsw-xx.exe`改名为`nginxd.exe`【与`xml`同名】  
然后执行  
```
nginxd.exe install 安装服务
nginxd.exe uninstall 删除服务
```
安装完后则可使用
```
net start nginx
```
如果启动错误，请查看 `logpath`下的`xxx.err.log`文件
