下载服务器上有众多的软件资源, 可是很多来源不是本站，是迅雷、flashget, 源源不断的带宽,防盗链绝对是当务之急.   
使用来源判断根本不靠谱，只能防止一些小白站点的盗链，迅雷之类的下载工具完全无效，如果你是`nginx`的话，使用`secure link`完美解决这个问题，远离迅雷.  
本文仅用于下载服务器，不适用于图片防盗链.  

#### 安装nginx  
默认情况下`nginx`不会安装`secure_link`模块,需要手动指定,配置参数如下  
```
# ./configure --with-http_secure_link_module \
--prefix=/usr/local/nginx-1.4.2 --with-http_stub_status_module
# make
# make install
```

#### 配置nginx
```
server {

    listen       80;
    server_name  s1.down.ttlsa.com;
    access_log  /data/logs/nginx/s1.down.ttlsa.com.access.log  main;

    index index.html index.php index.html;
    root /data/site/s1.down.ttlsa.com;

    location / {
        secure_link $arg_st,$arg_e;
        secure_link_md5 ttlsa.com$uri$arg_e;

        if ($secure_link = "") {
            return 403;
        }

        if ($secure_link = "0") {
            return 403;
        }
    }
}
```

#### php下载页面
```php
<?php
# 作用：生成nginx secure link链接
# 站点：www.ttlsa.com
# 作者：凉白开
# 时间：2013-09-11
$secret = 'ttlsa.com'; # 密钥
$path = '/web/nginx-1.4.2.tar.gz'; # 下载文件
# 下载到期时间,time是当前时间,300表示300秒,也就是说从现在到300秒之内文件不过期
$expire = time()+300;
# 用文件路径、密钥、过期时间生成加密串
$md5 = base64_encode(md5($secret . $path . $expire, true));
$md5 = strtr($md5, '+/', '-_');
$md5 = str_replace('=', '', $md5);
# 加密后的下载地址
echo '<a href=http://s1.down.test.com/web/nginx-1.4.2.tar.gz?st='.$md5.'&e='.$expire.'>nginx-1.4.2</a>';
echo '<br>http://s1.down.test.com/web/nginx-1.4.2.tar.gz?st='.$md5.'&e='.$expire;
```

#### 测试nginx防盗链
打开 http://test.test.com/down.php 点击上面的连接下载  
下载地址如下：  
http://s1.down.test.com/web/nginx-1.4.2.tar.gz?st=LSVzmZllg68AJaBmeK3E8Q&e=1378881984
页面不要刷新，等到5分钟后在下载一次，你会发现点击下载会跳转到403页面。  

#### secure link 防盗链原理

* 用户访问`down.php`
* `down.php`根据`secret`密钥、过期时间、文件`uri`生成加密串  
* 将加密串与过期时间作为参数跟到文件下载地址的后面  
* `nginx`下载服务器接收到了过期时间，也使用过期时间、配置里密钥、文件uri生成加密串  
* 将用户传进来的加密串与自己生成的加密串进行对比，一致允许下载，不一致`403`
* 整个过程实际上很简单，类似于用户密码验证. 尤为注意的一点是大家一定不要泄露了自己的密钥，否则别人就可以盗链了，除了泄露之外最好能经常更新密钥.

#### secure link 指令
`secure_link`  
语法: `secure_link md5_hash[,expiration_time]`
默认: `none`
配置段: `location`
`variables: yes`  
这个指令由`uri`中的`MD5`哈希值和过期时间组成. `md5`哈希必须由`base64`加密的,过期时间为`unix`时间.如果不加过期时间,那么这个连接永远都不会过期.  

`secure_link_md5`  
语法: `secure_link_md5 secret_token_concatenated_with_protected_uri`  
默认: `none`  
配置段: `location`  
`variables: yes`  
`md5`值对比结果,使用上面提供的`uri`、密钥、过期时间生成`md5`哈希值.如果它生成的`md5`哈希值与用户提交过来的哈希值一致，那么这个变量的值为1，否则为0  

`secure_link_secret`  
语法: `secure_link_secret word`
默认:
配置段: `location`
`Reference:    secure_link_secret`  
`nginx 0.8.50`之后的版本已经使用`secure_link_md5`取代,不在多说.  

#### 注意事项
密钥防止泄露、以及经常更新密钥    
下载服务器和`php`服务器的时间不能相差太大，否则容易出现文件一直都是过期状态.    

#### 最后
`secure link`以及内置到了`nginx`，不需要额外安装第三方模块，有下载服务器的兄弟,我极力推荐你们使用它，除非你不在乎你的带宽.  
