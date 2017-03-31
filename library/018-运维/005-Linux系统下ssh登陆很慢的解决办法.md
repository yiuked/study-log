我们编辑sshd_config 这个文件：  
```
vi /etc/ssh/sshd_config
```
找到UseDNS我们把前面的#号去了，然后把yes 改变为no，
```  
UseDNS no。
```
然后保存退出，再重启下ssh服务测试下就可以了，
```
service sshd restart。
```
