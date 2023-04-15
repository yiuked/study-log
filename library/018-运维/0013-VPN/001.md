生成服务端证书
```
sudo mkdir /etc/openvpn/easy-rsa/
sudo cp -r /usr/share/easy-rsa/3.0.8/* /etc/openvpn/easy-rsa/
sudo vim /etc/openvpn/easy-rsa/vars
```

在vars中写入以下内容
```
# 写入以下内容
export KEY_COUNTRY="US"
export KEY_PROVINCE="CA"
export KEY_CITY="SanFrancisco"
export KEY_ORG="MyOrganization"
export KEY_EMAIL="admin@myserver.com"
export KEY_OU="MyOrganizationalUnit"
```
初始化
```
sudo /etc/openvpn/easy-rsa/easyrsa init-pki
```
创建CA
```
sudo /usr/share/easy-rsa/3/easyrsa build-ca nopass
```

生成服务端与客户端证书
```
sudo /etc/openvpn/easy-rsa/easyrsa build-client-full server
sudo /etc/openvpn/easy-rsa/easyrsa build-client-full client
```

```
sudo mkdir /etc/openvpn/client
sudo cp /etc/openvpn/easy-rsa/pki/ca.crt /etc/openvpn/client/
sudo cp /etc/openvpn/easy-rsa/pki/issued/client.crt /etc/openvpn/client/
sudo cp /etc/openvpn/easy-rsa/pki/private/client.key /etc/openvpn/client/
```
生成客户端ovpn文件
```
sudo bash -c "openvpn --genkey --secret /etc/openvpn/easy-rsa/pki/ta.key && cat /etc/openvpn/client-template.txt \
<(echo -e '<ca>') \
/etc/openvpn/client/ca.crt \
<(echo -e '</ca>\n<cert>') \
/etc/openvpn/client/client.crt \
<(echo -e '</cert>\n<key>') \
/etc/openvpn/client/client.key \
<(echo -e '</key>\n<tls-auth>') \
/etc/openvpn/easy-rsa/pki/ta.key \
<(echo -e '</tls-auth>') \
> /etc/openvpn/client/client.ovpn"

```

操作
```
systemctl start openvpn@openvpn
systemctl restart openvpn@openvpn
systemctl stop openvpn@openvpn
```