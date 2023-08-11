## Mysql事务与锁
环境:
```
Windows7 64位
Mysql 5.6.17
数据库引擎：Innodb
表名:user
```
**场景一，WHERE条件未添加索引的情况**  

id(主键) | gid | age | name | rating
---|------|----|----|
1 | 1  | 20 | Tom | 2
2 | 2  | 22 | Joe | 3
3 | 1  | 22 | Alu | 5

表中，除了主键自带索引外，没有为其它字段设置索引  

```
mysql>BEGIN;
mysql>SELECT * FROM WHERE gid=1 FOR UPDATE;
...
```
`Innodb`的行锁依赖行索引，当`WHERE`条件中的`gid`未设置索引时，该更新语句会导致锁表，此时`user`表
只能进行`SELECT`所有的`INSERT,DELETE,UPDATE`都会被阻塞，只有在遇到`COMMIT`才会被释放。  

**场景二，WHERE条件存在一个索引**  
为`gid`字段添加索引  
```
ALTER  TABLE  `user`  ADD  INDEX gid_index (`gid`)
```
id(主键) | gid(索引) | age | name | rating
---|------|----|----|
1 | 1  | 20 | Tom | 2
2 | 2  | 22 | Joe | 3
3 | 1  | 22 | Alu | 5

```
mysql>BEGIN;
mysql>SELECT * FROM WHERE gid=1 FOR UPDATE;
...
```
由于`WHERE`条件中的`gid`已设置索引时，因此在执行该更新语句时`gid`为1的行会被锁住，而其它的项不会受影响，
如果语句中存在多个条件，最终会锁住所有满足索引条件的行。  
```
mysql>BEGIN;
mysql>SELECT * FROM WHERE age=22 AND gid=1 FOR UPDATE;
```
只有`gid`中存在索引，`age`条件，无论在前还是在后，结果都一样，运行结果会锁住所有`gid`为1的行，无论`age`的值为多少。  

**场景三，WHERE条件存在两个索引**  
为`age`字段添加索引  
```
ALTER  TABLE  `user`  ADD  INDEX age_index (`age`)
```
id(主键) | gid(索引) | age（索引） | name | rating
---|------|----|----|
1 | 1  | 20 | Tom | 2
2 | 2  | 22 | Joe | 3
3 | 1  | 22 | Alu | 5

```
mysql>BEGIN;
mysql>SELECT * FROM WHERE gid=1 AND age=22 FOR UPDATE;
...
```
按照场景二中的推论，是不是此时这三条数据都会被锁住呢,结果表明，所有`gid`为1的行被锁住，而`age`值为多少，对被锁结果无任何影响.  
那么是否与`WHERE`条件的顺序有关呢，尝试切换`WHERE`条件的顺序.  
```
mysql>BEGIN;
mysql>SELECT * FROM WHERE  age=22 AND gid=1 FOR UPDATE;
...
```
得到结果与未切换顺序前的一样，所有`gid`为1的行被锁住，而`age`值为多少，对被锁结果无任何影响，那么到底是什么影响锁行的条件呢，此时得用上`EXPLAIN`命令了  

```
mysql>BEGIN;
mysql>EXPLAIN SELECT * FROM user WHERE age=22 and gid=1 FOR UPDATE\G;
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: user
         type: ref
possible_keys: gid,age
          key: gid
      key_len: 4
          ref: const
         rows: 2
        Extra: Using where
1 row in set (0.00 sec)
```
两个重要的参数   

键名 | 描述
-- | --
**possible_keys** | `possible_keys`列指出`MySQL`能使用哪个索引在该表中找到行。注意，该列完全独立于`EXPLAIN`输出所示的表的次序。这意味着在`possible_keys`中的某些键实际上不能按生成的表次序使用。   
**key** | `key`列显示`MySQL`实际决定使用的键(索引)。如果没有选择索引，键是`NULL`。要想强制`MySQL`使用或忽视`possible_keys`列中的索引，在查询中使用`FORCE INDEX、USE INDEX`或者`IGNORE INDEX`。  
上面的描述中，我们得出，我们写的`WHERE`条件语句在执行时并不一定会按我们所写的顺序执行，最终执行以`Mysql`内部优化后由系统排序顺序且决定使用哪个索引。  
那么如果我们非得按自己的指定的索引来执行时，怎么办呢?
```
mysql>BEGIN;
mysql>EXPLAIN SELECT * FROM user USE INDEX(age) WHERE age=22 and gid=1 FOR UPDATE\G;
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: user
         type: ref
possible_keys: age
          key: age
      key_len: 2
          ref: const
         rows: 2
        Extra: Using where
1 row in set (0.00 sec)
```
得到的结果，所有`age`为22的行都被锁住，而gid值为多少，不影响被锁行的结果.  

>警告，事务过程不能有网络请求，网络请求过程不可预计，有可能会导致COMMIT无法提交，从而导致事务死锁,  
>任何不可100%肯定结果的情况，都不应该放在事务过程中，如以下
```
BEGIN;
SELECT XXX FOR UPDATE;
UPDATE XXX1
此处发起网络请求，如CURL,file_get_contents等
UPDATE XXX2
COMMIT;
```

>查看锁状态
```
show status like '%lock%'
```

* MYSQL的DML操作除`SELECT`,如`INSERT,DELETE,UPDATE`都是自带事务的的语句.
