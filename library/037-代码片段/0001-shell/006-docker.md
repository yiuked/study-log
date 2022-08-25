- 通过docker快速备份mysql

> docker exec mysql mysqldump --column-statistics=0 -hlocalhost -uroot -pxx -x test>$(date +%Y-%m-%d)-test.sql

--column-statistics=0 解决这个问题 `mysqldump: Couldn't execute 'SELECT COLUMN_NAME`
-x 解决这个问题`mysqldump: Got error: 1449: The user specified as a definer ('admin'@'%') does not exist when using LOCK TABLES`