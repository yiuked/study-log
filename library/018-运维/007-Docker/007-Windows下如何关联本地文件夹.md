## Windows下如何关联本地文件系统
在Linux下，我们可以通过数据卷或者数据容器对本地文件或者目录进行关联，那么在windows下我们该如何操作呢。  
如果你已经完成Docker在windows下的安装过程，那么你不定不会陌生，所谓的windows下运行Docker,
只不过是在windows下建立了一个虚拟机，加载了boot2dokcer.iso这个系统镜像，即我们在windows下创建
安装的Docker最终还是在linux内核中运行。  

既然如此，那么我们当然可以使用加载数据卷与数据容器的方式加载本地文件系统，可问题来了既然运行  
Docker是虚拟机，那么进行Docker关联时，也只能关联到虚拟机的文件系统，如何关联到我们的windows文件系统呢？  
此时，我们需要借助VMBox的强大功能：
（此处本来应该有图的，可是写主太懒了）
虚拟机列表-》选中加载boot2dokcer的主机-》配置-》共享文件夹-》固定分配
共享文件夹路径：windows文件目录  
共享文件夹名称：boot2dokcer关联目录  
关联好了，貌似需要重启Docker tools,或者VMBOX里的boot2dokcer主机。  
重启后，可以尝试：
```
docker-machine ssh
```
登录,boot2dokcer的终端查看是否已关联成功，在关联成功的情况下，我们就可以使用以下命令启动容器了.
```
docker run -tid -v /关联在boot2dokcer上的文件系统:/在容器里显示的文件系统 -pwindows上映射过来的端口:容器上需要映射的端口 --name 取个好听的名字 镜像名
docker run -tid -v /vm-www:/continar-www -p8080:80 --name docker-nginx nginx
```
