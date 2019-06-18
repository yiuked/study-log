1. import 怎么用?
> 要引用其他包的标识符，可以使用 import 关键字，导入的包名使用双引号包围，包名是从 GOPATH 开始计算的路径，使用/进行路径分隔。

2. 文件中的函数命名.
> 文件中函数以大写开头，表示将该函数导出供包外使用。当首字母小写时，为包内使用，包外无法引用到。

3. defer函数
> defer函数后面执行的函数，在当前函数return前执行，常用于函数退出前的内存资源注销等。

4. 实例化对象
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
