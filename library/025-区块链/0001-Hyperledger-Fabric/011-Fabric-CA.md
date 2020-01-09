创建orderer
```
ORGS="\
   orderer:36sn.com:9100:9101:1 \
   peer:org1.36sn.com:9102:9103:2 \
   peer:org2.36sn.com:9104:9105:2 \
"
```
设置FABRIC_CA_SERVER_HOME
```
export FABRIC_CA_SERVER_HOME=crypto-config/ordererOrganizations/36sn.com/ca/root
```
启动`fabric-ca-server`
```
fabric-ca-server start -p 9100 -b admin:adminpw
```
此处会生成以下文件结构
```
crypto-config/ordererOrganizations/36sn.com/ca/root
|-----------msp
|-------------keystore
|---------------*_sk
|---------------IssuerRevocationPrivateKey
|---------------IssuerSecretKey
```

设置FABRIC_CA_CLIENT_HOME
```
export FABRIC_CA_CLIENT_HOME=crypto-config/ordererOrganizations/36sn.com/ca/root/tls
```
