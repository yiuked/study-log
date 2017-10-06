## 一次完整的Docker实作
原文地址：http://dockone.io/article/2125  
#### 1. client用pull命令从仓库把image拉到docker host
docker pull的格式是：
```
docker pull[选项] [Docker Registry地址] <仓库名>:<标签名>
```
默认地址是 DockerHub。 仓库名：这里的仓库名是两段式名称，既 / ，“/”前面一般是用户名。对于 Docker Hub，如果不给出用户名，则默认为 library ，也就是官方镜像。  

下载 Ubuntu14.04的image（以Ubuntu为例）：
```
baohua@ubuntu:~$docker pull ubuntu:14.04  
14.04:Pulling from library/ubuntu  
c60055a51d74:Downloading [>                                                 ] 539.8 kB/65.69 MB  
755da0cdb7d2:Download complete  
969d017f67e6:Download complete  
37c9a9113595:Download complete  
a3d9f8479786:Download complete  
…  
```
运行docker images命令看看下载的images：  
```
$docker images  
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE  
ubuntu            ml 14.04              b969ab9f929b        4 weeksago         188 MB  
```

#### 2. 在docker host上面运行Ubuntu 14.04于Containers

我们现在运行Ubuntu14.04中的bash shell，因为docker运行image于容器时，需要指定主进程（本例的主进程为bash）。   
在终端1上面运行：  
```
docker run -it --rm ubuntu:14.04 bash  
```
在终端2上面运行：  
```
docker run -it --rm ubuntu:14.04 bash  
```
这样我们就运行了Ubuntu 14.04这个image的2次实例（得到2个容器）, Linux下面的ps命令是看进程的，Docker下面就是看image的实例容器了。
```
$ docker ps  
CONTAINER ID       IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES  
e3a913872698       ubuntu:14.04       "bash"              11seconds ago      Up 10 seconds                           wizardly_elion  
db1c25753e97       ubuntu:14.04       "bash"              21seconds ago      Up 21 secon
```
image和container之间的关系类似程序与进程之间的关系，一个静若处子，一个动如脱兔。比如程序QQ，运行一次就是1个QQ进程，再运行一个QQ就是第2个QQ进程。同样道理，一个image也可以运行多份Container。
#### 3. 如何进入正在运行中的容器
**docker attach**  
使用方法：`docker attach  [container name]`  
适用范围：`docker`宿主机内部登录容器   
优点：快捷方便  
缺点：1.`exit`后直接退出该`container`
     2.多屏同步 这相当于同一时间最多只能有一个终端连接容器  

**docker exec***  
使用方法：`docker exec -it [container name] [command]`  
适用范围：docker宿主机内部登录容器  
优点：快捷方便  
缺点：外部终端无法使用这种方法登录容器  
使用参数介绍：  
```
-i, --interactive               Keep STDIN open even if not attached ————交互
-t, --tty                        Allocate a pseudo-TTY————分配伪终端
```
一般情况会使用`-it`这个组合命令，如果单用也只能单独使用`-i`命令   
-i 参数不会产生伪终端，但是会有正确的返回  
>使用-it时，则和我们平常操作console界面类似。而且也不会像attach方式因为退出，导致整个容器退出。这种方式可以替代ssh或者nsenter、nsinit方式，在容器内进行操作。

#### 3. 构建自己的image
现在想在Ubuntu 14.04中增加Vim和GCC，构建一个增量image，因为目前的Ubuntu image里面没有这样的命令：  
```
root@e3a913872698:/# vim  
bash: vim: command not found  
```
于是在Ubuntu 14.04这个image基础上面，叠加一层，然后把它提交到docker hub的21cnbao的仓库。    
我们需要在客户端电脑上面创建一个Dockerfile文件（该文件用于描述image），以实现在现有的Ubuntu 14.04上面做增量的目的。  
```
$ mkdir myubuntu  
$ cd myubuntu/  
$ touch Dockerfile  
```
用Vim编辑Dockerfile，添加如下内容：
```
# ubuntu 14.04 with vim and gcc  
FROM ubuntu:14.04  
MAINTAINER Barry Song<21cnbao@gmail.com>  
RUN apt-get update && apt-getinstall –y vim gcc  
```
RUN 指令的含义是在指定在源image内执行一条命令，本例更新APT 缓存，并且安装Vim和 GCC以形成一个增量image。  
下面build这个image：
```
$ docker build -t 21cnbao/myubuntu:14.04 .  
time="2017-02-21T06:48:07+08:00"level=info msg="Unable to use system certificate pool: crypto/x509: systemroot pool is not available on Windows"  
Sending build context to Docker daemon2.048 kB  
Step 1/3 : FROM ubuntu:14.04  
---> b969ab9f929b  
Step 2/3 : MAINTAINER Barry Song<21cnbao@gmail.com>  
---> Running in f1449746b58c  
---> 5dacd7a6ee5d  
Removing intermediate containerf1449746b58c  
Step 3/3 : RUN apt-get update &&apt-get install vim gcc  
---> Running in b1469caf3509  
Ign http://archive.ubuntu.com trustyInRelease  
Get:1 http://archive.ubuntu.comtrusty-updates InRelease [65.9 kB]  
Get:2 http://archive.ubuntu.comtrusty-security InRelease [65.9 kB]  
Get:3 http://archive.ubuntu.com trustyRelease.gpg [933 B]  
Get:4 http://archive.ubuntu.com trustyRelease [58.5 kB]  
Get:5 http://archive.ubuntu.comtrusty-updates/main Sources [485 kB]  
…  
```
下面运行21cnbao/myubuntu 14.04这个镜像：
```
docker run -it --rm 21cnbao/myubuntu:14.04 bash  
```
发现GCC和Vim都有了：
```
$ docker run -it --rm 21cnbao/myubuntu:14.04 bash  
root@f33ee07caf43:/#gcc  
gcc: fatal error: no input files  
compilation terminated.  
root@f33ee07caf43:/#  
```
#### 4. 通过docker push把image提交到仓库
在Docker Hub上面创建一个仓库myubuntu，该仓库创建后，全名将为21cnbao/myubuntu。  
下面push这个image到Docker Hub，之前我们需要登录到Docker Hub：  
```
$ docker login --username=21cnbao --email=21cnbao@gmail.com  
Flag--email has been deprecated, will be removed in 1.14.  
Password:  
Login Succeeded  
```
下面开始push：
```
$ docker push 21cnbao/myubuntu  
time="2017-02-21T07:17:59+08:00"level=info msg="Unable to use system certificate pool: crypto/x509: systemroot pool is not available on Windows"  
The pushrefers to a repository [docker.io/21cnbao/myubuntu]  
87157b68b121:Pushing [>                                                 ] 1.109 MB/134.7 MB  
c9fc7024b484:Pushing [==================================================>] 3.072 kB  
ca893d4b83a6:Pushing [==================================================>] 4.608 kB  
153bd22a8e96:Pushing 7.168 kB  
83b575865dd1:Pushing [==================================================>] 209.9 kB  
918b1e79e358:Waiting  
…  
```
通过Docker Hub进哥的仓库看一眼，发现大功告成了。
