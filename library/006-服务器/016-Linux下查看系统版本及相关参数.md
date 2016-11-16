## Linux下查看系统信息

1. [如何查看已安装的CentOS版本信息](#如何查看已安装的CentOS版本信息： "如何查看已安装的CentOS版本信息：")
1. [查看linux版本](#查看linux版本： "查看linux版本：")
1. [查看系统是64位还是32位](#查看系统是64位还是32位: "查看系统是64位还是32位:")

### 如何查看已安装的CentOS版本信息：  
1. 查看`/proc/version`文件  
```
[root@localhost ~]# cat /proc/version
Linux version 2.6.18-194.el5 (mockbuild@builder10.centos.org) (gcc version 4.1.2 20080704 (Red Hat 4.1.2-48)) #1 SMP Fri Apr 2 14:58:14 EDT 2010
```
2. `uname` 命令  
```
[root@localhost ~]# uname -a
Linux localhost.localdomain 2.6.18-194.el5 #1 SMP Fri Apr 2 14:58:14 EDT 2010 x86_64 x86_64 x86_64 GNU/Linux
```

### 查看linux版本：

1. 列出所有版本信息  
```
[root@localhost ~]# lsb_release -a
LSB Version:    :core-3.1-amd64:core-3.1-ia32:core-3.1-noarch:graphics-3.1-amd64:graphics-3.1-ia32:graphics-3.1-noarch
Distributor ID: CentOS
Description:    CentOS release 5.5 (Final)
Release:        5.5
Codename:      Final
#注:这个命令适用于所有的linux，包括RedHat、SUSE、Debian等发行版。
```

2. 执行`cat /etc/issue`例如如下  
```
[root@localhost ~]# cat /etc/issue
CentOS release 5.5 (Final)
Kernel r on an m
```

3. 执行`cat /etc/redhat-release` ,例如如下  
```
[root@localhost ~]# cat /etc/redhat-release
CentOS release 5.5 (Final)
```

### 查看系统是64位还是32位:

1. `getconf LONG_BIT or getconf WORD_BIT`  
```
[root@localhost ~]# getconf LONG_BIT
64
```
2. `file /bin/ls`
```
[root@localhost ~]# file /bin/ls
/bin/ls: ELF 64-bit LSB executable, AMD x86-64, version 1 (SYSV), for GNU/Linux 2.6.9, dynamically linked (uses shared libs), for GNU/Linux 2.6.9, stripped
```

3. `lsb_release  -a`
```
[root@localhost ~]# lsb_release -a
LSB Version:    :core-3.1-amd64:core-3.1-ia32:core-3.1-noarch:graphics-3.1-amd64:graphics-3.1-ia32:graphics-3.1-noarch
Distributor ID: CentOS
Description:    CentOS release 5.5 (Final)
Release:        5.5
Codename:      Final
```

5. 查看文件的方法。
```
vim /ect/issue
```
