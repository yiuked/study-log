如果nginx被攻击或者访问量突然变大，nginx会因为负载变高或者内存不够用导致服务器宕机，最终导致站点无法访问。今天要谈到的解决方法来自淘宝开发的模块nginx-http-sysguard，主要用于当负载和内存达到一定的阀值之时，会执行相应的动作，比如直接返回503,504或者其他的.一直等到内存或者负载回到阀值的范围内，站点恢复可用。简单的说，这几个模块是让nginx有个缓冲时间，缓缓.
1. 安装nginx sysguard模块

1.1 下载文件
# wget http://nginx.org/download/nginx-1.4.2.tar.gz
# wget https://github.com/alibaba/nginx-http-sysguard/archive/master.zip \
-O nginx-http-sysguard-master.zip
# unzip nginx-http-sysguard-master.zip
# tar -xzvf nginx-1.4.2.tar.gz

1.2 打sysgrard补丁
这边没找到nginx-1.4.2对应的补丁，只有1.2.9和1.3.9的，索性试试1.3.9的吧，应该差不多.
# cd nginx-1.4.2
# patch -p1 < ../nginx-http-sysguard-master/nginx_sysguard_1.3.9.patch

1.3 安装nginx
# ./configure --prefix=/usr/local/nginx-1.4.2 \
--with-http_stub_status_module --add-module=../nginx-http-sysguard
# make
# make install
2. sysguard指令

语法: sysguard [on | off]
默认值: sysguard off
配置段: http, server, location
开关模块

语法: sysguard_load load=number [action=/url]
默认值: none
配置段: http, server, location
指定负载阀值,当系统的负载超过这个值，所有的请求都会被重定向到action定义的uri请求中.如果没有定义URL action没有定义，那么服务器直接返回503

语法: sysguard_mem swapratio=ratio% [action=/url]
默认值: none
配置段: http, server, location
定义交换分区使用的阀值，如果交换分区使用超过这个阀值，那么后续的请求全部被重定向到action定义的uri请求中.如果没有定义URL action没有定义，那么服务器直接返回503

语法: sysguard_interval time
默认值: sysguard_interval 1s
配置段: http, server, location
定义系统信息更新的频率,默认1秒.

语法: sysguard_log_level info | notice | warn | error
默认值: sysguard_log_level error
配置段: http, server, location
定义sysguard的日志级别
3. sysguard使用实例

3.1 nginx配置
server {
    listen       80;
    server_name  www.ttlsa.com www.heytool.com;
    access_log  /data/logs/nginx/www.ttlsa.com.access.log  main;
 
    index index.html index.php index.html;
    root /data/site/www.ttlsa.com;
 
    sysguard on;
    
# 为了方便测试，load阀值为0.01，平时大家一般都在5或10+
    sysguard_load load=0.01 action=/loadlimit;
    sysguard_mem swapratio=20% action=/swaplimit;
 
    location / {
 
    }
 
    location /loadlimit {
        return 503;
    }
 
    location /swaplimit {
        return 503;
    }
}

3.2 测试
负载OK的情况下,访问nginx
# uptime
 16:23:37 up 6 days,  8:04,  2 users,  load average: 0.00, 0.01, 0.05
# curl -I www.ttlsa.com
HTTP/1.1 403 Forbidden
Server: nginx
Date: Thu, 03 Oct 2013 16:27:13 GMT
Content-Type: text/html
Content-Length: 162
Connection: keep-alive

因为站点下没有文件，所以返回了403，实际上没关系.

负载超过阀值的情况下，访问nginx
# uptime
 16:25:59 up 6 days,  8:06,  2 users,  load average: 0.05, 0.04, 0.05
# curl -I www.ttlsa.com
HTTP/1.1 503 Service Temporarily Unavailable
Server: nginx
Date: Thu, 03 Oct 2013 16:26:19 GMT
Content-Type: text/html
Content-Length: 206
Connection: keep-alive

swap超过阀值的功能我就不再测试了。大家回家可以自己动手测试一下.
结束语

在nginx是realserver的情况下，个人也比较推荐使用这种方法，如果服务器负载一旦爬高，一般要比较长的时间才能恢复到正常水平，在采用这个插件的情况下，负载达到阀值，nginx返回503，前段使用故障转移将请求发往其他服务器，这台服务器在无访问的情况下，便能很快的恢复到正常水平，并且能够立即投入工作。超过阀值的服务器处理请求速度也会大打折扣，使用这个模块，巧妙的将请求发送到了更快速的服务器上，在一定程度上避免了访问速度慢的问题. 前面说的是在集群环境下，在单点环境下，用不用大家斟酌一下。

参考文章：
nginx-http-sysguard:https://github.com/alibaba/nginx-http-sysguard
TCP Proxy:https://github.com/yaoweibin/nginx_tcp_proxy_module (相同功能软件)