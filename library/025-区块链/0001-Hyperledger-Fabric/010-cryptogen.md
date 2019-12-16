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
我猜想 fabric 会根据证书中的`OrganizationalUnit`来识别当前证书的角色,`OrganizationalUnit`是一个数组，
因此它可以同时分担多个角色。

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


一个标准的配置模板文件
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

cryptogen 中，要生成一个组织所包含的 msp 最少需要以下内容组成。
1. 该组织必须具备 ca 与 tlsca 私钥各一份，经过x509标准的公钥证书各一份。
2. 由 ca 与 tlsca x509标准的公钥证书组成的组织 msp 一份。
3. peer 节点的私钥一份，经过x509标准的公钥证书，结合组织的 ca 与 tlsca 的x509标准的公钥证书组成 peer 节点的msp
4. 至少存在一个管理员，管理员需要自己的私钥一份，经过x509标准的公钥证书，结合组织的 ca 与 tlsca 的x509标准的公钥证书组成 user 节点的msp
> 合计：四份私钥、 x509标准的公钥证书四份

EnableNodeOUs

暂时没有任何方法证明`admincerts`与 msp 是否为管理员 msp 有关系。

### 关于x.509
X.509 是密码学里公钥证书的格式标准。X.509 证书己应用在包括TLS/SSL（WWW万维网安全浏览的基石）在内的众多 Internet协议里。
同时它也用在很多非在线应用场景里，比如电子签名服务。X.509证书里含有公钥、身份信息(比如网络主机名，组织的名称或个体名称等)和签名信息（可以是证书签发机构CA的签名，也可以是自签名）。
对于一份经由可信的证书签发机构签名或者可以通过其它方式验证的证书，证书的拥有者就可以用证书及相应的私钥来创建安全的通信，对文档进行数字签名。

证书组成结构
证书组成结构标准用ASN.1(一种标准的语言)来进行描述. X.509 v3数字证书结构如下：
* 证书
  - ...
  - 公钥算法
  - 主题公钥
  - 此日期前无效
  - 此日期后无效
  - 版本号
  - 序列号
  - 签名算法
  - 颁发者
  - 证书有效期
  - 主题
  - 主题公钥信息
  - 颁发者唯一身份信息（可选项）
  - 主题唯一身份信息（可选项）
  - 扩展信息（可选项）
* 证书签名算法
* 数字签名
