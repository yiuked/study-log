接触nginx的兄弟或多或少都有遇到缓存问题，要么是nginx为什么不缓存，要么就是nginx缓存很快就失效等等问题，在网上找了一遍nginx缓存优先级的文章，大家可以参考下。

架构图
client端  <——————>   nginx cache <——————>源服务器

经过大量测试发现：nginx的过期顺序是有一个优先级的。下面首先说明各个影响缓存过期的因素：

（1）inactive:在proxy_cache_path配置项中进行配置，说明某个缓存在inactive指定的时间内如果不访问，将会从缓存中删除。
（2）源服务器php页面中生成的响应头中的Expires，生成语句为：
header(“Expires: Fri, 07 Sep 2013 08:05:18 GMT”);
（3）源服务器php页面生成的max-age，生成语句为：
header(“Cache-Control: max-age=60″);
（4）nginx的配置项 proxy_cache_valid:配置nginx cache中的缓存文件的缓存时间，如果配置项为：proxy_cache_valid 200 304 2m;说明对于状态为200和304的缓存文件的缓存时间是2分钟，两分钟之后再访问该缓存文件时，文件会过期，从而去源服务器重新取数据。

其次对需要注意的一点：源服务器的expires和nginx cache的expires配置项的冲突进行说明，场景如下

（1）源服务器端有php文件ta1.php内容如下：
```php
<?php
header("Expires: Fri, 07 Sep 2013 08:05:18 GMT");
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: max-age=60");
echo "ta1";
?>
```
（2）在nginx cache服务器端的配置信息如下：
```
…….
proxy_cache_path  /data0/proxy_cache_dir  levels=1:2   keys_zone=cache_one:200m inactive=5s max_size=30g;
……..

location ~ .*\.(php|jsp|cgi)$
{
    proxy_read_timeout 10s;
    proxy_connect_timeout 10s;
    proxy_set_header Host $host;
    proxy_cache_use_stale updating;
    proxy_cache_key $host$uri$is_args$args;
    proxy_cache cache_one;
    #proxy_ignore_headers "Cache-Control";
    #proxy_hide_header "Cache-Control";
    #proxy_ignore_headers "Expires";
    #proxy_hide_header "Expires";
    proxy_hide_header "Set-Cookie";
    proxy_ignore_headers "Set-Cookie";
    #add_header Cache-Control max-age=60;
    add_header X-Cache '$upstream_cache_status from $server_addr';
    proxy_cache_valid 200 304 2m;
    #proxy_cache_valid any 0m;
    proxy_pass http:
//backend_server;
    expires 30s;
}
………….
```
从上面两项可以看出nginx cache 服务器中expires的配置是30s，该expires的值直接决定了在浏览器端看到的max-age以及expires的值。而源服务器断的代码中设置的响应头中的max-age为60，expires为Fri, 07 Sep 2013 08:05:18 GMT。这是源服务器的设置于nginx-cache的设置冲突了，那么着两个属性应该怎么设置呢？

这时client端的max-age与expires的值按照nginx cache中的expires配置项的设置，即:
```
Expires  Fri, 07 Sep 2012 08:59:16 GMT
Cache-Controlmax-age=30
```

而nginx cache端的缓存的max-age与expire的值按照源服务器上的代码的设置。即：
```
Expires  Fri, 07 Sep 2013 08:05:18 GMT
Cache-Controlmax-age=60
```

现在步入正题：

经过大量测试发现：对缓存的过期与清除起作用的因素的优先级从高到低一次为：
inactive配置项、源服务器设置的Expires、源服务器设置的Max-Age、proxy_cache_valid配置项
下面通过几个实例对这几个优先级进行说明

实例1：
服务器端php代码：
```php
<?php
header("Expires: Fri, 07 Sep 2012 08:03:18 GMT");//其实是3分钟之后
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: max-age=180");//2分钟
//header("Cache-Control: post-check=0, pre-check=0", false);
echo "ta1";
?>
```
nginx cache 配置项
inactive 4m//4分钟
proxy_cache_valid 1m//1分钟
现象：第一次访问页面ta1.php之后，各个时间的访问结果：
1分钟之后 ：HIT//这说明valid没有起作用
2分钟之后 ：HIT//这说明 源服务器设置的max-age没有起作用
3分钟之后：MISS//这说明源服务器设置的Expires起作用了
4分钟之后：MISS//这说明inactive起作用了

实例2：

服务器端php代码：
```php
<?php
header("Expires: Fri, 07 Sep 2012 08:03:18 GMT");//3分钟之后
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: max-age=180");//2分钟
//header("Cache-Control: post-check=0, pre-check=0", false);
echo "ta1";
?>
```
nginx cache 配置项
inactive 10s//10秒钟
proxy_cache_valid 1m//1分钟
现象：第一次访问页面ta1.php之后，各个时间的访问结果：
5秒后访问：HIT
10秒后访问: MISS
15秒后访问：HIT
20秒后访问:MISS
通过实例1和实例2综合分析：如果inactive已经进行了设置，则缓存的过期时间以inactive设置的值为准

