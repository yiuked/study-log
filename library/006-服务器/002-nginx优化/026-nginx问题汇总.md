错误信息：

谷歌报-ERR_SSL_PROTOCOL_ERROR，

火狐报-SSL 接收到一个超出最大准许长度的记录【ssl_error_rx_record_too_long】，

环境信息：

LNMP一键安装包

解决方案：

修改配置文件 /usr/local/nginx/config/***.com.conf

修改server里面的 listen 443;  为  listen 443 default ssl;  保存，重启Nginx。完美解决！
————————————————
版权声明：本文为CSDN博主「任Sir」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq371959453/article/details/80508518
