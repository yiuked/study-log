CentOS7
1. 安装依赖包
```
yum install -y yum-utils device-mapper-persistent-data lvm2
```
2. 添加Docker软件包源
```
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```
3. 更新yum包索引
```
yum makecache fast
```
4. 安装Docker CE
```
yum install docker-ce -y
```
5. 启动
```
systemctl start docker
```
6. 卸载
```
yum remove docker-ce
rm -rf /var/lib/docker
```
7. 安装docker-compose
```
yum install docker-compose
```
