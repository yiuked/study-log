场景：

        对Mysql 数据库中存储的 Json 、JsonArray 字段中指定字段做 like 模糊查询，在度娘的答案中辗转了许久，发现类似的提问很多，但很多都是千篇一律，牛头不对马嘴的无效复制文，因为项目需要，结合度娘某些类似答案思路和自己的多次尝试，找到了 目前 有效的模糊搜索方法，记录与此，给自己和大家食用。

      如有问题或其他更好的解决  JsonArray 模糊查询指定属性的方法，欢迎留言交流。

问题：

      解决Mysql 中  json、JsonArray 类型字段中指定属性的模糊查询问题

解决方法：

    话不多说，sql很简单，直接上代码：

   1. 解决json类型字段的模糊查询：

     存储的数据格式：`{"type": "10", "mobile": "13545678900", "countryCode": "86"}`

```sql
select * from a  where mobile_json->'$.mobile' like '%135%'
```
1.1 解决接送类型字段的精确查询

数据存储格式：`{"type": "10", "mobile": "13545678900", "countryCode": "86"}`
``` sql
select * from a where mobile_json-> '$.mobile' = 13545678900
```

 2. 解决 JsonArray 类型字段的模糊查询：

   存储的数据格式:` [{"type": "10", "mobile": "13545678900", "countryCode": "86"}]`
```sql
select * from a where mobile_json->'$[*].mobile' like '%135%'
```
2.1 解决 JsonArray 类型字段的精确查询：

 存储的数据格式: `[{"type": "10", "mobile": "13545678900", "countryCode": "86"}]`
```sql
select * from a where JSON_CONTAINS(mobile_json,JSON_OBJECT('mobile', "13545678900"))
```

以上两种解决方法，分别是针对 json 和 json 数组类型指定属性的查询方法，其中区别就是，json 数组的模糊查询方法中 $.mobile 改成 $[*].mobile 表示查询所有。
