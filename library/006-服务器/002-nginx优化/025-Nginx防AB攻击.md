Nginx(防止压力测试的恶意攻击)

ab压力测试工具命令：

ab -c 100 -n 1000 http://127.0.0.1/index.html

防止压力测试的恶意攻击的思路：

nginx限制同一个IP的并发最大为10，

vi /usr/local/nginx/conf/nginx.conf

在http{} 字段第一行添加：

limit_conn_zone $binary_remote_addr zone=one:10m;  

在对应的server{}里添加：

limit_conn one 10;

最后重启nginx，有两种方法：

./sbin/nginx -s reload;

service nginx reload;
