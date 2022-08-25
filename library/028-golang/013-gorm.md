```go
type RepayMethod struct {
	ID          uint   `gorm:"primary_key"`
	Alias       string `gorm:"type:varchar(32) not null COMMENT '引用别名';primary_key"`
	Name        string `gorm:"type:varchar(64) not null COMMENT '还款名称'"`
	PeriodUnit string `gorm:"type:varchar(32) not null COMMENT '周期单位:day|month|quarter|year'"`
	PeriodName  string `gorm:"type:varchar(64) not null COMMENT '周期显示名,如年、月、季、日'"`
}

type Project struct {
	gorm.Model
	Nid                string      `gorm:"type:varchar(64) not null COMMENT '标的号';primary_key"`
	Name               string      `gorm:"type:varchar(64) not null COMMENT '标的名称'"`
	Account            float64     `gorm:"type:int(10) not null COMMENT '金额'"`
	RepayMethod        string      `gorm:"type:varchar(32) not null COMMENT '还款方式'"`
	RepayMethods       RepayMethod `gorm:"ForeignKey:Alias;AssociationForeignKey:RepayMethod"`
}

```
* ForeignKey             外部表与本表关联的字段             
* AssociationForeignKey  当前表用于与外部表关联的字段


* 创建表时指定存储引擎
```go
DB.Set("gorm:table_options","ENGINE=InnoDB").AutoMigrate(
```



## 带条件的预加载

GORM 允许带条件的 Preload 关联

```go
// 带条件的预加载 Order
db.Preload("Orders", "state NOT IN (?)", "cancelled").Find(&users)
// SELECT * FROM users;
// SELECT * FROM orders WHERE user_id IN (1,2,3,4) AND state NOT IN ('cancelled');

db.Where("state = ?", "active").Preload("Orders", "state NOT IN (?)", "cancelled").Find(&users)
// SELECT * FROM users WHERE state = 'active';
// SELECT * FROM orders WHERE user_id IN (1,2) AND state NOT IN ('cancelled');
```

## 自定义预加载 SQL

您可以通过 `func(db *gorm.DB) *gorm.DB` 实现自定义预加载 SQL，例如：

```go
db.Preload("Orders", func(db *gorm.DB) *gorm.DB {
  return db.Order("orders.amount DESC")
}).Find(&users)
// SELECT * FROM users;
// SELECT * FROM orders WHERE user_id IN (1,2,3,4) order by orders.amount DESC;
```

## 嵌套预加载

GORM 支持嵌套预加载，例如：

```go
db.Preload("Orders.OrderItems.Product").Preload("CreditCard").Find(&users)

// 自定义预加载 `Orders` 的条件
// 这样，GORM 就不会加载不匹配的 order 记录
db.Preload("Orders", "state = ?", "paid").Preload("Orders.OrderItems").Find(&users)
```

### 更新选择的字段

如果您只想在更新时更新或忽略某些字段，可以使用`Select`, `Omit`

```go
db.Model(&user).Select("name").Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
//// UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111;

db.Model(&user).Omit("name").Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
//// UPDATE users SET age=18, actived=false, updated_at='2013-11-17 21:34:10' WHERE id=111;
```

### where条件另类用法
```
	// where条件
	where := func(db *gorm.DB) *gorm.DB {
		if !utils.IsEmpty(id) {
			db.Where("id=?", id)
		}
		return db
	}

	var histories []models.User
	inits.DB.Scopes(where).Count(&total)
```

设置表别名
```
db.Table("?", clause.Table{Name: "wom_sys_channel_type", Alias: "t"})
```

设置中国时区
```
# 数据库  
dns: root:123456@(192.168.1.168:8090)/test_db?charset=utf8mb4&parseTime=true&loc=PRC
```
> loc中的值不能乱写，可以查看系统目录下有哪些： ls /usr/share/zoneinfo/