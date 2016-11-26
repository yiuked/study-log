## nginx针对爬虫进行限速配置
网络爬虫一方面可以给网站带来一定的流量，便于搜索引擎收录，利于用户搜素，同时也会给服务器带来一定的压力，在网络爬虫对网站内容进行收录时，会引起服务器负载高涨。有没有什么方法既不阻止网络爬虫对网站内容进行收录，同时对其连接数和请求数进行一定的限制呢？  

先来普及下`robots.txt`协议：
`robots.txt`（也称为爬虫协议、爬虫规则、机器人协议等）是放置在网站根目录中的`.TXT`文件，是搜索引擎蜘蛛程序默认访问网站第一要访问的文件，如果 搜索引擎蜘蛛程序找到这个文件，它就会根据这个文件的内容，来确定它访问权限的范围。`robots.txt`将告诉搜索引擎蜘蛛程序网站哪些页面时可以访问，哪些不可以。`Robots`协议是网站国际互联网界通行的道德规范，其目的是保护网站数据和敏感信息、确保用户个人信息和隐私不被侵犯。因其不是命令，故需要搜索引擎自觉遵守。  
**robots.txt必须放置在一个站点的根目录下，而且文件名必须全部小写,一词不差。**  

`robots.txt`写法：  
```
User-agent: * 这里的*代表的所有的搜索引擎种类，*是一个通配符
Disallow: /admin/ 这里定义是禁止爬寻admin目录下面的内容
Disallow: /require/ 这里定义是禁止爬寻require目录下面的内容
```

对爬虫进行限速处理实现方法如下：
```
http {
    map $http_user_agent $agent {
        default "";
        ~curl $http_user_agent;
        ~*apachebench $http_user_agent;
        ~*spider $http_user_agent;
        ~*bot  $http_user_agent;
        ~*slurp $http_user_agent;
    }
    limit_conn_zone $agent zone=conn_ttlsa_com:10m;
    limit_req_zone $agent zone=req_ttlsa_com:10m rate=1r/s;

    server {
        listen       8080;
        server_name  test.ttlsa.com;
        root /data/webroot/www.ttlsa.com/

        location   / {
            limit_req zone=conn_ttlsa_com burst=5;
            limit_conn req_ttlsa_com 1;
            limit_rate 500k;
        }
    }
}
```
测试：
```
# ab -c 10 -n 300 http://test.com:8080/12.html
```
