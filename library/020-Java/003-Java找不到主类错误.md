```java
//这个问题原因有以下几种,但是和环境变量并没有太大的关系
//能够执行java 和 javac 就证明你的环境变量已经配置好了,其实 classpath 可以不配置
//假如有如下文件:H:\code\Hello.java
public class Hello{
    public static void main(String[]args){
        System.out.println("Hello");
    }
}
//正确编译命令: javac Hello.java
//正确运行命令: java Hello

错误1:H:\code>java Hello.java
错误: 找不到或无法加载主类 Hello.java
原因:命令错误

错误2:H:\code>java Hello.class
错误: 找不到或无法加载主类 Hello.class
原因:命令错误

错误3:java 源文件带有包名,往往容易出错
如:H:\code\Hello2.java
package com.example;

public class Hello2{
    public static void main(String[]args){
        System.out.println("Hello2");
    }
}
这代码看上去没什么问题,执行:
H:\code>javac Hello2.java
H:\code>java Hello2
错误: 找不到或无法加载主类 Hello2

解决办法:
+.删除包名  或者
+.在code 下创建一个与包名相同的文件结构(H:\code\com\example\Hello2.java)
  编译:H:\code>javac com/example/Hello2.java
  运行:H:\code>java com.example.Hello2
```
