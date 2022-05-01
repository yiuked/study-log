````go
import (
	"database/sql"
	"gorm.io/gorm"
	"time"
)

type SvGift struct {
	gorm.Model
	Name        string `gorm:"type:varchar(50) default '' not null COMMENT '礼物名称'"`
	Description string `gorm:"type:varchar(256) default null COMMENT '礼物描述'"`
	Logo        string `gorm:"type:varchar(128) default '' not null COMMENT '支付方式LOGO'"`
	Svga        string `gorm:"type:varchar(128) default '' not null COMMENT 'Svga地址'"`
	Coin        int    `gorm:"type:int(10) default 0 not null COMMENT '礼物需要消费积分'"`
	Sort        int    `gorm:"type:int(3) default 0 not null COMMENT '排序'"`
	Status      uint   `gorm:"type:tinyint(1) unsigned not null default 2 COMMENT '礼物状态:1为关闭，2为启用'"`
}

// SvCall 呼叫
type SvCall struct {
	gorm.Model
	Anchor          int64        `gorm:"type:bigint(16) unsigned not null COMMENT '呼叫人';index:idx_anchor"`
	Customer        int64        `gorm:"type:bigint(16) unsigned not null COMMENT '呼叫人';index:idx_customer"`
	ChannelName     string       `gorm:"type: varchar(64) default null COMMENT '频道名称';index:unique_index"`
	CallType        uint         `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '呼叫类型：1.用户呼叫主播，2.主播呼叫用户，3.用户呼叫临时主播'"`
	CallFrom        uint         `gorm:"type:tinyint(1) unsigned not null default 2 COMMENT '呼叫来源：1.hunting，2.正常呼叫'"`
	HuntingIncr     int          `gorm:"type:int(10) default 0 not null COMMENT '本次呼叫完成hunting时保存当日完成hunting的情况,本次呼叫未完成hunting时值为0'"`
	AnswerState     uint         `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '应答状态：1.呼叫中，2.接听，3.挂断'"`
	DeclinedRemark  string       `gorm:"type: varchar(128) default null COMMENT '呼叫挂断原因'"`
	CallFinishAt    sql.NullTime `gorm:"type:datetime default null COMMENT '呼叫结束呼叫时间'"`
	CallDuration    int          `gorm:"type:int(10) default 1 not null COMMENT '呼叫时长'"`
	ConsumeCnt      int          `gorm:"type:int(10) default 1 not null COMMENT '时长扣费次数'"`
	LastConsumeSt   sql.NullTime `gorm:"type:datetime default null COMMENT '最后消费时间'"`
	NextConsumeSt   sql.NullTime `gorm:"type:datetime default null COMMENT '下一次消费时间'"`
	VideoFinishAt   sql.NullTime `gorm:"type:datetime default null COMMENT '视频结束呼叫时间'"`
	VideoDuration   int          `gorm:"type:int(10) default 1 not null COMMENT '通话时长'"`
	VideoState      int          `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '视频状态：1.待接通，2.通话中，3.挂断'"`
	VideoTerminator int64        `gorm:"type:bigint(16) default 0 COMMENT '挂断人'"`
	HangupRemark    string       `gorm:"type: varchar(128) default null COMMENT '视频挂断原因'"`
}

// SvVideoCoinPurchaseRecord 视频过程金币扣费记录
type SvVideoCoinPurchaseRecord struct {
	gorm.Model
	CallFrom           uint      `gorm:"type:tinyint(1) unsigned not null COMMENT '金币模式，1-hunting类型，2-正常计费类型';"`
	CallID             uint      `gorm:"type:int(11) unsigned not null COMMENT '账户UID';index:idx_call"`
	Sender             int64     `gorm:"type:bigint(16) unsigned not null COMMENT '转出人UID';index:idx_sender"`
	Receiver           int64     `gorm:"type:bigint(16) unsigned not null COMMENT '转入人UID';index:idx_receiver"`
	CostPer            int       `gorm:"type:int(10) default 0 not null COMMENT '每分钟扣费基准'"`
	AnchorRate         int       `gorm:"type:int(10) default 0 not null COMMENT '主播提成比例'"`
	UserActualCost     int       `gorm:"type:int(10) default 0 not null COMMENT '用户实际扣费'"`
	AnchorActualIncome int       `gorm:"type:int(10) default 0 not null COMMENT '主播实际收入'"`
	StartAt            time.Time `gorm:"type:datetime default null COMMENT '开始时间'"`
	EndAt              time.Time `gorm:"type:datetime default null COMMENT '结束时间'"`
	TimeDuration       int       `gorm:"type:int(11) default 0 not null COMMENT '区间时长'"`
	SettleStatus       int       `gorm:"type:tinyint(1) default 1 not null COMMENT '结算状态，1-待结算，2-正常结算，3-提前结算，4-待确认结算'"`
	Remark             string    `gorm:"type:varchar(128) default '' default null COMMENT '备注'"`
}

