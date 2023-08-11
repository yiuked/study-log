1. 设置为表设置新增项时间。
```sql
`create_time` timestamp not null default current_timestamp
```
2. 当内容有更新时，自动更新更新字段。
```sql
`update_time` timestamp not null default current_timestamp on update current_timestamp
```
