#### ZMQContext
```
ZMQContext {
__construct ([ integer $io_threads = 1 [, boolean $is_persistent = true ]] )
public mixed getOpt ( string $key )
public ZMQSocket getSocket ( integer $type [, string $persistent_id = null [, callback $on_new_socket = null ]] )
public boolean isPersistent ( void )
public ZMQContext setOpt ( integer $key , mixed $value )
}
```
```
ZMQContext::__construct — Construct a new ZMQContext object
ZMQContext::getOpt — Get context option
ZMQContext::getSocket — Create a new socket
ZMQContext::isPersistent — Whether the context is persistent
ZMQContext::setOpt — Set a socket option
```

#### ZMQSocket
public ZMQSocket ZMQSocket::bind ( string $dsn [, boolean $force = false ] ) 新增一个绑定
public ZMQSocket ZMQSocket::unbind ( string $dsn ) 解除绑定

public boolean ZMQSocket::isPersistent ( void ) 检测socket是否持久
public array ZMQSocket::getEndpoints ( void ) 获取端点列表
public string ZMQSocket::getPersistentId ( void ) 获取持久ID

public string ZMQSocket::recv ([ integer $mode = 0 ] ) 收取一条信息
public string ZMQSocket::recvMulti ([ integer $mode = 0 ] ) 收取多条信息，
public ZMQSocket ZMQSocket::send ( array $message [, integer $mode = 0 ] ) 发送一条信息
public ZMQSocket ZMQSocket::sendmulti ( array $message [, integer $mode = 0 ] ) 发送一组信息，需要与recvMulti搭配使用

public integer ZMQSocket::getSocketType ( void ) 获取socket类型
public mixed ZMQSocket::getSockOpt ( string $key ) 获取一个socket属性
public ZMQSocket ZMQSocket::setSockOpt ( integer $key , mixed $value ) 设置一个sokcet属性


----------------------------------------------------------------------------------

public array ZMQSocket::getEndpoints ( void ) 获取端点列表
```
$queue = new ZMQSocket(new ZMQContext(), ZMQ::SOCKET_REQ, "MySock1");

/* Connect to an endpoint */
$queue->connect("tcp://127.0.0.1:5555");
$status = $queue->getEndpoints();
print_r($status);
```
输出结果
```
Array
(
    [connect] => Array
        (
            [0] => tcp://127.0.0.1:5555
        )

    [bind] => Array
        (
        )

)
```

public string ZMQSocket::getPersistentId ( void ) 获取持久ID
```
$queue = new ZMQSocket(new ZMQContext(), ZMQ::SOCKET_REQ, "MySock1");

/* Connect to an endpoint */
$queue->connect("tcp://127.0.0.1:5555");
echo $status = $queue->getPersistentId();
//输出结果：MySock1，为new ZMQSocket中的第三个参数
```

public integer ZMQSocket::getSocketType ( void ) 获取socket类型
```
$queue = new ZMQSocket(new ZMQContext(), ZMQ::SOCKET_REQ, "MySock1");

/* Connect to an endpoint */
$queue->connect("tcp://127.0.0.1:5555");
echo $status = $queue->getSocketType();
//输出结果：3，为new ZMQSocket中的第二个参数
```
