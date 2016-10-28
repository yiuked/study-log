进入`git bash`运行：  
`ssh-keygen`

生成文件后，到`Git`后台的`ssh`配置里，添加新的一条记录，名称随意，内容为`id_rsa.pub`的内容  
接下来，使用  
`ssh -T git@code.test.com`

测试，如果成功，则会显示  
 `**** Welcome to JD code hosting service ***`

如果显示  
`The authenticity of host 'code.jd.com (211.151.12.193)' can't be established.`  
等错误，可以重新输入一次  
`ssh -T git@code.test.com`  
在提示你输入`<yes/no>?`的时候，输入 `yes` (默认是`no`)
会有更详细的错误信息
通常找到`.ssh`目录，删除`known_hosts`文件则可

如果出现  
`Permission denied (publickey)`
那么使用  
`ssh -v git@code.test.com`
这个能够看到具体加载的是哪个公钥文件，通常是由于加载的公钥文件位置不正确影响的。  
在使用`git`连接远程服务器时  
不要使用`sudo`,否则系统会到`root`目录下去找公钥文件而不是当前用户.  
此为，如果`git`之前连接远程仓库用的是`https`，要改成`ssh`则可找到`.git/config`   
将`url`替换成`ssh`地址则可  
