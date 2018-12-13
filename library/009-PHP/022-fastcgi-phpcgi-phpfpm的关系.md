### 关于CGI(Common Gateway Interface) 公共网关接口
`CGI` 是一种协议，用 `C` 语言写 `web` 就是通过实现 `CGI` 协议的方式,
`WEB`服务器在接收到请求后，执行步骤是：
```
1.WEB服务器在接收到请求后，如果请求的是静态资源，则返回静态资源。
2.WEB服务器在接收到请求后，如果请求的是动态资源，先要创建cgi的子进程，激活一个CGI进程。
3.如果是php请求，这个CGI进程就是php解析器。
4.php解析器会去解析php.ini配置文件，初始化执行环境。
5.然后执行请求的文件，返回处理结果，并退出进程。
6.WEB服务器再将结果返回给浏览器。
```
以上的3-5的过程就是`CGI`需要处理的任务。

那么问题来了。服务器每接受到一次动态资源的请求，服务器就要去创建一个`CGI`进程，加载`php`配置文件，初始化执行环境。
当用户请求量大的时候，会大量挤占系统资源。这就是为什么要出现`fastCGI`。

### 关于Fast CGI
`Fast CGI` 是一种更高级的 `CGI` 协议。那么`Fast CGI`是怎么做的呢？
```
1.fastcgi会先启一个master，解析配置文件，初始化执行环境.
2.然后再启动多个worker。 当请求过来时，master会传递给一个worker.
3.然后立即可以接受下一个请求。这样就避免了重复的劳动，效率自然是高。
4.当worker不够用时，master可以根据配置预先启动几个worker等着；
5.当空闲worker太多时，也会停掉一些，这样就提高了性能，也节约了资源。
```
这就是`Fast CGI`的对进程的管理。
> `php-fpm` 和 `php-cgi` 都是实现了 `Fast CGI` 协议的应用程序。

### 关于PHP CGI
`PHP-CGI`是`PHP`自带的`FastCGI`管理器。

### 关于FPM(Fastcgi process manager) FastCGI 进程管理器
也就是说`PHP-FPM`即：`PHP fastcgi process manager`，是`PHP`用于管理`fastcgi`进程的一个管理器。

因为`Fast CGI`已经事先把php的配置文件加载到执行环境中。那么我们更改了配置文件后，在重启服务器时，就必须把现有的所有`worker`进程全部杀死，然后重新启动服务。
这样服务器就不能平滑重启了，`php-fpm`就是为了解决这个问题。`php-fpm`对此的处理机制是新的`worker`用新的配置，已经存在的`worker`处理完手上的活就可以歇着了，通过这种机制来平滑过度。


* 引用[https://segmentfault.com/a/1190000009863108]
