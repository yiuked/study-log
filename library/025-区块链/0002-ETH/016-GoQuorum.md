
GoQuorum 是一个geth的分支，GoQuorum使用geth命令来启动GoQuorum节点


为了适配其企业级的联盟链功能，Quorum 同时还对 geth 做了部分调整：
1. 用其自己实现的基于投票机制的共识方式 “QuorumChain” 来代替原来的 “Proof of work” 。
1. 在原来无限制的P2P传输方式上增加了权限功能。使得P2P传输只能在互相允许的节点间传输。
1. 原来区块中的 “global state root” 被替换成了 “global public state root”。
1. 原来的 state 存储被分成了两部分，分别存储 public state 和 private state。
1. 修改区块校验逻辑使其能支持 private transaction。
1. Transaction 生成时支持 transaction 内容的替换。这个调整是为了能支持联盟中的私有交易。


Raft 不适合生产环境。仅在开发环境中使用。您可以将 Raft 网络迁移到另一个共识协议。

生产环境使用用QBFT
