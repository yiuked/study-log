### 关于CGI(Common Gateway Interface) 公共网关接口
`CGI` 是一种协议，用 `C` 语言写 `web` 就是通过实现 `CGI` 协议的方式。

### 关于Fast CGI
`Fast CGI` 是一种更高级的 `cgi` 协议，`php-fpm` 和 `php-cgi` 都是实现了 `fast-cgi` 协议的应用程序。
你的服务器可以选择使用 php-cgi( 启动命令` php-cgi -b 127.0.0.1:9000`) ，也可以选择使用 php-fpm(启动命令`php-fpm -D`)，甚至两个一起用都可以（端口不能用一个）。
所以 php-cgi 和 php-fpm 其实就像 QQ 和微信一样，都是腾讯的 IM，只不过微信体验更好一些。

### FPM(Fastcgi process manager) FastCGI 进程管理器
也就是说`PHP-FPM`即：PHP fastcgi process manager，是PHP用于管理fastcgi进程的一个管理器。
