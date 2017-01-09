## CURL 操作详解

#### linux curl抓取网页：

抓取百度：
```
curl http://www.baidu.com
```

如发现乱码，可以使用iconv转码：
```
curl http://iframe.ip138.com/ic.asp|iconv -fgb2312
```
iconv的用法请参阅：在Linux/Unix系统下用iconv命令处理文本文件中文乱码问题

#### Linux curl使用代理：

linux curl使用http代理抓取页面：
```
curl -x 111.95.243.36:80 http://iframe.ip138.com/ic.asp|iconv -fgb2312
curl -x 111.95.243.36:80 -U aiezu:password http://www.baidu.com
```
使用socks代理抓取页面：
```
curl --socks4 202.113.65.229:443 http://iframe.ip138.com/ic.asp|iconv -fgb2312
curl --socks5 202.113.65.229:443 http://iframe.ip138.com/ic.asp|iconv -fgb2312
```
代理服务器地址可以从爬虫代理上获取。

#### linux curl处理cookies

接收cookies:
```
curl -c /tmp/cookies http://www.baidu.com #cookies保存到/tmp/cookies文件
```
发送cookies:
```
curl -b "key1=val1;key2=val2;" http://www.baidu.com #发送cookies文本
curl -b /tmp/cookies http://www.baidu.com #从文件中读取cookies
```

#### linux curl发送数据：

linux curl get方式提交数据：
```
curl -G -d "name=value&name2=value2" http://www.baidu.com
```
linux curl post方式提交数据：
```
curl -d "name=value&name2=value2" http://www.baidu.com #post数据
curl -d a=b&c=d&txt@/tmp/txt http://www.baidu.com #post文件
```

以表单的方式上传文件：
```
curl -F file=@/tmp/me.txt http://www.aiezu.com
```

相当于设置form表单的method="POST"和enctype='multipart/form-data'两个属性。

#### linux curl http header处理：

设置http请求头信息：
```
curl -A "Mozilla/5.0 Firefox/21.0" http://www.baidu.com #设置http请求头User-Agent
curl -e "http://pachong.org/" http://www.baidu.com #设置http请求头Referer
curl -H "Connection:keep-alive \n User-Agent: Mozilla/5.0" http://www.aiezu.com
```

设置http响应头处理：
```
curl -I http://www.aiezu.com #仅仅返回header
curl -D /tmp/header http://www.aiezu.com #将http header保存到/tmp/header文件
```

#### linux curl认证：
```
curl -u aiezu:password http://www.aiezu.com #用户名密码认证
curl -E mycert.pem https://www.baidu.com #采用证书认证
```
#### 其他：
```
curl -# http://www.baidu.com #以“#”号输出进度条
curl -o /tmp/aiezu http://www.baidu.com #保存http响应到/tmp/aiezu
```

#### 经验
linux 使用curl小经验教训：
http请求地址的url要使用""括起来。当有存在多个参数使用&连接时可能会出错。

原文地址：http://www.cnblogs.com/davidwang456/p/4266867.html
