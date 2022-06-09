以太坊合约支持读、写两种类型的成员函数，以`view`修饰的函数是只读函数，它不会修改成员变量，即不会改变合约的状态

合约可以定义事件（Event），我们在Vote合约中定义了一个`Voted`事件：

```
contract Vote {
    // Voted事件，有两个相关值:
    event Voted(address indexed voter, uint8 proposal);

    ...
}
```

只定义事件还不够，触发事件必须在合约的写函数中通过`emit`关键字实现。当调用`vote()`写方法时，会触发`Voted`事件：

```
contract Vote {
    ...

    function vote(uint8 _proposal) public {
        ...
        emit Voted(msg.sender, _proposal);
    }

    ...
}
```

## 合约执行流程
当一个合约编写完成并成功编译后，我们就可以把它部署到以太坊上。合约部署后将自动获得一个地址，通过该地址即可访问合约。

把`contract Vote {...}`看作一个类，部署就相当于一个实例化。如果部署两次，将得到两个不同的地址，相当于实例化两次，两个部署后的合约对应的成员变量是完全独立的，互不影响。

构造函数在部署合约时就会立刻执行，且仅执行一次。合约部署后就无法调用构造函数。

任何外部账户都可以发起对合约的函数调用。如果调用只读方法，因为不改变合约状态，所以任何时刻都可以调用，且不需要签名，也不需要消耗Gas。但如果调用写入方法，就需要签名提交一个交易，并消耗一定的Gas。

在一个交易中，只能调用一个合约的一个写入方法。无需考虑并发和同步的问题，因为以太坊交易的写入是严格串行的。

## 验证
由于任何外部账户都可以发起对合约的函数调用，所以任何验证工作都必须在函数内部自行完成。最常用的`require()`可以断言一个条件，如果断言失败，将抛出错误并中断执行。

常用的检查包括几类：

参数检查：

```
// 参数必须为1,2,3:
require(_proposal >= 1 && _proposal <= 3, "Invalid proposal.");
```

条件检查：

```
// 当前区块时间必须小于设定的结束时间:
require(block.timestamp < endTime, "Vote expired.");
```

调用方检查：

```
// msg.sender表示调用方地址:
require(!voted[msg.sender], "Cannot vote again.");
```

以太坊合约具备类似数据库事务的特点，如果中途执行失败，则整个合约的状态保持不变，不存在修改某个成员变量后，后续断言失败导致部分修改生效的问题：

```
function increment() {
    // 假设a,b均为成员变量:
    a++;
    emit AChanged(a);
    // 如果下面的验证失败，a不会被更新，也没有AChanged事件发生:
    require(b < 10, 'b >= 10');
    b++;
}
```

即合约如果执行失败，其状态不会发生任何变化，也不会有任何事件发生，仅仅是调用方白白消耗了一定的Gas。



当执行函数时不会去修改区块中的数据状态时，那么这个函数就可以被声明成constant的，比如说getter类的方法。
constant是 view 的别名，不过constant在0.5.0版本中将会被去掉。这也是我们在写智能合约时需要注意的事项。目前网络上的示例基本上还都采用constant来进行修饰。

`pure`不读取全局、状态变量

### 数据类型
#### 数组
**动态数组**
```
uint[] public users = [1,2,3]
```
> 支持 `users.push(4)`添加参数，定长数组不支持。
> 支持`users.pop()`
> 支持`users.length` 属性来获取长度
> `delete users[2]` 只删除值不改变数组长度
> 内存中不能定义动态数组


**定长数组**
> 在内存中局部变量只能定义定长数组，动态数组只能存放在状态变量中

**实现一个删除函数**
方式一
```
function remove(uint _iddex) public {
	required(_index<arr.length,"index out")
	for (uint i=_iddex;i<arr.length-1;i++){
		arr[i]=arr[i+1]
	}
	arr.pop()
}
```
> 这个方法太浪费`gas`

