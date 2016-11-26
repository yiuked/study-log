## 隐藏Nginx版本号的安全性与方法

搭建好`nginx`或者`apache`，为了安全起见我们都会隐藏他们的版本号，这边讲的是`nginx`的版本号。  
`Nginx`默认是显示版本号的，如：  
```
[root@bkjz ~]# curl -I www.nginx.org
HTTP/1.1 200 OK
Server: nginx/0.8.44
Date: Tue, 13 Jul 2010 14:05:11 GMT
Content-Type: text/html
Content-Length: 8284
Last-Modified: Tue, 13 Jul 2010 12:00:13 GMT
Connection: keep-alive
Keep-Alive: timeout=15
Accept-Ranges: bytes
```
这样就给人家看到你的服务器`nginx`版本是`0.8.44`，前些时间暴出了一些`Nginx`版本漏洞，就是说有些版本有漏洞，而有些版本没有。  
这样暴露出来的版本号就容易变成攻击者可利用的信息。所以，从安全的角度来说，隐藏版本号会相对安全些！  

那`nginx`版本号可以隐藏不？其实可以的，看下面的步骤：  

1. 进入`nginx`配置文件的目录（此目录根据安装时决定），用`vim`编辑打开
```
# vim nginx.conf
```
在`http {—}`里加上`server_tokens off;` 如：
```
http {
……省略
sendfile on;
tcp_nopush on;
keepalive_timeout 60;
tcp_nodelay on;
server_tokens off;
…….省略
}
```
2. 编辑`fastcgi`配置文件，如`fastcgi.conf`或`fcgi.conf`（这个配置文件通常与`nginx.conf`处于同一目录）：  
```
fastcgi_param SERVER_SOFTWARE nginx/$nginx_version;
```
改为：
```
fastcgi_param SERVER_SOFTWARE nginx;
```

3. 重新加载`nginx`配置：
```
# /etc/init.d/nginx reload
```

这样就完全对外隐藏了`nginx`版本号了，就是出现`404`、`501`等页面也不会显示`nginx`版本。  
