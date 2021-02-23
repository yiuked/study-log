地址：https://elk-docker.readthedocs.io/



### 问题

1. 虚拟内存设置过小 ax virtual memory areas vm.max_map_count

```
elk_1  | [2021-02-22T03:13:55,243][ERROR][o.e.b.Bootstrap          ] [elk] node validation exception
elk_1  | [1] bootstrap checks failed
elk_1  | [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```

> 虚拟内存过小，需要262144，但当前值 为65530，可以使用`sysctl -a|grep vm.max_map_count`查看当前设置

解决方式：

```
vim /etc/sysctl.conf
vm.max_map_count=262144

sysctl -p # 重新读取配置文件
```



2. filebeat已连接上logstash，但推送日志失败

   ```
   2021-02-22T18:39:22.933+0800	INFO	[publisher_pipeline_output]	pipeline/output.go:151	Connection to backoff(async(tcp://148.70.118.28:5044)) established
   2021-02-22T18:39:22.985+0800	ERROR	[logstash]	logstash/async.go:280	Failed to publish events caused by: read tcp 172.16.215.82:36222->145.50.116.38:5044: read: connection reset by peer
   
   ```

3. 关闭SSL（默认是开启的）