方式二
```
function remove(uint _idex) public {
	required(_index<arr.length,"index out")
	arr[_idex] = arr[arr.lenght-1]
	arr.pop()
}
```
> 该方式会打乱数组顺序

--------------------------------------

#### 映射
**语法**
```
// 定义
mapping(address => uint) public balances;
mapping(address=>mapping(address=>bool)) public isFriend;

// 赋值
balance[msg.sender] = 100;
isFriend[msg.sender][address(this)]=true;

// 删除合约(删除只会把值重置为默认值)
delete balances[msg.sender];
```

#### 结构体
**语法**
```
// 定义
struct  Car{
	string model;
	uint year;
	address owner;
}

// 引用 
Car memory car1 Car("Hongda",2019,msg.sender)
Car memory car2 Car({model:"Hongda",year:2019,address:msg.sender})
Car memory car3;
car3.model="hongda";
car3.year= 2019;
car3.owner=msg.sneder;

// 删除（将值恢复为默认）
delete car2.owner;
```


#### 枚举
**语法**
```
// 定义
enum Status {
	None,
	Padding,
	Completed,
	Canceled
}

```

### 变量

**状态变量**
>  概念：把一个数据写到链上，只要不写修改的方法，会永远存储在链上，状态变更默认会有一个`getter`方法，在对状态变量进行读取时，需要在函数上添加`view`修饰符。
>  默认值：
>  - bool 默认为 false
>  - uint,int 默认为0
>  - address 默认为0x0000*32位*00
>  - bytes32 默认0x00*64位*00

**局部变量***
> 只在函数内部生效，函数结束则终止，对外不可见

**全局变量**
> 不用定义就可以使用的变量，这些变量通常记录账户信息与链信息，只读取全局变量时需要添加`view`修饰词，常用的全局变量如下：
```
msg.sender              // 上个调用账户或者合约
block.timestamp         // 读取时间，如果写方法则为出块时间
block.number            // 块编号
address(this)           // 当前合约地址
```

**修饰符**
- `memory`只对当前函数有效，数组、字符串
- `calldata` 与 `memory`类似，但只能用在函数的参数中，参数传递时可以不用重新赋值,`memory`会。
- `storage`永久存储，代表状态变量


### 常量
**定义**
> 通过 `constant` 定义，通常大写 :
> ```
> address public constant MY_ADDRESS = 0x000...
> ```
> 通过`immutable`实现类常量定义
> ```
> address public immutable owner;
> ```

**优点**
> 相对对全局变量，gas费用要少一点


-------------------------------------
### 函数
#### 1. 函数修改器
主要用于减少重复代码，统一对函数进行执行前或者执行后的一些处理
**语法**
```
// 定义修改器
modifier check(uint x){
	require(x<=10,"x err");
	_;  // 此处代理引用函数执行的代码
	x++;
}

// 调用修改器
function add(uint x) external check {
	x++;
}
```

#### 2. 函数的返回值
**语法**
```
// 定义1
function userInfo() public pure returns (age uint,isReg bool){
	return (18,true);
}
// 定义2
function userInfo() public pure returns (uint,bool){
	return (18,true);
}

// 接收
function call(){
	// 接收1
	(uint age, bool isReg) = userInfo()
	// 接收2（忽略第一个返回）
	(, bool isReg) = userInfo()
}
```
> 返回与golang当中的返回有点类似
> 返回字符串时，需要添加 `memory`

