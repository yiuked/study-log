```
SELinux is preventing /usr/sbin/httpd from name_bind access on the tcp_socket port 。
# 查看开放的http端口列表
semanage port -l | grep http
# 添加一个端口
semanage port -a -t http_port_t -p tcp 9112
# 关闭端口
semanage port -d -t http_port_t -p tcp 5060
```

