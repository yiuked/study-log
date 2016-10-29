以往的`lamp`网站向着`lnmp`发展, 笔者工作环境使用`lnmp`多年, 在这里很高兴和大家分享一下多年的`lnmp`网站的`php`安全配置，至于`lamp`安全后续与大家分享，其实内容上八成相同，这边着重讲`php`安全配置，看内容.  
#### 使用`open_basedir`限制虚拟主机跨目录访问  
```
[HOST=www.test.com]
open_basedir=/data/site/www.test.com/:/tmp/
```
如上配置的意思是`www.test.com`下的`php`程序被限制在`open_basedir`配置的两个目录下, 不可以访问到其他目录。如果没有做以上的配置，那么`test.test.com`与`www.test.com`的程序可以互相访问.  
如果其中一个站点有漏洞被黑客植入了`webshell`，那么他可以通过这个站点拿下同一台服务器的其他站点，最后挂木马.  

注意：目录最后一定要加上`/.` 比如你写`/tmp`，你的站点同时存在`/tmp123`等等以`/tmp`开头的目录，那么黑客也可以访问到这些目录，另外, `php5.3`以上支持这个写法，`5.2`不支持.  

#### 禁用不安全`PHP`函数  
```
disable_functions = show_source,system,shell_exec,passthru,exec,popen,proc_open,proc_get_status,phpinfo
```
禁止`php`执行以上`php`函数,以上`php`程序可以执行`linux`命令, 比如可以执行`ping、netstat、mysql`等等.如果你的系统有提权`bug`,后果你懂得.  

#### 关注软件安全资讯  
积极关注`linux`内核、`php`安全等信息并及时采取错误  

#### `php`用户只读  
这个方法是我最推崇的方法，但是执行之前一定要和`php`工程师商量. 为什么？例如站点`www.test.com`根目录用户与组为`nobody`，而运行`php`的用户和组为`phpuser`。目录权限为`755`，文件权限为`644`. 如此，`php`为只读，无法写入任何文件到站点目录下。也就是说用户不能上传文件，即使有漏洞, 黑客也传不了后门, 更不可能挂木马.  这么干之前告知程序员将文件缓存改为`nosql`内存缓存（例如`memcached、redis`等），上传的文件通过接口传到其他服务器（静态服务器）。

备注：程序生成本地缓存是个非常糟糕的习惯，使用文件缓存速度缓慢、浪费磁盘空间、最重要一点是一般情况下服务器无法横向扩展.  

#### 关闭`php`错误日志  
```
display_errors = On
```
改为
```
display_errors = Off
```
程序一旦出现错误，详细错误信息便立刻展示到用户眼前，其中包含路径、有的甚至是数据库账号密码. 注入渗透密码基本上都是通过这个报错来猜取。生产环境上强烈关闭它

#### `php`上传分离  
将文件上传到远程服务器，例如`nfs`等。当然也可以调用你们写好的`php`接口. 即使有上传漏洞，那么文件也被传到了静态服务器上。木马等文件根本无法执行.

举个例子：  
```
php站点www.test.com，目录/data/site/www.test.com
静态文件站点static.test.com，目录/data/site/static.test.com
```
文件直接被传到了`/data/site/static.test.com`，上传的文件无法通过`www.test.com`来访问，只能使用`static.test.com`访问，但是`static.test.com`不支持`php`.

#### 关闭`php`信息
```
expose_php = On
```
改为
```
expose_php = Off
```

不轻易透露自己`php`版本信息，防止黑客针对这个版本的`php`发动攻击.

#### 禁止动态加载链接库
```
disable_dl = On;
```
改为
```
enable_dl = Off;
```

#### 禁用打开远程`url`
```
allow_url_fopen = On
```
改为
```
allow_url_fopen = Off
```
其实这点算不上真正的安全, 并不会导致`web`被入侵等问题,但是这个非常影响性能, 笔者认为它属于狭义的安全问题.

以下方法将无法获取远程url内容
```php
$data = file_get_contents("http://www.baidu.com/")；
```

以下方法可以获取本地文件内容  
```
$data = file_get_contents("1.txt");
```

如果你的站点访问量不大、数据库也运行良好，但是`web`服务器负载出奇的高，请你直接检查下是否有这个方法。笔者遇到过太多这个问题，目前生产环境已全线禁用，如果`php`工程师需要获取远程`web`的内容，建议他们使用`curl`.

`php curl`如何使用请查看我之前的文章《`PHP`使用`curl`替代`file_get_contents`》，以及`php`下`curl`与`file_get_contents`性能对比.  
#### 结束
今天`lnmp`站点的`php`安全暂时讲到这里,有问题后续将继续补充.  
