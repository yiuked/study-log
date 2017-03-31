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

docker stop cfb
stop 终止容器

docker ps -a -q
-a 所有
-q 退出
显示所有终上的容器
