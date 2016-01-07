Nginx 源码安装
1：首先安装Nginx所需要的库
a.GCC编译器
yum install -y gcc
b.G++编译器：C++来编译Nginx的http模块
yum install -y gcc-c++
c.PCRE库：正则表达式
yum install -y pcre pcre-devel
d.zlib库
对HTTP包的内容作gzip压缩
yum install -y zlib zlib-devel
e.OpenSSL开发库
如果服务器要支持在SSL协议上传输HTTP就需要OpenSSL
yum install -y openssl openssl-devel


2：准备磁盘目录
a.Nginx源码存放目录
b.Nginx编译阶段产生的中间文件存放目录
c.Nginx部署目录
d.Nginx日志存放目录

3：参数调整
配置高并发Web服务器还需要优化Linux内核参数
配置Nginx为静态Web内容服务器、反向代理服务器或是提供图片缩略图功能（实时压缩图片）的服务器时，其内核参数的调整都是不同的。
首先需要修改/etc/sysctl.conf 来更改内核参数

fs.file-max=999999
net.ipv4.tcp_tw_reuse= 1
net.ipv4.tcp_keepalive_time= 600
net.ipv4.tcp_fin_timeout= 30
net.ipv4.tcp_max_tw_buckets=5000
net.ipv4.ip_local_port_range= 1024 61000
net.ipv4.tcp_rmem=4096 32768 262142
net.ipv4.tcp_wmem=4096 32768 262142
net.core.netdev_max_backlog= 8096
net.core.rmem_default=262144
net.core.wmem_default= 262144
net.core.rmem_max=2097152
net.core.wmem_max=2097152
net.ipv4.tcp_syncookies=1
net.ipv4.tcp_max_syn.backlog=1024

参数说明：
file-max：这个参数表示进程（比如一个 worker 进程）可以同时打开的最大句柄数，这个参数直接限制最大并发连接数，需根据实际情况配置。　　
tcp_tw_reuse：这个参数设置为 1， 表示允许将 TIME-WAIT 状态的 socket 重新用于新的 TCP 连接，这对于服务器来说很有意义，因为服务器上总会有大量 TIME-WAIT 状态的连接。
tcp_keepalive_time：这个参数表示当 keepalive 启用时， TCP 发送 keepalive 消息的频度。默认是 2 小时，若将其设置得小一些，可以更快地清理无效的连接。
tcp_fin_timeout：这个参数表示当服务器主动关闭连接时， socket 保持在 FIN-WAIT-2 状态的最大时间。
tcp_max_tw_buckets： 这个参数表示操作系统允许 TIME_WAIT 套接字数量的最大值，如果超过这个数字， TIME_WAIT 套接字将立刻被清除并打印警告信息。该参数默认为 180000， 过多的 TIME_WAIT 套接字会使 Web 服务器变慢
tcp_max_syn_backlog： 这个参数表示 TCP 三次握手建立阶段接收 SYN 请求队列的最大长度，默认为 1024， 将其设置得大一些可以使出现 Nginx 繁忙来不及accept 新连接的情况时， Linux 不至于丢失客户端发起的连接请求。
ip_local_port_range： 这个参数定义了在 UDP 和 TCP 连接中本地（不包括连接的远端）端口的取值范围。
net.ipv4.tcp_rmem： 这个参数定义了 TCP 接收缓存（用于 TCP 接收滑动窗口）的最小值、默认值、最大值。
net.ipv4.tcp_wmem： 这个参数定义了 TCP 发送缓存（用于 TCP 发送滑动窗口）的最小值、默认值、最大值。
netdev_max_backlog： 当网卡接收数据包的速度大于内核处理的速度时，会有一个队列保存这些数据包。这个参数表示该队列的最大值。
rmem_ default： 这个参数表示内核套接字接收缓存区默认的大小。
wmem_ default： 这个参数表示内核套接字发送缓存区默认的大小。
rmem_ max： 这个参数表示内核套接字接收缓存区的最大大小。
wmem_ max： 这个参数表示内核套接字发送缓存区的最大大小。

4：下载Nginx并安装Nginx
注意，下载的时候，下载stable版本
cd /usr/local/
wget http://nginx.org/download/nginx-1.2.8.tar.gz
tar -zxvf nginx-1.2.8.tar.gz
cd nginx-1.2.8 
./configure --prefix=/usr/local/nginx/
make
make install

5：启动Nginx
cd /usr/local/nginx/sbin
./nginx
