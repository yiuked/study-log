### 什么是RPC

RPC是远程过程调用（Remote Procedure Call）的缩写形式

### 什么是gRPC

gRPC是一个高性能的RPC框架，它基于http/2传输。在gRPC中客户端可以像在本地一样调用服务端的方法。且无需关注服务端与客户端的开发语言。支持客户端、服务器和双向流式处理调用

![概念图](https://grpc.io/img/landing-2.svg)

gRPC默认使用 [Protocol Buffers](https://developers.google.com/protocol-buffers/docs/overview) 二进制序列化作为数据传输，减少对网络的使用。可用于多种语言的工具，以生成强类型服务器和客户端。

> gRPC 是由Google创建，早期Google使用Studbby做为内部的RPC通用基础设施，以此来连接各数据中心与海量的微服务。直到2015年3月，Google决定构建一个全新的版本的Stubby，这个新版本被命名为gRPC，此后Google对gRPC进行开源。



### 一、什么是Protobuf

Google Protocol Buffer( 简称 Protobuf) 是 Google 公司内部的混合语言数据标准。是一种轻便高效的结构化数据存储格式，可以用于结构化数据串行化，或者说序列化。它很适合做数据存储或 RPC 数据交换格式。可用于通讯协议、数据存储等领域的语言无关、平台无关、可扩展的序列化结构数据格式。

### 二、什么是protobuf-go

protobuf-go经历了两个大版本修订，第一个版本在2010年公开发布，发布的地址为 `github.com/golang/protobuf`。第二个版本在2020年发布，发布的地址为 `google.golang.org/protobuf`。

新版本在仍然在 github.com 上有仓库，地址为 `https://github.com/protocolbuffers/protobuf-go`。



### IDE插件

-  Protocol Buffers 在IDE中编辑 *.proto 文件时有语法高亮、提示。

- GenProtobuf  在IDE中快速生成 *.pb.go 文件 。

  使用步骤：

  > 1. 需要在 `Tools>Configure GenProtobuf >Quick Gen`中选择 Go
  > 2. 选中 *.proto 文件，右键选择`quick gen protobuf here`