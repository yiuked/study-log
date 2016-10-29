随着nginx的迅速崛起，越来越多公司将`apache`更换成`nginx`. 同时也越来越多人使用`nginx`作为负载均衡,   
并且代理前面可能还加上了`CDN`加速，但是随之也遇到一个问题：  
`nginx`如何获取用户的真实`IP`地址,如果后端是`apache`,请跳转到<`apache获取用户真实IP地址`>，  
如果是后端真实服务器是`nginx`，那么继续往下看。  

实例环境：  
```
用户IP 120.22.11.11
CDN前端 61.22.22.22
CDN中转 121.207.33.33
```
公司NGINX前端代理 `192.168.50.121`（外网`121.207.231.22`）  

1. 使用`CDN`自定义`IP`头来获取  

假如说你的`CDN`厂商使用`nginx`,那么在`nginx`上将`$remote_addr`赋值给你指定的头,方法如下:  
```
proxy_set_header remote-user-ip $remote_addr;
```
//如上,后端将会收到`remote_user_ip`的`http`头，有些人可能会挑错了，说我设置的头不是`remote-user-ip`吗,  
怎么写成了`remote_user_ip`,是不是作者写错了.请参考文章：<`nginx反向代理proxy_set_header自定义header头无效`>  

后端 `PHP` 代码`getRemoteUserIP.php`  
```php
    $ip = getenv("HTTP_REMOTE_USER_IP");
    echo $ip;   
```

访问`getRemoteUserIP.php`,结果如下：  
```
120.22.11.11 //取到了真实的用户IP,如果CDN能给定义这个头的话,那这个方法最佳
```
2. 通过`HTTP_X_FORWARDED_FOR`获取`IP`地址  

一般情况下`CDN`服务器都会传送`HTTP_X_FORWARDED_FOR`头,这是一个`ip`串,后端的真实服务器获取`HTTP_X_FORWARDED_FOR`头,
截取字符串第一个不为`unkown`的`IP`作为用户真实`IP`地址, 例如：  
```
120.22.11.11,61.22.22.22,121.207.33.33,192.168.50.121（用户IP,CDN前端IP,CDN中转,公司NGINX代理）
```
`getFor.php`
```php
    $ip = getenv("HTTP_X_FORWARDED_FOR");
    echo $ip;
```

访问`getFor.php`结果如下：  
```
120.22.11.11,61.22.22.22,121.207.33.33,192.168.50.121
```
如果你是`php`程序员,你获取第一个不为`unknow`的`ip`地址,这边就是`120.22.11.11`.

3. 使用`nginx`自带模块`realip`获取用户`IP`地址  
安装`nginx`之时加上`realip`模块，我的参数如下：  
```linux
./configure --prefix=/usr/local/nginx-1.4.1 --with-http_realip_module
```
真实服务器nginx配置  
```
server {
    listen       80;
    server_name  www.ttlsa.com;
    access_log  /data/logs/nginx/www.ttlsa.com.access.log  main;

    index index.php index.html index.html;
    root /data/site/www.ttlsa.com;

    location /
    {
            root /data/site/www.ttlsa.com;
    }
    location = /getRealip.php
    {
            set_real_ip_from  192.168.50.0/24;
            set_real_ip_from  61.22.22.22;
            set_real_ip_from  121.207.33.33;
            set_real_ip_from 127.0.0.1;
            real_ip_header    X-Forwarded-For;
            real_ip_recursive on;
            fastcgi_pass  unix:/var/run/phpfpm.sock;
            fastcgi_index index.php;
            include fastcgi.conf;
    }
}
```

`getRealip.php`内容  
```php
    $ip =  $_SERVER['REMOTE_ADDR'];
    echo $ip;   
```

访问`www.test.com/getRealip.php`,返回：  
```
120.22.11.11
```

如果注释 `real_ip_recursive on` 或者 `real_ip_recursive off`
访问`www.test.com/getRealip.php`,返回：  
```
121.207.33.33
```

很不幸,获取到了中继的`IP`,`real_ip_recursive`的效果看明白了吧.
```
set_real_ip_from：真实服务器上一级代理的IP地址或者IP段,可以写多行
real_ip_header：从哪个header头检索出要的IP地址
real_ip_recursive：递归排除IP地址,ip串从右到左开始排除set_real_ip_from里面出现的IP,如果出现了未出现这些ip段的IP，那么这个IP将被认为是用户的IP。
```
例如我这边的例子，真实服务器获取到的IP地址串如下：
```
120.22.11.11,61.22.22.22,121.207.33.33,192.168.50.121
```
在`real_ip_recursive on`的情况下  
```
61.22.22.22,121.207.33.33,192.168.50.121都出现在set_real_ip_from中,仅仅120.22.11.11没出现,那么他就被认为是用户的ip地址，并且赋值到remote_addr变量
```

在`real_ip_recursive off`或者不设置的情况下  
```
192.168.50.121出现在set_real_ip_from中,排除掉，接下来的ip地址便认为是用户的ip地址
```
如果仅仅如下配置：  
```
set_real_ip_from   192.168.50.0/24;
set_real_ip_from 127.0.0.1;
real_ip_header    X-Forwarded-For;
real_ip_recursive on;
```

访问结果如下：  
```
121.207.33.33
```
4. 三种在`CDN`环境下获取用户`IP`方法总结  
*  `CDN`自定义`header`头  
优点：获取到最真实的用户`IP`地址,用户绝对不可能伪装`IP`  
缺点：需要`CDN`厂商提供  

* 获取`forwarded-for`头  
优点：可以获取到用户的IP地址  
缺点：程序需要改动,以及用户IP有可能是伪装的  

* 使用`realip` 获取  
优点：程序不需要改动，直接使用`remote_addr`即可获取`IP`地址  
缺点：`ip`地址有可能被伪装，而且需要知道所有`CDN`节点的`ip`地址或者`ip`段  
