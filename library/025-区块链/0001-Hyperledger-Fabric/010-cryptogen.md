# cryptogen详解

## 一、概述
### 1.1 什么是MSP
cryptogen 为 Fabric CA 的临时替代品，它主要用于开发、测试环境中快速为成员提供服务凭证，即MSP。
MSP 全称 Membership Service Provider,中文可翻为“成员服务提供商”。

### 1.2 什么是成员？
在Fabric区块链网络中，用于排序、查询、发起交易、安装链码的节点都可以称之为成员，
这此成员在区块链网络中的执行以上的任何一种操作，都需要通过表明并证实自己的身份，
而证实的过程则需要 MSP 中所提供的相关凭证。

### 1.3 有哪些成员类型?
成员的角色分为 `peer` `、client`、`orderer`、`admin`四种类型，
而与之关联的权限可以分为`Readers`、`Writers`、`Admins`,可在在创建创收块的时候通过修改
`configtx.yaml`中成员所处于的组织中的`Policies`来配置具体的权限。类似如下:
```
Policies:
    Readers:
        Type: Signature
        Rule: "OR('Org1MSP.admin', 'Org1MSP.peer', 'Org1MSP.client')"
    Writers:
        Type: Signature
        Rule: "OR('Org1MSP.admin', 'Org1MSP.client')"
    Admins:
        Type: Signature
        Rule: "OR('Org1MSP.admin')"
```

### 1.4 成员所拥有的 MSP 包含哪些内容？
MSP 中采用了基于ECDSA算法的非对称加密算法来生成公钥和私钥，而证书格式则采用了X.509的标准规范。
```
admincerts
cacerts
keystore
signcerts
tlscacerts
```

#### 1.5 MSP 如何参与运作？


配置模板文件
```
OrdererOrgs:
  - Name: Orderer
    Domain: example.com
    EnableNodeOUs: false
    Specs:
      - Hostname: orderer
PeerOrgs:
  - Name: Org1
    Domain: org1.example.com
    EnableNodeOUs: false
    CA:
      Hostname: ca # implicitly ca.org1.example.com
      Country: US
      Province: California
      Locality: San Francisco
      OrganizationalUnit: Hyperledger Fabric
      StreetAddress: address for org # default nil
      PostalCode: postalCode for org # default nil
    Specs:
     - Hostname: foo # implicitly "foo.org1.example.com"
       CommonName: foo27.org5.example.com # overrides Hostname-based FQDN set above
       SANS:
         - "bar.{{.Domain}}"
         - "altfoo.{{.Domain}}"
         - "{{.Hostname}}.org6.net"
         - 172.16.10.31
     - Hostname: bar
     - Hostname: baz

    Template:
      Count: 1
      Start: 5 # 默认从0开始
      Hostname: {{.Prefix}}{{.Index}} # default
      SANS:
       - "{{.Hostname}}.alt.{{.Domain}}"
    Users:
      Count: 1 # 生成除管理员外的账户，默认会生成一个管理员账户
```



EnableNodeOUs
