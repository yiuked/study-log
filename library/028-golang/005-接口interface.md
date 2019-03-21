## 接口interface
### 目的
通过接口实现一个通用的数据连接驱动器。定义一个DB接口，包含一个基本的Connect方法。任何连接数据驱动，必须实现该接口。
### 接口定义
接口是一种约束形式，其中只包括成员定义，不包含成员实现的内容。主要目的是为不相关的类提供通用的处理服务。Golang中，一个类型可以同时实现多个接口。但每一个接口中的方法必须全部实现，否则实现接口失败。
```
DB interface
    |
  __|__
\|/   \|/
MYSQL  MSSQL
```
### 接口类型

### 接口实现
声明Mysql与Mssql两种类型，两种类型均实现了Dbinter接口。
```
// 定义接口
type DBinter interface {
	connect(dns string) (result DBinter, err error)
}

// 实现接口
type Mysql struct {
}

func (db *Mysql) connect(dns string) (result DBinter, err error) {
	fmt.Println("Connect MySQL success!")
	return db, nil
}

// 实现接口
type Mssql struct {
}

func (db *Mssql) connect(dns string) (result DBinter, err error) {
	fmt.Println("Connect MSSQL success!")
	return db, nil
}
// 定义应用层操作类型
type DB struct {
	driver map[string]DBinter
}
// 注册
func (db *DB) register(name string, driver DBinter) {
	if db.driver == nil {
		db.driver = make(map[string]DBinter)
	}
	if _, err := db.driver[name]; !err {
		db.driver[name] = driver
	}
}
// 获取
func (db *DB) instance(name string) (driver DBinter, err error) {
	if driver, err := db.driver[name]; err {
		return driver,nil
	}
	return nil,err
}

func main() {
	var db DB
	var mysql Mysql
	var mssql Mssql

	db.register("mysql", &mysql)
	db.register("mssql", &mssql)

	mysqlDb,_ := db.instance("mysql")
	mysqlDb.connect("127.0.0.1")
	mssqlDb,_ := db.instance("mysql")
	mssqlDb.connect("127.0.0.1")
}
```

### 接口应用
