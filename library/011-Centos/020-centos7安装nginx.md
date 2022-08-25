**1、添加CentOS 7 Nginx yum资源库**

[root@localhost ~]# rpm -Uvh  http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm

**2、安装nginx**

[root@localhost ~]# yum -y install nginx   //安装nginx

**3、启动nginx**

[root@localhost ~]# systemctl start nginx   //启动nginx