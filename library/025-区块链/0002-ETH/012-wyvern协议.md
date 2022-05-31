# 实现ERC20购买ERC1155

###  准备
需要部署wyvern协议中的以下合约：
- atomicizer
> 在一个订单中执行多笔交易，如果有一笔失败，所有交易都撤回
- exchange
> 交换合约
- registry
> 代理合约
> WyvernRegistry 实例化时，会调用父类ProxyRegistry的父类Ownable构造函数，设定当前操作者为合约的所有者
- statici

`WyvernRegistry`构造函数中，会创建一个`AuthenticatedProxy`,`AuthenticatedProxy`接收两个参数，一个是当前操作者用户地址，该用户将拥有吊销或者不吊销代理的权限，启动是会吊销代理权限，使得只有他自己可以调用`AuthenticatedProxy`的` proxy(address dest, HowToCall howToCall, bytes memory data)`方法。
构造函数还会将`delegateProxyImplementation`(委托代理执行)指定为上面的`AuthenticatedProxy`实例地址。

继承关系：`WyvernRegistry` is `ProxyRegistry` is `Ownable`，`Ownable`的构造函数会把当前操作者设置为合约的`_owner`(拥有者)。`_owner`将可以执行`grantInitialAuthentication`,`grantInitialAuthentication`接收一个合约地址，这个合约地址将被保存在`contracts`动态变量中，`contracts`的合约可以调用代理。

`WyvernRegistry` is `ProxyRegistry`有一个`registerProxy()`方法，该方法将当前操作者添加到动态变量`mapping(address => OwnableDelegateProxy) public override proxies`  中，`key`为用户的地址，值为一个`OwnableDelegateProxy`合约，这个合约在构造函数中，有三个参数：
- 参数1：接收当前操作者的`address`
- 参数2：接收前面的`delegateProxyImplementation`
- 参数3：接收`delegateProxyImplementation`的`initialize`的abi方法:
```
proxy = new OwnableDelegateProxy(user, delegateProxyImplementation, abi.encodeWithSignature("initialize(address,address)", user, address(this)));
```


`OwnedUpgradeabilityStorage` 是一个用来保存`_implementation`与`_upgradeabilityOwner`







分析过程看到一段这样的代码，对于其中的`address(impl)`,这只是一个内部引用，`AuthenticatedProxy`并没有部署，不应该有地址，经过验证发现`solidity`中每一个合约不管理是否部署，都会有地址
```
constructor ()  
    public  
{     
    AuthenticatedProxy impl = new AuthenticatedProxy();  
    impl.initialize(address(this), this);  
    impl.setRevoke(true);  
    delegateProxyImplementation = address(impl);  
  
    emit addr("hello",address(this),address(impl));  
}
```