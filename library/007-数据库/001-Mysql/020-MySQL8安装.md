#### 下载

https://dev.mysql.com/downloads/mysql/

####　初始化

```
mysqld --initialize --console
```

#### Windows

注册服务

```
mysqld --install  mysql8
```

> 会生成初始密码,数据存放路径,可以通过my.ini指定路径,如果需要重新初始化,需要删除data目录.

启动服务

```
net start mysql8
```

修改密码

```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
```

采用第三方工具如Navicat连接MySQL时,可能会报: Client does not support authentication ...,无法正常连接,这时候需要连接上

这是由于MySQL8默认采用的是`caching_sha2_password`连接方式,而我们采用的是`mysql_native_password`连接,因此需要更新连接方式,通过mysql cli连接上MySQL:

```
mysql> USE mysql;
mysql> select Host,User,plugin from user where User='root';
+-----------+------+-----------------------+
| Host      | User | plugin                |
+-----------+------+-----------------------+
| %         | root | caching_sha2_password |
| localhost | root | caching_sha2_password |
+-----------+------+-----------------------+
2 rows in set (0.00 sec)

```

> 可以看到其中的plugin的值为caching_sha2_password,
>
> 通过`ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';`可以调整过来.注意需要把host等于`%`与`localhost`都改过来.改完以后的结果为:
>
> ```
> mysql> select Host,User,plugin from user where User='root';
> +-----------+------+-----------------------+
> | Host      | User | plugin                |
> +-----------+------+-----------------------+
> | %         | root | mysql_native_password |
> | localhost | root | mysql_native_password |
> +-----------+------+-----------------------+
> 2 rows in set (0.00 sec)
> ```
>
> 改完以后,可能需要执行以下命令来刷新权限
>
> ```
> FLUSH PRIVILEGES;
> ```
>
> 如果还是无法连接,可以尝试
>
> ```
> telnet localhost 3306
> ```
>
> > 如果结果中出现 `caching_sha2_password`关键字,说明修改未生效

