## 通过Nginx实现负载均衡

>1. [通过Nginx实现负载均衡](#通过Nginx实现负载均衡 "通过Nginx实现负载均衡")
	1. [一、概述](#一、概述 "一、概述")
	1. [二、安装与配置Nginx](#二、安装与配置Nginx "二、安装与配置Nginx")
	1. [三、配置负载均衡](#三、配置负载均衡 "三、配置负载均衡")
	1. [四、负载均衡调度策略](#四、负载均衡调度策略 "四、负载均衡调度策略")
	1. [五、实现SSL](#五、实现SSL "五、实现SSL")

### 一、概述
`Nginx`负载均衡的应用很广，很多场景下都在使用这种架构。  

环境如下：
```
192.168.1.100 (master node)  server1
192.168.1.109 (slave)        server2
192.168.1.106 (slave)        server3
```

### 二、安装与配置Nginx
1. 安装nginx
在上面三台服务器上，分别安装`nginx`
```
yum install nginx
```
2. 配置nginx

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

3. 配置虚拟主机

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

### 三、配置负载均衡
1. master 只做负载均衡调度，不受理业务请求。
  在`server1`上  

  ```
  nano -w /etc/nginx/conf.d/balancer.com.conf
  upstream balancer {
      server 192.168.1.109:80 ;
      server 192.168.1.106:80 ;
  }

  server {
      listen 192.168.1.100:80;
      server_name yoursite.com;
      error_log /var/log/yoursite.com-error.log;
      location / {
          proxy_set_header Host  $host; # 设置Header中的Host
          proxy_pass http://balancer;
      }

  }
  ```
  `master`主机只转发请求，所有的请求都转向到`slave`上进行处理。  
2. master 即做负载均衡调度，又做业务请求。

  ```
  server {
  access_log off;
  error_log /var/log/yoursite.com-error.log;
          listen 127.0.01:80;
          server_name  yoursite.com www.yoursite.com;

      location / {
              root   /var/www/yoursite.com;
              index  index.php index.html index.htm;
          }

  }

  upstream balancer {
      server 192.168.1.109:80 ;
      server 192.168.1.106:80 ;
      server 127.0.0.1:80 ;
  }

  server {
      listen 192.168.1.100:80;
      server_name yoursite.com;
      error_log /var/log/yoursite.com-error.log;
      location / {
          proxy_set_header Host  $host; # 设置Header中的Host
          proxy_pass http://balancer;
      }

  }
  ```
> 由于负载均衡通过中间节点进行了转发，因此业务端最终接受到的参数与实际参数可能存在差异，如客户端IP地址、Host。  
同时 ，也可以通过转发节点进行header重写：
```
location / {
    proxy_set_header Host  $host; # 设置Header中的Host
    proxy_pass http://balancer;
}
```
以上通过重写Host,那么业务受理机，可以接受来处多个负载均衡转发节点转发过来的请求。
```
location / {
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://balancer;
}
```
客户端的IP地址如果不进行Header重写，会在转发节点丢失。

### 四、负载均衡调度策略
负载均衡的策略控制主要在以下代码中控制
```
upstream balancer {
    server 192.168.1.109:80 ;
    server 192.168.1.106:80 ;
    server 127.0.0.1:80 ;
}
```
Nginx支持6种策略:  

| 类型     | 描述     |
| :------------- | :------------- |
| 轮询       | 默认方式       |
| weight       | 指定权限       |
| ip_hash       | 通过IP地址分配       |
| least_conn       | 最小连接数方式       |
| fair       | 响应时间方式       |
| url_hash       | 根据URL地址分配       |

1. 设置weight的值，指定权重
```
upstream balancer {
    server 192.168.1.109:80 weight=10;
    server 192.168.1.106:80 weight=8;
    server 127.0.0.1:80 weight=5;
}
```
2. ip_hash 通过IP地址分配
```
upstream balancer {
    ip_hash;
    server 192.168.1.109:80 ;
    server 192.168.1.106:80 ;
    server 127.0.0.1:80 ;
}
```
3. least_conn 通过最小连接数分配
```
upstream balancer {
    least_conn;
    server 192.168.1.109:80 ;
    server 192.168.1.106:80 ;
    server 127.0.0.1:80 ;
}
```
4. fair 通过服务器的响应时间来分配
```
upstream balancer {
    fair;
    server 192.168.1.109:80 ;
    server 192.168.1.106:80 ;
    server 127.0.0.1:80 ;
}
```
5. url_hash 通过URL地址来分配
```
upstream balancer {
    hash $request_uri;
    server 192.168.1.109:80 ;
    server 192.168.1.106:80 ;
    server 127.0.0.1:80 ;
}
```

### 五、实现SSL
现在越来越多的网站接入SSL，SSK能提高数据传输的安全，当然这也不是绝对的。本节当实现负载均衡下接入SSL的方式。  

负载均衡模式下，数据先到master，再由master到slave,如果业务处理服务器仅在自己的专有网络上访问，不直接暴露在外网，SSL可只做到master，如下:
```
upstream balancer {
    server 192.168.1.109:80 ;
    server 192.168.1.106:80 ;
    server 127.0.0.1:80 ;
}

server {
    listen 192.168.1.100:443;
    server_name yoursite.com;
    error_log /var/log/yoursite.com-error.log;
    ssl on;

    ssl_certificate /usr/local/nginx/cert/server_cert.pem;
    ssl_certificate_key /usr/local/nginx/cert/private.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://balancer;
    }
}
```

如果安全性要求较高，或者业务受理服务器可能会直接暴露在外网，那么，可以选择为每一层转发做SSL。
```
upstream balancer {
    server 192.168.1.109:443 ;
    server 192.168.1.106:443 ;
}

server {
    listen 192.168.1.100:443;
    server_name yoursite.com;
    error_log /var/log/yoursite.com-error.log;
    ssl on;

    ssl_certificate /usr/local/nginx/cert/server_cert.pem;
    ssl_certificate_key /usr/local/nginx/cert/private.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://balancer;
    }
}
```

参考文档：  
http://nginx.org/en/docs/http/load_balancing.html  
http://wiki.nginx.org/HttpUpstreamModule  
http://wiki.nginx.org/LoadBalanceExample  
