```
# 整体使用情况
df -h

# 查看文件夹存储占用情况
du -hm --max-depth=1 /var/ | sort -n

# 查看journal占用存储情况
journalctl --disk-usage

# 只保留近一周的日志 
journalctl --vacuum-time=1w

# 只保留100MB的日志 
journalctl --vacuum-size=100M

# 直接删除 /var/log/journal/ 目录下的日志文件 
rm -rf /var/log/journal/*
```