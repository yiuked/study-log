* 镜像文件下载

  ```
  https://buildlogs.centos.org/centos/7/docker/
  ```

  

* 修改安装源

  ```
  wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.163.com/.help/CentOS7-Base-163.repo
  yum clean all
  yum makecache
  ```

* 常用软件安装

  ```
  yum install -y initscripts
  yum install -y bash-completion.noarch
  yum install -y net-tools vim lrzsz wget tree screen lsof tcpdump
  ```

* 