## 使用Fabric-Go-SDK实现客户端操作

### 一、下载SDK
下载SDK到GOPATH路径中:
```
go get -u github.com/hyperledger/fabric-sdk-go
```

### 二、配置
在`$GOPATH\src\github.com\hyperledger\fabric-sdk-go\test\fixtures\config`目录下
能够找到一些配置文件模板，以下我的配置：
```
version: 1.0.0
client:
  organization: org1
  logging:
    level: info
  cryptoconfig:
    path: /home/vagrant/fabric/crypto-config
  credentialStore:
    path: "/tmp/hfc-kvs"
    cryptoStore:
      path: /tmp/msp
  BCCSP:
    security:
      enabled: true
      default:
        provider: "SW"
      hashAlgorithm: "SHA2"
      softVerify: true
      level: 256
  tlsCerts:
    systemCertPool: false
    client:
      key:
        path: /home/vagrant/fabric/crypto-config/peerOrganizations/org1.36sn.com/users/User1@org1.36sn.com/tls/client.key
      cert:
        path: /home/vagrant/fabric/crypto-config/peerOrganizations/org1.36sn.com/users/User1@org1.36sn.com/tls/client.crt
channels:
  # 管道名
  zsjr:
    peers:
      peer0.org1.36sn.com:
        endorsingPeer: true
        chaincodeQuery: true
        ledgerQuery: true
        eventSource: true
    policies:
      queryChannelConfig:
        minResponses: 1
        maxTargets: 1
        retryOpts:
          attempts: 5
          initialBackoff: 500ms
          maxBackoff: 5s
          backoffFactor: 2.0
organizations:
  org1:
    mspid: Org1MSP
    cryptoPath:  peerOrganizations/org1.36sn.com/users/{username}@org1.36sn.com/msp
    peers:
      - peer0.org1.36sn.com
peers:
  peer0.org1.36sn.com:
    url: peer0.org1.36sn.com:7051
    grpcOptions:
      ssl-target-name-override: peer0.org1.36sn.com
      fail-fast: false
      allow-insecure: false
    tlsCACerts:
      path: /home/vagrant/fabric/crypto-config/peerOrganizations/org1.36sn.com/tlsca/tlsca.org1.36sn.com-cert.pem
```
### 三、编写客户端
```
package main

import (
	"fmt"
	"github.com/hyperledger/fabric-sdk-go/pkg/client/channel"
	"github.com/hyperledger/fabric-sdk-go/pkg/common/errors/retry"
	"github.com/hyperledger/fabric-sdk-go/pkg/common/providers/core"
	"github.com/hyperledger/fabric-sdk-go/pkg/core/config"
	"github.com/hyperledger/fabric-sdk-go/pkg/fabsdk"
	"log"
)

const (
	channelID      = "zsjr"
	orgName        = "Org1"
	orgAdmin       = "Admin"
	ordererOrgName = "Orderer"
	ccID           = "example"
)

// ExampleCC query and transaction arguments
var queryArgs = [][]byte{[]byte("b")}
var txArgs = [][]byte{[]byte("a"), []byte("b"), []byte("1")}

func setupAndRun(configOpt core.ConfigProvider, sdkOpts ...fabsdk.Option) {
	//Init the sdk config
	sdk, err := fabsdk.New(configOpt, sdkOpts...)
	if err != nil {
		log.Panicf("Failed to create new SDK: %s", err)
	}
	defer sdk.Close()
	// ************ setup complete ************** //

	//prepare channel client context using client context
	clientChannelContext := sdk.ChannelContext(channelID, fabsdk.WithUser("Admin"), fabsdk.WithOrg(orgName))

	// Channel client is used to query and execute transactions (Org1 is default org)
	client, err := channel.New(clientChannelContext)

	if err != nil {
		log.Panicf("Failed to create new channel client: %s", err)
	}

	value := queryCC(client)
	fmt.Printf("value is %s\n", string(value))

	// Move funds
	executeCC(client)
}

func executeCC(client *channel.Client) {
	_, err := client.Execute(channel.Request{ChaincodeID: ccID, Fcn: "invoke", Args: txArgs},
		channel.WithRetry(retry.DefaultChannelOpts))
	if err != nil {
		log.Panicf("Failed to move funds: %s", err)
	}
}

func queryCC(client *channel.Client) []byte {
	response, err := client.Query(channel.Request{ChaincodeID: ccID, Fcn: "query", Args: queryArgs},
		channel.WithRetry(retry.DefaultChannelOpts))
	if err != nil {
		log.Panicf("Failed to query funds: %s", err)
	}
	fmt.Println(response)

	return response.Payload
}

func main() {
	configPath := "./config.yaml"
	//End to End testing
	setupAndRun(config.FromFile(configPath))
}
```
该客户端完成两个功能
  * 账户余额查询
  * 由A账户向B账户转款
