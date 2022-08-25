## Golang连接MySQL解析
Go连接MySQL需要两个组件：
* database/sql
* github.com/go-sql-driver/mysql

```
import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)
```

### 连接MySQL
```
db, err := sql.Open("mysql", "root:@tcp(localhost:3306)/test?charset=utf8")
if err != nil {
  fmt.Print(err)
}

db.SetMaxOpenConns(2000) // 最大连接数
db.SetMaxIdleConns(1000) // 最大空闲连接数
db.SetConnMaxLifetime(60 * time.Second) //连接的最大空闲时间(可选)
db.Ping()
```
> 注：如果MaxIdleConns大于0并且MaxOpenConns小于MaxIdleConns ,那么会将MaxIdleConns置为MaxIdleConns

### 查询数据
```
rows, err := db.Query(query, args...)
if err != nil {
  log.Fatalf(err.Error())
}
if rows == nil {
  return nil
}

// 获取查询到的行名，返回了一个[]string
cols, err := rows.Columns()

result := Row{}

rawResult := make([][]byte, len(cols))
dest := make([]interface{}, len(cols))
for i := range rawResult {
  dest[i] = &rawResult[i]
}

if rows.Next() {
	// 传一个内存地址数组进行切割后，分散传入,每个内存地址保存一个字段值。
	err = rows.Scan(dest...)
	// 将存在内存地址中的值，传给result
  for i, raw := range rawResult {
		// 将值以key=>value的形式进行存储.
    if raw == nil {
      result[cols[i]] = ""
    } else {
      result[cols[i]] = string(raw)
    }
  }
} else {
  return nil
}

_ = err
return result
```
