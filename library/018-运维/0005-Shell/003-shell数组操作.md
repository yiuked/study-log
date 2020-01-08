```
#!/bin/bash +x

ORGS="\
   orderer:36sn.com:9100:9101:1 \
   peer:org1.36sn.com:9102:9103:2 \
   peer:org2.36sn.com:9104:9105:2 \
"

# Setup orderer and peer organizations
function setupOrgs {
   for ORG in $ORGS
   do
      echo $ORG
      sleep 1
   done
}

setupOrgs
```
