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

