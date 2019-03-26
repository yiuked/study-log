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
## 启动数据库
mysqld_safe --defaults-file=/var/lib/mysql/backup-my.cnf --user=mysql --datadir=/var/lib/mysql &

```
