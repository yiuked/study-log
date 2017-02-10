## Laravel中的env

`env`是`Laravel`中的一个辅助函数，以下是官方的文档的备注:

```
#`env` 函数获取一个环境变量的值或者返回默认值  
$env = env('APP_ENV');

// 如果变量不存在，返回默认值
$env = env('APP_ENV', 'production');
```

`env`函数定义中以下文件中:  
```
\vendor\laravel\framework\src\Illuminate\Foundation\helpers.php
```
#### php内置函数getenv
从官方的文档，或者`env`函数定义的源码中，能够了解到，配置上是调用`php`的系统函数`getenv`，
并对`getenv`后的结果进行进一步的处理.  
那么`getenv`函数是做什么的，关于 [getenv](https://secure.php.net/manual/en/function.getenv.php "getenv")。

`getenv`函数用于从环境变现中获取指定`key`的值。

#### 环境变量是哪来的
在`Laravel`中，使用`env`函数的地方主要集中在`config`目录下,如`app.php`中
```
'env' => env('APP_ENV', 'production'),
'debug' => env('APP_DEBUG', true),
```
`database.php`中
```
'mysql' => [
    'driver'    => 'mysql',
    'host'      => env('DB_HOST', 'localhost'),
    'database'  => env('DB_DATABASE', 'test'),
    'username'  => env('DB_USERNAME', 'root'),
    'password'  => env('DB_PASSWORD', 'root'),
    'charset'   => 'utf8',
    'collation' => 'utf8_unicode_ci',
    'prefix'    => '',
    'strict'    => false,
    'engine'    => null,
],
```
通过`phpinfo()`输出结果中查找`Environment`，
```
Variable	Value
HTTP_HOST 	127.0.0.1
HTTP_USER_AGENT 	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0
HTTP_ACCEPT 	text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
HTTP_ACCEPT_LANGUAGE 	zh-CN
HTTP_ACCEPT_ENCODING 	gzip, deflate
...
```
可以得知，在我们的`web`服务器中，
其实并没有以上的这些`key`值,那么以上的环境变量是何时加载，何时赋予的初值呢？
在`Http`与`Console`的`Kernel.php`文件中
```
\vendor\laravel\framework\src\Illuminate\Foundation\Console\Kernel.php
\vendor\laravel\framework\src\Illuminate\Foundation\Http\Kernel.php
```
都有以一段
```
protected $bootstrappers = [
    //初始环境变量
    'Illuminate\Foundation\Bootstrap\DetectEnvironment',
    //加载config目录下的配置文件
    'Illuminate\Foundation\Bootstrap\LoadConfiguration',
    'Illuminate\Foundation\Bootstrap\ConfigureLogging',
    'Illuminate\Foundation\Bootstrap\HandleExceptions',
    'Illuminate\Foundation\Bootstrap\RegisterFacades',
    'Illuminate\Foundation\Bootstrap\RegisterProviders',
    'Illuminate\Foundation\Bootstrap\BootProviders',
];
```
这个数组定义启动引导过程的优化级，其中第一项就是初始环境变量,
这些引导文件会在入口文件中的以下方法中，被依次调用执行。
```
$response = $kernel->handle(
    $request = Illuminate\Http\Request::capture()
);
```
到此，我们知道了，引导过程，确实对环境变量进行了一次初始化，那么，`Laravel`是通过什么加进行环境变量初始化呢？

#### PHP dotenv
通过上一流程，我们得知，`Laravel`通过初始引导加载环境变量，其中调用了以下引导文件
```
\vendor\laravel\framework\src\Illuminate\Foundation\Bootstrap\DetectEnvironment.php
```
从该文件中，可以得知，`Laravel`引入了一个组件`PHP dotenv`，至此，所有的谜底都将在此被解开  
`PHP dotenv`的`github`地址:
https://github.com/vlucas/phpdotenv  

### 总结
至此，我们对`env`、`getenv`有了一定的理解，也知道`Laravel`通过`PHP dotenv`来加载环境变量配置文件。  
`Laravel`默认的情况下，在网站根目录下有一个`.env`文件，或者`.env.example`文件，`Laravel`默认的配置文件为`.env`
```
# From \vendor\laravel\framework\src\Illuminate\Foundation\Application.php
/**
 * The environment file to load during bootstrapping.
 *
 * @var string
 */
protected $environmentFile = '.env';
```
当我们的服务器环境变量中，不存在`APP_ENV`时，将自动加载根目录下的`.env`文件,当环境变量中存在`APP_ENV`时，
将加载`.env.[APP_ENV的值]`。  

那么，我们如何在本地与服务器配置不同的`.env`文件呢?  
如，在本地时，我需要加载`.env.local`文件，在服务器时，需要加载`.env.production`。
在`Apache`，可以通过以下配置：
```
<VirtualHost *:8000>
ServerAdmin webmaster@aa
...
SetEnv APP_ENV production
<Directory />
  ...
</Directory>
</VirtualHost>
```
在`Nginx`中，可能通过以下配置:
```
fastcgi_param APP_ENV production;
```
配置完成后，重启服务器，可以在`phpinfo()`中的`Environment`找到`APP_ENV`则说明配置成功了.
