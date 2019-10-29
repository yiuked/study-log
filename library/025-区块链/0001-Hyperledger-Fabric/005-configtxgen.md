## configtxgen
`configtxgen`模块用来生成`orderer`的初始化文件和`channel`的初始化文件。
```
Usage of ./configtxgen:
  -asOrg string 以某个特定组织生成配置
  -channelCreateTxBaseProfile string
        Specifies a profile to consider as the orderer system channel current state to allow modification of non-application parameters during channel create tx generation. Only valid in conjuction with 'outputCreateChannelTx'.
  -channelID string
        The channel ID to use in the configtx
  -configPath string
        The path containing the configuration to use (if set)
  -inspectBlock string
        Prints the configuration contained in the block at the specified path
  -inspectChannelCreateTx string
        Prints the configuration contained in the transaction at the specified path
  -outputAnchorPeersUpdate string
        Creates an config update to update an anchor peer (works only with the default channel creation, and only for the first update)
  -outputBlock string
        The path to write the genesis block to (if set)
  -outputCreateChannelTx string
        The path to write a channel creation configtx to (if set)
  -printOrg string
        Prints the definition of an organization as JSON. (useful for adding an org to a channel manually)
  -profile string
        The profile from configtx.yaml to use for generation. (default "SampleInsecureSolo")
  -version
        Show version information
```
