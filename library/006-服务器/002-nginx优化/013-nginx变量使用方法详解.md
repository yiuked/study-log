`Nginx` 的配置文件使用的就是一门微型的编程语言，许多真实世界里的 Nginx 配置文件其实就是一个一个的小程序。
当然，是不是“图灵完全的”暂且不论，至少据我观察，它在设计上受 `Perl` 和 `Bourne Shell` 这两种语言的影响很大。
在这一点上，相比 `Apache` 和 `Lighttpd` 等其他 `Web` 服务器的配置记法，不能不说算是 `Nginx` 的一大特色了。
既然是编程语言，一般也就少不了“变量”这种东西`（当然，Haskell` 这样奇怪的函数式语言除外了）。  

熟悉 `Perl、Bourne Shell、C/C++` 等命令式编程语言的朋友肯定知道，变量说白了就是存放“值”的容器。
而所谓“值”，在许多编程语言里，既可以是 3.14 这样的数值，也可以是 `hello world` 这样的字符串，
甚至可以是像数组、哈希表这样的复杂数据结构。然而，
在 `Nginx` 配置中，变量只能存放一种类型的值，
因为也只存在一种类型的值，那就是字符串。

比如我们的` nginx.conf` 文件中有下面这一行配置：
`set $a "hello world";`

我们使用了标准 `ngx_rewrite` 模块的 set 配置指令对变量 `$a` 进行了赋值操作。
特别地，我们把字符串 h`ello world` 赋给了它。

`我们看到，Nginx` 变量名前面有一个 `$` 符号，这是记法上的要求。
所有的 `Nginx` 变量在 `Nginx` 配置文件中引用时都须带上 `$` 前缀。这种表示方法和 `Perl、PHP` 这些语言是相似的。

虽然 `$` 这样的变量前缀修饰会让正统的 `Java` 和 `C#` 程序员不舒服，
但这种表示方法的好处也是显而易见的，那就是可以直接把变量嵌入到字符串常量中以构造出新的字符串：

```
set $a hello;
set $b "$a, $a";
```
这里我们通过已有的 `Nginx` 变量 `$a` 的值，来构造变量 `$b` 的值，于是这两条指令顺序执行完之后，`$a` 的值是 `hello` ，而 `$b` 的值则是 `hello`, `hello`. 这种技术在 `Perl` 世界里被称为“变量插值”（`variable interpolation`），它让专门的字符串拼接运算符变得不再那么必要。我们在这里也不妨采用此术语。

我们来看一个比较完整的配置示例：

```
server {
  listen 8080;
  location /test {
    set $foo hello;
    echo "foo: $foo";
  }
}
```
这个例子省略了 `nginx.conf` 配置文件中最外围的 `http` 配置块以及 `events` 配置块。
使用 `curl` 这个 `HTTP` 客户端在命令行上请求这个 `/test` 接口，我们可以得到
```
$ curl 'http://localhost:8080/test'
foo: hello
```
这里我们使用第三方 `ngx_echo` 模块的 `echo` 配置指令将 `$foo` 变量的值作为当前请求的响应体输出。

我们看到，`echo` 配置指令的参数也支持“变量插值”。不过，需要说明的是，并非所有的配置指令都支持“变量插值”。事实上，指令参数是否允许“变量插值”，取决于该指令的实现模块。

如果我们想通过 `echo` 指令直接输出含有“美元符”（`$`）的字符串，那么有没有办法把特殊的 `$` 字符给转义掉呢？答案是否定的（至少到目前最新的 `Nginx` 稳定版 `1.0.10`）。不过幸运的是，我们可以绕过这个限制，比如通过不支持“变量插值”的模块配置指令专门构造出取值为 `$` 的 `Nginx` 变量，然后再在 `echo` 中使用这个变量。看下面这个例子：
```  
geo $dollar {
  default "$";
}
server {
  listen 8080;
    location /test {
    echo "This is a dollar sign: $dollar";
  }
}
```
测试结果如下：
```
$ curl 'http://localhost:8080/test'
This is a dollar sign: $
```
这里用到了标准模块 ngx_geo 提供的配置指令 geo 来为变量 $dollar 赋予字符串 “$”，这样我们在下面需要使用美元符的地方，就直接引用我们的 $dollar 变量就可以了。其实 ngx_geo 模块最常规的用法是根据客户端的 IP 地址对指定的 Nginx 变量进行赋值，这里只是借用它以便“无条件地”对我们的 $dollar 变量赋予“美元符”这个值。

在“变量插值”的上下文中，还有一种特殊情况，即当引用的变量名之后紧跟着变量名的构成字符时（比如后跟字母、数字以及下划线），我们就需要使用特别的记法来消除歧义，例如：
server {
listen 8080;
location /test {
set $first "hello ";
echo "${first}world";
}
}

这里，我们在 echo 配置指令的参数值中引用变量 $first 的时候，后面紧跟着 world 这个单词，所以如果直接写作 “$firstworld” 则 Nginx “变量插值”计算引擎会将之识别为引用了变量 $firstworld. 为了解决这个难题，Nginx 的字符串记法支持使用花括号在 $ 之后把变量名围起来，比如这里的 ${first}. 上面这个例子的输出是：
$ curl 'http://localhost:8080/test
hello world

set 指令（以及前面提到的 geo 指令）不仅有赋值的功能，它还有创建 Nginx 变量的副作用，即当作为赋值对象的变量尚不存在时，它会自动创建该变量。比如在上面这个例子中，如果 $a 这个变量尚未创建，则 set 指令会自动创建 $a 这个用户变量。如果我们不创建就直接使用它的值，则会报错。例如
server {
listen 8080;
location /bad {
echo $foo;
}
}

此时 Nginx 服务器会拒绝加载配置:
[emerg] unknown "foo" variable

是的，我们甚至都无法启动服务！

有趣的是，Nginx 变量的创建和赋值操作发生在全然不同的时间阶段。Nginx 变量的创建只能发生在 Nginx 配置加载的时候，或者说 Nginx 启动的时候；而赋值操作则只会发生在请求实际处理的时候。这意味着不创建而直接使用变量会导致启动失败，同时也意味着我们无法在请求处理时动态地创建新的 Nginx 变量。

Nginx 变量一旦创建，其变量名的可见范围就是整个 Nginx 配置，甚至可以跨越不同虚拟主机的 server 配置块。我们来看一个例子：
server {
listen 8080;
location /foo {
echo "foo = [$foo]";
}
location /bar {
set $foo 32;
echo "foo = [$foo]";
}
}

这里我们在 location /bar 中用 set 指令创建了变量 $foo，于是在整个配置文件中这个变量都是可见的，因此我们可以在 location /foo 中直接引用这个变量而不用担心 Nginx 会报错。

下面是在命令行上用 curl 工具访问这两个接口的结果：
$ curl 'http://localhost:8080/foo'
foo = []

$ curl 'http://localhost:8080/bar'
foo = [32]

$ curl 'http://localhost:8080/foo'
foo = []



