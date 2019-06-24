## 安装amqp扩展
### 安装rabbitmq-c
前往[github](https://github.com/alanxz/rabbitmq-c/releases)下载最新版的rabbitmq-c
```shell
$ wget https://github.com/alanxz/rabbitmq-c/archive/v0.9.0.tar.gz
$ tar -zxvf v0.9.0.tar.gz
$ cd rabbitmq-c-0.9.0
$ mkdir build && cd build
$ sudo cmake -DCMAKE_INSTALL_PREFIX=/usr/local/rabbitmq-c ..
$ sudo cmake --build .  --target install
$ sudo ln -s /usr/local/rabbitmq-c/lib64 /usr/local/rabbitmq-c/lib
```
> 注意，如果操作系统为64位的
```
/usr/local/rabbitmq-c
├── include
│   ├── amqp_framing.h
│   ├── amqp.h
│   ├── amqp_ssl_socket.h
│   └── amqp_tcp_socket.h
├── lib -> lib64
└── lib64
    ├── librabbitmq.a
    ├── librabbitmq.so -> librabbitmq.so.4
    ├── librabbitmq.so.4 -> librabbitmq.so.4.3.0
    ├── librabbitmq.so.4.3.0
    └── pkgconfig
        └── librabbitmq.pc
```
> 如果操作系统为32位的，安装完成后，可能是这样的
```
/usr/local/rabbitmq-c
├── include
│   ├── amqp_framing.h
│   ├── amqp.h
│   ├── amqp_ssl_socket.h
│   └── amqp_tcp_socket.h
├── lib
│   └── x86_64-linux-gnu
│       ├── librabbitmq.a
│       ├── librabbitmq.so -> librabbitmq.so.4
│       ├── librabbitmq.so.4 -> librabbitmq.so.4.3.0
│       ├── librabbitmq.so.4.3.0
│       └── pkgconfig
│           └── librabbitmq.pc
```
32位操作系统，在执行`pecl install amqp`命令前，需要把`/usr/local/rabbitmq-c/lib/x86_64-linux-gnu`下面的文件移动到`/usr/local/rabbitmq-c/lib`下面，否则会提示以下错误信息：
```
/usr/bin/ld: cannot find -lrabbitmq
collect2: error: ld returned 1 exit status
Makefile:221: recipe for target 'amqp.la' failed
make: *** [amqp.la] Error 1
ERROR: `make' failed
```

### 安装amqp扩展
```
$ sudo pecl install amqp
WARNING: channel "pecl.php.net" has updated its protocols, use "pecl channel-update pecl.php.net" to update
downloading amqp-1.9.4.tgz ...
Starting to download amqp-1.9.4.tgz (102,604 bytes)
........................done: 102,604 bytes
28 source files, building
running: phpize
Configuring for:
PHP Api Version:         20160303
Zend Module Api No:      20160303
Zend Extension Api No:   320160303
Set the path to librabbitmq install prefix [autodetect] : /usr/local/rabbitmq-c
```
