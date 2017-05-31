# Validate 验证器使用

在我们`PHP`中用`curl`来访问数据接口的时候，有的时候根据具体情况需要加`header`头，
但是关于这个`json`的头的标示有，这里我就不写具体怎么初始化`curl`等一系列代码，只标注出有关`header`的
```php
array_push($header, 'Content-Type:application/json');
array_push($header, 'Accept:application/json');
curl_setopt($ch, CURLOPT_HTTPHEADER,$header);//curl设置header头
```

这两种写法有什么不一样呢,简单易懂的通俗的解释就是：
`Accept` 就表示接口要返回给客户端的数据格式，  
`Content-Type` 表示客户端发送给服务器端的数据格式。这个是写`REST`接口时候定义的  
正常如果服务器没定义`Accept`但是自己添加了的话 会报404 没找到对应接口.


## Laravel中如何定义Validate的结果输出格式.
从上面的内容中，可以得知，当我们在开发`REST`接口时，显示，我们提交的数据以及接收的数据都希望是`json`格式，因此
在使客户端发起请求时，一定要记得在请求头里添加以上两项，否则`Laravel`的验证器会默认重定向。
