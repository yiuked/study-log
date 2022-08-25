rpc

grpc

protobuf

protoc

### Protocol Buffers 简介

protobuf 即 Protocol Buffers，是一种轻便高效的结构化数据存储格式，与语言、平台无关，可扩展可序列化。protobuf 性能和效率大幅度优于 JSON、XML 等其他的结构化数据格式。protobuf 是以二进制方式存储的，占用空间小，但也带来了可读性差的缺点。protobuf 在通信协议和数据存储等领域应用广泛。

Protobuf 在 `.proto` 定义需要处理的结构化数据，可以通过 `protoc` 工具，将 `.proto` 文件转换为 C、C++、Golang、Java、Python 等多种语言的代码，兼容性好，易于使用。

### 编写.protc文件

```
# 协议版本
syntax = "proto3";

# go 引用包名（！！包名至少包含一个“/”，如包名为 “order”，也需要写成"order/"或者"./order"）
option go_package = "google.golang.org/grpc/examples/helloworld/helloworld";

# proto 文件包名，和输出文件包名无关，仅在proto文件内部引用
package Helloworld;
// 定义服务.
service Greeter {
  // 在服务中定义 rpc 方法，指定请求的和响应类型。gRPC 允许定义4种类型的 service 方法:
  // 一个 简单 RPC ， 客户端使用存根发送请求到服务器并等待响应返回，就像平常的函数调用一样。
  rpc SayHello1 (HelloRequest) returns (HelloReply) {}
  
  // 一个 服务器端流式 RPC ， 客户端发送请求到服务器，拿到一个流去读取返回的消息序列。 
  // 客户端读取返回的流，直到里面没有任何消息。
  rpc SayHello2 (HelloRequest) returns (stream HelloReply) {} 
  
  // 一个 客户端流式 RPC ， 客户端写入一个消息序列并将其发送到服务器，同样也是使用流。
  // 一旦客户端完成写入消息，它等待服务器完成读取返回它的响应。
  rpc SayHello3 (stream HelloRequest) returns (HelloReply) {}
  
  // 一个 双向流式 RPC 是双方使用读写流去发送一个消息序列。
  // 两个流独立操作，因此客户端和服务器可以以任意喜欢的顺序读写：
  // 比如， 服务器可以在写入响应前等待接收所有的客户端消息，或者可以交替的读取和写入消息，或者其他读写的组合。 
  // 每个流中的消息顺序被预留。
  rpc SayHello4 (stream HelloRequest) returns (stream HelloReply) {}
}


// 定义消息结构
message HelloRequest {
  // 定义语法
  // [出现次数] 类型 结构名称 = 序号
  // 出现次数：可为 required（至少出现一次） 、optional（出现0或者1次，默认）、repeated（可出现任意次） 
  // 类型：int32、int64、string、bytes、bool、enum等
  // 结构名称：等同变量名
  // 序号：由1开始计数，不可重复，子结构体内单独计数
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}

```



### 编译文件.protc文件

通过`protoc`编译工具，可以将`.protc`编译成`C++、Java、Go、Python、Ruby、Node.js、Android Java、C#、Objective-C、PHP`等语言的源码文件

```
protoc --go_out=plugins=grpc:./ ./spider.proto
```



[1.Go Protobuf 简明教程](https://geektutu.com/post/quick-go-protobuf.html)



#### 常见错误信息

1. protoc-gen-go: unable to determine Go import path for "student.proto"

   ```
   protoc --go_out=plugins=grpc:./ .\student.proto
   protoc-gen-go: unable to determine Go import path for "student.proto"
   
   Please specify either:
           • a "go_package" option in the .proto source file, or
           • a "M" argument on the command line.
   
   See https://developers.google.com/protocol-buffers/docs/reference/go-generated#package for more information.
   
   --go_out: protoc-gen-go: Plugin failed with status code 1.
   ```

   > 需要在`.proto`文件中指定`go_package`属性,格式如下：
   >
   > ```
   > # 协议版本
   > syntax = "proto3";
   > 
   > # go 引用包名（！！包名至少包含一个“/”，如包名为 “order”，也需要写成"order/"）
   > option go_package = "google.golang.org/grpc/examples/helloworld/helloworld";
   > 
   > ```

```
github.com/golang/protobuf/protoc-gen-go
google.golang.org/grpc
google.golang.org/protobuf
```


```
(\w+)\s+(\w+)\s*=\s*(\d+); ===> $1 \u$2 = $3;

```