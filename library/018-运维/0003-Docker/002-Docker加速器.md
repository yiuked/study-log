### MACOS
右键点击桌面顶栏的 docker 图标，选择 Preferences ，在 Advanced 标签下的 Registry mirrors 列表中加入下面的镜像地址:
```
http://c1b6a867.m.daocloud.io
```
点击 Apply & Restart 按钮使设置生效。

### Windows
在桌面右下角状态栏中右键 docker 图标，修改在 Docker Daemon 标签页中的 json ，把下面的地址:
```
http://c1b6a867.m.daocloud.io
```  
加到"registry-mirrors"的数组里。点击 Apply 。


### Linux
```
curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://c1b6a867.m.daocloud.io
```
该脚本可以将 --registry-mirror 加入到你的 Docker 配置文件 /etc/default/docker 中。适用于 Ubuntu14.04、Debian、CentOS6 、CentOS7、Fedora、Arch Linux、openSUSE Leap 42.1，其他版本可能有细微不同。更多详情请访问文档。

引用地址:
https://www.daocloud.io/mirror#accelerator-doc

### 修改文件
1. 安装／升级Docker客户端
推荐安装1.10.0以上版本的Docker客户端，参考文档 docker-ce

2. 配置镜像加速器
针对Docker客户端版本大于 1.10.0 的用户

您可以通过修改daemon配置文件`/etc/docker/daemon.json`来使用加速器
```
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://5kmuleak.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```
