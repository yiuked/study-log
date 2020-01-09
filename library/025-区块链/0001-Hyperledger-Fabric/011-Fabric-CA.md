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
crypto-config/ordererOrganizations/36sn.com/ca/root/msp
|-------------keystore
|---------------*_sk
|---------------IssuerRevocationPrivateKey
|---------------IssuerSecretKey
```

设置FABRIC_CA_CLIENT_HOME
```
export FABRIC_CA_CLIENT_HOME=crypto-config/ordererOrganizations/36sn.com/ca/root/tls
```
获取tlscacerts证书,该命令会生成以下文件结构
```
crypto-config/ordererOrganizations/36sn.com/ca/root/tls/msp
|-----------cacerts
|-----------keystore
|-------------*_sk
|-----------signcerts
|-------------cert.pem
|-----------tlscacerts
|-------------tls-localhost-9100.pem
|-----------user
|-----------IssuerPublicKey
|-----------IssuerRevocationPublicKey
```

重新整理文件结构
```
$srcMSP=crypto-config/ordererOrganizations/36sn.com/ca/root/tls/msp
$tlsDir=crypto-config/ordererOrganizations/36sn.com/ca/root/tls
$dstMSP=crypto-config/ordererOrganizations/36sn.com/ca/root/msp

cp $srcMSP/signcerts/* $tlsDir/server.crt
cp $srcMSP/keystore/* $tlsDir/server.key
mkdir -p $dstMSP/keystore
cp $srcMSP/keystore/* $dstMSP/keystore
mkdir -p $dstMSP/tlscacerts
cp $srcMSP/tlscacerts/* $dstMSP/tlscacerts/tlsca.${orgName}-cert.pem
if [ -d $srcMSP/tlsintermediatecerts ]; then
   cp $srcMSP/tlsintermediatecerts/* $tlsDir/ca.crt
   mkdir -p $dstMSP/tlsintermediatecerts
   cp $srcMSP/tlsintermediatecerts/* $dstMSP/tlsintermediatecerts
else
   cp $srcMSP/tlscacerts/* $tlsDir/ca.crt
fi
rm -rf $srcMSP $homeDir/enroll.log $homeDir/fabric-ca-client-config.yaml
```

标准化MSP
-------------------------------------------------
如何生成一个组织的MSP？
* 启动`fabric-ca-server`
```
export FABRIC_CA_SERVER_HOME=crypto-config/ordererOrganizations/36sn.com/ca/root
fabric-ca-server start -p 9100 -b admin:adminpw
```