从这个例子我们可以看到，set 指令因为是在 location /bar 中使用的，所以赋值操作只会在访问 /bar 的请求中执行。而请求 /foo 接口时，我们总是得到空的 $foo 值，因为用户变量未赋值就输出的话，得到的便是空字符串。

从这个例子我们可以窥见的另一个重要特性是，Nginx 变量名的可见范围虽然是整个配置，但每个请求都有所有变量的独立副本，或者说都有各变量用来存放值的容器的独立副本，彼此互不干扰。比如前面我们请求了 /bar 接口后，$foo 变量被赋予了值 32，但它丝毫不会影响后续对 /foo 接口的请求所对应的 $foo 值（它仍然是空的！），因为各个请求都有自己独立的 $foo 变量的副本。

对于 Nginx 新手来说，最常见的错误之一，就是将 Nginx 变量理解成某种在请求之间全局共享的东西，或者说“全局变量”。而事实上，Nginx 变量的生命期是不可能跨越请求边界的。



nginx变量使用方法详解(2)
关于 Nginx 变量的另一个常见误区是认为变量容器的生命期，是与 location 配置块绑定的。其实不然。我们来看一个涉及“内部跳转”的例子：
server {
    listen 8080;

    location /foo {
        set $a hello;
        echo_exec /bar;
    }

    location /bar {
        echo "a = [$a]";
    }
}

这里我们在 location /foo 中，使用第三方模块 ngx_echo 提供的 echo_exec 配置指令，发起到 location /bar 的“内部跳转”。所谓“内部跳转”，就是在处理请求的过程中，于服务器内部，从一个 location 跳转到另一个 location 的过程。这不同于利用 HTTP 状态码 301 和 302 所进行的“外部跳转”，因为后者是由 HTTP 客户端配合进行跳转的，而且在客户端，用户可以通过浏览器地址栏这样的界面，看到请求的 URL 地址发生了变化。内部跳转和 Bourne Shell（或 Bash）中的 exec 命令很像，都是“有去无回”。另一个相近的例子是 C 语言中的 goto 语句。

既然是内部跳转，当前正在处理的请求就还是原来那个，只是当前的 location 发生了变化，所以还是原来的那一套 Nginx 变量的容器副本。对应到上例，如果我们请求的是 /foo 这个接口，那么整个工作流程是这样的：先在 location /foo 中通过 set 指令将 $a 变量的值赋为字符串 hello，然后通过 echo_exec 指令发起内部跳转，又进入到 location /bar 中，再输出 $a 变量的值。因为 $a 还是原来的 $a，所以我们可以期望得到 hello 这行输出。测试证实了这一点：
$ curl localhost:8080/foo
a = [hello]

但如果我们从客户端直接访问 /bar 接口，就会得到空的 $a 变量的值，因为它依赖于 location /foo 来对 $a 进行初始化。

从上面这个例子我们看到，一个请求在其处理过程中，即使经历多个不同的 location 配置块，它使用的还是同一套 Nginx 变量的副本。这里，我们也首次涉及到了“内部跳转”这个概念。值得一提的是，标准 ngx_rewrite 模块的 rewrite 配置指令其实也可以发起“内部跳转”，例如上面那个例子用 rewrite 配置指令可以改写成下面这样的形式：
server {

    listen 8080;

    location /foo {
        set $a hello;
        rewrite ^ /bar;
    }

    location /bar {
        echo "a = [$a]";
    }
}

其效果和使用 echo_exec 是完全相同的。后面我们还会专门介绍这个 rewrite 指令的更多用法，比如发起 301 和 302 这样的“外部跳转”。

从上面这个例子我们看到，Nginx 变量值容器的生命期是与当前正在处理的请求绑定的，而与 location 无关。

前面我们接触到的都是通过 set 指令隐式创建的 Nginx 变量。这些变量我们一般称为“用户自定义变量”，或者更简单一些，“用户变量”。既然有“用户自定义变量”，自然也就有由 Nginx 核心和各个 Nginx 模块提供的“预定义变量”，或者说“内建变量”（builtin variables）。

Nginx 内建变量最常见的用途就是获取关于请求或响应的各种信息。例如由 ngx_http_core 模块提供的内建变量 $uri，可以用来获取当前请求的 URI（经过解码，并且不含请求参数），而 $request_uri 则用来获取请求最原始的 URI （未经解码，并且包含请求参数）。请看下面这个例子：
location /test {
    echo "uri = $uri";
    echo "request_uri = $request_uri";
}

这里为了简单起见，连 server 配置块也省略了，和前面所有示例一样，我们监听的依然是 8080 端口。在这个例子里，我们把 $uri 和 $request_uri 的值输出到响应体中去。下面我们用不同的请求来测试一下这个 /test 接口：
$ curl 'http://localhost:8080/test'
uri = /test
request_uri = /test

$ curl 'http://localhost:8080/test?a=3&b=4'
uri = /test
request_uri = /test?a=3&b=4

$ curl 'http://localhost:8080/test/hello%20world?a=3&b=4'
uri = /test/hello world
request_uri = /test/hello%20world?a=3&b=4

另一个特别常用的内建变量其实并不是单独一个变量，而是有无限多变种的一群变量，即名字以 arg_ 开头的所有变量，我们估且称之为 $arg_XXX 变量群。一个例子是 $arg_name，这个变量的值是当前请求名为 name 的 URI 参数的值，而且还是未解码的原始形式的值。我们来看一个比较完整的示例：
location /test {
    echo "name: $arg_name";
    echo "class: $arg_class";
}

然后在命令行上使用各种参数组合去请求这个 /test 接口：
$ curl 'http://localhost:8080/test'
name:
class:

$ curl 'http://localhost:8080/test?name=Tom&class=3'
name: Tom
class: 3

$ curl 'http://localhost:8080/test?name=hello%20world&class=9'
name: hello%20world
class: 9

其实 $arg_name 不仅可以匹配 name 参数，也可以匹配 NAME 参数，抑或是 Name，等等：
$ curl 'http://localhost:8080/test?NAME=Marry'
name: Marry
class:

$ curl 'http://localhost:8080/test?Name=Jimmy'
name: Jimmy
class:

Nginx 会在匹配参数名之前，自动把原始请求中的参数名调整为全部小写的形式。

如果你想对 URI 参数值中的 %XX 这样的编码序列进行解码，可以使用第三方 ngx_set_misc 模块提供的 set_unescape_uri 配置指令：
location /test {
    set_unescape_uri $name $arg_name;
    set_unescape_uri $class $arg_class;
    echo "name: $name";
    echo "class: $class";
}

现在我们再看一下效果：
$ curl 'http://localhost:8080/test?name=hello%20world&class=9'
name: hello world
class: 9

空格果然被解码出来了！

从这个例子我们同时可以看到，这个 set_unescape_uri 指令也像 set 指令那样，拥有自动创建 Nginx 变量的功能。后面我们还会专门介绍到 ngx_set_misc 模块。

像 $arg_XXX 这种类型的变量拥有无穷无尽种可能的名字，所以它们并不对应任何存放值的容器。而且这种变量在 Nginx 核心中是经过特别处理的，第三方 Nginx 模块是不能提供这样充满魔法的内建变量的。

