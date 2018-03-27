```
# 清除预设表filter中所有规则链中的规则。
iptables -F
# 清除预设表filter中使用者自定链中的规则。
iptables -X

# 首先禁止所有的包，然后根据需要的服务允许特定的包通过防火墙。
# 重要的事说三次、以下三条不要千万不要轻易执行，一但执行，如第一条，执行后，任何远程连接立即中断。
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# 或者允许所有的包，然后再禁止有危险的包通过放火墙。
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

# 向链中添加规则。下面的语句用于开放网络接口
# 仅允许IP为125.70.231.10的主机连接8080端口
iptables -A INPUT -s 120.55.118.86 -p tcp --dport 8080 -j ACCEPT
iptables -A OUTPUT -d 120.55.118.86 -p tcp --sport 8080 -j ACCEPT
# 任何主机都可以连接当前服务器的22端口
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

# 列出表/链中的所有规则
iptables -L -n

# 保存表
service iptables save
```
