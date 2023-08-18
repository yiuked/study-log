来看一个例子，下面的代码输出什么呢？
```go
func TestFor(t *testing.T) {  
	type User struct {  
		Name string  
		RegAt time.Time  
	}  
	var users []User  
	users = append(users, User{  
			Name: "张三",  
			RegAt: time.Now(),  
		}, User{  
			Name: "李四",  
			RegAt: time.Now().Add(1 * time.Hour),  
		})  
	  
	mapUsers := make(map[*string]*time.Time)  
	for _, user := range users {  
		ps := &user  
		log.Printf("%p", ps)  
		mapUsers[&user.Name] = &user.RegAt  
	}  
	for s, t2 := range mapUsers {  
		log.Println(s, ":", t2)  
	}  
}
```

结果是：
```
2023/08/18 15:12:01 0xc0003d3bc0
2023/08/18 15:12:01 0xc0003d3bc0
2023/08/18 15:12:01 0xc0003d3bc0 : 2023-08-18 16:12:01.295613 +0800 CST m=+3600.009067802
```

也就是说，当golang执行for循环时，只初始化了一次`user`,每次迭代时，只是重置了`user`的值，指针没有发生变化。因此如果在循环中使用&符号去取值时，只会取到最后一次循环的结果。
