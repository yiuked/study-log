## MyISAM与Innodb
###  MyISAM
#### 索引类型
  1. B-Tree
  2. R-Tree
  3. Full-text
> B-tre最常用，偶尔Full-text,很少用于R-Tree,B-Tree参与一个索引的所有字段长度之和不能超过1000字节.


###  Innodb
#### Innodb的特性
1. 支持事务安全
2. 数据多版本读取
3. 锁定机制的改进，MyISAM是表锁，Innodb支持行锁，因此如果需要加入锁的情况下，Innodb显示比MyISAM更有优势.
4. 实现外键
