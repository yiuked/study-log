## Fabric CA服务器搭建

### 下载
安装服务端
```
go get -u github.com/hyperledger/fabric-ca/cmd/fabric-ca-server
```
安装客户端
```
go get -u github.com/hyperledger/fabric-ca/cmd/fabric-ca-client
```
执行结果:
>1.将在`$GOPATH/bin`中安装`fabric-ca-server`和`fabric-ca-client`二进制文件。  
 2.并克隆`fabric-ca`源码到`$GOPATH/src/github.com/hyperledger/fabric-ca/`目录下。

### 启动
下载文件中，为我们提供了两种启动方式，一种是基于docker,另一种则是原生的启动方式。
1. docker启动:
```
cd $GOPATH/src/github.com/hyperledger/fabric-ca/docker/server/docker-compose.yml
docker-compose up –d
```
2. 原生启动:
```
cd $GOPATH/bin
fabric-ca-server start -b admin:adminpw
```


### 参考文献:  
1.[Fabric CA 官方用户指南（中文版）](https://blog.csdn.net/greedystar/article/details/80344984)
