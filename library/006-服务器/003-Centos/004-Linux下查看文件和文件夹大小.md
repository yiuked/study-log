## 与磁盘、文件夹相关的操作

* `df`
命令可以显示目前所有文件系统的可用空间及使用情形
```
$ df -h
```
* `du`
查询文件或文件夹的磁盘使用空间
如果当前目录下文件和文件夹很多，使用不带参数`du`的命令，可以循环列出所有文件和文件夹所使用的空间。  
这对查看究竟是那个地方过大是不利的，所以得指定深入目录的层数，参数：``--max-depth=``，这是个极为有用的参数！如下，注意使用 " * "，可以得到文件的使用空间大小.  
```
du -h --max-depth=1 work/testing
```

* lsblk
查看磁盘空间和分区：
```
# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
vda    253:0    0   80G  0 disk
└─vda1 253:1    0   80G  0 part /
vdb    253:16   0  120G  0 disk
```
> 也可用使用`fdisk -l`

* `fdisk /dev/vdb`
挂载磁盘vdb,可以根据提示进行分区。
> n 创建新分区，创建完成以后，一定要记得输入 w,写入分区表信息.

* mkfs格式化磁盘
```
mkfs.ext4 /dev/vdb1
```

* fstab 开机自动挂载

```
vim /etc/fstab
# <要挂载的分区> <挂载点> <格式类型> <挂载形式> <备份设置> <磁盘检查顺序>
/dev/vdb1 /data ext4 defaults 0 0
```
> 挂载形式:  
> auto: 系统自动挂载，fstab默认就是这个选项  
> defaults: rw, suid, dev, exec, auto, nouser, and async.  
> noauto 开机不自动挂载  
> nouser 只有超级用户可以挂载  
> ro 按只读权限挂载  
> rw 按可读可写权限挂载  
> user 任何用户都可以挂载  

> 备份设置:  0 不允许，1允许  

* mount
将磁盘挂载到指定目录
```
mount /dev/vdb1 /data
```
