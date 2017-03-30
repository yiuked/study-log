## nginx+memcached构建页面缓存应用
`nginx`的`memcached_module`模块可以直接从`memcached`服务器中读取内容后输出，后续的请求不再经过应用程序处理，如`php-fpm`、`django`，大大的提升动态页面的速度。`nginx`只负责从`memcached`服务器中读取数据，要往`memcached`写入数据还得需要后台的应用程序来完成，主动的将要缓存的页面缓存到`memcached`中，可以通过404重定向到后端去处理的。
`ngx_http_memcached_module`可以操作任何兼用`memcached`协议的软件。如`ttserver`、`membase`等。

结构图如下：

memcached

`memcached`的`key`可以通过`memcached_key`变量来设置，如以`$uri`。如果命中，那么直接输出内容，没有命中就意味着`nginx`需要从应用程序请求页面。同时，我们还希望该应用程序将键值对写入到`memcached`，以便下一个请求可以直接从`memcached`获取。
如果键值不存在，`nginx`将报告`not found`错误。最好的方法是使用`error_page`指定和`location`请求处理。同时包含"Bad Gateway"错误和"Gateway Timeout"错误，如：error_page 404 502 504 = @app;。
注意：需要设置d`efault_type`，否则可能会显示不正常。

1. 模块指令说明：
memcached_bind
语法: memcached_bind address | off;
默认值: none
配置段: http, server, location
指定从哪个IP来连接memcached服务器

memcached_buffer_size
语法: memcached_buffer_size size;
默认值: 4k|8k;
配置段: http, server, location
读取从memcached服务器接收到响应的缓冲大小。尽快的将响应同步传给客户端。

memcached_connect_timeout
语法：memcached_connect_timeout time;
默认值：60s;
配置段：http, server, location
与memcached服务器建立连接的超时时间。通常不超过75s。

memcached_gzip_flag
语法：memcached_gzip_flag flag;
默认值：none
配置段：http, server, location
测试memcached服务器响应标志。如果设置了，将在响应头部添加了Content-Encoding：gzip。

memcached_next_upstream
语法: memcached_next_upstream error | timeout | invalid_response | not_found | off …;
默认值： error timeout;
配置段: http, server, location
指定在哪些状态下请求将转发到另外的负载均衡服务器上，仅当memcached_pass有两个或两个以上时使用。

memcached_pass
语法：memcached_pass address:port or socket；
默认值：none
配置段：location, if in location
指定memcached服务器地址。使用变量$memcached_key为key查询值，如果没有相应的值则返回error_page 404。

memcached_read_timeout
语法：memcached_read_timeout time;
默认值：60s;
配置段：http, server, location
定义从memcached服务器读取响应超时时间。

memcached_send_timeout
语法：memcached_send_timeout
默认值：60s
配置段：http, server, location
设置发送请求到memcached服务器的超时时间。

$memcached_key变量：
memcached key的值。

2. nginx memcached的增强版ngx_http_enhanced_memcached_module
基于nginx memcached 模块的，添加的新特性有：
1. 自定义HTTP头，如Content-Type, Last-Modified。
2. hash键可超过250个字符，memcached受限。
3. 通过HTTP请求将数据存储到memcached。
4. 通过HTTP请求从memcached删除数据。
5. 通过HTTP请求清除所有memcached缓存数据。
6. 通过HTTP请求获取memcached状态数据。
7. 键名空间管理，来部分刷新缓存。
8. 缓存通过If-Modified-Since头和内容Last-Modified来回复304Not Modified请求。

3. 应用实例
`nginx`配置实例：
```
upstream memcacheds {
        server 10.1.240.166:22222;
}
server  {
        listen       8080;
        server_name  nm.ttlsa.com;
        index index.html index.htm index.php;
        root  /data/wwwroot/test.ttlsa.com/webroot;

        location /images/ {
                set $memcached_key $request_uri;
                add_header X-mem-key  $memcached_key;
                memcached_pass  memcacheds;
                default_type text/html;
                error_page 404 502 504 = @app;
        }

        location @app {
                rewrite ^/.* /nm_ttlsa.php?key=$request_uri;
        }

        location ~ .*\.php?$
        {
                include fastcgi_params;
                fastcgi_pass  127.0.0.1:10081;
                fastcgi_index index.php;
                fastcgi_connect_timeout 60;
                fastcgi_send_timeout 180;
                fastcgi_read_timeout 180;
                fastcgi_buffer_size 128k;
                fastcgi_buffers 4 256k;
                fastcgi_busy_buffers_size 256k;
                fastcgi_temp_file_write_size 256k;
                fastcgi_intercept_errors on;
                fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
        }
}
```
`nm_ttlsa.php`实例：  
```
<?php
$fn = dirname(__FILE__)  . $_SERVER['REQUEST_URI'];
if(file_exists($fn)) {
	$data = file_get_contents($fn);
	$m = new Memcached();
	$servers = array(
					array('10.1.240.166', 22222)
				);
	$m->addServers($servers);

	$r=$m->set($_GET['key'],$data);
	header('Content-Length: '.filesize($fn)."\r\n");
	header('Content-Type: image/gif'."\r\n");
	header('X-cache: MISS'."\r\n");
	print $data;
}else{
	header('Location: http://www.ttlsa.com'."\r\n");
}
```
#### 测试  
第一次访问：（需要经过`php`处理）
