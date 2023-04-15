## Xdebug 应用
#### 安装
下载地址：  
windows  
http://windows.php.net/downloads/pecl/releases/xdebug  

其它平台  
https://xdebug.org/docs/install  

配置  
```
[xdebug]
zend_extension = "C:\php\ext\php_xdebug.dll"
xdebug.remote_enable = 1
xdebug.remote_host = 127.0.0.1
xdebug.remote_port = 9000
xdebug.remote_mode = req
xdebug.remote_handler = dbgp
xdebug.profiler_output_dir="C:\php\tmp\xdebug"
xdebug.trace_output_dir="C:\php\tmp\xdebug"
```

将日志输出到标准的输出
```
zend_extension=xdebug.so
xdebug.mode=debug
xdebug.start_with_request=yes
xdebug.client_host=127.0.0.1
xdebug.log=/dev/stdout
```

如果php是在docker启动，需要在宿主机调用，需要将host改为
```
# docker-compose.yaml添加以下代码
extra_hosts:
  - "host.docker.internal:host-gateway"

zend_extension=xdebug.so
xdebug.mode=debug
xdebug.start_with_request=yes
xdebug.client_host=host.docker.internal
xdebug.log=/dev/stdout
```

是IDE监听9000端口，php中的xdebug向IDE上报调试信息