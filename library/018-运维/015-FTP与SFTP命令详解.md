## FTP与SFTP命令详解
### FTP连接命令
```
D:\>ftp -h

将文件传送到运行 FTP 服务器服务(经常称为后台程序)的计算机以及将文件从该计算机
传出。可以交互使用 Ftp。

FTP [-v] [-d] [-i] [-n] [-g] [-s:filename] [-a] [-A] [-x:sendbuffer] [-r:recvbuf
fer] [-b:asyncbuffers] [-w:windowsize] [host]

  -v              禁止显示远程服务器响应。
  -n              禁止在初始连接时自动登录。
  -i              关闭多文件传输过程中的
                  交互式提示。
  -d              启用调试。
  -g              禁用文件名通配(请参阅 GLOB 命令)。
  -s:filename     指定包含 FTP 命令的文本文件；命令
                  在 FTP 启动后自动运行。
  -a              在绑字数据连接时使用所有本地接口。
  -A              匿名登录。
  -x:send sockbuf 覆盖默认的 SO_SNDBUF 大小 8192。
  -r:recv sockbuf 覆盖默认的 SO_RCVBUF 大小 8192。
  -b:async count  覆盖默认的异步计数 3
  -w:windowsize   覆盖默认的传输缓冲区大小 65535。
  host            指定主机名称或要连接到的远程主机
                  的 IP 地址。

注意:
  - mget 和 mput 命令将 y/n/q 视为 yes/no/quit。
  - 使用 Ctrl-C 中止命令。
```
### SFTP连接命令
```
D:\cron>sftp -h
usage: sftp [-1246aCfpqrv] [-B buffer_size] [-b batchfile] [-c cipher]
          [-D sftp_server_path] [-F ssh_config] [-i identity_file] [-l limit]
          [-o ssh_option] [-P port] [-R num_requests] [-S program]
          [-s subsystem | sftp_server] host
       sftp [user@]host[:file ...]
       sftp [user@]host[:dir[/]]
       sftp -b batchfile [user@]host

       -B              缓冲区大小
       -b              批处理命令
       -c              加密处理程序，如aes128-ctr,aes192-ctr,aes256-ctr等等
       -D              登录么服务器的路径。
       -F              SSH连接配置。
       -i              指定私钥登录文件
       -l              不知道是干啥的
       -o              SSH连接配置。
       -P              端口号
       -R              不知道是干啥的
       -S              不知道是干啥的
       -s              不知道是干啥的
       host            指定主机名称或要连接到的远程主机的 IP 地址。
```

### 交互命令
`SFTP`与`ftp`的连接命令差别非常大，参数几乎都不一样，但它们在与服务器的交互命令上，是
一致的。
```
sftp> help
Available commands:
bye                                Quit sftp
cd path                            Change remote directory to 'path'
chgrp grp path                     Change group of file 'path' to 'grp'
chmod mode path                    Change permissions of file 'path' to 'mode'
chown own path                     Change owner of file 'path' to 'own'
df [-hi] [path]                    Display statistics for current directory or
                                   filesystem containing 'path'
exit                               Quit sftp
get [-afPpRr] remote [local]       Download file
reget [-fPpRr] remote [local]      Resume download file
reput [-fPpRr] [local] remote      Resume upload file
help                               Display this help text
lcd path                           Change local directory to 'path'
lls [ls-options [path]]            Display local directory listing
lmkdir path                        Create local directory
ln [-s] oldpath newpath            Link remote file (-s for symlink)
lpwd                               Print local working directory
ls [-1afhlnrSt] [path]             Display remote directory listing
lumask umask                       Set local umask to 'umask'
mkdir path                         Create remote directory
progress                           Toggle display of progress meter
put [-afPpRr] local [remote]       Upload file
pwd                                Display remote working directory
quit                               Quit sftp
rename oldpath newpath             Rename remote file
rm path                            Delete remote file
rmdir path                         Remove remote directory
symlink oldpath newpath            Symlink remote file
version                            Show SFTP version
!command                           Execute 'command' in local shell
!                                  Escape to local shell
?                                  Synonym for help
```
我较关注的下载与上传命令`get`、`put`、`mget`、`mput`,其中可以看到可选参数`[-afPpRr]`,
对于此参数，一直比较疑惑，也无更多的说明。仔细收集一下，做以下总结:
```
-a
-f
-P
-p
-R
-r 表示下载或者上整个目录
```
