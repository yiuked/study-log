写文件-编译-部署


部署：
Environment
- JavaScript VM(London) 会连接MetaMusk
Account:
- 选择MetaMusk中的账户

同步本地文件到浏览器
```
# 安装remixd
npm install -g @remix-project/remixd

# 开启同步
remixd -s /Users/mac/Documents/dev/solidity/openzeppelin-contracts/app --remix-ide https://remix.ethereum.org
```