类似 $arg_XXX 的内建变量还有不少，比如用来取 cookie 值的 $cookie_XXX 变量群，用来取请求头的 $http_XXX 变量群，以及用来取响应头的 $sent_http_XXX 变量群。这里就不一一介绍了，感兴趣的读者可以参考 ngx_http_core 模块的官方文档。

需要指出的是，许多内建变量都是只读的，比如我们刚才介绍的 $uri 和 $request_uri. 对只读变量进行赋值是应当绝对避免的，因为会有意想不到的后果，比如：
$ curl 'http://localhost:8080/test?name=hello%20world&class=9'
name: hello world
class: 9

这个有问题的配置会让 Nginx 在启动的时候报出一条令人匪夷所思的错误：
[emerg] the duplicate "uri" variable in ...

如果你尝试改写另外一些只读的内建变量，比如 $arg_XXX 变量，在某些 Nginx 的版本中甚至可能导致进程崩溃。


nginx变量使用方法详解(3)
也有一些内建变量是支持改写的，其中一个例子是 $args. 这个变量在读取时返回当前请求的 URL 参数串（即请求 URL 中问号后面的部分，如果有的话 ），而在赋值时可以直接修改参数串。我们来看一个例子：
location /test {
    set $orig_args $args;
    set $args "a=3&b=4";
    echo "original args: $orig_args";
    echo "args: $args";
}

这里我们把原始的 URL 参数串先保存在 $orig_args 变量中，然后通过改写 $args 变量来修改当前的 URL 参数串，最后我们用 echo 指令分别输出 $orig_args 和 $args 变量的值。接下来我们这样来测试这个 /test 接口：
$ curl 'http://localhost:8080/test'
original args:
args: a=3&b=4

$ curl 'http://localhost:8080/test?a=0&b=1&c=2'
original args: a=0&b=1&c=2
args: a=3&b=4

在第一次测试中，我们没有设置任何 URL 参数串，所以输出 $orig_args 变量的值时便得到空。而在第一次和第二次测试中，无论我们是否提供 URL 参数串，参数串都会在 location /test 中被强行改写成 a=3&b=4.

需要特别指出的是，这里的 $args 变量和 $arg_XXX 一样，也不再使用属于自己的存放值的容器。当我们读取 $args 时，Nginx 会执行一小段代码，从 Nginx 核心中专门存放当前 URL 参数串的位置去读取数据；而当我们改写 $args 时，Nginx 会执行另一小段代码，对相同位置进行改写。Nginx 的其他部分在需要当前 URL 参数串的时候，都会从那个位置去读数据，所以我们对 $args 的修改会影响到所有部分的功能。我们来看一个例子：
location /test {
    set $orig_a $arg_a;
    set $args "a=5";
    echo "original a: $orig_a";
    echo "a: $arg_a";
}

这里我们先把内建变量 $arg_a 的值，即原始请求的 URL 参数 a 的值，保存在用户变量 $orig_a 中，然后通过对内建变量 $args 进行赋值，把当前请求的参数串改写为 a=5 ，最后再用 echo 指令分别输出 $orig_a 和 $arg_a 变量的值。因为对内建变量 $args 的修改会直接导致当前请求的 URL 参数串发生变化，因此内建变量 $arg_XXX 自然也会随之变化。测试的结果证实了这一点：
$ curl 'http://localhost:8080/test?a=3'
original a: 3
a: 5

我们看到，因为原始请求的 URL 参数串是 a=3, 所以 $arg_a 最初的值为 3, 但随后通过改写 $args 变量，将 URL 参数串又强行修改为 a=5, 所以最终 $arg_a 的值又自动变为了 5.

我们再来看一个通过修改 $args 变量影响标准的 HTTP 代理模块 ngx_proxy 的例子：
server {
    listen 8080;

    location /test {
        set $args "foo=1&bar=2";
        proxy_pass http://127.0.0.1:8081/args;
    }
}

server {

    listen 8081;
    location /args {
        echo "args: $args";
    }
}

这里我们在 http 配置块中定义了两个虚拟主机。第一个虚拟主机监听 8080 端口，其 /test 接口自己通过改写 $args 变量，将当前请求的 URL 参数串无条件地修改为 foo=1&bar=2. 然后 /test 接口再通过 ngx_proxy 模块的 proxy_pass 指令配置了一个反向代理，指向本机的 8081 端口上的 HTTP 服务 /args. 默认情况下，ngx_proxy 模块在转发 HTTP 请求到远方 HTTP 服务的时候，会自动把当前请求的 URL 参数串也转发到远方。

而本机的 8081 端口上的 HTTP 服务正是由我们定义的第二个虚拟主机来提供的。我们在第二个虚拟主机的 location /args 中利用 echo 指令输出当前请求的 URL 参数串，以检查 /test 接口通过 ngx_proxy 模块实际转发过来的 URL 请求参数串。

我们来实际访问一下第一个虚拟主机的 /test 接口：
$ curl 'http://localhost:8080/test?blah=7'
args: foo=1&bar=2

我们看到，虽然请求自己提供了 URL 参数串 blah=7，但在 location /test 中，参数串被强行改写成了 foo=1&bar=2. 接着经由 proxy_pass 指令将我们被改写掉的参数串转发给了第二个虚拟主机上配置的 /args 接口，然后再把 /args 接口的 URL 参数串输出。事实证明，我们对 $args 变量的赋值操作，也成功影响到了 ngx_proxy 模块的行为。

在读取变量时执行的这段特殊代码，在 Nginx 中被称为“取处理程序”（get handler）；而改写变量时执行的这段特殊代码，则被称为“存处理程序”（set handler）。不同的 Nginx 模块一般会为它们的变量准备不同的“存取处理程序”，从而让这些变量的行为充满魔法。

其实这种技巧在计算世界并不鲜见。比如在面向对象编程中，类的设计者一般不会把类的成员变量直接暴露给类的用户，而是另行提供两个方法（method），分别用于该成员变量的读操作和写操作，这两个方法常常被称为“存取器”（accessor）。下面是 C++ 语言中的一个例子：
#include <string>
using namespace std;
class Person {
public:
    const string get_name() {
        return m_name;
    }

    void set_name(const string name) {
        m_name = name;
    }

private:
    string m_name;
};

在这个名叫 Person 的 C++ 类中，我们提供了 get_name 和 set_name 这两个公共方法，以作为私有成员变量 m_name 的“存取器”。

这样设计的好处是显而易见的。类的设计者可以在“存取器”中执行任意代码，以实现所需的业务逻辑以及“副作用”，比如自动更新与当前成员变量存在依赖关系的其他成员变量，抑或是直接修改某个与当前对象相关联的数据库表中的对应字段。而对于后一种情况，也许“存取器”所对应的成员变量压根就不存在，或者即使存在，也顶多扮演着数据缓存的角色，以缓解被代理数据库的访问压力。

与面向对象编程中的“存取器”概念相对应，Nginx 变量也是支持绑定“存取处理程序”的。Nginx 模块在创建变量时，可以选择是否为变量分配存放值的容器，以及是否自己提供与读写操作相对应的“存取处理程序”。

