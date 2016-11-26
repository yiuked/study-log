## Mysql主从构架实列
1. [实列环境详情](#实列环境详情 "实列环境详情")
1. [环境配置与搭建](#环境配置与搭建 "环境配置与搭建")
### 实列环境详情
##### 主机(Master)
```
操作系统: Windows7 64位
Mysql版本:Mysql 5.6.17 32位
IP地址:192.168.1.198
```
##### 从机(Slave)
```
操作系统: Centos 6.8 (2.6.32-642.6.2.e16.i686)
Mysql版本:Mysql 5.6.34 32位
IP地址:192.168.1.252
```
### 环境配置与搭建
`Windows` 下直接安装 `Wamp` 集成了 `5.6.17` 版的`Mysql` 没什么可说的.  
`Centos` 下直接到官方下载:  
下载地址: https://dev.mysql.com/downloads/mysql/5.6.html#downloads  
由于官方没有 `5.6.17` 版,因此，选择了 `5.6.34`  
下载的时候一定要根据自己的系统版本以及位数选择正确的版本，否则会导致安装失败，这里我选择了
```
MySQL-5.6.34-1.el6.i686.rpm-bundle.tar
```
下载下来以后，解包：  
```
#tar -xvf MySQL-5.6.34-1.el6.i686.rpm-bundle.tar
...
#ls
MySQL-server-5.6.34-1.el6.i686.rpm  #Mysql主程序
MySQL-client-5.6.34-1.el6.i686.rpm  #客户端连接程序
MySQL-devel-5.6.34-1.el6.i686.rpm   #所需的库和包含文件
...
```
出于需求，仅安装了以上三个`rpm`包  
安装过程
```
rpm -ivh  MySQL-server-5.6.34-1.el6.i686.rpm
...
```
安装完成，启动：
```
service mysql start
```
启用成功，没有设置补始密码,可参考[>>Mysql设置初始密码篇](?file=007-Mysql/002-Mysql设置初始密码)

### 主机(Master)配置
`my.ini`文件配置, 这里为了便于显示，去掉备注及其它不相关配置.
```
[mysqld]

log-bin=mysql-bin
server-id=198
binlog-ignore-db=mysql # 忽略mysql表
binlog-do-db=yii_cart  # 指定数据库
binlog_format=statement# statement row | mixed

sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
```
**statement | row | mixed**  的区别，请参照[>>MySQL之binlog_format详解](?file=007-Mysql/004-MySQL之binlog_format详解)

接下来重启`Mysql`,登录并进入`Mysql`客户端,创建一个允许在从机登录，并拥有`File、REPLICATION、SLAVE`权限的用户。    
```
GRANT File,REPLICATION SLAVE ON *.* TO 'slave1'@'192.168.1.252' IDENTIFIED BY '123456';
```
创建完成，查看一下主机(`Master`)状态:
```
mysql> show master status\G;
*************************** 1. row ***************************
             File: mysql-bin.000001
         Position: 120
     Binlog_Do_DB: myshop
 Binlog_Ignore_DB: information_schema,mysql
Executed_Gtid_Set:
1 row in set (0.00 sec)

ERROR:
No query specified
```
如果查询不到数据，请尝试重启`Mysql`或者，检测`my.ini`文件配置是否正确。  

**获取主机(Slave)的备份**
在主机(Master)配置完成后，需要获得主机(Master)的一个快照备份，这个备份将用于恢复到从机(Slave)，而从机(Slave)则通过这个快照的时间点开始进行对主机(Master)的复制工作。  
由于日志文件与日志定位文件，以就是上面的:
```
File: mysql-bin.000001
Position: 120
```
并不是一成不变的，因此需要获得一个精准的快照备份信息,因此进行备份请，需要对数据库进行全局锁操作,以防止数据在备份过程产生新数据而导致备份数据不全面问题.
```
mysql>FLUSH TABLES WITH READ LOCK;
mysql>SHOW PROCESSLIST;
```
由于`FLUSH TABLES WITH READ LOCK`命令执行后，将无法对表进行增、删、改，仅允许读，但`FLUSH TABLES WITH READ LOCK`会等待所有的读写完后再执行，因此某些慢查询或者
带事务锁的语句，可能会让`FLUSH TABLES WITH READ LOCK`延迟一段时间，但正是因为这样才保证了备份过程的精准性。


### 从机(Slave)配置
```
[mysqld]

server-id=252
replicate-do-db=myshop
replicate-ignore-db=mysql
log-slave-updates
slave-skip-errors=all
slave-net-timeout=60

sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
```
配置完成后重新启动`Mysql`,并登录从机(Slave)的客户端,执行以下语句:  
```
mysql>STOP SLAVE;
mysql> CHANGE MASTER TO
-> MASTER_HOST='192.168.1.198',
-> MASTER_USER='slave1',
-> MASTER_PASSWORD='123456',
-> MASTER_LOG_FILE='mysql-bin.000001',
-> MASTER_LOG_POS=120;
mysql>START SLAVE;
```
关于`CHANGE MASTER TO`的详细语法，可以参考[>>CHANGE MASTER TO 语法详解](?file=007-Mysql/005-CHANGE MASTER TO 语法详解)  
更改完成后，则可查看从机运行状态  
```
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 192.168.1.198
                  Master_User: slave
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000007
          Read_Master_Log_Pos: 120
               Relay_Log_File: localhost-relay-bin.000014
                Relay_Log_Pos: 283
        Relay_Master_Log_File: mysql-bin.000007
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB: myshop
          Replicate_Ignore_DB: mysql
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 120
              Relay_Log_Space: 460
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 198
                  Master_UUID: ad125682-4578-11e6-97de-00ffb04c738d
             Master_Info_File: /var/lib/mysql/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for the slave I/O thread to update it
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
1 row in set (0.02 sec)

ERROR:
No query specified
```

如果一切正常，可以看到
```
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
```
如果状态为`No`,可以通过可以尝试以启动`slave`  
```
mysql>start slave; #启动
mysql>stop slave;  #停止
```
此时可以尝试，在主机(Master)下新增或者修改数据，然后查看从机.
