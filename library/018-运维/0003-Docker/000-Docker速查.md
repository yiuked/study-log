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

* docker 日志

  ```
  docker logs [OPTIONS] CONTAINER
   
  Options:
   
  --details 显示更多的信息
   
  -f, --follow 实时输出日志，最后一行为当前时间戳的日志
   
  --since string 输出日志开始日期，即只输出指定日期之后的日志。
   
  --tail string 显示最后多少行日志， 默认是all
              （如： -tail=10 : 查看最后的 10 行日志。）
   
  -t, --timestamps 显示时间戳
  ```


**对日志进行过虑**

通过`docker logs cfb|grep test`会输出所有日志, 这是因为管道仅对stdout有效，如果容器将日志记录到stderr，这种情况就会发生，这时可以尝试这样写:

```
docker logs cfb 2>&1|grep 'test'
```

```
# 基于当前文件夹下的 dockerfile 创建一个镜像
docker build -t helloworld .      
# 上面指令的全写
docker build --tag=helloworld .
# 运行这个镜像，并将本机 4000 端口映射到容器对外暴露的 80 端口，外部通过 4000端口访问 
docker run -p 4000:80 helloworld 
# 使 container 在后台运行
docker run -d -p 4000:80 helloworld 
# 所有正在运行的容器列表
docker container ls                        
# 所有容器列表
docker container ls -a  
# 停用一个容器
docker container stop <hash>
# 强制停止一个容器
docker container kill <hash>
# 移除一个容器
docker container rm <hash>  
# 移除所有容器
docker container rm $(docker container ls -a -q)
# 所有镜像列表
docker image ls -a 
# 移除一个镜像
docker image rm <image id> 
# 移除所有镜像
docker image rm $(docker image ls -a -q) 
# 登录注册过的 docker hub
docker login 
# 为镜像打标签
docker tag <image> username/repository:tag
# 将镜像推送至远程仓库
docker push username/repository:tag 
# 运行这个镜像
docker run username/repository:tag
```

