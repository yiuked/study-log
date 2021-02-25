# Elasticsearch 



## 账户安全

elasticsearch 默认没有提供账户安全，可以通过x-pack插件进行扩展。

1. 生成安全证书

```
bin/elasticsearch-certutil cert -out config/elastic-certificates.p12 -pass ""
```

2. 配置x-pack插件，在config/elasticsearch.yml中加入以下配置内容

```
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12
```

3. 生成密码

```
bin/elasticsearch-setup-passwords auto        // 自动生成密码
bin/elasticsearch-setup-passwords interactive // 设置自定义密码

Changed password for user apm_system
PASSWORD apm_system = dFRBkx1RW8oCxswiQW6r

Changed password for user kibana_system
PASSWORD kibana_system = tJNANrOt7vGfpHdBoZ6v

Changed password for user kibana
PASSWORD kibana = tJNANrOt7vGfpHdBoZ6v

Changed password for user logstash_system
PASSWORD logstash_system = cJPnErIHSyvQ4mR5Yppw

Changed password for user beats_system
PASSWORD beats_system = monfhoIx7vEf6oHyyP3H

Changed password for user remote_monitoring_user
PASSWORD remote_monitoring_user = rqo1dDDwdTtRaeASPafp

# 这个是超级管理员账户，可以用来登录 kibana面板
Changed password for user elastic
PASSWORD elastic = ahpWMK9wIm0VAIfHifHe
```

4. 数据操作接口

 ```
curl -XPUT http://localhost:9200/index1     // 创建索引index1
curl -XGET http://localhost:9200/index1     // 获取索引index1信息
curl -XDELETE http://localhost:9200/index1  // 删除索引index1

// 为索引添加mapping
curl -H "Content-Type: application/json" -XPOST 'http://localhost:9200/index1/_mapping/user?include_type_name=true' -d '
{
    "user":{
        "properties": {
            "uid": {"type": "text"},
            "name":{"type": "text"}
        }
    }
}'

// 创建索引时，同时创建mapping
curl -H "Content-Type: application/json" -XPUT 'http://localhost:9200/gogogo' -d '
{
    "mappings":{
        "dynamic":"true",
        "properties": {
            "uid": {"type": "text"},
            "name":{"type": "text"}
        }
    }
}
'



// 写入数据
curl -H 'Content-Type: application/json' -XPOST http://localhost:9200/index1/user -d '
{
    "uid": "abcdef",
    "name": "isname"
}
'

curl -XGET http://localhost:9200/index1/_search // 读取写入数据
// 更新数据
curl -H 'Content-Type: application/json' -XPOST http://localhost:9200/index1/user/rVSnz3cB7IZm39X_xjQA/_update -d '
{
	"doc":{
		"uid": "111111111"
	}
}
'
// 删除数据
curl -XDELETE http://localhost:9200/index1/user/rVSnz3cB7IZm39X_xjQA
 ```

5. 通过nginx建立安全访问

   ```
   htpasswd -c nginx/config/conf.d/passwd elk
   
   server {
       listen       80;
       server_name  localhost;
   
       #charset koi8-r;
       #access_log  /var/log/nginx/host.access.log  main;
   
       auth_basic "Please input password:";
       auth_basic_user_file /etc/nginx/conf.d/passwd;
   
   ```

   



