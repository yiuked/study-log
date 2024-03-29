### goroutine
Go语言中，没有多线程机制，取而代之的是goroutine。goroutine的概念类似于线程，
但 goroutine 由 Go 程序运行时的调度和管理，Go 程序会智能地将 goroutine 中的任务合理地分配给每个 CPU。

具体的调试模式采用了GPM模式，G为goroutine，P为逻辑处理器，M为物理处理器

### 创建goroutine
程序在启用时，会默认创建一个goroutine。当我们需要主动去创建一个goroutine时，只需要通过以下方式：
```
go 函数名( 参数列表 )
# 列如
func main() {
	go func() {
		for i :=0; ;  i++{
			log.Printf("GO!GO!GO!,%d", i)
			time.Sleep(time.Second)
		}
	}()
	for i :=0; ;  i++{
		log.Printf("TO!TO!TO!,%d", i)
		time.Sleep(time.Second)
	}
}
```
以上匿名函数中的循环与main函数中的循环会并发执行，无先后顺序。
需要注意的是当main函数执行完时，新建的goroutine函数体也会中断？

### 管道channel
Go 语言中的管道（channel）是一种特殊的类型。在任何时候，同时只能有一个 goroutine 访问管道进行发送和获取数据。这使得goroutine 间通过管道就可以通信。管道像一个传送带或者队列，总是遵循先入先出的规则，保证收发数据的顺序。  
是引用类型，需要使用 make 进行创建，格式如下：
```
通道实例 := make(chan 数据类型)
# 列如
x := true
c := make(chan bool) //创建一个无缓冲的bool型Channel 
go func() {
	c <- x           //向一个Channel发送一个值
}()
x = 
//从Channel c接收一个值并将其存储到x中
x, ok = <- c         //从Channel接收一个值，如果channel关闭了或没有数据，那么ok将被置为false
```


```
x := true
c := make(chan bool) //创建一个无缓冲的bool型Channel 
c <- x               //向一个Channel发送一个值
x = <- c             //从Channel c接收一个值并将其存储到x中
```

### goroutine间通信
```
c := make(chan int)
go func() {
  c <- 1
  c <- 2
}()
// 循环读取
for d := range c {
  fmt.Println(d)
  if d >= 1 {
    break
  }
}
// 单条读取
d, ok := <-c
fmt.Println(d)
fmt.Println(ok)
```
### 定向通信管道
管道的操作权限还可以进行发送与接收的拆分
```
ch := make(chan int)
// 声明一个只能发送的通道类型, 并赋值为ch
var sendCh chan<- int = ch
//声明一个只能接收的通道类型, 并赋值为ch
var recvCh <-chan int = ch
```
### 创建带缓冲通道

```
通道实例 := make(chan 通道类型, 缓冲大小)
```

### 实现一个协程池

> [深入浅出Golang的协程池设计 - Go语言中文网 - Golang中文社区 (studygolang.com)](https://studygolang.com/articles/15477)
