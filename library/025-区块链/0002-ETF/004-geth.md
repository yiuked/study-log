### 启动客户端
```
geth --datadir="/Users/mac/Documents/eth/data" -verbosity 6 --ipcdisable --port 30301 --http.port 8101 console 2>>/Users/mac/Documents/eth/log/01.log
```
> 参数可查看[006-geth参数]

```
# Generate desired config file. You must specify testnet here.
geth --goerli --syncmode "full" ... dumpconfig > goerli.toml

# Start geth with given config file. Here too the testnet must be specified.
geth --goerli --config goerli.toml
```
> 正式网配置导出与导入：
> ```
> geth --datadir="/Users/mac/Documents/eth/data" -verbosity 6 --ipcdisable --port 30301 --http.port 8101 dumpconfig > ethnet.toml
> geth --config ethnet.toml
> ```
### 启动轻服务器
```
geth --light.serve 50 --txlookuplimit 0
```
>  --light.serve 取百分比作为值。大于 100 的数字表示您希望将多个线程专用于此功能，例如`--light.serve 200`2 个内核。
>  `--txlookuplimit 0`geth 取消索引旧事务以节省空间。
轻量模式，这对最终用户有几个好处：
-   轻客户端并不直接与区块链交互，而是使用全节点作为中介。轻客户端依赖于全节点去执行许多操作
-   同步需要几分钟而不是几小时（对于快速同步）或几天（对于完全同步）
-   它使用的存储空间显着减少，例如，与主网同步的节点不到 1Gb
-   它在 CPU 和可能的其他资源上更轻
-   因此它适用于资源受限的设备
-   离线一段时间后，它可以更快地赶上
-   轻客户端需要下载区块链的区块头
-   普通用户使用全节点、轻节点或受信任的远程节点在网络上发送交易。
-   全节点从网络上的对等节点接收交易，检查这些交易的有效性，并将它们广播到网络。
-   矿工是连接到特定软件的全节点。他们像一个普通的全节点一样从网络上接收和验证交易，但是会额外投入大量的精力来寻找问题的解决方案，才会被允许生成下一个区块。矿工使用的全节点通过应该将哪个区块添加到区块链并构建在其上达成共识。任何在其上构建了至少 10 个块的块都被认为是安全的，因为它包含的交易被还原的概率非常低。
### 启动轻客户端
```
geth --syncmode light --http --http.api --rpc --rpcapi "eth,debug"


geth --syncmode light --datadir="/Users/mac/Documents/eth/light-data" -verbosity 6 --http --ws console 2>>/Users/mac/Documents/eth/log/light-data.log
```


### 节点信息
1. 查看当前节点信息
```
admin.nodeInfo
```
2. 查看当前节点连接信息
```
admin.peers
```


```
enode://72609b09110c5b79ff7ef29e24fa5f4bfb1d35c8f5af619609462ec031661dcaf1736b446f954dbd8e8cd65a78d67dc5d49d9c14106b636dae68c35051c1a1ef@127.0.0.1:30301
```

当节点在后台运行时，可以使用以下命令进入到控制台
```
geth attach http://127.0.0.1:8545
```

### 备份与恢复
