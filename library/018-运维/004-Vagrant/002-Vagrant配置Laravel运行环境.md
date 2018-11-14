**需要安装的软件:**
```
VirtualBox
Vagrant
```
关于`VirtualBox`平时可能经常遇到,本文加假定你已经安装好了`VirtualBox`,特别注意的一点
需要安装` VirtualBox 5.1`或者更高的版本。


关于`Vagrant`，这才是我们的主角,下载地址:
https://www.vagrantup.com/downloads.html  
当你迫不及待的想要入手开弄时，你可能会发现，这玩意下载速度实在太慢太慢了，或者更悲催的直接就下载不下来。  
对于此等悲催的体验，不想再尝试第二次，于下在我完成安装时，顺便将自己所用的版本(V1.9.4)放在了百度网盘：
https://pan.baidu.com/s/1slPjmbF  
当然，当你下载的时候，可能已经不是最新版了，如果你和我一样，实在不想再被那蜗牛般的速度所折腾，那还是将就用吧。


下载完成，一路狂飙，安装完成.  


**其它相关文件**
```
virtualbox.box
homestead
```
`virtualbox.box`是一个`VirtualBox`的镜像文件，这如我们平时在`Virtualbox`上安装系统的镜像文件一样(我姑且暂时这么认为，可能是错的哦~~)  
`vagrant`为我们提供了一套强大的工具，可以让我们免去在 `VirtualBox` 上面安装各种繁锁的过程,你可以试着点开这个链接: https://atlas.hashicorp.com/boxes/search 以及 http://www.vagrantbox.es/  
里面有各种镜像文件。  
`vagrant`添加box的语法如下:
```shell
$ vagrant box add {title} {url}
$ vagrant init {title}
$ vagrant up
```
从 https://atlas.hashicorp.com/boxes/search 中，可以找到 `laravel/homestead` 这个镜像(你不会真的去找了一遍吧)。
使用`vagrant box add`添加到本地镜像列表:
```
vagrant box add laravel/homestead
```
>当然，正当你认为一切都进行得如此顺利时，你可能会遇到和我一样的问题，那便是网速太慢下不下来，下不下来...  
>如果你已成功通过以上命令下载完成，恭喜你，可以跳过此段，以下仅为苦逼人士准备。  
>v2.1.0 版，百度网盘地址:https://pan.baidu.com/s/1hrTpjAc  
>下载完成，放本地任意位置，通过以下命令添加  
>vagrant box add laravel/homestead file://d:/box/virtualbox.box  
>听大家都说必须使用file://，但我通过相对路径貌似添加也是没有任何问题的.  

接下来，需要`clone`一份`laravel`官方提代的`homestead`
```
>git clone https://github.com/laravel/homestead.git Homestead
>cd Homestead
>init.bat #会在Homestead目录下生成Homestead.yaml文件
```
充满好奇的我，刚看到官方提供的`homestead`时，没接触这`vagrant`的我，心中也是一万头草泥马
在狂奔，一会是`VirtualBox`,一会是`Vagrant`,还有接下的`virtualbox.box`,这都什么和什么呢？

是时候搞清楚他们的之间的各种关系了。


那么，它们的之间的关系是这样的，通过`homestead`,我们配置网络、文件共享、WEB服务器等。  
当`Vagrant`通过`vagrant up`启动时，会自动加载当前目录下的`Homestead.yaml`配置文件。    
`vagrant up`成功后，实际是加载了一个`virtualbox.box`镜像文件在`VirtualBox`运行。

不知道此时，此时你是否已经能理清梦它们之间的各种关系，  
如果依旧模糊(此处你可以开骂,这写的什么JB玩意)，那我们再来理一理，我们的第一个目的是成功运行`vagrant up`
必需条件:
```
Vagrant 已安装
VirtualBox 已安装
virtualbox.box 已成功加载到本地(可以通过vagrant box list查看哦)
Homestead.yaml 配置文件未修改(默认也可以哦)
```
我相信你和我一样对`Homestead.yaml`配置文件很感兴趣.
```
---
ip: "192.168.10.10"
memory: 2048
cpus: 1
provider: virtualbox

authorize: ~/.ssh/id_rsa.pub

keys:
    - ~/.ssh/id_rsa

# 一旦建立关联，本地环境目录下虚拟机目录会自动同步
folders:
    - map: D:/laravel/5.4    # 本地开环境环境路径
      to: /home/vagrant/cike # 虚拟机上的路径

# 默认是nginx站点，你可通过此项配置多个站点.
sites:
    - map: cike.app                 # 站点名
      to: /home/vagrant/cike/public # 站点对应路径

# 数据库，此处表示新增一个cike数据库，数据库的连接信息，可以通过 ~/Homestead/scripts/create-mysql.sh 中查看
databases:
    - cike

# blackfire:
#     - id: foo
#       token: bar
#       client-id: foo
#       client-token: bar

# 端口映射,默认会映射80，22，443，3306等常用端口
# ports:
#     - send: 50000  # 本地端口
#       to: 5000     # 虚拟机中的端口
#     - send: 7777
#       to: 777
#       protocol: udp

```
配置完成，当然还有更多的配置，主要是我不会~~,准备开机:
```
vagrant up
```
> 通过本地加载镜像的，可能此处会提示找某种和镜像文件有关的错误，具体是什么不负责不作为小篇也忘了~~  
> 由于版本问题导致 Box 'laravel/homestead' couldnot befound.  
> 通过 vagrant box list 你可能会发现，本地的laravel/homestead 版本为 0   
> 在clone回来的Homestead/scripts/文件夹中，打开homestead.rb文件  
> 把 config.vm.box_version = settings["version"] ||= ">= 0.4.0" 改为 config.vm.box_version = settings["version"] ||= ">= 0"

