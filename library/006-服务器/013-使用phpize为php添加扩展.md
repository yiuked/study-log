以`php7`下添加`mcrypt`为列，  
官方提供的`php`安装包内已包含`mcrypt`  
```
#cd /usr/php-7.0.0/ext/mcrypt
#/usr/local/php/bin/phpize
#./configure --with-php-config=/usr/local/php/bin/php-config
#make && make install
```
给你的`php.ini`添加一条`extension=mcrypt.so`
