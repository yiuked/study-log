网友问如何在URL后面添加上斜杠。顺便总结了下针对URL结尾添加斜杠和删除斜杠的改写规则。
#### 在URL结尾添加斜杠
在虚拟主机中这么添加一条改写规则：  
```
rewrite ^(.*[^/])$ $1/ permanent;
```
例如：
```
server {
    listen 80;
    server_name bbs.ttlsa.com;
    rewrite ^(.*[^/])$ $1/ permanent;
}
```
#### 删除URL结尾的斜杠
在虚拟主机中这么添加一条改写规则：  
```
rewrite ^/(.*)/$ /$1 permanent;
```
例如：
```
server {
    listen 80;
    server_name bbs.ttlsa.com;
    rewrite ^/(.*)/$ /$1 permanent;
}
```
不过建议删除URL结尾的斜杠，会混乱搜索引擎的。  
