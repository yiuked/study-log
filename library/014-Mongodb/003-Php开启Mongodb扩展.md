## Php在Windows下开启MongoDB扩展

`PHP`连接`mongo`有两种方式，一种是`mongo`,一种为`mongodb`
### 一、环境
```
WampServer Version 2.5 64位版本
Apache 2.4.9
PHP 5.5.12
```

### 二、安装
#### 2.1 mongo扩展
下载地址：http://pecl.php.net/package/mongo
下载完成后，放入`php/ext`目录,并修改`php.ini`文件，加入
```
extension=php_mongo.dll
```
`mongo`使用文档可参照：
http://php.net/manual/zh/book.mongo.php


#### 2.2 php_mongodb扩展
>`php_mongodb`仅支持php5.4(5.4才开始支持命名空间)及以上的版本  

下载地址：http://pecl.php.net/package/mongodb/
下载完成后，放入`php/ext`目录,并修改`php.ini`文件，加入
```
extension=php_mongodb.dll
```
`mongo`使用文档可参照：
http://php.net/manual/zh/set.mongodb.php


### 三、使用
#### 3.1 开通`mongo`扩展，以`mongo`方式连接`mongodb`：
```php
<?php
$m = new MongoClient("mongodb://zsjr:zsjr@localhost:27017/zsjr");
$db = $m->selectDB('zsjr');
$users = $db->selectCollection('users');
$result = $users->find();
var_dump(iterator_to_array($result));
```

#### 3.2 开通`mongodb`扩展，以`mongodb`方式连接`mongodb`：
```php
<?php
require 'vendor/autoload.php';
$m = new MongoDB\Client("mongodb://zsjr:zsjr@localhost:27017/zsjr");
$users = $m->zsjr->users;
$result = $users->find();
var_dump($result);
```
