1. import 怎么用?
> 要引用其他包的标识符，可以使用 import 关键字，导入的包名使用双引号包围，包名是从 GOPATH 开始计算的路径，使用/进行路径分隔。

2. 文件中的函数命名.
> 文件中函数以大写开头，表示将该函数导出供包外使用。当首字母小写时，为包内使用，包外无法引用到。

3. defer函数
> defer函数后面执行的函数，在当前函数return前执行，常用于函数退出前的内存资源注销等。

4. 函数方法
正常的函数声明可能是这样的：
```
func 函数名(参数列表)(返回参数列表){
    函数体
}
```
但有时，你可能会看到这样声明的：
```
func (variable_name variable_data_type) function_name() [return_type]{
   /* 函数体*/
}
func (file *File) Read(b []byte) (n int, err Error)
```
这类函数称为方法，它表示在对应的类型或者结构体上新增一个方法:
  ```
  package main

  import (
     "fmt"  
  )

  /* 定义结构体 */
  type Circle struct {
    radius float64
  }

  func main() {
    var c1 Circle
    c1.radius = 10.00
    fmt.Println("圆的面积 = ", c1.getArea())
  }

  //该 method 属于 Circle 类型对象中的方法
  func (c Circle) getArea() float64 {
    //c.radius 即为 Circle 类型对象中的属性
    return 3.14 * c.radius * c.radius
  }
  ```

5. 函数中的三个点`...`是什么意思。  
`...`主要有两个用途，第一个当函数有不确定性参数时，第二个是对传入参数进行切片，如下
```
# 表示可以接受任意个任意类型的参数，如果需要固定类型，可表示为：`args ...string`等
func cart(args ...interface{}) {
	for _, v:= range args{
		fmt.Println(v)
	}
}
# 假设 func cart(args ...string){},当传入product时，会被切为三个参数。
var product = []string{
        "price",
        "name",
        "quitity"
    }
cart(product...) //切片被打散传入
```

6. 我想吐槽的时间格式化.
Go语言中，使用的时间格式为:
```
2006-01-02 03:04:05
```
其中，时间03当改为15时，则变为24小时制，网上说，这是为了方便记忆，因为按月日时分秒年的顺序
刚好为01-02-03-04-05-06，我不明白这样的设置到底哪好记了，24小时制的15怎么解释，
多大数的开发语言在格式化日期时，都类似于yyyymmddhhmmii这种格式基本记住一次，后续不会忘记,
而go的时间格式化，只要你过一段时间不接触，估计又得查文档了.

7. 字符串与数字间的转化
```
int, err := strconv.Atoi(string) // 字符串转
int64, err := strconv.ParseInt(string, 10, 64) // string转成int64  
string := strconv.Itoa(int) // int转成string
string := strconv.FormatInt(int64,10) //int64转成string
```

8. golang连接mysql时parseTime和loc是什么意思？
```
root:@tcp(localhost:3306)/test?charset=utf8&parseTime=true&loc=Asia%2FShanghai
#parseTime 是查询结果是否自动解析为时间。
#loc 是配置操作数据库的时区。
```
使用gorm时，在代码内设置的时区不会生效,必须在连接数据库时设置loc
```
var token Token
token.ExpireAt = time.Now().In(locZone).Add(time.Second * 60)
db.Save(&token)
```
9. golang中如何实现时间添加或者减少?
```
  // 当前时间基础上增加1小时
  durdm,_ := time.ParseDuration("1h")
  ta = time.Now().Add(durdm)

  // 当前时间基础上减少1小时
  dur,_ := time.ParseDuration("-1h")
  ta = time.Now().Add(dur)

  // 当前时间基础上减少5分钟
  durmi,_ := time.ParseDuration("-5m")
  ta = time.Now().Add(durmi)

  // 当前时间基础上减少60秒
  durs,_ := time.ParseDuration("-60s")
  ta = time.Now().Add(durs)
```
ParseDuration 可以将一个字符串转为Duration格式,
可以使用的格式包含:"ns", "us" (or "µs"), "ms", "s", "m", "h".


10. 实例化对象
> p := &People{}

5. 构造函数
> go中没有构造函数，网上有很多使用`New类名`的方式，替换构造函数，如:  
>  ```
>  type Array struct {
>  	arr  []interface{}
>  	size int
>  }
>
>  func NewArray() *Array {
>  	var arr = &Array{}
>  	arr.size = 5
>  	return arr
>  }
>  ```
