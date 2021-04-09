## MySQL binlog详解

### binlog目的

* 主从复制
* 备份恢复后需要重新应用部分binlog，从而达到全备+增备的效果

### 配置

my.conf

```
log-bin=mysql-bin
binlog_format=row
binlog_rows_query_log_events=1
```

### 日志格式

| 格式      | 模式              | 优点                                 | 缺点                                                         |
| --------- | ----------------- | ------------------------------------ | ------------------------------------------------------------ |
| statement | 基于SQL语句的模式 | 生成的binlog尺寸较小                 | 某些不确定性SQL语句或函数在复制过程可能导致数据不一致甚至出错 |
| row       | 基于数据行的模式  | 记录的是数据行的完整变化，更安全     | 生成的日志文件很大                                           |
| mixed     | 混合模式          | 根据情况自动选用statement抑或row模式 | 属于MySQL 5.1版本时期的过渡方案                              |

推荐设置`binlog_format=row`

### 分析工具`mysqlbinlog`

提取SQL

```
mysqlbinlog.exe --base64-output=decode-rows -v ../data/mysql-bin.000002

# 附加参数通过时间筛选
--start-date='2014-09-16 14:00:00' 
--stop-date='2014-09-16 14:20:00' 
```

