默认情况下`proxy_max_temp_file_size`值为1024MB,也就是说后端服务器的文件不大于1G都可以缓存到nginx代理硬盘中，如果超过1G，那么文件不缓存，而是直接中转发送给客户端.如果`proxy_max_temp_file_size`设置为0，表示不使用临时缓存。  

在大文件的环境下，如果想启用临时缓存，那么可以修改配置，值改成你想要的。  
修改nginx配置
```
location /
 {
 ...
 proxy_max_temp_file_size 2048m;
 ...
 }
 ```
重启nginx
```
# /usr/local/nginx-1.7.0/sbin/nginx -s reload
```
