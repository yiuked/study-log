### 安装

```
yum -y install epel-release
yum -y install fail2ban
```

### 配置文件类型

```
/etc/fail2ban                  ## fail2ban 服务配置目录
/etc/fail2ban/action.d         ## iptables 、mail 等动作文件目录
/etc/fail2ban/filter.d         ## 条件匹配文件目录，过滤日志关键内容
/etc/fail2ban/jail.d           ## 规则文件目录，按具体防护项目分成文件
/etc/fail2ban/jail.local       ## 默认规则文件
/etc/fail2ban/jail.conf        ## fail2ban 防护配置文件
/etc/fail2ban/fail2ban.conf    ## fail2ban 配置文件，定义日志级别、日志、sock 文件位置等
```

### 配置文件模板

```
[DEFAULT]
ignoreip = 127.0.0.1/8
bantime  = 300
findtime = 600
maxretry = 5
banaction = firewallcmd-ipset
action = %(action_mwl)s
backend = auto

[sshd]
enabled = true
filter  = sshd
port    = 22
action = %(action_mwl)s
logpath = /var/log/secure

[womlogin]
enabled = true
port = 9211
filter = nginx-login-request
logpath = /var/log/nginx/womapi_access.log
```

>[DEFAULT] 组内容 表示默认参数值
>
>ignoreip：IP白名单，白名单中的IP不会屏蔽，可填写多个以（,）分隔
>bantime：屏蔽时间，单位为秒（s）
>findtime：时间范围
>maxretry：最大次数
>banaction：屏蔽IP所使用的方法，上面使用firewalld屏蔽端口
>action：采取的行动，可选值（action_mw、action_mwl）对应（/etc/fail2ban/action.d/mail-whois.conf、/etc/fail2ban/action.d/mail-whois-lines.conf）两个模板
>destemail 收件人地址
>mta 使用哪个发送邮件命令，可以选mail或sendmail
>
>[sshd]
>...
>[womlogin]
>...
>
>可以定义多个项目
>enabled 表示启用当前项目
>filter 当前项目采用哪个规则（放在filter.d目录下以.conf结尾，比如sshd.conf那个值填写sshd）
>logpath 监听哪个日志文件可以写多个
> ```
> logpath  = /home/wwwlogs/access.log
           /home/wwwlogs/www.imydl.com.log
           /home/wwwlogs/www.imydl.tech.log
           /home/wwwlogs/service.imydl.com.log
           /home/wwwlogs/eat.ymanz.com.log
      ```



默认情况下，Fail2Ban 将所有配置文件保存在 /etc/fail2ban/ 目录中。  
主配置文件是 jail.conf，它包含一组预定义的过滤器。所以，不要编辑该文件，这是不可取的，因为只要有新的更新，配置就会重置为默认值。  
只需在同一目录下创建一个名为 jail.local 的新配置文件，并根据您的意愿进行修改

```
#新建配置
vi /etc/fail2ban/jail.local
# 默认配置
[DEFAULT]
ignoreip = 127.0.0.1/8
bantime  = 86400
findtime = 600
maxretry = 5
# 这里banaction必须用firewallcmd-ipset,这是fiewalll支持的关键，如果是用Iptables请不要这样填写
# banaction = iptables-multiport
banaction = firewallcmd-ipset
action = %(action_mwl)s
destemail = xxxxx@qq.com
mta = mail
backend = auto
```

参数说明：

```bash
ignoreip：IP白名单，白名单中的IP不会屏蔽，可填写多个以（,）分隔
bantime：屏蔽时间，单位为秒（s）
findtime：时间范围
maxretry：最大次数
banaction：屏蔽IP所使用的方法，上面使用firewalld屏蔽端口
action：采取的行动，可选值（action_mw、action_mwl）对应（/etc/fail2ban/action.d/mail-whois.conf、/etc/fail2ban/action.d/mail-whois-lines.conf）两个模板
destemail 收件人地址
mta 使用哪个发送邮件命令，可以选mail或sendmail
```

> https://www.gaoyaxuan.net/blog/335.html

```
# 查看规则是否生效
fail2ban-regex /var/log/gorm.log /etc/fail2ban/filter.d/gogs.conf --print-all-matched
```
### 状态

1. **查看启用的监狱列表**

```
fail2ban-client status
```

2. **运行以下命令来获取sshd服务被禁止的 IP 地址**

```
fail2ban-client status sshd
```

3. **要从 Fail2Ban 中删除禁止的 IP 地址**

```
fail2ban-client set ssh unbanip 104.218.13.80
```

显示防火墙规则：

```text
iptables -L
```

显示防火墙规则对应的命令：

```text
iptables -S
```

```text
systemctl restart fail2ban.service
```

### firewall-cmd 相关操作

```bash
#查看Firewalld状态
systemctl status  firewalld
#启动firewalld
systemctl start firewalld
#设置开机启动
systemctl enable firewalld.service
#放行22端口
firewall-cmd --zone=public --add-port=80/tcp --permanent
#重载配置
firewall-cmd --reload
#查看已放行端口
firewall-cmd --zone=public --list-ports

```
