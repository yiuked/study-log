## Centos 6 32/64位系统下安装pptpd VPN服务
参考文档：  
http://wiki.diahosting.com  
http://wiki.diahosting.com/linux_extend/pptpd_for_centos6  

将以下内容另存为 `install_pptpd.sh` 然后自行安装则可以  
```
yum remove -y pptpd ppp
iptables --flush POSTROUTING --table nat
iptables --flush FORWARD
rm -rf /etc/pptpd.conf
rm -rf /etc/ppp

sed -i 's/net.ipv4.ip_forward = 0/net.ipv4.ip_forward = 1/g' /etc/sysctl.conf
sysctl -p
yum -y install make libpcap iptables ppp gcc-c++ logrotate tar cpio perl pam tcp_wrappers
arch=`uname -m`
wget wget http://wiki.diahosting.com/dload/pptpd-1.4.0-1.el6.$arch.rpm
rpm -ivh pptpd-1.4.0-1.el6.$arch.rpm

mknod /dev/ppp c 108 0
echo 1 > /proc/sys/net/ipv4/ip_forward
echo "mknod /dev/ppp c 108 0" >> /etc/rc.local
echo "echo 1 > /proc/sys/net/ipv4/ip_forward" >> /etc/rc.local
echo "localip 172.16.36.1" >> /etc/pptpd.conf
echo "remoteip 172.16.36.2-254" >> /etc/pptpd.conf
echo "ms-dns 8.8.8.8" >> /etc/ppp/options.pptpd
echo "ms-dns 8.8.4.4" >> /etc/ppp/options.pptpd

echo ms-dns 222.85.85.85 >> /etc/ppp/options.pptpd
echo ms-dns 222.88.88.88 >> /etc/ppp/options.pptpd

pass=`openssl rand 6 -base64`
if [ "$1" != "" ]
then pass=$1
fi

echo "vpn pptpd ${pass} *" >> /etc/ppp/chap-secrets

iptables -t nat -A POSTROUTING -s 172.16.36.0/24 -j SNAT --to-source `ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk 'NR==1 { print $1}'`
iptables -A FORWARD -p tcp --syn -s 172.16.36.0/24 -j TCPMSS --set-mss 1356
service iptables save

chkconfig iptables on
chkconfig pptpd on

service iptables start
service pptpd start

echo "VPN service is installed, your VPN username is vpn, VPN password is ${pass}"
```