不是所有的 Nginx 变量都拥有存放值的容器。拥有值容器的变量在 Nginx 核心中被称为“被索引的”（indexed）；反之，则被称为“未索引的”（non-indexed）。

我们前面在 （二） 中已经知道，像 $arg_XXX 这样具有无数变种的变量群，是“未索引的”。当读取这样的变量时，其实是它的“取处理程序”在起作用，即实时扫描当前请求的 URL 参数串，提取出变量名所指定的 URL 参数的值。很多新手都会对 $arg_XXX 的实现方式产生误解，以为 Nginx 会事先解析好当前请求的所有 URL 参数，并且把相关的 $arg_XXX 变量的值都事先设置好。然而事实并非如此，Nginx 根本不会事先就解析好 URL 参数串，而是在用户读取某个 $arg_XXX 变量时，调用其“取处理程序”，即时去扫描 URL 参数串。类似地，内建变量 $cookie_XXX 也是通过它的“取处理程序”，即时去扫描 Cookie 请求头中的相关定义的。

想了解请看nginx变量使用方法详解2，下一篇nginx变量使用方法详解4



nginx变量使用方法详解(4)

在设置了“取处理程序”的情况下，Nginx 变量也可以选择将其值容器用作缓存，这样在多次读取变量的时候，就只需要调用“取处理程序”计算一次。我们下面就来看一个这样的例子：

    map $args $foo {
        default     0;
        debug       1;
    }

    server {
        listen 8080;

        location /test {
            set $orig_foo $foo;
            set $args debug;
            echo "orginal foo: $orig_foo";
            echo "foo: $foo";
        }
    }

这里首次用到了标准 ngx_map 模块的 map 配置指令，我们有必要在此介绍一下。map 在英文中除了“地图”之外，也有“映射”的意思。比方说，中学数学里讲的“函数”就是一种“映射”。而 Nginx 的这个 map 指令就可以用于定义两个 Nginx 变量之间的映射关系，或者说是函数关系。回到上面这个例子，我们用 map 指令定义了用户变量 $foo 与 $args 内建变量之间的映射关系。特别地，用数学上的函数记法 y = f(x) 来说，我们的 $args 就是“自变量” x，而 $foo 则是“因变量” y，即 $foo 的值是由 $args 的值来决定的，或者按照书写顺序可以说，我们将 $args 变量的值映射到了 $foo 变量上。

现在我们再来看 map 指令定义的映射规则：

    map $args $foo {
        default     0;
        debug       1;
    }

花括号中第一行的 default 是一个特殊的匹配条件，即当其他条件都不匹配的时候，这个条件才匹配。当这个默认条件匹配时，就把“因变量” $foo 映射到值 0. 而花括号中第二行的意思是说，如果“自变量” $args 精确匹配了 debug 这个字符串，则把“因变量” $foo 映射到值 1. 将这两行合起来，我们就得到如下完整的映射规则：当 $args 的值等于 debug 的时候，$foo 变量的值就是 1，否则 $foo 的值就为 0.

明白了 map 指令的含义，再来看 location /test. 在那里，我们先把当前 $foo 变量的值保存在另一个用户变量 $orig_foo 中，然后再强行把 $args 的值改写为 debug，最后我们再用 echo 指令分别输出 $orig_foo 和 $foo 的值。

从逻辑上看，似乎当我们强行改写 $args 的值为 debug 之后，根据先前的 map 映射规则，$foo 变量此时的值应当自动调整为字符串 1, 而不论 $foo 原先的值是怎样的。然而测试结果并非如此：

    $ curl 'http://localhost:8080/test'
    original foo: 0
    foo: 0

第一行输出指示 $orig_foo 的值为 0，这正是我们期望的：上面这个请求并没有提供 URL 参数串，于是 $args 最初的取值就是空，再根据我们先前定义的映射规则，$foo 变量在第一次被读取时的值就应当是 0（即匹配默认的那个 default 条件）。

而第二行输出显示，在强行改写 $args 变量的值为字符串 debug 之后，$foo 的条件仍然是 0 ，这显然不符合映射规则，因为当 $args 为 debug 时，$foo 的值应当是 1. 这究竟是为什么呢？

其实原因很简单，那就是 $foo 变量在第一次读取时，根据映射规则计算出的值被缓存住了。刚才我们说过，Nginx 模块可以为其创建的变量选择使用值容器，作为其“取处理程序”计算结果的缓存。显然，ngx_map 模块认为变量间的映射计算足够昂贵，需要自动将因变量的计算结果缓存下来，这样在当前请求的处理过程中如果再次读取这个因变量，Nginx 就可以直接返回缓存住的结果，而不再调用该变量的“取处理程序”再行计算了。

为了进一步验证这一点，我们不妨在请求中直接指定 URL 参数串为 debug:

    $ curl 'http://localhost:8080/test?debug'
    original foo: 1
    foo: 1

我们看到，现在 $orig_foo 的值就成了 1，因为变量 $foo 在第一次被读取时，自变量 $args 的值就是 debug，于是按照映射规则，“取处理程序”计算返回的值便是 1. 而后续再读取 $foo 的值时，就总是得到被缓存住的 1 这个结果，而不论 $args 后来变成什么样了。

map 指令其实是一个比较特殊的例子，因为它可以为用户变量注册“取处理程序”，而且用户可以自己定义这个“取处理程序”的计算规则。当然，此规则在这里被限定为与另一个变量的映射关系。同时，也并非所有使用了“取处理程序”的变量都会缓存结果，例如我们前面在 （三） 中已经看到 $arg_XXX 并不会使用值容器进行缓存。

类似 ngx_map 模块，标准的 ngx_geo 等模块也一样使用了变量值的缓存机制。

在上面的例子中，我们还应当注意到 map 指令是在 server 配置块之外，也就是在最外围的 http 配置块中定义的。很多读者可能会对此感到奇怪，毕竟我们只是在 location /test 中用到了它。这倒不是因为我们不想把 map 语句直接挪到 location 配置块中，而是因为 map 指令只能在 http 块中使用！

很多 Nginx 新手都会担心如此“全局”范围的 map 设置会让访问所有虚拟主机的所有 location 接口的请求都执行一遍变量值的映射计算，然而事实并非如此。前面我们已经了解到 map 配置指令的工作原理是为用户变量注册 “取处理程序”，并且实际的映射计算是在“取处理程序”中完成的，而“取处理程序”只有在该用户变量被实际读取时才会执行（当然，因为缓存的存在，只在请求生命期中的第一次读取中才被执行），所以对于那些根本没有用到相关变量的请求来说，就根本不会执行任何的无用计算。

这种只在实际使用对象时才计算对象值的技术，在计算领域被称为“惰性求值”（lazy evaluation）。提供“惰性求值” 语义的编程语言并不多见，最经典的例子便是 Haskell. 与之相对的便是“主动求值” （eager evaluation）。我们有幸在 Nginx 中也看到了“惰性求值”的例子，但“主动求值”语义其实在 Nginx 里面更为常见，例如下面这行再普通不过的 set 语句：

    set $b "$a,$a";

