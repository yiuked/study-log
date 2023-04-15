```shell
#!/bin/bash

# 定义备份目录
backup_dir=/data/mysql_backup/sql

# 定义备份文件名
backup_file=catering_$(date +%Y%m%d_%H%M%S).sql

# 进入 mysql 容器，并执行备份命令
docker exec mysql sh -c "exec mysqldump -uroot -p'RedisRds2020' catering" > ${backup_dir}/${backup_file}

# 压缩备份文件
cd ${backup_dir}
tar -zcvf ${backup_file}.tar.gz ${backup_file}

# 删除原始备份文件
rm -f ${backup_dir}/${backup_file}

# 删除过期备份文件（保留最近 30 天备份）
find ${backup_dir} -type f -mtime +30 -name "*.tar.gz" -exec rm -f {} \;
```