## Mac下安装PHP扩展
通过`brew`已经安装好了`php`,查看对应的版本号：
```
$ php -v
PHP 7.1.7 (cli) (built: Jul 15 2017 18:08:09) ( NTS )
Copyright (c) 1997-2017 The PHP Group
Zend Engine v3.1.0, Copyright (c) 1998-2017 Zend Technologies
```
通过`php.net`可能已经找不到对应的版本号源文件，则可前往`github`进行下载：
```
https://github.com/php/php-src/tags
```
下载解压后，进入对应的扩展目录，以安装`pcntl`为例：
```
$ cd ext/pcntl
$ sudo phpize
Password:
grep: /usr/include/php/main/php.h: No such file or directory
grep: /usr/include/php/Zend/zend_modules.h: No such file or directory
grep: /usr/include/php/Zend/zend_extensions.h: No such file or directory
Configuring for:
PHP Api Version:        
Zend Module Api No:     
Zend Extension Api No:
```
结果找不到对应的`php`头文件，通过更新,`xcode`建立关系（这一步有点不太明白，总之执行了，
环境就都好了）：
```
xcode-select --install
```
再次执行`phpize`:
```
$ phpize
Configuring for:
PHP Api Version:         20160303
Zend Module Api No:      20160303
Zend Extension Api No:   320160303
$ ./Configuation
....
$ make && make install
cp: /usr/lib/php/extensions/no-debug-non-zts-20160303/#INST@54285#: Operation not permitted
make: *** [install-modules] Error 1
```
这里可能会报以上错误，`mac`各种权限总是太麻烦了。索性不再考虑复制到以上目录。
```
$ sudo mkdir /usr/local/php-ext
$ sudo cp ./modules/pcntl.so /usr/local/php-ext/pcntl.so
$ sudo /etc/php.ini.dufualt /etc/php.ini # etc目录下可能不存在php.ini
$ vim /etc/php.ini
```
新增一行：
```
extension=/usr/local/php-ext/pcntl.so
```
检测是否加载成功：
```
$ php -m|grep pcntl
pcntl
```
有输出，则表明已安装成功。

### 延伸扩展
`extension`意为基于`php`引擎的扩展  
`zend_extension`意为基于`zend`引擎的扩展  
>注：`php`是基于`zend`引擎的.  

不同的扩展安装后，在`php.ini`里是用`extension`还是`zend_extension`，是取决于该扩展，有的扩展可能只能用`zend_extension`，如`xdebug`，
也有的扩展可以用`extension`或`zend_extension`，如`mmcache`。  

>注：上面的结论不保证准确。`zend_extension`加载`php`扩展时需用全路径，而`extension`加载时可以用相对`extension_dir`的路径。  

根据 PHP 版本，zend_extension 指令可以是以下之一：
```
zend_extension (non ZTS, non debug build)
zend_extension_ts ( ZTS, non debug build)
zend_extension_debug (non ZTS, debug build)
zend_extension_debug_ts ( ZTS, debug build)

ZTS：ZEND Thread Safety
```
参考地址：http://blog.sina.com.cn/s/blog_788fd8560100vx03.html
