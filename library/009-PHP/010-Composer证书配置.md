## Composer证书配置

在使用Composer时，经常会遇到这么一个问题
```
You are running Composer with SSL/TLS protection disabled.
```
现Composer官方所有的安装源都已采用https连接，因此当我们本地未启用openssl时则会报这个错误。

CA证书下载地址：http://curl.haxx.se/docs/caextract.html
然后修改php.ini文件
openssl.cafile= D:/wamp/php/verify/cacert.pem
