`nginx`文件非常小但是性能非常的高效,这方面完胜`apache`,`nginx`文件小的一个原因之一是`nginx`自带的功能相对较少,
好在`nginx`允许第三方模块,第三方模块使得`nginx`越发的强大. 在安装模块方面,`nginx`显得没有`apache`安装模块方便，当然也没有`php`安装扩展方便.在原生的`nginx`,他不可以动态加载模块,所以当你安装第三方模块的时候需要覆盖`nginx`文件.接下来看看如何安装nginx第三模块吧.  


nginx第三方模块安装方法：
```
./configure --prefix=/你的安装目录  --add-module=/第三方模块目录
```

以安装`pagespeed`模块实例  
在未安装`nginx`的情况下安装`nginx`第三方模块  
```
# ./configure --prefix=/usr/local/nginx-1.4.1 \
--with-http_stub_status_module \
--with-http_ssl_module --with-http_realip_module \
--with-http_image_filter_module \
--add-module=../ngx_pagespeed-master --add-module=/第三方模块目录
# make
# make install
# /usr/local/nginx-1.4.1/sbin/nginx
```
在已安装`nginx`情况下安装`nginx`模块  
```
# ./configure --prefix=/usr/local/nginx-1.4.1 \
 --with-http_stub_status_module \
 --with-http_ssl_module --with-http_realip_module \
 --with-http_image_filter_module \
 --add-module=../ngx_pagespeed-master
# make
# /usr/local/nginx-1.4.1/sbin/nginx -s stop
# cp objs/nginx /usr/local/nginx/sbin/nginx
# /usr/local/nginx-1.4.1/sbin/nginx
```
相比之下仅仅多了一步覆盖`nginx`文件.    

总结,安装`nginx`安装第三方模块实际上是使用`–add-module`重新安装一次`nginx`，不要`make install`而是直接把编译目录下`objs/nginx`文件直接覆盖老的`nginx`文件.如果你需要安装多个`nginx`第三方模块,你只需要多指定几个相应的`–add-module`即可.    

备注：重新编译的时候，记得一定要把以前编译过的模块一同加到`configure`参数里面.  
`nginx`提供了非常多的`nginx`第三方模块提供安装,地址http://wiki.nginx.org/3rdPartyModules
