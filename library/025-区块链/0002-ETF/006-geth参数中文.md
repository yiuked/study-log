```
$ geth --help
NAME:
   geth - the go-ethereum command line interface

   Copyright 2013-2021 The go-ethereum Authors

USAGE:
   geth [options] [command] [command options] [arguments...]

VERSION:
   1.10.15-stable-8be800ff

COMMANDS:
   account                            管理账户
   attach                             启动交互式 JavaScript 环境（连接到节点）
   console                            启动交互式 JavaScript 环境
   db                                 底层数据库操作
   dump                               从存储中转储特定块
   dumpconfig                         显示配置值
   dumpgenesis                        将创世块 JSON 配置转储到标准输出
   export                             导出区块链到文件
   export-preimages                   将原像数据库导出到 RLP 流中
   import                             导入区块链文件
   import-preimages                   从 RLP 流中导入原像数据库
   init                               引导并初始化一个新的创世块
   js                                 执行指定的JavaScript文件
   license                            显示许可证信息
   makecache                          生成ethash验证缓存（用于测试）
   makedag                            生成ethash挖矿DAG（用于测试）
   removedb                           删除区块链和状态数据库
   show-deprecated-flags              显示已弃用的标志
   snapshot                           基于快照的一组命令
   version                            打印版本号
   version-check                      检查（在线）当前版本是否存在任何已知的安全漏洞钱包 
   wallet                             管理以太坊预售钱包
   help, h                            显示命令列表或一个命令的帮助

以太坊选项:
  --config value                      TOML 配置文件
  --datadir value                     数据库和密钥库的数据目录（默认值：“~/.ethereum”）
  --datadir.ancient value             内部链 段的数据目录（默认 = 内部链数据）
  --datadir.minfreedisk value         以 MB 为单位的最小可用磁盘空间，一旦达到触发自动关闭（默认 = --cache.gc 转换为 MB，0 = 禁用）
  --keystore value                    密钥库的目录（默认 = 在 datadir 内）
  --usb                               启用对 USB 硬件钱包的监控和管理
  --pcscdpath value                   智能卡守护程序 (pcscd) 套接字文件的路径
  --networkid value                   设置网络ID（整数）（对于测试网：使用--ropsten、--rinkeby、--goerli）（默认值：1）
  --mainnet                           以太坊主网
  --goerli                            Görli network: 预配置的权威证明测试网络
  --rinkeby                           Rinkeby network: 预配置的权威证明测试网络
  --ropsten                           Ropsten network: 预配置的工作量证明测试网络
  --sepolia                           Sepolia network: 预配置的工作量证明测试网络
  --syncmode value                    区块链同步模式（“snap”、“full”或“light”）（默认：snap）
  --exitwhensynced                    块同步完成后退出
  --gcmode value                      区块链垃圾收集模式（“full”，“archive”）（默认：“full”）
  --txlookuplimit value               最近要维护交易索引的块数（默认 = 大约一年，0 = 整个链）（默认：2350000）
  --ethstats value                    ethstats 服务的报告 URL (nodename:secret@host:port)
  --identity value                    自定义节点名称
  --lightkdf                          以牺牲 KDF 强度为代价减少密钥派生 RAM 和 CPU 使用率
  --whitelist value                   逗号分隔的区块编号到哈希映射以强制执行 (<number>=<hash>)

轻客户端选项：
  --light.serve value                 允许服务 LES 请求的最大时间百分比（多线程处理允许值超过 100）（默认值：0）
  --light.ingress value               为轻客户端提供服务的传入带宽限制（千字节/秒，0 = 无限制）（默认值：0）
  --light.egress value                服务轻客户端的传出带宽限制（千字节/秒，0 = 无限制）（默认值：0）
  --light.maxpeers value              要服务的轻客户端或要附加的轻服务器的最大数量（默认值：100）
  --ulc.servers value                 受信任的超轻服务器列表
  --ulc.fraction value                宣布新头所需的可信超轻型服务器的最小百分比（默认值：75）
  --ulc.onlyannounce                  超轻型服务器仅发送公告
  --light.nopruning                   禁用原始轻链数据修改
  --light.nosyncserve                 在同步之前启用服务轻客户端

开发者链选项：
  --dev                               具有预先资助的开发者帐户的临时授权证明网络，已启用挖掘
  --dev.period value                  在开发者模式下使用的区块周期（0 = 仅当我的交易挂起时）（默认值：0）
  --dev.gaslimit value                初始区块 gas 限制（默认值：11500000）

ETHASH 选项:
  --ethash.cachedir value             存储 ethash 验证缓存的目录（默认 = 在 datadir 内）
  --ethash.cachesinmem value          最近要保存在内存中的 ethash 缓存数（每个 16MB）（默认值：2）
  --ethash.cachesondisk value         最近要保存在磁盘上的 ethash 缓存数（每个 16MB）（默认值：3）
  --ethash.cacheslockmmap             锁定最近的 ethash 缓存的内存映射
  --ethash.dagdir value               存储 ethash 挖掘 DAG 的目录（默认：“~/.ethash”）
  --ethash.dagsinmem value            要保存在内存中的最近 ethash 挖掘 DAG 的数量（每个 1+GB）（默认值：1）
  --ethash.dagsondisk value           最近要保存在磁盘上的 ethash 挖掘 DAG 的数量（每个 1+GB）（默认值：2）
  --ethash.dagslockmmap               为最近的 ethash 挖掘 DAG 锁定内存映射

交易池选项：
  --txpool.locals value               逗号分隔的账户被视为本地（不刷新，优先包含）
  --txpool.nolocals                   对本地提交的交易禁用价格豁免
  --txpool.journal value              本地事务的磁盘日志以在节点重新启动后存活（默认值：“transactions.rlp”）
  --txpool.rejournal value            重新生成本地事务日志的时间间隔（默认：1h0m0s）
  --txpool.pricelimit value           强制执行的最低 gas 价格限制以接受池（默认值：1）
  --txpool.pricebump value            替换现有交易的价格上涨百分比（默认值：10） transaction (default: 10)
  --txpool.accountslots value         每个帐户保证的最小可执行交易槽数（默认值：16）
  --txpool.globalslots value          所有账户的最大可执行交易槽数（默认值：5120）
  --txpool.accountqueue value         每个帐户允许的最大不可执行事务槽数（默认值：64）
  --txpool.globalqueue value          所有账户的最大不可执行交易槽数（默认：1024）
  --txpool.lifetime value             不可执行事务排队的最长时间（默认值：3h0m0s）

性能调整选项：
  --cache value                       分配给内部缓存的兆字节内存（默认 = 4096 主网全节点，128 轻模式）（默认：1024）
  --cache.database value              用于数据库 io 的缓存内存限额百分比（默认值：50）
  --cache.trie value                  用于 trie 缓存的缓存内存余量百分比（默认 = 15% 完整模式，30% 存档模式）（默认：15）
  --cache.trie.journal value          trie缓存的磁盘日志目录以在节点重新启动后存活（默认值：“triecache”）
  --cache.trie.rejournal value        重新生成 trie 缓存日志的时间间隔（默认值：1h0m0s）
  --cache.gc value                    用于 trie 修剪的缓存内存余量百分比（默认 = 25% 完整模式，0% 存档模式）（默认：25）
  --cache.snapshot value              于快照缓存的缓存内存百分比（默认 = 10% 完整模式，20% 存档模式）（默认：10）
  --cache.noprefetch                  在块导入期间禁用启发式状态预取（更少的 CPU 和磁盘 IO，更多的时间等待数据）
  --cache.preimages                   启用记录 trie 键的 SHA3/keccak 原映射

账户选项：
  --unlock value                      逗号分隔的要解锁的账户列表
  --password value                    用于非交互式密码输入的密码文件
  --signer value                      外部签名者（ipc文件的url或路径）
  --allow-insecure-unlock             当与账户相关的 RPC 被 http 暴露时，允许不安全的账户解锁

API 和控制台选项：
  --ipcdisable                        禁用 IPC-RPC 服务器
  --ipcpath value                     数据目录中 IPC 套接字/管道的文件名（显式路径转义它）
  --http                              启用 HTTP-RPC 服务器
  --http.addr value                   HTTP-RPC 服务器监听接口（默认：“localhost”）
  --http.port value                   HTTP-RPC 服务器监听端口（默认：8545）
  --http.api value                    API 通过 HTTP-RPC 接口提供
  --http.rpcprefix value              提供 JSON-RPC 的 HTTP 路径路径前缀。使用“/”在所有路径上投放。
  --http.corsdomain value             逗号分隔的域列表，从中接受跨源请求（浏览器强制）
  --http.vhosts value                 逗号分隔的虚拟主机名列表，从中接受请求（服务器强制）。接受“*”通配符。 （默认：“localhost”）
  --ws                                启用 WS-RPC 服务器
  --ws.addr value                     WS-RPC 服务器监听接口（默认：“localhost”）
  --ws.port value                     WS-RPC 服务器监听端口（默认：8546）
  --ws.api value                      API 通过 WS-RPC 接口提供
  --ws.rpcprefix value                提供 JSON-RPC 的 HTTP 路径前缀。使用“/”在所有路径上投放。
  --ws.origins value                  接受 websockets 请求的来源
  --graphql                           在 HTTP-RPC 服务器上启用 GraphQL。请注意，只有同时启动了 HTTP 服务器才能启动 GraphQL。
  --graphql.corsdomain value          逗号分隔的域列表，从中接受跨源请求（浏览器强制）
  --graphql.vhosts value              逗号分隔的虚拟主机名列表，从中接受请求（服务器强制）。接受“*”通配符。 （默认：“本地主机”）
  --rpc.gascap value                  设置可以在 eth_call/estimateGas 中使用的 gas 上限（0=infinite）（默认值：50000000）
  --rpc.evmtimeout value              设置用于 eth_call 的超时（0=无限）（默认值：5s）
  --rpc.txfeecap value                设置可以通过 RPC API 发送的交易费用上限（以太币）（0 = 无上限）（默认值：1）
  --rpc.allow-unprotected-txs         允许通过 RPC 提交未受保护（非 EIP155 签名）的交易
  --jspath loadScript                 loadScript 的 JavaScript 根路径（默认值：“.”）
  --exec value                        执行 JavaScript 语句
  --preload value                     逗号分隔的 JavaScript 文件列表以预加载到控制台

网络选项：
  --bootnodes value                   逗号分隔的用于 P2P 发现引导的 enode URL
  --discovery.dns value               设置 DNS 发现入口点（使用 "" 禁用 DNS）
  --port value                        网络监听端口（默认：30303）
  --maxpeers value                    网络对等点的最大数量（如果设置为 0，则禁用网络）（默认值：50）
  --maxpendpeers value                挂起连接尝试的最大次数（如果设置为 0，则使用默认值）（默认值：0）
  --nat value                         NAT 端口映射机制 (any|none|upnp|pmp|extip:<IP>) (默认: "any")
  --nodiscover                        禁用对等发现机制（手动添加对等）
  --v5disc                            启用实验性 RLPx V5（主题发现）机制
  --netrestrict value                 将网络通信限制到给定的 IP 网络（CIDR 掩码）
  --nodekey value                     P2P节点密钥文件
  --nodekeyhex value                  P2P 节点密钥为十六进制（用于测试）

挖矿选项: 
  --mine                              启用挖矿
  --miner.threads value               用于挖掘的 CPU 线程数（默认值：0）
  --miner.notify value                逗号分隔的 HTTP URL 列表以通知新的工作包
  --miner.notify.full                 使用待处理的块头而不是工作包通知
  --miner.gasprice value              挖掘交易的最低 gas 价格（默认值：1000000000）
  --miner.gaslimit value              开采区块的目标 gas 上限（默认值：8000000）
  --miner.etherbase value             块挖矿奖励的公共地址（默认=第一个帐户）（默认：“0”）
  --miner.extradata value             矿工设置的区块额外数据（默认 = 客户端版本）
  --miner.recommit value              重新创建正在开采的区块的时间间隔（默认值：3s）
  --miner.noverify                    禁用远程隔离验证

GAS 价格预言机选项:
  --gpo.blocks value                  最近要检查 gas 价格的块数（默认值：20）
  --gpo.percentile value              建议的 gas 价格是一组最近交易 gas 价格的给定百分比（默认值：60）
  --gpo.maxprice value                gpo 推荐的最大交易优先费用（或伦敦分叉前的gasprice）（默认值：500000000000）
  --gpo.ignoreprice value             gpo 将忽略交易的 Gas 价格（默认值：2）

虚拟机选项：
  --vmdebug                           记录对VM和合约调试有用的信息

记录和调试选项：
  --fakepow                           禁用工作证明验证
  --nocompaction                      在导入后禁用数据库压缩
  --verbosity value                   记录详细程度：0=silent，1=error，2=warn，3=info，4=debug，5=detail（默认值：3）
  --vmodule value                     每个模块的详细程度：<pattern>=<level> 的逗号分隔列表（例如 eth/*=5,p2p=4）
  --log.json                          使用 JSON 格式化日志
  --log.backtrace value               在特定的日志记录语句中请求堆栈跟踪（例如“block.go:271”）
  --log.debug                         在日志消息前添加调用栈点位置（文件和行号）
  --pprof                             启用 pprof HTTP 服务器
  --pprof.addr value                  pprof HTTP 服务器监听接口（默认：“127.0.0.1”）
  --pprof.port value                  pprof HTTP 服务器监听端口（默认：6060）
  --pprof.memprofilerate value        以给定的速率打开内存分析（默认值：524288）
  --pprof.blockprofilerate value      以给定的速率打开块分析（默认值：0）
  --pprof.cpuprofile value            将 CPU 配置文件写入给定文件
  --trace value                       将执行跟踪写入给定文件

指标和统计选项：
  --metrics                              启用指标收集和报告
  --metrics.expensive                    启用昂贵的指标收集和报告
  --metrics.addr value                   启用独立的metrics HTTP服务器监听接口（默认：“127.0.0.1”）
  --metrics.port value                   Metrics HTTP 服务器监听端口（默认：6060）
  --metrics.influxdb                     启用指标导出/推送到外部 InfluxDB 数据库
  --metrics.influxdb.endpoint value      InfluxDB API 端点报告指标（默认值：“http://localhost:8086”）
  --metrics.influxdb.database value      InfluxDB 数据库名称，将报告的指标推送到（默认值：“geth”）
  --metrics.influxdb.username value      授权访问数据库的用户名（默认值：“test”）
  --metrics.influxdb.password value      授权访问数据库的密码（默认：“test”）
  --metrics.influxdb.tags value          附加到所有测量值的逗号分隔的 InfluxDB 标签（键/值）（默认值：“host=localhost”）
  --metrics.influxdbv2                   启用指标导出/推送到外部 InfluxDB v2 数据库
  --metrics.influxdb.token value         授权访问数据库的令牌（仅限 v2）（默认值：“test”）
  --metrics.influxdb.bucket value        InfluxDB 存储桶名称，用于将报告的指标推送到（仅限 v2）（默认值：“geth”）
  --metrics.influxdb.organization value  InfluxDB 组织名称（仅限 v2）（默认值：“geth”）
  
别名（已弃用）选项：
  --nousb                             禁用监控和管理 USB 硬件钱包（已弃用）

其他选项：
  --snapshot                                启用快照数据库模式（默认 = 启用）
  --bloomfilter.size value                  分配给bloom-filter进行修剪的兆字节内存（默认值：2048）
  --help, -h                                显示帮助
  --catalyst                                Catalyst 模式（eth2 集成测试）
  --override.arrowglacier value             手动指定 Arrow Glacier fork-block，覆盖捆绑设置（默认值：0）
  --override.terminaltotaldifficulty value  Manu手动指定 TerminalTotalDifficulty，覆盖捆绑设置（默认值：0）


COPYRIGHT:
   Copyright 2013-2021 The go-ethereum Authors
```