这里会在执行 set 规定的赋值操作时，“主动”地计算出变量 $b 的值，而不会将该求值计算延缓到变量 $b 实际被读取的时候。

nginx变量使用方法详解(5)

前面在 （二） 中我们已经了解到变量值容器的生命期是与请求绑定的，但是我当时有意避开了“请求”的正式定义。大家应当一直默认这里的“请求”都是指客户端发起的 HTTP 请求。其实在 Nginx 世界里有两种类型的“请求”，一种叫做“主请求”（main request），而另一种则叫做“子请求”（subrequest）。我们先来介绍一下它们。

所谓“主请求”，就是由 HTTP 客户端从 Nginx 外部发起的请求。我们前面见到的所有例子都只涉及到“主请求”，包括 （二） 中那两个使用 echo_exec 和 rewrite 指令发起“内部跳转”的例子。

而“子请求”则是由 Nginx 正在处理的请求在 Nginx 内部发起的一种级联请求。“子请求”在外观上很像 HTTP 请求，但实现上却和 HTTP 协议乃至网络通信一点儿关系都没有。它是 Nginx 内部的一种抽象调用，目的是为了方便用户把“主请求”的任务分解为多个较小粒度的“内部请求”，并发或串行地访问多个 location 接口，然后由这些 location 接口通力协作，共同完成整个“主请求”。当然，“子请求”的概念是相对的，任何一个“子请求”也可以再发起更多的“子子请求”，甚至可以玩递归调用（即自己调用自己）。当一个请求发起一个“子请求”的时候，按照 Nginx 的术语，习惯把前者称为后者的“父请求”（parent request）。值得一提的是，Apache 服务器中其实也有“子请求”的概念，所以来自 Apache 世界的读者对此应当不会感到陌生。

下面就来看一个使用了“子请求”的例子：

    location /main {
        echo_location /foo;
        echo_location /bar;
    }

    location /foo {
        echo foo;
    }

    location /bar {
        echo bar;
    }

这里在 location /main 中，通过第三方 ngx_echo 模块的 echo_location 指令分别发起到 /foo 和 /bar 这两个接口的 GET 类型的“子请求”。由 echo_location 发起的“子请求”，其执行是按照配置书写的顺序串行处理的，即只有当 /foo 请求处理完毕之后，才会接着处理 /bar 请求。这两个“子请求”的输出会按执行顺序拼接起来，作为 /main 接口的最终输出：

    $ curl 'http://localhost:8080/main'
    foo
    bar

我们看到，“子请求”方式的通信是在同一个虚拟主机内部进行的，所以 Nginx 核心在实现“子请求”的时候，就只调用了若干个 C 函数，完全不涉及任何网络或者 UNIX 套接字（socket）通信。我们由此可以看出“子请求”的执行效率是极高的。

回到先前对 Nginx 变量值容器的生命期的讨论，我们现在依旧可以说，它们的生命期是与当前请求相关联的。每个请求都有所有变量值容器的独立副本，只不过当前请求既可以是“主请求”，也可以是“子请求”。即便是父子请求之间，同名变量一般也不会相互干扰。让我们来通过一个小实验证明一下这个说法：

    location /main {
        set $var main;
        echo_location /foo;
        echo_location /bar;
        echo "main: $var";
    }

    location /foo {
        set $var foo;
        echo "foo: $var";
    }

    location /bar {
        set $var bar;
        echo "bar: $var";
    }

在这个例子中，我们分别在 /main，/foo 和 /bar 这三个 location 配置块中为同一名字的变量，$var，分别设置了不同的值并予以输出。特别地，我们在 /main 接口中，故意在调用过 /foo 和 /bar 这两个“子请求”之后，再输出它自己的 $var 变量的值。请求 /main 接口的结果是这样的：

    $ curl 'http://localhost:8080/main'
    foo: foo
    bar: bar
    main: main

显然，/foo 和 /bar 这两个“子请求”在处理过程中对变量 $var 各自所做的修改都丝毫没有影响到“主请求” /main. 于是这成功印证了“主请求”以及各个“子请求”都拥有不同的变量 $var 的值容器副本。

不幸的是，一些 Nginx 模块发起的“子请求”却会自动共享其“父请求”的变量值容器，比如第三方模块 ngx_auth_request. 下面是一个例子：

    location /main {
        set $var main;
        auth_request /sub;
        echo "main: $var";
    }

    location /sub {
        set $var sub;
        echo "sub: $var";
    }

这里我们在 /main 接口中先为 $var 变量赋初值 main，然后使用 ngx_auth_request 模块提供的配置指令 auth_request，发起一个到 /sub 接口的“子请求”，最后利用 echo 指令输出变量 $var 的值。而我们在 /sub 接口中则故意把 $var 变量的值改写成 sub. 访问 /main 接口的结果如下：

    $ curl 'http://localhost:8080/main'
    main: sub

我们看到，/sub 接口对 $var 变量值的修改影响到了主请求 /main. 所以 ngx_auth_request 模块发起的“子请求”确实是与其“父请求”共享一套 Nginx 变量的值容器。

对于上面这个例子，相信有读者会问：“为什么‘子请求’ /sub 的输出没有出现在最终的输出里呢？”答案很简单，那就是因为 auth_request 指令会自动忽略“子请求”的响应体，而只检查“子请求”的响应状态码。当状态码是 2XX 的时候，auth_request 指令会忽略“子请求”而让 Nginx 继续处理当前的请求，否则它就会立即中断当前（主）请求的执行，返回相应的出错页。在我们的例子中，/sub “子请求”只是使用 echo 指令作了一些输出，所以隐式地返回了指示正常的 200 状态码。

如 ngx_auth_request 模块这样父子请求共享一套 Nginx 变量的行为，虽然可以让父子请求之间的数据双向传递变得极为容易，但是对于足够复杂的配置，却也经常导致不少难于调试的诡异 bug. 因为用户时常不知道“父请求”的某个 Nginx 变量的值，其实已经在它的某个“子请求”中被意外修改了。诸如此类的因共享而导致的不好的“副作用”，让包括 ngx_echo，ngx_lua，以及 ngx_srcache 在内的许多第三方模块都选择了禁用父子请求间的变量共享。



nginx变量使用方法详解(6)

Nginx 内建变量用在“子请求”的上下文中时，其行为也会变得有些微妙。

前面在 （三） 中我们已经知道，许多内建变量都不是简单的“存放值的容器”，它们一般会通过注册“存取处理程序”来表现得与众不同，而它们即使有存放值的容器，也只是用于缓存“存取处理程序”的计算结果。我们之前讨论过的 $args 变量正是通过它的“取处理程序”来返回当前请求的 URL 参数串。因为当前请求也可以是“子请求”，所以在“子请求”中读取 $args，其“取处理程序”会很自然地返回当前“子请求”的参数串。我们来看这样的一个例子：
location /main {
    echo "main args: $args";
    echo_location /sub "a=1&b=2";
}

location /sub {
    echo "sub args: $args";
}

