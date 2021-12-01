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