// SvVideoGiftPurchaseRecord 视频过程礼物消费记录
type SvVideoGiftPurchaseRecord struct {
	gorm.Model
	CallID             uint   `gorm:"type:int(11) unsigned not null COMMENT '账户UID';index:idx_call"`
	Sender             int64  `gorm:"type:bigint(16) unsigned not null COMMENT '赠送人UID';index:idx_sender"`
	Receiver           int64  `gorm:"type:bigint(16) unsigned not null COMMENT '收取人UID';index:idx_receiver"`
	GiftID             uint   `gorm:"type:int(10) default 0 not null COMMENT '礼物ID'"`
	GiftName           string `gorm:"type:varchar(32) not null COMMENT '礼物引用名称';index:idx_gift"`
	Logo               string `gorm:"type:varchar(128) default '' not null COMMENT '支付方式LOGO'"`
	Svga               string `gorm:"type:varchar(128) default '' not null COMMENT 'Svga地址'"`
	GiftCnt            int    `gorm:"type:int(10) default 0 not null COMMENT '赠送礼物数量'"`
	Coin               int    `gorm:"type:int(10) default 0 not null COMMENT '礼物单价'"`
	UserActualCost     int    `gorm:"type:int(10) default 0 not null COMMENT '用户实际扣费'"`
	AnchorRate         int    `gorm:"type:int(10) default 0 not null COMMENT '主播提成比例'"`
	AnchorActualIncome int    `gorm:"type:int(10) default 0 not null COMMENT '主播实际收入'"`
	SettleStatus       int    `gorm:"type:tinyint(1) default 1 not null COMMENT '结算状态，1-待结算，2-待审核（触发风控），3-正常结算，3-非正常结算'"`
	Remark             string `gorm:"type:varchar(128) default '' default null COMMENT '备注'"`
}

// SvVideoRecord 视频消费统计
type SvVideoRecord struct {
	gorm.Model
	Anchor               int64 `gorm:"type:bigint(16) unsigned not null COMMENT '主播ID';index:idx_anchor"`
	Customer             int64 `gorm:"type:bigint(16) unsigned not null COMMENT '客户ID';index:idx_customer"`
	CallID               uint  `gorm:"type:int(11) unsigned not null COMMENT '账户UID';index:idx_call"`
	CostPer              int   `gorm:"type:int(10) default 0 not null COMMENT '每分钟扣费'"`
	CustomerHuntingCoin  int   `gorm:"type:int(10) default 0 not null COMMENT 'hunting收入金币（hunting收入不分配给主播）'"`
	CustomerGiftCoin     int   `gorm:"type:int(10) default 0 not null COMMENT '礼物收入总金币'"`
	CustomerGiftRiskCoin int   `gorm:"type:int(10) default 0 not null COMMENT '用户触发风控的礼物收入总金币'"`
	CustomerTimeCoin     int   `gorm:"type:int(10) default 0 not null COMMENT '基准收入总金币'"`
	CustomerTotal        int   `gorm:"type:int(10) default 0 not null COMMENT '用户总消费金额'"`
	AnchorGiftCoin       int   `gorm:"type:int(10) default 0 not null COMMENT '礼物收入总金币'"`
	AnchorGiftRiskCoin   int   `gorm:"type:int(10) default 0 not null COMMENT '主播触发风控的礼物收入总金币'"`
	AnchorTimeCoin       int   `gorm:"type:int(10) default 0 not null COMMENT '基准收入总金币'"`
	AnchorTotal          int   `gorm:"type:int(10) default 0 not null COMMENT '主播合计收入'"`
	GiftCnt              int   `gorm:"type:int(10) default 0 not null COMMENT '礼物数量'"`
	HuntingDuration      int64 `gorm:"type:int(10) default 1 not null COMMENT 'hunting通话时长'"`
	VideoDuration        int64 `gorm:"type:int(10) default 1 not null COMMENT '通话时长'"`
}


