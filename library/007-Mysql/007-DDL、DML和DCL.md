## DDL，DML和DCL的区别与理解
1. **DML（data manipulation language）：**  
　　它们是`SELECT、UPDATE、INSERT、DELETE`，就象它的名字一样，这4条命令是用来对数据库里的数据进行操作的语言.  
2. **DDL（data definition language）：**  
　　DDL比DML要多，主要的命令有`CREATE、ALTER、DROP`等，DDL主要是用在定义或改变表（TABLE）的结构，数据类型，表之间的链接和约束等初始化工作上，他们大多在建立表时使用.
3. **DCL（Data Control Language）：**  
　　是数据库控制功能。是用来设置或更改数据库用户或角色权限的语句，包括（`grant,deny,revoke`等）语句。在默认状态下，只有sysadmin,dbcreator,db_owner或db_securityadmin等人员才有权力执行DCL.  


### 详细解释：  
#### DDL is Data Definition Language statements. Some examples:
数据定义语言，用于定义和管理 SQL 数据库中的所有对象的语言  
1. CREATE - to create objects in the database   创建        
2. ALTER - alters the structure of the database   修改        
3. DROP - delete objects from the database   删除
4. TRUNCATE - remove all records from a table, including all spaces allocated for the records are removed  
5. COMMENT - add comments to the data dictionary 注释
6. GRANT - gives user's access privileges to database 授权         7.REVOKE - withdraw access privileges given with the GRANT command   收回已经授予的权限
  
#### DML is Data Manipulation Language statements. Some examples:  
数据操作语言，SQL中处理数据等操作统称为数据操纵语言  
1. SELECT - retrieve data from the a database           查询         
2. INSERT - insert data into a table                    添加          
3. UPDATE - updates existing data within a table    更新
4. DELETE - deletes all records from a table, the space for the records remain   删除
5. CALL - call a PL/SQL or Java subprogram         
6. EXPLAIN PLAN - explain access path to data  
7. LOCK TABLE - control concurrency 锁，用于控制并发

#### DCL is Data Control Language statements. Some examples:
数据控制语言，用来授予或回收访问数据库的某种特权，并控制数据库操纵事务发生的时间及效果，对数据库实行监视等  
1. COMMIT - save work done 提交    
2. SAVEPOINT - identify a point in a transaction to which you can later roll back 保存点  
3. ROLLBACK - restore database to original since the last COMMIT   回滚  
4. SET TRANSACTION - Change transaction options like what rollback segment to use   设置当前事务的特性，它对后面的事务没有影响．  
