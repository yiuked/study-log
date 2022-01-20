#### 软件简介



redis-search 是一款基于 [Redis](http://www.oschina.net/p/redis) 的高效搜索组件

## 特点

- 实时更新搜索索引
- 高效
- 分词搜索和逐字匹配搜索
- 别名搜索
- 支持 ActiveRecord 和 Mongoid
- 暂时只能用一个字段做为排序条件
- 中文同音词，汉语拼音搜索支持
- 可以用一些简单的附加条件组合搜索

## 快速启动

```
  redis:
    image: redislabs/redisearch:latest
    container_name: redis
    volumes:
      - ./depoly/components/redis/data:/data
    environment:
      TZ: Asia/Shanghai
    restart: always
    sysctls:
      net.core.somaxconn: 1024
    command: redis-server --requirepass 123456 --appendonly yes --loadmodule /usr/lib/redis/modules/redisearch.so --loadmodule /usr/lib/redis/modules/rejson.so
    ports:
      - 6379:6379
```

> redisearch 镜像已带了rejson模块,启动时加载进去则可