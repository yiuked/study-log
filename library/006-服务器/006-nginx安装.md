### nginx 简介  
`nginx` 全名 `engine`  可读作"恩几可思"  

#### 下载
到http://nginx.org/en/download.html  下载最新版的`Stable version`版本  

#### 安装
```
tar -zxvf xx.tgr.gz
cd xx/
./configure --prefix=/usr/local/nginx
```

如果出现  
```
./configure: error: the HTTP rewrite module requires the PCRE library.
```
则安装依赖程序  
```
yum -y install pcre-devel
yum -y install openssl openssl-devel
```

然后再次执行安装
```  
./configure --prefix=/usr/local/nginx
make
make install
```

安装完后通过
```
/usr/local/nginx/sbin/nginx -t //检查是否安装正确
/usr/local/nginx/sbin/nginx //启动nginx
/usr/local/nginx/sbin/nginx -s reload //重启
```

#### 配置
```
/usr/local/nginx/conf
```

#### 说明
正常情况下，`nginx`应该是主进程以`root`运行,子进程以`nobody`运行，为了保持权限一致，`php-fpm`也应该如此.  
