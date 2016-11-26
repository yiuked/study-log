## Nginx重写规则指南


介绍`nginx`的重写模块，创建重写规则向导，便于快捷正确的创建新的重写规则，不求救于人。同时，如果想把`apache`转换成`nginx`，重写规则也是要改的咯。  
### rewrite模块介绍

`nginx`的重写模块是一个简单的正则表达式匹配与一个虚拟堆叠机结合。依赖于`PCRE`库，因此需要安装`pcre`。根据相关变量重定向和选择不同的配置，从一个`location`跳转到另一个`location`，不过这样的循环最多可以执行10次，超过后`nginx`将返回500错误。同时，重写模块包含`set`指令，来创建新的变量并设其值，这在有些情景下非常有用的，如记录条件标识、传递参数到其他`location`、记录做了什么等等。  
### rewrite模块指令
```
break
语法：break
默认值：none
使用字段：server, location, if
```
完成当前设置的重写规则，停止执行其他的重写规则。  

```
if
语法：if (condition) { … }
默认值：none
使用字段：server, location
```
注意：尽量考虑使用`trp_files`代替。  
判断的条件可以有以下值：
1. 一个变量的名称：空字符传”“或者一些“0”开始的字符串为`false`。
2. 字符串比较：使用`=`或`!=`运算符
3. 正则表达式匹配：使用`~`(区分大小写)和`~*`(不区分大小写)，取反运算`!~`和`!~*`。
4. 文件是否存在：使用`-f`和`!-f`操作符
5. 目录是否存在：使用`-d`和`!-d`操作符
7. 文件、目录、符号链接是否存在：使用`-e`和`!-e`操作符
8. 文件是否可执行：使用`-x`和`!-x`操作符

```
return
语法：return code
默认值：none
使用字段：server, location, if
```
停止处理并为客户端返回状态码。非标准的`444`状态码将关闭连接，不发送任何响应头。可以使用的状态码有：`204，400，402-406，408，410, 411, 413, 416`与`500-504`。如果状态码附带文字段落，该文本将被放置在响应主体。相反，如果状态码后面是一个`URL`，该`URL`将成为`location`头补值。没有状态码的`URL`将被视为一个`302`状态码。  

```
rewrite
语法：rewrite regex replacement flag
默认值：none
使用字段：server, location, if
```
按照相关的正则表达式与字符串修改`URI`，指令按照在配置文件中出现的顺序执行。可以在重写指令后面添加标记。   
注意：如果替换的字符串以`http://开头`，请求将被重定向，并且不再执行多余的`rewrite`指令。  
尾部的标记(`flag`)可以是以下的值：  
`last` – 停止处理重写模块指令，之后搜索`location`与更改后的`URI`匹配。
`break` – 完成重写指令。
`redirect` – 返回`302`临时重定向，如果替换字段用`http://开头则被使用`。
`permanent` – 返回`301`永久重定向。

```
rewrite_log
语法：rewrite_log on | off
默认值：rewrite_log off
使用字段：server, location, if
```
变量：无
启用时将在`error log`中记录`notice`级别的重写日志。

```
set
语法：set variable value
默认值：none
使用字段：server, location, if
```
为给定的变量设置一个特定值。

```
uninitialized_variable_warn
语法：uninitialized_variable_warn on|off
默认值：uninitialized_variable_warn on
使用字段：http, server, location, if
```
控制是否记录未初始化变量的警告信息。

### 重写规则组成部分

##### 任何重写规则的第一部分都是一个正则表达式  
可以使用括号来捕获，后续可以根据位置来将其引用，位置变量值取决于捕获正则表达式中的顺序，`$1`引用第一个括号中的值，`$2`引用第二个括号中的值，以此类推。如：
```
^/images/([a-z]{2})/([a-z0-9]{5})/(.*)\.(png|jpg|gif)$
```
`$1`是两个小写字母组成的字符串，`$2`是由小写字母和0到9的数字组成的5个字符的字符串，`$3`将是个文件名，`$4`是`png、jpg、gif`中的其中一个。  

##### 重写规则的第二部分是URI
请求被改写。该`URI`可能包含正则表达式中的捕获的位置参数或这个级别下的`nginx`任何配置变量。如：
```
/data?file=$3.$4
```
如果这个`URI`不匹配`nginx`配置的任何`location`，那么将给客户端返回`301`(永久重定向)或`302`(临时重定向)的状态码来表示重定向类型。该状态码可以通过第三个参数来明确指定。

