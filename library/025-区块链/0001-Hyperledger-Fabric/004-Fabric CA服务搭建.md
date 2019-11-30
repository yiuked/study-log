# Fabric CA服务器搭建
>1. [概述](#概述 "概述")
1. [下载](#下载 "下载")
1. [服务端](#服务端 "服务端")
	1. [启动服务端](#启动服务端 "启动服务端")
	1. [配置服务端](#配置服务端 "配置服务端")
	1. [客户端](#客户端 "客户端")
	1. [生成`Fabric CA`管理员凭证:](#生成`Fabric CA`管理员凭证: "生成`Fabric CA`管理员凭证:")
	1. [设计联盟间的关系](#设计联盟间的关系 "设计联盟间的关系")
1. [RESTful接口](#RESTful接口 "RESTful接口")
	1. [参考文献:](#参考文献: "参考文献:")


## 概述
Fabric CA 用于管理参与联盟各组织下的MSP证书管理。它的工作流程分为：
1. 设计联盟间的关系。
2. 生成每个组织的MSP证书。
3. 生成每个组织下的管理员MSP证书。
4. 使用每个组织下的管理员生成相对的子账户。


## 下载
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

>直接下载二进制文件点[这里](https://nexus.hyperledger.org/content/repositories/releases/org/hyperledger/fabric-ca)

## 服务端
### 启动服务端
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

### 配置服务端
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
默认读取当前目录下的`fabric-ca-server-config.yaml`文件，如果需要读取其它的配置文件，
需要在启动时，设置对应的配置文件:
```
export FABRIC_CA_SERVER_HOME=/home/vagrant/fabric-ca/server/ca-files
./fabric-ca-server start -b admin:admin --cafiles ca/ca1/fabric-ca-server-config.yaml
```

### 客户端
客户端生成用户凭证的过程：
```
登录用户(register)->生成凭证(enroll)
```
### 生成`Fabric CA`管理员凭证:
```
export FABRIC_CA_CLIENT_HOME=/home/vagrant/fabric-ca/client
./fabric-ca-client enroll -u http://admin:admin@localhost:7054 -M $FABRIC_CA_CLIENT_HOME/ca-files/admin
```
`Fabric CA`管理员账户在`Fabric CA Server` 启动时，已经进行登记，因此可直接进行`enroll`生成凭证。

### 设计联盟间的关系

## RESTful接口
Fabric CA提供的`RESTful`接口，可通过`http/https`访问。

| 请求URL | 方法类型 | 描述
| :-------- | :------ | :---
| /api/v1/cainfo | GET | 获取CA信息
| /api/v1/enroll | POST | 获取注册证书
| /api/v1/reenroll | POST | 重新获取注册证书
| /api/v1/register | POST | 获取CA信息
| /api/v1/revoke | POST | 用户注销
| /api/v1/tcert | POST | 批量获取交易证书

### 参考文献:  
1.[Fabric CA 官方用户指南（中文版）](https://blog.csdn.net/greedystar/article/details/80344984)
2.[超级账本HyperLedger的Fabric-CA的使用（两个组织一个Orderer三个Peer)](https://blog.csdn.net/lijiaocn/article/details/80261529)
3.[Hyperledger Fabric 1.4 特性调研之Operations Service（二）](https://www.jianshu.com/p/6cf812a9dc50)
