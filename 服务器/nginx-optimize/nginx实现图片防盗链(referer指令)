前几天讲了《nginx下载防盗链》，今天继续说下图片防盗链. 他们两个使用的指令不同，前者使用secure link,并且需要程序配合,但是效果非常好;后者不需要程序配合,根据图片来源来实现,但是只能先限制基本的图片盗用,无法防止图片采集.
nginx referer指令简介

nginx模块ngx_http_referer_module通常用于阻挡来源非法的域名请求.我们应该牢记,伪装Referer头部是非常简单的事情，所以这个模块只能用于阻止大部分非法请求.我们应该记住，有些合法的请求是不会带referer来源头部的,所以有时候不要拒绝来源头部（referer）为空的请求.
图片防盗链配置
location ~* \.(gif|jpg|png|bmp)$ {
    valid_referers none blocked *.ttlsa.com server_names ~\.google\. ~\.baidu\.;
    if ($invalid_referer) {
        return 403;
        
#rewrite ^/ http://www.ttlsa.com/403.jpg;
    }
}

以上所有来至ttlsa.com和域名中包含google和baidu的站点都可以访问到当前站点的图片,如果来源域名不在这个列表中，那么$invalid_referer等于1，在if语句中返回一个403给用户，这样用户便会看到一个403的页面,如果使用下面的rewrite，那么盗链的图片都会显示403.jpg。如果用户直接在浏览器输入你的图片地址,那么图片显示正常，因为它符合none这个规则.
nginx防盗链指令

语法: referer_hash_bucket_size size;
默认值: referer_hash_bucket_size 64;
配置段: server, location
这个指令在nginx 1.0.5中开始出现.
Sets the bucket size for the valid referers hash tables. The details of setting up hash tables are provided in a separate document.

语法:     referer_hash_max_size size;
默认值:     referer_hash_max_size 2048;
配置段:     server, location
这个指令在nginx 1.0.5中开始出现.
Sets the maximum size of the valid referers hash tables. The details of setting up hash tables are provided in a separate document.

语法: valid_referers none | blocked | server_names | string …;
默认值: —
配置段: server, location
指定合法的来源’referer’, 他决定了内置变量$invalid_referer的值，如果referer头部包含在这个合法网址里面，这个变量被设置为0，否则设置为1.记住，不区分大小写的.
参数说明

none
“Referer” 来源头部为空的情况
blocked
“Referer”来源头部不为空，但是里面的值被代理或者防火墙删除了，这些值都不以http://或者https://开头.
server_names
“Referer”来源头部包含当前的server_names（当前域名）
arbitrary string
任意字符串,定义服务器名或者可选的URI前缀.主机名可以使用*开头或者结尾，在检测来源头部这个过程中，来源域名中的主机端口将会被忽略掉
regular expression
正则表达式,~表示排除https://或http://开头的字符串.
最后

图片使用来源头部做防盗链是最合理的. 简单、实用。但是没有办法防采集。如果想做文件的防盗链请参考前面章节讲到的使用secure link文件防盗链文章.