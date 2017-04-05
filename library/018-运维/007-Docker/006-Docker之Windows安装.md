#### 安装之前先了解下关键概念：
在linux上安装Docker，你的机器即使localhost也是docker主机；在网络中，localhost是指您的计算机。docker主机是容器中在该机器上运行。说白了就是直接安装在linux上，英文翻译真蛋疼。  
在Windows安装，Docker守护进程运行Linux虚拟机内。您可以使用Windows的客户端与虚拟机中的Docker主机通信。这台主机中运行你的Docker容器。  

在Windows中，Docker主机地址是Linux VM的地址。当启动docker-machine虚拟机时会被分配一个IP地址。当你启动一个容器，容器的端口会映射到VM。

https://www.docker.com/toolbox

下载 完一路安装就行了


安装完成，启动：Docker Quickstart Terminal，首次启动会下载一个boot2docker.iso的镜像文件，
下载速度太慢，可以在此链接下载
https://github.com/boot2docker/boot2docker/releases
下载完成后，放在以下目录则可。
C:\Users\Administrator\.docker\machine\cache
