1. 自我介绍
    
2. 讲一个项目的点，因为用到了中间件平台的数据同步，于是开始鞭打数据同步。。
    
3. 如果同步的时候，插入了新数据怎么处理？
    
4. binlog有什么用？
    
5. binlog的数据格式有哪些？
    
6. 如何监听binlog？
    
7. mysqldump 之后需要进行什么处理？（这个问的太细了，细到我都不知道面试官是什么意思？）
    
8. 唯一索引和联合索引有什么区别？
    
9. 联合索引可以是唯一索引吗？
    
10. 那mysql索引结构是什么样的？
    
11. 一个索引的建立过程是什么样的？
    
12. 如果我对age字段建立索引，建立的过程是什么样的？
    
13. 为什么走索引加快了？
    
14. 为什么age可以建立索引？sex字段就不行？
    
15. 为什么sex建立索引还是会扫全表？
    
16. 如果我订单表达到一定规模之后mysql单表是撑不住了，怎么办？
    
17. 具体你会怎么分库分表？
    
18. 分库分表如果进行条件查询？
    
19. 同步ES？不使用其他组件，单单是mysql怎么操作，所有表遍历找过去吗？索引会不会失效？
    
20. ok，redis源码有了解吗？他的线程模型是什么样的？
    
21. redis有哪些存储日志的形式？同步还是异步？
    
22. 那AOF具体是怎么存储日志的？
    
23. AOF不断的写日志不是会有很多的io操作吗？怎么避免？
    
24. RDB是怎么进行操作？
    
25. 那如果数据库和redis需要缓存一致性怎么解决？
    
26. 那我不考虑最终一致性，我要强一致性，怎么解决？
    
27. ok，网络这块我也问问。http和https的区别是什么？
    
28. https是怎么建立连接的？先建立什么？再建立什么？
    
29. 具体是怎么建立的ssl tls加密？
    
30. http的请求头和响应头一般有什么信息，有什么用？
    
31. ok，页的概念你清楚吗？
    
32. 为什么需要内存对齐？
    
33. 页碎是什么？
    
34. go里面怎么样会发生死锁？死锁的场景具体有哪些？
    
35. 内存泄漏有哪些场景？怎么排查？
    
36. goruntine泄漏的场景有哪些？怎么排查？
    
37. 进程、线程、协程有什么区别？
    
38. 协程能被 kill 掉吗？
    
39. 那协程应该怎么处理？
    
40. 那context一般有什么信息？有什么用途？
    
41. 那如果我要 clone 一个context，子context 和 父context 是一摸一样吗？为什么？
    
42. singleflight 是什么？什么时候用的？
    
43. 如果这个goruntine超时怎么办？
    
44. doChan方法具体是怎么实现的？
    
45. 为什么会有饥饿模式？
    
46. 什么时候会让出时间片？
    
47. IO密集型和计算密集型的区别？

最后是几道代码题，飞书文档看着代码，不使用任何编辑器。

这段代码会发生什么？为什么？具体是怎么溢出的？
```go
var a uint = 1   
var b uint = 2   
fmt.Println(a-b)
```

说出以下输出结果？为什么？
```go
func TestSlicePrint(t *testing.T) {    
	a := []byte("AAAA/BBBBB")    
	index := bytes.IndexByte(a, '/')    
	b := a[:index]    
	c := a[index+1:]    
	b = append(b, "CCC"...)    
	fmt.Println(string(a))    
	fmt.Println(string(b))    
	fmt.Println(string(c))   
}   
```

这个锁是什么用的？这段代码有什么问题？
```go
func TestNumPrint(t *testing.T) {    
	wg := sync.WaitGroup{}    
	lock := sync.Mutex{}    
	a := 0    
	b := 10    
	for i := 0; i < 5; i++ {     
		go func() {      
			if a > b {       
				fmt.Println("done")       
				return      
			}      
			lock.Lock()      
			defer lock.Unlock()      
			a++      
			fmt.Printf("i: %d \n", i)     
		}()    
	}    
	wg.Wait()   
}
```

来源：https://mp.weixin.qq.com/s/yIRtCpkYxB5H-wMHBexlDQ