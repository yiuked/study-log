## 解决mySQL占用内存超大问题

为了装`mysql`环境测试，装上后发现启动后`mysql`占用了很大的虚拟内存，达8百多兆。  
网上搜索了一下，得到高人指点my.ini。再也没见再详细的了..只好打开my.ini逐行的啃，  
虽然英文差了点，不过多少M还是看得明的^-^  

更改后如下：
```
innodb_buffer_pool_size=576M ->256M InnoDB引擎缓冲区占了大头，首要就是拿它开刀
query_cache_size=100M        ->16M  查询缓存
tmp_table_size=102M          ->64M  临时表大小
key_buffer_size=256m         ->32M
```

重启`mysql`服务后，虚拟内存降到200以下．  

优化`mysql`数据库性能的十个参数


#### max_connections：
允许的同时客户的数量。增加该值增加 `mysqld` 要求的文件描述符的数量。这个数字应该增加，否则，你将经常看到 `too many connections` 错误。 默认数值是100，我把它改为1024 。  

#### record_buffer：
每个进行一个顺序扫描的线程为其扫描的每张表分配这个大小的一个缓冲区。如果你做很多顺序扫描，你可能想要增加该值。默认数值是131072(128k)，我把它改为16773120 (16m)  


#### key_buffer_size：
索引块是缓冲的并且被所有的线程共享。key_buffer_size是用于索引块的缓冲区大小，增加它可得到更好处理的索引(对所有读和多重写)，到你能负担得起那样多。  
如果你使它太大，系统将开始换页并且真的变慢了。默认数值是8388600(8m)，我的`mysql`主机有2gb内存，所以我把它改为 402649088(400mb)。  


#### back_log：
要求 `mysql` 能有的连接数量。当主要`mysql`线程在一个很短时间内得到非常多的连接请求，这就起作用，然后主线程花些时间(尽管很短)检查连接并且启动一个新线程。   
back_log 值指出在`mysql`暂时停止回答新请求之前的短时间内多少个请求可以被存在堆栈中。只有如果期望在一个短时间内有很多连接，你需要增加它，换句话说，这值对到来的tcp/ip连接的侦听队列的大小。  
你的操作系统在这个队列大小上有它自己的限制。试图设定back_log高于你的操作系统的限制将是无效的。  
当你观察你的主机进程列表，发现大量 264084 | unauthenticated user | xxx.xxx.xxx.xxx | null | connect | null | login | null 的待连接进程时，就要加大 back_log 的值了。默认数值是50，我把它改为500。  



#### interactive_timeout：
服务器在关闭它前在一个交互连接上等待行动的秒数。一个交互的客户被定义为对 `mysql_real_connect()`使用 client_interactive 选项的客户。 默认数值是28800，我把它改为7200。  


#### sort_buffer：
每个需要进行排序的线程分配该大小的一个缓冲区。增加这值加速order by或group by操作。默认数值是2097144(2m)，我把它改为 16777208 (16m)。

#### table_cache：
为所有线程打开表的数量。增加该值能增加mysqld要求的文件描述符的数量。`mysql`对每个唯一打开的表需要2个文件描述符。默认数值是64，我把它改为512。


#### thread_cache_size：
可以复用的保存在中的线程的数量。如果有，新的线程从缓存中取得，当断开连接的时候如果有空间，客户的线置在缓存中。如果有很多新的线程，为了提高性能可以这个变量值。通过比较 connections 和 threads_created 状态的变量，可以看到这个变量的作用。我把它设置为 80。

#### `mysql`的搜索功能
用`mysql`进行搜索，目的是能不分大小写，又能用中文进行搜索
只需起动mysqld时指定 --default-character-set=gb2312


#### wait_timeout：
服务器在关闭它之前在一个连接上等待行动的秒数。 默认数值是28800，我把它改为7200。

注：参数的调整可以通过修改 /etc/my.cnf 文件并重启 `mysql` 实现。这是一个比较谨慎的工作，上面的结果也仅仅是我的一些看法，你可以根据你自己主机的硬件情况（特别是内存大小）进一步修改。
