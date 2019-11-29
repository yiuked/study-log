```
$docker run -t -i ...
```
-t 选项让Dokcer分配一个伪终端，并绑定容器的标准输入上。
-i 让容器的标准输入保持打开。

```
$docker run -d centos /bin/sh -c "while true;do echo hello world;sleep 1;done;"
$cfb21a35efe8ac28f41e5f2a0bf4ff18e035fa5e3bfae370671afaafa110ae48
```
-d 表示程序将在后台运行，命令执行后返返回一个唯一ID标识。
>在使用-d参数启动后的容器，可以使用attach、exec、nsenter与容器进行交互操作。
>docker attach cfb #这个操作将直接进入容器内。
>docker exec -ti cfb /bin/bash #ti与前面的ti参数同义，与attach最大的区别在于，exec可无需进入容器，直接将指令发送给容器。
>nsenter 在此不作描述

```
$docker stop cfb
```
stop 终止容器

```
$docker ps -a -q
```
-a 所有
-q 退出
显示所有终上的容器

```
$dokcer inspect cfb
```
查看某个容器的详细信息

```
$dokcer logs cfb
```
查看容器标准输出的日志

```
$dokcer export cfb>centos_cfb.tar
```
导出容器，

```
$docker import centos_8d35.tar local/centos
```
导入容器，准确的说应该是导入镜像，容器是无法导入的，当我们通过export导出容器快照，我们可
以通过import导入为镜像。


使用 docker network ls 查看docker容器中网络
