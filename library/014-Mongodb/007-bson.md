bson与json类似，是一种数据序列化格式，全称（  
Binary Serialized Document Format）。与json不同的是，它采用的是一种二进制表示形式，则json是以字符串来表达。

### bson.A
```
bson.A{"bar", "world", 3.14159, bson.D{{"qux", 12345}}}  
```
A（array）是一个用来保存数组的结构

### bson.D
```
bson.D{{"foo", "bar"}, {"hello", "world"}, {"pi", 3.14159}}  
```
D（docment）存的是文档。当元素的顺序很重要时，例如MongoDB命令文档，应使用此类型。如果元素的顺序无关紧要，则应使用M。

### bson.E
用来表示D的，通常是D内部使用

### bson.M
```
bson.M{"foo": "bar", "hello": "world", "pi": 3.14159}  
```
M 是由`map[string]interface{}` 构成，因此它是无序的，如果需要考虑顺序，请使用D