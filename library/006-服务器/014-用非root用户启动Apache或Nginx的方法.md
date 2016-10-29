众所周知，`apache`的`80`端口为系统保留端口，如果通过其他非`root`用户启动，会报错如下：  
```
(13)Permission denied: make_sock: could not bind to address [::]:80
(13)Permission denied: make_sock: could not bind to address 0.0.0.0:80
no listening sockets available, shutting down
Unable to open logs
```
因为普通用户只能用`1024`以上的端口，`1024`以内的端口只能由`root`用户使用。  
但是为了避免每次启动都通过root用户，可以通过set UID的方式来解决此问题。  

一次性进行如下操作即可完成。  
在`root`用户环境中做如下操作  
```
cd ……/apache/bin
chown root httpd
chmod u+s httpd
```
再
```
su - USERNAME
```
到普通用户下，通过
```
……/apache/bin/apachectl start
```
即可

为何不`chmod u+s apachectl`呢？
因为`set UID`这种方式只针对二进制文件有效，而`tail`一下`apachectl`发现：  
`apachectl`是一个脚本文件，仔细查阅发现有如下一句  
```
HTTPD='/home/……/apache/bin/httpd'
```
得出结论：`apachectl`脚本是通过启动`httpd`文件来启动整个`httpd`服务。  
再次`cat httpd`，出现各种不可读乱码，`ctrl+c`结束输出之后，断定`httpd`为二进制文件。  
最后`chmod u+s httpd`即可，当然得保证`httpd`的所属者为`root`用户，如果不是，执行：  
```
chown root httpd
```
即可。

同样，`nginx`启动也如此，用`root`用户进入`....nginx/sbin`  
然后  
```
chown root nginx
chmod u+s nginx
```
然后通过普通用户就可以启动了。  
再同样，`tomcat`也如此。  
当然，修改默认端口到大于`1024`也是可以的。  
