灰度发布是指在黑与白之间，能够平滑过渡的一种发布方式。  
AB test就是一种灰度发布方式，让一部分用户继续用A，一部分用户开始用B，如果用户对B没有什么反对意见，那么逐步扩大范围，把所有用户都迁移到B上面来。  
灰度发布可以保证整体系统的稳定，在初始灰度的时候就可以发现、调整问题，以保证其影响度。  
灰度发布一般有三种方式 `nginx+lua`，`nginx`根据`cookie`分流，`nginx` 根据权重来分配  
`nginx+lua`根据来访者`ip`地址区分，由于公司出口是一个ip地址，会出现访问网站要么都是老版，要么都是新版，采用这种方式并不适合  
`nginx` 根据权重来分配，实现很简单，也可以尝试  
`nginx` 根据`cookie`分流，灰度发布基于用户才更合理  

两台服务器分别定义为  
```
tts_V6  192.168.3.81:5280
tts_V7  192.168.3.81:5380
```

默认服务器为：  
```
default：192.168.3.81:5280
```

前端`nginx`服务器监听端口80，需要根据`cookie`转发，查询的`cookie`的键（`key`）为`tts_version_id`（该键由开发负责增加），如果该`cookie`值（`value`）为`tts1`则转发到`tts_V6`，为`tts2`则转发到`tts_V7`。  

```
upstream tts_V6 {
         server 192.168.3.81:5280 max_fails=1 fail_timeout=60;
 }
 upstream tts_V7 {
        server 192.168.3.81:5380 max_fails=1 fail_timeout=60;
 }
 upstream default {
         server 192.168.3.81:5280 max_fails=1 fail_timeout=60;
 }
 server {
         listen 80;
         server_name  test.taotaosou.com;
        access_log  logs/test.taotaosou.com.log  main buffer=32k;

#match cookie
         set $group "default";
         if ($http_cookie ~* "tts_version_id=tts1"){
                 set $group tts_V6;
         }
         if ($http_cookie ~* "tts_version_id=tts2"){
                 set $group tts_V7;
         }
         location / {
                 proxy_pass http://$group;
                 proxy_set_header   Host             $host;
                 proxy_set_header   X-Real-IP        $remote_addr;
                 proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
                 index  index.html index.htm;
        }
}
```
