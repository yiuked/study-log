中文文档
https://hyperledgercn.github.io/hyperledgerDocs/

超级账本 fabric多机部署步骤（solo）
https://www.jianshu.com/p/7dd4e1bee6d8


Orderers: 即Consenter，共识插件，提供共识服务的网络节点，负责接受交易信息进行排序，以及对交易进行切割并打包，打包后返回批量交易。例如，使用Kafka或PBFT(SBFT)，单节点使用solo单节点。
Peers: 维护账本的网络节点，通常在Hyperledger Fabric架构中存在各种角色，如endorser和committer。
通道：通道是有共识服务（ordering）提供的一种通讯机制，类似于消息系统中的发布-订阅（PUB/SUB)中的topic；基于这种发布-订阅关系，将peer和orderer连接在一起，形成一个个具有保密性的通讯链路（虚拟），实现了业务隔离的要求；通道也与账本（ledger）-状态（worldstate）紧密相关； peer可以在订阅多个通道，并且只能访问订阅通道上的交易；且通道上的数据仅与peer有关，与order无关。
账本：账本保存Orders提交经节点确认的交易记录。
成员：访问和使用账本的网络节点。
成员管理： 每个membership（MSP组织）可以有自己的fabric-ca作为第三方认证机构，与背书策略对应。成员都需要在MSP中注册
链：基本上，一个链由1个通道+ 1个账本+ N个成员组成。非链的成员无法访问该链上的交易。链的成员可以由应用程序动态指定。



hyperledger CA 包下载下来后，里面的Makefile文件依然是从线下去读取packege，因此需要把
解压后的hyperledger-ca目录copy到GOPATH目录中