实例3：

服务器端php代码：
```php
<?php
header("Expires: Fri, 07 Sep 1977 08:03:18 GMT");//直接过期
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: max-age=120");//2分钟
//header("Cache-Control: post-check=0, pre-check=0", false);
echo "ta1";
?>
```
nginx cache 配置项
inactive 4m//4分钟
proxy_cache_valid 1m//1分钟
现象：第一次访问页面ta1.php之后，各个时间的访问结果：
每隔一秒访问一次：MISS//这说明源服务器端设置的Expires屏蔽了nginx的valide和源服务器端设置的max-age的作用

实例4：
服务器端php代码：
<?php
header("Expires: Fri, 07 Sep 2012 08:03:18 GMT");//3分钟之后
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: max-age=120");//2分钟
//header("Cache-Control: post-check=0, pre-check=0", false);
echo "ta1";
?>

nginx cache 配置项
inactive 4m//4分钟
proxy_cache_valid 1m//1分钟

现象：第一次访问页面ta1.php之后，各个时间的访问结果：
1分钟之后 ：   HIT//这说明valid没有起作用，因为源服务器设置的Expires将valid的效果屏蔽了
2分钟之后 ：   HIT//这说明 源服务器设置的max-age没有起作用，因为源服务器设置的Expires将max-age屏蔽了
3分钟之后：    MISS//这说明服务器端设置的expires起作用了

通过实例2和实例3的现象说明：如果inactive设置的比较大，在inactive到期之前，如果valid、服务器端设置的expires、服务器端设置的max-age都进行了设置，则以服务器端设置的expires为准。

实例5：

服务器端php代码：
```
<?php
header("Expires: Fri, 07 Sep 2012 08:03:18 GMT");//3分钟之后
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: max-age=120");//2分钟
//header("Cache-Control: post-check=0, pre-check=0", false);
echo "ta1";
?>
```
nginx cache 配置项
inactive 4m//4分钟
#下面两行用于消除服务器端配置的Expires响应头的影响
proxy_ignore_headers “Expires”;
proxy_hide_header “Expires”;
proxy_cache_valid 1m//1分钟
现象：第一次访问页面ta1.php之后，各个时间的访问结果：
1分钟之后   HIT //这说明valid的作用已经被服务器端的max-age屏蔽
2分钟之后   MISS//服务器端设置的max-age起作用

实例6：

服务器端php代码：
```
<?php
header("Expires: Fri, 07 Sep 2012 08:03:18 GMT");//3分钟之后
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: max-age=50");//50秒钟
//header("Cache-Control: post-check=0, pre-check=0", false);
echo "ta1";
?>
```

nginx cache 配置项

inactive 4m//4分钟
#下面两行用于消除服务器端配置的Expires响应头的影响
```
proxy_ignore_headers “Expires”;
proxy_hide_header “Expires”;
proxy_cache_valid 2m//2分钟
```
现象：第一次访问页面ta1.php之后，各个时间的访问结果：

50秒钟之后 ：   MISS//这说明服务器端配置的max-age起作用
1分钟之后 ：   HIT//
100秒钟之后：   MISS//这说明服务器端设置的max-age起作用了

通过实例5和实例6的现象说明：如果inactive设置的比较大，而且在nginx配置文件中取消服务器端Expires对缓存的影响。在同时设置了proxy_cache_valid和服务器端设置了max-age响应头字段的情况下，以服务器端设置的max-age的值为标准进行缓存过期处理。

综上所述：

（1）在同时设置了源服务器端Expires、源服务器端max-age和nginx cahe端的proxy_cache_valid的情况下，以源服务器端设置的Expires的值为标准进行缓存的过期处理
（2）若在nginx中配置了相关配置项，取消原服务器端Expires对缓存的影响，在同时设置了源服务器端Expires、源服务器端max-age和nginx cahe端的proxy_cache_valid的情况下，以源服务器端max-age的值为标准进行缓存的过期处理
（3）若同时取消源服务器端Expires和源服务器端max-age对缓存的影响，则以proxy_cache_valid设置的值为标准进行缓存的过期处理
（4）   Inactive的值不受上述三个因素的影响，即第一次请求页面之后，每经过inactvie指定的时间，都要强制进行相应的缓存清理。因此inactive的优先级最高。
（5）所以对缓存过期影响的优先级进行排序为：inactvie、源服务器端Expires、源服务器端max-age、proxy_cache_valid
