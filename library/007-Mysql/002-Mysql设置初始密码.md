刚安装或者遗忘`Mysql`时，如何重置`Mysql`密码呢!  
这个我们用到
```
mysqld_safe --skip-grant-tables &
```
顾名思义，就是在启动`mysql`时不启动`grant-tables`，授权表,这样，我们就能在不通过登录验证的情况下，登录`Mysql`进而重置密码。  
在使用这个命令之前，我们必须关闭正在运行`Mysql`服务：  
```
service mysqld stop
```
停止服务以后，即可通过`mysqld_safe`来重新启用`mysql`  
```
/usr/bin/mysqld_safe --skip-grant-tables &
```
如果提示`mysqld_safe`找不到，可以通过  
```
whereis mysqld_safe
```
来进行查找.  

以上命令中 `&` 表示在后台运行，但有时可能`mysql`并没有转到后台，此时可以通过 `CTRL+C`退出  
然后再次登录，无需输入密码:
```
$mysql -uroot
>use msyql;
mysql>update user set password=password('123456') where user='root';
mysql>flush privileges;
mysql>exit;
```
然后重新启动`Mysql`则可.  