// SvUser 用户
type SvUser struct {
	UID                 int64     `gorm:"primarykey"`
	UserNumber          int64     `gorm:"type:bigint(16) unsigned not null COMMENT '用户展示号码';uniqueIndex"`
	CostPer             int       `gorm:"type:int(11) not null default 0 COMMENT '计费起点'"`
	Country             string    `gorm:"type:char(2) default null COMMENT '国家二位ISO代码'"`
	AccountType         uint      `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '用户来源，1游客，2邮箱注册，3苹果，4安卓'"`
	Role                uint      `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '账户类型，1普通用户，2主播，默认1'"`
	Email               string    `gorm:"type: char(128) default null COMMENT '邮箱地址';index:idx_email"`
	NickName            string    `gorm:"type:varchar(32) not null COMMENT '昵称'"`
	Password            string    `gorm:"type:char(32) not null COMMENT '用户密码'"`
	Age                 uint      `gorm:"type:tinyint(2) default '0' COMMENT '年龄'"`
	Sex                 uint      `gorm:"type:tinyint(1) default '1' COMMENT '姓别，1女，2男'"`
	Experience          uint      `gorm:"type:int(11) unsigned not null default 0 COMMENT '用户经验值'"`
	LoginCnt            uint      `gorm:"type:int(5) unsigned not null default 0 COMMENT '用户登录次数'"`
	UUID                string    `gorm:"type: varchar(128) default null COMMENT '设备唯一标识';index:idx_uuid"`
	DeviceType          string    `gorm:"type: varchar(128) default null COMMENT '设备类型'"`
	DeviceBrand         string    `gorm:"type: varchar(128) default null COMMENT '设备品牌'"`
	LastPlatform        int32     `gorm:"type:tinyint(1) default null COMMENT '操作系统 iOS 1, Android 2, Windows 3, OSX 4, WEB 5, 小程序 6，linux 7'"`
	LastPlatformVersion string    `gorm:"type:varchar(32) default null COMMENT '操作系统版本'"`
	LastAppVersion      string    `gorm:"type:varchar(32) default null COMMENT 'App版本'"`
	LastIP              string    `gorm:"type:varchar(128) default null COMMENT '最后登录IP'"`
	HeadImage           string    `gorm:"type:varchar(128) default null COMMENT '用户头像'"`
	Status              uint      `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '账户状态:1为正常，2为锁定'"`
	RechargeTotal       float64   `gorm:"type:decimal(15,2) unsigned not null default 0.00 COMMENT '累计充值金额'"`
	AnswerMode          uint      `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '启用应答模式:1为正常，2为启用1v1,3为启用1V多'"`
	TracelessMode       uint      `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '启用无痕模式:1为正常，2为启用'"`
	AuditStatus         uint      `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '主播认证|审核状态:1为未认证，2认证中，3认证通过,4审核失败（审核失败，可重新认证）'"`
	Score               float32   `gorm:"type:float(2,1) not null default 4.5 COMMENT '综合评分'"`
	VipExpireAt         time.Time `gorm:"type:datetime default NOW() COMMENT 'VIP到期时间'"`
	VipLevel            uint      `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT 'VIP等级:1为普通，2为正常VIP,3为超级VIP'"`
	CreatedAt           time.Time
	UpdatedAt           time.Time
	Profile             SvUserProfile  `gorm:"foreignKey:UID;references:UID"`
	Photos              []SvUserPhoto  `gorm:"foreignKey:UID;references:UID"`
	UserCoin            SvUserCoin     `gorm:"foreignKey:UID;references:UID"`
	UserCountry         SvCountry      `gorm:"foreignKey:Country;references:Iso"`
	DeletedAt           gorm.DeletedAt `gorm:"index"`
	Hot                 int64          `gorm:"type:bigint(16) UNSIGNED NOT NULL DEFAULT 0 COMMENT '热度'"`
}

