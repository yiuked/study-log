
手动添加 Nginx 的第三方仓库，可以按照以下步骤操作：

1.  打开 `/etc/yum.repos.d/` 目录，并创建一个名为 `nginx.repo` 的文件，可以使用 vim 或 nano 等文本编辑器打开该文件。
    
2.  将以下文本复制到 `nginx.repo` 文件中：
    
    makefileCopy code
```
[nginx] 
name=nginx repo baseurl=http://nginx.org/packages/centos/$releasever/$basearch/ gpgcheck=0 
enabled=1
```
    
    以上文本指定了 Nginx 的仓库名称 `nginx`，仓库地址 `http://nginx.org/packages/centos/$releasever/$basearch/`，禁用 GPG 验证（因为官方仓库没有 GPG 验证），并启用该仓库。
    
3.  保存并关闭文件。
    
4.  运行 `yum update` 命令，让 Yum 知道您添加了一个新的仓库，并更新缓存。
    
5.  运行 `yum install nginx` 命令安装最新版本的 Nginx。