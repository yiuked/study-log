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

   



