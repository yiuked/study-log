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