#### 3.修饰符
**constant、view、pure**
>  三个函数修饰词的作用是告诉编译器，函数不改变/不读取状态变量，这样函数执行就可以不消耗gas了。constant在4.17以后废弃，view的作用和constant一模一样，可以读取状态变量但是不能改；pure则更为严格，pure修饰的函数不能改也不能读状态变量，否则编译通不过。
**payable函数**
> 具有`payable`属性的函数可以接收主币，`constructor`、`fallback`、`receive`函数也可以添加该属性，当合约中有其它函数添加`payable`时，会跳过`fallback`与`receive`。
------------------------------------
#### 4.回退函数
**fallback() 函数**
当调用的函数不存在时，或者向合约中发送主币时调用，如果要接收主币需要添加`payable`,不添加则不接收
```
fallback() external payable{}
```
**receive()函数**
```
receive() external payable{}
```
> 优化级`receive`高于`fallback`，当有参数时调用`fallback`,因为`receive`不带参数
---------------------------------------
-------------------------------------
-------------------------------------
### 流程控制
**循环**
> `for(uint i=0;i<10;i++)`
> `while(i<10)`
> 通过`continue`跳过，`break`退出
**三元运算符**
> `return x<10?1:2;`

------------------------------------
-------------------------------------
### 错误处理
当合约出现异常时，调用正常的错误处理方法可以退还gas费用，同时使状态变量回滚，常见的错误处理方法有
#### require

```
function add(uint x) public pure{
	require(x<=10,"x err");
}
```
#### revert
**语法**
```
function add(uint x) public pure{
	if (x<=0){
		revert("x err");
	}
}
```
#### assert
**语法**
```
function add(uint x) public pure{
	assert(x == 100);
}
```

#### 自定义错误
**语法**
```
error MyErr(address sender,uint i);
function add(uint x) public view{
	if (x<=0){
		revert MyErr(msg.sender,x);
	}
}
```

-------------------------------------
-------------------------------------
###  事件
在Web3浏览器与区块链日志中会打印相应的信息
**语法**
```
contract Event{
	// 定义
	event Log(string msg,uint val);
	// 定义有索引的事件（有索引的变量定义不能超过3个，超过会报错）
	event IndexLog(address indexed sender,uint val);
	// 调用
	function example() external{
		emit Log("foo",123);
		emit IndexLog(msg.sender,789);
	}
}
```

-------------------------------------
### 继承
**语法**
```
// 定义
contract A {
	contract(string memory as) {
	
	}
	// virtual 修饰符表示该方法可以被重写
	function A1() public pure virtual{
	}
	function A2() public pure virtual{
	}
}

contract B is A{
	contract(string memory as) {
	
	}
	// 调用父级合约
	function A1() {
		A.A2();
		super.A2();
	}
}
// 引用
// 多重继承
// 构造函数固定参数
contract C is A("A")，B("B") {

}
// 构造函数传入参数
contract C is A,B {
	contract(string memory A,string memory B) A(A) B(B){} 
}
```
> - 继承可以重写方法，需要在父类中添加`virtual`修饰符
> - 多重继承时，靠近基础类的需要写在前面 
> - 通过`super`调用父级合约是会向上传递，但如果多个父级合约继承同一个合约时，方法只会调用一次（即每个合约的方法只会被调用一次）

-------------------------------------
###  可视范围
可视范围可修饰函数，也可以修饰变量

**private 内部可视**
> 在合约内部可见。

**internal 内部与继承可视**
> 只有在合约内部与子合约可视。

**external 外部可视**
> 在合约中的内部其它函数不可调用它，只能通过外部调用。（可以通过this.funcName的形式访问）

**public 公开可视**
> 内部、外部都可以调用

-------------------------------------
### 转账
消费2300 gas，失败则执行reverts
** transfer **
```
function transferTx(address payable _to) external payable{
	_to.transfer(1);
}
```
消费2300 gas,返回bool
**send**
```
function sendTx(address payable _to) external payable{
	bool send = _to.send(1);
	require(succes,"err");
}
```
消费所有gas，返回bool与data
**call**
```
function callTx(address payable _to) external payable{
	(bool send,) = _to.call{value:1}("call");
	require(succes,"err");
}
```


### 调用其它合约
#### 内部调用
#### 低级call调用
#### 委托调用


### 问题
1. gas级与主币的关系

hardhat