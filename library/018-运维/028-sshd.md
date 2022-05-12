### ssh反向链接
本地机 192.168.1.135 远程机 example.com,要实现远程机访问本地机

1. 在本地机执行以下代码:
```
ssh -CqTfnN -R :11111:localhost:22 root@example.com
```
> 11111 为端口号
> root@example.com 远程机信息s 
> 查看启动状态
> ```
> ps axu |grep ssh   
> ssh -NfR 2222:localhost:22 root@example.com
> ```

2. 远程机访问本地机:
```
ssh -p 2222 httpd@localhost
```
> httpd 为本地机的用户名