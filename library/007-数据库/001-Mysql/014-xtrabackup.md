### 概述
云数据库 MySQL 备份系统改造已发布上线，新版本备份系统，无论是物理备份还是逻辑备份，都会进行压缩与打包。具体流程是：先经过 qpress 压缩，后经过 xbstream 打包（xbstream 为 Percona 的一种打包/解包工具）。备份文件后缀名以.xb结尾。

### 安装
https://www.percona.com/doc/percona-xtrabackup/2.4/installation/apt_repo.html

### 无压缩备份
```
sudo innobackupex --user=dbuser --password=dbpass /var/backup/
```

### 无压缩还原
```
# 请谨慎操作，该操作会删旧库
sudo rm -rf /var/lib/mysql/*
sudu cp -r /var/backup/20xxx/* /var/lib/mysql/

innobackupex --defaults-file=/var/lib/mysql/backup-my.cnf --apply-log /var/lib/mysql
## 修改数据库文件夹权限
chown -R mysql:mysql /var/lib/mysql
```

### 有压缩还原
查看mysql数据存储目录
```
mysqld -v|grep data_dir
```
安装qpress,qpree是一款免费的解压缩工具，阿里的MYSQL备份文件采用qpress进行压缩
```
wget http://www.quicklz.com/qpress-11-linux-x64.tar
tar xvf qpress-11-linux-x64.tar
sudo cp qpress /usr/bin
```
wget可能下载不了，可直接通过其它下载工具下载。
```
## 如果此前用过innobackupx会创建文件失败，建立直接清除/var/lib/mysql/下面所有文件
rm -rf /var/lib/mysql/*
## 解包 如果解包失败进行重新解包时，一定要清除/var/lib/mysql/已解包的文件，否则进行解压时会提示文件被损失。
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
$service mysql start
$mysql_upgrade -u root -p --force
# #如果此处不知道root账户密码，使用其它可登录mysql的账户登录然后，重置密码，
# mysql -u myuser -p mypass
# mysql>update user set password=password('new password') where user='root';
# #更新完如果还不行，试试mysql_upgrade -h 127.0.0.1 -u root -p --force，因此默认是使用localhost登录
$service mysql stop
$service mysql start

## 如果默认启用配置文件不对，可以参考以下命令：
mysqld_safe --defaults-file=/var/lib/mysql/backup-my.cnf --user=mysql --datadir=/var/lib/mysql &
```

### 兼容
升级到MYSQL5.7后，很多原本可以运行的SQL可能会报错,比如提示:
```
... doesn’t have a default value
```
这是因为5.7默认启用了严格的传输表，找到`my.conf`文件:
> 如果找不到文件在哪，可以偿试执行'mysqld --verbose --help|grep conf'  

