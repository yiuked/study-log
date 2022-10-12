使用-v标记可以指定挂载一个本地民有目录到容器中去作为数据卷:
```
-v /home/wwwroot:/dockerhost/wwwroot:ro
```
Docker挂载数据卷默认权限是读写，用户也可以通过ro 指定为只读.
