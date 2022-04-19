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

> redis

### 查询语句

```
FT.SEARCH idx "@title|body:(hello world) @url|image:mydomain"
```

| SQL表达式                                | 对应Redis表达式                    | 描述                                     |
| ---------------------------------------- | ---------------------------------- | ---------------------------------------- |
| WHERE x='foo' AND y='bar'                | @x:foo @y:bar                      | for less ambiguity use (@x:foo) (@y:bar) |
| WHERE x='foo' AND y!='bar'               | @x:foo -@y:bar                     |                                          |
| WHERE x='foo' OR y='bar'                 | (@x:foo)\|(@y:bar)                 |                                          |
| WHERE x IN ('foo', 'bar','hello world')  | @x:(foo\|bar\|"hello world")       | quotes mean exact phrase                 |
| WHERE y='foo' AND x NOT IN ('foo','bar') | @y:foo (-@x:foo) (-@x:bar)         |                                          |
| WHERE x NOT IN ('foo','bar')             | -@x:(foo\|bar)                     |                                          |
| WHERE num BETWEEN 10 AND 20              | @num:[10 20]                       |                                          |
| WHERE num >= 10                          | @num:[10 +inf]                     |                                          |
| WHERE num > 10                           | @num:[(10 +inf]                    |                                          |
| WHERE num < 10                           | @num:[-inf (10]                    |                                          |
| WHERE num <= 10                          | @num:[-inf 10]                     |                                          |
| WHERE num < 10 OR num > 20               | @num:[-inf (10] \| @num:[(20 +inf] |                                          |
| WHERE name LIKE 'john%'                  | @name:john*                        |                                          |

索引操作

```
FT.DROPINDEX idx

FT.CREATE idx ON JSON PREFIX 1 blog:post: SCHEMA $.sku AS sku_text TEXT
FT.CREATE idx1 ON JSON PREFIX 1 blog:tag: SCHEMA $.sku AS sku_text TEXT

FT.CREATE idx ON JSON PREFIX 1 blog:post: SCHEMA $.sku AS sku_tag TAG


JSON.SET blog:post:1 $ '{"sku":"a,b,c"}'
JSON.SET blog:tag:1 $ '{"sku":"a,b,c"}'


FT.SEARCH idx '@sku_text:a,b,c'


FT.CREATE userIdx ON JSON SCHEMA $.user.name AS name TEXT $.user.tag AS country TAG
JSON.SET myDoc $ '{"user":{"name":"John Smith","tag":"foo,bar","hp":1000, "dmg":150}}'
FT.SEARCH userIdx '@name:(John)'


FT.CREATE musicItem_idx ON JSON SCHEMA
 $.id AS id NUMERIC SORTABLE
 $.data_type AS data_type TEXT
 $.name AS name TEXT
 $.singer AS singer TEXT
 $.duration AS duration NUMERIC SORTABLE
 $.play_total AS play_total NUMERIC SORTABLE
 $.collect_total AS collect_total NUMERIC SORTABLE
 $.hot_value AS hot_value NUMERIC SORTABLE
 $.tag_ids[0] AS tag1 TEXT
 $.tag_ids[1] AS tag2 TEXT
 $.tag_ids[2] AS tag3 TEXT
 $.tag_ids[3] AS tag4 TEXT
 $.tag_ids[4] AS tag5 TEXT
 $.tag_ids[5] AS tag6 TEXT
 $.tag_ids[6] AS tag7 TEXT
 $.tag_ids[7] AS tag8 TEXT
 $.tag_ids[8] AS tag9 TEXT
 $.tag_ids[9] AS tag10 TEXT
 
```

