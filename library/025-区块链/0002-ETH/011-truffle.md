### Windows
**安装**
```
npm install -g truffle
```
需要依赖：
- `VS 2017`或者`VS 2015`，
- `Python 3.0` 或更高的版本

**初始项目**
```
truffle init
```

在工程中如果需要引入`openzeppelin/contracts`
```
npm install @openzeppelin/contracts
```
> 更多信息 [OpenZeppelin/openzeppelin-contracts: OpenZeppelin Contracts is a library for secure smart contract development. (github.com)](https://github.com/OpenZeppelin/openzeppelin-contracts)
`openzeppelin/contracts` 当前默认是支持`solc ^8.0.0`,如果需版本要求低的可以修改项目根目录下的`packge.json`文件，如果需要`solc ^7.0.0`:
```
{  
  "dependencies": {  
    "@openzeppelin/contracts": "^3.4.0-solc-0.7"  
  }  
}
```
需要完成后需要执行`npm install`,或者安装时直接采用：
```
npm install @openzeppelin/contracts@^3.4.0-solc-0.7
```
> 在`solc`文件在引入时需要按以下格式写:
> ```
> import "@openzeppelin/contracts/access/Ownable.sol";
> ```


**配置**
项目配置文件为`truffle-config.js`,在文件中可以配置网络与编译器版本信息
```
 development: {  
  host: "127.0.0.1",     // Localhost (default: none)  
  port: 8545,            // Standard Ethereum port (default: none)  
  network_id: "*",       // Any network (default: none)  
},

// Configure your compilers  
compilers: {  
  solc: {  
    version: "0.7.5",      // Fetch exact version from solc-bin (default: truffle's version)  
    // docker: true,        // Use "0.5.1" you've installed locally with docker (default: false)    // settings: {          // See the solidity docs for advice about optimization and evmVersion    //  optimizer: {    //    enabled: false,    //    runs: 200    //  },    //  evmVersion: "byzantium"    // }  }  
},
```
> 网络信息可以安装canache

**编译项目**
```
truffle compile
```

