通过使用 ntfs-3g 来解决。  
打开ntfs-3g的下载点http://www.tuxera.com/community/ntfs-3g-download/ ，将最新稳定ntfs-3g_ntfsprogs-2014.2.15.tgz下载到linux系统中。  
执行以下命令编译安装ntfs-3g：
```  
# tar -zxvf ntfs-3g_ntfsprogs-2014.2.15.tgz
# cd ntfs-3g_ntfsprogs-2014.2.15
# ./configure
# make
# make install
# mount -t ntfs-3g  /dev/sdc1 /mnt/usb
```
人们通常把需要挂载的分区，挂载在`/mnt/`下。  
有时候，我们可能找不到对应的盘叫什么名字怎么呢？
可使用`sudo fdisk -l`来找到对应的盘:
```
[admin@localhost ~]$ sudo fdisk -l
[sudo] password for shrakie:
磁盘 /dev/sda：250.1 GB, 250058268160 字节，488395055 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x35bd35bc

   设备 Boot      Start         End      Blocks   Id  System
/dev/sda1            2048      616447      307200    6  FAT16
/dev/sda2       119754752   304072703    92158976    7  HPFS/NTFS/exFAT
/dev/sda3       304072704   488392703    92160000    7  HPFS/NTFS/exFAT
/dev/sda4          616448   119754751    59569152    5  Extended
/dev/sda5   *      618496     2715647     1048576   83  Linux
/dev/sda6         2717696    14632959     5957632   82  Linux swap / Solaris
/dev/sda7        14635008    85270527    35317760   83  Linux
/dev/sda8        85272576   119754751    17241088   83  Linux
```
通过上面的步骤，可能已经挂载好分区，可是每一次重启后，会发现所挂载的分区又消失了，
如何才能在每次启动后无需再次挂载呢？  
此时，我们需要了解fstab.
>关于fstab ,文件fstab包含了你的电脑上的存储设备及其文件系统的信息。使用fstab可以实现开机自动挂载各种文件系统格式的硬盘、分区、可移动设备和远程设备等。
让我们对fstab的用法进行一个详细的了解。一个典型的entry有下面的fields (fields用空格或tab分开):

关于配置/etc/fstab配置格式：
```
<file system>	<dir>	<type>	<options>	<dump>	<pass>
```
*file system*:设备名称，可以通过ls /dev查看。  
*dir*:期望挂载的目录，这个必须已经存在。  
*type*:指挂载设备或分区为何种文件系统类型（例如：ext2, ext3, reiserfs, xfs, jfs, smbfs, iso9660, vfat, ntfs, swap等）。  
*options*：选项。设置一些文件系统的具体选项。这里不详细介绍，具体说明：  
fat32文件系统配置如下：defaults,user,rw,codepage=936,iocharset=utf8，分配代表：默认，所有用户可以使用，可读可写，后面的一项为避免显示乱码。  
ntfs文件系统配置如下：defaults,user,rw,iocharset=utf8,umask=000,nls=utf8，分配代表：默认，所有用户可以使用，可读可写，后面的一项为避免显示乱码。  
*dump*：是dump utility用来决定是否做备份的. 大部分的用户是没有安装dump的，所以应该写为0。  
*pass*： fsck会检查这个头目下的数字来决定检查文件系统的顺序，配置成0的话，开机将不做检查。  
```
/dev/sda1 /mnt/windows ntfs-3g defaults 0 0
```
#### 判断fstab是否正确
可以使用sudo mount -a, －a参数表明使用/etc/fstab中的配置进行挂载。如果发现配置不正确，可以再使用sudo umount /dev/XXX卸载对应设备。这样避免了每次修改重启电脑。 对于挂载失败的原因，可以通过dmesg命令查看。
