#### 使用RSA算法：
生成私钥：
```
openssl genrsa -out privatekey.key 1024
```
对应公钥：
```
openssl rsa -in privatekey.key -pubout -out pubkey.key
```

#### 使用DSA算法：
生成`DSA`参数：
```  
openssl dsaparam -out dsa_param.pem 1024
```
生成私钥：
```
openssl gendsa -out dsa_private_key.pem dsa_param.pem
```
对应公钥：
```
openssl dsa -in dsa_private_key.pem -pubout -out dsa_public_key.pem
```
