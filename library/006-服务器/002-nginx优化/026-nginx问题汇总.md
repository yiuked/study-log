1. 谷歌报-ERR_SSL_PROTOCOL_ERROR,狐报-SSL 接收到一个超出最大准许长度的记录【ssl_error_rx_record_too_long

   修改配置文件：

```
# listen 443; 
listen 443 default ssl;
```

2. 服务器返回 415 错误

   415 错误上传文件大小超出限制

```
http{
	client_max_body_size  8M;
}
```



