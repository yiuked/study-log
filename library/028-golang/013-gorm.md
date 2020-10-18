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
