## configtxgen
由于区块链系统自身的分布式特性，对其中配置进行更新和管理是一件很有挑战的任务。
一旦出现不同节点之间配置不一致，就可能导致整个网络功能异常。

在Fabric网络中，通过采用配置交易（Configuration Transaction，ConfigTX）这一创新设计来实现对通道相关配置的更新。
配置更新操作如果被执行，也要像应用交易一样经过网络中节点的共识确认。

configtxgen（Configuration Transaction Generator）工具是一个很重要的辅助工具，
它可以配合cryptogen生成的组织结构身份文件使用，离线生成跟通道有关的配置信息，
相关的实现 在common/configtx包下。

主要功能有如下三个：
* 生成启动Orderer需要的初始区块，并支持检查区块内容；
* 生成创建应用Channel需要的配置信息，并支持检查交易内容；
* 生成节点与Channel关联的配置信息。

默认情况下，configtxgen工具会依次尝试从`$FABRIC_CFG_PATH`环境变量指定的路径，当前路径和 /etc/hyperledger/fabric路径下查找configtx.yaml配置文件并读入，作为默认的配置。环境变量中以CONFIGTX_ 前缀开头的变量也会被作为配置项。

`configtxgen`模块用来生成`orderer`的初始化文件和`channel`的初始化文件。
```
Usage of ./configtxgen:
  -asOrg string 以某个特定组织生成配置
  -channelCreateTxBaseProfile string
        Specifies a profile to consider as the orderer system channel current state to allow modification of non-application parameters during channel create tx generation. Only valid in conjuction with 'outputCreateChannelTx'.
  -channelID string
        指派channelID
  -configPath string
        配置文件路径
  -inspectBlock string
        打印指定区块文件中的配置信息
  -inspectChannelCreateTx string
        Prints the configuration contained in the transaction at the specified path
  -outputAnchorPeersUpdate string
        Creates an config update to update an anchor peer (works only with the default channel creation, and only for the first update)
  -outputBlock string
        将初始区块写入指定文件
  -outputCreateChannelTx string
        The path to write a channel creation configtx to (if set)
  -printOrg string
        以json格式输出组织信息
  -profile string
        The profile from configtx.yaml to use for generation. (default "SampleInsecureSolo")
  -version
        Show version information
```
> 在YAML文件中，&KEY所定位的字段信息，可以通过'<<：KEY'语法来引用，相当于导入定位部分的内容。

1. 生成创世块
```
./configtxgen -channelID first-channel -profile OneOrgsOrdererGenesis -outputBlock ../channel-artifacts/mygenesis.block
```

2. 生成channel配置
```
./configtxgen -profile OneOrgsChannel -outputCreateChannelTx ../channel-artifacts/channel.tx -channelID first-channel
```

3. 生成channel关联的锚点文件
```
./configtxgen -profile OneOrgsChannel -outputAnchorPeersUpdate ../channel-artifacts/anchors.tx -channelID first-channel -asOrg Org1MSP
```

4. 启动orderer(启动之前需要配置orderer.yaml)
```
# configtx.yaml与orderer.yaml必须在同一目录
export FABRIC_CFG_PATH=/home/vagrant/fabric/config
./orderer start
```

5. 启用子节点
```
./peer node start
```

### 参考文献:
1. [configtxgen生成通道配置](https://blog.csdn.net/xiaohuanglv/article/details/89033298)
2. [Fabric实战（5）Fabric模块配置参数详解-configtxgen](https://blog.csdn.net/xiaohuanglv/article/details/89033298)
3. [hyperledger fabric 1.4 创建联盟](https://segmentfault.com/a/1190000020323773)
