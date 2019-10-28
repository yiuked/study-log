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

### 配置
初始化后，会生成以下目录结构:
```
fabric-ca-server init -b admin:adminpw
...
tree ./
├── ca-cert.pem                           # 生成的证书文件
├── fabric-ca-server
├── fabric-ca-server-config.yaml          # CA server配置文件
├── fabric-ca-server.db                   # 存储发放证书信息的sqlite3数据库
├── IssuerPublicKey                       # 颁布者公钥
├── IssuerRevocationPublicKey             # 颁布者吊销公钥
└── msp
    └── keystore
        ├── c430084e7c0ccfeb691a2d78eb1b5f657523da0b66904c9820143677a5084080_sk
        ├── IssuerRevocationPrivateKey    # 颁布者吊销私钥
        └── IssuerSecretKey               # 颁布者密钥(非私钥)
```
查看证书文件信息：
```
# openssl x509 -in ca-cert.pem -inform pem -noout -text
Certificate:
    Data:
        ...
    Signature Algorithm: ecdsa-with-SHA256
        ...
    Signature Algorithm: ecdsa-with-SHA256
        ...
```
编辑CA server配置文件
```
vim fabric-ca-server-config.yaml
...
# 监听端口号
port:7054
...
# 配置MySQLl连接(默认为SQLLite)
db:
type: mysql
datasource: root:rootpw@tcp(localhost:3306)/fabric_ca?parseTime=true&tls=custom
```

### 参考文献:  
1.[Fabric CA 官方用户指南（中文版）](https://blog.csdn.net/greedystar/article/details/80344984)
