### 一、什么是protobuff

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