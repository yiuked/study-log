### 安装

```
yum install -y flannel
```

### 配置

```
vim /etc/sysconfig/flanneld

# etcd 服务地址
FLANNEL_ETCD_ENDPOINTS="http://10.0.0.11:2379"

# etcd 中用于保存配置文件的key
FLANNEL_ETCD_PREFIX="/atomic.io/network"

# 其它参数，-iface=enp0s8 指定网卡地址，（注意，如果flannel启用用IP地址一致，请检查是不是存在相同的网卡地址）
FLANNEL_OPTIONS="-iface=enp0s8"

```

flannel启动后两个节点的IP地址相同，修改配置文件在`FLANNEL_OPTIONS="-iface=enp0s8"`中指定IP地址不相同的网上名：

* master

  ```
  docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
          inet 172.16.40.1  netmask 255.255.255.0  broadcast 0.0.0.0
          ether 02:42:b4:0b:18:29  txqueuelen 0  (Ethernet)
          RX packets 0  bytes 0 (0.0 B)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 0  bytes 0 (0.0 B)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
  
  enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
          inet 10.0.2.15  netmask 255.255.255.0  broadcast 10.0.2.255
          inet6 fe80::a00:27ff:fe6c:3e95  prefixlen 64  scopeid 0x20<link>
          ether 08:00:27:6c:3e:95  txqueuelen 1000  (Ethernet)
          RX packets 5021  bytes 410195 (400.5 KiB)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 6521  bytes 901899 (880.7 KiB)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
  
  enp0s8: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
          inet 10.0.0.11  netmask 255.255.255.0  broadcast 10.0.0.255
          inet6 fe80::a00:27ff:fe89:a478  prefixlen 64  scopeid 0x20<link>
          ether 08:00:27:89:a4:78  txqueuelen 1000  (Ethernet)
          RX packets 6755  bytes 1023603 (999.6 KiB)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 6531  bytes 3656928 (3.4 MiB)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
  
  flannel0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1472
          inet 172.16.40.0  netmask 255.255.0.0  destination 172.16.40.0
          unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
          RX packets 0  bytes 0 (0.0 B)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 0  bytes 0 (0.0 B)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
  
  ```

* node1

  ```
  docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
          inet 172.16.40.1  netmask 255.255.255.0  broadcast 0.0.0.0
          ether 02:42:72:91:1c:3d  txqueuelen 0  (Ethernet)
          RX packets 0  bytes 0 (0.0 B)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 0  bytes 0 (0.0 B)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
  
  enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
          inet 10.0.2.15  netmask 255.255.255.0  broadcast 10.0.2.255
          inet6 fe80::a00:27ff:fe6c:3e95  prefixlen 64  scopeid 0x20<link>
          ether 08:00:27:6c:3e:95  txqueuelen 1000  (Ethernet)
          RX packets 24463  bytes 28315676 (27.0 MiB)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 5411  bytes 853788 (833.7 KiB)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
  
  enp0s8: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
          inet 10.0.0.12  netmask 255.255.255.0  broadcast 10.0.0.255
          inet6 fe80::a00:27ff:fec1:9775  prefixlen 64  scopeid 0x20<link>
          ether 08:00:27:c1:97:75  txqueuelen 1000  (Ethernet)
          RX packets 7324  bytes 3233632 (3.0 MiB)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 7416  bytes 1607787 (1.5 MiB)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
  
  flannel0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1472
          inet 172.16.9.0  netmask 255.255.0.0  destination 172.16.9.0
          unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
          RX packets 0  bytes 0 (0.0 B)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 0  bytes 0 (0.0 B)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions
  ```

  

  