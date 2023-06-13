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
* 向相关机构申请证书，如赛门铁克、GeoTrust、GMO GlobalSign、CFCA等，各家各有特征，可根据价格与需求量选择。  
* 选择后将server.csr提供给对方则可，申请后，1~2周内可收到证书及证书链。  
* 收到的证书通常会包含两部分，一部分即SSL证书，一部分为证书链（https://www.itsvse.com/thread-3979-1-1.html）。

--------------------------------------------------------------------------------
## 二、部署证书
证书格式转换:
https://help.aliyun.com/knowledge_detail/42214.html?spm=5176.11065259.1996646101.searchclickresult.93871631Q5pFdT

### 2.1 证书导入
* 开始 -〉运行 -〉MMC；
* 启动控制台程序，选择菜单“文件”中的”添加/删除管理单元”-> “添加”，从“可用的独立管理单元”列表中选择“证书”-> 选择“计算机帐户”；
* 在控制台的左侧显示证书树形列表，选择“个人”->“证书”，右键单击，选择“所有任务”-〉”导入”, 根据”证书导入向导”的提示，导入PFX文件（此过程当中有一步非常重要： “根据证书内容自动选择存储区”）。安装过程当中需要输入密码为您当时设置的密码。导入成功后,可以看到证书信息。

### 2.2 分配服务器证书
* 打开 IIS8.0 管理器面板,找到待部署证书的站点,点击“绑定”。
* 设置参数选择“绑定”->“添加”->“类型选择 https” ->“端口 443” ->“ssl 证书【导入的证书名称】” ->“确定”。
* SSL 缺省端口为 443 端口(请不要随便修改。 如果您使用其他端口如:8443,则访问时必须输入:https://www.domain.com:8443)。

## 存在CDN
阿里上传证书的时候，需要包含证书链
```
-----BEGIN CERTIFICATE-----
SSL证书
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
证书链
-----END CERTIFICATE-----
```
上传私钥的时候，如果私钥是加密的，需要进行解密后再上传

## 测试
可能通过以下连接测试证链是否正常:
https://www.geocerts.com/ssl-checker


参与资料:
https://help.aliyun.com/knowledge_detail/50239.html?spm=a2c4g.11186631.2.13.5a5f4a58iNSbMt#h2-url-1
