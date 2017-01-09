## Reids对PHP的支持

扩展下载,一定要下载正确。
http://windows.php.net/downloads/pecl/releases/


我使用的环境是php5.5.12 x86 ts版本
http://windows.php.net/downloads/pecl/releases/redis/2.2.7/php_redis-2.2.7-5.5-ts-vc11-x86.zip



下载完后，复制到php的ext目录，修改php.ini文件增加
```
extension=php_redis.dll
```

检测是否适用于当前版本，可以切换到php目录，
```
php -v
```
如果版本不匹配，通常是无法正常运行php的，如果启动正常
```
php --re redis
```
可以查看可使用的扩展函数
