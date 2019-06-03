### 核心组件
```flow
produce=>start: 生产者
exchange=>operation: 交换器 (Exchange)
queue=>operation: 队列(Queue)
comsume=>end: 消费者

produce(right)->exchange(right)->queue(right)->comsume
```
**1. 交换机(Exchange)**  
交换机的功能主要是接收消息并且转发到绑定的队列，交换机不存储消息，在启用ack模式后，交换机找不到队列会返回错误。  
交换机有四种类型：Direct、topic、Headers、Fanout：
  * Direct：直连型交换机（direct exchange）是根据消息携带的路由键（routing key）将消息投递给对应队列的。
  * Topic（主题交换机）：队列通过路由键绑定到交换机上，然后，交换机根据消息里的路由值，将消息路由给一个或多个绑定队列。
  * Fanout（扇型交换机）：将消息路由给绑定到它身上的所有队列。不同于直连交换机，路由键在此类型上不启任务作用。如果N个队列绑定到某个扇型交换机上，当有消息发送给此扇型交换机时，交换机会将消息的发送给这所有的N个队列。
  * Headers（头交换机）：类似主题交换机，但是头交换机使用多个消息属性来代替路由键建立路由规则。通过判断消息头的值能否与指定的绑定相匹配来确立路由规则。
  * Default（默认交换机）：是一个由RabbitMQ预先声明好的名字为空字符串的直连交换机（direct exchange）。它有一个特殊的属性使得它对于简单应用特别有用处：那就是每个新建队列（queue）都会自动绑定到默认交换机上，绑定的路由键（routing key）名称与队列名称相同。
  * 类似`amq.*`的名称的交换机： 这些是RabbitMQ默认创建的交换机。这些队列名称被预留做RabbitMQ内部使用，不能被应用使用，否则抛出403 (ACCESS_REFUSED)错误。

> 交换机不会存储消息，如果当前交换机未绑定任何队列，消息会被丢弃。
