## Ubuntu

### 安装源

将`/etc/apt/sources.list`内容替换为以下内容

```
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
##测试版源
deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse
# 源码
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
##测试版源
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse
# Canonical 合作伙伴和附加
deb http://archive.canonical.com/ubuntu/ xenial partner
deb http://extras.ubuntu.com/ubuntu/ xenial main
```
然后执行
```
sudo apt update
```

### 软件兼容

| 系统版本  | 软件                    |
| --------- | ----------------------- |
| ubuntu 16 | mysql5.6                |
| ubuntu 18 | mysql5.7、xtrabackup2.3 |
| ubuntu 20 | xtrabackup2.4           |

安装指定版本软件 

```
add-apt-repository 'deb http://archive.ubuntu.com/ubuntu trusty main'
apt-get update
apt-cache search mysql | grep 5.6
apt install mysql-server-5.6
```

