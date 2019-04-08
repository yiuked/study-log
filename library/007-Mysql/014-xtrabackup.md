### 安装
https://www.percona.com/doc/percona-xtrabackup/2.4/installation/apt_repo.html


### 备份
```
sudo innobackupex --user=dbuser --password=dbpass /var/backup/
```

### 还原
查看mysql数据存储目录
```
mysqld -v|grep data_dir
```
安装qpress
```
wget http://www.quicklz.com/qpress-11-linux-x64.tar
tar xvf qpress-11-linux-x64.tar
cp qpress /usr/bin
```
wget可能下载不了，可直接通过其它下载工具下载。
```
## 解包
cat <数据备份文件名>_qp.xb | xbstream -x -v -C /var/lib/mysql
## 解压
innobackupex --decompress --remove-original /var/lib/mysql
## 恢复备份文件
innobackupex --defaults-file=/var/lib/mysql/backup-my.cnf --apply-log /var/lib/mysql
## 修改数据库文件夹权限
chown -R mysql:mysql /var/lib/mysql
```
迁移成功后，启动MYSQL正常,但是在执行SQL
```
 Table 'performance_schema.session_status' doesn't exist
 [Err] 1682 - Native table 'performance_schema'.'session_status' has the wrong structure
```
mysql可能会去读取/etc/mysql/my.conf配置文件。备份的配置文件在`/var/lib/mysql/backup-my.cnf`
做以下处理
```
## 版本兼容注示以下代码
vi /var/lib/mysql/backup-my.cnf
#innodb_fast_checksum
#innodb_page_size
#innodb_log_block_size
# 保存后，切换到linux 的root账户
mysql_upgrade -u root -p --force

## 启动数据库(vagrant 上测试不成功)
mysqld_safe --defaults-file=/var/lib/mysql/backup-my.cnf --user=mysql --datadir=/var/lib/mysql &
```
