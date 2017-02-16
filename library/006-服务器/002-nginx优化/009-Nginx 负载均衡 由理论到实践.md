`Nginx`负载均衡的应用很广，很多场景下都在使用这种架构。  

环境如下：
```
192.168.1.100 (master node)  server1
192.168.1.109 (slave)        server2
192.168.1.106 (slave)        server3
```

### 安装nginx
在上面三台服务器上，分别安装`nginx`
```
yum install nginx
```
### 配置nginx

在上面三台服务器上，分别配置`nginx`
```
user  nginx;
worker_processes  1;
error_log  /var/log/nginx_error.log crit;

worker_rlimit_nofile  8192;

events {
worker_connections  1024;
# you might need to increase this setting for busy servers
use epoll;
#  Linux kernels 2.6.x change to epoll
}

http {
server_names_hash_max_size 2048;
server_names_hash_bucket_size 512;

server_tokens off;

include    mime.types;
default_type  application/octet-stream;

sendfile on;
tcp_nopush on;
tcp_nodelay on;
keepalive_timeout  10;

# Gzip on
gzip on;
gzip_min_length  1100;
gzip_buffers  4 32k;
gzip_types    text/plain application/x-javascript text/xml text/css;

ignore_invalid_headers on;
client_max_body_size    8m;
client_header_timeout  3m;
client_body_timeout 3m;
send_timeout     3m;
connection_pool_size  256;
client_header_buffer_size 4k;
large_client_header_buffers 4 64k;
request_pool_size  4k;
output_buffers   4 32k;
postpone_output  1460;

# Cache most accessed static files
open_file_cache          max=10000 inactive=10m;
open_file_cache_valid    2m;
open_file_cache_min_uses 1;
open_file_cache_errors   on;

# Include each virtual host
include "/etc/nginx/conf.d/*.conf";
}
```
### 配置虚拟主机

在`server2`和`server3`上  
```
nano -w /etc/nginx/conf.d/mysite.com.conf
server {
access_log off;
error_log /var/log/yoursite.com-error.log;
        listen 80;
        server_name  yoursite.com www.yoursite.com;
        location ~* .(gif|jpg|jpeg|png|ico|wmv|3gp|avi|mpg|mpeg|mp4|flv|mp3|mid|js|css|wml|swf)$ {
        root   /var/www/yoursite.com;
                expires max;
                add_header Pragma public;
                add_header Cache-Control "public, must-revalidate, proxy-revalidate";

        }
        location / {
            root   /var/www/yoursite.com;
            index  index.php index.html index.htm;
        }
      }
```

在`server1`上  

```
nano -w /etc/nginx/conf.d/balancer.com.conf
upstream balancer {
    server 192.168.1.100:80 ;
    server 192.168.1.106:80 ;
}

server {
    listen 192.168.1.100:80;
    server_name yoursite.com;
    error_log /var/log/yoursite.com-error.log;
    location / {
        proxy_pass http://balancer;
    }

}
```
重启`nginx`  
```
service nginx restart
```

`DNS`记录
```
yoursite.com IN A 192.168.1.100
www IN A 192.168.1.100
```

如果仅仅是为了测试，直接绑定`hosts`文件。  
```
The master server
```
之所以叫它`master`，是由于作为主的负载均衡器使用的。它也可以被用来从`slave`上请求服务。  
```
upstream balancer {
    server 192.168.1.100:80 ;
    server 192.168.1.106:80 ;
}

server {
    listen 192.168.1.100:80;
    server_name yoursite.com;
    error_log /var/log/yoursite.com-error.log;
    location / {
        proxy_pass http://balancer;
    }

}
```

### 另一种场景，负载均衡器同时做为请求  
```
server {
access_log off;
error_log /var/log/yoursite.com-error.log;
        listen 127.0.01:80;
        server_name  yoursite.com www.yoursite.com;

location ~* .(gif|jpg|jpeg|png|ico|wmv|3gp|avi|mpg|mpeg|mp4|flv|mp3|mid|js|css|wml|swf)$ {
        root   /var/www/yoursite.com;
                expires max;
                add_header Pragma public;
                add_header Cache-Control "public, must-revalidate, proxy-revalidate";

        }

    location / {
            root   /var/www/yoursite.com;
            index  index.php index.html index.htm;
        }

}

upstream balancer {
    server 192.168.1.100:80 ;
    server 192.168.1.106:80 ;
    server 127.0.0.1:80 ;
}

server {
    listen 192.168.1.100:80;
    server_name yoursite.com;
    error_log /var/log/yoursite.com-error.log;
    location / {
        proxy_pass http://balancer;
    }

}
```

参考文档：  
http://nginx.org/en/docs/http/load_balancing.html  
http://wiki.nginx.org/HttpUpstreamModule  
http://wiki.nginx.org/LoadBalanceExample  
