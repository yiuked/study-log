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
