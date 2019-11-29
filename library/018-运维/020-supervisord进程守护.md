## supervisord 进程守护
### 安装
```
yum install supervisor
```

### 配置
/etc/supervisord.conf
```
[program:xx]
command=php /root/task.php  ; 程序启动命令
autostart=true       ; 在supervisord启动的时候也自动启动
startsecs=10         ; 启动10秒后没有异常退出，就表示进程正常启动了，默认为1秒
autorestart=true     ; 程序退出后自动重启,可选值：[unexpected,true,false]，默认为unexpected，表示进程意外杀死后才重启
startretries=3       ; 启动失败自动重试次数，默认是3
user=root          ; 用哪个用户启动进程，默认是root
priority=999         ; 进程启动优先级，默认999，值小的优先启动
redirect_stderr=true ; 把stderr重定向到stdout，默认false
stdout_logfile_maxbytes=20MB  ; stdout 日志文件大小，默认50MB
stdout_logfile_backups = 20   ; stdout 日志文件备份数，默认是10
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile=/opt/apache-tomcat-8.0.35/logs/catalina.out
stopasgroup=false     ;默认为false,进程被杀死时，是否向这个进程组发送stop信号，包括子进程
killasgroup=false     ;默认为false，向进程组发送kill信号，包括子进程
```
> 请不要写 `/usr/bin/php /root/task.php` 这样会导致PHP引用文件路径错误
### 加入开机启动
```
chkconfig supervisord on
```

### 错误
```
error: <class 'socket.error'>, [Errno 2] No such file or directory: file: <string> line: 1
```
解决办法：   
这个可能有多种原因，可能是已经启动过了也可能是没权限，解决步骤如下：   
1. 先要确认是否已经启动过了：`ps aux|grep supervisor`
2. 如果有的话先kill掉
3. 运行下面命令：
```
sudo touch /var/run/supervisor.sock
sudo chmod 777 /var/run/supervisor.soc
```
