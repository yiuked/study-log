#### 更新
```js
db.customer.update({"otherability" : ""}, {"otherability" : null})
db.getCollection("customer").update( { _id: ObjectId("637450905c9512676f9ef3d8") }, { $set: { otherability: null } } )
```

#### 查询
golang or 查询示例
``` go
filter := bson.M{}  
// 关键词查询  
if len(info.Keyword) > 0 {  
   filter = bson.M{"$or": []bson.M{  
      bson.M{"phone": bson.M{"$regex": info.Keyword}},  
      bson.M{"username": bson.M{"$regex": info.Keyword}},  
      bson.M{"artname": bson.M{"$regex": info.Keyword}},  
   }}  
}  
// 性别  
if len(info.Sex) > 0 {  
   filter["sex"] = info.Sex  
}
```