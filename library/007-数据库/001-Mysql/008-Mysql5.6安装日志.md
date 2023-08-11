```
准备中...                          ################################# [100%]
正在升级/安装...
   1:atom-1.14.4-0.1                  ################################# [100%]
[shrakie@localhost 下载]$ sudo rpm -ivh MySQL-server-5.6.35-1.el7.x86_64.rpm
警告：MySQL-server-5.6.35-1.el7.x86_64.rpm: 头V3 DSA/SHA1 Signature, 密钥 ID 5072e1f5: NOKEY
准备中...                          ################################# [100%]
正在升级/安装...
   1:MySQL-server-5.6.35-1.el7        ################################# [100%]
警告：用户mysql 不存在 - 使用root
警告：群组mysql 不存在 - 使用root
警告：用户mysql 不存在 - 使用root
警告：群组mysql 不存在 - 使用root
2017-03-07 23:50:27 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2017-03-07 23:50:27 0 [Note] Ignoring --secure-file-priv value as server is running with --bootstrap.
2017-03-07 23:50:27 0 [Note] /usr/sbin/mysqld (mysqld 5.6.35) starting as process 8989 ...
2017-03-07 23:50:27 8989 [Note] InnoDB: Using atomics to ref count buffer pool pages
2017-03-07 23:50:27 8989 [Note] InnoDB: The InnoDB memory heap is disabled
2017-03-07 23:50:27 8989 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
2017-03-07 23:50:27 8989 [Note] InnoDB: Memory barrier is not used
2017-03-07 23:50:27 8989 [Note] InnoDB: Compressed tables use zlib 1.2.3
2017-03-07 23:50:27 8989 [Note] InnoDB: Using Linux native AIO
2017-03-07 23:50:27 8989 [Note] InnoDB: Using CPU crc32 instructions
2017-03-07 23:50:27 8989 [Note] InnoDB: Initializing buffer pool, size = 128.0M
2017-03-07 23:50:27 8989 [Note] InnoDB: Completed initialization of buffer pool
2017-03-07 23:50:27 8989 [Note] InnoDB: The first specified data file ./ibdata1 did not exist: a new database to be created!
2017-03-07 23:50:27 8989 [Note] InnoDB: Setting file ./ibdata1 size to 12 MB
2017-03-07 23:50:27 8989 [Note] InnoDB: Database physically writes the file full: wait...
2017-03-07 23:50:27 8989 [Note] InnoDB: Setting log file ./ib_logfile101 size to 48 MB
2017-03-07 23:50:28 8989 [Note] InnoDB: Setting log file ./ib_logfile1 size to 48 MB
2017-03-07 23:50:29 8989 [Note] InnoDB: Renaming log file ./ib_logfile101 to ./ib_logfile0
2017-03-07 23:50:29 8989 [Warning] InnoDB: New log files created, LSN=45781
2017-03-07 23:50:29 8989 [Note] InnoDB: Doublewrite buffer not found: creating new
2017-03-07 23:50:29 8989 [Note] InnoDB: Doublewrite buffer created
2017-03-07 23:50:29 8989 [Note] InnoDB: 128 rollback segment(s) are active.
2017-03-07 23:50:29 8989 [Warning] InnoDB: Creating foreign key constraint system tables.
2017-03-07 23:50:29 8989 [Note] InnoDB: Foreign key constraint system tables created
2017-03-07 23:50:29 8989 [Note] InnoDB: Creating tablespace and datafile system tables.
2017-03-07 23:50:29 8989 [Note] InnoDB: Tablespace and datafile system tables created.
2017-03-07 23:50:29 8989 [Note] InnoDB: Waiting for purge to start
2017-03-07 23:50:29 8989 [Note] InnoDB: 5.6.35 started; log sequence number 0
A random root password has been set. You will find it in '/root/.mysql_secret'.
2017-03-07 23:50:34 8989 [Note] Binlog end
2017-03-07 23:50:34 8989 [Note] InnoDB: FTS optimize thread exiting.
2017-03-07 23:50:34 8989 [Note] InnoDB: Starting shutdown...
2017-03-07 23:50:36 8989 [Note] InnoDB: Shutdown completed; log sequence number 1625977


2017-03-07 23:50:36 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2017-03-07 23:50:36 0 [Note] Ignoring --secure-file-priv value as server is running with --bootstrap.
2017-03-07 23:50:36 0 [Note] /usr/sbin/mysqld (mysqld 5.6.35) starting as process 9011 ...
2017-03-07 23:50:36 9011 [Note] InnoDB: Using atomics to ref count buffer pool pages
2017-03-07 23:50:36 9011 [Note] InnoDB: The InnoDB memory heap is disabled
2017-03-07 23:50:36 9011 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
2017-03-07 23:50:36 9011 [Note] InnoDB: Memory barrier is not used
2017-03-07 23:50:36 9011 [Note] InnoDB: Compressed tables use zlib 1.2.3
2017-03-07 23:50:36 9011 [Note] InnoDB: Using Linux native AIO
2017-03-07 23:50:36 9011 [Note] InnoDB: Using CPU crc32 instructions
2017-03-07 23:50:36 9011 [Note] InnoDB: Initializing buffer pool, size = 128.0M
2017-03-07 23:50:36 9011 [Note] InnoDB: Completed initialization of buffer pool
2017-03-07 23:50:36 9011 [Note] InnoDB: Highest supported file format is Barracuda.
2017-03-07 23:50:36 9011 [Note] InnoDB: 128 rollback segment(s) are active.
2017-03-07 23:50:36 9011 [Note] InnoDB: Waiting for purge to start
2017-03-07 23:50:36 9011 [Note] InnoDB: 5.6.35 started; log sequence number 1625977
2017-03-07 23:50:36 9011 [Note] Binlog end
2017-03-07 23:50:36 9011 [Note] InnoDB: FTS optimize thread exiting.
2017-03-07 23:50:36 9011 [Note] InnoDB: Starting shutdown...
2017-03-07 23:50:38 9011 [Note] InnoDB: Shutdown completed; log sequence number 1625987




A RANDOM PASSWORD HAS BEEN SET FOR THE MySQL root USER !
You will find that password in '/root/.mysql_secret'.

You must change that password on your first connect,
no other statement but 'SET PASSWORD' will be accepted.
See the manual for the semantics of the 'password expired' flag.

Also, the account for the anonymous user has been removed.

In addition, you can run:

  /usr/bin/mysql_secure_installation

which will also give you the option of removing the test database.
This is strongly recommended for production servers.

See the manual for more instructions.

Please report any problems at http://bugs.mysql.com/

The latest information about MySQL is available on the web at

  http://www.mysql.com

Support MySQL by buying support/licenses at http://shop.mysql.com

New default config file was created as /usr/my.cnf and
will be used by default by the server when you start it.
You may edit this file to change server settings
```