这里在 /main 接口中，先用 echo 指令输出当前请求的 $args 变量的值，接着再用 echo_location 指令发起子请求 /sub. 这里值得注意的是，我们在 echo_location 语句中除了通过第一个参数指定“子请求”的 URI 之外，还提供了第二个参数，用以指定该“子请求”的 URL 参数串（即 a=1&b=2）。最后我们定义了 /sub 接口，在里面输出了一下 $args 的值。请求 /main 接口的结果如下：

$ curl ‘http://localhost:8080/main?c=3′
main args: c=3
sub args: a=1&b=2

显然，当 $args 用在“主请求” /main 中时，输出的就是“主请求”的 URL 参数串，c=3；而当用在“子请求” /sub 中时，输出的则是“子请求”的参数串，a=1&b=2。这种行为正符合我们的直觉。

与 $args 类似，内建变量 $uri 用在“子请求”中时，其“取处理程序”也会正确返回当前“子请求”解析过的 URI:
location /main {
    echo "main uri: $uri";
    echo_location /sub;
}

location /sub {
    echo "sub uri: $uri";
}

请求 /main 的结果是
$ curl 'http://localhost:8080/main'
main uri: /main
sub uri: /sub

这依然是我们所期望的。

但不幸的是，并非所有的内建变量都作用于当前请求。少数内建变量只作用于“主请求”，比如由标准模块 ngx_http_core 提供的内建变量 $request_method.

变量 $request_method 在读取时，总是会得到“主请求”的请求方法，比如 GET、POST 之类。我们来测试一下：
location /main {
    echo "main method: $request_method";
    echo_location /sub;
}

location /sub {
    echo "sub method: $request_method";
}

在这个例子里，/main 和 /sub 接口都会分别输出 $request_method 的值。同时，我们在 /main 接口里利用 echo_location 指令发起一个到 /sub 接口的 GET “子请求”。我们现在利用 curl 命令行工具来发起一个到 /main 接口的 POST 请求：
$ curl --data hello 'http://localhost:8080/main'
main method: POST
sub method: POST

这里我们利用 curl 程序的 –data 选项，指定 hello 作为我们的请求体数据，同时 –data 选项会自动让发送的请求使用 POST 请求方法。测试结果证明了我们先前的预言，$request_method 变量即使在 GET “子请求” /sub 中使用，得到的值依然是“主请求” /main 的请求方法，POST.

有的读者可能觉得我们在这里下的结论有些草率，因为上例是先在“主请求”里读取（并输出）$request_method 变量，然后才发“子请求”的，所以这些读者可能认为这并不能排除 $request_method 在进入子请求之前就已经把第一次读到的值给缓存住，从而影响到后续子请求中的输出结果。不过，这样的顾虑是多余的，因为我们前面在 （五） 中也特别提到过，缓存所依赖的变量的值容器，是与当前请求绑定的，而由 ngx_echo 模块发起的“子请求”都禁用了父子请求之间的变量共享，所以在上例中，$request_method 内建变量即使真的使用了值容器作为缓存（事实上它也没有），它也不可能影响到 /sub 子请求。

为了进一步消除这部分读者的疑虑，我们不妨稍微修改一下刚才那个例子，将 /main 接口输出 $request_method 变量的时间推迟到“子请求”执行完毕之后：
location /main {
    echo_location /sub;
    echo "main method: $request_method";
}

location /sub {
    echo "sub method: $request_method";
}

让我们重新测试一下：
$ curl --data hello 'http://localhost:8080/main'
sub method: POST
main method: POST

可以看到，再次以 POST 方法请求 /main 接口的结果与原先那个例子完全一致，除了父子请求的输出顺序颠倒了过来（因为我们在本例中交换了 /main 接口中那两条输出配置指令的先后次序）。

由此可见，我们并不能通过标准的 $request_method 变量取得“子请求”的请求方法。为了达到我们最初的目的，我们需要求助于第三方模块 ngx_echo 提供的内建变量 $echo_request_method：
location /main {
    echo "main method: $echo_request_method";
    echo_location /sub;
}

location /sub {
    echo "sub method: $echo_request_method";
}

此时的输出终于是我们想要的了：
$ curl --data hello 'http://localhost:8080/main'
main method: POST
sub method: GET

我们看到，父子请求分别输出了它们各自不同的请求方法，POST 和 GET.

类似 $request_method，内建变量 $request_uri 一般也返回的是“主请求”未经解析过的 URL，毕竟“子请求”都是在 Nginx 内部发起的，并不存在所谓的“未解析的”原始形式。

如果真如前面那部分读者所担心的，内建变量的值缓存在共享变量的父子请求之间起了作用，这无疑是灾难性的。我们前面在 （五） 中已经看到 ngx_auth_request 模块发起的“子请求”是与其“父请求”共享一套变量的。下面是一个这样的可怕例子：
map $uri $tag {
    default     0;
    /main       1;
    /sub        2;
}

server {
    listen 8080;

    location /main {
        auth_request /sub;
        echo "main tag: $tag";
    }

    location /sub {
        echo "sub tag: $tag";
    }
}

这里我们使用久违了的 map 指令来把内建变量 $uri 的值映射到用户变量 $tag 上。当 $uri 的值为 /main 时，则赋予 $tag 值 1，当 $uri 取值 /sub 时，则赋予 $tag 值 2，其他情况都赋 0. 接着，我们在 /main 接口中先用 ngx_auth_request 模块的 auth_request 指令发起到 /sub 接口的子请求，然后再输出变量 $tag 的值。而在 /sub 接口中，我们直接输出变量 $tag. 猜猜看，如果我们访问接口 /main，将会得到什么样的输出呢？
$ curl 'http://localhost:8080/main'
main tag: 2

咦？我们不是分明把 /main 这个值映射到 1 上的么？为什么实际输出的是 /sub 映射的结果 2 呢？

其实道理很简单，因为我们的 $tag 变量在“子请求” /sub 中首先被读取，于是在那里计算出了值 2（因为 $uri 在那里取值 /sub，而根据 map 映射规则，$tag 应当取值 2），从此就被 $tag 的值容器给缓存住了。而 auth_request 发起的“子请求”又是与“父请求”共享一套变量的，于是当 Nginx 的执行流回到“父请求”输出 $tag 变量的值时，Nginx 就直接返回缓存住的结果 2 了。这样的结果确实太意外了。

从这个例子我们再次看到，父子请求间的变量共享，实在不是一个好主意。

nginx变量使用方法详解(7)
在 （一） 中我们提到过，Nginx 变量的值只有一种类型，那就是字符串，但是变量也有可能压根就不存在有意义的值。没有值的变量也有两种特殊的值：一种是“不合法”（invalid），另一种是“没找到”（not found）。

举例说来，当 Nginx 用户变量 $foo 创建了却未被赋值时，$foo 的值便是“不合法”；而如果当前请求的 URL 参数串中并没有提及 XXX 这个参数，则 $arg_XXX 内建变量的值便是“没找到”。

