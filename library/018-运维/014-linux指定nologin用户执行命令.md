为了安全，使用`nologin`账号来运行程序，
```
su -s /bin/bash -c "ls" www
```
这条命令到底做了什么呢？`su -s` 是指定`shell`，这里`www`用户是`nologin`用户，是没有默认的`shell`的，
这里指定使用`/bin/bash`, `-c` 后面接需要运行的命令， 后面`www`是用`www`用户来运行。

方法2：
```
sudo -u www command
```
这样也可以使用`www`用户来执行命令
