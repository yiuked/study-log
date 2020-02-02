1. docker安装
```
version: '2'

networks:
  byfn:

services:
   couchdb.peer0.org1.36sn.com:
    container_name: couchdb.peer0.org1.36sn.com
    image: hyperledger/fabric-couchdb
    environment:
      - COUCHDB_USER=admin
      - COUCHDB_PASSWORD=admin
    volumes:
        - ../../data/peer0.org1.36sn.com:/var/couchdb/data
    ports:
      - 5984:5984
    networks:
      - byfn
```

2. web管理端
```
http://couchdb.peer0.org1.36sn.com:5984/_utils/
```