```
[mysqld]
sql-mode="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
```
修改为
```
[mysqld]
sql-mode="NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
```
关于`STRICT_TRANS_TABLES`的更多说明如下：  
  >  原来在MySQL 5.0.2之前，MySQL对非法或不当值并不严厉，而且为了数据输入还会强制将它们变为合法值。在MySQL 5.0.2和更高版本中，保留了以前的默认行为，但你可以为不良值选择更传统的处理方法，从而使得服务器能够拒绝并放弃出现不良值的语句。本节介绍了MySQL的默认行为（宽大行为），新的严格的SQL模式，以及它们的区别。  
    如果你未使用严格模式，下述情况是真实的。如果将“不正确”的值插入到列，如将NULL值插入非NULL列，或将过大的数值插入数值列，MySQL会将这些列设置为“最可能的值”，而不是生成错误信息。  
  　　· 如果试图将超范围的值保存到数值列，MySQL服务器将保存0（最小的可能值）取而代之，或最大的可能值。  
  　　· 对于字符串，MySQL或保存空字符串，或将字符串尽可能多的部分保存到列中。  
  　　· 如果打算将不是以数值开头的字符串保存到数值列，MySQL将保存0。  
  　　· MySQL允许将特定的不正确日期值保存到DATE和DATETIME列（如“2000-02-31”或“2000-02-00”）。其观点在于，验证日期不是SQL服务器的任务。如果MySQL能保存日期值并准确检索相同的值，MySQL就能按给定的值保存它。如果日期完全不正确（超出服务器能保存的范围）将在列中保存特殊的日期值“0000-00-00”取而代之。  
  　　· 如果试图将NULL值保存到不接受NULL值的列，对于单行INSERT语句，将出现错误。对于多行INSERT语句或INSERT INTO … SELECT语句，MySQL服务器会保存针对列数据类型的隐含默认值。一般情况下，对于数值类型，它是0，对于字符串类型，它是空字符串(”)，对于日期和时间类型是“zero”。  
  　　· 如果INSERT语句未为列指定值，如果列定义包含明确的DEFAULT子句，MySQL将插入默认值。如果在定义中没有这类DEFAULT子句，MySQL会插入列数据类型的隐含默认值。  
  　　采用前述规则的原因在于，在语句开始执行前，无法检查这些状况。如果在更新了数行后遇到这类问题，我们不能仅靠回滚解决，这是因为存储引擎可能不支持回滚。中止语句并不是良好的选择，在该情况下，更新完成了“一半”，这或许是最差的情况。对于本例，较好的方法是“仅可能做到最好”，然后就像什么都未发生那样继续。  
  　　在MySQL 5.0.2和更高版本中，可以使用STRICT_TRANS_TABLES或STRICT_ALL_TABLES SQL模式，选择更严格的处理方式。  
  　　STRICT_TRANS_TABLES的工作方式：  
  　　· 对于事务性存储引擎，在语句中任何地方出现的不良数据值均会导致放弃语句并执行回滚。  
  　　· 对于非事务性存储引擎，如果错误出现在要插入或更新的第1行，将放弃语句。（在这种情况下，可以认为语句未改变表，就像事务表一样）。首行后出现的错误不会导致放弃语句。取而代之的是，将调整不良数据值，并给出告警，而不是错误。换句话讲，使用STRICT_TRANS_TABLES后，错误值会导致MySQL执行回滚操作，如果可以，所有更新到此为止。  
  　　要想执行更严格的检查，请启用STRICT_ALL_TABLES。除了非事务性存储引擎，它与STRICT_TRANS_TABLES等同，即使当不良数据出现在首行后的其他行，所产生的错误也会导致放弃语句。这意味着，如果错误出现在非事务性表多行插入或更新过程的中途，仅更新部分结果。前面的行将完成插入或更新，但错误出现点后面的行则不然。对于非事务性表，为了避免这种情况的发生，可使用单行语句，或者在能接受转换警告而不是错误的情况下使用STRICT_TRANS_TABLES。要想在第1场合防止问题的出现，不要使用MySQL来检查列的内容。最安全的方式（通常也较快）是，让应用程序负责，仅将有效值传递给数据库。  
  　　有了严格的模式选项后，可使用INSERT IGNORE或UPDATE IGNORE而不是不带IGNORE的INSERT或UPDATE，将错误当作告警对待。  



一键脚本

```
#/bin/bash


if [ ! -n "$1" ]; then
	echo $1
	echo "Option:"
	echo "<xb file path>"
	exit 1
fi

echo "Stop mysql service ..."
service mysql stop

set -x
rm -rf /var/lib/mysql/*
res=$?
set +x

if [ $res -ne 0 ];then
	echo "Delete /var/lib/mysql fail"
	exit 1
fi

cat $1 | xbstream -x -v -C /var/lib/mysql
res=$?

if [ $res -ne 0 ];then
	echo "xbstream /var/lib/mysql fail"
	exit 1
fi

innobackupex --decompress --remove-original /var/lib/mysql
res=$?

if [ $res -ne 0 ];then
	echo "decompress /var/lib/mysql fail"
	exit 1
fi

innobackupex --defaults-file=/var/lib/mysql/backup-my.cnf --apply-log /var/lib/mysql
res=$?

if [ $res -ne 0 ];then
	echo "restore /var/lib/mysql fail"
	exit 1
fi


chown -R mysql:mysql /var/lib/mysql

mysqld_safe --defaults-file=/etc/mysql/conf.d/mysql.cnf --user=mysql --datadir=/var/lib/mysql &


```



启动出现以下错误

```
* Starting MySQL database server mysqld
No directory, logging in with HOME=/
mkdir: cannot create directory '//.cache': Permission denied
-su: 19: /etc/profile.d/wsl-integration.sh: cannot create //.cache/wslu/integration: Directory nonexistent
```

设置账户初始目录

```
usermod -d /var/lib/mysql mysql
```

