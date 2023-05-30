轻量级服务没有安装centos-release，需要手动安装，下载地址
http://mirror.centos.org/centos/7/os/x86_64/Packages/

如centos 7.9 
```shell
wget http://mirror.centos.org/centos/7/os/x86_64/Packages/centos-release-7-9.2009.0.el7.centos.x86_64.rpm
```


下载完了以后执行
```shell
rpm -ivh centos-release-7-9.2009.0.el7.centos.x86_64.rpm
```