本文使用操作系统：Centos 6；
原GCC版本：4.4.7；
目标：升级GCC到gcc-4.9.4
```shell
$wget http://mirrors.ustc.edu.cn/gnu/gcc/gcc-4.9.4/gcc-4.9.4.tar.gz；
$tar -xf gcc-4.9.4.tar.gz；
$cd gcc-4.9.4
$./contrib/download_prerequisites。#下载、配置、安装依赖库。
$mkdir gcc-build-4.9.4
$cd gcc-build-4.9.4
$../configure --enable-checking=release --enable-languages=c,c++ --disable-multilib
#--enable-languages表示你要让你的gcc支持那些语言，
#--disable-multilib不生成编译为其他平台可执行代码的交叉编译器。
#--disable-checking生成的编译器在编译过程中不做额外检查，
#--enable-checking=xxx来增加一些检查；
$make
$make install
$gcc -v # 如果显示的gcc版本仍是以前的版本，就需要重启系统
$which gcc # 查看gcc的安装位置
#/usr/local/bin/gcc -v #通常gcc都安装在该处位置，如果显示为
```
