某些网站系统需要用户上传图片等文件到某些目录下,难免程序有些漏洞,导致用户上传了php、cgi等等可执行的文件，导致网站陷入非常为难的境地. 此时我们可以通过nginx来禁止用户访问这些目录下的可执行文件。
nginx配置
```
location ~* /(images|cache|media|logs|tmp)/.*.(php|pl|py|jsp|sh|cgi)$ {
 return 403;
 error_page 403 /403_error.html;
 }
```
作用：在目录images、cache、media、logs、tmp目录下面的所有php、pl、py、jsp、sh、cgi都不能访问。
