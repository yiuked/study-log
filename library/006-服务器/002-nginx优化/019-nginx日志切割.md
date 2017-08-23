`nginx`日志默认情况下统统写入到一个文件中，文件会变的越来越大，非常不方便查看分析。以日期来作为日志的切割是比较好的，通常我们是以每日来做统计的。  
下面来说说`nginx`日志切割。  
关于`nginx`相关日志配置参见：《`nginx`日志配置》一文。`logrotate`用法参见《`logrotate`日志管理工具》。
1. 定义日志轮滚策略
```
# vim nginx-log-rotate
/data/weblogs/*.log {
    nocompress
    daily
    copytruncate
    create
    notifempty
    rotate 7
    olddir /data/weblogs/old_log
    missingok
    dateext
    postrotate
        /bin/kill -HUP `cat /var/run/nginx.pid 2> /dev/null` 2> /dev/null || true
    endscript
}
```
> `/data/weblogs/*.log`使用通配符时，`/data/weblogs/`目录下的所有匹配到的日志文件都将切割。如果要切割特定日志文件，就指定到该文件.

2. 设置计划任务
```
# vim /etc/crontab
59 23 * * * root ( /usr/sbin/logrotate -f /PATH/TO/nginx-log-rotate)
```
这样每天23点59分钟执行日志切割。