无论是“不合法”也好，还是“没找到”也罢，这两种 Nginx 变量所拥有的特殊值，和空字符串（””）这种取值是完全不同的，比如 JavaScript 语言中也有专门的 undefined 和 null 这两种特殊值，而 Lua 语言中也有专门的 nil 值: 它们既不等同于空字符串，也不等同于数字 0，更不是布尔值 false. 其实 SQL 语言中的 NULL 也是类似的一种东西。

虽然前面在 （一） 中我们看到，由 set 指令创建的变量未初始化就用在“变量插值”中时，效果等同于空字符串，但那是因为 set 指令为它创建的变量自动注册了一个“取处理程序”，将“不合法”的变量值转换为空字符串。为了验证这一点，我们再重新看一下 （一） 中讨论过的那个例子：
location /foo {
    echo "foo = [$foo]";
}

location /bar {
    set $foo 32;
    echo "foo = [$foo]";
}

这里为了简单起见，省略了原先写出的外围 server 配置块。在这个例子里，我们在 /bar 接口中用 set 指令隐式地创建了 $foo 变量这个名字，然后我们在 /foo 接口中不对 $foo 进行初始化就直接使用 echo 指令输出。我们当时测试 /foo 接口的结果是
$ curl 'http://localhost:8080/foo'
foo = []

从输出上看，未初始化的 $foo 变量确实和空字符串的效果等同。但细心的读者当时应该就已经注意到，对于上面这个请求，Nginx 的错误日志文件（一般文件名叫做 error.log）中多出一行类似下面这样的警告：
[warn] 5765
#0: *1 using uninitialized "foo" variable, ...

这一行警告是谁输出的呢？答案是 set 指令为 $foo 注册的“取处理程序”。当 /foo 接口中的 echo 指令实际执行的时候，它会对它的参数 “foo = [$foo]” 进行“变量插值”计算。于是，参数串中的 $foo 变量会被读取，而 Nginx 会首先检查其值容器里的取值，结果它看到了“不合法”这个特殊值，于是它这才决定继续调用 $foo 变量的“取处理程序”。于是 $foo 变量的“取处理程序”开始运行，它向 Nginx 的错误日志打印出上面那条警告消息，然后返回一个空字符串作为 $foo 的值，并从此缓存在 $foo 的值容器中。

细心的读者会注意到刚刚描述的这个过程其实就是那些支持值缓存的内建变量的工作原理，只不过 set 指令在这里借用了这套机制来处理未正确初始化的 Nginx 变量。值得一提的是，只有“不合法”这个特殊值才会触发 Nginx 调用变量的“取处理程序”，而特殊值“没找到”却不会。

上面这样的警告一般会指示出我们的 Nginx 配置中存在变量名拼写错误，抑或是在错误的场合使用了尚未初始化的变量。因为值缓存的存在，这条警告在一个请求的生命期中也不会打印多次。当然，ngx_rewrite 模块专门提供了一条 uninitialized_variable_warn 配置指令可用于禁止这条警告日志。

刚才提到，内建变量 $arg_XXX 在请求 URL 参数 XXX 并不存在时会返回特殊值“找不到”，但遗憾的是在 Nginx 原生配置语言（我们估且这么称呼它）中是不能很方便地把它和空字符串区分开来的，比如：
location /test {
    echo "name: [$arg_name]";
}

这里我们输出 $arg_name 变量的值同时故意在请求中不提供 URL 参数 name:
$ curl 'http://localhost:8080/test'
name: []

我们看到，输出特殊值“找不到”的效果和空字符串是相同的。因为这一回是 Nginx 的“变量插值”引擎自动把“找不到”给忽略了。

那么我们究竟应当如何捕捉到“找不到”这种特殊值的踪影呢？换句话说，我们应当如何把它和空字符串给区分开来呢？显然，下面这个请求中，URL 参数 name 是有值的，而且其值应当是空字符串：
$ curl 'http://localhost:8080/test?name='
name: []

但我们却无法将之和前面完全不提供 name 参数的情况给区分开。

幸运的是，通过第三方模块 ngx_lua，我们可以轻松地在 Lua 代码中做到这一点。请看下面这个例子：
location /test {
    content_by_lua '
        if ngx.var.arg_name == nil then
            ngx.say("name: missing")
        else
            ngx.say("name: [", ngx.var.arg_name, "]")
        end
    ';
}

这个例子和前一个例子功能上非常接近，除了我们在 /test 接口中使用了 ngx_lua 模块的 content_by_lua 配置指令，嵌入了一小段我们自己的 Lua 代码来对 Nginx 变量 $arg_name 的特殊值进行判断。在这个例子中，当 $arg_name 的值为“没找到”（或者“不合法”）时，/foo 接口会输出 name: missing 这一行结果:
curl 'http://localhost:8080/test'
name: missing

因为这是我们第一次接触到 ngx_lua 模块，所以需要先简单介绍一下。ngx_lua 模块将 Lua 语言解释器（或者 LuaJIT 即时编译器）嵌入到了 Nginx 核心中，从而可以让用户在 Nginx 核心中直接运行 Lua 语言编写的程序。我们可以选择在 Nginx 不同的请求处理阶段插入我们的 Lua 代码。这些 Lua 代码既可以直接内联在 Nginx 配置文件中，也可以单独放置在外部 .lua 文件里，然后在 Nginx 配置文件中引用 .lua 文件的路径。

回到上面这个例子，我们在 Lua 代码里引用 Nginx 变量都是通过 ngx.var 这个由 ngx_lua 模块提供的 Lua 接口。比如引用 Nginx 变量 $VARIABLE 时，就在 Lua 代码里写作 ngx.var.VARIABLE 就可以了。当 Nginx 变量 $arg_name 为特殊值“没找到”（或者“不合法”）时， ngx.var.arg_name 在 Lua 世界中的值就是 nil，即 Lua 语言里的“空”（不同于 Lua 空字符串）。我们在 Lua 里输出响应体内容的时候，则使用了 ngx.say 这个 Lua 函数，也是 ngx_lua 模块提供的，功能上等价于 ngx_echo 模块的 echo 配置指令。

现在，如果我们提供空字符串取值的 name 参数，则输出就和刚才不相同了：
$ curl 'http://localhost:8080/test?name='
name: []

在这种情况下，Nginx 变量 $arg_name 的取值便是空字符串，这既不是“没找到”，也不是“不合法”，因此在 Lua 里，ngx.var.arg_name 就返回 Lua 空字符串（””），和刚才的 Lua nil 值就完全区分开了。

这种区分在有些应用场景下非常重要，比如有的 web service 接口会根据 name 这个 URL 参数是否存在来决定是否按 name 属性对数据集合进行过滤，而显然提供空字符串作为 name 参数的值，也会导致对数据集中取值为空串的记录进行筛选操作。

不过，标准的 $arg_XXX 变量还是有一些局限，比如我们用下面这个请求来测试刚才那个 /test 接口：
$ curl 'http://localhost:8080/test?name'
name: missing

