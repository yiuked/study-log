```
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
```
DB.Set("gorm:table_options","ENGINE=InnoDB").AutoMigrate(
```



## 带条件的预加载

GORM 允许带条件的 Preload 关联

```
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

```
db.Preload("Orders", func(db *gorm.DB) *gorm.DB {
  return db.Order("orders.amount DESC")
}).Find(&users)
// SELECT * FROM users;
// SELECT * FROM orders WHERE user_id IN (1,2,3,4) order by orders.amount DESC;
```

## 嵌套预加载

GORM 支持嵌套预加载，例如：

```
db.Preload("Orders.OrderItems.Product").Preload("CreditCard").Find(&users)

// 自定义预加载 `Orders` 的条件
// 这样，GORM 就不会加载不匹配的 order 记录
db.Preload("Orders", "state = ?", "paid").Preload("Orders.OrderItems").Find(&users)
```