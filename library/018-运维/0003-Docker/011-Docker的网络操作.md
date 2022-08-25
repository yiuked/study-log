## Docker的网络操作
Docker启动的时候会在主机上自动创建一个docker0网桥，实际上是一个Linux网桥，所有容器的启动如果在docker run的时候没有指定网络模式的情况下都会挂载到docker0网桥上。这样容器就可以和主机甚至是其他容器之间通讯了。
```
brctl show
```
通过`ifconfig`可以查看对应的IP地址
```
ifconfig
```

* 配置主机名
```
docker run -h hostname
```

* 自定义网络方式
```
[root@VM_0_14_centos ~]# docker network create -d bridge my-net
d90fc3d8515b9402f2aca86767aa81ebb115cb4fcea4c90ed82446326cce7d35
[root@VM_0_14_centos ~]# docker run -it -d --name centos1 --network my-net centos
a43d83dbbde5827aeb3a66bab0e954df3b95a157dc0aea218cb23565af9655ce
[root@VM_0_14_centos ~]# docker run -it -d --name centos2 --network my-net centos
4f59c5ed14e075a1ef05468d9bfd75fe02fd210b3b580c8b0994bb3c0310a80e
[root@VM_0_14_centos ~]# docker exec -it centos1 /bin/bash
[root@a43d83dbbde5 /]# ping centos2
PING centos2 (172.18.0.3) 56(84) bytes of data.
64 bytes from centos2.my-net (172.18.0.3): icmp_seq=1 ttl=64 time=0.112 ms
64 bytes from centos2.my-net (172.18.0.3): icmp_seq=2 ttl=64 time=0.061 ms
64 bytes from centos2.my-net (172.18.0.3): icmp_seq=3 ttl=64 time=0.058 ms
64 bytes from centos2.my-net (172.18.0.3): icmp_seq=4 ttl=64 time=0.056 ms
^C
--- centos2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3000ms
rtt min/avg/max/mdev = 0.056/0.071/0.112/0.025 ms
[root@a43d83dbbde5 /]#
```


https://blog.csdn.net/u012943767/article/details/79767670
