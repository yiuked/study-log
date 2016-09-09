环境：
CentOS release 5.8 192.168.10.108 cat

CentOS release 5.5 912.168.200.208
主调度器：192.168.10.108 192.169.10.251

备调度器：192.168.200.208 192.168.200.148

real ip :
192.169.10.251
192.168.200.148

vip : 192.168.10.104

 

一、在主备服务器上部署nginx

1、下载

wget http://nginx.org/download/nginx-1.0.11.tar.gz

wget http://labs.frickle.com/files/ngx_cache_purge-1.4.tar.gz

 

2、安装

yum -y install zlib-devel pcre-devel openssl-devel  # 安装依赖

tar –xvf ngx_cache_purge-1.4.tar.gz

tar –xvf nginx-1.0.11.tar.gz
cd nginx-1.0.11/

./configure –prefix=/usr/local/nginx –add-module=../ngx_cache_purge-1.4 –with-http_stub_status_module –with-http_ssl_module –with-http_flv_module –with-http_gzip_static_module

Make && make install

 

vi /usr/local/nginx/conf/nginx.conf

user nobody;
worker_processes 8;

#error_log logs/error.log error;
error_log /data/logs/error.log crit;

#error_log logs/error.log notice;
#error_log logs/error.log info;

#pid logs/nginx.pid;
events {
worker_connections 1024;
}
http {
include mime.types;
default_type application/octet-stream;

charset utf-8;
server_names_hash_bucket_size 128;
client_header_buffer_size 32k;
large_client_header_buffers 4 32k;
client_max_body_size 300m;
tcp_nopush on;
tcp_nodelay on;
client_body_buffer_size 512k;
proxy_connect_timeout 5;
proxy_read_timeout 60;
proxy_send_timeout 5;
proxy_buffer_size 16k;
proxy_buffers 4 64k;
proxy_busy_buffers_size 128k;
proxy_temp_file_write_size 128k;
#log_format main ‘$remote_addr – $remote_user [$time_local] “$request” ‘
# ‘$status $body_bytes_sent “$http_referer” ‘
# ‘”$http_user_agent” “$http_x_forwarded_for”‘;

#access_log logs/access.log main;

sendfile on;

#keepalive_timeout 65;
gzip on;
gzip_min_length 1k;
gzip_buffers 4 16k;
gzip_http_version 1.1;
gzip_comp_level 2;
gzip_types text/plain application/x-javascript text/css application/xml;
gzip_vary on;
proxy_temp_path /data/proxy_temp_dir;
proxy_cache_path /data/proxy_cache_dir levels=1:2 keys_zone=cache_one:50m inactive=1m max_size=2g;
upstream real_server_pool{
server 192.168.200.148:80 weight=1 max_fails=2 fail_timeout=30s;
server 192.168.10.251:80 weight=1 max_fails=2 fail_timeout=30s;
}

#tcp_nopush on;

#keepalive_timeout 0;
keepalive_timeout 65;

#gzip on;

server {
listen 80;
server_name localhost;

#charset koi8-r;

#access_log logs/host.access.log main;

location / {
root html;

index index.html index.htm;

proxy_next_upstream http_502 http_504 error timeout invalid_header;
proxy_cache cache_one;
proxy_cache_valid 200 304 12h;
proxy_cache_key $host$uri$is_args$args;
proxy_set_header Host $host;
proxy_set_header X-Forwarded-For $remote_addr;
proxy_pass http://real_server_pool;
expires 1d;

 

}

#error_page 404 /404.html;

# redirect server error pages to the static page /50x.html
#
error_page 500 502 503 504 /50x.html;
location = /50x.html {
root html;
}

# proxy the PHP scripts to Apache listening on 127.0.0.1:80
#
#location ~ \.php$ {
# proxy_pass http://127.0.0.1;
#}
location ~ .*\.(php|jsp|cgi)?$
{
proxy_set_header Host $host;
proxy_set_header X-Forwarded-For $remote_addr;
proxy_pass http://real_server_pool;
}
log_format access ‘$remote_addr – $remote_user [$time_local] “$request”‘
‘$status $body_bytes_sent “$http_referer” ‘
‘”$http_user_agent” $http_x_forwarded_for';
access_log /data/logs/access.log access;
}

 

# pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
#
#location ~ \.php$ {
# root html;
# fastcgi_pass 127.0.0.1:9000;
# fastcgi_index index.php;
# fastcgi_param SCRIPT_FILENAME /scripts$fastcgi_script_name;
# include fastcgi_params;
#}

# deny access to .htaccess files, if Apache’s document root
# concurs with nginx’s one
#
#location ~ /\.ht {
# deny all;
#}
}
# another virtual host using mix of IP-, name-, and port-based configuration
#
#server {
# listen 8000;
# listen somename:8080;
# server_name somename alias another.alias;

# location / {
# root html;
# index index.html index.htm;
# }
#}
# HTTPS server
#
#server {
# listen 443;
# server_name localhost;

# ssl on;
# ssl_certificate cert.pem;
# ssl_certificate_key cert.key;

# ssl_session_timeout 5m;

# ssl_protocols SSLv2 SSLv3 TLSv1;
# ssl_ciphers HIGH:!aNULL:!MD5;
# ssl_prefer_server_ciphers on;

# location / {
# root html;
# index index.html index.htm;
# }
#}

 

备用调度器的nginx配置文件和主调度器的配置文件一样。

启动nginx

/usr/local/nginx/sbin/nginx

 

二、安装keepalived（在nginx的mater和backup都安装）

 

1、  下载

wget http://www.keepalived.org/software/keepalived-1.1.19.tar.gz

 

2、  安装

tar zxvf keepalived-1.1.19.tar.gz
cd keepalived-1.1.19
./configure –prefix=/usr/local/keepalived
make
make install

cp /usr/local/keepalived/sbin/keepalived /usr/sbin/
cp /usr/local/keepalived/etc/sysconfig/keepalived /etc/sysconfig/
cp /usr/local/keepalived/etc/rc.d/init.d/keepalived /etc/init.d/
mkdir /etc/keepalived

 

vi /etc/keepalived/keepalived.conf

vrrp_instance VI_INET1 {
state MASTER
interface eth0
virtual_router_id 53
priority 100
advert_int 1
authentication {
auth_type pass
auth_pass 1111
}
virtual_ipaddress {
192.168.10.104/24
}
}
virtual_server 192.168.10.104 80 {
delay_loop 6
lb_algo rr
lb_kind NAT
nat_mask 255.255.255.0
persistence_timeout 50
protocol TCP
real_server 192.168.10.251 80 {
weight 3
TCP_CHECK {
connect_timeout 10
nb_get_retry 3

delay_before_retry 3
connect_port 80
}
}
real_server 192.168.200.148 80 {
weight 3
TCP_CHECK {
connect_timeout 10
nb_get_retry 3
delay_before_retry 3
connect_port 80
}
}

}

4、配置备用调度器的keepalived,只需要将state MASTER 改为state BACKUP,降低priority 100 的值:

state MASTER —> state BACKUP

priority 100 —>  priority 99 （此值必须低于主的）

主备启动

/etc/init.d/keepalived start

 

三、测试

建立虚拟主机（自己测试啊    O(∩_∩)O~）