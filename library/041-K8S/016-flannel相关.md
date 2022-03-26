### 概述

Flannel是CoreOS团队针对Kubernetes设计的一个网络规划服务，简单来说，它的功能是让集群中的不同节点主机创建的Docker容器都具有全集群唯一的虚拟IP地址。

### 问题

1. 没有`flannel`时`coredns`无法启动
2. 启动`flannel`后,同网段`192.168.3.10`可以访问安装过`flannel`的机器(`192.168.3.50`),而`192.168.0.10`则无法访问`192.168.3.50`



### 相关命令

```
ifconfig cni0 down
ifconfig flannel.1 down
ifconfig del flannel.1
ifconfig del cni0

ip link del flannel.1
ip link del cni0

如果没有 brctl 命令
yum install bridge-utils

brctl delbr  flannel.1
brctl delbr cni0

rm -rf /var/lib/cni/flannel/* && rm -rf /var/lib/cni/networks/cbr0/* && ip link delete cni0 && rm -rf /var/lib/cni/network/cni0/*

```

