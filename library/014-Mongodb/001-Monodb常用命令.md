## Monodb常用命令

#### 启动`mongod`并指定数据库路径
```
>mongod --dbpath=E:\mongodb\db
```
>测试是否已启动：http://localhost:27017/

#### 如果需要安装为windows服务，加上--install则可，如
```
>mongod --dbpath D:\mongodb\db --logpath=D:\mongodb\logs\mongodb.log --logappend --install
```
>注：以服务的形式安装必须指定日志路径

#### 以配置文件形式启动mongod

建立配置文件`mongod.conf`，并根据配置文件中的内容建立相应的目录与文件
```
#数据库路径
dbpath=D:\MongoDB\db
#日志输出文件路径
logpath=D:\MongoDB\logs\mongodb.log
#错误日志采用追加模式，配置这个选项后mongodb的日志会追加到现有的日志文件，而不是从新创建一个新文件
logappend=true
#启用日志文件，默认启用
journal=true
#这个选项可以过滤掉一些无用的日志信息，若需要调试使用请设置为false
quiet=true
#端口号 默认为27017
port=27017
#使用身份验证
auth=true
```
如果要安装为系统服务则加上 `--install`,否则去掉
```
>mongod --config D:\MongoDB\etc\mongod.conf --install
```
#### 如果安装了windows服务，现在不想用了，则可以通过以下方式删除
```
>sc delete MongoDB
```

#### 建立用户过程
如果是首次创建用户，请先将`auth`参数去掉后，启动`mongodb`
接下来登录`mongo`
```
>mongo
MongoDB shell version: 2.7.8
connecting to: test
```
切换到`admin`表
```
>use admin
```
首次执行由于没有任何用户，因此没有任何信息
```
>show collections
>db.createUser({
	user:"root",
	pwd:"root",
	#首先建立一个超级管理账户
	roles:["userAdminAnyDatabase", "dbAdminAnyDatabase"]
})
```

>记住，此处一定要切换到自己要添加用户的数据库上进行用户添加,否则默认添加的用户所关联的表依然为admin

```
>use mydb
>db.createUser({
	user:"mydb",
	pwd:"mypwd",
	#首先建立一个超级管理账户
	roles:["dbOwner"]
})
```

接下来，我们就可以使用以下命令连接`mongo`
```
mongo -umydb -pmypwd mydb
```
也可以在登录数据库后使用
```
db.auth('用户名','密码');
```
来验证.


#### 修改密码(需要切换到所归属数据库下操作)
修改数据库密码
```
db.changeUserPassword("reporting", "SOh3TbYhxuLiW8ypJPxmt1oOfL")
```
或者
```
use test
db.updateUser(
   "user123",
   {
      pwd: "KNlZmiaNUp0B",
      customData: { title: "Senior Manager" }
   }
)
```
#### 查询
```
db.col.find().pretty()
```
权限，以下仅为部分做为参考，更多详细可参考
https://docs.mongodb.com/manual/reference/built-in-roles/#built-in-roles
```
read
readWrite

dbAdmin
userAdmin
dbOwner
dbOwner 包含了dbAdmin、userAdmin、read、readWrite所有权限

userAdminAnyDatabase
dbAdminAnyDatabase
```
