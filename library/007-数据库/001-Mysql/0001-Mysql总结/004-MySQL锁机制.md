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



### InnoDB行锁实现方式
InnoDB行锁是通过给索引上的索引项加锁来实现的，** 只有通过索引条件检索数据，InnoDB才使用行级锁，否则，InnoDB将使用表锁**
在实际应用中，要特别注意InnoDB行锁的这一特性，不然的话，可能导致大量的锁冲突，从而影响并发性能。下面通过一些实际例子来加以说明。
* 在不通过索引条件查询的时候，InnoDB确实使用的是表锁，而不是行锁。
* 由于MySQL的行锁是针对索引加的锁，不是针对记录加的锁，所以虽然是访问不同行的记录，但是如果是使用相同的索引键，是会出现锁冲突的。
* 当表有多个索引的时候，不同的事务可以使用不同的索引锁定不同的行，另外，不论是使用主键索引、唯一索引或普通索引，InnoDB都会使用行锁来对数据加锁。
* 即便在条件中使用了索引字段，但是否使用索引来检索数据是由MySQL通过判断不同执行计划的代价来决定的，如果MySQL认为全表扫描效率更高，比如对一些很小的表，它就不会使用索引，这种情况下InnoDB将使用表锁，而不是行锁。因此，在分析锁冲突时，别忘了检查SQL的执行计划，以确认是否真正使用了索引。