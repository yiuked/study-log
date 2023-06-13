
https://nginx.viraptor.info/

nginx 日志输出对应的文件目录
```
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
				  '$status $body_bytes_sent "$http_referer" '
				  '"$http_user_agent" "$http_x_forwarded_for" '
				  '"$document_root$uri"';
```
这样在日志中就会输出文件路径
```
127.0.0.1 - - [06/Jun/2023:18:37:12 +0800] "GET /adm/index.html HTTP/1.0" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36" "182.149.161.74" "/usr/share/nginx/html/index.html
```