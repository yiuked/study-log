删除已安装的Docker
```
# Uninstall installed docker
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```
更新yum安装源
```
# Set up repository
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# Use Aliyun Docker
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```
显示可安装版本
```
yum list docker-ce --showduplicates
```
安装指定版本
```
sudo yum install docker-ce-18.03.0.ce
```
设置镜像加速：
https://cr.console.aliyun.com/cn-chengdu/instances/mirrors

iptables -I INPUT -p tcp --dport 36580 -j ACCEPT
