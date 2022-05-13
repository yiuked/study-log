Apache下Worker模式MPM参数分析
https://www.cnblogs.com/fjping0606/p/4759890.html

### 虚拟机配置
```
1.打开监听端口号
Listen 80
Listen 8080
Listen 9081

2.注示默认的主机
#ServerAdmin admin@phpStudy.net
#ServerName localhost
#DocumentRoot  "C:\phpStudy\ZSJR"
#<Directory />
#    Options +Indexes +FollowSymLinks +ExecCGI
#    AllowOverride All
#    Order allow,deny
#    Allow from all
#    Require all granted
#</Directory>

3.打开虚拟机文件
Include conf/extra/httpd-vhosts.conf

4.添加内容
<VirtualHost *:80> 
ServerAdmin webmaster@aa 
DocumentRoot C:/phpStudy/WWW  
ServerName aa 
ErrorLog logs/aa_log 
CustomLog logs/aa-access_log common
<Directory />
    Options +Indexes +FollowSymLinks +ExecCGI
    AllowOverride All
    Order allow,deny
    Allow from all
    Require all granted
</Directory>
</VirtualHost>

<VirtualHost *:9081> 
ServerAdmin webmaster@aa 
DocumentRoot C:/phpStudy/ZSJR 
ServerName bb 
ErrorLog logs/aa_log 
CustomLog logs/aa-access_log common
<Directory />
    Options +Indexes +FollowSymLinks +ExecCGI
    AllowOverride All
    Order allow,deny
    Allow from all
    Require all granted
</Directory> 
</VirtualHost>

注:
一定要加上，这部分对网站的访问权限进行配置
<Directory />
    Options +Indexes +FollowSymLinks +ExecCGI
    AllowOverride All
    Order allow,deny
    Allow from all
    Require all granted
</Directory>   
```