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