此时，$arg_name 变量仍然读出“找不到”这个特殊值，这就明显有些违反常识。此外，$arg_XXX 变量在请求 URL 中有多个同名 XXX 参数时，就只会返回最先出现的那个 XXX 参数的值，而默默忽略掉其他实例：
$ curl 'http://localhost:8080/test?name=Tom&name=Jim&name=Bob'
name: [Tom]

要解决这些局限，可以直接在 Lua 代码中使用 ngx_lua 模块提供的 ngx.req.get_uri_args 函数。

nginx变量使用方法详解(8)
与 $arg_XXX 类似，我们在 （二） 中提到过的内建变量 $cookie_XXX 变量也会在名为 XXX 的 cookie 不存在时返回特殊值“没找到”：

    location /test {
        content_by_lua '
            if ngx.var.cookie_user == nil then
                ngx.say("cookie user: missing")
            else
                ngx.say("cookie user: [", ngx.var.cookie_user, "]")
            end
        ';
    }

利用 curl 命令行工具的 –cookie name=value 选项可以指定 name=value 为当前请求携带的 cookie（通过添加相应的 Cookie 请求头）。下面是若干次测试结果：

    $ curl --cookie user=agentzh 'http://localhost:8080/test'
    cookie user: [agentzh]

    $ curl --cookie user= 'http://localhost:8080/test'
    cookie user: []

    $ curl 'http://localhost:8080/test'
    cookie user: missing

我们看到，cookie user 不存在以及取值为空字符串这两种情况被很好地区分开了：当 cookie user 不存在时，Lua 代码中的 ngx.var.cookie_user 返回了期望的 Lua nil 值。

在 Lua 里访问未创建的 Nginx 用户变量时，在 Lua 里也会得到 nil 值，而不会像先前的例子那样直接让 Nginx 拒绝加载配置：

    location /test {
        content_by_lua '
           ngx.say("$blah = ", ngx.var.blah)
        ';
    }

这里假设我们并没有在当前的 nginx.conf 配置文件中创建过用户变量 $blah，然后我们在 Lua 代码中通过 ngx.var.blah 直接引用它。上面这个配置可以顺利启动，因为 Nginx 在加载配置时只会编译 content_by_lua 配置指令指定的 Lua 代码而不会实际执行它，所以 Nginx 并不知道 Lua 代码里面引用了 $blah 这个变量。于是我们在运行时也会得到 nil 值。而 ngx_lua 提供的 ngx.say 函数会自动把 Lua 的 nil 值格式化为字符串 “nil” 输出，于是访问 /test 接口的结果是：

    curl 'http://localhost:8080/test'
    $blah = nil

这正是我们所期望的。

上面这个例子中另一个值得注意的地方是，我们在 content_by_lua 配置指令的参数中提及了 $bar 符号，但却并没有触发“变量插值”（否则 Nginx 会在启动时抱怨 $blah 未创建）。这是因为 content_by_lua 配置指令并不支持参数的“变量插值”功能。我们前面在 （一） 中提到过，配置指令的参数是否允许“变量插值”，其实取决于该指令的实现模块。

设计返回“不合法”这一特殊值的例子是困难的，因为我们前面在 （七） 中已经看到，由 set 指令创建的变量在未初始化时确实是“不合法”，但一旦尝试读取它们时，Nginx 就会自动调用其“取处理程序”，而它们的“取处理程序”会自动返回空字符串并将之缓存住。于是我们最终得到的是完全合法的空字符串。下面这个使用了 Lua 代码的例子证明了这一点：

    location /foo {
        content_by_lua '
            if ngx.var.foo == nil then
                ngx.say("$foo is nil")
            else
                ngx.say("$foo = [", ngx.var.foo, "]")
            end
        ';
    }

    location /bar {
        set $foo 32;
        echo "foo = [$foo]";
    }

请求 /foo 接口的结果是：

    $ curl 'http://localhost:8080/foo'
    $foo = []

我们看到在 Lua 里面读取未初始化的 Nginx 变量 $foo 时得到的是空字符串。

最后值得一提的是，虽然前面反复指出 Nginx 变量只有字符串这一种数据类型，但这并不能阻止像 ngx_array_var 这样的第三方模块让 Nginx 变量也能存放数组类型的值。下面就是这样的一个例子：

    location /test {
        array_split "," $arg_names to=$array;
        array_map "[$array_it]" $array;
        array_join " " $array to=$res;
        echo $res;
    }

这个例子中使用了 ngx_array_var 模块的 array_split、 array_map 和 array_join 这三条配置指令，其含义很接近 Perl 语言中的内建函数 split、map 和 join（当然，其他脚本语言也有类似的等价物）。我们来看看访问 /test 接口的结果：

    $ curl 'http://localhost:8080/test?names=Tom,Jim,Bob
    [Tom] [Jim] [Bob]

我们看到，使用 ngx_array_var 模块可以很方便地处理这样具有不定个数的组成元素的输入数据，例如此例中的 names URL 参数值就是由不定个数的逗号分隔的名字所组成。不过，这种类型的复杂任务通过 ngx_lua 来做通常会更灵活而且更容易维护。

至此，本系列教程对 Nginx 变量的介绍终于可以告一段落了。我们在这个过程中接触到了许多标准的和第三方的 Nginx 模块，这些模块让我们得以很轻松地构造出许多有趣的小例子，从而可以深入探究 Nginx 变量的各种行为和特性。在后续的教程中，我们还会有很多机会与这些模块打交道。

通过前面讨论过的众多例子，我们应当已经感受到 Nginx 变量在 Nginx 配置语言中所扮演的重要角色：它是获取 Nginx 中各种信息（包括当前请求的信息）的主要途径和载体，同时也是各个模块之间传递数据的主要媒介之一。在后续的教程中，我们会经常看到 Nginx 变量的身影，所以现在很好地理解它们是非常重要的。

在下一个系列的教程，即 Nginx 配置指令的执行顺序系列 中，我们将深入探讨 Nginx 配置指令的执行顺序以及请求的各个处理阶段，因为很多 Nginx 用户都搞不清楚他们书写的众多配置指令之间究竟是按照何种时间顺序执行的，也搞不懂为什么这些指令实际执行的顺序经常和配置文件里的书写顺序大相径庭。



[link_post name=”nginx%e5%8f%98%e9%87%8f%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95%e8%af%a6%e8%a7%a31″]|[link_post name=”nginx%e5%8f%98%e9%87%8f%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95%e8%af%a6%e8%a7%a32″]|[link_post name=”nginx%e5%8f%98%e9%87%8f%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95%e8%af%a6%e8%a7%a33″]|[link_post name=”nginx%e5%8f%98%e9%87%8f%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95%e8%af%a6%e8%a7%a34″]|[link_post name=”nginx%e5%8f%98%e9%87%8f%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95%e8%af%a6%e8%a7%a35″]|[link_post name=”nginx%e5%8f%98%e9%87%8f%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95%e8%af%a6%e8%a7%a36″]|[link_post name=”nginx%e5%8f%98%e9%87%8f%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95%e8%af%a6%e8%a7%a37″]|[link_post name=”nginx%e5%8f%98%e9%87%8f%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95%e8%af%a6%e8%a7%a38″]