当然你可以通过以下命令登录虚拟机:  
```
vagrant ssh
```

**Xdebug配置**
主要是在 `phpstrom` 中,添加 `server` 时,将 use path mappings选中.
并将本地项目路径、网站根目录 与 虚拟机中的路径进行关联.

**最后的话**  
我在为另一台 `Windows` 机器上配置(原已安装过`VirtualBox 5.1.x`具体版本号忘了)，  
当我遇到前面由于版本为0而修改时`homestead.rb`文件时，只要一改版本号便提示配置文件不正确，  
最后删除`Homestead`,重新`clone`了一份,通过重新`init.bat`,很好，不再报配置文件的错误了.  
但接下来，在运行
```shell
$ git up
Bringing machine 'homestead-7' up with 'virtualbox' provider...
==> homestead-7: Clearing any previously set forwarded ports...
==> homestead-7: Clearing any previously set network interfaces...
==> homestead-7: Preparing network interfaces based on configuration...
    homestead-7: Adapter 1: nat
    homestead-7: Adapter 2: hostonly
==> homestead-7: Forwarding ports...
    homestead-7: 80 (guest) => 8000 (host) (adapter 1)
    homestead-7: 443 (guest) => 44300 (host) (adapter 1)
    homestead-7: 3306 (guest) => 33060 (host) (adapter 1)
    homestead-7: 5432 (guest) => 54320 (host) (adapter 1)
    homestead-7: 8025 (guest) => 8025 (host) (adapter 1)
    homestead-7: 27017 (guest) => 27017 (host) (adapter 1)
    homestead-7: 22 (guest) => 2222 (host) (adapter 1)
==> homestead-7: Running 'pre-boot' VM customizations...
==> homestead-7: Booting VM...
此处开始报错...(由于报错时没截图，此处无法保留原具体报错信息)
```
在网找，都说是`VirtualBox`本身的问题，于是到官方下载了`VirtualBox 5.1.22 released! `，
安装后，重新`vagrant up`还是报一样的错误,这个问题整整折腾了一个晚上，没解决，直到第二天，  
特意查看了安装成功的电脑上的`VirtualBox`版本,版本号为`5.1.10 r112026 (Qt5.6.2)`，于是下载同这一个版本，  
安装后`vagrant up`,顺序跳过了`Booting VM...`,可是又卡在这个地方:
```
==> homestead-7: Booting VM...
==> homestead-7: Waiting for machine to boot. This may take a few minutes...
    homestead-7: SSH address: 127.0.0.1:2222
    homestead-7: SSH username: vagrant
    homestead-7: SSH auth method: private key
```
虽然最后跳过去了，但提示了很多警告，通过`vagrant ssh`连接不上，`127.0.0.1:8000`也无法访问，
在`virtualbox`中可以看到为`运行中`状态。  
看来，并没有真正意义上的安装成功。

众里寻它千百度，最后还是在网上找到解决方法.
打开`VirtualBox` -> 选中vagrant启动的虚拟机 -> 设置 -> 网卡1 -> 高级 -> 选中接入网线  
然后在`VirtualBox`中正常关闭虚拟机，重新 `vagrant up` 这一次，终于成功了.

### 后续
在给同事配置时启用过程卡在了下面这个步骤：
```
default: SSH auth method: private key
```
1. 遇到这个问题，打开Oracle VM,选择相关连的虚拟机，然后点菜单栏上的"显示",查看到以下结果:
```
a start job is runing for raise netwrok interfaces
```
该过程一直处于加载中，时长了，就超时了。
2. 在Oracle VM中选择正常退出系统，然后检查网络配置项中的高级选项,其中有一栏“接入网络”把它沟上，然后重试就正常了.


### 导出
找到VBOX的安装目录，执行虚拟机列表查看：
```
 ./VBoxManage.exe list vms
```
通过以下命令导出虚拟机的镜像文件:
```
vagrant package --base homestaed-7 --output ./zsjr_task.box
# --base 为要导出的镜像文件
# --output 保存路径及文件名
```
经过数分钟后，导出BOX文件，那么如何使用这个文件呢？我想继续使用homestaed中的yml配置。
```
vagrant add zsjr/task ./zsjr_task.box
```
再查看是否已导入成功:
```
vagrant box list
```
导入成功后，修改homestaemd.yml文件,新增
```
name: task
box: zsjr/task
```
修改完成后，执行启用命令:
```
vagrant up
```
如果中途出现验证私钥不通过，找到homestaed根目录`.vagrant\machines\homestaed-7\virtualbox\private_key`,
将它复制到`.vagrant\machines\task\virtualbox\private_key`则可。
