```
docker run --rm -v "//var/run/docker.sock:/var/run/docker.sock" docker-in-docker-non-root /bin/sh -c "docker ps"
```

Docker采取的是C/S架构，Docker的成功运行需要Docker Daemon和Docker Client(客户端)的支持，当我们运行一些docker build等命令时，实际是需要Docker Client连接Docker Daemon发送命令，Docker Daemon会在宿主机操作系统分配文件、网络等资源。

![img](../../../images/typora/webp.webp)