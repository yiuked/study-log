```go
package database

import (
	"fmt"
	"github.com/spf13/viper"
	"gopkg.in/mgo.v2"
	"novel/common/log"
	"time"
)

type MongoClient struct {
	Session *mgo.Session
}

# MongoLogger 自定义日志组件
type MongoLogger struct {
}

func (m MongoLogger) Output(calldepth int, s string) error {
	log.Logger.Info(fmt.Sprintf("calldepth:%d,s:%s", calldepth, s))
	return nil
}
# GetDB 获取实例（注意此处不要像gorm那样去调用Clone,每一个Clone会创建一个链接）
func (c *MongoClient) GetDB() *mgo.Database {
	return c.Session.DB(viper.GetString("mongo.database"))
}

var mongoClient *MongoClient

func NewMongoClient() *MongoClient {
	if mongoClient != nil {
		return mongoClient
	}

	mgoDailInfo := &mgo.DialInfo{
		Addrs:     viper.GetStringSlice("mongo.host"),
		Direct:    viper.GetBool("mongo.direct"),
		Timeout:   time.Second * time.Duration(viper.GetInt("mongo.timeout")),
		Database:  viper.GetString("mongo.database"),
		Source:    viper.GetString("mongo.source"),
		Username:  viper.GetString("mongo.username"),
		Password:  viper.GetString("mongo.password"),
		PoolLimit: viper.GetInt("mongo.pool_limit"),
	}
	mgoSession, err := mgo.DialWithInfo(mgoDailInfo)
	if err != nil {
		panic(err)
	}

	mgoSession.SetMode(mgo.Monotonic, true)
	mgo.SetDebug(true)
	mgo.SetLogger(new(MongoLogger))
	mongoClient = &MongoClient{}
	mongoClient.Session = mgoSession

	return mongoClient
}

```

