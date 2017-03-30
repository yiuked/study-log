## MySQL锁机制

### 行级锁
行级锁分两种类型，一种为共享锁，一种排它锁.
### 表级锁
表级锁分两种类型，一种为读锁定，一种为写锁定。Mysql主要通过4个队列来维护这两种锁.
```
Current read-lock queue(lock->read)
Pending read-lock queue(lock->read_wait)
Current write-lock queue(lock->read)
Pending read-lock queue(lock->read_wait)
```
操作语句:
```
LOCK TABEL table_name READ;  #读锁表
LOCK TABEL table_name WRITE; #写锁表
UNLOCK TABLES;               #解锁表
```
### 页级锁