##### 重写规则的第三部分
第三部分也就是尾部的标记(`flag`)。 `last`标记将导致重写后的`URI`搜索匹配`nginx`的其他`location`，最多可循环10次。如：
```
rewrite '^/images/([a-z]{2})/([a-z0-9]{5})/(.*)\.(png|jpg|gif)$' /data?file=$3.$4 last;
```
`break`指令可以当做自身指令。如：
```
if ($bwhog) {
    limit_rate 300k;
    break;
}
```
另一个停止重写模块处理指令是`return`， 来控制主`HTTP`模块处理请求。 这意味着，`nginx`直接返回信息给客户端，与`error_page`结合为客户端呈现格式化的`HTML`页面或激活不同的模块来完成请求。  
如果状态码附带文字段落，该文本将被放置在响应主体。相反，如果状态码后面是一个`URL`，该`URL`将成为`location`头补值。没有状态码的`URL`将被视为一个`302`状态码。如：  
```
location = /image404.html {
    return 404 "image not found\n";
}
```
### 实例
```
http {
    # 定义image日志格式
    log_format imagelog '[$time_local] ' $image_file ' ' $image_type ' ' $body_bytes_sent ' ' $status;
    # 开启重写日志
    rewrite_log on;

    server {
        root /home/www;

        location / {
                # 重写规则信息
                error_log logs/rewrite.log notice;
                # 注意这里要用‘’单引号引起来，避免{}
                rewrite '^/images/([a-z]{2})/([a-z0-9]{5})/(.*)\.(png|jpg|gif)$' /data?file=$3.$4;
                # 注意不能在上面这条规则后面加上“last”参数，否则下面的set指令不会执行
                set $image_file $3;
                set $image_type $4;
        }

        location /data {
                # 指定针对图片的日志格式，来分析图片类型和大小
                access_log logs/images.log mian;
                root /data/images;
                # 应用前面定义的变量。判断首先文件在不在，不在再判断目录在不在，如果还不在就跳转到最后一个url里
                try_files /$arg_file /image404.html;
        }
        location = /image404.html {
                # 图片不存在返回特定的信息
                return 404 "image not found\n";
        }
}
```

### 创建新的重新规则

在接到要创建新的重写规则时，要弄清楚需求是什么样的，再决定怎么做。毕竟重写也是耗资源的有效率之分的。 下面的这些问题有些帮助的：
1. 你的`URL`的模式是什么样的?
2. 是否有一个以上的方法来实现？
3. 是否需要捕获`URL`部分作为变量？
4. 重定向到另一个`web`上可以看到我的规则？
5. 是否要替换查询的字符串参数？

检查网站或应用程序布局，清楚`URL`模式。啰嗦一句：我一而再再而三的强调，运维不能与开发脱节，运维要参与到开发当中。如果有不止一种方法实现，创建一个永久重定向。同时，定义一个重写规范，来使网址清洁，还可以帮助网站更容易被找到。  

实例1. 要将home目录重定向到主页面上，目录结构如下：
```
/
/home
/home/
/home/index
/home/index/
/index
/index.php
/index.php/
```
重写规则如下：
```
rewrite ^/(home(/index)?|index(\.php)?)/?$ $scheme:
//$host/ permanent;
```
指定`$scheme`和`$host`变量，因为要做一个永久重定向并希望`nginx`使用相同的参数来构造`URL`。

实例2. 如果想分别记录各个部分的`URL`，可以使用正则表达式来捕获`URI`，然后，给变量分配指定位置变量，见上面的实例。

实例3. 当重写规则导致内部重定向或指示客户端调用该规则本身被定义的`location`时，必须采取特殊的动作来避免重写循环。如：在`server`配置段定义了一条规则带上`last`标志，在引用`location`时，必须使用`break`标志。  
```
server {
    rewrite ^(/images)/(.*)\.(png|jpg|gif)$ $1/$3/$2.$3 last;
    location /images/ {
        rewrite ^(/images)/(.*)\.(png|jpg|gif)$ $1/$3/$2.$3 break;
    }
}
```
实例4. 作为重写规则的一部分，传递新的查询字符串参数是使用重写规则的目标之一。 如：  
```
rewrite ^/images/(.*)_(\d+)x(\d+)\.(png|jpg|gif)$ /resizer/$1.$4?width=$2&height=$3? last;
```
`nginx`重写规则说起来挺简单的，做起来就难，重点在于正则表达式，同时，还需要考虑到`nginx`执行顺序。  
