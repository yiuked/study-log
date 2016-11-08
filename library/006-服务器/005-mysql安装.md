#### 检测系统是否自带安装mysql
```
yum list installed | grep mysql
```
#### 删除系统自带的mysql及其依赖
```
yum -y remove mysql-libs.x86_64
```

#### 给CentOS添加rpm源，并且选择较新的源
```
# wget dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm
# yum localinstall mysql-community-release-el6-5.noarch.rpm
# yum repolist all | grep mysql
# yum-config-manager --disable mysql55-community
# yum-config-manager --disable mysql56-community
# yum-config-manager --enable mysql57-community-dmr
# yum repolist enabled | grep mysql
```

#### 安装mysql 服务器
```
yum install mysql-community-server
```

#### 启动mysql
```
service mysqld start
```

#### 查看mysql是否自启动,并且设置开启自启动
```
chkconfig --list | grep mysqld
chkconfig mysqld on
```

#### mysql 5.7设置密码
修改`MySQL`的配置文件（默认为`/etc/my.cnf`）,在`[mysqld]`下添加一行
```
skip-grant-tables
```
然后重新启动`Mysql`  
```
service mysqld restart后，即可直接用mysql进入
mysql> update mysql.user set authentication_string=password('root') where user='root' and Host = 'localhost';
mysql> flush privileges;
mysql> quit;
```
将`/etc/my.cnf`文件还原，重新启动。
```
mysql:service mysql restart
```
这个时候可以使用`mysql -u root -p`进入了  


#### mysql.sock文件丢失导致mysql自动死机问题，
查看`/var/log/mysql.log` 日志文件，看是否是由于内存不足的原因导致。  
如果是，可以设置(默认为 `128M`)  
```
join_buffer_size = 32M
```

#### php连接mysql失败问题
错误提示:  
```
SQLSTATE[HY000] [2002] No such file or directory
```
修改`php.ini`文件  
```
default_socket_timeout = 60
pdo_mysql.default_socket=/var/lib/mysql/mysqld.sock
mysql.default_socket =/var/lib/mysql/mysqld.sock
mysqli.default_socket =/var/lib/mysql/mysqld.sock
```