// SvUserProfile 用户扩展信息
type SvUserProfile struct {
	gorm.Model
	UID       int64   `gorm:"type:bigint(16) unsigned not null COMMENT '账户UID';uniqueIndex"`
	Introduce string  `gorm:"type:varchar(512) default null COMMENT '个人简介'"`
	Height    float64 `gorm:"type:decimal(10,2) not null COMMENT '身高'"`
	Weight    float64 `gorm:"type:decimal(10,2) not null COMMENT '体重'"`
	Birthday  string  `gorm:"type: varchar(32) default null COMMENT '生日'"`
}

// SvUserPhoto 用户相册
type SvUserPhoto struct {
	gorm.Model
	UID   int64  `gorm:"type:bigint(16) unsigned not null COMMENT '账户UID';index:idx_uid"`
	Path  string `gorm:"type: varchar(256) default null COMMENT '照片地址'"`
	Cover uint   `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '账户状态:1为正常，2为封面'"`
}

// SvUserApplyAnchor 申请主播记录
type SvUserApplyAnchor struct {
	gorm.Model
	UID         int64  `gorm:"type:bigint(16) unsigned not null COMMENT '账户UID';index:idx_uid"`
	Posture     string `gorm:"type: varchar(256) default null COMMENT '真人姿势图片路径'"`
	Auditor     int64  `gorm:"type:bigint(16) unsigned not null COMMENT '审核人';index:idx_uid"`
	Remark      string `gorm:"type:varchar(128) not null default '' COMMENT '审核备注'"`
	AuditStatus uint   `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '主播认证|审核状态:1为待审核，2审核未通过，3认证通过'"`
}

// SvUserNumber 靓号
type SvUserNumber struct {
	gorm.Model
	Status uint `gorm:"type:tinyint(1) unsigned not null default 1 COMMENT '账户状态:1未使用，2为使用，3不可用'"`
}

// SvUserCoin 用户金币余额
type SvUserCoin struct {
	gorm.Model
	UID         int64 `gorm:"type:bigint(16) unsigned not null COMMENT '账户UID';index:unique_index"`
	IncomeTotal int   `gorm:"type:int(10) default 0 not null COMMENT '累计收入'"`
	ExpendTotal int   `gorm:"type:int(10) default 0 not null COMMENT '累计支付'"`
	Coin        int   `gorm:"type:int(10) default 0 not null COMMENT '可用余额'"`
}

// SvUserCoinRecord 用户余额变更记录
type SvUserCoinRecord struct {
	gorm.Model
	UID           int64  `gorm:"type:bigint(16) unsigned not null COMMENT '账户ID';index:idx_uid"`
	TransferNo    string `gorm:"type:varchar(64) default '' not null COMMENT '交易流水号';index:idx_transfer_no"`
	TransferType  int    `gorm:"type:tinyint(1) default 0 not null COMMENT '业务类型'"`
	RelationID    uint   `gorm:"type:int(11) default 0 not null COMMENT '交易关联ID'"`
	RelationUID   int64  `gorm:"type:int(11) default 0 not null COMMENT '交易关联ID'"`
	BeforeBalance int    `gorm:"type:int(10) default 0 not null COMMENT '变更前余额'"`
	ActionValue   int    `gorm:"type:int(10) default 0 not null COMMENT '操作金额'"`
	AfterBalance  int    `gorm:"type:int(10)  default 0 not null COMMENT '变更后余额'"`
	Remark        string `gorm:"type:varchar(128) default '' default null COMMENT '备注'"`
}

// SvUserDevice 用户登录设备信息
type SvUserDevice struct {
	gorm.Model
	UID             int64  `gorm:"type:bigint(16) unsigned not null COMMENT '用户ID';index:idx_uid"`
	UUID            string `gorm:"type: varchar(128) default null COMMENT '设备唯一标识';index:idx_uuid"`
	DeviceType      string `gorm:"type: varchar(128) default null COMMENT '设备类型'"`
	DeviceBrand     string `gorm:"type: varchar(128) default null COMMENT '设备品牌'"`
	Platform        int32  `gorm:"type:tinyint(1) default null COMMENT '操作系统 iOS 1, Android 2, Windows 3, OSX 4, WEB 5, 小程序 6，linux 7'"`
	PlatformVersion string `gorm:"type:varchar(32) default null COMMENT '操作系统版本'"`
	AppVersion      string `gorm:"type:varchar(32) default null COMMENT 'App版本'"`
}

````

