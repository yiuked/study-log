## 一、申请证书
向证书提供商申请证书时，需要向提供商提交csr文件(生成一对对称密钥，然后将公钥提供给提供商)。
### 1.1 成生csr文件
生成csr文件的方式很多种，如openssl，网上在线生成工具等。
1. 推荐一个在线生成csr文件的地址，除了生成csr文件，还附带其它的功能，比较全：  
https://www.myssl.cn/tools/create-csr.html

2. 使用`openssl`进行生成:

```
$ openssl req -new -newkey rsa:2048 -nodes -keyout server.key -out server.csr
Generating a 2048 bit RSA private key
.................................................+++++
............................+++++
writing new private key to 'server.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN # 中国写CN
State or Province Name (full name) [Some-State]:Sichuan # 省/州
Locality Name (eg, city) []:Chengdu # 城市
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Chengdu XXX Ltd # 公司名
Organizational Unit Name (eg, section) []:Technology Department # 部门，如技术部或者运维部
Common Name (e.g. server FQDN or YOUR name) []:www.example.com # 域名
Email Address []:service@example.com # 邮箱地址

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []: # 私钥保护密码 [非必填]
An optional company name []: # 可选公司名称 [非必填]
```
更多关于openssl的详解可以参考：https://www.jianshu.com/p/56f7a350b0ab

### 1.2 申请证书
--------------------------------------------------------------------------------
##
